import pandas as pd
import tabula
import json 

#Using tabula to read the PDF and extract tables from it.
df = tabula.read_pdf("1.pdf", pages = '1', multiple_tables = True, output_format="json")

#Tabula data table can be converted into JSON format. Making extraction easy.
data =json.loads(json.dumps(df))
# print (json.dumps(data,indent=2))

# Extracting Data field(table) in particular
for d in data:
    d1= (d["data"])
print (d1)

#For invidual rows in table
d3 = json.loads(json.dumps(d1))
print ("Layer 3##########################")
print(len(d3))


print (d3[0])

# Individual value and data extractions as per our needs
a=json.loads(json.dumps(d3[2]))
print (type(a))
print (a[1])

for i in range (2,23):
    a=json.loads(json.dumps(d3[i]))
    b=json.loads(json.dumps(a[0]))
    c=json.loads(json.dumps(a[1]))
    print (b["text"]+" : " + c["text"])
