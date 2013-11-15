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
        if 'auction_id' not in session:
            return redirect(url_for('setup.step1'))
        else:
            g.auction = db.session.query(Auction).get(session['auction_id'])
            if g.auction == None:
                return redirect(url_for('setup.step1'))
        return f(*args, **kwargs)
    return tomato

