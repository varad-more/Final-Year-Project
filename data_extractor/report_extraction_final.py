#Combined Version 
import pymongo
import tabula
import json 
import numpy
from datetime import datetime

#Using tabula to read the PDF and extract tables from it.
df = tabula.read_pdf("10.pdf", pages = 'all', multiple_tables = True, output_format="json")

#Tabula data table can be converted into JSON format. Making extraction easy.
data =json.loads(json.dumps(df))
i=0

d1 = numpy.empty(len(data), dtype=object) 

#Dictioanry test
final_report={}
for d in data:
    d1=(d["data"])
    # print (d1)
    print ("##############")

#For invidual rows in table
    d3 = json.loads(json.dumps(d1))
    l=len(d3)

# Individual value and data extractions as per our needs
    a=json.loads(json.dumps(d3))
    report_data=numpy.empty(l,dtype=object) 
    for i in range (0,l):
        a=json.loads(json.dumps(d3[i]))
        b=json.loads(json.dumps(a[0]))
        c=json.loads(json.dumps(a[1]))
        report_data[i]=(b["text"]+":"+ c["text"])
        final_report[b["text"]]=c["text"]

#For individual element
from datetime import datetime
date = datetime.strptime(final_report['Date'], '%d/%m/%Y').date()
# final_report['Date'] = date
print (final_report)
print (len(final_report))

#Reference Values for Males
ref_male={'Fasting Sugar':120,
'Hemoglobin':{'min':14, 'max':18},
'RBC Count':{'min':4.5,'max':6.4},
'Packed Cell Volume (PCV)' : {'min':42,'max':52},
'MCV' :{'min':78,'max':94},
'MCH': {'min':27,'max':32},
'MCHC'	: {'min':32,'max':38},
'WBV (Leucocytes)': {'min':4000,'max':11000},	
'Neutrophils': {'min':60,'max':75},	
'Lymphocytes': {'min':20,'max':30},	
'Monocytes'	 : {'min':2,'max':8},
'Eosinophils': {'min':1,'max':6},
'Basophils' : {'min':0,'max':1},
'Platelet' : {'min':15000,'max':450000},
'Post Prandial (PP) Blood Sugar'	: 120,
'Blood-Glucose Level Maximum Value'	: 160,
'Glycosylated Haemoglobin':{'min' :	4.2, 'max': 7.6},
'Blood Urea' :{'min' :	0, 'max': 40} ,
'BUN-Blood Urea Nitrogen':{'min' :	0, 'max': 18},
'Serum Uric acid'	:{'min' :3, 'max': 5.7},
'Serum Creatinine'	:{'min' :0.5, 'max': 1.4},
'Routine urine for albumin':	'Nil',
}

#Reference Values for Females
ref_female = { 
    'Hemoglobin':{'min':14, 'max':18},
}

#Final reference variable for comparision
ref={}

#Implementation of Basic function for gender categorization
# ref=ref_male
#def ref_gender():
if final_report['Gender'] == 'Male':
        print ('Male')
        ref = ref_male
    
elif final_report['Gender'] == 'Female':
        print ('Female')
        ref = ref_female
    
else:
        print ("Error")
#Function Ends
 
# ref_gender()
# print(ref)


normal={}
abnormal={}
not_found={}

#Comparing Parameters and mapping with reference values

def param_cmp():
    for i in final_report:
        try :
            if (type(ref[i]) is dict):
                print ("Dict#######################",i)
            
                # print (ref[i])
                # print (final_report[i])
                reference = ref[i]
                min = float(reference['min'])
                max = float(reference['max'])
                obs = float(final_report[i])
                # print (max,min)
                
                if(obs< max) & (obs>min):
                    print (i," - Obserserved Normal")
                    normal [i] = obs
                else:
                    print (i," - Abnormalities Obserserved")
                    abnormal[i] = obs

            elif (type(ref[i]) is float) | (type(ref[i]) is int)  :
                print ("Float~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",i)
            
                print (ref[i])
                print (final_report[i])
                max = float(ref[i])
                # max = float(reference[i])
                # max = float(reference['max'])
                obs = float(final_report[i])
                # print (max,min)
                
                if(obs< max):
                    print (i," - Obserserved Normal")
                    normal [i] = obs
                else:
                    print (i," - Abnormalities Obserserved")
                    normal [i] = obs         
        
        except:
            not_found[i] = final_report[i]
            pass
            # print(i," ----    Value not found")


param_cmp()
print('\n Normal Values', normal)
print ('#############################')
print('\n ABNORMAL Values', abnormal)
print ('#############################')
print('\n Error 404:', not_found)


def database_connect():
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient["test"]
	print(mydb)

	mycol = mydb["reports"]
	print (mycol)

	collist = mydb.list_collection_names()
	if "reports" in collist:
  		print("The collection exists.")

	name=final_report['Name']
	gender=final_report['Gender']
	
	mydict = { "name": name, "gender": gender, "Date":final_report['Date'],"normal":normal, "abnormalities": abnormal }
	x = mycol.insert_one(mydict)
	print (x)

database_connect()