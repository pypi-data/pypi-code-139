from src.microservice.core.kafka import publish_pb


class Context:
    def __init__(self):
        self.data = dict(has_error=False)
        self.publish_data = []

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, data):
        self.data[key] = data

    async def __aenter__(self):
        return self

    def raise_error(self):
        self.data["has_an_error"] = True

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.data.get("has_an_error"):
            return
        for (topic, pb, value) in self.publish_data:
            await publish_pb(topic, pb)(value)

    def publish(self, topic, pb, value):
        self.publish_data.append((topic, pb, value))


def context(func):
    async def arg_wrapper(*args, **kwargs):
        async with Context() as ctx:
            try:
                result = await func(*args, ctx=ctx, **kwargs)
            except Exception as e:
                ctx.raise_error()
                raise e

        return result

    return arg_wrapper
