import os
import sys

from flask import Flask
from models.shared import db


sys.path.append(os.getcwd())
base = os.path.abspath(os.path.dirname(__file__))


def make_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(base, 'site.db')
    app.secret_key = 'IShouldntTellAnyoneThisString'
    register_blueprints(app)
    db.init_app(app)
    return app


def register_blueprints(app):
    import views_auction
    import views_setup
    app.register_blueprint(views_setup.setup_views)
    app.register_blueprint(views_auction.auction_views)


def run_webserver(app):
    app.debug = True
    app.run()

splitit_app = make_app()

if __name__ == '__main__':
    run_webserver(splitit_app)
