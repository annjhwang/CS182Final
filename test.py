# ***Temporary Title Here***
# A CS182 Final Project
# Jason Cui | jasoncui@college.harvard.edu
# Annie Hwang | annhwang@college.harvard.edu
import pandas as pd
# from constraint import *
import numpy as np
from itertools import combinations
import time
 
from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)
app.debug = True

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
restaurant_static = ['/static/burgerking.jpg', '/static/elpollo.png', '/static/chickfila.jpg', '/static/tacobell.jpg', '/static/subway.jpg', '/static/abp.png', \
                    '/static/pandaexpress.png', '/static/panera.jpg', '/static/carlsjr.jpeg', '/static/kfc.png']

class Food():
    def init(self, item):
        self.food_name = item['Item_Name']
        self.protein = item['Protein']
        self.carb = item['Carbohydrates']
        self.fat = item['Fat']
        self.calories = item['Calories']

@app.route('/')
def my_form(name=None):
    return render_template('my-form.html', name=name)

@app.route('/', methods=['POST'])
def my_form_post():
    #nutrient_type = str(request.form['nutrient'])
    nutrient_type = str(request.form['nutrient'])
    capacity = request.form['capacity']
    #print nutrient
    nutrient_capacity = int(capacity)

    def finalValueWeight(comb):
        tot_nutrients = totval = 0
        for item, nutrient, val in comb:
            tot_nutrients  += nutrient
            totval += val
        return (totval, -tot_nutrients) if tot_nutrients <= nutrient_capacity else (0, 0)

     
    # DYNAMIC PROGRAMMING APPROACH
    def knapsack_dp(foods, limit):
        # 2D table to memoize as we go
        table = [[0 for w in range(limit + 1)] for j in xrange(len(foods) + 1)]
        for j in xrange(1, len(foods) + 1):
            food, nutrient, val = foods[j-1]
            for w in xrange(1, limit + 1):
                if nutrient > w:
                    table[j][w] = table[j-1][w]
                else:
                    table[j][w] = max(table[j-1][w],
                                      table[j-1][w-nutrient] + val)
        best_foods = []
        w = limit
        for j in range(len(foods), 0, -1):
            was_bagged = table[j][w] != table[j-1][w]
            # checking if the food has been added to the bag
            if was_bagged:
                food, nutrient, val = foods[j-1]
                best_foods.append(foods[j-1])
                # decrementing the limit as we add more food items
                w -= nutrient
        return best_foods


    answers = []
    for restaurant, name, image in zip(restaurants, restaurant_names, restaurant_static):
        #answer = ''
        names = restaurant['Item_Name'].values
        chosen_nutrient = [int(x) for x in restaurant[nutrient_type].values]
        protein = restaurant['Protein'].values
        items = zip(names, chosen_nutrient, protein)
        # knapsack problem for burgerking 
        bagged_foods = knapsack_dp(items, nutrient_capacity)
        val, chosen_nutrient = finalValueWeight(bagged_foods)
        #bagged = knapsack_dp(items, nutrient_capacity)
        #answer += ("Bagged the following food items from " + name + ":\n  " +
        #      '\n  '.join(sorted(item for item,_,_ in bagged)))
        
        #answer += "Total grams of protein of " + str(val) + " and a total " + nutrient_type + " intake of " + str(-chosen_nutrient)
       
        answers.append([name,bagged_foods, val, -chosen_nutrient, image, nutrient_type])
    return render_template("returned-output.html",result = answers)
    #return answer

@app.route('/csp')
def my_csp_form(name=None):
    return render_template('my-csp-form.html', name=name)

@app.route('/csp', methods=['POST'])
def my_csp_post(name=None):
    
    calories = int(request.form['calories'])
    carbs = int(request.form['carb'])
    protein = int(request.form['protein'])
    fat = int(request.form['fat'])
    print calories
    answers = []
    for restaurant, name in zip(restaurants, restaurant_names):
        #print name
        foods = []
        for i in range(len(restaurant)):
        #for i in range(1):
            item = restaurant.iloc[i]
            #print item
            food = Food()
            food.init(item)
            #print 'protein: ', food.protein
            foods.append(food)
        p = Problem()
        p.addVariables(["bagged"], foods)
        def func(a):
            protein_total = 0
            return (a.protein > protein and a.fat < fat and a.carb < carbs and a.calories < calories)

        p.addConstraint(func, ["bagged"])
        p.addConstraint(AllDifferentConstraint())
        solutions = p.getSolutions() 

        for sol in solutions:
            food = []
            name = sol['bagged'].food_name
            protein = sol['bagged'].protein
            carb = sol['bagged'].carb
            calories = sol['bagged'].calories
            food.append([name, protein, carb, calories])
        answers.append(food)

    return render_template("returned-csp.html",result = answers)

if __name__ == '__main__':
    app.run()