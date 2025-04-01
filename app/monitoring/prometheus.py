import time
from dataclasses import dataclass, field

from prometheus_client import Counter, Histogram, generate_latest
from streamlit_extras import prometheus


@dataclass
class PrometheusMonitor:
    ui_total_requests: Counter = field(init=False)
    ui_request_duration: Histogram = field(init=False)

    def __post_init__(self) -> None:
        self.total_requests = Counter(
            "ui_total_requests",
            "Total number of UI requests",
            labelnames=["action"],
            registry=prometheus.streamlit_registry(),
        )
        self.ui_request_duration_seconds = Histogram(
            "ui_request_duration_seconds",
            "Duration of UI actions",
            labelnames=["action"],
            registry=prometheus.streamlit_registry(),
        )

    def start_time(self) -> float:
        return time.time()

    def get_duration(self, start_time: float) -> float:
        return time.time() - start_time

    def record_request(self, action: str, duration: float) -> None:
        self.total_requests.labels(action=action).inc()
        self.ui_request_duration_seconds.labels(action=action).observe(duration)

    def collect_metrics(self) -> bytes:
        return generate_latest()  # type: ignore


PROMETHEYS_MONITOR = PrometheusMonitor()
