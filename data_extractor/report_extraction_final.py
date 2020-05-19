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

#Reference Values for Females
ref_female={
'Hemoglobin':{'min':12, 'max':16.4},
'Total WBC Count':{'min':4000, 'max':11000},
'Packed Cell Volume (PCV)' : {'min':37,'max':47},
'WBV (Leucocytes)': {'min':4000,'max':11000},	
'Neutrophils': {'min':60,'max':75},	
'Lymphocytes': {'min':20,'max':30},	
'Monocytes'	 : {'min':2,'max':8},
'Esoinophils': {'min':1,'max':6},
'Basophils' : {'min':0,'max':1},
'RBC Count':{'min_RBC':4.0,'max_RBC':5.4},
'MCV' :{'min':78,'max':94},
'MCH': {'min':27,'max':32},
'MCHC'	: {'min':32,'max':38},
'RDW' :{'min':12.2,'max':16.1},
'Platelets' : {'min':150000,'max':450000},
'Reticulocytes':{'min':0.5,'max':1.5}
'Color Index':{'min':0.85,'max':1.15}
'ESR':{'min':0,'max':20}
'Fasting Sugar':120,
'Post Prandial (PP) Blood Sugar'	: 120,
'Blood-Glucose Level Maximum Value'	: 160,
'Glycosylated Haemoglobin':{'min' : 4.2, 'max': 7.6},
'Blood Urea' :{'min' :	0, 'max': 40} ,
'BUN-Blood Urea Nitrogen':{'min' :	0, 'max': 18},
'Serum Uric acid'	:{'min' :3, 'max': 5.7},
'Serum Creatinine'	:{'min' :0.5, 'max': 1.4},
'Routine urine for albumin':	'Nil',
'24 hours albumin in the urine': 150,
'S.Cholestrol'	:{'min' :150, 'max': 250},
'S.HDL'	:{'min' :40, 'max': 70},
'S.LDL'	:{'min' :60, 'max': 160},
'S.VLDL':{'min' :3, 'max': 35},
'S.Triglycerides':{'min' :60, 'max': 150},
'Total Cholestrol/HDL':4.5,
'Serum Bilirubin'	:{'min' :0.2, 'max': 1},
'SGOT'	:{'min' :8, 'max': 40},
'SGPT'	:{'min' :5, 'max': 35},
'Alkaline Phosphatase'	:{'min' :60, 'max': 170},
'Gamma GT'	:{'min' :8, 'max': 37},
'Serum Mayo globin'	:{'min' :6, 'max': 90},
'PH Test':{'min':6.0,'max':7.0},
'R A Factor Test': Nil,
'S.Sodium':{'min':135,'max':145},
'S.Potassium':{'min':3.5,'max':5.5},
'S.Chlorides':{'min':96,'max':106},
'S.Magnesium':{'min':1.7,'max':2.2},
'S.Calcium':{'min':9,'max':10.6},
'S.Phosphorus':{'min':2.5,'max':4.8},
'S.Amylase':9.5,
'S.Acid Phosphates':{'min':1,'max':4},
'Prostatis fraction':{'min':0,'max':0.8},
'S.Proteins total':{'min':6,'max':8},
'Albumin':{'min':3.5,'max':5.6},
'Globulin':{'min':1.3,'max':3.2},
}

#Reference Values for Males
ref_male={
'Hemoglobin':{'min':14, 'max':18},
'Total WBC Count':{'min':4000, 'max':11000},
'Packed Cell Volume (PCV)' : {'min':42,'max':52},
'WBV (Leucocytes)': {'min':4000,'max':11000},	
'Neutrophils': {'min':60,'max':75},	
'Lymphocytes': {'min':20,'max':30},	
'Monocytes'	 : {'min':2,'max':8},
'Esoinophils': {'min':1,'max':6},
'Basophils' : {'min':0,'max':1},
'RBC Count':{'min_RBC':4.0,'max_RBC':6.4},
'MCV' :{'min':78,'max':94},
'MCH': {'min':27,'max':32},
'MCHC'	: {'min':32,'max':38},
'RDW' :{'min':11.8,'max':14.5},
'Platelets' : {'min':150000,'max':450000},
'Reticulocytes':{'min':0.5,'max':1.5}
'Color Index':{'min':0.85,'max':1.15}
'ESR':{'min':0,'max':15}
'Fasting Sugar':120,
'Post Prandial (PP) Blood Sugar'	: 120,
'Blood-Glucose Level Maximum Value'	: 160,
'Glycosylated Haemoglobin':{'min' : 4.2, 'max': 7.6},
'Blood Urea' :{'min' :	0, 'max': 40} ,
'BUN-Blood Urea Nitrogen':{'min' :	0, 'max': 18},
'Serum Uric acid'	:{'min' :3, 'max': 5.7},
'Serum Creatinine'	:{'min' :0.5, 'max': 1.4},
'Routine urine for albumin':	'Nil',
'24 hours albumin in the urine': 150,
'S.Cholestrol'	:{'min' :150, 'max': 250},
'S.HDL'	:{'min' :30, 'max': 60},
'S.LDL'	:{'min' :60, 'max': 160},
'S.VLDL':{'min' :3, 'max': 35},
'S.Triglycerides':{'min' :60, 'max': 150},
'Total Cholestrol/HDL':4.5,
'Serum Bilirubin'	:{'min' :0.2, 'max': 1},
'SGOT'	:{'min' :8, 'max': 40},
'SGPT'	:{'min' :5, 'max': 35},
'Alkaline Phosphatase'	:{'min' :60, 'max': 170},
'Gamma GT'	:{'min' :8, 'max': 37},
'Serum Mayo globin'	:{'min' :6, 'max': 90},
'PH Test':{'min':6.0,'max':7.0},
'R A Factor Test': Nil,
'S.Sodium':{'min':135,'max':145},
'S.Potassium':{'min':3.5,'max':5.5},
'S.Chlorides':{'min':96,'max':106},
'S.Magnesium':{'min':1.7,'max':2.2},
'S.Calcium':{'min':9,'max':10.6},
'S.Phosphorus':{'min':2.5,'max':4.8},
'S.Amylase':9.5,
'S.Acid Phosphates':{'min':1,'max':4},
'Prostatis fraction':{'min':0,'max':0.8},
'S.Proteins total':{'min':6,'max':8},
'Albumin':{'min':3.5,'max':5.6},
'Globulin':{'min':1.3,'max':3.2},
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