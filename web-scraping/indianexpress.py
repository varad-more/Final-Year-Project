from bs4 import BeautifulSoup
import requests
import csv

source = requests.get('https://indianexpress.com/section/india/').text
soup= BeautifulSoup(source,'lxml')
for article in soup.find_all('div',class_='articles'):
	link=article.a
	print(link["href"])
	print(article.h2.text)
	print(article.p.text)
	print()

