import typing

import aiokafka


class ProducerMessage(typing.TypedDict):
    key: str
    message: str


class KafkaProducer:
    def __init__(self, host="localhost", port="9092", error_topic=None):
        self.host = host
        self.port = port
        self.error_topic = error_topic
        self.producer: typing.Optional[aiokafka.AIOKafkaProducer] = None
        self.messages: typing.List[ProducerMessage] = []

    def create_producer(self, loop):
        self.producer = aiokafka.AIOKafkaProducer(
            loop=loop,
            bootstrap_servers=f"{self.host}:{self.port}"
        )

    async def start(self, *args, **kwargs):
        from src.core.config import conf

        if conf.ENV == "testing":
            return
        await self.producer.start()

    async def produce(self, key, message, *args, **kwargs):
        from src.core.config import conf

        print(f"<<<<<<PUBLISHED>>>>>> {key}: {message}")
        if conf.ENV == "testing":
            self.messages.insert(0, dict(key=key, message=message))
        else:
            await self.producer.send_and_wait(
                *args, topic=key, value=message, key=key.encode(), **kwargs
            )

    async def produce_error(self, message, *args, **kwargs):
        from src.core.config import conf

        print(f"<<<<<<PUBLISHED>>>>>> {self.error_topic}: {message}")
        if conf.ENV == "testing":
            self.messages.insert(0, dict(key=self.error_topic, message=message))
        else:
            await self.producer.send_and_wait(
                *args,
                topic=self.error_topic,
                value=message,
                key=self.error_topic.encode(),
                **kwargs,
            )

    def clear_messages(self):
        from src.core.config import conf

        if conf.ENV != "testing":
            assert "It works only on testing mode"
        self.messages = []

    async def stop(self):
        if self.producer:
            await self.producer.stop()


producer = KafkaProducer()


async def start_kafka_producer(**kwargs):
    import asyncio
    from src.core.config import conf

    producer.host = conf.KAFKA["HOST"]
    producer.port = conf.KAFKA["PORT"]
    producer.error_topic = conf.KAFKA["EXCEPTION_TOPIC"]
    producer.create_producer(asyncio.get_event_loop())
    await producer.start(**kwargs)
    print("Kafka producer is started")


async def stop_kafka_producer():
    await producer.stop()
    print("Kafka producer is stopped")
