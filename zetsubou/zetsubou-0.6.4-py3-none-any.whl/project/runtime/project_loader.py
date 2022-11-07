from dataclasses import dataclass
from typing import List, Optional
import importlib_resources as resources

import fs
import os
from fs.base import FS
from zetsubou.project.model.configuration_enums import EBaseConfiguration
from zetsubou.project.model.config_string import EDefaultConfigSlots
from zetsubou.project.model.configuration import Configuration
from zetsubou.project.model.kind import ETargetKind
from zetsubou.project.model.platform import Platform
from zetsubou.project.model.project_template import Project
from zetsubou.project.model.rule import Rule
from zetsubou.project.model.target import Dependencies, Target, TargetReference
from zetsubou.project.model.toolchain import ECppStandard, ICompiler, Toolchain, get_compiler_by_family
from zetsubou.utils import logger, yaml_loader
from zetsubou.utils.common import fix_path, null_or_empty
from zetsubou.utils.error import ProjectError

import bentoudev.dataclass.base as base


class NoTraceError(Exception):
    pass


def foreach(list, fn):
    if list is None:
        return
    if len(list) == 0:
        return
    for element in list:
        fn(element)


def find_target(targets: List[Target], name: str) -> Optional[Target]:
    for target in targets:
        if target.target == name:
            return target
    return None


class ValidationContext:
    error_format: base.EErrorFormat


def resolve_target_references(ctx:ValidationContext, targets: List[Target], deps: Optional[List[TargetReference]]) -> List[TargetReference]:
    failed_refs = []
    if deps:
        for ref in deps:
            found_target = find_target(targets, ref.name)
            if found_target is None:
                failed_refs.append(ref)
            else:
                ref.target = found_target
    return failed_refs


def validate_duplicates(ctx:ValidationContext, targets: List[Target]):
    visited = dict()
    for target in targets:
        if target.target in visited:
            tmp_msg = target.format_field_message('target', 'error', f"Duplicated target name '{target.target}'!", ctx.error_format)
            err_msg = f"{tmp_msg}\n'{visited[target.target].format_field_message('target', '', 'Second', ctx.error_format)}'"
            raise ProjectError(err_msg)
        else:
            visited[target.target] = target


def validate_cyclic_dependency(ctx:ValidationContext, targets: List[Target]):
    visited = dict()

    def visit_target(in_target):
        nonlocal visited

        target = in_target

        if isinstance(in_target, TargetReference):
            target = in_target.target

        if target.target in visited:
            target_path = []
            msg = []

            for path_element, path_ref in visited.items():
                target_path.append(path_element)
                target_path.append(' -> ')

                if isinstance(path_ref, TargetReference):
                    msg.append(path_ref.format_message('', '\nReferenced here', ctx.error_format))
                    msg.append('\n')

            target_path.append(f'{target.target}')

            path_msg = ''.join(target_path)
            ref_msg = ''.join(msg)

            main_msg = in_target.format_message('error', f"Cyclic dependency to target '{target.target}' through '{path_msg}'", ctx.error_format)
            err_msg = f'{main_msg}\n{ref_msg}'
            raise ProjectError(err_msg)

        def visit_dependencies(t: Target, d: Dependencies):
            foreach(d.interface, visit_target)
            foreach(d.public, visit_target)
            foreach(d.private, visit_target)

        visited[target.target] = in_target

        if target.dependencies is not None:
            visit_dependencies(target, target.dependencies)

        if target.filters is not None:
            for f in target.filters:
                if f.dependencies is not None:
                    visit_dependencies(target, f.dependencies)

        del visited[target.target]

    for target in targets:
        visit_target(target)


def resolve_target_dependencies(ctx:ValidationContext, target_name: str, dependencies, targets: List[Target]):
    if dependencies is not None:
        for name, dep_list in {
            'interface': dependencies.interface,
            'public': dependencies.public,
            'private': dependencies.private
        }.items():

            failed_refs = resolve_target_references(ctx, targets, dep_list)

            if len(failed_refs) > 0:
                msg = ''
                for failed_ref in failed_refs:
                    msg += failed_ref.format_message('error', f"\nUnknown target '{failed_ref.name}'", ctx.error_format)

                raise ProjectError(
                    f'Reference to undefined targets in \'{name}\' dependencies of target \'{target_name}\'{msg}')


def resolve_targets_dependencies(ctx:ValidationContext, targets: List[Target]):
    for target in targets:
        resolve_target_dependencies(ctx, target.target, target.dependencies, targets)
        for f in target.filters:
            resolve_target_dependencies(ctx, target.target, f.dependencies, targets)


def validate_targets_not_empty(ctx:ValidationContext, targets: List[Target]):
    if (len(targets)) == 0:
        raise ProjectError("Cannot load project with no targets!")


def validate_unresolved_targets(ctx:ValidationContext, targets: List[Target]):
    validate_targets_not_empty(ctx, targets)


def validate_targets(ctx:ValidationContext, targets : List[Target]):
    validate_unresolved_targets(ctx, targets)
    resolve_targets_dependencies(ctx, targets)
    validate_duplicates(ctx, targets)
    validate_cyclic_dependency(ctx, targets)


