'''
from PyPDF2 import PdfFileReader

def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

    txt = f"""
    Information about {pdf_path}: 

    Author: {information.author}
    Creator: {information.creator}
    Producer: {information.producer}
    Subject: {information.subject}
    Title: {information.title}
    Number of pages: {number_of_pages}

    """

    print(txt)
    return information

if __name__ == '__main__':
    path = '1.pdf'
    extract_information(path)
'''

import pandas as pd
import tabula
import json 
file = "1.pdf"
path =  file
df = tabula.read_pdf(path, pages = '1', multiple_tables = True, output_format="json")
# print(df.text)    

par= (json.dumps(df))
data =json.loads(par)
print (json.dumps(data,indent=2))
# print (data)

for d in data:
    d1= (d["data"])
print (d1)

d2 = json.dumps(d1)
print ("d2############################")
print (d2)
d3 = json.loads(d2)
print ("d3##########################")
print(len(d3))


print (d3[0])
a=json.loads(json.dumps(d3[2]))
print (type(a))
print (a[1])
b=json.loads(json.dumps(a[1]))
print (b["text"])




# print (d3)
# d3 = json.dumps(d3)
# print (d3)
# # for d in d2:
# #     d4=(d2['text'])
# print(type (d3))
# print (d3[4])
print("########################################")


# d4 = json.dumps(d3,indent=2)
# print (d4)
# print(type (d4))

# for d in d4:
# print (d4[6])