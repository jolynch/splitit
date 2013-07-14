item-splitter
=============
A framework and algorithm to fairly split costs amoung roommates when there is
no obvious criteria to split the costs based on.

This was made to help a few roommates and I split rent in San Francisco between
rooms that were very inequitable, but we couldn't quite figure out what people
should pay for the rent, however this can also be used to split arbitrary
items.


Installation
------------
Clone the package ... run the auction ... better instructions coming soon.

Running
-------
After installing, to run the auction simply type:

```
python auction.py
```

This will run an auction via the command line, asking you relevant questions
along the way.

Auctions
--------
item-splitter supports simultaneous auctions based on bids on multiple items.
Once an auction has begun, you will get asked a series of questions that are
needed to setup the auction, and then the program will split the items
according to a [maximum weight matching](http://jorisvr.nl/maximummatching.html)
of the auction graph.  The auction graph is constructed as follows:

```
edges = []
for bid_on_item in all_bids:
  item, actor, bid = bid_on_item
  edges.append(item, actor, score(bid, ...))
```

In other words, the auction graph is a complete bipartite graph between the
items and the actors in the auction, with the edge weights determined by the
splitter function that you are using.  The program maximizes total surplus and
then normalizes the bids to determine the final price of each room.

Splitters
---------

Currently there is only the surplus maximizing splitter, which scores bids
based on the implied consumer surplus of their bids.  What this means is that
the "score" of your bid is as follows:

```
score(bid, item_i) = bid - average_bid(item_i)
```

This splitter has the following properties:
1. You will never pay more than the bid that you make.
2. Bidders who express strong preferences pay more of the real rent.
3. You generally only win a room if you outbid the average (consensus) bid.

These properties are probably all you ever need to split things like rent, but
we can always add more splitters.
