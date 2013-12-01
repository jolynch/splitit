""" Basic auction runner """
from pprint import pprint

from splitter import Cost
from surplus_maximizer import SurplusMaximizer


class Auction(object):
    def run(self):
        auctions = []
        print "Welcome to splitit!"
        while True:
            action = raw_input("> ")
            if action in ("h", "help"):
                self.print_help()
            elif action in ("q", "quit"):
                return
            elif action in ("s", "start"):
                result = self.start_auction()
                if result is not None:
                    auctions.append(result)
            elif action in ("v", "view"):
                num = raw_input("Which auction (0, {0})".format(len(auctions) - 1))
                if num < len(auctions):
                    pprint(auctions[num])
            elif action in ("vi", "view_all"):
                pprint(auctions)
            elif action in ("c", "clear"):
                auctions = []

    def print_help(self):
        print "Welcome to the Auction repl, you can do things like:\n\
        (h)elp - print a help dialog\n\
        (s)tart - start an auction\n\
        (v)iew - view an auction\n\
        (vi)ew_all - view all auctions\n\
        (c)lear - clear all auctions\n\
        (q)uit - leave the repl \n"

    def start_auction(self):
        num_people = int(raw_input("How many people? "))
        total_dollars = int(raw_input("How much can each person bid? "))
        actors = []
        while len(actors) != num_people:
            actors = raw_input("Names of actors, separated by commas: ")
            if actors in ("q", "quit"):
                return
            actors = [p.strip() for p in actors.split(",")]

        num_items = int(raw_input("How many items? "))
        items = []
        while len(items) != num_items:
            items = raw_input("Names of items, separated by commas: ")
            if items in ("q", "quit"):
                return
            items = [i.strip() for i in items.split(",")]

        print actors
        print items
        bids = []
        for actor in actors:
            a_bids = []
            while len(a_bids) != num_items:
                a_bids = raw_input("Please enter %s's bids for %s, separated by commas: " % (actor, items))
                if a_bids in ("q", "quit"):
                    return
                a_bids = [int(a.strip()) for a in a_bids.split(",")]
                if sum(a_bids) == total_dollars:
                    for i in range(len(a_bids)):
                        bids.append(Cost(items[i], actor, a_bids[i]))
                else:
                    print "That is the wrong total, %d != %d" % (sum(a_bids), total_dollars)
                    a_bids = []
        splitter = SurplusMaximizer()
        result = splitter.split(items, actors, bids)
        final_result = {}
        print result
        total = sum([v[1] for k, v in result.items()])
        for k, v in result.items():
            final_result[k] = (v[0], v[1] / float(total) * total_dollars)

        print "Result of auction:"
        pprint(final_result)

        return (bids, result, final_result)


if __name__ == '__main__':
    auction = Auction()
    auction.run()
