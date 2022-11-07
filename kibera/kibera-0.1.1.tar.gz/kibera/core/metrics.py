from prometheus_client import Counter, Histogram, start_http_server


def start_metrics_server(metrics_port):
    if metrics_port:
        start_http_server(metrics_port)


key_requests_total = Counter(
    "key_requests_total", "Number of requests made for fetching keys"
)

# To use: sample_metric.inc()
