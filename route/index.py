from .backblaze_route import router as router_backblaze

__all__ = ["all_routers"]


all_routers = [
    router_backblaze
]