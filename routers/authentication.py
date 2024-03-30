from fastapi import HTTPException,APIRouter,status,Depends
from templates import Login
from passlib.context import CryptContext
from raw_sql import connect,verify
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import Oauth
from config import Settings

conn = connect(Settings().db_port,Settings().db_username,Settings().db_password,Settings().db_name)
auth_router = APIRouter()
hasher = CryptContext(schemes=['bcrypt'])

@auth_router.post("/login",status_code=status.HTTP_202_ACCEPTED)
def login(info:OAuth2PasswordRequestForm=Depends()):
    hashed_pass = None
    if type(verify.login_check(conn,info.username)) == dict:
        hashed_pass = verify.login_check(conn,info.username).get("password")   
    cond = hasher.verify(info.password,hashed_pass)
    if not cond:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Email or Password")
    access_token = Oauth.create_access_token(data={"email":info.username})
    return({"access_token":access_token,"token_type":"bearer"})