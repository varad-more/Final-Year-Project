from bs4 import BeautifulSoup
import requests

source = requests.get('https://www.hindustantimes.com/health/').text
soup= BeautifulSoup(source,'lxml')
for article in soup.find_all('div',class_='media-body'):
	head=article.a.text
	print(head)

