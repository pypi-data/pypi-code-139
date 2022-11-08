import asyncio
import json
import traceback
import typing
from collections import defaultdict

import aiokafka
from google.protobuf.json_format import MessageToDict

consumer_group: typing.Dict[str, typing.Dict[str, typing.Callable]] = defaultdict(dict)


async def start_consumer(group_name: str, consumers_path: str,  **consumer_configs):
    _collect_consumers(consumers_path=consumers_path)
    consumers = consumer_group.get(group_name)

    if not consumers:
        print(f"Consumer group \"{group_name}\" is empty.")
        return

    topics = list(consumers.keys())

    futures = []
    for topic in topics:
        func = consumers[topic]
        futures.append(_run_consumer_loop(topic, func, consumer_configs))

    print("Kafka consumer is started")
    await asyncio.gather(*futures)


async def _run_consumer_loop(topic, func, consumer_configs):
    consumer = await _start_kafka_consumer([topic], **consumer_configs)

    while True:
        message = await consumer.getone()
        tp = aiokafka.TopicPartition(message.topic, message.partition)

        try:
            print(f"<<<<<<CONSUMED>>>>>>  {message.topic}: {message.value}")
            await func(message.value)
            await consumer.commit({tp: message.offset + 1})
        except Exception as e:
            traceback.print_exc()


def add_consumer(topic, handler, group="main"):
    protobuf_ = getattr(handler, "protobuf", None)
    assert protobuf is not None, "Use decorator protobuf"
    method = _deserialize_and_pass(topic, handler, protobuf_)
    consumer_group[group][topic] = method
    return method


def protobuf(protocol_buffer):
    def func_wrapper(func):
        async def arg_wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        arg_wrapper.protobuf = protocol_buffer
        return arg_wrapper

    return func_wrapper


async def _start_kafka_consumer(topics, **configs):
    import asyncio
    from src.core.config import conf

    consumer = aiokafka.AIOKafkaConsumer(
        *topics,
        loop=asyncio.get_event_loop(),
        bootstrap_servers=f'{conf.KAFKA["HOST"]}:{conf.KAFKA["PORT"]}',
        group_id=conf.KAFKA["GROUP_ID"],
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        **configs,
    )
    await consumer.start()
    return consumer


def _deserialize_and_pass(topic, func, protocol_buffer):
    from .producer import producer

    try:
        import broker.consumer_exceptions_pb2 as pb
    except ImportError:
        raise Exception("Protobuf library not found")

    async def wrapper(message: bytes):
        pb_obj = protocol_buffer().FromString(message)
        try:
            return await func(pb_obj)
        except Exception as e:
            print(e)
            error = traceback.format_exc()
            data = dict(
                description=error,
                topic=topic,
                body=message,
                json_body=json.dumps(MessageToDict(pb_obj)),
            )
        await producer.produce_error(pb.Exception(**data).SerializeToString())

    return wrapper


def _collect_consumers(consumers_path: str):
    try:
        __import__(consumers_path)
    except ModuleNotFoundError as e:
        pass

