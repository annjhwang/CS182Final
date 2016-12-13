# Optimization of Caloric and Macronutrient Intake 
# Through Constraint Satisfaction Problems
# A CS182 Final Project
# Jason Cui | jasoncui@college.harvard.edu
# Annie Hwang | annhwang@college.harvard.edu

from constraint import *
import pandas as pd
import numpy as np
from itertools import combinations
import time

from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

class Food():
	def init(self, item):
		self.food_name = item['Item_Name']
		self.protein = item['Protein']
		self.carb = item['Carbohydrates']
		self.fat = item['Fat']
		self.calories = item['Calories']

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

for restaurant, name in zip(restaurants, restaurant_names):
	print name
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
		return (a.protein >20 and a.fat < 15 and a.carb < 50 and a.calories < 600)

	p.addConstraint(func, ["bagged"])
	p.addConstraint(AllDifferentConstraint())
	solutions = p.getSolutions() 

	for sol in solutions:
		print sol['bagged'].food_name
	print 
