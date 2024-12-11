# /app/main.py

import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.routes.user import user_router
from src.api.middleware.auth.jwt_middleware import JWTMiddleware
from src.core.exceptions.base.base_exceptions import BaseApplicationException
from src.infrastructure.database import Base, engine

load_dotenv()

HOST = os.getenv("API_HOST")
PORT = int(os.getenv("API_PORT"))  # type: ignore

app = FastAPI()

app.add_middleware(JWTMiddleware)


@app.exception_handler(BaseApplicationException)
async def base_exception_handler(
    request: Request, exc: BaseApplicationException
):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )


app.include_router(user_router.router, prefix="/api-v1")

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)  # type: ignore
