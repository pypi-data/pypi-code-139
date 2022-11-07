"""

    """

from dataclasses import dataclass
from pathlib import Path


class Conf :
    def_fn = Path('conf.json')
    repo_url = 'repo_url'
    python_version = 'python_version'
    module_2_run = "module_2_run"
    rm_venv = 'rm_venv'

@dataclass
class UserRepo :
    user_name: str
    repo_name: str
    user_slash_repo: str
    user_und_repo: str
