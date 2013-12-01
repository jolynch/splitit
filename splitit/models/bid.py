from splitit.models.shared import db


class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    item = db.relationship('Item', backref=db.backref('bids', lazy='dynamic', cascade='all,delete'))

    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    participant = db.relationship('Participant', backref=db.backref('bids', lazy='dynamic', cascade='all,delete'))

    def __init__(self, item_id, participant_id, amount):
        self.item_id = int(item_id)
        self.participant_id = int(participant_id)
        self.amount = int(amount)
