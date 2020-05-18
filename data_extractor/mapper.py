#Input from report
final_report={'Date': '01/02/2020', 'Name': 'Chavaa', 'Gender': 'Male', 'Age': '12', 'TestNameResultsUnitsBio.Ref.Interval\rCOMPLETE BLOOD COUNT (CBC)\r(Electrical Impedance & VCS,Photometry )': '', 'Hemoglobin': '14.40', 'Packed Cell Volume (PCV)': '43.80', 'RBC Count': '5.27', 'MCV': '83.00', 'MCH': '27.20', 'MCHC': '32.80', 'Red Cell Distribution Width (RDW)': '14.50', 'Total Leukocyte Count (TLC)': '11.00', 'Differential Leucocyte Count (DLC)': '', 'Segmented Neutrophils': '66.40', 'Lymphocytes': '2.72', 'Monocytes': '0.54', 'Eosinophils': '0.34', 'Basophils': '0.10', 'Absolute Leucocyte Count': '', 'Neutrophils': '7.30', 'Platelet Count': '290.0', 'COMPLETE BLOOD COUNT (CBC)': ''}

#Reference Values
ref_male={'Hemoglobin':{'min_Haemoglobin':14, 'max_Haemoglobin':18},'rbc':{'min_RBC':4.5,'max_RBC':6.4}}
min_Haemoglobin=14
max_Haemoglobin=18
min_PCV=42
max_PCV=52
min_MCV =78
max_MCV = 94

#Final reference for comparision 
ref={}
# ref=ref_male

def ref_gender():
    if final_report['Gender'] == 'Male':
        print ('Male')
        ref=ref_male
    
    elif final_report['Gender'] == 'Female':
        print ('Female')
        ref['Gender']=123
    
    else:
        print ("Error")

 
ref_gender()

print(ref)

#Ignore below this
def param_cmp():
    print ((ref_male["rbc"]))
# print(type(ref_male["Hemoglobin"]))
    if (type(ref_male["Hemoglobin"]) is dict):
        print ("true")

    if (type(ref_male["rbc"]) is float):
        print ("Float")

