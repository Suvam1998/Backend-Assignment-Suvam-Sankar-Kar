from prometheus_client import Counter, Histogram

http_requests = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["path", "status"]
)

webhook_counter = Counter(
    "webhook_requests_total",
    "Webhook results",
    ["result"]
)

latency = Histogram("request_latency_ms", "Latency in ms")
