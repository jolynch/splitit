from functools import wraps

from flask import Flask
from flask import g
from flask import redirect
from flask import session
from flask import url_for
from models.auction import Auction
from models.shared import db


def ensure_auction(f):
    @wraps(f)
    def tomato(*args, **kwargs):
        return f(*args, **kwargs)
    return tomato

def lookup_or_404(model, model_id, name):
    def actually_lookup(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            kwargs[name] = model.query.get_or_404(kwargs[model_id])
            return func(*args, **kwargs)
        return wrapper
    return actually_lookup

