"""
asight config
"""
import os
from configparser import ConfigParser

from asight.util.singleton import singleton


@singleton
class Config:
    """
    config
    """

    _CONFIG_DIR_NAME = "config"
    _CONFIG_FILE_NAME = "config.ini"

    def __init__(self) -> None:
        config = ConfigParser(allow_no_value=True)
        self._work_path = os.path.abspath("")  # pwd
        self._root_path = os.path.abspath(os.path.join(__file__, "../../"))  # asight/
        config.read(os.path.join(self._root_path, self._CONFIG_DIR_NAME, self._CONFIG_FILE_NAME))
        # LOG
        self._console_logging_level = config.get("LOG", "console_logging_level").upper()
        # OUTPUT
        self._analysis_result_file = self._normalize_path(config.get("OUTPUT", "analysis_result_file"))
        self._tune_ops_file = self._normalize_path(config.get("OUTPUT", "tune_ops_file"))

    def get_console_log_level(self) -> str:
        """
        get console log level
        :return: console log level
        """
        return self._console_logging_level

    def _normalize_path(self, file) -> str:
        if not file.startswith("/"):
            file = os.path.join(self._work_path, file)
        return os.path.abspath(file)

    @property
    def work_path(self) -> str:
        """
        get work path
        :return: work path
        """
        return self._work_path

    @property
    def root_path(self) -> str:
        """
        get root path
        :return: root path
        """
        return self._root_path

    def set_config(self, key, value) -> None:
        """
        set config value
        :param key: config key
        :param value: config value
        """
        setattr(self, key, value)

    def get_config(self, key) -> str:
        """
        get value of config
        :param key: config key
        :return: config value
        """
        try:
            return getattr(self, key)
        except AttributeError:
            return ""

    @property
    def analysis_result_file(self) -> str:
        """
        get filename of op result file
        :return: filename
        """
        return self._analysis_result_file

    @property
    def tune_ops_file(self) -> str:
        """
        get filename of tune op file
        :return: filename
        """
        return self._tune_ops_file
