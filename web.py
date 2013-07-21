from flask import Flask, render_template, request, session, redirect, url_for, g
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/db.sqlite3"
db = SQLAlchemy(app)

def ensure_auction(f):
    @wraps(f)
    def tomato(*args, **kwargs):
        if 'auction_id' not in session:
            return redirect(url_for('step1'))
        else:
            g.auction = db.session.query(Auction).get(session['auction_id'])
            if g.auction == None:
                return redirect(url_for('step1'))
        return f(*args, **kwargs)
    return tomato

@app.route('/')
def homepage():
    session['auction_id'] = None
    return render_template('homepage.html')

@app.route('/step/1', methods=['GET'])
def step1():
    if session['auction_id'] == None:
        auction = Auction()
        db.session.add(auction)
        db.session.commit()
        session['auction_id'] = auction.id
    else:
        auction = db.session.query(Auction).get(session['auction_id'])
    return render_template('step1.html')

@app.route('/step/1', methods=['POST'])
@ensure_auction
def step1_process():
    for name in request.form.getlist('people[]'):
        p = Participant(name, session['auction_id'])
        db.session.add(p)
    db.session.commit()
    return redirect(url_for('step2'))

@app.route('/step/2', methods=['GET'])
@ensure_auction
def step2():
    participants = g.auction.participants.count()

    return render_template('step2.html', participant_count=participants)

@app.route('/step/2', methods=['POST'])
@ensure_auction
def step2_process():
    for item in request.form.getlist('items[]'):
        i = Item(item, g.auction.id)
        db.session.add(i)
    db.session.commit()
    return redirect(url_for('step3'))

@app.route('/step/3', methods=['GET'])
@ensure_auction
def step3():
    items = g.auction.items.count()

    return render_template('step3.html', item_count=items)

@app.route('/step/3', methods=['POST'])
@ensure_auction
def step3_process():
    g.auction.total_bid = request.form['total_bid']
    db.session.add(g.auction)
    db.session.commit()

    return redirect(url_for('auction', auction_id=g.auction.id))

@app.route('/auction/<int:auction_id>')
def auction(auction_id):
    auction = db.session.query(Auction).get(auction_id)
    if auction == None:
        return "404 page not found :("
    return str(auction)

class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_bid = db.Column(db.Integer)

    def __init__(self, total_bid=0):
        self.total_bid = total_bid

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id'))
    auction = db.relationship('Auction', backref=db.backref('participants', lazy='dynamic'))

    def __init__(self, name, auction_id):
        self.name = name
        self.auction_id = int(auction_id)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id'))
    auction = db.relationship('Auction', backref=db.backref('items', lazy='dynamic'))

    def __init__(self, name, auction_id):
        self.name = name
        self.auction_id = int(auction_id)

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'IShouldntTellAnyoneThisString'
    db.create_all()
    app.run()
