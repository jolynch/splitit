from splitit.models.shared import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id'))
    auction = db.relationship('Auction', backref=db.backref('items', lazy='dynamic'))

    def __init__(self, name, auction_id):
        self.name = name
        self.auction_id = int(auction_id)
