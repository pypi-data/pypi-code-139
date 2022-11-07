from typing import List, Optional, Union
from dataclasses import dataclass, field

from zetsubou.project.model.platform_enums import ESystem, EArch, EVersionSelector
from zetsubou.project.model.filter import TargetFilter
from zetsubou.project.model.target import TargetData
from zetsubou.project.model.toolchain import ECompilerFamily, ECppStandard


@dataclass
class PlatformData(TargetData):
    filter: TargetFilter = field(default_factory=TargetFilter)


@dataclass
class IPlatformToolchain:
    family: ECompilerFamily
    version: Union[EVersionSelector, List[str]]
    cppstd: ECppStandard


@dataclass
class IWindowsToolchain(IPlatformToolchain):
    toolset: Union[EVersionSelector, List[str]]


@dataclass
class ILinuxToolchain(IPlatformToolchain):
    libcxx: List[str]


@dataclass
class PlatformDataclass(TargetData):
    platform: str = None
    host_system: ESystem = None
    host_arch: EArch = None
    target_arch: EArch = None
    filters: Optional[List[PlatformData]] = field(default_factory=list)
    toolchains: List[Union[IPlatformToolchain, IWindowsToolchain, ILinuxToolchain]] = field(default_factory=list)
