from flask import request, session, g, current_app


class Context:
    request = request
    session = session
    current_app = current_app
    g = g

    @staticmethod
    def g_set(k, v):
        setattr(g, k, v)

    @staticmethod
    def g_get(k, default=None):
        return getattr(g, k, default)

    @staticmethod
    def g_all():
        return g.__dict__.copy()

    @staticmethod
    def get_view_function(endpoint=None):
        if endpoint is None:
            endpoint = request.endpoint
        f = current_app.view_functions.get(endpoint)
        f = getattr(f, '__func__', f)

        return f

    @staticmethod
    def get_real_ip():
        ip_addr = Context.request.remote_addr
        headers = dict([(str(k).lower(), str(v)) for k, v in Context.request.headers.items() if v])
        forward_ips = headers.get('X-Forwarded-For'.lower())  # type: str
        if forward_ips:
            real_ip = forward_ips.split(',').pop(0).strip()
            if real_ip:
                ip_addr = real_ip
        return ip_addr
