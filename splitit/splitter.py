""" Basic splitter interface """
import mwmatching
from pprint import pprint

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
        print "Attempting to split:"
        print "== Items: "
        pprint(items)
        print "== between:"
        pprint(actors)
        print "== as per the bids:"
        pprint(bids)

        print "== Generating sufficent fake items and actors for a full auction =="


        averages = self.calc_averages(items, bids)
        bid_dict = {}
        for bid in bids:
            bid_dict[(bid.item, bid.actor)] = bid

        edges = []
        for i in range(len(items)):
            for j in range(len(actors)):
                if (items[i], actors[j]) in bid_dict:
                    bid = bid_dict[(items[i], actors[j])]
                    edges.append((i, len(items) + j, self.score(bid, averages)))

        # Actually do the auction, maximizing whatever score function we have
        mw = mwmatching.maxWeightMatching(edges, maxcardinality=True)
        result = {}
        for i in range(len(items)):
            if mw[i] != -1:
                winner = actors[mw[i] - len(items)]
                result[items[i]] = (winner, bid_dict[(items[i], winner)].amount)
            else:
                result[items[i]] = None

        # If we have left over items then continue auctioning off items
        # TODO: figure out if this is "good enough" or actually optimal, I
        # really don't think that it is optimal.  I think that this is greedy
        remaining_items = [item for item in items if result[item] is None]
        if len(remaining_items) > 0:
            remaining_result = self.split(remaining_items, actors, bids, exclusive)
            result = dict(result.items() + remaining_result.items())

        return result

    def score(self, bid, averages):
        return bid.amount



