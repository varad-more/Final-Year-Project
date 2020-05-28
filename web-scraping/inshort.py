from bs4 import BeautifulSoup
import requests
import csv

source = requests.get('https://inshorts.com/en/read').text
soup= BeautifulSoup(source,'lxml')

csv_file = open('cms_scrape.csv', 'w')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headline', 'summary'])

for article in soup.find_all('div',class_='news-card z-depth-1'):
	
	headline=article.select_one("span[itemprop*=headline]").text
	print(headline)
	summary=article.select_one("div[itemprop*=articleBody]").text
	print()
	print(summary)
	print()
	print()
	csv_writer.writerow([headline, summary])
csv_file.close()
