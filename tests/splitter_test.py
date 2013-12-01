import unittest

from splitit.splitter import Cost
from splitit.surplus_maximizer import SurplusMaximizer
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
        bids = [Cost(ITEM1, ACTOR1, 1640),
                Cost(ITEM2, ACTOR1, 1540),
                Cost(ITEM3, ACTOR1, 1140),
                Cost(ITEM4, ACTOR1, 1640),
                Cost(ITEM5, ACTOR1, 1740),
                Cost(ITEM1, ACTOR2, 1540),
                Cost(ITEM2, ACTOR2, 1240),
                Cost(ITEM3, ACTOR2, 1340),
                Cost(ITEM4, ACTOR2, 1640),
                Cost(ITEM5, ACTOR2, 1940),
                Cost(ITEM1, ACTOR3, 1740),
                Cost(ITEM2, ACTOR3, 1540),
                Cost(ITEM3, ACTOR3, 1040),
                Cost(ITEM4, ACTOR3, 1640),
                Cost(ITEM5, ACTOR3, 1740),
                Cost(ITEM1, ACTOR4, 1440),
                Cost(ITEM2, ACTOR4, 1640),
                Cost(ITEM3, ACTOR4, 1240),
                Cost(ITEM4, ACTOR4, 1640),
                Cost(ITEM5, ACTOR4, 1740),
                Cost(ITEM1, ACTOR5, 1640),
                Cost(ITEM2, ACTOR5, 1640),
                Cost(ITEM3, ACTOR5, 1140),
                Cost(ITEM4, ACTOR5, 1640),
                Cost(ITEM5, ACTOR5, 1640)]
        result = self.splitter.split(ITEMS[:5], ACTORS[:5], bids)
        expected = [(ITEM1, ACTOR3, None),
                    (ITEM2, ACTOR5, None),
                    (ITEM3, ACTOR4, None),
                    (ITEM4, ACTOR1, None),
                    (ITEM5, ACTOR2, None)]
        item_assignments_present(self, result, expected)

    def test_obvious_auction(self):
        """ Test when people bid such that there is a "right" answer """
        bids = [Cost(ITEM1, ACTOR1, 1000),
                Cost(ITEM2, ACTOR1, 1000),
                Cost(ITEM3, ACTOR1, 1000),
                Cost(ITEM4, ACTOR1, 5000),

                Cost(ITEM1, ACTOR2, 1000),
                Cost(ITEM2, ACTOR2, 1000),
                Cost(ITEM3, ACTOR2, 5000),
                Cost(ITEM4, ACTOR2, 1000),

                Cost(ITEM1, ACTOR3, 1000),
                Cost(ITEM2, ACTOR3, 5000),
                Cost(ITEM3, ACTOR3, 1000),
                Cost(ITEM4, ACTOR3, 1000),

                Cost(ITEM1, ACTOR4, 5000),
                Cost(ITEM2, ACTOR4, 1000),
                Cost(ITEM3, ACTOR4, 1000),
                Cost(ITEM4, ACTOR4, 1000)]

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
                # I have no preferences
        bids = [Cost(ITEM1, ACTOR1, 1000),
                Cost(ITEM2, ACTOR1, 1000),
                Cost(ITEM3, ACTOR1, 1000),
                Cost(ITEM4, ACTOR1, 1000),
                Cost(ITEM5, ACTOR1, 1000),

                # I have linear preferences
                Cost(ITEM1, ACTOR2, 700),
                Cost(ITEM2, ACTOR2, 800),
                Cost(ITEM3, ACTOR2, 1000),
                Cost(ITEM4, ACTOR2, 1200),
                Cost(ITEM5, ACTOR2, 1300),

                # I have non-linear preferences
                Cost(ITEM1, ACTOR3, 400),
                Cost(ITEM2, ACTOR3, 800),
                Cost(ITEM3, ACTOR3, 1000),
                Cost(ITEM4, ACTOR3, 1200),
                Cost(ITEM5, ACTOR3, 1600),

                # I have arbitrary preference
                Cost(ITEM1, ACTOR4, 2435),
                Cost(ITEM2, ACTOR4, 305),
                Cost(ITEM3, ACTOR4, 310),
                Cost(ITEM4, ACTOR4, 1725),
                Cost(ITEM5, ACTOR4, 225),

                # I have strong preferences
                Cost(ITEM1, ACTOR5, 0),
                Cost(ITEM2, ACTOR5, 0),
                Cost(ITEM3, ACTOR5, 0),
                Cost(ITEM4, ACTOR5, 0),
                Cost(ITEM5, ACTOR5, 5000)]
        result = self.splitter.split(ITEMS[:5], ACTORS[:5], bids)
        expected = [(ITEM1, ACTOR4, None),
                    (ITEM2, ACTOR1, None),
                    (ITEM3, ACTOR3, None),
                    (ITEM4, ACTOR2, None),
                    (ITEM5, ACTOR5, None)]
        item_assignments_present(self, result, expected)

    def test_odd_items(self):
        """ Test an auction where we have more items than people

        """
                # I have some preferences
        bids = [Cost(ITEM1, ACTOR1, 1000),
                Cost(ITEM2, ACTOR1, 1000),
                Cost(ITEM3, ACTOR1, 1000),
                Cost(ITEM4, ACTOR1, 0),
                Cost(ITEM5, ACTOR1, 2000),

                # I have other preferences
                Cost(ITEM1, ACTOR2, 0),
                Cost(ITEM2, ACTOR2, 1500),
                Cost(ITEM3, ACTOR2, 1500),
                Cost(ITEM4, ACTOR2, 500),
                Cost(ITEM5, ACTOR2, 1500)]

        result = self.splitter.split(ITEMS[:5], ACTORS[:2], bids)
        expected = [(ITEM1, ACTOR1, None),
                    (ITEM2, ACTOR2, None),
                    (ITEM3, ACTOR2, None),
                    (ITEM4, ACTOR2, None),
                    (ITEM5, ACTOR1, None)]
        item_assignments_present(self, result, expected)

    def test_normalize_equal(self):
        test_dict = {
            ITEM1: (ACTOR1, 1000),
            ITEM2: (ACTOR2, 500),
            ITEM3: (ACTOR3, 0),
            ITEM4: (ACTOR4, 2000)
        }
        total = 3500

        expected = [(ITEM1, ACTOR1, 1000),
                    (ITEM2, ACTOR2, 500),
                    (ITEM3, ACTOR3, 0),
                    (ITEM4, ACTOR4, 2000)]

        result = self.splitter.normalize(test_dict, total)
        item_assignments_present(self, result, expected)

    def test_normalize_high(self):
        test_dict = {
            ITEM1: (ACTOR1, 1000),
            ITEM2: (ACTOR2, 500),
            ITEM3: (ACTOR3, 0),
            ITEM4: (ACTOR4, 2000)
        }
        total = 1000

        expected = [(ITEM1, ACTOR1, 286),
                    (ITEM2, ACTOR2, 143),
                    (ITEM3, ACTOR3, 0),
                    (ITEM4, ACTOR4, 571)]

        result = self.splitter.normalize(test_dict, total)
        item_assignments_present(self, result, expected)

    def test_normalize_low(self):
        test_dict = {
            ITEM1: (ACTOR1, 1000),
            ITEM2: (ACTOR2, 500),
            ITEM3: (ACTOR3, 0),
            ITEM4: (ACTOR4, 2000)
        }
        total = 5000

        expected = [(ITEM1, ACTOR1, 1429),
                    (ITEM2, ACTOR2, 714),
                    (ITEM3, ACTOR3, 0),
                    (ITEM4, ACTOR4, 2857)]

        result = self.splitter.normalize(test_dict, total)
        item_assignments_present(self, result, expected)

if __name__ == '__main__':
    unittest.main()
