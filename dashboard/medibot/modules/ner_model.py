
# from dashboard.views import prescription
import spacy 
from spacy.gold import GoldParse 
# from spacy.language import EntityRecognizer 
from spacy.pipeline import EntityRecognizer
from medacy.model.model import Model
import os 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_model(sentences):
    # for sentence in sentences:
        nlp = spacy.load(BASE_DIR+'/NER_model/model_full_batch_15000_droupout_mix') 
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


def run_medacy(sentences):      
    model = Model.load_external('medacy_model_clinical_notes')
    annotation = model.predict(sentences)
    med_list = []
    for i in annotation:
        if i.tag == "Drug":
            med_list.append(i.text)
        else :
            temp = med_list[-1]
            temp = temp + ' ' + i.text 
            med_list[-1] = temp
    return med_list