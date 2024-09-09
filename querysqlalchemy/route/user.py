from datetime import date
import json
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Path, Query
from fastapi.encoders import jsonable_encoder
from urllib.parse import unquote
import urllib.parse

from querysqlalchemy.controller import user
from querysqlalchemy.baseClass.user import UserCreate, UserDisplay
from querysqlalchemy.lib.dependencies import db_dependency
from querysqlalchemy.lib.helpers import dbModel
from querysqlalchemy.models.user import User
from querysqlalchemy.utils.utility import extractTupleArray


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/create", response_model=UserDisplay)
def create(request: UserCreate, db: db_dependency):
    return user.create(db, request)


# search
@router.post("/searchbyname/")
def create(name: str, db: db_dependency):
    return user.getSearchByName(db, name)


@router.get("/pipeline", response_model=List[UserDisplay])
def pipeline(
    db: db_dependency,
    searchTerm: Optional[str] = None,
    searchTerms: Optional[str] = Query(None),
):
    columnFilters = []
    if searchTerms:
        terms = json.loads(searchTerms)
        columnFilters = extractTupleArray(terms)
    filters = {
        "search_terms": columnFilters,  # [("first_name", "string"), ("id", 1)],
        "search_term": searchTerm,
        "global_search_terms": ["first_name", "last_name", "id"],
        "number_range": ("id", 1, 10),
        "date_range": ("created_at", "8-9-2024", "31-12-2024"),
    }

    return user.pipeline(db, filters)


@router.delete("/remove/{id}")
def remove(
    db: db_dependency,
    id: int = Path(gt=0),
):
    user.delete(db, id)
    return {"message": "delete Successfully"}


@router.get("", response_model=List[UserDisplay])
def list(db: db_dependency):
    return user.list(db)


@router.get("/list", response_model=List[UserDisplay])
def list(db: db_dependency):
    return user.list2(dbModel(db, User))


@router.get("/join", description="join with role")
def list(db: db_dependency):
    return user.join(db)


@router.get(
    "/join_filter",
    description="join with role and filter role name",
)
def list(db: db_dependency):
    return user.join_filter(db)


@router.get("/order_by", description="order by first name")
def list(db: db_dependency):
    return user.order_by(dbModel(db, User))


@router.get(
    "/order_by_desc",
    description="order by desc first name",
)
def list(db: db_dependency):
    return user.order_by_desc(db)


@router.get(
    "/order_by_users",
    description="order by first name and last name in desc order",
)
def list(db: db_dependency):
    return user.order_by_users(dbModel(db, User))


@router.get(
    "/limit",
    description="limit the list",
)
def list(db: db_dependency):
    return user.limit(dbModel(db, User))


@router.get(
    "/count",
    description="count the list",
)
def list(db: db_dependency):
    return user.countList(dbModel(db, User))


@router.get(
    "/offset",
    description="skip the list",
)
def list(db: db_dependency):
    return user.offset(dbModel(db, User))
