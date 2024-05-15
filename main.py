import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, VideoTransformerBase
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

class TorchTransformer(VideoTransformerBase):
    def transform(self, frame):
        if st.checkbox("Activer la lampe torche"):
            frame.enable_torch()
        else:
            frame.disable_torch()
        return frame


def main():
    
    st.title("ALOKAN")
    st.title("Analyse audio en temps réel")

    # Boutons pour allumer et éteindre la lampe torche
    st.title("Parlez....")
    st.write("""<a href="whatsapp://send?phone=+22953537434">Cliquez ici pour ouvrir WhatsApp</a>""", unsafe_allow_html=True)
    st.write("""<script>/Test browser support
const SUPPORTS_MEDIA_DEVICES = 'mediaDevices' in navigator;

if (SUPPORTS_MEDIA_DEVICES) {
  //Get the environment camera (usually the second one)
  navigator.mediaDevices.enumerateDevices().then(devices => {
  
    const cameras = devices.filter((device) => device.kind === 'videoinput');

    if (cameras.length === 0) {
      throw 'No camera found on this device.';
    }
    const camera = cameras[cameras.length - 1];

    // Create stream and get video track
    navigator.mediaDevices.getUserMedia({
      video: {
        deviceId: camera.deviceId,
        facingMode: ['user', 'environment'],
        height: {ideal: 1080},
        width: {ideal: 1920}
      }
    }).then(stream => {
      const track = stream.getVideoTracks()[0];

      //Create image capture object and get camera capabilities
      const imageCapture = new ImageCapture(track)
      const photoCapabilities = imageCapture.getPhotoCapabilities().then(() => {

        //todo: check if camera has a torch

        //let there be light!
        const btn = document.querySelector('.switch');
        btn.addEventListener('click', function(){
          track.applyConstraints({
            advanced: [{torch: true}]
          });
        });
      });
    });
  });
  
  //The light will be on as long the track exists
  
  
}</script> <button class="switch">On / Off</button>""", unsafe_allow_html=True)
    time.sleep(2.0)
    # Paramètres
    # webrtc_ctx = webrtc_streamer(
    #     key="torch",
    #     rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    #     media_stream_constraints={"video": False, "audio": True},
    #     video_transformer_factory=TorchTransformer,
    #     async_transform=True,
    # )


    time.sleep(15.0)
    st.title("Votre Commande: Allumer la lampe torche")

    # Configuration du client WebRTC
    # client_settings = ClientSettings(
    #     rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    #     media_stream_constraints={"video": False, "audio": True},
    # )
    
    # Capture audio en temps réel
    # try:
    #     webrtc_ctx = webrtc_streamer(
    #         key="audio",
    #         mode="audio",
    #         audio_processor_factory=lambda: MyAudioProcessor(trigger_word),
    #         client_settings=client_settings,
    #     )
    # except KeyboardInterrupt:
    #     pass

if __name__ == "__main__":
    main()
