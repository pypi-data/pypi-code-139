import os
import posixpath
from tempfile import mkdtemp
import numpy as np
from silx.io.url import DataUrl
from tomoscan.io import HDF5File
from tomoscan.esrf.hdf5scan import ImageKey
from ..utils import check_supported, is_writeable, deprecation_warning
from ..io.writer import NXProcessWriter
from ..io.utils import get_first_hdf5_entry, hdf5_entry_exists, get_h5_str_value, get_compacted_dataslices
from ..thirdparty.tomwer_load_flats_darks import get_flats_frm_process_file, get_darks_frm_process_file
from .logger import LoggerOrPrint


def get_frame_possible_urls(dataset_info, user_dir, output_dir, frame_type):
    """
    Return a DataUrl with the possible location of reduced dark/flat frames.

    Parameters
    ----------
    dataset_info: DatasetAnalyzer object
        DatasetAnalyzer object
    user_file: str or None
        User-provided file location for the reduced frames.
    output_dir: str or None
        Output processing directory
    frame_type: str
        Frame type, can be "flats" or "darks".
    """
    check_supported(frame_type, ["flats", "darks"], "frame type")

    h5scan = dataset_info.dataset_scanner # tomoscan object
    if frame_type == "flats":
        dataurl_default_template = h5scan.REDUCED_FLATS_DATAURLS[0]
    else:
        dataurl_default_template = h5scan.REDUCED_DARKS_DATAURLS[0]

    def make_dataurl(dirname):
        return DataUrl(
            file_path=os.path.join(dirname, dataurl_default_template.file_path()),
            data_path=dataurl_default_template.data_path(),
            data_slice=dataurl_default_template.data_slice(),
            scheme="silx",
        )

    urls = {"user": None, "dataset": None, "output": None}

    if user_dir is not None:
        urls["user"] =  make_dataurl(user_dir)

    # tomoscan.esrf.scan.hdf5scan.REDUCED_{DARKS|FLATS}_DATAURLS.file_path() is a relative path
    # Create a absolute path instead
    urls["dataset"] = make_dataurl(os.path.dirname(h5scan.master_file))

    if output_dir is not None:
        urls["output"] = make_dataurl(output_dir)

    return urls


def update_dataset_info_flats_darks(dataset_info, flatfield_mode, output_dir=None, darks_flats_dir=None):
    """
    Update a DatasetAnalyzer object with reduced flats/darks (hereafter "reduced frames").

    How the reduced frames are loaded/computed/saved will depend on the "flatfield_mode" parameter.

    The principle is the following:
    (1) Attempt at loading already-computed reduced frames (XXX_darks.h5 and XXX_flats.h5):
       - First check files in the user-defined directory 'darks_flats_dir'
       - Then try to load from files located alongside the .nx dataset (dataset directory)
       - Then try to load from output_dir, if provided
    (2) If loading fails, or flatfield_mode == "force_compute", compute the reduced frames.
    (3) Save these reduced frames
       - Save in darks_flats_dir, if provided by user
       - Otherwise, save in the data directory (next to the .nx file), if write access OK
       - Otherwise, save in output directory
    """
    if flatfield_mode is False:
        return
    logger = dataset_info.logger
    dataset_dir = os.path.dirname(dataset_info.dataset_hdf5_url.file_path())
    frames_types = ["darks", "flats"]

    reduced_frames_urls = {}
    for frame_type in frames_types:
        reduced_frames_urls[frame_type] = get_frame_possible_urls(dataset_info, darks_flats_dir, output_dir, frame_type)

    #
    # Attempt at loading frames
    #
    frames_loaded = dict.fromkeys(frames_types, False)
    if flatfield_mode != "force-load":
        for load_from in ["user", "dataset", "output"]: # in that order
            for frame_type in frames_types:
                url = reduced_frames_urls[frame_type][load_from]
                if url is None:
                    continue # cannot load from this source (eg. undefined folder)
                tomoscan_method = getattr(dataset_info.dataset_scanner, "load_reduced_%s" % frame_type)
                reduced_frames = tomoscan_method(
                    input_urls=[url],
                    return_as_url=True
                )
                if reduced_frames not in (None, {}):
                    dataset_info.logger.info("Loaded %s from %s" % (frame_type, reduced_frames.values()))
                    setattr(dataset_info, frame_type, reduced_frames)
                    frames_loaded[frame_type] = True
                else:
                    msg = "Could not load %s from %s" % url.file_path()
                    logger.error(msg)
            if all(frames_loaded.values()):
                break

    frames_saved = dict.fromkeys(frames_types, False)
    if not all(frames_loaded.values()):
        for save_to in ["user", "dataset", "output"]: # in that order
            for frame_type in frames_types:
                url = reduced_frames_urls[frame_type][save_to]
                if url is None:
                    continue # cannot load from this source (eg. undefined folder)
                tomoscan_reduction_method = getattr(dataset_info.dataset_scanner, "compute_reduced_%s" % frame_type)
                frames_reduced = tomoscan_reduction_method()
                tomoscan_method = getattr(dataset_info.dataset_scanner, "save_reduced_%s" % frame_type)
                tomoscan_method(frames_reduced, output_urls=[url])
                dataset_info.logger.info("Saved reduced %s to %s" % (frame_type, url.file_path()))
                frames_saved[frame_type] = True
            if all(frames_saved.values()):
                break



# tomoscan "compute_reduced_XX" is quite slow. If needed, here is an alternative implementation
def my_reduce_flats(di):
    res = {}
    with HDF5File(di.dataset_hdf5_url.file_path(), "r") as f:
        for data_slice in di.get_data_slices("flats"):
            data = f[di.dataset_hdf5_url.data_path()][data_slice.start:data_slice.stop]
            res[data_slice.start] = np.median(data, axis=0)
    return res


