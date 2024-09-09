from typing import Annotated

from fastapi import Depends

from querysqlalchemy.lib.database import get_db
from sqlalchemy.orm.session import Session

db_dependency = Annotated[Session, Depends(get_db)]
