import asyncio
from uvicorn import run
from fastapi import FastAPI
from db.db_setup import init_db
from routes.thread import router


def db_init_models():
    asyncio.run(init_db())


app = FastAPI(docs_url="/docs", redoc_url=None)

app.include_router(router)

if __name__ == "__main__":
    db_init_models()
    run("main:app", reload=True)
