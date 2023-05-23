from flask import Flask, request, jsonify
import requests, uuid, json
import os

app = Flask(__name__)

key = os.environ.get('KEY', '')
endpoint = os.environ.get('ENDPOINT', '')
location = os.environ.get('LOCATION', '')

path = '/translate'
constructed_url = endpoint + path

params = {
    'api-version': '3.0',
    'from': 'en'
}

headers = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json'
}

@app.route('/translate', methods=['POST'])
def translate():
    print("Received translation request:")
    data = request.json
    text = data.get('text')
    target_language = data.get('target_language')
    print(f"Text: {text}, Target language: {target_language}")
    if not text:
        return jsonify({'error': 'Missing input text'}), 400
    if not target_language:
        return jsonify({'error': 'Missing target language'}), 400
    body = [{'text': text}]
    params['to'] = target_language
    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    if response.status_code == 200:
        result = response.json()
        print(f"Translation successful: {result[0]['translations'][0]['text']}")
        return jsonify({'translations': result[0]['translations']}), 200
    else:
        print("Translation failed. Response:")
        print(json.dumps(response.json(), sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
        return jsonify({'error': 'Translation failed'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)




