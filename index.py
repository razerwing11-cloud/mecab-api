from flask import Flask, request, jsonify
import re
import requests
import os

app = Flask(__name__)

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_URL = "https://api-free.deepl.com/v2/translate"

def clean_text(text):
    # Remove Japanese scripts and punctuation but keep spacing
    text = re.sub(r"[\u3040-\u30FF\u3400-\u4DBF\u4E00-\u9FFF]+", "", text)
    text = re.sub(r"[・「」『』【】（）\[\]〈〉《》｛｝…‥]", "", text)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r"(\n\s*\n)+", "\n", text)
    return text.strip()

@app.route("/", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text", "")
    cleaned_text = clean_text(text)

    response = requests.post(
        DEEPL_URL,
        data={
            "auth_key": DEEPL_API_KEY,
            "text": cleaned_text,
            "target_lang": "EN"
        },
    )

    if response.status_code != 200:
        return jsonify({"error": response.text}), 500

    result = response.json()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
