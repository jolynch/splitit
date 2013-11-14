from web import db
from surplus_maximizer import SurplusMaximizer
from splitter import Bid as SplitterBid

class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    total_bid = db.Column(db.Integer)

    def __init__(self, total_bid=0):
        self.total_bid = total_bid

    def is_complete(self):
        return all([p.has_completed_bidding() for p in self.participants.all()])

    def splitter_bids(self):
        return [SplitterBid(i.name, b.participant.name, b.amount) for i in self.items for b in i.bids]

    def calculate(self):
        item_splitter = SurplusMaximizer()
        result = item_splitter.split(                       \
                 [i.name for i in self.items.all()],        \
                 [p.name for p in self.participants.all()], \
                 self.splitter_bids()                       \
                 )
        return result
