import contamxpy as cxLib
import os, sys
from optparse import OptionParser

#===================================================================================== main() =====
def main():
    #----- Manage option parser
    parser = OptionParser(usage="%prog [options] arg1\n\targ1=PRJ filename\n")
    parser.set_defaults(verbose=0)
    parser.add_option("-v", "--verbose", action="store", dest="verbose", type="int", default=0,
                        help="Define verbose output level: 0=Min, 1=Medium, 2=Maximum.")
    (options, args) = parser.parse_args()

    #----- Process command line options -v
    verbose = options.verbose

    if len(args) != 1:
        parser.error("Need one argument:\n  arg1 = PRJ file.")
        return
    else:
        prj_name  = args[0]

    if ( not os.path.exists(prj_name) ):
        print("ERROR: PRJ file not found.")
        return

    if verbose > 1:
        print(f"cxLib attributes =>\n\t{dir(cxLib)}")

    msg_cmd = "Running test_cxcffi.py: arg1 = " + args[0] + " " + str(options)
    print(msg_cmd, "\n")

    #----- Initialize contamx-lib State
    p_contam_state: object = cxLib.getState()
    cxLib.setWindPressureMode(p_contam_state, 0)

    #----- Query State for PRJ info
    verStr = cxLib.getVersion(p_contam_state)
    if verbose >= 0:
        print(f"getVersion() returned {verStr}.")


# --- End main() ---#

if __name__ == "__main__":
    main()