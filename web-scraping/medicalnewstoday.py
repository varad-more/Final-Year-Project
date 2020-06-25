from bs4 import BeautifulSoup
import requests

source = requests.get('https://www.medicalnewstoday.com/').text
soup= BeautifulSoup(source,'lxml')
article=soup.find('div',{"id":"LATEST NEWS"})
for link in article.find_all('a',class_="css-ni2lnp"):
	print(link.text)
	print('https://www.medicalnewstoday.com'+link["href"])	
	print()

