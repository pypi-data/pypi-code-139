class LogLevel:
    from colorama import Fore as __Fore

    def __init__(self, name, color: str = __Fore, isFatal: bool = False):
        self.name = name
        self.color = color
        self.isFatal = isFatal

    def log(self, message):
        logger = Logger()
        logger.log(message, self)
        if self.isFatal and logger.quitWhenLogFatal:
            quit()


class Logger:
    from colorama import Fore as __Fore

    def __init__(self,
                 logLevel: bool = True,
                 colorLevelText: bool = True,
                 quitWhenLogFatal: bool = False,
                 colorText: bool = True,
                 prefixBeforeTime: bool = True,
                 warnLevel: LogLevel = LogLevel("WARN", __Fore.YELLOW),
                 infoLevel: LogLevel = LogLevel("INFO", __Fore.RESET),
                 debugLevel: LogLevel = LogLevel("DEBUG", __Fore.WHITE),
                 errorLevel: LogLevel = LogLevel("ERROR", __Fore.LIGHTRED_EX),
                 fatalLevel: LogLevel = LogLevel("FATAL", __Fore.RED, isFatal=True),
                 prefix: str = ""):

        self.logLevel = logLevel
        self.colorLevelText = colorLevelText
        self.quitWhenLogFatal = quitWhenLogFatal
        self.colorText = colorText
        self.prefixBeforeTime = prefixBeforeTime
        self.warnLevel = warnLevel
        self.infoLevel = infoLevel
        self.debugLevel = debugLevel
        self.errorLevel = errorLevel
        self.fatalLevel = fatalLevel
        self.prefix = prefix

    def log(self, message: str, level: LogLevel = None, end: str = "\n"):
        from datetime import datetime
        from colorama import Fore
        if not level:
            level = self.debugLevel

        current_time = datetime.now().strftime("%X")

        if self.colorText:
            if self.logLevel:
                print(
                    self.prefix if self.prefixBeforeTime else "",
                    " " if self.prefix and self.prefixBeforeTime else "",

                    f"[{current_time}]",
                    " " if self.prefix and not self.prefixBeforeTime else "",
                    self.prefix if not self.prefixBeforeTime else "",


                    f" {level.color if self.colorLevelText else Fore.RESET}[{level.name}]",
                    f" {level.color}{message}",
                    end=end + Fore.RESET,
                    sep="")

            else:
                print(self.prefix if self.prefixBeforeTime else "",
                    " " if self.prefix and self.prefixBeforeTime else "",

                    f"[{current_time}]",
                    " " if self.prefix and not self.prefixBeforeTime else "",
                    self.prefix if not self.prefixBeforeTime else "",

                    f" {level.color}{message}",
                    end=end + Fore.RESET,
                    sep="")
        else:
            if self.logLevel:
                print(self.prefix if self.prefixBeforeTime else "",
                    " " if self.prefix and self.prefixBeforeTime else "",

                    f"[{current_time}]",
                    " " if self.prefix and not self.prefixBeforeTime else "",
                    self.prefix if not self.prefixBeforeTime else "",


                    f" [{level.name}]",
                    f" {message}",
                    end=end + Fore.RESET,
                    sep="")

            else:
                print(self.prefix if self.prefixBeforeTime else "",
                    " " if self.prefix and self.prefixBeforeTime else "",

                    f"[{current_time}]",
                    " " if self.prefix and not self.prefixBeforeTime else "",
                    self.prefix if not self.prefixBeforeTime else "",

                    f" {message}",
                    end=end + Fore.RESET,
                    sep="")

    def log_warning(self, message: str):
        self.log(message, self.warnLevel)

    def log_info(self, message: str):
        self.log(message, self.infoLevel)

    def log_debug(self, message: str):
        self.log(message, self.debugLevel)

    def log_error(self, message: str):
        self.log(message, self.errorLevel)

    def log_fatal(self, message: str, exception=""):
        self.log(message, self.fatalLevel)
        if self.quitWhenLogFatal:
            quit(exception)
