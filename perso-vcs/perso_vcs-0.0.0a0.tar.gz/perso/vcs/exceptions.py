class PersoVCSBaseException(Exception):
    error_msg: str = "base exception."

    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs

    def __str__(self) -> str:
        return self.error_msg.format(**self.kwargs)
