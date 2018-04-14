from numpy import inf, random

def dfbnb_debug(depth, b_factor, best_weight, route_weight):
    if depth == 0:
        return route_weight, []
    print "**************** depth {} *********************".format(depth)

    best_branch = -1
    best_route = []
    for branch in range(b_factor):
        branch_weight = random.randint(2)
        print "branch {} in d={} have weight {}".format(branch + 1, depth, branch_weight)
        if branch_weight + route_weight < best_weight:
            weight, route = dfbnb(depth - 1, b_factor, best_weight,
                                  route_weight + branch_weight)

            if weight < best_weight:
                best_branch = branch
                best_route = route
                best_weight = weight

    if best_branch == -1:
        return inf, best_route + [best_branch]

    return best_weight, [best_branch + 1] + best_route


def dfbnb(depth, b_factor, best_weight, route_weight):
    if depth == 0:
        return route_weight, []

    best_branch = -1
    best_route = []
    for branch in range(b_factor):
        branch_weight = (random.rand() > 0.5) * 1
        if branch_weight + route_weight < best_weight:
            weight, route = dfbnb(depth - 1, b_factor, best_weight,
                                  route_weight + branch_weight)

            if weight < best_weight:
                best_branch = branch
                best_route = route
                best_weight = weight

    if best_branch == -1:
        return inf, best_route + [best_branch]

    return best_weight, [best_branch + 1] + best_route

import time
for i in range(12):
    print "b-factor = {}".format(i+2)
    t1 = time.time()
    dfbnb(400, i + 2, inf, 0)
    t2 = time.time()
    print t2 - t1