# pyright: reportMissingImports=false
# pylint: disable=import-error, bare-except
from conans.model import Generator
from conans import ConanFile
import os

toolchain_available:bool = False
try:
    import from_conan
    toolchain_available = True
except Exception as ex:
    print("Failed to import 'from_conan'")


def emit_list(lst):
    return '\n       - '.join(lst)


def emit_property(out, prop, tmpl):
    if prop is not None and len(prop) > 0:
        out.append(tmpl.format(data = emit_list(prop)))


def fix_no_ext(libs, paths):
    results = []
    for path in paths:
        for _, _, filenames in os.walk(path):
            for file in filenames:
                for lib in libs:
                    if file.find(lib) != -1:
                        results.append(os.path.basename(file))
    return results


class _toolchain(object):
    project_file: str
    conanfile: ConanFile
    platform_file = None

    def platform_filename(self, install_dir:str):
        return os.path.join(install_dir, 'conan_platform.yml')

    def init(self, conanfile:ConanFile, project_file:str="project.yml"):
        self.conanfile = conanfile
        self.project_file = project_file

    def configure(self):
        if not self.conanfile:
            raise ValueError('Zetsubou not initialized! call self.zetsubou.init(self) before using!')

        if toolchain_available:
            plat_file = self.platform_filename(self.conanfile.folders.base_install)
            if not from_conan.export_platform(self.conanfile, plat_file):
                self.conanfile.output.error('Unable to generate platform file!')
                return

            build_type = self.conanfile.settings.get_safe('build_type')
            self.conanfile.run(f'zetsubou config {self.project_file} --platform={plat_file} --base_config={build_type} --nologo --ide')

    def build(self):
        if not self.conanfile:
            raise ValueError('Zetsubou not initialized! call self.zetsubou.init(self) before using!')

        plat_file = self.platform_filename(self.conanfile.folders.base_install)
        build_type = self.conanfile.settings.get_safe('build_type')

        self.conanfile.run(f'zetsubou build {self.project_file} --platform={plat_file} --base_config={build_type} --nologo --ide')


class ZetsubouBase(object):
    _zetsubou: _toolchain = _toolchain()

    @property
    def zetsubou(self):
        if self._zetsubou is None:
            print("Zetsubou not initialized!")
        return self._zetsubou


class zetsubou_multi(Generator):
    @property
    def filename(self):
        pass

    @property
    def content(self):
        result = {}

        for dep_name, dep_cpp_info in self.deps_build_info.dependencies:
            sections = []
            emit_property(sections, dep_cpp_info.include_paths,
                '    includes:\n'
                '       interface:\n'
                '       - {data}\n')

            emit_property(sections, dep_cpp_info.defines,
                '    defines:\n'
                '       interface:\n'
                '       - {data}\n')

            emit_property(sections, dep_cpp_info.cppflags,
                '    compiler_flags:\n'
                '       interface:\n'
                '       - {data}\n')

            emit_property(sections, fix_no_ext(dep_cpp_info.libs, dep_cpp_info.lib_paths),
                '    link_libraries:\n'
                '       interface:\n'
                '       - {data}\n')

            emit_property(sections, dep_cpp_info.lib_paths,
                '    linker_paths:\n'
                '       interface:\n'
                '       - {data}\n')

            emit_property(sections, dep_cpp_info.sharedlinkflags + dep_cpp_info.exelinkflags,
                '    linker_flags:\n'
                '       interface:\n'
                '       - {data}\n')

            dep_name = dep_name.replace("-", "_")
            result[f'{dep_name}.part.yml'] = ''.join(sections)

        # result['conan_multi.txt'] = '\n'.join([ name for name, _ in self.deps_build_info.dependencies ])

        return result


class ZetsubouGeneratorPackage(ConanFile):
    name = "zetsubougen"
    version = "0.6.4"
    license = "MIT"
    description = 'Zetsubou yml files generator'
    url = "https://github.com/BentouDev/Zetsubou"
    exports = [
        "*",
        "../from_conan.py",
         "../../project/model/platform_data.py",
         "../../project/model/platform_enums.py",
         "../../project/model/configuration_enums.py",
         "../../project/model/toolchain_enums.py",
         "../../project/model/runtime_library.py",
         "../../project/model/kind.py",
         "../../utils/yaml_simple_writer.py",
    ]

    def build(self):
        pass

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []
