import pandas as pd
import numpy as np

try:
    xrange
except:
    xrange = range
 
# allows user to input maximum caloric intake
max_calories = input('Enter the maximum amount of calories: ')

def totalvalue(comb):
    ' Totalise a particular combination of items'
    totwt = totval = 0
    for item, wt, val in comb:
        totwt  += wt
        totval += val
    return (totval, -totwt) if totwt <= max_calories else (0, 0)
 
items = pd.DataFrame.from_csv('burgerkingdata.csv')
items = items.drop('Food Category', 1)
items = items.drop('Item Description 2015', 1)
items = items.drop('Servings Size Text 2015', 1)
items = items.drop('Menu_Item_ID', 1)
items = items.drop('Serving Size Unit 2015', 1)
items = items.drop('Servings Per Item 2015', 1)

names = items['Item_Name'].values
calories = items['Calories 2015'].values
protein = items['Protein (g) 2015'].values
items = zip(names, calories, protein)

print type(items)
 
def knapsack01_dp(items, limit):
    table = [[0 for w in range(limit + 1)] for j in xrange(len(items) + 1)]
 
    for j in xrange(1, len(items) + 1):
        item, wt, val = items[j-1]
        for w in xrange(1, limit + 1):
            if wt > w:
                table[j][w] = table[j-1][w]
            else:
                table[j][w] = max(table[j-1][w],
                                  table[j-1][w-wt] + val)
 
    result = []
    w = limit
    for j in range(len(items), 0, -1):
        was_added = table[j][w] != table[j-1][w]
 
        if was_added:
            item, wt, val = items[j-1]
            result.append(items[j-1])
            w -= wt
 
    return result
 
 
bagged = knapsack01_dp(items, max_calories)
print bagged
print("Bagged the following items\n  " +
      '\n  '.join(sorted(item for item,_,_ in bagged)))
val, wt = totalvalue(bagged)
print("for a total grams of protein of %i and a total caloric intake of %i" % (val, -wt))