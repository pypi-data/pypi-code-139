from typing import List, Dict
from zetsubou.project.model.platform_enums import EVersionSelector
from zetsubou.project.model.platform_data import IWindowsToolchain
from zetsubou.project.model.toolchain import ECompilerFamily, Toolchain
from zetsubou.project.runtime.project_loader import ProjectTemplate
from zetsubou.utils.common import Version


def is_second_newer_toolchain(first:Toolchain, second:Toolchain) -> bool:
    if first.CompilerFamily == ECompilerFamily.MSVC:
        if first.ide_version < second.ide_version:
            return True

    return first.version < second.version


# MSVC entries needs to check against IDE version :<
def is_matching_compiler_version(toolchain:Toolchain, versions:List[str]) -> bool:
    if toolchain.CompilerFamily == ECompilerFamily.MSVC:
        if str(toolchain.ide_version.major) in versions:
            return True
    else:
        if str(toolchain.version.major) in versions:
            return True


def get_toolchains_per_platform(project_template: ProjectTemplate) -> Dict[str, List[str]]:
    result = {}

    for platform in project_template.platforms:
        compatible_toolchains = set()

        for tool_filter in platform.toolchains:
            latest_by_compiler : Toolchain = None
            latest_by_toolset : Toolchain = None

            filter_by_toolset = isinstance(tool_filter, IWindowsToolchain)

            for tool_entry in project_template.toolchains:
                if tool_entry.CompilerFamily != tool_filter.family:
                    continue # Family mismatch

                if tool_filter.version == EVersionSelector.latest:
                    if latest_by_compiler is None:
                        latest_by_compiler = tool_entry
                    elif is_second_newer_toolchain(latest_by_compiler, tool_entry):
                        latest_by_compiler = tool_entry
                    continue

                elif tool_filter.version != EVersionSelector.all and not is_matching_compiler_version(tool_entry, tool_filter.version):
                    continue # Version mismatch

                if filter_by_toolset:
                    if tool_filter.toolset == EVersionSelector.latest:
                        if latest_by_toolset is None:
                            latest_by_toolset = tool_entry
                        elif latest_by_toolset.Toolset < tool_entry.Toolset:
                            latest_by_toolset = tool_entry
                        continue

                    elif tool_filter.toolset != EVersionSelector.all and tool_entry.Toolset not in tool_filter.toolset:
                        continue # Version mismatch

                compatible_toolchains.add(tool_entry)

            if latest_by_compiler is not None:
                compatible_toolchains.add(latest_by_compiler)

            if latest_by_toolset is not None:
                compatible_toolchains.add(latest_by_toolset)

        # --

        result[platform.platform] = [ t.name for t in compatible_toolchains]

    return result
