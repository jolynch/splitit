from flask import Flask, session, redirect, url_for, g
from flask.ext.sqlalchemy import SQLAlchemy
from splitter import Bid as SplitterBid
from surplus_maximizer import SurplusMaximizer
import pdb
import os

base = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(base, 'site.db')
db = SQLAlchemy(app)

def register_blueprints():
    import views_setup, views_auction
    app.register_blueprint(views_setup.setup_views)
    app.register_blueprint(views_auction.auction_views)

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'IShouldntTellAnyoneThisString'
    register_blueprints()
    app.run()
