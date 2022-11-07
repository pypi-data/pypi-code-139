from copy import copy
from zetsubou.commands.base_command import CommandContext
from typing import List
from zetsubou.project.model.configuration import Configuration
from zetsubou.project.model.platform_enums import EArch, ESystem
from zetsubou.project.model.platform import Platform
from zetsubou.project.model.runtime_library import ERuntimeLibrary

from zetsubou.project.model.toolchain import ECompilerFamily, ECppStandard, Toolchain


def platform_to_conan(context: CommandContext, plat : Platform) -> List[str]:
    return [
        '-s', f'os={plat.host_system.name}'
    ]


def toolchain_to_conan(context: CommandContext, toolchain: Toolchain) -> List[str]:
    if toolchain is not None:

        arch = {
            EArch.x86.name : 'x86',
            EArch.x64.name : 'x86_64'
        }.get(toolchain.arch)

        compiler = {
            ECompilerFamily.MSVC.name  : 'Visual Studio',
            ECompilerFamily.CLANG.name : 'clang',
            ECompilerFamily.GCC.name   : 'gcc'
        }.get(toolchain.CompilerFamily.name)

        result = [
            '-s', f'arch={arch}',
            '-s', f'compiler={compiler}',
        ]

        for path in toolchain.PathEnv:
            result.extend([
                '-e', f'PATH=[{path}]'
            ])

        if context.host_system == ESystem.Windows and toolchain.Toolset is not None:
            if toolchain.CompilerFamily == ECompilerFamily.MSVC:
                result.extend([
                    '-s', f'compiler.toolset={toolchain.Toolset}'
                ])
            elif toolchain.CompilerFamily == ECompilerFamily.CLANG:
                result.extend([
                    '-s', f'compiler.runtime_version={toolchain.Toolset}'
                ])

        if toolchain.CompilerFamily == ECompilerFamily.MSVC:
            result.extend([
                '-s', f'compiler.version={toolchain.ide_version.major}'
            ])
        else:
            # Remove path, conan is interested only in Major.Minor at best
            ver_no_path = copy(toolchain.version)
            ver_no_path.path = 0

            result.extend([
                '-s', f'compiler.version={ver_no_path}'
            ])

        return result

    return []


def config_base_to_conan(context: CommandContext, config: Configuration, toolchain:Toolchain) -> List[str]:
    if config is not None and toolchain is not None:

        build_type = {
            'DEBUG' : 'Debug',
            'RELEASE' : 'Release',
            'RELEASE_WITH_DEBUG_INFO' : 'RelWithDebInfo'
        }.get(config.base_configuration.name)

        result = [
            '-s', f'build_type={build_type}',
        ]

        if context.host_system == ESystem.Windows:

            if toolchain.CompilerFamily == ECompilerFamily.MSVC:
                runtime_library = {
                    ERuntimeLibrary.DYNAMIC_DEBUG.name   : 'MDd',
                    ERuntimeLibrary.DYNAMIC_RELEASE.name : 'MD',
                    ERuntimeLibrary.STATIC_DEBUG.name    : 'MTd',
                    ERuntimeLibrary.STATIC_RELEASE.name : 'MT',
                }.get(config.runtime_library.name)

                result.extend([
                    '-s', f'compiler.runtime={runtime_library}'
                ])
            elif toolchain.CompilerFamily == ECompilerFamily.CLANG:
                runtime, runtime_type = {
                    ERuntimeLibrary.DYNAMIC_DEBUG.name   : ('dynamic', 'Debug'),
                    ERuntimeLibrary.DYNAMIC_RELEASE.name : ('dynamic', 'Release'),
                    ERuntimeLibrary.STATIC_DEBUG.name    : ('static',  'Debug'),
                    ERuntimeLibrary.STATIC_RELEASE.name  : ('static',  'Release'),
                }.get(config.runtime_library.name)

                result.extend([
                    '-s', f'compiler.runtime={runtime}',
                    '-s', f'compiler.runtime_type={runtime_type}',
                ])

        return result

    return []

def cppstd_to_conan(cppstd:ECppStandard):
    cpp = {
        ECppStandard.cpp11  : '11',
        ECppStandard.cpp14  : '14',
        ECppStandard.cpp17  : '17',
        ECppStandard.cpp20  : '20',
        ECppStandard.cpp23  : '23',
        ECppStandard.latest : '23',
    }.get(cppstd)
    return [
        '-s', f"compiler.cppstd={cpp}"
    ]
