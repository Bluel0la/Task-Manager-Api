from fastapi.middleware.cors import CORSMiddleware
from api.v1.routes import api_version_one
from starlette.requests import Request
from fastapi import FastAPI
import uvicorn


app = FastAPI()


origins = [
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_version_one)
# app.include_router(users, tags=["Users"])


@app.get("/", tags=["Home"])
async def get_root(request: Request) -> dict:
    return {
        "message": "Welcome to API",
        "URL": "",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", port=7001, reload=True)
