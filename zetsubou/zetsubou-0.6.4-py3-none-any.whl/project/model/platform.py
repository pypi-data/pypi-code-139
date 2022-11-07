from dataclasses import dataclass

from zetsubou.project.model.platform_data import PlatformDataclass
from bentoudev.dataclass.base import loaded_from_file


@dataclass
@loaded_from_file
class Platform(PlatformDataclass):
    pass
