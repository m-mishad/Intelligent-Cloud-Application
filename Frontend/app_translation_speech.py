import os
from flask import Flask, request, render_template, jsonify
import requests
import json
import base64
import tempfile

app = Flask(__name__)

# URL of the prediction server
PREDICTION_URL = os.environ.get('PREDICTION', '')

# URL of the translation server
TRANSLATION_URL = os.environ.get('TRANSLATION', '')

# URL of the text-to-speech server
TTS_URL = os.environ.get('TTS', '')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            # Get image from frontend form
            image = request.files['image']

            # Show loader
            loader_display = 'block'

            # Prepare data for request to prediction server
            data = {'image': image}

            # Send request to prediction server
            prediction_response = requests.post(PREDICTION_URL, files=data)
            prediction_response.raise_for_status()
            digit = prediction_response.json()['digit']

            # Get target language from user input
            language = request.form.get('language', 'fr')

            # Prepare data for translation request
            text = f'The predicted digit is {digit}.'
            data = {'text': text, 'target_language': language}

            # Send translation request to translation server
            response = requests.post(TRANSLATION_URL, json=data)
            response.raise_for_status()
            translations = response.json()['translations']
            translation_text = ' '.join([t['text'] for t in translations])

            # Prepare data for text-to-speech request
            data = {'text': translation_text, 'language': language}

            # Send text-to-speech request
            response = requests.post(TTS_URL, json=data)

            # Create a temporary file to write the audio bytes to
            with tempfile.NamedTemporaryFile(delete=False) as f:
                f.write(response.content)
                file_name = f.name

            # Read the audio file and convert it to base64 encoding
            with open(file_name, 'rb') as f:
                audio_bytes = f.read()

            audio_base64 = base64.b64encode(audio_bytes).decode()

            # Remove the temporary file
            os.unlink(file_name)

            # Return audio file to the user's browser
            return render_template('home.html', audio_base64=audio_base64, digit=digit, translation_text=translation_text)
           # return render_template('home.html', audio_base64=audio_base64)
        except Exception as e:
            # Render error message in template
            return render_template('home.html', error=str(e), loader_display='none')

    else:
        # Render initial form in template
        return render_template('home.html', loader_display='none')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

