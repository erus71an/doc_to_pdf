from prometheus_client import Counter, Summary

# Метрики Prometheus
REQUEST_COUNT = Counter(
    "request_count", "Общее количество запросов", ["endpoint", "method", "status"]
)
REQUEST_LATENCY = Summary(
    "request_latency_seconds", "Время обработки запроса", ["endpoint"]
)
