""" Basic splitter interface """
from pprint import pprint

import mwmatching
from util import lcm


class Cost(object):
    def __init__(self, item, actor, amount):
        self.item = item
        self.actor = actor
        self.amount = amount

    def __eq__(self, other):
        return self.item == other.item and   \
               self.actor == other.actor and \
               self.amount == other.amount

    def __repr__(self):
        return "Cost(" + str(self.item) + ", " + str(self.actor) + \
               ", " + str(self.amount) + ")"


class Splitter(object):
    def calc_averages(self, items, costs):
        averages = {}
        for item in items:
            costs_for_item = [cost.amount for cost in costs if cost.item == item]
            if len(costs_for_item) > 0:
                averages[item] = float(sum(costs_for_item)) / len(costs_for_item)
            else:
                averages[item] = 0
        return averages

    def split(self, items, actors, costs, exclusive=True):
        print "Attempting to split:"
        print "== Items: "
        pprint(items)
        print "== between:"
        pprint(actors)
        print "== as per the costs:"
        pprint(costs)
        print "== Expanding the actors and items =="

        def expand_list(lst, new_length):
            # This ensures that if we have more items than actors or more actors
            # than items, we ensure that we always return the optimal result
            expanded_lst = lst * (new_length / len(lst))
            return [
                item + "-" + str(index / len(lst))
                for index, item
                in enumerate(expanded_lst)
            ]

        lcm_actors_items = lcm(len(actors), len(items))
        expanded_actors = expand_list(actors, lcm_actors_items)
        expanded_items = expand_list(items, lcm_actors_items)

        cost_dict = {}
        for cost in costs:
            cost_dict[(cost.item, cost.actor)] = cost

        exp_cost = {}
        for actor in expanded_actors:
            for item in expanded_items:
                root_actor = actor[:actor.rfind('-')]
                root_item = item[:item.rfind('-')]
                real_item = item[item.find('-') + 1:] == '0'
                if real_item:
                    original_cost = cost_dict[(root_item, root_actor)]
                    exp_cost[(item, actor)] = Cost(item, actor, original_cost.amount)
                else:
                    exp_cost[(item, actor)] = Cost(item, actor, 0)

        cost_dict = exp_cost
        new_costs = [Cost(b.item, b.actor, b.amount) for k, b in cost_dict.iteritems()]
        averages = self.calc_averages(expanded_items, new_costs)

        edges = []
        for i in range(len(expanded_items)):
            for j in range(len(expanded_actors)):
                if (expanded_items[i], expanded_actors[j]) in cost_dict:
                    cost = cost_dict[(expanded_items[i], expanded_actors[j])]
                    edges.append((i, len(expanded_items) + j, self.score(cost, averages)))

        # Actually do the auction, maximizing whatever score function we have
        mw = mwmatching.maxWeightMatching(edges, maxcardinality=True)
        result = {}
        for i in range(len(expanded_items)):
            if mw[i] != -1:
                winner = expanded_actors[mw[i] - len(expanded_items)]
                result[expanded_items[i]] = \
                    (winner, cost_dict[(expanded_items[i], winner)].amount)
            else:
                result[expanded_items[i]] = None

        final_result = {}
        for item, winner in result.iteritems():
            root_item = item[:item.rfind('-')]
            root_winner = (winner[0][:winner[0].rfind('-')], winner[1])
            real_item = item[item.find('-') + 1:] == '0'
            if real_item:
                final_result[root_item] = root_winner

        return final_result

    def normalize(self, item_assignments, total):
        total_costs = float(sum(v[1] for k, v in item_assignments.iteritems()))
        total = float(total)
        return dict([
            (item, (winner[0], int(round(winner[1] / total_costs * total))))
            for item, winner
            in item_assignments.iteritems()
        ])

    def score(self, cost, averages):
        return cost.amount
