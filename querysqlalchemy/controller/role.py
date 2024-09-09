from fastapi import HTTPException
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session
from querysqlalchemy.baseClass.role import RoleCreate
from querysqlalchemy.baseClass.user import UserCreate
from querysqlalchemy.models.user import Role, User
from typing import Type, List
from sqlalchemy.orm import joinedload


def create(db: Session, request: RoleCreate):
    create_role = Role(
        name=request.name,
    )
    db.add(create_role)
    db.commit()
    db.refresh(create_role)
    print(create_role)
    return create_role


def delete(db: Session, id: int):
    item = db.query(Role).filter(Role.id == id).first()
    db.delete(item)
    db.commit()


def update(db: Session, id: int, request: RoleCreate):
    item = db.query(Role).filter(Role.id == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found.")
    item.name = request.name
    db.commit()
    # Commit the changes
    db.commit()

    # Refresh the session to get the updated item
    db.refresh(item)

    # Return the updated item
    return item


## Transaction
def updateTransaction(
    db: Session,
    role_id: int,
    user_id: int,
    requestRole: RoleCreate,
    requestUser: UserCreate,
):
    # role update
    role = db.query(Role).filter(Role.id == role_id).first()
    role.name = requestRole.name
    # raise HTTPException(detail="Something went wrong")
    # user update
    user = db.query(User).filter(User.id == user_id).first()
    user.first_name = requestUser.first_name
    user.last_name = requestUser.last_name
    user.email = requestUser.email
    user.role_id = requestUser.role_id

    db.commit()


## List Function ##
def list(model: Query):
    data = model.all()
    return data


def get_roles_with_users(db: Session):
    data = db.query(Role).options(joinedload(Role.users)).all()
    return data
