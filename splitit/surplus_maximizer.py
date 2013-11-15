""" This splitter attempts to maximize apparent total surplus """
from splitter import Splitter
from splitter import Cost

class SurplusMaximizer(Splitter):
    def score(self, cost, averages):
        return cost.amount - averages[cost.item]
