from datetime import date
from typing import Any, List, Optional
from sqlalchemy import Tuple, and_, between, desc, or_, select
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query
from querysqlalchemy.baseClass.user import UserCreate
from querysqlalchemy.models.user import Address, User, Role
from sqlalchemy.orm import joinedload

from querysqlalchemy.utils.utility import parse_date


def create(db: Session, request: UserCreate):
    # Create the Address instance if address data is provided
    address_instance = None
    if request.address:
        address_instance = Address(
            postcode=request.address.postcode, city=request.address.city
        )
    create_user = User(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        father_name=request.father_name,
        role_id=request.role_id,
        phone=request.phone,
        address=address_instance,  # Associate the Address with the User
    )
    db.add(create_user)
    db.commit()
    db.refresh(create_user)
    return create_user


def delete(db: Session, id: int):
    item = db.query(User).filter(User.id == id).first()
    db.delete(item)
    db.commit()


def getSearchByName(db: Session, name: str):
    data = db.query(User).filter(User.first_name.like(f"%{name}%")).all()
    return data


## List Function Queries##
def list(db: Session):
    data = db.query(User).all()
    return data


def list2(model: Query):
    data = model.all()
    return data


# join method
def join(db: Session):
    data = (
        db.query(User)
        .outerjoin(Role, User.role_id == Role.id)
        .outerjoin(Address, User.id == Address.user_id)
        .options(joinedload(User.role))
        .options(joinedload(User.address))
        .all()
    )
    # db.query(User).options(joinedload(User.role)).all()
    return data


# join with filter
def join_filter(db: Session):
    data = db.query(User).join(User.role).filter(Role.name == "admin").all()
    return data


# orderBy
def order_by(model: Query):
    data = model.order_by(User.first_name).all()
    return data


def order_by_desc(db: Session):
    data = db.query(User).order_by(desc(User.first_name)).all()
    return data


def order_by_users(model: Query):
    data = model.order_by(desc(User.first_name)).order_by(desc(User.last_name)).all()
    return data


# --------------------------------------------


# pagination
def limit(model: Query):
    data = model.limit(3).all()
    return data


def offset(model: Query):
    data = model.offset(3).all()
    return data


def countList(model: Query):
    data = model.count()
    return data


def statement(db: Session):
    data = db.query(User).join(Role, User.role_id == Role.id).all()
    return data


# def list(db: Session):
#     # Query with join to include role information
#     stmt = (
#         select(User)
#         .join(Role, User.role_id == Role.id)
#         .options(joinedload(User.role))  # Ensures that the role relationship is loaded
#     )
#     users_with_roles = db.execute(stmt).scalars().all()
#     return users_with_roles
# ----------------------------------------------

Model = User


# def filter_by_column(query, column, value, operator="=="):
#     if operator == "==":
#         return query.filter(column == value)
#     elif operator == ">":
#         return query.filter(column > value)
#     elif operator == "<":
#         return query.filter(column < value)
#     elif operator == "like":
#         return query.filter(column.like(f"%{value}%"))
#     else:
#         raise ValueError("Unsupported operator")


# def filter_by_number_range(query, number_column, min_value, max_value):
#     return query.filter(number_column.between(min_value, max_value))


# query filter
# def apply_filters(
#     query: Query,
#     date_range=None,
#     column_filters=None,
#     search_terms=None,
#     search_term=None,
#     global_search_terms=None,
#     number_range=None,
# ):
# if date_range:
#     start_date, end_date = date_range
#     query = query.filter(
#         and_(Model.date_column >= start_date, Model.date_column <= end_date)
#     #     )

#     # if column_filters:
#     #     for column_name, value, operator in column_filters:
#     #         column = getattr(
#     #             Model, column_name
#     #         )  # Adjust 'Model' to your actual model class
#     #         query = filter_by_column(query, column, value, operator)

#     if search_terms:
#         query = filter_by_search_terms(query, search_terms)
#     if search_term and global_search_terms:
#         query = filter_by_global_search_terms(query, global_search_terms, search_term)

# if number_range:
#     number_column, min_value, max_value = number_range
#     query = filter_by_number_range(query, number_column, min_value, max_value)

#     return query


# filters = {
#     # "date_range": (date(2024, 1, 1), date(2024, 12, 31)),
#     # "column_filters": [("age", 25, ">"), ("status", "active", "==")],
#     # "search_terms": [("first_name", "string"), ("id", 1)],
#     "global_search_terms": ["first_name", "last_name", "id"],
#     "search_term": "john",
#     # "number_range": (Model.salary, 50000, 100000),
# }


def filter_by_data_range(
    query, column_name, start_date_str, end_date_str, formats: Optional[List] = None
):
    data_column = getattr(Model, column_name)
    start_date = parse_date(start_date_str)
    end_date = parse_date(end_date_str)
    return query.filter(and_(data_column >= start_date, data_column <= end_date))


def filter_by_number_range(query, column_name, min_value, max_value):
    column = getattr(Model, column_name)
    return query.filter(column.between(min_value, max_value))


def filter_by_search_terms(query, search_terms):
    search_filters = []
    for column_name, search_term in search_terms:
        column = getattr(Model, column_name)
        # Check if the term is a string to use `like` filter, otherwise use equality filter
        if isinstance(search_term, str):
            search_filters.append(column.like(f"%{search_term}%"))
        else:
            search_filters.append(column == search_term)

    return query.filter(and_(*search_filters))


def filter_by_global_search_terms(
    query: Query, global_search_terms: List[str], search_term: str
):
    global_search_filters = []
    for column_name in global_search_terms:
        # column = Model[column_name]
        column = getattr(Model, column_name)
        global_search_filters.append(column.like(f"%{search_term}%"))
    return query.filter(or_(*global_search_filters))


def apply_filters(
    query: Query,
    search_terms=None,
    search_term=None,
    global_search_terms=None,
    number_range=None,
    date_range=None,
):

    if search_terms:
        query = filter_by_search_terms(query, search_terms)
    if search_term and global_search_terms:
        query = filter_by_global_search_terms(query, global_search_terms, search_term)
    if number_range:
        column_name, min_value, max_value = number_range
        query = filter_by_number_range(query, column_name, min_value, max_value)
    if date_range:
        column_name, start_date, end_date = date_range
        query = filter_by_data_range(query, column_name, start_date, end_date)

    print(query)
    return query


def pipeline(db: Session, filters: dict[str, any]):
    query = db.query(User)
    get_query = apply_filters(query, **filters)
    results = get_query.all()
    return results
