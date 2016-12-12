# Optimization of Caloric and Macronutrient Intake 
# Through Constraint Satisfaction Problems
# A CS182 Final Project
# Annie Hwang | annhwang@college.harvard.edu
# Jason Cui | jasoncui@college.harvard.edu

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from itertools import combinations
import operator
from sklearn.utils import shuffle
import random

##################################################################
######################## DATA EXTRACTION #########################
##################################################################

allRestaraunts = pd.DataFrame.from_csv('data/all.csv')
nutrient_type = 'Fat'
nutrient_capacity = 60

##################################################################
####################### HELPER FUNCTIONS #########################
##################################################################

def finalValueWeight(combination, nutrient_capacity):
    tot_calories = totval = 0
    for food, calories, val in combination:
        tot_calories  += calories
        totval += val
    if tot_calories <= nutrient_capacity:
        return (totval, -tot_calories)
    # if the total calories exceed capacity return 0,0 
    else:
        return (0, 0)

# function that finds all combinations
def combinations(foods):
    result = [[]]
    for food in foods:
        new_comb = [r+[food] for r in result]
        result.extend(new_comb)
    return result

# random assignments for local search algorithms
def randomAssignment(foods, nutrient_capacity):
    # return knapsacked food items and rest of food items
    knapsack = []
    total_weight = 0
    total_value = 0
    keep_adding = True
    # check the knapsack is under weight and there list of foods not empty
    while keep_adding:
        food = random.choice(foods)
        weight = food[1]
        value = food[2]
        if (total_weight + weight) > nutrient_capacity or not foods:
            keep_adding = False
        else:
            foods.remove(food)
            knapsack.append(food)
            total_value += value
            total_weight += weight
    print 'random assignments: ', knapsack
    return [knapsack, foods, total_value, total_weight]

# generating success for local search algorithms
def generateSuccessor(knapsack, foods, nutrient_capacity):
    # swapping items with successor
    # first delete random item from knapsack and put back in food list
    randomFoodInKnapsack = random.choice(knapsack)
    knapsack.remove(randomFoodInKnapsack)
    foods.append(randomFoodInKnapsack)

    # include random item from food list
    total_weight = sum(list(zip(*knapsack)[1]))
    total_value = sum(list(zip(*knapsack)[2]))
    while True:
        food = random.choice(foods)
        weight = food[1]
        if (total_weight + weight) <= nutrient_capacity:
            total_value += food[2]
            total_weight += weight
            break
    knapsack.append(food)
    print 'generateSuccessor:', knapsack
    return [knapsack, foods, total_value, total_weight]

##################################################################
#################### BRUTE FORCE APPROACH #######################
##################################################################

def knapsack_brute_force(items, max_weight):
    knapsack = []
    best_weight = 0
    best_value = 0
    for item_set in combinations(items):
        set_weight = sum(map(weight, item_set))
        set_value = sum(map(value, item_set))
        if set_value > best_value and set_weight <= capacity:
            best_weight = set_weight
            best_value = set_value
            knapsack = item_set
    return knapsack, best_weight, best_value

##################################################################
######################## GREEDY APPROACH #########################
##################################################################

# value heuristic for greedy
def value(items):
    values = items
    values.sort(key=operator.itemgetter(2), reverse=True)
    return values

# val/weight ratio heuristic for greedy
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

def knapsack_greedy(foods, limit, function, column_index):
    knapsack = []
    sorted_foods = function(foods)
    #print 'sorted: ', sorted_foods
    #print sorted_foods
    total_weight = 0
    total_value = 0
    counter = 0
    while (total_weight + sorted_foods[counter][1]) <= limit and (counter < (len(sorted_foods)-1)):
        knapsack.append(sorted_foods[counter][:column_index])
        total_weight += sorted_foods[counter][1]
        total_value += sorted_foods[counter][2]
        counter += 1
    return knapsack, total_weight, total_value


##################################################################
##################### LOCAL SEARCH APPROACH ######################
##################################################################

# Hill Climbing solution
def knapsack_hc(foods, limit):
    currentAssignment = randomAssignment(foods, limit)
    bestAssignment = None
    end = False
    while not end:
        newAssignment = generateSuccessor(currentAssignment[0], currentAssignment[1], limit)
        # compare values from each assignment
        if newAssignment[2] > currentAssignment[2]:
            currentAssignment = newAssignment
        if currentAssignment[1]:
            bestAssignment = currentAssignment
        else:
            end = True
    return bestAssignment[0], bestAssignment[3], bestAssignment[2]


# Simulated Annealing solution
def knapsack_sa(foods, limit):
    return None


##################################################################
################# DYNAMIC PROGRAMMING APPROACH ###################
##################################################################

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

##################################################################
#################### COMPARING ALL ALGORITHMS ####################
##################################################################

result = []
names = allRestaraunts['Item_Name'].values
nutrient = [int(x) for x in allRestaraunts[nutrient_type].values]
protein = [int(x) for x in allRestaraunts['Protein'].values]
item = zip(names, nutrient, protein)
max_weight = nutrient_capacity

# randomizing order of training set b/c some restaurant
# items are better than others
item = shuffle(item)
for i in xrange(len(item)):
    # gradually increase trainings set
    items = item[:i+3]
    knapsack = knapsack_dp(items, max_weight)
    opt_val, opt_wt = finalValueWeight(knapsack, max_weight)
    r = []
    if opt_val != 0:
        # greedy using value heuristic
        knapsack, wt, val = knapsack_greedy(items, max_weight, value, 3)
        r.append(float(val)/opt_val)

        # greedy using value/weight heuristic
        knapsack, wt, val = knapsack_greedy(items, max_weight, val_weight_ratio, 3)
        r.append(float(val)/opt_val)

        # hill climbing
        # knapsack, wt, val = knapsack_hc(items, max_weight)
        # print 'knapsack for hc', knapsack
        
        # DP
        knapsack = knapsack_dp(items, max_weight)
        val, wt = finalValueWeight(knapsack, max_weight)
        r.append(float(val)/opt_val)
    else:
        r = [1.0, 1.0, 1.0]
    result.append(r)

##################################################################
######################## PLOTTING RESULTS ########################
##################################################################

xs = xrange(len(item))
fig = plt.figure()
ax = plt.subplot(111)

ax.scatter(xs, [e[0] for e in result], c='r', marker='x', s=20, label='greedy - value')
ax.scatter(xs, [e[1] for e in result], c='b', marker='x', s=20, label='greedy - ratio')
ax.scatter(xs, [e[2] for e in result], c='g', marker='x', s=20, label='dp')
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()

##################################################################
################# PRINTING AVERAGES OF RESULTS ###################
##################################################################

transposed = zip(*result)
avg = lambda items: float(sum(items)) / len(items)
averages = map(avg, transposed) 
print averages