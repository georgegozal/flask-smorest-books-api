from sqlalchemy.sql.elements import ClauseElement
from flask import abort


def get_or_create(db, model, defaults=None, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance, False
    else:
        params = {k: v for k, v in kwargs.items() if not isinstance(v, ClauseElement)}
        params.update(defaults or {})
        instance = model(**params)
        try:
            db.session.add(instance)
            db.session.commit()
            """
            except Exception:  # The actual exception depends on the specific
                database so we catch all exceptions. This is similar to the
                official documentation: https://docs.sqlalchemy.org/en/latest/orm/session_transaction.html
            """
        except Exception:
            db.session.rollback()
            instance = db.session.query(model).filter_by(**kwargs).one()
            return instance, False
        else:
            return instance, True


def get_or_404(model, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance
    abort(404)


def get_extension(filename):
    splited = filename.rsplit(".", 1)[1].lower()
    return f".{splited}".lower()
