from fastapi import FastAPI
from routers.router import router as user_router
from routers.database import create_db as initialize_database
import uvicorn
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 在應用程式啟動時執行
    print("Initializing database...")
    if initialize_database():
        print("Database and table are ready.")
    else:
        print("Failed to initialize database.")
    yield
    # 在應用程式關閉時執行的清理工作 (如果需要)
    print("Application shutting down.")

app = FastAPI(
    title="SQL TEST",
    version="1.0.0",
    description="A simple fastapi project with sql.",
    lifespan=lifespan,
)

app.include_router(user_router, prefix="/user", tags=["user"])

@app.get("/")
async def root():
    return {"message": "The root of the API."}