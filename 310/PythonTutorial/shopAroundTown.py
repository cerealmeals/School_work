# shopAroundTown.py
# -----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
Here's the intended output of this script, once you fill it in:

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
Welcome to shop3 fruit shop
Orders: [('apples', 1.0), ('oranges', 3.0), ('limes', 2.0)]
At gas price 1 the best route is: ['shop1', 'shop2', 'shop3']
At gas price 3 the best route is: ['shop1', 'shop3']
At gas price 5 the best route is: ['shop2']
At gas price -1 the best route is: ['shop2', 'shop1', 'shop3']
"""

#from __future__ import print_function
import shop
import town


def shopAroundTown(orderList, fruitTown, gasCost):
    """
    orderList: List of (fruit, numPound) tuples
    fruitTown: A Town object
    gasCost: A number representing the cost of going one mile
    Returns a list of shops in the order that is the optimal route to take when
    buying the fruit in the orderList
    """
    "*** YOUR CODE HERE ***"
    # print("start")
    route = getAllSubsets(fruitTown.getShops())
    all_routes = []
    for x in route:
        perm_x = getAllPermutations(x)
        all_routes += perm_x

    lowest = float("inf")
    ret = []
    for route in all_routes:
        if fruitTown.allFruitsCarriedAtShops(orderList, route):
            current = fruitTown.getPriceOfOrderOnRoute(orderList, route, gasCost)
            if (lowest > current):
                lowest = current
                ret = route
    return ret


def getAllSubsets(lst):
    """
        lst: A list
    Returns the powerset of lst, i.e. a list of all the possible subsets of lst
    """
    if not lst:
        return [[]]
    firstElement = lst[0]
    restSubsets = getAllSubsets(lst[1:])

    withFirst = [[firstElement] + subset for subset in restSubsets]
    withoutFirst = restSubsets
    withFirst.extend(withoutFirst)
    return withFirst


def getAllPermutations(lst):
    """
        lst: A list
    Returns a list of all permutations of lst
    """
    if not lst:
        return [[]]
    elif len(lst) == 1:
        return [lst]
    allPermutations = []
    for i in range(len(lst)):
        item = lst[i]
        withoutItem = lst[:i] + lst[i+1:]
        allPermutations += prependToAll(item, getAllPermutations(withoutItem))
    return allPermutations


def prependToAll(item, lsts):
    """
        item: Any object
        lsts: A list of lists
    Returns a copy of lsts with item prepended to each list contained in lsts
    """
    ret = [[item] + lst for lst in lsts]
    return ret


if __name__ == '__main__':
    "This code runs when you invoke the script from the command line"
    orders = [('apples', 1.0), ('oranges', 3.0), ('limes', 2.0)]
    dir1 = {'apples': 2.0, 'oranges': 1.0}
    dir2 = {'apples': 1.0, 'oranges': 5.0, 'limes': 3.0}
    dir3 = {'apples': 2.0, 'limes': 2.0}
    shop1 = shop.FruitShop('shop1', dir1)
    shop2 = shop.FruitShop('shop2', dir2)
    shop3 = shop.FruitShop('shop3', dir3)
    shops = [shop1, shop2, shop3]
    distances = {('home', 'shop1'): 2,
                 ('home', 'shop2'): 1,
                 ('home', 'shop3'): 1,
                 ('shop1', 'shop2'): 2.5,
                 ('shop1', 'shop3'): 2.5,
                 ('shop2', 'shop3'): 1
                 }
    fruitTown = town.Town(shops, distances)
    print("Orders:", orders)
    for price in (1, 3, 5, -1):
        print("At gas price", price, "the best route is:", \
              shopAroundTown(orders, fruitTown, price))
