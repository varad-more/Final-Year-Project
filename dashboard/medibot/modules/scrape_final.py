from bs4 import BeautifulSoup
import requests
import mysql.connector

start="<p>"
end="</p>"

# pip3 install mysql-connector-python 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="virtual_managers" # Change as per requirements
)

mycursor = mydb.cursor()



def database_connect():
    # #Reading from Database
    # mycursor.execute("SELECT * FROM dashboard_scraped_data")
    # rows = mycursor.fetchall()
    # print (rows)

    #Inserting into Database
    sql = ("INSERT INTO dashboard_scraped_data (headline,summary,links ) values (%s, %s, %s)") 
    data = (headline,summary,link)
    # print(data)	
    print (headline)

    # mycursor.execute(sql, data)
    # mydb.commit()  # Changes are not commited until you put this, so testing ke liye nikal ke try kar sakte ho.
    # print(mycursor.rowcount, "record inserted.")



source1 = requests.get('https://www.medicalnewstoday.com/').text
soup1= BeautifulSoup(source1,'lxml')
print (soup1)
article=soup1.find('div',{"id":"latest-news"})
print ('article:', article)
for link in article.find_all('a',class_="css-ni2lnp"):
    headline=link.text
    link='https://www.medicalnewstoday.com'+link["href"]
    print ('medical_news:',headline)
    print ('______________________________')
    print ('______________________________')

def extract_source(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    source=requests.get(url, headers=headers).text
    return source
          
source=extract_source('https://www.hindustantimes.com/lifestyle/health')
soup= BeautifulSoup(source,'lxml')
for article in soup.find_all('h2',class_="hdg3"):
    headline=article.a.text
    r=article.a
    link='https://www.hindustantimes.com/'+r['href']
    '''page=article.p
    res=str(page)
    if res.startswith(start):
        res=res.replace(start,"")
        res=res.replace(end,"")
    summary=res'''
    summary=" "
    if summary == "None":
        database_connect()
    database_connect()

