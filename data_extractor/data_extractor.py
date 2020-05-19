# import pandas as pd
import tabula
import json 
import numpy
from datetime import datetime

#Using tabula to read the PDF and extract tables from it.
df = tabula.read_pdf("10.pdf", pages = 'all', multiple_tables = True, output_format="json")

#Tabula data table can be converted into JSON format. Making extraction easy.
data =json.loads(json.dumps(df))
# print (json.dumps(data,indent=2))
# print (df)
# Extracting Data field(table) in particular
# print (len(data))
# print(data)
i=0
# d1 = []
d1 = numpy.empty(len(data), dtype=object) 
# final_report=[]

#Dictioanry test
final_report={}
for d in data:
    d1=(d["data"])
    # print (d1)
    print ("##############")

#For invidual rows in table
    d3 = json.loads(json.dumps(d1))
    # print ("Layer 3##########################")
# print(len(d3))
    l=len(d3)

    # print (d3[0])

# Individual value and data extractions as per our needs
    a=json.loads(json.dumps(d3))
    # print (type(a))
    # print (a[1])
    report_data=numpy.empty(l,dtype=object) 
    for i in range (0,l):
        a=json.loads(json.dumps(d3[i]))
        b=json.loads(json.dumps(a[0]))
        c=json.loads(json.dumps(a[1]))
        # print (b["text"]+" : " + c["text"])
        report_data[i]=(b["text"]+":"+ c["text"])
        # if b["text"] == "Date":
        #     datetime_object = datetime.strptime(c["text"],'%m/%d/%y')
        #     print(datetime_object)
    # print (report_data)
        # final_report.append(report_data[i])
        final_report[b["text"]]=c["text"]
    print ('```````````')
print (final_report)
print (len(final_report))

#For individual element
# print(final_report[47].split(':'))
#print(final_report['Date'])

from datetime import datetime
date = datetime.strptime(final_report['Date'], '%d/%m/%Y').date()
final_report['Date'] = date
print (date)


'''
    # print (d)
    d1[i]=(d["data"])
    # print (d1)
    print ("##############")
    i=i+1

#For invidual rows in table
d3 = json.loads(json.dumps(d1[0]))
print ("Layer 3##########################")
print(len(d3))
l=len(d3)

print (d3[0])

# Individual value and data extractions as per our needs
a=json.loads(json.dumps(d3))
print (type(a))
print (a[1])

for i in range (0,l):
    a=json.loads(json.dumps(d3[i]))
    b=json.loads(json.dumps(a[0]))
    c=json.loads(json.dumps(a[1]))
    print (b["text"]+" : " + c["text"])
    '''
