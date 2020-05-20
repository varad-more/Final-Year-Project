import csv

f=open('names.csv','r')
reader=csv.reader(f)
ref_male={}
for row in reader:
	ref_male[row[0]]={row[1]}
print(ref_male)


