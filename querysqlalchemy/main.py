from fastapi import FastAPI

app = FastAPI()

from querysqlalchemy.lib.database import engine

from querysqlalchemy.models.base import Base
from querysqlalchemy.route import user, role


@app.get("/hello")
async def root():
    return {"message": "Welcome to the FastAPI server!"}


app.include_router(user.router)
app.include_router(role.router)


# Base.metadata.drop_all(engine)

# Base.metadata.create_all(engine)
