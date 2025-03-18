from fastapi import FastAPI
from route.index import include_routers

app = FastAPI()

include_routers(app)
