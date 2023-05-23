from flask import Flask, request, jsonify
import boto3
import json
import os

app = Flask(__name__)

access_key = os.environ.get('AWS_ACCESS_KEY_ID', '')
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
region_name = os.environ.get('AWS_DEFAULT_REGION', '')

translate = boto3.client('translate', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region_name)

@app.route('/translate', methods=['POST'])
def translate_text():
    print("Received translation request:")
    data = request.json
    text = data.get('text')
    target_language = data.get('target_language')
    print(f"Text: {text}, Target language: {target_language}")
    
    if not text:
        return jsonify({'error': 'Missing input text'}), 400
    if not target_language:
        return jsonify({'error': 'Missing target language'}), 400
    
    try:
        response = translate.translate_text(
            Text=text,
            SourceLanguageCode='en',
            TargetLanguageCode=target_language
        )
        
        if 'TranslatedText' in response:
            translated_text = response['TranslatedText']
            print(f"Translation successful: {translated_text}")
            return jsonify({'translations': [{'text': translated_text}]}), 200
        else:
            print("Translation failed. Response:")
            print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
            return jsonify({'error': 'Translation failed'}), 500
    except Exception as e:
        print(f"Translation failed. Exception: {str(e)}")
        return jsonify({'error': 'Translation failed'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
