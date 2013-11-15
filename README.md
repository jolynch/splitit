splitit
=============
An algorithm and UI to fairly split costs amoung agents when there is no obvious
criteria to split the costs based on.

This was made to help a few roommates and I split rent in San Francisco between
rooms that were very inequitable, but we couldn't quite figure out what people
should pay for the rent, however this can also be used to split arbitrary
items.

Some potential use cases of the UI:
* Splitting rent among roommates
* Dividing shared posessions (e.g. when roommates move out)

The algorithm itself is just a framework around the basic maximum weight perfect
matching problem, which basically solves the assignment problem. Internally I
use the mwmatching.py library, so we are doing the actual edmunds algorithm in
python, which could be considerably slower than using a C implementation.


Installation
------------
You can download the code and install it via setup.py
```
sudo python setup.py install
```

Alternatively you can download the code, don't install it at all and run the various make targets.


Running Without Installation
----------------------------
There are two user interfaces, one on the command line and the other as a web
application. The web application is pretty much the supported method of using
this tool.

To run an auction on the webapp where everyone can go to the auction separately
and submit their bids anonomously do:
```
make web

```

You can also run an auction via a command line interface. If you need help type
'h' or 'help'.

```
make cmd
```

This will run an auction via the command line, asking you relevant questions
along the way.

Running After Installation
--------------------------
If you choose to actually install the package, you can run the command line
auction as any user, and you can run the web app as the super user.

To run the command line auction, from any command line launch:
```
splitit-repl
```

To run the webapp:
```
sudo splitit-web
```

Auctions
--------
splitit supports simultaneous auctions based on bids on multiple items.
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
2. Bidders who express strong preferences pay more of the real cost.
3. You generally only win an item if you outbid the average (consensus) bid.

These properties are probably all you ever need to split things like rent, but
we can always add more splitters.
