class StampHQException:
    """base class for exceptions from stampHQ library"""


class StampHQClientError(StampHQException, Exception):
    """Indicates client's error."""

    def __init__(self, *args, **kwargs):
        self.error_code = kwargs.pop("error_code")
        super().__init__(*args, **kwargs)
