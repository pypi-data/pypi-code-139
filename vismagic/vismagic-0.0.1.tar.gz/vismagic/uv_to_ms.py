# This script converts a UVTable to an MSTable, given a reference MSTable of
# the same observations (from which the UVTable was originally created).
# NB: This must be run in casapy (a CASA custom python environment).

import os
import argparse
import numpy as np

def parse_parameters(*args):
    parser = argparse.ArgumentParser("Convert a UVTable to MSTable in casapy")

    parser.add_argument("-ref_ms", "--reference_mstable_filename",
                        default=None, type=str,
                        help="Original MSTable from which the UVTable was"
                             " generated")
    parser.add_argument("-uv_tab", "--uvtable_filename",
                        default=None, type=str,
                        help="UVTable to be converted into a new MSTable")
    parser.add_argument("-new_ms", "--new_mstable_filename",
                        default=None, type=str,
                        help="Filename for the new MSTable")

    args = parser.parse_args(*args)

    return args


def load_uvtable(data_file):
    r"""
    Read in a UVTable

    Parameters
    ----------
    data_file : string
          UVTable.
          If in ASCII format, the table should have columns:
            u [lambda]  v [lambda]  Re(V) [Jy]  Im(V) [Jy]  Weight [Jy^-2]
          If in .npz format, the file should have arrays:
            "u" [lambda], "v" [lambda], "V" [Jy; complex: real + imag * 1j],
            "weights" [Jy^-2]

    Returns
    -------
    u, v : array, unit = :math:`\lambda`
          u and v coordinates of observations
    vis : array, unit = Jy
          Observed visibilities (complex: real + imag * 1j)
    weights : array, unit = Jy^-2
          Weights on the visibilities, of the form
          :math:`1 / \sigma^2`
    """

    # Get extension, removing compressed part
    base, extension = os.path.splitext(data_file)
    if extension in {'.gz', '.bz2'}:
        extension = os.path.splitext(base)[1]
        if extension not in {'.txt', '.dat'}:
            raise ValueError("Compressed UV tables (`.gz` or `.bz2`) must be in "
                             "one of the formats `.txt` or `.dat`.")

    if extension in {'.txt', '.dat'}:
        u, v, re, im, weights = np.genfromtxt(data_file).T
        vis = re + 1j*im

    elif extension == '.npz':
        dat = np.load(data_file)
        u, v, vis, weights = [dat[i] for i in ['u', 'v', 'V', 'weights']]
        if not np.iscomplexobj(vis):
            raise ValueError("You provided a UVTable with the extension {}. "
                             "This extension requires the UVTable's variable "
                             "'V' to be complex (of the form Re(V) + Im(V) * "
                             "1j).".format(extension))

    else:
        raise ValueError("You provided a UVTable with the extension {}."
                         " Please provide it as a `.txt`, `.dat`, or `.npz`."
                         " Formats .txt and .dat may optionally be"
                         " compressed (`.gz`, `.bz2`).".format(extension))

    return u, v, vis, weights


def duplicate_mstable(orig_ms, new_ms):
    r"""
    Make a copy of an MSTable

    Parameters
    ----------
    orig_ms : string
        The filename of the MSTable to be copied
    new_ms : string
        The filename of the new MSTable to be created
    """

    # Remove new_ms if it exists
    syscommand = 'rm -rf '+ new_ms
    os.system(syscommand)
    # Create new_ms as a copy of orig_ms
    syscommand = 'cp -r ' + orig_ms + ' ' + new_ms
    os.system(syscommand)


def convert_uv_to_ms(ref_ms, uv_tab, new_ms, check_consistency=True, tb=None):
    r"""
    Convert a UVTable to an MSTable, using a reference MSTable to copy its
    contents and replace select columns. The reference MSTable should be that
    from which the UVTable was extracted (i.e., contain the same
    observations as the UVTable).
    Values in the DATA and WEIGHT columns (and the CORRECTED_DATA column, if it
    exists) are replaced in the new MSTable with corresponding values from the
    UVTable.
    NB: Visibility amplitudes and weights in all polarization columns of the
    MSTable are replaced with the single (presumably averaged) values in the
    UVTable.

    Parameters
    ----------
    ref_ms : MSTable
        The reference MSTable
    uv_tab : UVTable
        The UVTable to be converted to a new MSTable
    new_ms : string
        Filename for the MSTable to be created. Should end in '.ms'
    check_consistency : bool, default = True
        Whether to verify that the MSTable and UVTable have the same number of
        spatial frequency points
    tb : CASA internal 'table tool'
        See https://casa.nrao.edu/docs/CasaRef/table-Module.html
    """
    # Instantiate the 'tb' object
    if tb is None:
        import casa
        tb = casa.tbtool()

    u, v, vis, weights = load_uvtable(uv_tab)

    duplicate_mstable(ref_ms, new_ms)

    # Open the MSTable
    tb.open(new_ms, nomodify=False)

    if check_consistency:
        ms_uvw = tb.getcol("UVW")
        ms_npts = len(ms_uvw[0])
        uv_npts = len(u)
        if ms_npts != uv_npts:
            raise ValueError(" The number of (u, v) coordinates in the"
                               " reference MSTable ({:d}) must be equal to the"
                               " number of coordinates in the UVTable ({:d})."
                               " Verify the observations in the reference"
                               " MStable correspond to those in the"
                               " UVTable.".format(ms_npts, uv_npts)
                             )

    # Replace visibility amplitudes and weights in MSTable
    ms_vis = tb.getcol("DATA")
    ms_weights = tb.getcol("WEIGHT")
    ms_vis[:] = vis
    ms_weights[:] = weights
    print("Placing values from UVTable into DATA and WEIGHTS columns in new"
         " MSTable")
    tb.putcol("DATA", ms_vis)
    tb.putcol("WEIGHT", ms_weights)
    # If the CORRECTED_DATA column exists, replace its values
    if 'CORRECTED_DATA' in tb.colnames():
        ms_corrected_vis = tb.getcol("CORRECTED_DATA")
        ms_corrected_vis[:] = vis
        print("Placing values from UVTable into CORRECTED_DATA column in new"
             " MSTable")
        tb.putcol("CORRECTED_DATA", ms_corrected_vis)

    tb.flush()
    tb.close()

    print("Saved converted UVTable to {}".format(new_ms))


def main(*args):
    """Run the UVTable to MSTable conversion

    Parameters
    ----------
    *args : strings
        Simulates the command line arguments
    """

    args = parse_parameters(*args)
    convert_uv_to_ms(args.reference_mstable_filename, args.uvtable_filename,
                    args.new_mstable_filename)


if __name__ == "__main__":
    main()
