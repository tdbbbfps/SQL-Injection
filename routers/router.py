from fastapi import APIRouter
from .schemas import UserCreate
from .database import create_user

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Here's the root of the API."}

@router.post("/register-user")
async def register_user(user : UserCreate):
    if create_user(user.username, user.password):
        return {"message": f"User {user.username} created successfully."}
    return {"message": "Failed to create user."}

