#!/usr/bin/env python3
# Copyright 2022 Jason C. Nucciarone
# See LICENSE file for licensing details.

"""`spack-install` command for installing a Spack package on the cluster."""

from __future__ import annotations

import textwrap
from typing import Optional

from craft_cli import BaseCommand


class _SpackInstallHandler:
    ...


class SpackInstallCommand(BaseCommand):
    """Install a spack package on the micro-HPC cluster."""

    name = "spack-install"
    help_msg = "Install a spack package on the micro-HPC cluster."
    overview = textwrap.dedent(
        """
        Install a spack package on the micro-HPC cluster.
        
        This command should be run after executing `build-container`.
        """
    )

    def run(self, parsed_args) -> Optional[int]:
        """Run steps to install Spack package on micro-HPC cluster."""
        ...
