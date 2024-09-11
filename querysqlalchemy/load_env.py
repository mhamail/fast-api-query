import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()
# print(type(int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))))

# class Settings(BaseSettings):
#     SECRET_KEY: str
#     ALGORITHM: str
#     ACCESS_TOKEN_EXPIRE_MINUTES: int

#     class Config:
#         env_file = ".env"


# env = Settings()


# SECRET_KEY = env.SECRET_KEY
# ALGORITHM = env.ALGORITHM
# ACCESS_TOKEN_EXPIRE_MINUTES = env.ACCESS_TOKEN_EXPIRE_MINUTES

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
db = os.getenv("db")
