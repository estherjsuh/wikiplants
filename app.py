import requests
from bs4 import BeautifulSoup
# import wikipedia
import wikipediaapi

html = requests.get('https://en.wikipedia.org/wiki/Houseplant')
soup = BeautifulSoup(html.text, 'html.parser')

plantquery = []

for i in soup.select("li > i"):
    for href in i.find_all("a", href=True):
        plantquery.append(href['href'].split('/')[-1])

light, poison, air, temp = ['']*len(plantquery),['']*len(plantquery),['']*len(plantquery),['']*len(plantquery)

## Bring in wik

wiki = wikipediaapi.Wikipedia(language='en')


for i in range(len(plantquery)):
    current_content = wiki.page(plantquery[i]).text
    content_array = current_content.split('.')
    scrap_light(content_array, light,i)

def scrap_light(content_array, light,i):
    for sentence in content_array:
        if 'light' in sentence:
            light[i] += sentence
            break
