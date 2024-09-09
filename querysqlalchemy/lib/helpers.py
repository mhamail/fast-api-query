from querysqlalchemy.lib.dependencies import db_dependency


def dbModel(db: db_dependency, model: str):
    return db.query(model)
