import pathlib
import re
import typing
from datetime import datetime

import pydantic

from . import hashing
from .settings import get_settings

_content_name_regex: re.Pattern = re.compile(r"^((?!(\/{2,})|(\/$)|(^\/)).)*$")

_tag_regex: re.Pattern = re.compile(r"^[\w\-.]{1,30}$")


class PackageContent(pydantic.BaseModel):
    is_directory: bool = False
    name: str
    hash_value: str = None

    @pydantic.validator("name")
    def validate_name(cls, v: str):
        if not _content_name_regex.match(v):
            raise ValueError(f"invalid name format: {v}")
        return v

    @pydantic.validator("hash_value")
    def validate_hash_value(cls, v: str):
        if v:
            try:
                v, _, _ = hashing.verify_hash(v)
            except hashing.exceptions.HashException as e:
                raise ValueError() from e
        return v

    @pydantic.root_validator(skip_on_failure=True)
    def validate_dir_hash(cls, values):
        if not (values["is_directory"] ^ bool(values["hash_value"])):
            raise ValueError(
                f"hash value {'not' if not values['is_directory'] else ''}present for a {'directory' if values['is_directory'] else 'file'}."
            )
        return values


class Package(pydantic.BaseModel):
    hash_value: str = None
    created_at: datetime = datetime.now()
    contents: typing.List[PackageContent]

    @pydantic.validator("contents")
    def validate_contents(cls, v: typing.List[PackageContent]):
        v.sort(key=lambda x: (x.name, x.is_directory))
        return v

    @pydantic.root_validator(skip_on_failure=True)
    def validate_hash_value(cls, values):
        hash_algo = get_settings().allowed_hashes[0]
        if values["hash_value"]:
            try:
                _, provided_algo, _ = hashing.verify_hash(values["hash_value"])
                hash_algo = provided_algo
            except hashing.exceptions.HashException as e:
                raise ValueError from e

        hasher = hashing.get_hasher(hash_algo)

        for content in values["contents"]:
            hasher.update(content.name.encode())
            if not content.is_directory:
                hasher.update(content.hash_value.encode())

        computed_hash_value = hashing.write_hash(hasher)

        if values["hash_value"] and values["hash_value"] != computed_hash_value:
            raise ValueError("hash value of package is incorrect.")

        values["hash_value"] = computed_hash_value

        return values

    class Config:
        arbitrary_types_allowed = True


class PackageTag(pydantic.BaseModel):
    name: str
    tag: str
    package_hash_value: str

    @pydantic.validator("name")
    def validate_name(cls, v: str):
        if not _tag_regex.match(v):
            raise ValueError("only ~30 chars in [A-Za-z0-9-_.] are allowed")
        return v

    @pydantic.validator("tag")
    def validate_tag(cls, v: str):
        if not _tag_regex.match(v):
            raise ValueError("only ~30 chars in [A-Za-z0-9-_.] are allowed")
        return v

    @pydantic.validator("package_hash_value")
    def validate_package_hash_value(cls, v: str):
        try:
            v, _, _ = hashing.verify_hash(v)
        except hashing.exceptions.HashException as e:
            raise ValueError() from e
        return v


def process_directory(directory: pathlib.Path) -> typing.List[PackageContent]:
    if not directory.exists():
        raise OSError(f"{directory} does not exist.")
    if not directory.is_dir():
        raise NotADirectoryError(f"{directory} is not a directory.")

    contents: typing.List[PackageContent] = list()
    for path in directory.rglob("*"):
        if path.is_dir():
            foldername = path.relative_to(directory)
            content = PackageContent(name=str(foldername), is_directory=True)
            contents.append(content)
        elif path.is_file():
            hash_value = hashing.compute_hash_file(path)
            filename = path.relative_to(directory)
            content = PackageContent(name=str(filename), hash_value=hash_value)
            contents.append(content)

    contents.sort(key=lambda x: (x.name, x.is_directory))

    return contents
