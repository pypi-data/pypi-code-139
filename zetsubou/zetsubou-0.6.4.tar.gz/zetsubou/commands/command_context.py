import os
from dataclasses import dataclass, field
from typing import List, Optional, Any
from fs.base import FS

from zetsubou.commands.execute_stage import execute_stage
from zetsubou.utils import logger
from zetsubou.utils.common import null_or_empty, fix_path
from zetsubou.project.config_matrix import ConfigMatrix
from zetsubou.project.base_context import BaseContext
from zetsubou.project.model.target import Target
from zetsubou.project.model.toolchain import Toolchain
from zetsubou.project.runtime.resolve import ResolvedTarget
from zetsubou.project.runtime.project_loader import ProjectTemplate, resolve_venv
from zetsubou.utils.error_codes import EErrorCode

@dataclass
class Fastbuild:
    emit_fs : FS
    bff_dir : str
    bff_file : str


@dataclass
class Conan:
    yml_files: List[str] = field(default_factory=list)
    dependencies: List[Target] = field(default_factory=list)
    resolved_targets: List[ResolvedTarget] = field(default_factory=list)


@dataclass
class CommandContext(BaseContext):
    command_args: Any = None

    project_template: Optional[ProjectTemplate] = None
    toolchains: List[Toolchain] = field(default_factory=list)
    config_matrix: Optional[ConfigMatrix] = None
    resolved_targets: List[ResolvedTarget] = field(default_factory=list)
    fastbuild: Optional[Fastbuild] = None
    conan: Conan = field(default_factory=Conan)

    def to_out_path(self, path : str):
        return fix_path(os.path.join(self.fs_root, path))

    def resolve_venv(self):
        if null_or_empty(self.fs_venv):
            venv_path = execute_stage(lambda: resolve_venv(self.project_fs, self.project_template.project, self.fs_root),
                                        'Virtual environemnt found',
                                        EErrorCode.UNABLE_TO_FIND_VENV)

            logger.Info(f"Virtual environement - '{venv_path}'")
            self.fs_venv = fix_path(venv_path)
