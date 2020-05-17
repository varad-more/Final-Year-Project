import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["test"]
print(mydb)
# print(myclient.list_database_names())
mycol = mydb["reports"]
print (mycol)

# Checking if Collection exists
collist = mydb.list_collection_names()
if "reports" in collist:
  print("The collection exists.")

name="test"
gender="Male"

mydict = { "name": name, "gender": gender, "Date":"12","Irregularities":"abc" }
x = mycol.insert_one(mydict)
print (x)