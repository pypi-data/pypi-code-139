import hashlib
import pathlib
import re
from typing import List

import pydantic

_git_repo_regex = re.compile(
    r"((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(/)?"
)


class Settings(pydantic.BaseSettings):
    allowed_hashes: List[str] = ["sha512", "blake2b"]

    chunk_size: int = 2**16

    data_path: str = "~/.perso.vcs/"

    metadata_git: str = "https://git.estsoft.com/hunet-ai/perso-vcs-metadata.git"

    @pydantic.validator("allowed_hashes")
    def validate_settings_allowed_hashes(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError(f"allowed_hashes should not be empty.")
        for hash_algo in v:
            if hash_algo not in hashlib.algorithms_guaranteed:
                raise ValueError(f"{hash_algo} not avalible on this platform")
        return v

    @pydantic.validator("data_path")
    def validate_settings_data_path(cls, v: str) -> str:
        pathlib.Path(v).expanduser().resolve().mkdir(exist_ok=True)
        return v

    @pydantic.validator("metadata_git")
    def validate_settings_metadata_git(cls, v: str) -> str:
        if not _git_repo_regex.match(v):
            raise ValueError("invalid git repo address.")
        return v

    class Config:
        allow_mutation = False


_init_done = False
_settings = Settings()


def perso_vcs_init():
    global _init_done
    _init_done = True


def get_settings():
    if not _init_done:
        raise RuntimeError("please init() before using the module.")
    return _settings


def set_settings(settings: Settings):
    if _init_done:
        raise RuntimeError("can't set settings after init is done.")
    global _settings
    _settings = settings
