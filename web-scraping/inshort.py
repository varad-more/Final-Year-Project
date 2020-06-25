from bs4 import BeautifulSoup
import requests
import csv

source = requests.get('https://inshorts.com/en/read').text
soup= BeautifulSoup(source,'lxml')

source1 = requests.get('https://indianexpress.com/section/india/').text
soup1= BeautifulSoup(source1,'lxml')


csv_file = open('cms_scrape.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headline', 'summary','link'])

for article in soup.find_all('div',class_='news-card z-depth-1'):
	
	headline=article.select_one("span[itemprop*=headline]").text
	print(headline)
	summary=article.select_one("div[itemprop*=articleBody]").text
	print()
	print(summary)
	try:
		link=article.find('div',class_='read-more')
		link1=link.a["href"]
		print(link1)
	except:
		link1='https://inshorts.com/en/read'
		print(link1)
	print()
	print()
	csv_writer.writerow([headline, summary,link1])

for article1 in soup1.find_all('div',class_='articles'):
	headline=article1.h2.text
	print(headline)
	summary=article1.p.text
	print()
	print(summary)
	link=article1.a
	link1=link["href"]
	print(link1)
	print()
	print()
	csv_writer.writerow([headline, summary,link1])
csv_file.close()
