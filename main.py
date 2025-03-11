from fastapi import FastAPI
from route.index import all_routers

app = FastAPI()

for router in all_routers:
    app.include_router(router)
