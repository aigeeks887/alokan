from flask import Flask, requests, jsonify
from audio_to_speech import text_to_text_francais

app = Flask(__name__)

@app.routes("/", methods=['POST'])
def upload_audio():
    
    if "audio" not in requests.files:
        return jsonify({"error": "No audio file found"}), 400
     
    audio = requests.files['audio']


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)