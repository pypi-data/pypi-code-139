import requests as r


class BaseManager:
    def __init__(self) -> None:
        self.settings = self.SETTINGS()

    def auth(self):
        raise NotImplementedError

    def pagination(self, url, *, params=None, **kwargs):
        raise NotImplementedError

    def pagination_next(self, response):
        raise NotImplementedError

    def make_request(self, path, *, method, params=None):
        _path = f"{self.BASE_URL}{path}"
        _r = r.request(
            method,
            _path,
            headers=self.get_headers(),
            **dict(
                (dict(params=params) or {}) if method == 'GET' else (dict(json=params) or {})
            )
        )

        assert _r.ok, f"Запрос {method.upper()} {_path} прошел с ошибкой {_r.status_code}"
        return _r
