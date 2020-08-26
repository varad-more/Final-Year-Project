from bs4 import BeautifulSoup
import requests

source1 = requests.get('https://www.medicalnewstoday.com/').text
soup1= BeautifulSoup(source1,'lxml')
article=soup.find('div',{"id":"LATEST NEWS"})
for link in article.find_all('a',class_="css-ni2lnp"):
	headline=link.text
	link='https://www.medicalnewstoday.com'+link["href"]
	print(headline)
	print(link)
	print()



