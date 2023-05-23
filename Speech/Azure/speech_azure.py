from flask import Flask, request, send_file, jsonify
import requests, uuid, json
import os
from io import BytesIO
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, audio

app = Flask(__name__)

speech_key = os.environ.get('SPEECH_KEY', '')
speech_location = os.environ.get('SPEECH_LOCATION', '')

def get_speech_synthesizer(speech_key, speech_location):
    speech_config = SpeechConfig(subscription=speech_key, region=speech_location)
    audio_config = audio.AudioOutputConfig(use_default_speaker=True)
    return SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

@app.route('/tts', methods=['POST'])
def tts():
    print("Received text-to-speech request:")
    data = request.json
    text = data.get('text')
    print(f"Input Text: {text}")
    if not text:
        return jsonify({'error': 'Missing input text'}), 400

    speech_config = SpeechConfig(subscription=speech_key, region=speech_location)
    synthesizer = SpeechSynthesizer(speech_config=speech_config)

    # Synthesize the audio
    result = synthesizer.speak_text_async(text).get()

    # Convert audio stream to AudioDataStream
    stream = AudioDataStream(result)

    # Save audio to a WAV file
    file_name = "output.wav"
    stream.save_to_wav_file(file_name)

    # Return the audio file
    return send_file(file_name, mimetype='audio/wav')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
