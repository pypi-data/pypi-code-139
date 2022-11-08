#!/usr/bin/env python3
# Copyright 2022 Jason C. Nucciarone
# See LICENSE file for licensing details.

"""`setup-ldap` command for setting up LDAP inside the micro-HPC cluster."""

from __future__ import annotations

import textwrap
from typing import Optional

from craft_cli import BaseCommand


class _SetupLDAPHandler:
    ...


class SetupLDAPCommand(BaseCommand):
    """Set up LDAP user and group on the micro-HPC cluster."""

    name = "setup-ldap"
    help_msg = "Set up LDAP user and group on the micro-HPC cluster."
    overview = textwrap.dedent(
        """
        Set up LDAP user and group on the micro-HPC cluster.
        
        The default user created will be named `ubuntu` and the default
        group will be `research`.
        
        This command should be used after executing `hpc-workshop init`.
        """
    )

    def run(self, _) -> Optional[int]:
        """Run steps to add user and group to the cluster."""
        ...
