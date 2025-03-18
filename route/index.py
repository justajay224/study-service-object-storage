import os
from importlib import import_module

def include_routers(app):
    current_dir = os.path.dirname(__file__)
    for file in os.listdir(current_dir):
        if file.endswith("_route.py") and file not in {"__init__.py", "index.py"}: # Hanya file yang diakhiri dengan _route.py, kecuali __init__.py dan index.py
            module = import_module(f".{file[:-3]}", __package__)
            if router := getattr(module, "router", None):
                app.include_router(router)