from typing import Annotated, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel

from querysqlalchemy.baseClass.auth_user import AuthBase, Login, AuthUserDisplay
from querysqlalchemy.lib.dependencies import (
    db_dependency,
    require_token,
    RefreshTokenBearer,
)
from querysqlalchemy.controller import auth
from querysqlalchemy.models.auth import AuthUser
from querysqlalchemy.utils.hash import Hash


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
def createUser(request: AuthBase, db: db_dependency):
    db_user = auth.get_user_by_email(db, email=request.email)
    if db_user:
        raise HTTPException(status_code=400, detail="this user already exist")
    create_user = AuthUser(
        username=request.username,
        email=request.email,
        password=Hash.crypt(request.password),
    )
    db.add(create_user)
    db.commit()
    db.refresh(create_user)
    return create_user


@router.post("/login")
def login(request: Login, db: db_dependency):
    return auth.login(request, db)


@router.get("")
def list(db: db_dependency):
    return db.query(AuthUser).all()


@router.get("/verify")
def list(db: db_dependency, user_details=require_token):
    print(user_details)

    return db.query(AuthUser).all()


@router.get("/refresh_token")
def refreshToken(token_details=Depends(RefreshTokenBearer())):

    return auth.refreshToken(token_details)
