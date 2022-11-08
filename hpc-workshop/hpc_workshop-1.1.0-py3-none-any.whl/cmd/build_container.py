#!/usr/bin/env python3
# Copyright 2022 Jason C. Nucciarone
# See LICENSE file for licensing details.

"""`build-container` command for building example Apptainer container."""

from __future__ import annotations

import textwrap
from typing import Optional

from craft_cli import BaseCommand


class _BuildContainerHandler:
    ...


class BuildContainerCommand(BaseCommand):
    """Build a container inside the micro-HPC cluster."""

    name = "build-container"
    help_msg = "Build a container inside the micro-HPC cluster."
    overview = textwrap.dedent(
        """
        Build a container inside the micro-HPC cluster.
        
        This command should be used after executing `setup-module`.
        """
    )

    def run(self, _) -> Optional[int]:
        """Run steps to build Apptainer container."""
        ...
