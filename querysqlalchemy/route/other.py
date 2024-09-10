from typing import Any, Optional
from fastapi import APIRouter, Header
from pydantic import BaseModel


router = APIRouter()


##its work on postman only
@router.get("/get-header")
def get_header_value(
    authorization: str = Header(
        None, description="Authorization header with Bearer token"
    ),
    content_type: Optional[str] = Header(
        None, description="Content-Type header indicating the media type"
    ),
    accept: Optional[str] = Header(
        None,
        description="Accept header indicating the media types that are acceptable for the response",
    ),
) -> dict[str, Optional[str]]:
    request_headers = {
        "Authorization": authorization,
        "Content-Type": content_type,
        "Accept": accept,
    }
    return request_headers
