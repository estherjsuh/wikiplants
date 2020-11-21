import requests
from bs4 import BeautifulSoup
import wikipediaapi
from collections import defaultdict

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



print(dict)