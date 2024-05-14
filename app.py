from flask import Flask, requests, jsonify
from audio_to_speech import audio_to_text_fon, get_translation, text_to_text_francais

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

audio = None

@app.route('/', methods=["POST"])
def upload_audio():
    if "audio" not in requests.files:
        return jsonify({"message": "Aucun audio trouvé! "})
    
    audio = requests.files["audio"]
    return 'Hello, World!'

def translate():
    translated = text_to_text_francais(audio)
    
    response = {
        "translated": translated
    }
    return response

if __name__ == '__main__':
    app.run(debug=True)