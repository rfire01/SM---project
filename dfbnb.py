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
            weight, route = dfbnb_debug(depth - 1, b_factor, best_weight,
                                  route_weight + branch_weight)

            if weight < best_weight:
                best_branch = branch
                best_route = route
                best_weight = weight

    if best_branch == -1:
        return inf, best_route + [best_branch]

    return best_weight, [best_branch + 1] + best_route


def dfbnb_live(depth, b_factor, best_weight, route_weight):
    if depth == 0:
        return route_weight, []

    best_branch = -1
    best_route = []
    for branch in range(b_factor):
        branch_weight = (random.rand() > 0.5) * 1
        if branch_weight + route_weight < best_weight:
            weight, route = dfbnb_live(depth - 1, b_factor, best_weight,
                                       route_weight + branch_weight)

            if weight < best_weight:
                best_branch = branch
                best_route = route
                best_weight = weight

    if best_branch == -1:
        return inf, best_route + [best_branch]

    return best_weight, [best_branch + 1] + best_route


class btree_node(object):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def __repr__(self):
        output = str(self.value) + ":["
        for child in self.children:
            output += str(child) + ","

        output += "]"
        return output


def create_btree(depth, b_factor):
    if depth == 0:
        return btree_node((random.random() > 0.5) * 1, [])

    children = [create_btree(depth - 1, b_factor) for _ in xrange(b_factor)]
    return btree_node((random.rand() > 0.5) * 1, children)


def dfbnb_prebuild(tree, best_weight, route_weight):
    if not tree.children:
        return route_weight, []

    best_child = -1
    best_route = []
    for index, child in enumerate(tree.children):
        branch_weight = child.value
        if branch_weight + route_weight < best_weight:
            weight, route = dfbnb_prebuild(child, best_weight,
                                           route_weight + branch_weight)

            if weight < best_weight:
                best_child = index
                best_route = route
                best_weight = weight

    if best_child == -1:
        return inf, best_route + [best_child]

    return best_weight, [best_child + 1] + best_route

# import pickle
# with open('tree30.pkl', 'wb') as output:
#     tree = create_btree(30, 2)
#     pickle.dump(tree, output, pickle.HIGHEST_PROTOCOL)

import time

for depth in range(5,8):
    print "**************** depth = {} ****************".format(depth)
    print "------------prebuild tree-------------"
    for i in xrange(2,6):
        print "b-factor = {}".format(i)
        total_time = 0
        for _ in xrange(5*(i**depth)):
            tree = create_btree(depth, i)
            t1 = time.time()
            for _ in xrange(10):
                dfbnb_prebuild(tree, inf, 0)

            t2 = time.time()
            total_time += (t2 - t1) / 10.0

        print total_time / (5*(i**depth))

    print "------------live tree-------------"
    for i in xrange(2,6):
        print "b-factor = {}".format(i+2)

        t1 = time.time()
        for _ in xrange((5*(i**depth))):
            # dfbnb_prebuild(tree, inf, 0)
            dfbnb_live(depth, i + 2, inf, 0)

        t2 = time.time()
        print (t2 - t1) / (5*(i**depth))