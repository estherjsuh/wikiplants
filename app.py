import requests
from bs4 import BeautifulSoup
import wikipediaapi
from collections import defaultdict
import pandas as pd 
import os

html = requests.get('https://en.wikipedia.org/wiki/Houseplant')
soup = BeautifulSoup(html.text, 'html.parser')

plantquery = []

for i in soup.select("li > i"):
    for href in i.find_all("a", href=True):
        plantquery.append(href['href'].split('/')[-1])

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


df = pd.DataFrame([(k, v[0], v[1], v[2]) for k,v in dict.items()], columns=['plant_name', 'light', 'poison', 'temperature'])

df = df.replace('\n','', regex=True)

output = 'plants.csv'
if not os.path.exists('data/'):
    os.mkdir('data/')
fullpathname = 'data/' + output
df.to_csv(fullpathname)