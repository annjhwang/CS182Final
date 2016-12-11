# 0/1 knapsack.py
# includes: brute force, greedy
# needs: dynamic programming
# needs: proof that greedy (on value) >= 0.5 * optimal

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from itertools import combinations
import operator
import time
import copy
from sklearn.cross_validation import train_test_split

# allows user to input maximum caloric intake
nutrient_type = raw_input('Enter the type of nutrient you want to limit: ')
print 'nutrient:', nutrient_type
nutrient_capacity = input('Enter the maximum maximum of this nutrient (in kcal or g): ')
print 'Capacity for ' + str(nutrient_type) + ' intake: ' + str(nutrient_capacity)

allRestaraunts = pd.DataFrame.from_csv('data/all.csv')

def powerset(items):
    res = [[]]
    for item in items:
        newset = [r+[item] for r in res]
        res.extend(newset)
    return res

def totalvalue(comb, nutrient_capacity):
    tot_calories = totval = 0

    for item, calories, val in comb:
        tot_calories  += calories
        totval += val
    return (totval, -tot_calories) if tot_calories <= nutrient_capacity else (0, 0)

def knapsack_dp(foods, limit):
    table = [[0 for w in range(limit + 1)] for j in xrange(len(foods) + 1)]
    for j in xrange(1, len(foods) + 1):
        food, calories, val = foods[j-1]
        for w in xrange(1, limit + 1):
            if calories > w:
                table[j][w] = table[j-1][w]
            else:
                table[j][w] = max(table[j-1][w],
                                  table[j-1][w-calories] + val)
    best_foods = []
    w = limit
    for j in range(len(foods), 0, -1):
        was_added = table[j][w] != table[j-1][w]
 
        if was_added:
            food, calories, val = foods[j-1]
            best_foods.append(foods[j-1])
            w -= calories
    return best_foods

def knapsack_brute_force(items, max_weight):
    knapsack = []
    best_weight = 0
    best_value = 0
    for item_set in powerset(items):
        set_weight = sum(map(weight, item_set))
        set_value = sum(map(value, item_set))
        if set_value > best_value and set_weight <= max_weight:
            best_weight = set_weight
            best_value = set_value
            knapsack = item_set
    return knapsack, best_weight, best_value

def value(items):
    values = items
    values.sort(key=operator.itemgetter(2), reverse=True)
    #print values
    #print items
    return values

def val_weight_ratio(items):
    ratio = []
    for item in items:
        #print item
        weight = item[1]
        value = item[2]
        name = item[0]
        if weight != 0:
            ratio.append([name, weight, value, 1.*value/weight])
        else:
            ratio.append([name, weight, value, 1.*value])
    ratio.sort(key=operator.itemgetter(3), reverse=True)
    return ratio

# items: [(id, weight, value)]
def knapsack_greedy(foods, limit, function, column_index):
    knapsack = []
    sorted_foods = function(foods)
    #print 'sorted: ', sorted_foods
    #print sorted_foods
    total_weight = 0
    total_value = 0
    counter = 0
    while (total_weight + sorted_foods[counter][1]) < limit and (counter < (len(sorted_foods)-1)):
        knapsack.append(sorted_foods[counter][:column_index])
        total_weight += sorted_foods[counter][1]
        total_value += sorted_foods[counter][2]
        counter += 1
    return knapsack, total_weight, total_value
#items = [(0,2,4), (1,5,3), (2,7,4), (3,3,5)]
res = []
#sims = 1000
names = allRestaraunts['Item_Name'].values
nutrient = [int(x) for x in allRestaraunts[nutrient_type].values]
protein = [int(x) for x in allRestaraunts['Protein'].values]
item = zip(names, nutrient, protein)
max_weight = nutrient_capacity

# gradually increase trainings set
train, test = train_test_split(item, train_size = 0.99)

item = train
'''
knapsack = knapsack_dp(item, max_weight)
opt_val, opt_wt = totalvalue(knapsack, max_weight)
print 'optimal:', opt_val

knapsack = knapsack_greedy(item, max_weight, value, 3)
val, wt = totalvalue(knapsack, nutrient_capacity)
print 'greedy', val'''

for i in xrange(len(item)):
    #train = i * 0.01

    items = item[:i+2]
    #knapsack, opt_wt, opt_val = knapsack_brute_force(items, max_weight)
    knapsack = knapsack_dp(items, max_weight)
    opt_val, opt_wt = totalvalue(knapsack, max_weight)
    r = []

    if opt_val != 0:
        knapsack, wt, val = knapsack_greedy(items, max_weight, value, 3)
        #val, wt = totalvalue(knapsack, max_weight)
        r.append(float(val)/opt_val)
        #print 'density'

        knapsack, wt, val = knapsack_greedy(items, max_weight, val_weight_ratio, 3)
        #val, wt = totalvalue(knapsack, max_weight)
        r.append(float(val)/opt_val)
        # DP
        knapsack = knapsack_dp(items, max_weight)
        val, wt = totalvalue(knapsack, max_weight)
        r.append(float(val)/opt_val)
    else:
        r = [1.0, 1.0, 1.0]
    res.append(r)

xs = xrange(len(item))

plt.scatter(xs, [e[0] for e in res], c='r', marker='x', s=20, label='greedy - value')
plt.scatter(xs, [e[1] for e in res], c='b', marker='x', s=20, label='greedy - ratio')
plt.scatter(xs, [e[2] for e in res], c='g', marker='x', s=20, label='dp')
plt.legend()
plt.show()