from genericpath import isfile
import pytest
from pathlib import PosixPath
from easyfs.file import File
from easyfs.directory import Directory
import os


def test_dir_composing() -> None:

    mydir = Directory()
    my_file =  File(b"hio")
    mydir["dir/file"] =     my_file 


    root = Directory()  # default
    root["root"] = mydir

    assert {"root/dir/file":my_file} == root.as_dict()


def test_dir_metadata_retention() -> None:

    mydir = Directory(metadata="hi")
    my_file =  File(b"hio")
    mydir["dir/file"] =     my_file 


    root = Directory()  # default
    root["root"] = mydir

    assert {"root/dir/file":my_file} == root.as_dict()
    assert root["root"].metadata == "hi"


def test_file_no_overdride() -> None:
    mydir = Directory(allow_override=False)
    mydir["file"] = File(b"hio")
    with pytest.raises(Exception):
        mydir["file"] = File(b"hio")


def test_dir_composing_no_overdride() -> None:
    mydir = Directory({"dir/file": File(b"hio")})
    with pytest.raises(Exception):
        Directory({"dir/file": File(b"fuuu"), ".": mydir}, allow_override=False)


def test_access() -> None:
    root = Directory()
    my_file = File(b"hio")
    root["mydir/myfile"] =my_file
    assert isinstance(root["mydir/myfile"], File)

    assert isinstance(root["mydir"], Directory)

    assert {"myfile": my_file} == root["mydir"].as_dict()



def test_create(tmp_path: PosixPath):
    root = Directory()
    root["mydir/myfile"] = File(b"hio")
    root.create(tmp_path.as_posix())

    assert os.path.exists(os.path.join(tmp_path, "mydir"))
    assert os.path.isdir(os.path.join(tmp_path, "mydir"))
    assert os.path.exists(os.path.join(tmp_path, "mydir", "myfile"))
    assert os.path.isfile(os.path.join(tmp_path, "mydir", "myfile"))


def test_from_local(tmp_path: PosixPath):
    content = b"hello-world"
    with open(os.path.join(tmp_path, "tempfile.txt"), "wb") as f:
        f.write(content)

    root = Directory.from_local(tmp_path.as_posix())
    tempfile_obj =  root.as_dict()["tempfile.txt"]
    assert isinstance(tempfile_obj, File)
    assert tempfile_obj.content == content


def test_from_cookiecutter():
    root = Directory.from_cookiecutter(
        template="https://github.com/danielbraun-org/lib-devops",
        directory="cookiecutter/minimal",
    )
    assert "cookiecutter_pypackage_minimal/.gitignore" in root.as_dict()
    assert "cookiecutter_pypackage_minimal/pyproject.toml" in root.as_dict()
