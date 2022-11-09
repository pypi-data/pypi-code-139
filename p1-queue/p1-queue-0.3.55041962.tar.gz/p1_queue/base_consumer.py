# -*- coding: utf-8 -*-

from __future__ import absolute_import
from builtins import str
from builtins import object
import logging
import os

from google.cloud import pubsub_v1

LOGGER = logging.getLogger(__name__)


class BaseConsumer(object):
    subscription_name = None

    def __init__(self, topic_id):
        if self is BaseConsumer:
            raise Exception(
                "Can't directly use the BaseConsumer class. Please extend it.")

        subscriber_project_id = os.getenv('PUBSUB_PROJECT_ID'),
        self.subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
            project_id=os.getenv('PUBSUB_PROJECT_ID'),
            sub=topic_id + '-' + subscriber_project_id
        )
        self.instance = pubsub_v1.SubscriberClient()

    def on_message(self, message):
        pass

    def run(self):
        def handle_message(message):
            LOGGER.info('Received message # %s from %s: %s',
                        message.message_id, message.common_project_path, message.data)

            try:
                self.on_message(message)
                message.ack()
            except Exception as e:
                LOGGER.warning(
                    'Error occured when handling message: %s', str(e))
                message.nack()

        self.instance.subscribe(self.subscription_name, handle_message)
