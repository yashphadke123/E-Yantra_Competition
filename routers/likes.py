from fastapi import HTTPException,APIRouter,status,Depends
from templates import Login
from passlib.context import CryptContext
from raw_sql import connect,like
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import Oauth
from config import Settings

conn = connect(Settings().db_port,Settings().db_username,Settings().db_password,Settings().db_name)
like_router = APIRouter()
hasher = CryptContext(schemes=['bcrypt'])

@like_router.post("/likes")
def add_like(id:int,email:str = Depends(Oauth.current_user)):
    return like(conn,id,email)
