import subprocess
import os


files = os.listdir("/content/hindi_male_english_org/english/wav")

for file in files:
	print (file)
	os.system("sox /content/hindi_male_english_org/english/wav/"+ file  + " -r 16000 /content/hindi_male_english/english/wav/" + file )


files = os.listdir("/content/hindi_female_english_org/english/wav")

for file in files:
	print (file)
	os.system("sox /content/hindi_female_english_org/english/wav/"+ file  + " -r 16000 /content/hindi_female_english/english/wav/" + file )
