import logging

FMT_NO_MODULENAME = "%(asctime)s - %(levelname)s - %(message)s"
FMT_WITH_MODULENAME = '%(asctime)s - %(funcName)s - %(levelname)s - %(message)s'
class CustomLoggerWrapper():

    def __init__(self, logger_name, logger_level=logging.INFO, logger_propagate=False, logger_fmt=FMT_NO_MODULENAME, log_filename="mylog.log"):
        self.custom_logger = None
        self.logger_name = logger_name
        self.logger_propagate = logger_propagate
        self.logger_level = logger_level
        self.logger_fmt = logger_fmt
        self.log_filename = log_filename

    def InitLogger(self):
        self.custom_logger = logging.getLogger(self.logger_name)
        self.custom_logger.propagate = False
        self.custom_logger.setLevel(level=self.logger_level)
        logger_fmt = logging.Formatter(self.logger_fmt)
        # Add file_handler
        file_handler = logging.FileHandler(self.log_filename)
        file_handler.setFormatter(logger_fmt)
        self.custom_logger.addHandler(file_handler)

    def GetInitedLogger(self):
        return logging.getLogger(self.logger_name)
