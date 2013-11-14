""" This splitter attempts to maximize apparent total surplus """
from splitter import Splitter
from splitter import Bid

class SurplusMaximizer(Splitter):
    def score(self, bid, averages):
        return bid.amount - averages[bid.item]
