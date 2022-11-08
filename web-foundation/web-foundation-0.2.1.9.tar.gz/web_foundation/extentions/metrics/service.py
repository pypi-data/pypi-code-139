import asyncio

from web_foundation.extentions.metrics.metric import Metric
from web_foundation.extentions.metrics.events import MetricRequestEvent, NewMetricEvent, MetricResponseEvent
from web_foundation.extentions.metrics.exporter import MetricExporter
from web_foundation.kernel.service import Service


class MetricsService(Service):

    async def collect_metrics(self, exporter: MetricExporter):
        metrics_response: MetricResponseEvent = await self.wait_for_response(MetricRequestEvent(exporter))
        return metrics_response.metrics_data

    async def give_metric(self, metric: Metric):
        asyncio.create_task(self.channel.produce(NewMetricEvent(metric)))
