from flask import abort
from functools import wraps
from models.shared import db


def lookup_or_404(model, model_id, name):
    def actually_lookup(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            obj = db.session.query(model).get(kwargs[model_id])
            if obj:
                kwargs[name] = obj
            else:
                abort(404)
            return func(*args, **kwargs)
        return wrapper
    return actually_lookup
