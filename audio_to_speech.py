import google.generativeai as genai
import getpass
from transformers import pipeline
from speechbrain.inference.ASR import EncoderASR
# Run this is your python version is not 3.8 THIS IS VERY IMPORTANT
#virtualenv -p python3.8 venv
# git clone https://github.com/edaiofficial/mmtafrica.git

import torch
from mmtafrica.mmtafrica import load_params, translate
from huggingface_hub import hf_hub_download


language_map = {'English':'en','Swahili':'sw','Fon':'fon','Igbo':'ig',
                'Kinyarwanda':'rw','Xhosa':'xh','Yoruba':'yo','French':'fr'}

# Load parameters and model from checkpoint
checkpoint = hf_hub_download(repo_id="chrisjay/mmtafrica", filename="mmt_translation.pt")
device = 'gpu' if torch.cuda.is_available() else 'cpu'
params = load_params({'checkpoint':checkpoint,'device':device})

# Create a speech recognition pipeline using a pre-trained model
#pipe = pipeline("automatic-speech-recognition", model=" ")

# To transcribe an audio file, simply pass the file path to the pipeline
#audio_path = "/content/eli2.aac"  # Update this path with your actual audio file path
# transcription = pipe(audio_path)

# print("Transcription:", transcription['text'])

def audio_to_text_fon(audio_path):
    asr_model = EncoderASR.from_hparams(source="speechbrain/asr-wav2vec2-dvoice-fongbe", savedir="pretrained_models/asr-wav2vec2-dvoice-fongbe")
    text = asr_model.transcribe_file(audio_path)
    return text



def get_translation(source_language,target_language,source_sentence=None):
    '''
    This takes a sentence and gets the translation.
    '''

    source_language_ = language_map[source_language]
    target_language_ = language_map[target_language]


    try:
        pred = translate(params,source_sentence,source_lang=source_language_,target_lang=target_language_)
        if pred=='':
            return f"Could not find translation"
        else:
            return pred
    except Exception as error:
        return f"Issue with translation: \n {error}"

# Example usage, adjust to your needs. Check the laguage_map dict to select your language
def text_to_text_francais(audio_path):
    source_language = 'Fon'
    target_language = 'French'
    source_sentence = audio_to_text_fon(audio_path)
    translation = get_translation(source_language, target_language, source_sentence)
    return translation
    #print(translation)







