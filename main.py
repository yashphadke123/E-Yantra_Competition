from fastapi import FastAPI
from routers import post,user,authentication,likes

app = FastAPI()
app.include_router(post.post_router)
app.include_router(user.user_router)
app.include_router(authentication.auth_router)
app.include_router(likes.like_router)