"""
pip install deepspeech==0.9.0

Alternatively 

pip install deepspeech-gpu==0.9.0
"""
import os
import librosa
import shutil

root = '/home/varad/speech_recog/'
model = root+'deepspeech-0.9.x-models/male_female_mix_0.9.3_50e_5.1L_extended.pbmm'
scorer = root+'deepspeech-0.9.x-models/deepspeech-0.9.3-models.scorer'


# model = 'deepspeech-0.9.x-models/deepspeech-0.9.2-models.pbmm'
# scorer = 'deepspeech-0.9.x-models/deepspeech-0.9.2-models.scorer'
# file_path = 'test_web1.wav'

# model = 'deepspeech-0.7.4-models/male_female_mix.pbmm'
# model = 'deepspeech-0.7.4-models/deepspeech-0.7.4-models.pbmm'
# scorer = 'deepspeech-0.7.4-models/deepspeech-0.7.4-models.scorer'


"""
Return specified audio file duration and sample rate
"""

def get_audio_info(file_name):

    
    return librosa.get_duration(filename=file_name), librosa.get_samplerate(file_name)

"""
Takes file path and converts it into text and returns the text 
"""
def custom_tts(file_path):
    
    
    fdur, fsr = get_audio_info(file_path)

    if fsr != 16000:
        print("Different SR:", file_path)
        file_name = file_path.split('.')[0]
        os.system("sox "+ file_path  + " -r 16000 " + file_name +"_16000" + '.wav' )
        shutil.move(file_name+'_16000.wav',file_path)
    if fdur > 10:
        print("Too Long:", file_path)


    command = " ".join(
        [
            "deepspeech",
            "--model",
            model,
            "--scorer",
            scorer,
            "--audio",
            file_path
        ]
    )

    os.system(command + '> output.txt')

    f = open("output.txt", "r")
    result = f.read()
    
    print(result)
    f.close()
    os.remove('output.txt')
    return result 
