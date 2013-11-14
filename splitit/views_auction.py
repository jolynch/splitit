from decorators import ensure_auction
from flask import Blueprint, render_template, current_app, session, request, redirect, url_for, g
from models.auction import Auction
from models.bid import Bid
from models.item import Item
from models.participant import Participant
from web import db

auction_views = Blueprint('auction', __name__, template_folder = 'templates')

@auction_views.route('/auction/<int:auction_id>')
def auction(auction_id):
    g.auction = db.session.query(Auction).get(auction_id)
    if g.auction == None:
        return "404 page not found :("
    if g.auction.total_bid > 0:
        if g.auction.is_complete():
            return str(g.auction.calculate())
        else:
            return render_template('auction.html',       \
                    participants=g.auction.participants, \
                    total_bid=g.auction.total_bid,       \
                    items=g.auction.items,               \
                    )
    else:
        return "This auction has not been prepared yet :("

@auction_views.route('/auction/<int:auction_id>/<int:participant_id>', methods=['GET'])
def auction_bid(auction_id, participant_id):
    auction = db.session.query(Auction).get(auction_id)
    participant = db.session.query(Participant).get(participant_id)
    if auction == None or participant == None:
        return "404 page not found :("
    return render_template('auction_bid.html', \
            auction=auction, \
            participant=participant, \
            items=auction.items)

@auction_views.route('/auction/<int:auction_id>/<int:participant_id>', methods=['POST'])
def auction_bid_process(auction_id, participant_id):
    auction = db.session.query(Auction).get(auction_id)
    participant = db.session.query(Participant).get(participant_id)
    for i in auction.items:
        key = "item_bid[" + str(i.id) + "]"
        bid = request.form[key]
        if bid != None:
            b = Bid(i.id, participant.id, bid)
            db.session.add(b)
    db.session.commit()
    return redirect(url_for('auction.auction', auction_id=auction.id))
