import streamlit as st
from streamlit_webrtc import  AudioProcessorBase 
import streamlit_webrtc as sw
import speech_recognition as sr
import numpy as np
import tempfile
import time

# Définition d'un processus audio pour traiter les données audio en temps réel
class MyAudioProcessor(AudioProcessorBase):
    def __init__(self, trigger_word):
        super().__init__()
        self.trigger_word = trigger_word
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.audio_buffer = []

    def recv(self, frame_data):
        try:
            audio = sr.AudioData(frame_data, self.sample_rate, 2)
            text = self.recognizer.recognize_google(audio)
            if self.trigger_word.lower() in text.lower():
                st.success(f"Mot déclencheur '{self.trigger_word}' détecté !")
                self.audio_buffer.append(frame_data)
                self.save_audio()
                # Attente de silence pendant 2 secondes
                self.wait_for_silence(2)
                raise KeyboardInterrupt
            else:
                self.audio_buffer.append(frame_data)
        except sr.UnknownValueError:
            st.write("Impossible de reconnaître l'audio.")
        except sr.RequestError:
            st.error("Erreur lors de la requête vers le service de reconnaissance vocale.")
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        return frame_data

    def save_audio(self):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            filename = f.name
            for audio_data in self.audio_buffer:
                f.write(audio_data)
        st.success(f"Audio enregistré: {filename}")

    def wait_for_silence(self, timeout):
        start_time = time.time()
        while time.time() - start_time < timeout:
            audio_data = self.microphone.listen(timeout=1)
            try:
                self.recognizer.recognize_google(audio_data)
                st.write("Silence interrompu, continue l'enregistrement...")
                start_time = time.time()  # Réinitialise le compteur de temps si du son est détecté
            except sr.UnknownValueError:
                pass  # Silence détecté, continuer l'attente
            except sr.RequestError:
                st.error("Erreur lors de la requête vers le service de reconnaissance vocale.")

def main():
    st.title("Analyse audio en temps réel avec détection de mot déclencheur")
    
    # Paramètres
    trigger_word = st.text_input("Entrez le mot déclencheur")


    # Capture audio en temps réel
    try:
        webrtc_ctx = sw.webrtc_streamer(
        key="audio",
        audio_processor_factory=lambda: MyAudioProcessor(trigger_word),
        # rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        # media_stream_constraints={"audio": True},
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={
            "video": False,  # Pas de vidéo, seulement de l'audio
            "audio": True,   # Autoriser l'audio
            # Ajouter des contraintes spécifiques pour une meilleure compatibilité avec les mobiles
            "audioOptions": {
                "echoCancellation": True,
                "autoGainControl": False,
                "noiseSuppression": True,
                "channelCount": 1,  # Utiliser un seul canal audio
            },
        },
    )
        
        if webrtc_ctx.audio_processor:
                print("OK")
                webrtc_ctx.audio_processor.recv()

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
