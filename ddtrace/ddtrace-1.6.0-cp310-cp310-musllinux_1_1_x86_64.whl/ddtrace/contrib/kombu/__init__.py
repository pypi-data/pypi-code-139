"""Instrument kombu to report AMQP messaging.

``patch_all`` will not automatically patch your Kombu client to make it work, as this would conflict with the
Celery integration. You must specifically request kombu be patched, as in the example below.

Note: To permit distributed tracing for the kombu integration you must enable the tracer with priority
sampling. Refer to the documentation here:
https://ddtrace.readthedocs.io/en/stable/advanced_usage.html#priority-sampling

Without enabling distributed tracing, spans within a trace generated by the kombu integration might be dropped
without the whole trace being dropped.
::

    from ddtrace import Pin, patch
    import kombu

    # If not patched yet, you can patch kombu specifically
    patch(kombu=True)

    # This will report a span with the default settings
    conn = kombu.Connection("amqp://guest:guest@127.0.0.1:5672//")
    conn.connect()
    task_queue = kombu.Queue('tasks', kombu.Exchange('tasks'), routing_key='tasks')
    to_publish = {'hello': 'world'}
    producer = conn.Producer()
    producer.publish(to_publish,
                     exchange=task_queue.exchange,
                     routing_key=task_queue.routing_key,
                     declare=[task_queue])

    # Use a pin to specify metadata related to this client
    Pin.override(producer, service='kombu-consumer')
"""

from ...internal.utils.importlib import require_modules


required_modules = ["kombu", "kombu.messaging"]

with require_modules(required_modules) as missing_modules:
    if not missing_modules:
        from .patch import patch

        __all__ = ["patch"]
