class RequestBase:
    __slots__ = ("method", "url", "headers", "cookies", "data", "proxy", "json", "params", "timeout",)

    def __init__(
            self,
            method,
            url,
            params=None,
            headers=None,
            cookies=None,
            data=None,
            json=None,
            timeout=10,
    ):
        self.method = method
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.data = data
        self.json = json
        self.params = params
        self.timeout = timeout
        self.proxy = None

    @property
    def get_dict(self) -> dict:
        result = {}
        for k in self.__slots__:
            result[k] = self.__getattribute__(k)
        return result


class Request:
    __slots__ = (
        "request_info", "call_back", "meta", "retry"
    )

    def __init__(
            self,
            method,
            url,
            call_back,
            params=None,
            headers=None,
            cookies=None,
            data=None,
            json=None,
            timeout=10,
            meta=None,
            retry=3,
    ):
        self.request_info = RequestBase(
            method=method,
            url=url,
            headers=headers,
            cookies=cookies,
            data=data,
            json=json,
            params=params,
            timeout=timeout
        )
        self.call_back = call_back
        self.meta = meta
        self.retry = retry

    @staticmethod
    def get(url, call_back=None, params=None, headers=None, cookies=None, timeout=10, meta=None, retry=3):
        return Request("GET", url, call_back=call_back, params=params, headers=headers, cookies=cookies,
                       timeout=timeout,
                       meta=meta, retry=retry)

    @staticmethod
    def post(url, call_back=None, params=None, headers=None, data=None, json=None, cookies=None, timeout=10,
             meta=None, retry=3):
        return Request("POST", url, call_back=call_back, params=params, headers=headers, cookies=cookies, data=data,
                       json=json,
                       timeout=timeout, meta=meta, retry=retry)


class Response:
    __slots__ = (
        "headers", "cookies", "read", "text", "url", "status", "ok", "history", "links", "request_info", "meta"
    )

    def __init__(self):
        self.request_info = None
        self.headers = None
        self.cookies = None
        self.status = None
        self.read = None
        self.text = None
        self.url = None
        self.ok = False
        self.history = None
        self.links = None
        self.meta = {}

    async def start_await(self, resp):
        self.request_info = resp.request_info
        self.links = resp.links
        self.history = resp.history
        self.url = resp.url
        self.status = resp.status
        self.ok = resp.ok
        self.headers = resp.headers
        self.cookies = resp.cookies
        self.read = await resp.read()
        self.text = await resp.text()

