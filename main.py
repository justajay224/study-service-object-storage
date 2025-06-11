from fastapi import FastAPI
from route.index import include_routers
from middleware.cors_middleware import add_cors_middleware
import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

include_routers(app)

add_cors_middleware(app)

# @app.get("/")
# async def root():
#     return {"Service kosong"}

port = int(os.getenv("PORT")) 

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=port, 
        reload=True
    )
