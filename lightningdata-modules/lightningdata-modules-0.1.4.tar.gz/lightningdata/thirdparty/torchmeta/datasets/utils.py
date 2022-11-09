import os
import json
from typing import Optional, Tuple, Iterator


def get_asset_path(*args):
    basedir = os.path.dirname(__file__)
    return os.path.join(basedir, 'assets', *args)


def get_asset(*args, dtype=None):
    filename = get_asset_path(*args)
    if not os.path.isfile(filename):
        raise IOError('{} not found'.format(filename))

    if dtype is None:
        _, dtype = os.path.splitext(filename)
        dtype = dtype[1:]

    if dtype == 'json':
        with open(filename, 'r') as f:
            data = json.load(f)
    else:
        raise NotImplementedError()
    return data

# QKFIX: The current version of `download_file_from_google_drive` (as of torchvision==0.8.1)
# is inconsistent, and a temporary fix has been added to the bleeding-edge version of
# Torchvision. The temporary fix removes the behaviour of `_quota_exceeded`, whenever the
# quota has exceeded for the file to be downloaded. As a consequence, this means that there
# is currently no protection against exceeded quotas. If you get an integrity error in Torchmeta
# (e.g. "MiniImagenet integrity check failed" for MiniImagenet), then this means that the quota
# has exceeded for this dataset. See also: https://github.com/tristandeleu/pytorch-meta/issues/54
# 
# See also: https://github.com/pytorch/vision/issues/2992
# 
# The following functions are taken from
# https://github.com/pytorch/vision/blob/cd0268cd408d19d91f870e36fdffd031085abe13/torchvision/datasets/utils.py

from torchvision.datasets.utils import _save_response_content, check_integrity


def _quota_exceeded(response: "requests.models.Response"):
    return False
    # See https://github.com/pytorch/vision/issues/2992 for details
    # return "Google Drive - Quota exceeded" in response.text

def _extract_gdrive_api_response(response, chunk_size: int = 32 * 1024) -> Tuple[bytes, Iterator[bytes]]:
    import itertools, re
    content = response.iter_content(chunk_size)
    first_chunk = None
    # filter out keep-alive new chunks
    while not first_chunk:
        first_chunk = next(content)
    content = itertools.chain([first_chunk], content)

    try:
        match = re.search("<title>Google Drive - (?P<api_response>.+?)</title>", first_chunk.decode())
        api_response = match["api_response"] if match is not None else None
    except UnicodeDecodeError:
        api_response = None
    return api_response, content

def download_file_from_google_drive(file_id: str, root: str, filename: Optional[str] = None, md5: Optional[str] = None):
    """Download a Google Drive file from  and place it in root.
    Args:
        file_id (str): id of file to be downloaded
        root (str): Directory to place downloaded file in
        filename (str, optional): Name to save the file under. If None, use the id of the file.
        md5 (str, optional): MD5 checksum of the download. If None, do not check
    """
    # Based on https://stackoverflow.com/questions/38511444/python-download-files-from-google-drive-using-url
    import requests
    root = os.path.expanduser(root)
    if not filename:
        filename = file_id
    fpath = os.path.join(root, filename)

    os.makedirs(root, exist_ok=True)

    if check_integrity(fpath, md5):
        print(f"Using downloaded {'and verified ' if md5 else ''}file: {fpath}")
        return

    url = "https://drive.google.com/uc"
    params = dict(id=file_id, export="download")
    with requests.Session() as session:
        response = session.get(url, params=params, stream=True)

        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                token = value
                break
        else:
            api_response, content = _extract_gdrive_api_response(response)
            token = "t" if api_response == "Virus scan warning" else None

        if token is not None:
            response = session.get(url, params=dict(params, confirm=token), stream=True)
            api_response, content = _extract_gdrive_api_response(response)

        if api_response == "Quota exceeded":
            raise RuntimeError(
                f"The daily quota of the file {filename} is exceeded and it "
                f"can't be downloaded. This is a limitation of Google Drive "
                f"and can only be overcome by trying again later."
            )

        _save_response_content(content, fpath)
