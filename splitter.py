""" Basic splitter interface """

class Item(object):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return "Item(%s)" % self.name

class Actor(object):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return "Actor(%s)" % self.name

class Bid(object):
    def __init__(self, item, actor, amount):
        self.item = item
        self.actor = actor
        self.amount = amount

    def __eq__(self, other):
        return self.item   == other.item  and \
               self.actor  == other.actor and \
               self.amount == other.amount

    def __repr__(self):
        return "Bid(" + str(self.item) + ", " + str(self.actor) + \
                ", " + str(self.amount) + ")"

class Splitter(object):
    def calc_averages(self, items, bids):
        averages = {}
        for item in items:
            bids_for_item = [bid.amount for bid in bids if bid.item == item]
            if len(bids_for_item) > 0:
                averages[item] = float(sum(bids_for_item)) / len(bids_for_item)
            else:
                averages[item] = 0
        return averages

    def split(self, items, actors, bids, exclusive=True):
        averages = self.calc_averages(items, bids)
        item_to_bids = {}
        item_to_actor = {}
        for item in items:
            item_to_bids[item] = [bid for bid in bids if bid.item == item]

        if exclusive:


        return item_to_bids

items = [Item("Room 1"), Item("Room 2"), Item("Room 3")]
bids = [Bid(Item("Room 1"), "Joey", 10), Bid(Item("Room 1"), "Josh", 15)]
s = Splitter()
print s.split(items, ["Joey", "Josh"], bids)
