from passlib.context import CryptContext
from fastapi import status,HTTPException,APIRouter,Depends
from templates import Post_res,Post
from typing import List
from raw_sql import connect,get,post,delete,update
import Oauth
from config import Settings

conn = connect(Settings().db_port,Settings().db_username,Settings().db_password,Settings().db_name)
hasher = CryptContext(schemes=['bcrypt'])
post_router = APIRouter()

@post_router.get("/",response_model=List[Post_res])
async def root(email:str = Depends(Oauth.current_user)):
    print(email)
    return get.get_all_posts(conn,"tweets")

@post_router.get("/get_one_post",response_model=Post_res)
async def get_one(id:int,email:str = Depends(Oauth.current_user)):
    if not get.get_one_post(conn,"tweets",id,email):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="post with id = {} was not found".format(id))
    return get.get_one_post(conn,"tweets",id,email)


@post_router.post("/post",status_code=status.HTTP_204_NO_CONTENT)
async def posting(inputs:Post,email:str = Depends(Oauth.current_user)):
    print(email)
    return post.single_element(conn,["id","title","content","user_email"],[inputs.id,inputs.title,inputs.content,email],"tweets")

@post_router.delete("/delete",status_code=status.HTTP_202_ACCEPTED)
async def delete_by_id(id:int,email:str = Depends(Oauth.current_user)):
    return delete.delete_id(conn,"tweets",id,email)

@post_router.put("/update")
async def updates(inputs:Post,email:str = Depends(Oauth.current_user)):
    return update.updating(conn,[inputs.title,inputs.content,inputs.id],"tweets",email)