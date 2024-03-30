from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    db_username:str
    db_password:str
    db_name:str
    db_port:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int

    class Config:
        env_file = ".env"

print(Settings().db_username)