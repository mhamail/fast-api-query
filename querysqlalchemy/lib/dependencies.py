from datetime import datetime, timezone
from fastapi import HTTPException
from typing import Annotated, Any, Dict, Optional, Union
from fastapi import status
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


from querysqlalchemy.controller.auth import decode_token
from querysqlalchemy.lib.database import get_db
from sqlalchemy.orm.session import Session


db_dependency = Annotated[Session, Depends(get_db)]


class RequireTokenClass(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Union[Dict[str, Any], None]:
        creds: Optional[HTTPAuthorizationCredentials] = await super().__call__(request)
        if creds is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization credentials are missing",
            )

        token = creds.credentials
        token_data = decode_token(token)
        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="401 Error,Invalid or expired token",
            )

        # print(token_data)
        if not self.token_valid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token"
            )

        self.verify_token_data(token_data)

    def token_valid(self, token: str) -> bool:

        token_data = decode_token(token)

        return token_data is not None

    def verify_token_data(self, token_data: Dict[str, Any]) -> None:
        return token_data
        raise NotImplementedError("Please override this method in child classes")


class AccessTokenBearer(RequireTokenClass):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token",
            )


class RefreshTokenBearer(RequireTokenClass):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token",
            )


require_token = Depends(RequireTokenClass())
