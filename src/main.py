import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from itsdangerous import URLSafeTimedSerializer
from starlette.middleware.sessions import SessionMiddleware

from api import api_router
from config import settings

app = FastAPI(title="IGStoryBooster")

app.add_middleware(
    DBSessionMiddleware,
    db_url=settings.database_uri,
    session_args={"expire_on_commit": False},
)
if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


secret_key = "some-secret-key"  # Replace this with your actual secret key
signer = URLSafeTimedSerializer(secret_key)

app.add_middleware(
    SessionMiddleware, secret_key=secret_key, max_age=3600 * 24  # Session age: 1 day
)
# Set all CORS enabled origins
if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix="")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="debug", reload=True)
    #app.run("main:app", host="127.0.0.1", port=8000, log_level="debug", reload=True)
