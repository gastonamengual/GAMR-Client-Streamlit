from dataclasses import dataclass
from enum import StrEnum

from app.settings import Settings


@dataclass
class BackendService(StrEnum):
    VERCEL = "Vercel"
    RENDER_DOCKER = "Render + Docker"
    LOCAL = "Local"


backend_service_urls = {
    BackendService.VERCEL.value: Settings.VERCEL_BASE_URL,
    BackendService.RENDER_DOCKER.value: Settings.RENDER_DOCKER_BASE_URL,
    BackendService.LOCAL.value: Settings.LOCAL_BASE_URL,
}
