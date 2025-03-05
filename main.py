from fastapi import FastAPI
from route.backblaze_route import router as backblaze_router

app = FastAPI()

app.include_router(backblaze_router)
