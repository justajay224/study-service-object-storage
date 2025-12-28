from fastapi import FastAPI
from route.index import include_routers
from dotenv import load_dotenv
import uvicorn
import os

load_dotenv()

app = FastAPI()

include_routers(app)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
