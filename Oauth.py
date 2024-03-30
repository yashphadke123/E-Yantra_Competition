from jose import JWTError,jwt
import datetime as dt
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from config import Settings
SECRET_KEY = Settings().secret_key
ALGORITHM = Settings().algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = Settings().access_token_expire_minutes

ouath2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data:dict):
    to_encode = data.copy()
    expire_time = dt.datetime.utcnow() + dt.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire_time})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str,error:str):
    try:
        payload =jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email:str = payload.get("email")
        if email is None:
            raise error
    except JWTError:
        raise error
    return email
    
def current_user(token:str = Depends(ouath2_scheme)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect Email",headers={"www.Authenticate":"Bearer"})
    return verify_token(token=token,error=exception)