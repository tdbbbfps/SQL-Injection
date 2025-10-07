from pydantic import BaseModel

class User(BaseModel):
    id : int
    email : str
    username : str
    password : str

class UserCreate(BaseModel):
    email : str
    username : str
    password : str
