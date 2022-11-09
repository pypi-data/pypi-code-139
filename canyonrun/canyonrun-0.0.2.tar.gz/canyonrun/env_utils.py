import sys
import glob
import numpy as np
from pathlib import Path
import subprocess

from mlagents_envs import logging_util


# def get_commit_hash(file_name):
#     """Return commit hash associated with file name.
#
#     If file is named file_hash, returns hash. If there are no underscores in the file name, raises ValueError.
#     """
#     underscore_index = file_name.rfind("_")
#
#     # no underscores
#     if underscore_index == -1:
#         raise ValueError(
#             f"File {file_name} does not contain underscores; could not extract commit hash."
#         )
#
#     return file_name[underscore_index + 1 :]


# def get_latest_path(paths):
#     """Return the path associated with the latest commit hash
#     If the files are named path1_hash1, path2_hash2, and hash2 is more recent than hash1, then returns path2_hash2
#     """
#     all_commit_hashes = subprocess.check_output(["git", "log", "--format=%h"]).decode('ascii').strip().split("\n")
#
#     def _key(file_name):
#         try:
#             commit_hash = get_commit_hash(file_name)
#             return all_commit_hashes.index(commit_hash)
#         except ValueError:
#             return float("inf")
#
#     latest = min(paths, key=_key)
#
#     # Check that this is actually a valid commit hash
#     if get_commit_hash(latest) not in all_commit_hashes:
#         raise ValueError("List of file names contains no files with commit hashes.")
#
#     return latest


def get_exe_path(env_name, executable_name):
    """Return path to environment executable associated with the latest commit."""
    if sys.platform == "darwin":
        platform = "Mac"
    elif sys.platform == "win32":
        platform = "Windows"
        executable_name = executable_name + ".exe"
    elif sys.platform == "linux":
        platform = "Linux"
        executable_name = executable_name + ".x86_64"
    else:
        raise ValueError("Unknown system platform")

    executable_path = (
        Path(__file__).parent.absolute() / env_name / platform / executable_name
    )

    if not executable_path.exists():
        raise ValueError(
            f"No executable for environment with this name were found: '{executable_path}'"
        )
    return str(executable_path)


def process_raycast(raycast, obs_shape, reorder_mat):
    # raycast = raycast[1::2] # remove hit flags
    raycast = np.reshape(raycast, obs_shape)
    raycast = np.einsum("ijk,jl->ilk", raycast, reorder_mat)
    raycast = 255 - (raycast * 255.0).astype(np.uint8)
    return raycast


def generate_reorder_mat(totalRays):
    raysPerSide = int(np.floor(totalRays / 2))
    reorderMatrix = np.zeros([totalRays, totalRays])
    # fill in first half of the matrix
    for (row, col) in zip(
        np.array(range(totalRays - 1, 0, -2)), np.array(range(0, raysPerSide))
    ):
        reorderMatrix[row, col] = 1
    # fill in middle value
    reorderMatrix[0, raysPerSide] = 1
    # fill in second half of matrix
    for (row, col) in zip(
        np.array(range(1, totalRays - 1, 2)),
        np.array(range(raysPerSide + 1, 2 * raysPerSide + 1)),
    ):
        reorderMatrix[row, col] = 1
    return reorderMatrix