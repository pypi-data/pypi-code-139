from aiohttp import web


class AioServer:

    def __init__(self, client_max_size: int = 1024 ** 2, **kwargs):
        self.app = web.Application(client_max_size=client_max_size, **kwargs)

    def router_get(self, path: str):
        def inner(func):
            self.app.router.add_get(path, func)
            return

        return inner

    def router_post(self, path: str):
        def inner(func):
            self.app.router.add_post(path, func)
            return

        return inner

    def run(self, host=None, port=None):
        web.run_app(app=self.app, host=host, port=port)


server = AioServer()


@server.router_get("/")
def ssr(request):
    # name = request.match_info.get('name', "Anonymous")
    text = "Hello, "
    return web.Response(text=text)


if __name__ == '__main__':
    server.run("localhost", 8180)
