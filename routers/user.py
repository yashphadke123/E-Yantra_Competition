from passlib.context import CryptContext
from fastapi import status,APIRouter
from templates import User,User_res
from raw_sql import connect,get,post
from config import Settings

conn = connect(Settings().db_port,Settings().db_username,Settings().db_password,Settings().db_name)
hasher = CryptContext(schemes=['bcrypt'])
user_router = APIRouter()

@user_router.post("/user",status_code=status.HTTP_201_CREATED)
def create_user(user:User):
    return post.single_element(conn,["id","email","password"],[user.id,user.email,hasher.hash(user.password)],"users")

@user_router.get("/user",response_model=User_res)
def find_users(id:int):
    return get.get_one_post(conn,"users",id)