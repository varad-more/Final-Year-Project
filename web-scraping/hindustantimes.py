from bs4 import BeautifulSoup
import requests
import re

start="<p>"
end="</p>"

def extract_source(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
	source=requests.get(url, headers=headers).text
	return source
        
def extract_data(source):
	soup= BeautifulSoup(source,'lxml')
	for article in soup.find_all('div',class_="media-body"):
		link=article.a.text
		r=article.a
		print(link)
		print(r['href'])
		page=article.p
		res=str(page)
		# result = re.search('<p>;</p>', res)
		if res.startswith(start):
			res=res.replace(start,"")
			print(res.replace(end,""),"#######")
		# print()
		# print(result)
		# print()
'''source = requests.get('https://www.hindustantimes.com/health/').text
soup= BeautifulSoup(source,'lxml')
print(soup)
article=soup.find('div',class_="media-body")
print(article)
for article in soup.find_all('div',class_="media-left"):
	link=article.a
	print(link)'''

extract_data(extract_source('https://www.hindustantimes.com/health/'))
