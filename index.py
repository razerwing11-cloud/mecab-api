from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse_text():
    data = request.get_json()
    fifteen_japanese = data.get("text", "")

    # --- Step 1: Gentle cleanup (remove stray punctuation, not real text)
    fifteen_japanese = re.sub(r'[「」『』【】（）［］〈〉《》｛｝…‥・]+', '', fifteen_japanese)
    fifteen_japanese = re.sub(r'\s{2,}', ' ', fifteen_japanese)
    fifteen_japanese = fifteen_japanese.strip()

    # --- Step 2: Send text to DeepL
    payload = {
        "auth_key": "7dd7bd5d-5555-4c91-9246-6940994a2103:fx",  # Replace with your actual key
        "text": fifteen_japanese,
        "target_lang": "EN"
    }

    headers = {
        "Content-Type": "application/json"
    }

    deepl_response = requests.post(
        "https://api-free.deepl.com/v2/translate",
        json=payload,
        headers=headers
    )

    # --- Step 3: Handle response
    if deepl_response.status_code == 200:
        result = deepl_response.json()
        translated_text = result["translations"][0]["text"]
        return jsonify({"translated_text": translated_text})
    else:
        return jsonify({"error": "Translation failed", "details": deepl_response.text}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
