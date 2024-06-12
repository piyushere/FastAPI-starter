import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.controllers.routes import router
from src.config.db import sync_engine, async_engine
from src.models import generate_models
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifecycle(app: FastAPI):
    generate_models(sync_engine)
    yield
    await async_engine.dispose()


app = FastAPI(
    title="Todos API",
    lifespan=lifecycle
)
app.include_router(router, prefix='/api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)