##########################################################################


def validate_compiler_duplicates(ctx:ValidationContext, platforms : List[Platform]):
    for plat in platforms:
        compiler_families = dict()
        for tool_filter in plat.toolchains:
            if tool_filter.family in compiler_families:
                first_occur = compiler_families[tool_filter.family].format_field_message('family', '', 'First referenced here', ctx.error_format)
                msg = tool_filter.format_field_message(
                    'family',
                    'error',
                    f"Duplicated toolchain definition for '{tool_filter.family.name}'.\n{first_occur}", ctx.error_format)
                raise ProjectError(msg)
            else:
                compiler_families[tool_filter.family] = tool_filter


def validate_cpp_standard(ctx:ValidationContext, platforms : List[Platform]):
    def built_supported_values(compiler_t:ICompiler):
        all_values = ECppStandard.__members__.items()
        allowed_values = []
        for value in all_values:
            if compiler_t.cpp_to_str(value[1]) is not None:
                allowed_values.append(value[0])
        return allowed_values

    for plat in platforms:
        for tool_filter in plat.toolchains:
            compiler_t = get_compiler_by_family(tool_filter.family)
            if compiler_t.cpp_to_str(tool_filter.cppstd) is None:
                msg = tool_filter.format_field_message(
                        'cppstd',
                        'error',
                        f"Unsupported C++ version '{tool_filter.cppstd.name}' for compiler family '{tool_filter.family.name}'.\n"
                        f"Supported are: {', '.join(built_supported_values(compiler_t))}",
                        ctx.error_format)
                raise ProjectError(msg)


def validate_platforms(ctx:ValidationContext, platforms : List[Platform]):
    validate_compiler_duplicates(ctx, platforms)
    validate_cpp_standard(ctx, platforms)


##########################################################################


@dataclass
class ExternalConfig:
    platform_file: Optional[str] = None
    base_config: Optional[EBaseConfiguration] = None


@dataclass
class ProjectTemplate:
    project: Project
    platforms: List[Platform]
    toolchains: List[Toolchain]
    configurations: List[Configuration]
    rules: List[Rule]
    targets: List[Target]

    def find_target(self, name:str):
        return find_target(self.targets, name)

    def find_platform(self, name : str):
        for plat in self.platforms:
            if plat.platform == name:
                return plat
        return None

    def find_config(self, name : str):
        for conf in self.configurations:
            if conf.configuration == name:
                return conf
        return None

    def find_toolchain(self, name: str):
        for tool in self.toolchains:
            if name == tool.name:
                return tool
        return None

    def list_configurations(self):
        result = []
        for conf in self.configurations:
            result.append(conf.configuration)
        return result

    def list_platforms(self):
        result = []
        for plat in self.platforms:
            result.append(plat.platform)
        return result

    def list_toolchain(self):
        result = []
        for tool in self.toolchains:
            result.append(tool.name)
        return result

    def slot_values(self):
        result = {
            EDefaultConfigSlots.platform.name : self.list_platforms(),
            EDefaultConfigSlots.configuration.name : self.list_configurations(),
            EDefaultConfigSlots.toolchain.name : self.list_toolchain()
        }

        for option in self.project.options:
            result[option.name] = option.values

        return result

    @staticmethod
    def compile_target_variant_name(kind: ETargetKind, name: str, config_string: str = ''):
        parts = []

        if kind != ETargetKind.INVALID:
            parts.append(f'{name}_{kind.name}')
        else:
            parts.append(name)

        if not null_or_empty(config_string):
            parts.append(config_string)

        return '-'.join(parts)

    @staticmethod
    def decompose_variant_name(variant:str, template_str:str):
        parts = variant.split('-')
        target = parts[0]
        config_parts = parts[1:]

        slots = template_str.split('-')

        if len(config_parts) != len(slots):
            return None, None

        result = {}
        for slot, val in zip(slots, config_parts):
            slot_name = slot.strip('}{')
            result[slot_name] = val

        return target, result


def resolve_venv(project_fs : FS, proj : Project, proj_path : str):
    if proj.config.venv == '':
        env_dir = ''
        for path in project_fs.walk.files(filter=['activate.*']):
            env_dir = fs.path.dirname(path)
            if env_dir.startswith('/'):
                env_dir = env_dir[1:]

        if env_dir == '':
            proj_yml_path = proj.get_loaded_from_file()
            logger.CriticalError('Virtual environment not found! \n'
                f" Please, either set path to config.venv in {proj_yml_path}, run 'zetsubou install' command, or place activate.bat in one of the project subdirectories ")
            return None

        return env_dir

    else:
        venv = os.path.abspath(os.path.join(proj_path, proj.config.venv))

        if os.path.exists(venv) and os.path.isdir(venv):
            def walk_for_env(search_root : str) -> Optional[str]:
                for root, _, files in os.walk(search_root):
                    for file in files:
                        if file.find('activate.') != -1:
                            return root
                return None

            venv = walk_for_env(venv)

        if venv is None:
            raise ProjectError(
                f"Virtual environment not found! Path '{proj.config.venv}' doesnt exist or is not a directory!\n"
                f'{proj.config.format_field_message("venv")}')
        else:
            return venv


