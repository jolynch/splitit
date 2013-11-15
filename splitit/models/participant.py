from splitit.models.shared import db


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id'))
    auction = db.relationship('Auction', backref=db.backref('participants', lazy='dynamic'))

    def __init__(self, name, auction_id):
        self.name = name
        self.auction_id = int(auction_id)

    def has_completed_bidding(self):
        return self.bids.count() > 0
