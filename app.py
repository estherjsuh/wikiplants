import requests
from bs4 import BeautifulSoup
import wikipediaapi
from collections import defaultdict
import pandas as pd 
import os

html = requests.get('https://en.wikipedia.org/wiki/Houseplant')
soup = BeautifulSoup(html.text, 'html.parser')

##Get query parameters for the list of houseplants##
plantquery = []

for i in soup.select("li > i"):
    for href in i.find_all("a", href=True):
        plantquery.append(href['href'].split('/')[-1])

##Add light, poison, and temperature data for each plant into dictionary##
wiki = wikipediaapi.Wikipedia(language='en')

dict = defaultdict(list)
keywords = ['light', 'poison', '°C']

def search(content_array, search_word, key):
    match = ''
    for sentence in content_array:
        if search_word in sentence:
            match += sentence
            break
    dict[key].append(match)

for plant in plantquery:
    current_content = wiki.page(plant).text
    content_array = current_content.split('.')
    for search_word in keywords:
        search(content_array, search_word, plant)

##Convert dictionary into dataframe##
df = pd.DataFrame([(k, v[0], v[1], v[2]) for k,v in dict.items()], columns=['plant_name', 'light', 'poison', 'temperature'])

##Cleanse Data##

#1. Remove new lines and white-space
df = df.replace({r'\s+$': '', r'^\s+': ''}, regex=True).replace(r'\n',  ' ', regex=True)

#2. When 'poison' is not found in the article, replace empty strings with 'not poisonous' 
df['poison'].replace('', 'not poisonous', inplace=True)

#3. Remove rows with missing data 
df = df.loc[~((df['light']=='') | (df['temperature']==''))]

##Export cleansed data to csv
output = 'plants.csv'
if not os.path.exists('data/'):
    os.mkdir('data/')
fullpathname = 'data/' + output
df.to_csv(fullpathname)