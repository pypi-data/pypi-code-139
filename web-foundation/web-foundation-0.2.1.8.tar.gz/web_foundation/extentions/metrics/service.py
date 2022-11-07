import asyncio

from web_foundation.extentions.metrics.basemetric import BaseMetric
from web_foundation.extentions.metrics.events import MetricRequest, NewMetricEvent
from web_foundation.extentions.metrics.exporter import MetricExporter
from web_foundation.kernel.service import Service


class MetricsService(Service):

    async def collect_metrics(self, exporter: MetricExporter):
        metrics_response: MetricResponse = await self.wait_for_response(MetricRequest(exporter))
        return metrics_response.metrics_data

    async def give_metric(self, metric: BaseMetric):
        asyncio.create_task(self.channel.produce(NewMetricEvent(metric)))
