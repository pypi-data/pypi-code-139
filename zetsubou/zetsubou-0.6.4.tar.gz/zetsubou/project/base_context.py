from dataclasses import dataclass
from fs.base import FS
from zetsubou.project.model.platform_enums import ESystem, EArch


@dataclass
class BaseContext:
    host_system: ESystem = 0
    host_arch: EArch = 0
    fs_root: str = ''
    fs_venv: str = ''
    project_fs: FS = ''
    project_file: str = ''
