from bs4 import BeautifulSoup
import requests
import csv

source = requests.get('https://inshorts.com/en/read').text
soup= BeautifulSoup(source,'lxml')

for article in soup.find_all('div',class_='news-card z-depth-1'):
	headline=article.select_one("span[itemprop*=headline]").text
	print(headline)
	summary=article.select_one("div[itemprop*=articleBody]").text
	print()
	print(summary)
	link=article.find('div',class_='read-more')
	print(link.a["href"])
	print()
	print()
