from bs4 import BeautifulSoup
import requests
import csv
from urllib.request import urlopen

source1 = requests.get('https://inshorts.com/en/read').text
soup1= BeautifulSoup(source1,'lxml')

source2 = requests.get('https://indianexpress.com/section/india/').text
soup2= BeautifulSoup(source2,'lxml')

source3 = requests.get('https://www.medicalnewstoday.com/').text
soup3= BeautifulSoup(source3,'lxml')

'''news_url="https://news.google.com/news/rss"
Client=urlopen(news_url)
xml_page=Client.read()
Client.close()

soup_page=soup(xml_page,"xml")
news_list=soup_page.findAll("item")'''


csv_file = open('cms_scrape.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headline', 'summary','link'])

for article in soup1.find_all('div',class_='news-card z-depth-1'):
	
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

for article1 in soup2.find_all('div',class_='articles'):
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

article2=soup3.find('div',{"id":"LATEST NEWS"})
for link in article2.find_all('a',class_="css-ni2lnp"):
	headline=link.text
	print(headline)
	link1='https://www.medicalnewstoday.com'+link["href"]	
	print(link1)
	csv_writer.writerow([headline,link1])
	
'''soup_page=soup(xml_page,"xml")
news_list=soup_page.findAll("item")
# Print news title, url and publish date
for news in news_list:
	headline=news.title.text
	summary=news.pubDate.text
	link1=news.link.text
	csv_writer.writerow([headline, summary,link1])


csv_file.close()'''


