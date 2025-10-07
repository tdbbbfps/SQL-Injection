from fastapi import APIRouter
from .schemas import UserRegister, UserLogin, UserUpdatePassword
from .models import User
from .database import create_user, login_user, update_user_password

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Here's the root of the API."}

@router.post("/user-register")
async def user_register(user : UserRegister):
    if create_user(user):
        return {"message": f"User {user.username} created successfully."}
    return {"message": "Failed to create user."}

@router.get("/user-login")
async def user_login(user : UserLogin):
    if login_user(user.username, user.password):
        return {"status": True, "message": f"User {user.username} logged in successfully."}
    return {"status": False, "message": "Invalid username or password."}

@router.put("/user-update-password")
async def user_update_password(user : UserUpdatePassword):
    if update_user_password(user.username, user.old_password, user.new_password):
        return {"status": True, "message": f"User {user.username} password updated successfully."}
    return {"status": False, "message": "Failed to update password. Please check your old password and ensure the new password meets the requirements."}