## create poetry project

```
poetry new newpoetry
```

## install dependencies

```
poetry add fastapi "uvicorn[standard] alembic"
```

## command to run server

```poetry run uvicorn backend.main:app --host 0.0.0.0 --port 8002

```

## configure poetry that run server with uvicorn directly

```
- poetry shell
- uvicorn backend.main:app --port 8002 --reload
```

## alembic

poetry run alembic
poetry run alembic init alembic
poetry run alembic revision --autogenerate -m "Add User, Address, and Role models"
poetry run alembic upgrade head

# enter in sql terminal

sqlite3 query.db

- .mode column: Sets the output mode to a columnar format, which aligns the columns for better readability.
- .headers on: Ensures that column headers are included in the output.
- SELECT \* FROM users;: Displays all the rows in the users table.

```
   .mode column
   .headers on
   .mode csv
   .mode list
   .mode table
   SELECT \* FROM alembic_version;
```

### drop alembic

> DROP TABLE alembic_version;
> reinit
