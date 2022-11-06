#!/usr/bin/env python3
# Copyright 2022 Jason C. Nucciarone
# See LICENSE file for licensing details.

"""`setup-slurm` command for setting up SLURM inside the micro-HPC cluster."""

from __future__ import annotations

import textwrap
from typing import Optional

from craft_cli import BaseCommand


class _SetupSLURMHandler:
    ...


class SetupSLURMCommand(BaseCommand):
    """Set up SLURM authentication and configuration for micro-HPC cluster."""

    name = "setup-slurm"
    help_msg = "Set up SLURM authentication and configuration for micro-HPC cluster."
    overview = textwrap.dedent(
        """
        Set up SLURM authentication and configuration for micro-HPC cluster.

        Automatically sync the munge key and slurm configuration files amongst
        the head and compute nodes in the micro-HPC cluster.

        This command should be used after executing `hpc-workshop setup-nfs`.
        """
    )

    def run(self, _) -> Optional[int]:
        """Run steps to set up SLURM authentication and configuration."""
        ...
