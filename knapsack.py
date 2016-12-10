# ***Temporary Title Here***
# A CS182 Final Project
# Jason Cui | jasoncui@college.harvard.edu
# Annie Hwang | annhwang@college.harvard.edu
import pandas as pd
import numpy as np
from itertools import combinations
import time
 

# allows user to input maximum caloric intake
nutrient_type = raw_input('Enter the type of nutrient you want to limit: ')
print 'nutrient:', nutrient_type
nutrient_capacity = input('Enter the maximum maximum of this nutrient (in kcal or g): ')
print 'Capacity for ' + str(nutrient_type) + ' intake: ' + str(nutrient_capacity)

# importing all the data and cleaning
burgerking = pd.DataFrame.from_csv('data/burgerking.csv')
elpollo = pd.DataFrame.from_csv('data/elpollo.csv')
chickfila = pd.DataFrame.from_csv('data/chickfila.csv')
tacobell = pd.DataFrame.from_csv('data/tacobelldata.csv')
subway= pd.DataFrame.from_csv('data/subwaydata.csv')
abp = pd.DataFrame.from_csv('data/ABP.csv')
pandaexpress = pd.DataFrame.from_csv('data/pandaexpress.csv')
panera = pd.DataFrame.from_csv('data/panera.csv')
carlsjr = pd.DataFrame.from_csv('data/carlsjr.csv')
kfc = pd.DataFrame.from_csv('data/kfc.csv')

restaurants = [burgerking, elpollo, chickfila, tacobell, subway, abp, pandaexpress, panera, carlsjr, kfc]
restaurant_names = ['Burger King', 'El Pollo Loco', 'Chick-Fila-A' , 'Taco Bell', 'Subway', 'Au Bon Pain', 'Panda Express', 'Panera Bread', 'Carls Jr', 'KFC']

def totalvalue(comb):
    tot_calories = totval = 0
    for item, calories, val in comb:
        tot_calories  += calories
        totval += val
    return (totval, -tot_calories) if tot_calories <= nutrient_capacity else (0, 0)

# BRUTE FORCE APPROACH 
def knapsack_brute_force(items):
    # brute force approach that just tries every combination possible
    return ( comb
             for r in range(1, len(items)+1)
             for comb in combinations(items, r)
             )
 
# DYNAMIC PROGRAMMING APPROACH
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

# TIME BRUTE FORCE APPROACH FOR 10 RESTAURANTS
'''
print 'Brute Force Approach:'
start_time = time.time()
for restaurant, name in zip(restaurants, restaurant_names):
    names = restaurant['Item_Name'].values
    calories = restaurant['Calories'].values
    protein = restaurant['Protein (g)'].values
    items = zip(names, calories, protein)

    # knapsack problem for burgerking 
    bagged = max(knapsack_brute_force(items), key=totalvalue)
    print("Bagged the following food items from " + name + ":\n  " +
          '\n  '.join(sorted(item for item,_,_ in bagged)))
    val, calories = totalvalue(bagged)
    print("Total grams of protein of %i and a total caloric intake of %i" % (val, -calories)) 
end_time = time.time()
print("--- %s seconds ---" % (end_time - start_time))'''

# TIME DP APPROACH FOR 10 RESTAURANTS 
print 'Dynamic Programming Approach:'
start_time = time.time()
for restaurant, name in zip(restaurants, restaurant_names):
    names = restaurant['Item_Name'].values
    print nutrient_type
    nutrient = [int(x) for x in restaurant[nutrient_type].values]
    protein = restaurant['Protein'].values
    items = zip(names, nutrient, protein)

    # knapsack problem for burgerking 
    bagged = knapsack_dp(items, nutrient_capacity)
    print("Bagged the following food items from " + name + ":\n  " +
          '\n  '.join(sorted(item for item,_,_ in bagged)))
    val, nutrient = totalvalue(bagged)
    print("Total grams of protein of " + str(val) + " and a total " + nutrient_type + " intake of " + str(-nutrient))
end_time = time.time()
print("--- %s seconds ---" % (end_time - start_time))