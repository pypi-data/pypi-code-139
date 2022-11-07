class DgError(ValueError):
    pass


class InnerError(ValueError):
    pass


class ErrorInfo(object):

    _error_hub = {
        "19998": "Auth Error",
        "19999": "Illegal request Error",
        "20000": "Parameter Error",
        "20001": "App Info Error",
        "20002": "Security Error",
        "20003": "Callback Error",
        "20004": "DSL Error",
        "20005": "ACL Words Error",
        "20009": "Scene Setting Error",
        "20010": "Search Program Error",
        "20011": "Empty Results Error",
        "20012": "Results Paging Error",
        "20013": "Expression Error",
        "30001": "Query Analysis, Name Error",
        "30002": "Query Analysis Error",
        "40001": "Speech Recognition Error"
    }

    _inner_error_list = ["20003", "30002"]

    @staticmethod
    def get_error(code, msg):
        err_pre = ErrorInfo._error_hub.get(code, "Unknown Error")
        if code in ErrorInfo._inner_error_list:
            # return InnerError(code, f"{err_pre}: {msg}")
            return InnerError(code, f"{msg}")
        # return DgError(code, f"{err_pre}: {msg}")
        return DgError(code, f"{msg}")
