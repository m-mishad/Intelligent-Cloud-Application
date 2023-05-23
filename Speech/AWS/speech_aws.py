from flask import Flask, request, send_file, jsonify
import boto3
from io import BytesIO
import wave
import os

app = Flask(__name__)

access_key = os.environ.get('ACCESS_KEY', '')
secret_key = os.environ.get('SECRET_KEY', '')
region_name = os.environ.get('REGION_NAME', '')

polly = boto3.client('polly', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region_name)

@app.route('/tts', methods=['POST'])
def tts():
    print("Received text-to-speech request:")
    data = request.json
    text = data.get('text')
    print(f"Input Text: {text}")
    
    if not text:
        return jsonify({'error': 'Missing input text'}), 400
    
    try:
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat='pcm',
            VoiceId='Joanna'
        )
        
        if 'AudioStream' in response:
            audio_stream = response['AudioStream'].read()
            
            # Convert PCM audio stream to WAV format
            wav_file = BytesIO()
            with wave.open(wav_file, 'wb') as wave_obj:
                wave_obj.setnchannels(1)
                wave_obj.setsampwidth(2)
                wave_obj.setframerate(16000)
                wave_obj.writeframes(audio_stream)
            
            wav_file.seek(0)
            
            # Return the WAV audio file
            return send_file(wav_file, mimetype='audio/wav')
        else:
            print("Text-to-speech synthesis failed. Response:")
            print(response)
            return jsonify({'error': 'Text-to-speech synthesis failed'}), 500
    except Exception as e:
        print(f"Text-to-speech synthesis failed. Exception: {str(e)}")
        return jsonify({'error': 'Text-to-speech synthesis failed'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)

