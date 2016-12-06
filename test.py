# ***Temporary Title Here***
# A CS182 Final Project
# Jason Cui | jasoncui@college.harvard.edu
# Annie Hwang | annhwang@college.harvard.edu
import pandas as pd
import numpy as np
from itertools import combinations
import time
 
from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

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


@app.route('/')
def my_form(name=None):
    return render_template('my-form.html', name=name)

@app.route('/', methods=['POST'])
def my_form_post():
    #nutrient_type = str(request.form['nutrient'])
    nutrient_type ='Carbohydrates'
    capacity = request.form['capacity']
    #print nutrient
    nutrient_capacity = int(capacity)

    def totalvalue(comb):
	    tot_nutrients = totval = 0
	    for item, nutrient, val in comb:
	        tot_nutrients  += nutrient
	        totval += val
	    return (totval, -tot_nutrients) if tot_nutrients <= nutrient_capacity else (0, 0)

	 
	# DYNAMIC PROGRAMMING APPROACH
    def knapsack_dp(foods, limit):
	    table = [[0 for w in range(limit + 1)] for j in xrange(len(foods) + 1)]
	    for j in xrange(1, len(foods) + 1):
	        food, nutrient, val = foods[j-1]
	        for w in xrange(1, limit + 1):
	            if nutrient> w:
	                table[j][w] = table[j-1][w]
	            else:
	                table[j][w] = max(table[j-1][w],
	                                  table[j-1][w-nutrient] + val)
	    best_foods = []
	    w = limit
	    for j in range(len(foods), 0, -1):
	        was_added = table[j][w] != table[j-1][w]
	 
	        if was_added:
	            food, nutrient, val = foods[j-1]
	            best_foods.append(foods[j-1])
	            w -= nutrient
	    return best_foods


    answer = ' '
    for restaurant, name in zip(restaurants, restaurant_names):
	    names = restaurant['Item_Name'].values
	    chosen_nutrient = [int(x) for x in restaurant[nutrient_type].values]
	    protein = restaurant['Protein'].values
	    items = zip(names, chosen_nutrient, protein)
	    # knapsack problem for burgerking 
	    bagged = knapsack_dp(items, nutrient_capacity)
	    answer += ("Bagged the following food items from " + name + ":\n  " +
	          '\n  '.join(sorted(item for item,_,_ in bagged)))
	    val, chosen_nutrient = totalvalue(bagged)
	    answer += "Total grams of protein of " + str(val) + " and a total " + nutrient_type + " intake of " + str(-chosen_nutrient)

    return answer

if __name__ == '__main__':
    app.run()