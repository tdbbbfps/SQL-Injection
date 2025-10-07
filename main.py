from fastapi import FastAPI
from routers import router as user_router
import uvicorn

app = FastAPI(
    title="SQL TEST",
    version="1.0.0",
    description="A simple fastapi project with sql.",
)

app.include_router(user_router, prefix="/user", tags=["user"])

@app.get("/")
async def root():
    return {"message": "The root of the API."}
