#!/usr/bin/env python3
# Copyright 2022 Jason C. Nucciarone
# See LICENSE file for licensing details.

"""`setup-module` command for setting up the Lua module file needed to access Apptainer."""

from __future__ import annotations

import textwrap
from typing import Optional

from craft_cli import BaseCommand


class _SetupModuleHandler:
    ...


class SetupModuleCommand(BaseCommand):
    """Set up access to Apptainer via a Lua module file."""

    name = "setup-module"
    help_msg = "Set up access to Apptainer via a Lua module file."
    overview = textwrap.dedent(
        """
        Set up access to Apptainer via a Lua module file.
        
        This will allow users to load Apptainer inside their computing environment.
        
        This command should be used after executing `hpc-workshop setup-slurm`.
        """
    )

    def run(self, _) -> Optional[int]:
        """Run steps to set up Apptainer module file."""
        ...
