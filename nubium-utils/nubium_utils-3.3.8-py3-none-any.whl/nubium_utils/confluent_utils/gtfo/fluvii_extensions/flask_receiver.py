import logging
from os import environ
from unittest import mock

from fluvii.fluvii_app import FluviiConfig
from fluvii.producer import Producer
from fluvii.schema_registry import SchemaRegistry

from .nubium.metrics import NubiumMetricsManager

LOGGER = logging.getLogger(__name__)


def get_flask_fluvii_producer(fluvii_config, topic_schema_dict):
    return Producer(
        urls=fluvii_config.client_urls,
        schema_registry=SchemaRegistry(url=fluvii_config.schema_registry_url,
                                       auth_config=fluvii_config.client_auth_config),
        client_auth_config=fluvii_config.client_auth_config,
        topic_schema_dict=topic_schema_dict
    )


class NubiumFlaskConfig:
    def __init__(self, producer=None, topic=None, schema=None):
        self.LOGLEVEL = environ['LOGLEVEL']

        self.TOPIC = topic
        self.PRODUCER = producer
        self.SCHEMA = schema

        if self.TOPIC is None:
            self.TOPIC = environ['OUTPUT_TOPIC']

        self.TOPIC_SCHEMA_DICT = {self.TOPIC: self.SCHEMA}

        fluvii_config = FluviiConfig()

        self.METRICS_MANAGER = NubiumMetricsManager(metrics_config=fluvii_config.metrics_manager_config,
                                                    pusher_config=fluvii_config.metrics_pusher_config)

        if self.PRODUCER is None:
            self.PRODUCER = get_flask_fluvii_producer(fluvii_config, self.TOPIC_SCHEMA_DICT)


class NubiumTestFlaskConfig:
    def __init__(self):
        self.TESTING = True
        self.LOGLEVEL = "DEBUG"
        self.TOPIC = mock.MagicMock()
        self.SCHEMA = mock.MagicMock()
        self.METRICS_MANAGER = mock.MagicMock()
        self.PRODUCER = mock.MagicMock()
