from typing import List, Optional
from zetsubou.utils.subprocess import call_process, call_process_venv
import zetsubou.utils.logger as logger


def check_conan_present():
    out, err = call_process(['conan', '--version'], capture=True, realtime=False)
    if err is not None:
        logger.CriticalError('Conan is missing, unable to proceed')
        return False

    logger.Success(out.rstrip())
    return True


def call_conan(args : List[str], cwd : str, venv : Optional[str] = None):
    verbose = logger.IsVisible(logger.ELogLevel.Verbose)

    out = None
    err = None

    if venv is not None:
        out, err = call_process_venv(['conan'] + args, venv, capture = not verbose, realtime = verbose, cwd = cwd)
    else:
        out, err = call_process(['conan'] + args, capture = not verbose, realtime = verbose, cwd = cwd)

    if err is not None:
        if not verbose:
            logger.CriticalError(f'Conan command failed: {" ".join(args)}')
            logger.Error(out)

        logger.CriticalError(f"Conan returned error '{err}'")
        return False
    return True
