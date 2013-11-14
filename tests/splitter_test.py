import unittest
from splitit.surplus_maximizer import SurplusMaximizer
from splitit.splitter import Bid

from test_util import item_assignment_present
from test_util import item_assignments_present

ACTOR1 = "Ben Bitdiddle (1)"
ACTOR2 = "Eva Lu Ator (2)"
ACTOR3 = "Louis Reasoner (3)"
ACTOR4 = "Alyssa P Hacker (4)"
ACTOR5 = "Cy D. Fect (5)"
ACTOR6 = "Lem E. Tweakit (6)"

ACTORS = [ACTOR1, ACTOR2, ACTOR3, ACTOR4, ACTOR5, ACTOR6]

ITEM1 = "Item_1"
ITEM2 = "Item_2"
ITEM3 = "Item_3"
ITEM4 = "Item_4"
ITEM5 = "Item_5"
ITEM6 = "Item_6"

ITEMS = [ITEM1, ITEM2, ITEM3, ITEM4, ITEM5, ITEM6]

class TestSurplusMaximizer(unittest.TestCase):
    """ Test the Surplus Maximizer splitter """

    def setUp(self):
        self.splitter = SurplusMaximizer()

    def test_single_identical_bid(self):
        """ Test when people bid the same thing on a single item

        This should theoretically not happen very frequently, but if it did we
        would expect the algo to cope with it
        """
        bids =  [Bid(ITEM1, ACTOR1, 1640),
                 Bid(ITEM2, ACTOR1, 1540),
                 Bid(ITEM3, ACTOR1, 1140),
                 Bid(ITEM4, ACTOR1, 1640),
                 Bid(ITEM5, ACTOR1, 1740),
                 Bid(ITEM1, ACTOR2, 1540),
                 Bid(ITEM2, ACTOR2, 1240),
                 Bid(ITEM3, ACTOR2, 1340),
                 Bid(ITEM4, ACTOR2, 1640),
                 Bid(ITEM5, ACTOR2, 1940),
                 Bid(ITEM1, ACTOR3, 1740),
                 Bid(ITEM2, ACTOR3, 1540),
                 Bid(ITEM3, ACTOR3, 1040),
                 Bid(ITEM4, ACTOR3, 1640),
                 Bid(ITEM5, ACTOR3, 1740),
                 Bid(ITEM1, ACTOR4, 1440),
                 Bid(ITEM2, ACTOR4, 1640),
                 Bid(ITEM3, ACTOR4, 1240),
                 Bid(ITEM4, ACTOR4, 1640),
                 Bid(ITEM5, ACTOR4, 1740),
                 Bid(ITEM1, ACTOR5, 1640),
                 Bid(ITEM2, ACTOR5, 1640),
                 Bid(ITEM3, ACTOR5, 1140),
                 Bid(ITEM4, ACTOR5, 1640),
                 Bid(ITEM5, ACTOR5, 1640)]
        result = self.splitter.split(ITEMS[:5], ACTORS[:5], bids)
        expected = [(ITEM1, ACTOR3, None),
                    (ITEM2, ACTOR5, None),
                    (ITEM3, ACTOR4, None),
                    (ITEM4, ACTOR1, None),
                    (ITEM5, ACTOR2, None)]
        item_assignments_present(self, result, expected)

    def test_obvious_auction(self):
        """ Test when people bid such that there is a "right" answer """
        bids =  [Bid(ITEM1, ACTOR1, 1000),
                 Bid(ITEM2, ACTOR1, 1000),
                 Bid(ITEM3, ACTOR1, 1000),
                 Bid(ITEM4, ACTOR1, 5000),

                 Bid(ITEM1, ACTOR2, 1000),
                 Bid(ITEM2, ACTOR2, 1000),
                 Bid(ITEM3, ACTOR2, 5000),
                 Bid(ITEM4, ACTOR2, 1000),

                 Bid(ITEM1, ACTOR3, 1000),
                 Bid(ITEM2, ACTOR3, 5000),
                 Bid(ITEM3, ACTOR3, 1000),
                 Bid(ITEM4, ACTOR3, 1000),

                 Bid(ITEM1, ACTOR4, 5000),
                 Bid(ITEM2, ACTOR4, 1000),
                 Bid(ITEM3, ACTOR4, 1000),
                 Bid(ITEM4, ACTOR4, 1000)]

        result = self.splitter.split(ITEMS[:4], ACTORS[:4], bids)
        expected = [(ITEM1, ACTOR4, None),
                    (ITEM2, ACTOR3, None),
                    (ITEM3, ACTOR2, None),
                    (ITEM4, ACTOR1, None)]
        item_assignments_present(self, result, expected)

    def test_reasonable_auction(self):
        """ Test a "real world" auction

        Each person has 5000 to use as they wish, on 5 items
        """
        bids =  [# I have no preferences
                 Bid(ITEM1, ACTOR1, 1000),
                 Bid(ITEM2, ACTOR1, 1000),
                 Bid(ITEM3, ACTOR1, 1000),
                 Bid(ITEM4, ACTOR1, 1000),
                 Bid(ITEM5, ACTOR1, 1000),

                 # I have linear preferences
                 Bid(ITEM1, ACTOR2, 700),
                 Bid(ITEM2, ACTOR2, 800),
                 Bid(ITEM3, ACTOR2, 1000),
                 Bid(ITEM4, ACTOR2, 1200),
                 Bid(ITEM5, ACTOR2, 1300),

                 # I have non-linear preferences
                 Bid(ITEM1, ACTOR3, 400),
                 Bid(ITEM2, ACTOR3, 800),
                 Bid(ITEM3, ACTOR3, 1000),
                 Bid(ITEM4, ACTOR3, 1200),
                 Bid(ITEM5, ACTOR3, 1600),

                 # I have arbitrary preference
                 Bid(ITEM1, ACTOR4, 2435),
                 Bid(ITEM2, ACTOR4, 305),
                 Bid(ITEM3, ACTOR4, 310),
                 Bid(ITEM4, ACTOR4, 1725),
                 Bid(ITEM5, ACTOR4, 225),

                 # I have strong preferences
                 Bid(ITEM1, ACTOR5, 0),
                 Bid(ITEM2, ACTOR5, 0),
                 Bid(ITEM3, ACTOR5, 0),
                 Bid(ITEM4, ACTOR5, 0),
                 Bid(ITEM5, ACTOR5, 5000)]
        result = self.splitter.split(ITEMS[:5], ACTORS[:5], bids)
        expected = [(ITEM1, ACTOR4, None),
                    (ITEM2, ACTOR1, None),
                    (ITEM3, ACTOR3, None),
                    (ITEM4, ACTOR2, None),
                    (ITEM5, ACTOR5, None)]
        item_assignments_present(self, result, expected)

    def test_edge_cover(self):
        """ Test an auction where we have more items than people

        """
        bids = [# I have no preferences
                Bid(ITEM1, ACTOR1, 1000),
                Bid(ITEM2, ACTOR1, 1000),
                Bid(ITEM3, ACTOR1, 1000),
                Bid(ITEM4, ACTOR1, 1000),

                # I have some preferences
                Bid(ITEM1, ACTOR2, 500),
                Bid(ITEM2, ACTOR2, 1500),
                Bid(ITEM3, ACTOR2, 1500),
                Bid(ITEM4, ACTOR2, 500)]

        result = self.splitter.split(ITEMS[:4], ACTORS[:2], bids)
        expected = [(ITEM1, ACTOR1, None),
                    (ITEM2, ACTOR2, None),
                    (ITEM3, ACTOR2, None),
                    (ITEM4, ACTOR1, None)]
        print result
        item_assignments_present(self, result, expected)


if __name__ == '__main__':
    unittest.main()
