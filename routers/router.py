from fastapi import APIRouter, HTTPException, status
from .schemas import UserRegister, UserLogin, UserUpdatePassword
from . import database

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Here's the root of the API."}

# Registration endpoint
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def user_register(user : UserRegister):
    if database.create_user(email=user.email, username=user.username, password=user.password):
        return {"message": f"User {user.username} created successfully."}
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Failed to create user. Email or username may already exist, or password is not strong enough."
    )

# Login endpoint
@router.get("/login")
async def user_login(user : UserLogin):
    if database.login_user(user.username, user.password):
        return {"status": True, "message": f"User {user.username} logged in successfully."}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password.")

# Update password endpoint
@router.put("/update-password")
async def user_update_password(user : UserUpdatePassword):
    if database.update_user_password(user.username, user.old_password, user.new_password):
        return {"status": True, "message": f"User {user.username} password updated successfully."}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to update password. Please check your old password and ensure the new password meets the requirements."
    )