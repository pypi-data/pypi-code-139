from __future__ import annotations
import sys, inspect, logging
from pathlib import Path
from .logging import configure_logging
from .network import configure_proxy

_venv: Path|None = None
_venv_lookedup = False

def get_venv() -> Path|None:
    """ Returns venv Path if any, else None """
    global _venv, _venv_lookedup

    if not _venv_lookedup:
        _venv = None
        _venv_lookedup = True
        cwd = Path.cwd()
        potential_venv = Path(sys.executable).parent.parent
        if cwd in potential_venv.parents:
            _venv = potential_venv

    return _venv

def configure_env(**options) -> Path:
    """
    Load `.env` file into environment variables, configure logging and proxy, and return a `BASE_DIR` from which other paths in your project may be built.

    This should be called in the file `__init__.py` or `settings.py` of your project package.

    If your package is installed as a Python library (that is, if it is in a directory named `dist-packages` or `site-packages`), `BASE_DIR` will be the current working directory.
    Otherwise, `BASE_DIR` will be your package container.

    File `.env` will be loaded from the current working directory if available, otherwise from `BASE_DIR` is available.
    """

    caller_filename = inspect.stack()[1].filename 

    BASE_DIR = Path(caller_filename).resolve().parent.parent
    if BASE_DIR.name in ["dist-packages", "site-packages"]:
        BASE_DIR = Path.cwd()

    dotenv = Path.cwd().joinpath(".env")
    if not dotenv.exists():
        dotenv = BASE_DIR.joinpath(".env")
        if not dotenv.exists():
            dotenv = None
    
    if dotenv:
        from dotenv import load_dotenv
        load_dotenv(dotenv)

    # Configure logging
    configure_logging_func = options.pop("configure_logging", configure_logging)
    if configure_logging_func:
        kwargs = {}
        for key in ["level", "default_level", "format", "filename", "filelevel", "fileformat", "nocount", "nocolor"]:
            if key in options:
                kwargs[key] = options.pop(key)

        configure_logging_func(**kwargs)

    # Configure proxy
    configure_proxy_func = options.pop("configure_proxy", configure_proxy)
    if configure_proxy_func:
        configure_proxy_func(**options)

    logger = logging.getLogger(__name__)
    logger.debug(f"configured BASE_DIR: {BASE_DIR}, dotenv: {dotenv}")

    return BASE_DIR
