""" This splitter attempts to maximize apparent total surplus """
from splitter import Cost
from splitter import Splitter


class SurplusMaximizer(Splitter):
    def score(self, cost, averages):
        return cost.amount - averages[cost.item]
