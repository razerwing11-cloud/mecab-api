from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse_text():
    data = request.get_json()
    text_from_image = data.get("text from image", "")

    # --- Step 1: Light cleanup (remove stray punctuation and extra spaces)
    text_from_image = re.sub(r'[「」『』【】（）［］〈〉《》｛｝…‥・]+', '', text_from_image)
    text_from_image = re.sub(r'\s{2,}', ' ', text_from_image)
    text_from_image = text_from_image.strip()

    # --- Step 2: Send text to MeCab (morphological parsing)
    payload = {
        "text": text_from_image
    }

    headers = {
        "Content-Type": "application/json"
    }

    mecab_response = requests.post(
        "https://api.mecab.com/v1/parse",  # Replace with your actual MeCab endpoint if different
        json=payload,
        headers=headers
    )

    # --- Step 3: Handle response
    if mecab_response.status_code == 200:
        result = mecab_response.json()
        return jsonify({"parsed_text": result})
    else:
        return jsonify({"error": "Parsing failed", "details": mecab_response.text}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
