from typing import List
from fastapi import APIRouter, Path
from sqlalchemy.orm.query import Query
from querysqlalchemy.baseClass.user import UserCreate
from querysqlalchemy.controller import role
from querysqlalchemy.baseClass.role import RoleCreate, ResponseRole, RoleDisplay
from querysqlalchemy.lib.dependencies import db_dependency
from querysqlalchemy.models.user import Role
from querysqlalchemy.lib.helpers import dbModel

router = APIRouter(prefix="/role", tags=["role"])


@router.post("/create", response_model=ResponseRole)
def create(request: RoleCreate, db: db_dependency):
    data = role.create(db, request)
    print(data)
    return {"message": "Role created successfully", "data": data}


@router.get("")
def list(db: db_dependency):
    model: Query = dbModel(db, Role)
    data = role.list(model)
    return data


@router.get("/get_roles_with_users")
def list(db: db_dependency):
    data = role.get_roles_with_users(db)
    return data


@router.delete("/remove/{id}")
def remove(
    db: db_dependency,
    id: int = Path(gt=0),
):
    role.delete(db, id)
    return {"message": "delete Successfully"}


@router.put("/update/{id}")
def update(db: db_dependency, request: RoleCreate, id: int = Path(gt=0)):
    data = role.update(db, id, request)
    return {"message": "Role Update successfully", "data": data}


@router.put(
    "/update/{role_id}/{user_id}",
)
def update(
    db: db_dependency,
    requestRole: RoleCreate,
    requestUser: UserCreate,
    role_id: int = Path(gt=0),
    user_id: int = Path(gt=0),
):
    role.updateTransaction(db, role_id, user_id, requestRole, requestUser)
    return {"message": "ok"}