def load_dataclass_list(clazz: type, obj_ref_list: Optional[List[str]], proj_dir : str, project_fs : FS, loader, local_types):
    result = []

    if obj_ref_list is not None and len(obj_ref_list) > 0:

        for obj_ref in obj_ref_list:
            obj_path = fs.path.join(proj_dir, obj_ref)

            if not project_fs.exists(obj_path) or not project_fs.isfile(obj_path):
                raise ProjectError(f"Unknown to locate file '{obj_path}'")

            with project_fs.open(obj_path, 'r', encoding='utf-8') as obj_file:
                obj_templ = loader.load_dataclass(clazz, obj_path, obj_file.read(), local_types)

                if obj_templ is not None:
                    if not base.is_loaded_from_file(obj_templ):
                        raise ProjectError(f"Unable to load class '{type(obj_templ)}' from file, missing attribute 'loadable_from_file'!")

                    if logger.IsVisible(logger.ELogLevel.Verbose):
                        logger.Success(f"Loaded [{clazz.__name__}] '{obj_path}'")

                    obj_templ.set_loaded_from_file(obj_path)
                    result.append(obj_templ)
                else:
                    raise NoTraceError()

    return result


def load_bundled_rules(loader, local_types) -> List[Rule]:
    result = []
    for res_path in [ 'MsvcRules.yml', 'ClangRules.yml' ]:
        res_content = resources.files('zetsubou.data.rules').joinpath(res_path).read_text()
        obj_templ = loader.load_dataclass(Rule, res_path, res_content, local_types)

        if obj_templ is not None:
            if not base.is_loaded_from_file(obj_templ):
                raise ProjectError(f"Unable to load class '{type(obj_templ)}' from file, missing attribute 'loadable_from_file'!")

            if logger.IsVisible(logger.ELogLevel.Verbose):
                logger.Success(f"Loaded [Rule] '{res_path}'")

            obj_templ.set_loaded_from_file(res_path)
            result.append(obj_templ)
    return result


def load_project_template(project_fs: FS, fs_root : str, filename: str, proj_file_content: str, *, loader=yaml_loader.YamlDataclassLoader(), external_config:Optional[ExternalConfig]=None) -> Optional[ProjectTemplate]:
    try:
        local_types = base.get_types_from_modules([__name__, 'zetsubou.project.model.target'])

        proj_dir = os.path.dirname(filename)
        proj_templ: Project = loader.load_dataclass(Project, filename, proj_file_content, local_types)
        if proj_templ is None:
            return

        proj_templ.set_loaded_from_file(filename)

        # TODO validate config string in proj

        # First load targets, resolve references and report undefined ones, validate for cyclic dependency
        targets = load_dataclass_list(Target, proj_templ.targets, proj_dir, project_fs, loader, local_types)

        proj = ProjectTemplate(
            project=proj_templ,
            platforms=[],
            toolchains=[],
            configurations=load_dataclass_list(Configuration, proj_templ.config.configurations, proj_dir, project_fs, loader, local_types),
            rules=load_dataclass_list(Rule, proj_templ.config.rules, proj_dir, project_fs, loader, local_types),
            targets=targets,
        )

        # External platform
        if external_config is None or external_config.platform_file is None:
            proj.platforms = load_dataclass_list(Platform, proj_templ.config.platforms, proj_dir, project_fs, loader, local_types)
        else:
            proj.platforms = load_dataclass_list(Platform, [ external_config.platform_file ], proj_dir, project_fs, loader, local_types)

        # Filter by config
        if external_config is not None and external_config.base_config is not None:
            def is_from_base(config:Configuration):
                return config.base_configuration == external_config.base_config

            proj.configurations = list(filter(is_from_base, proj.configurations))
            if len(proj.configurations) == 0:
                raise ProjectError(f"No configurations of base type '{external_config.base_config}' found!")
            else:
                proj.configurations = [ proj.configurations[0] ]

        proj.rules += load_bundled_rules(loader, local_types)

        return proj

    except NoTraceError:
        logger.CriticalError(f'Failed to load project \'{filename}\'')
        return None

    except base.DataclassLoadError as error:
        logger.Error(error)
        logger.CriticalError(f'Failed to load project \'{filename}\'')
        return None

    except ProjectError as error:
        logger.Error(error)
        logger.CriticalError(f'Failed to load project \'{filename}\'')
        return None

    except Exception as error:
        logger.Exception(error)
        logger.CriticalError(f'Failed to load project  \'{filename}\'')
        return None


def load_project_from_file(project_fs: FS, fs_root : str, filename: str, *, external_config:Optional[ExternalConfig]=None) -> Optional[ProjectTemplate]:
    if not project_fs.exists(filename):
        logger.CriticalError(f"Unable to locate file '{filename}'")
        return None
    with project_fs.open(filename, 'r', encoding='utf-8') as proj_file:
        return load_project_template(project_fs, fs_root, filename, proj_file.read(), external_config=external_config)
