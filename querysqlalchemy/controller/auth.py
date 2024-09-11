from datetime import timedelta, datetime, timezone
from http.client import HTTPException
from typing import Dict, Optional

from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from querysqlalchemy.baseClass.auth_user import Login
from querysqlalchemy.lib.database import get_db
from querysqlalchemy.models.auth import AuthUser
from sqlalchemy.orm.session import Session
from jose import jwt, JWTError

from fastapi import Depends, Request, status

from querysqlalchemy.utils.hash import Hash

from querysqlalchemy.load_env import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def get_user_by_email(db: Session, email: str):
    return db.query(AuthUser).filter(AuthUser.email == email).first()


def create_access_token(
    user_data: dict, expiry: Optional[timedelta] = None, refresh: Optional[bool] = False
):
    payload = {
        "user": user_data,
        "exp": datetime.now(timezone.utc)
        + (
            expiry
            if expiry is not None
            else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        ),
        "refresh": refresh,
    }

    token = jwt.encode(payload, env.SECRET_KEY, algorithm=ALGORITHM)
    return token


def authenticate_user(email: str, password: str, db):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not Hash.verify(password, user.password):
        print("Password verification failed")
        return False
    return user


def login(request: Login, db: Session = Depends(get_db)):
    print(request)
    user = authenticate_user(request.email, request.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )

    access_token = create_access_token(
        user_data={"email": user.email, "user_id": str(user.id)},
    )
    refresh_token = create_access_token(
        user_data={"email": user.email, "user_id": str(user.id)},
        refresh=True,
        expiry=timedelta(days=30),
    )
    exp_time = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return JSONResponse(
        content={
            "message": "Login successful",
            "token_type": "bearer",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {"email": user.email, "id": str(user.id)},
            "exp": exp_time.isoformat(),
        }
    )


def refreshToken(token_details):
    print(token_details)
    if token_details:
        user_data = token_details["user"]
        access_token = create_access_token(user_data)
        exp_time = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return JSONResponse(
            content={
                "access_token": access_token,
                "user": user_data,
                "exp": exp_time.isoformat(),
            }
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
    )


def decode_token(token: str) -> Optional[Dict]:
    try:
        token_data = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": True},  # Ensure expiration is verified
        )

        return token_data

    except JWTError as e:
        print(f"Token decoding failed: {e}")
        return None
