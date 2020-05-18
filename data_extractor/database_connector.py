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
txt=['Date:01/02/2020', 'Name:Chavaa', 'Gender:Male', 'Age:12', 'TestNameResultsUnitsBio.Ref.Interval\rCOMPLETE BLOOD COUNT (CBC)\r(Electrical Impedance & VCS,Photometry ):', 'Hemoglobin:14.40', 'Packed Cell Volume (PCV):43.80', 'RBC Count:5.27', 'MCV:83.00', 'MCH:27.20', 'MCHC:32.80', 'Red Cell Distribution Width (RDW):14.50', 'Total Leukocyte Count (TLC):11.00', 'Differential Leucocyte Count (DLC):', 'Segmented Neutrophils:66.40', 'Lymphocytes:24.70', 'Monocytes:4.90', 'Eosinophils:3.10', 'Basophils:0.90', 'Absolute Leucocyte Count:', 'Neutrophils:7.30', 'Lymphocytes:2.72', 'Monocytes:0.54', 'Eosinophils:0.34', 'Basophils:0.10', 'Platelet Count:290.0', 'COMPLETE BLOOD COUNT (CBC):', 'Hemoglobin:14.40', 'Packed Cell Volume (PCV):43.80', 'RBC Count:5.27', 'MCV:83.00', 'MCH:27.20', 'MCHC:32.80', 'Red Cell Distribution Width (RDW):14.50', 'Total Leukocyte Count (TLC):11.00', 'Differential Leucocyte Count (DLC):', 'Segmented Neutrophils:66.40', 'Lymphocytes:24.70', 'Monocytes:4.90', 'Eosinophils:3.10', 'Basophils:0.90', 'Absolute Leucocyte Count:', 'Neutrophils:7.30', 'Lymphocytes:2.72', 'Monocytes:0.54', 'Eosinophils:0.34', 'Basophils:0.10', 'Platelet Count:290.0']

mydict = { "name": name, "gender": gender, "Date":"12","Irregularities":"abc", "Free_text":txt }
x = mycol.insert_one(mydict)
print (x)