from decorators import ensure_auction
from flask import Blueprint, render_template, current_app, session, request, redirect, url_for, g
from models.item import Item
from models.participant import Participant
from models.auction import Auction
from web import db

setup_views = Blueprint('setup', __name__, template_folder = 'templates')

@setup_views.route('/')
def homepage():
    session['auction_id'] = None
    auctions = Auction.query.all()
    return render_template('homepage.html', auctions=auctions)

@setup_views.route('/step/1', methods=['GET'])
def step1():
    if session['auction_id'] == None:
        auction = Auction()
        db.session.add(auction)
        db.session.commit()
        session['auction_id'] = auction.id
    else:
        auction = db.session.query(Auction).get(session['auction_id'])
    return render_template('step1.html')

@setup_views.route('/step/1', methods=['POST'])
@ensure_auction
def step1_process():
    for name in request.form.getlist('people[]'):
        p = Participant(name, session['auction_id'])
        db.session.add(p)
    db.session.commit()
    return redirect(url_for('setup.step2'))

@setup_views.route('/step/2', methods=['GET'])
@ensure_auction
def step2():
    participants = g.auction.participants.count()

    return render_template('step2.html', participant_count=participants)

@setup_views.route('/step/2', methods=['POST'])
@ensure_auction
def step2_process():
    for item in request.form.getlist('items[]'):
        i = Item(item, g.auction.id)
        db.session.add(i)
    db.session.commit()
    return redirect(url_for('setup.step3'))

@setup_views.route('/step/3', methods=['GET'])
@ensure_auction
def step3():
    items = g.auction.items.count()

    return render_template('step3.html', item_count=items)

@setup_views.route('/step/3', methods=['POST'])
@ensure_auction
def step3_process():
    g.auction.total_bid = request.form['total_bid']
    g.auction.name = request.form['name']
    db.session.add(g.auction)
    db.session.commit()

    return redirect(url_for('auction.auction', auction_id=g.auction.id))
