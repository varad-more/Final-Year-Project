#Input from report
final_report={'Date': '01/02/2020',
'Name': 'Chavaa', 
'Gender': 'Female', 
'Age': '12',
'Fasting Sugar':'120', 
'Hemoglobin': '14.40', 
'Packed Cell Volume (PCV)': '43.80', 
'MCV': '83.00',
'RBC Count': '5.27',
'MCH': '27.20',
'MCHC': '32.80',
'Red Cell Distribution Width (RDW)': '14.50', 
'Total Leukocyte Count (TLC)': '11.00', 
'Differential Leucocyte Count (DLC)': '', 
'Segmented Neutrophils': '66.40', 
'Lymphocytes': '2.72', 
'Monocytes': '0.54', 
'Eosinophils': '0.34', 
'Basophils': '0.10', 
'Absolute Leucocyte Count': '', 
'Neutrophils': '7.30', 
'Platelet Count': '290.0'}


#Reference Values for Males
ref_male={'Fasting Sugar':120,
'Hemoglobin':{'min':14, 'max':18},
'RBC Count':{'min_RBC':4.5,'max_RBC':6.4},
'Packed Cell Volume (PCV)' : {'min':42,'max':52},
'MCV' :{'min':78,'max':94},
'MCH': {'min':27,'max':32},
'MCHC'	: {'min':32,'max':38},
'WBV (Leucocytes)': {'min':4000,'max':11000},	
'Neutrophils': {'min':60,'max':75},	
'Lymphocytes': {'min':20,'max':30},	
'Monocytes'	 : {'min':2,'max':8},
'Esoinophils': {'min':1,'max':6},
'Basophils' : {'min':0,'max':1},
'Platelets' : {'min':15000,'max':450000},
'Post Prandial (PP) Blood Sugar'	: 120,
'Blood-Glucose Level Maximum Value'	: 160,
'Glycosylated Haemoglobin':{'min' :	4.2, 'max': 7.6},
'Blood Urea' :{'min' :	0, 'max': 40} ,
'BUN-Blood Urea Nitrogen':{'min' :	0, 'max': 18},
'Serum Uric acid'	:{'min' :	3, 'max': 5.7},
'Serum Creatinine'	:{'min' :	0.5, 'max': 1.4},
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
    # print ((ref_male["rbc"]))
# print(type(ref_male["Hemoglobin"]))    
    for i in final_report:
        try :
            if (type(ref_male[i]) is dict):
                # print ("Dict#######################")
            
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

            elif (type(ref_male[i]) is float) | (type(ref_male[i]) is int)  :
                # print ("Float~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            
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
