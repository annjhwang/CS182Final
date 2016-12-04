
import re
import csv
from bs4 import BeautifulSoup
import urllib

r = urllib.urlopen('https://www.mcdonalds.com/us/en-us/about-our-food/nutrition-calculator.html').read()
soup = BeautifulSoup(r)
print type(soup)

#print soup.prettify()[1000:2000]



print soup.find('tbody')