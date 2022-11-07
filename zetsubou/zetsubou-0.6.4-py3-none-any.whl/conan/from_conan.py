# pyright: reportMissingImports=false
# pylint: disable=import-error, bare-except

# This file can be imported from conan generator
# So it needs to support importing via absolute and relative packages
import os
from typing import Optional
from conans import ConanFile

try:
    from zetsubou.project.model.configuration_enums import EBaseConfiguration
    from zetsubou.project.model.runtime_library import ERuntimeLibrary
    from zetsubou.project.model.toolchain_enums import ECompilerFamily, ECppStandard
    from zetsubou.project.model.platform_enums import EArch, ESystem, EVersionSelector
    from zetsubou.project.model.platform_data import PlatformDataclass, IPlatformToolchain, ILinuxToolchain, IWindowsToolchain
    from zetsubou.utils.yaml_simple_writer import to_yaml
except:
    pass


try:
    from configuration_enums import EBaseConfiguration
    from runtime_library import ERuntimeLibrary
    from toolchain_enums import ECompilerFamily, ECppStandard
    from platform_enums import EArch, ESystem, EVersionSelector
    from platform_data import PlatformDataclass, IPlatformToolchain, ILinuxToolchain, IWindowsToolchain
    from yaml_simple_writer import to_yaml
except:
    pass


defined = lambda o: o is not None


def os_from_conan(system:str) -> Optional[ESystem]:
    return {
        'Windows' : ESystem.Windows,
        'Linux' : ESystem.Linux
    }.get(system, None)


def arch_from_conan(arch:str) -> Optional[EArch]:
    return {
        'x86' : EArch.x86,
        'x86_64' : EArch.x64
    }.get(arch, None)


def compiler_family_from_conan(compiler:str) -> Optional[ECompilerFamily]:
    return {
        'Visual Studio' : ECompilerFamily.MSVC,
        'msvc' : ECompilerFamily.MSVC,
        'gcc' : ECompilerFamily.GCC,
        'clang' : ECompilerFamily.CLANG,
    }.get(compiler, None)


def runtime_library_from_conan(runtime:str, runtime_type:str) -> Optional[ERuntimeLibrary]:
    if runtime_type == 'Debug':
        return ERuntimeLibrary.STATIC_DEBUG if runtime == 'static' else ERuntimeLibrary.DYNAMIC_DEBUG
    else:
        return ERuntimeLibrary.STATIC_RELEASE if runtime == 'static' else ERuntimeLibrary.DYNAMIC_RELEASE


def cppstd_from_conan(cppstd:str) -> Optional[ECppStandard]:
    return {
        '11' : ECppStandard.cpp11,
        '14' : ECppStandard.cpp14,
        '17' : ECppStandard.cpp17,
        '20' : ECppStandard.cpp20,
        '23' : ECppStandard.cpp23,
    }.get(cppstd, None)


def build_type_from_conan(build_type:str) -> Optional[EBaseConfiguration]:
    return {
        'Debug' : EBaseConfiguration.DEBUG,
        'Release' : EBaseConfiguration.RELEASE,
        'RelWithDebInfo' : EBaseConfiguration.RELEASE_WITH_DEBUG_INFO
    }.get(build_type, None)


def export_platform(conanfile:ConanFile, platform_filename:str) -> bool:
    plat = platform_from_conan(conanfile)
    if plat is None:
        print('Unable to setup Platform')
        return False

    compiler = toolchain_from_settings(conanfile, plat.host_system)
    if compiler is None:
        print('Unable to setup Toolchain')
        return False

    plat.toolchains = [ compiler ]

    with open(platform_filename, 'w') as out_file:
        out_file.write(to_yaml(plat))

    return True


def platform_from_conan(conanfile:ConanFile) -> Optional[PlatformDataclass]:
    arch_host = None
    arch_target = None
    arch = conanfile.settings.get_safe('arch')
    if arch is None:
        arch_host = conanfile.settings.get_safe('arch_build')
        arch_target = conanfile.settings.get_safe('arch_target')
    else:
        arch_target = arch
        arch_host = arch

    arch_host = arch_from_conan(arch_host)
    arch_target = arch_from_conan(arch_target)
    os_host = os_from_conan(conanfile.settings.get_safe('os'))

    if not defined(os_host) or not (defined(arch_target) and defined(arch_host)):
        return None

    platform = PlatformDataclass(
        platform=f"{os_host.name}_{arch_target.name}",
        host_system=os_host,
        host_arch=arch_host,
        target_arch=arch_target
    )

    return platform


def toolchain_from_settings(conanfile:ConanFile, host_os: ESystem) -> Optional[IPlatformToolchain]:
    compiler_family = compiler_family_from_conan(conanfile.settings.get_safe('compiler'))
    if compiler_family is None:
        print('Unable to discover compiler family')
        return None

    compiler_version = conanfile.settings.get_safe('compiler.version')
    if compiler_version is None:
        compiler_version = EVersionSelector.latest

    cppstd = cppstd_from_conan(conanfile.settings.get_safe('compiler.cppstd'))
    if cppstd is None:
        cppstd = ECppStandard.latest

    # if compiler_family in (ECompilerFamily.MSVC, ECompilerFamily.CLANG, ECompilerFamily.CLANG_CL):
    if host_os == ESystem.Windows:
        compiler_toolset = conanfile.settings.get_safe('compiler.toolset')
        if compiler_toolset is None:
            print('Unable to discover compiler toolset')
            return None

        return IWindowsToolchain(
            family=compiler_family,
            version=compiler_version,
            cppstd=cppstd,
            toolset=compiler_toolset
        )
    else:
        compiler_libcxx = conanfile.settings.get_safe('compiler.libcxx')
        if compiler_libcxx is None:
            print('Unable to discover compiler libcxx')
            return None

        return ILinuxToolchain(
            family=compiler_family,
            version=compiler_version,
            cppstd=cppstd,
            libcxx=compiler_libcxx
        )
