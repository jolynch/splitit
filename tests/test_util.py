def item_assignment_present(test_case, result, item, actor=None, amount=None):
    """ Test that an expected item assignment is present

    Arguments:
    result [dict] -- the auction results in {'item': (winner, bid) ... } format
    item [string] -- the item we want to check was won
    actor (string) -- the actor who should win the item
    amount (int) -- The winning bid on the item
    """
    test_case.assertIn(item, result)
    test_case.assertIsNotNone(result[item])
    winner, winning_bid = result[item]
    if actor is not None:
        test_case.assertEqual(winner, actor)
    if amount is not None:
        test_case.assertEqual(winning_bid, amount)

def item_assignments_present(test_case, result, assignments):
    """ Test that an expected list of assignments are present

    Arguments:
    result [dict] -- the auction results in {'item': (winner, bid) ... } format
    assignments [list] -- the assignments we want in [(item, actor, bid) ...]
                          format.
    """
    for assignment in assignments:
        item_assignment_present(test_case,
                                result,
                                assignment[0],
                                assignment[1],
                                assignment[2])
    print "All passed: ", assignments


