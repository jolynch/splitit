""" Basic splitter interface """
import mwmatching
from pprint import pprint
from util import lcm

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

        print "== Expanding the actors and items =="
        # This ensures that if we have more items than actors or more actors
        # than items, we ensure that we always return the optimal result
        def expand_list(lst, new_length):
            expanded_lst = lst * (new_length / len(lst))
            return [
                item + "-" + str(index / len(lst))
                for index, item
                in enumerate(expanded_lst)
            ]

        lcm_actors_items = lcm(len(actors), len(items))
        expanded_actors = expand_list(actors, lcm_actors_items)
        expanded_items = expand_list(items, lcm_actors_items)

        bid_dict = {}
        for bid in bids:
            bid_dict[(bid.item, bid.actor)] = bid

        exp_bid = {}
        for actor in expanded_actors:
            for item in expanded_items:
                root_actor = actor[:actor.rfind('-')]
                root_item = item[:item.rfind('-')]
                real_item = item[item.find('-')+1:] == '0'
                if real_item:
                    original_bid = bid_dict[(root_item, root_actor)]
                    exp_bid[(item, actor)] = Bid(item, actor, original_bid.amount)
                else:
                    exp_bid[(item, actor)] = Bid(item, actor, 0)

        bid_dict = exp_bid
        new_bids = [Bid(b.item, b.actor, b.amount) for k,b in bid_dict.iteritems()]
        averages = self.calc_averages(expanded_items, new_bids)

        edges = []
        for i in range(len(expanded_items)):
            for j in range(len(expanded_actors)):
                if (expanded_items[i], expanded_actors[j]) in bid_dict:
                    bid = bid_dict[(expanded_items[i], expanded_actors[j])]
                    edges.append((i, len(expanded_items) + j, self.score(bid, averages)))

        # Actually do the auction, maximizing whatever score function we have
        mw = mwmatching.maxWeightMatching(edges, maxcardinality=True)
        result = {}
        for i in range(len(expanded_items)):
            if mw[i] != -1:
                winner = expanded_actors[mw[i] - len(expanded_items)]
                result[expanded_items[i]] = \
                    (winner, bid_dict[(expanded_items[i], winner)].amount)
            else:
                result[expanded_items[i]] = None

        final_result = {}
        for item, winner in result.iteritems():
            root_item = item[:item.rfind('-')]
            root_winner = (winner[0][:winner[0].rfind('-')], winner[1])
            real_item = item[item.find('-')+1:] == '0'
            if real_item:
                final_result[root_item] = root_winner

        return final_result

    def score(self, bid, averages):
        return bid.amount



