import asyncio
from .command import init_command
from .config import init_conf
from .database import import_models, init_db
from .kafka import start_kafka_producer, start_consumer, stop_kafka_producer


async def bootstrap_consumer(consumer_group_name: str, consumers_path: str, **consumer_configs):
    command_args = init_command()
    if command_args.config == "testing":
        while True:
            await asyncio.sleep(1000000)
    init_conf(command_args.config)
    gen_db = init_db()
    await gen_db.__anext__()
    await start_kafka_producer()
    await start_consumer(consumer_group_name, consumers_path, **consumer_configs)
