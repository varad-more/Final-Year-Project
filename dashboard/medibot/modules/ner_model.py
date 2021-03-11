
# from dashboard.views import prescription
import spacy 
from spacy.gold import GoldParse 
from spacy.language import EntityRecognizer 
  
nlp = spacy.load('/home/varad/Downloads/Spacy_medical_models/model_full_batch_15000_droupout_mix-20201209T052531Z-001/model_full_batch_15000_droupout_mix') 
    
def run_model(sentences):
    # for sentence in sentences:
        doc = nlp(sentences) 
    
        symptom =''
        medicine = ''
        dosage = ''
    
        for ent in doc.ents: 
            print(ent.text, ent.start_char, ent.end_char, ent.label_) 
    
    
    
            if ent.label_ == 'symptom':
                symptom+=', ' + ent.text
                # print ('inside symp', ent.text)
    
            if ent.label_ == 'medicine':
                medicine+=', ' + ent.text
    
            if ent.label_ == 'dosage':
                dosage+=', ' + ent.text
    
        content = { 'symptom': symptom,
        'medicine': medicine,
        'dosage': dosage
        }
    
    
        print (content)
        return content
    