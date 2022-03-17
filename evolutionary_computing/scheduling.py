"""
Created on Sun Nov  1 20:28:22 2020

@author: rachlin
@file: sorting_v3.py
@description: Sort numbers using evolutionary computing

Rewritten to use version4 of the evo framework (evo_v4.py)
"""

import evo
import random as rnd
import json
import copy

def setups(L):
    """ Objective: Count the number of setups within a schedule
        (Changing from one product to another)
    """
    keys = list(L.keys())
    helper = dict(L)
    helper.pop(keys[0], None)
    return sum([L[i]['product'] != L[j]['product'] for i, j in zip(L, helper)])

def low_priority(L):
    keys = list(L.keys())
    reversed = copy.deepcopy(keys)
    reversed.reverse()
    # Find the last instance of a HIGH priority
    for key in reversed:
        if L[key]['priority'] == 'HIGH':
            index = len(keys) - reversed.index(key)
            break
    return sum(L[keys[i]]['quantity'] for i in range(index) if L[keys[i]]['priority'] == 'LOW')

def delays(L):
    keys = list(L.keys())
    length = len(keys) - 1
    return sum(L[keys[i]]['quantity'] for i in range(length) if int(keys[i]) > int(keys[i + 1]))

def simple_swap_products(solutions):
    """ Agent: try to make the beginning of the schedule the same products"""
    schedule = solutions[0]
    items = list(schedule.items())
    # Find the product of the first order
    i_product = items[0][1]["product"]
    # Loop through from the back, bringing an order with the same product to the front
    for item in reversed(items):
        if item[1]['product'] == i_product:
            items.insert(1, items.pop(items.index(item)))
            break
    return dict(items)
    # Wanted to use functional programming but wanted to keep this one as a swapper than ran once
    # items = [items.pop(items.index(item)) for item in reversed(items) if item[1]['product'] == i_product]


def manage_priority(solutions):
    """ Agent: Make sure high priority orders are moved to the front"""
    schedule = solutions[0]
    items = list(schedule.items())
    temp_items = [items.pop(items.index(item)) for item in items if item[1]['priority'] == 'HIGH']
    return dict(temp_items + items)

def orders_ordered(solutions):
    """Agent: A pretty basic solution that limits setups and delays
    Note: will always return the same solution
    Serves as a baseline to improve in other attributes"""
    schedule = solutions[0]
    items = list(schedule.values())
    values = sorted(items, key=lambda x: x['product'])
    keys = sorted(schedule, key=lambda x: schedule[x]['product'])
    zipper = zip(keys, values)
    return dict(zipper)

def delay_agent(solutions):
    schedule = solutions[0]
    items = list(schedule.items())
    range = rnd.randrange(0, 10)
    iter = 0
    while iter < range:
        i = rnd.randrange(1, len(schedule))
        j = rnd.randrange(1, len(schedule))

        if items[i][0] > items[j][0]:
            items[i], items[j] = items[j], items[i]
        iter += 1

    return dict(items)




def main():

    # Create environment
    E = evo.Evo()

    # Register fitness criteria
    E.add_fitness_criteria("setups", setups)
    E.add_fitness_criteria("low_priority", low_priority)
    E.add_fitness_criteria("delays", delays)
    # Register agents
    E.add_agent("simple_swap_products", simple_swap_products, 1)
    E.add_agent("manage_priority", manage_priority, 1)
    E.add_agent("orders_ordered", orders_ordered, 1)
    E.add_agent("delay_agent", delay_agent, 1)

    # Add initial solution
    with open('orders.json') as file:
        orders = json.load(file)
    E.add_solution(orders)
    #print(E)


    # Run the evolver
    E.evolve(100000, 500, 10000)
    #E.evolve(1000, 50, 100)
    print(E.show_evals())
    #E.evals_viz()

if __name__ == '__main__':
    main()
