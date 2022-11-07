import os
from typing import List

from bentoudev.dataclass.yaml_loader import LineLoader

from zetsubou.commands.command_context import CommandContext
from zetsubou.project.model.platform_enums import EArch, ESystem
from zetsubou.project.model.platform import Platform
from zetsubou.project.model.toolchain import Toolchain
from zetsubou.utils.common import is_in_enum
from zetsubou.utils.error import ProjectError
from zetsubou.utils.yaml_tools import to_yaml
from zetsubou.utils import logger


def discover_toolchain_list(context: CommandContext) -> List[Toolchain] :
    system_toolchains = discover_toolchain_by_system(context.host_system, context.host_arch)

    # filter by platform
    toolchains = list(filter(lambda t: filter_toolchains_by_target_arch(t, context.project_template.platforms), system_toolchains))

    # filter by whatever is known to Conan
    user_dir = os.path.expanduser('~')
    conan_settings_path = os.path.join(user_dir, '.conan/settings.yml')

    if os.path.exists(conan_settings_path):
        with open(conan_settings_path, encoding='utf-8') as conan_settings_file:
            loader = LineLoader(conan_settings_file.read())
            loaded_yaml = loader.get_single_data()

            if context.host_system == ESystem.Windows:
                toolchains = list(filter(lambda t: filter_toolchains_by_conan_toolchain(t, loaded_yaml), toolchains))

            num_toolchains = len(toolchains)

            if num_toolchains == 0:
                logger.Error("No suitable toolchains found!")

                return None

    else:
        logger.Warning('Unable to filter toolchains by Conan settings!')

    return toolchains


def discover_toolchain_by_system(host_system: ESystem, host_arch: EArch) -> List[Toolchain] :
    if host_system == ESystem.Windows:
        from zetsubou.system.windows import windows
        return windows.discover_toolchain_list(host_arch)
    else:
        raise EnvironmentError(f'Sorry, discovering toolchains on \"{host_system.name}\" arch \"{host_arch.name}\" is not currently supported!')


def filter_toolchains_by_target_arch(toolchain:Toolchain, platforms:List[Platform]):
    for plat in platforms:
        if not is_in_enum(toolchain.arch, EArch):
            logger.Warning(f"Unknown arch '{toolchain.arch}' for toolchain '{toolchain.name}'")
            return False

        if EArch[toolchain.arch] == plat.target_arch:
            return True

    return False


def filter_toolchains_by_conan_toolchain(toolchain:Toolchain, conan_settings):
    try:
        if toolchain.Toolset in conan_settings['compiler']['Visual Studio']['toolset']:
            return True
    except Exception:
        return False
    return False
