from .producer import producer


def convert_dict_to_pb(data, pb):
    from google.protobuf.json_format import ParseDict

    return ParseDict(data, pb(), ignore_unknown_fields=True)


async def _publisher_pb(key, pb_class, data):
    pb_data = convert_dict_to_pb(data, pb_class)
    message = pb_data.SerializePartialToString()
    await producer.produce(key, message)


def publish_pb(key, pb_class):
    async def handler(data):
        assert not isinstance(data, (list, tuple))
        await _publisher_pb(key, pb_class, data)

    return handler
