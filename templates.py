from pydantic import BaseModel,EmailStr
import datetime
from pydantic_settings import BaseSettings

class Post(BaseModel):
    id:int
    title:str
    content:str

class Post_res(BaseModel):
    title:str
    content:str
    user_email:str

class User(BaseModel):
    id:int
    email:EmailStr
    password:str

class User_res(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime.datetime

class Login(BaseModel):
    email:EmailStr
    password:str

class token(BaseModel):
    access_token:str
    token_type:str
