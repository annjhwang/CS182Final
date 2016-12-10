# ***Temporary Title Here***
# A CS182 Final Project
# Jason Cui | jasoncui@college.harvard.edu
# Annie Hwang | annhwang@college.harvard.edu
import pandas as pd
import numpy as np
from itertools import combinations
import operator
import time
 
# allows user to input maximum caloric intake
nutrient_type = raw_input('Enter the type of nutrient you want to limit: ')
print 'nutrient:', nutrient_type
nutrient_capacity = input('Enter the maximum maximum of this nutrient (in kcal or g): ')
print 'Capacity for ' + str(nutrient_type) + ' intake: ' + str(nutrient_capacity)

# importing all the data and cleaning
burgerking = pd.DataFrame.from_csv('burgerking.csv')
elpollo = pd.DataFrame.from_csv('elpollo.csv')
chickfila = pd.DataFrame.from_csv('chickfila.csv')
tacobell = pd.DataFrame.from_csv('tacobelldata.csv')
subway= pd.DataFrame.from_csv('subwaydata.csv')
abp = pd.DataFrame.from_csv('ABP.csv')
pandaexpress = pd.DataFrame.from_csv('pandaexpress.csv')
panera = pd.DataFrame.from_csv('panera.csv')
carlsjr = pd.DataFrame.from_csv('carlsjr.csv')
kfc = pd.DataFrame.from_csv('kfc.csv')

restaurants = [burgerking, elpollo, chickfila, tacobell, subway, abp, pandaexpress, panera, carlsjr, kfc]
restaurant_names = ['Burger King', 'El Pollo Loco', 'Chick-Fila-A' , 'Taco Bell', 'Subway', 'Au Bon Pain', 'Panda Express', 'Panera Bread', 'Carls Jr', 'KFC']

def weight(item):
	return item[1]

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
def knapsack_greedy(foods, limit):
    knapsack = []
    sorted_foods = val_weight_ratio(foods)
    #print sorted_foods
    total_weight = 0
    counter = 0
    while total_weight < limit:
        knapsack.append(sorted_foods[counter][:3])
        counter += 1
        total_weight += sorted_foods[counter][1]
    return knapsack

def totalvalue(comb):
    tot_calories = totval = 0
    for item, calories, val in comb:
        tot_calories  += calories
        totval += val
    return (totval, -tot_calories) if tot_calories <= nutrient_capacity else (0, 0)

for restaurant, name in zip(restaurants, restaurant_names):
    names = restaurant['Item_Name'].values
    print nutrient_type
    nutrient = [int(x) for x in restaurant[nutrient_type].values]
    protein = restaurant['Protein'].values
    items = zip(names, nutrient, protein)

    # knapsack problem for burgerking 
    bagged = knapsack_greedy(items, nutrient_capacity)
    print("Bagged the following food items from " + name + ":\n  " +
          '\n  '.join(sorted(item for item,_,_ in bagged)))
    val, nutrient = totalvalue(bagged)
    print("Total grams of protein of " + str(val) + " and a total " + nutrient_type + " intake of " + str(-nutrient))
