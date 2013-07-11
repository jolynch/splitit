""" This splitter attempts to maximize apparent total surplus """
from splitter import Splitter
from splitter import Bid

class SurplusMaximizer(Splitter):
    def score(self, bid, averages):
        return bid.amount - averages[bid.item]

items = ["Room 1", "Room 2", "Room 3"]
bids = [Bid("Room 1", "Joey", 10), Bid("Room 1", "Josh", 15),
        Bid("Room 2", "Joey", 5), Bid("Room 2", "Josh", 0)]
s = Splitter()
print s.split(items, ["Joey", "Josh"], bids)
