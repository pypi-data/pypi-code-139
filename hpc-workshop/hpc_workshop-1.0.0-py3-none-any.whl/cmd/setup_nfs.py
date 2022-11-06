#!/usr/bin/env python3
# Copyright 2022 Jason C. Nucciarone
# See LICENSE file for licensing details.

"""`setup-nfs` command for setting up NFS inside the micro-HPC cluster."""

from __future__ import annotations

import textwrap
from typing import Optional

from craft_cli import BaseCommand


class _SetupNFSHandler:
    ...


class SetupNFSCommand(BaseCommand):
    """Set up NFS mounts for micro-HPC cluster."""

    name = "setup-nfs"
    help_msg = "Set up NFS mounts for micro-HPC cluster."
    overview = textwrap.dedent(
        """
        Set up NFS mounts for micro-HPC cluster.
        
        Automatically mount instances to share information between nodes.
        
        This command should be used after executing `hpc-workshop setup-ldap`.
        """
    )

    def run(self, _) -> Optional[int]:
        """Run steps to mount NFS on the nodes."""
        ...
