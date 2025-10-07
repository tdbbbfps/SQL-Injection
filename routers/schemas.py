from pydantic import BaseModel

class UserRegister(BaseModel):
    email : str
    username : str
    password : str

class UserLogin(BaseModel):
    username : str
    password : str

class UserUpdatePassword(BaseModel):
    username : str
    old_password : str
    new_password : str
