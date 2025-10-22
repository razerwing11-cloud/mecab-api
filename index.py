from flask import Flask, request, jsonify
import re
import requests
import os

app = Flask(__name__)

DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY")
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"

# --- Text cleanup before sending to DeepL ---
def clean_text(text):
    # 1️⃣ Remove Japanese scripts (Hiragana, Katakana, Kanji)
    text = re.sub(r"[\u3040-\u30FF\u3400-\u4DBF\u4E00-\u9FFF]+", "", text)
    
    # 2️⃣ Remove Japanese punctuation and symbols
    text = re.sub(r"[・「」『』【】（）\[\]〈〉《》｛｝…‥ー]", "", text)
    
    # 3️⃣ Collapse duplicate spaces but keep newlines for formatting
    text = re.sub(r" {2,}", " ", text)
    
    # 4️⃣ Remove extra blank lines
    text = re.sub(r"(\n\s*\n)+", "\n", text)
    
    return text.strip()

# --- DeepL translation function ---
def translate_text(text, target_lang="EN"):
    cleaned = clean_text(text)
    
    data = {
        "auth_key": DEEPL_API_KEY,
        "text": cleaned,
        "target_lang": target_lang,
    }
    
    response = requests.post(DEEPL_API_URL, data=data)
    result = response.json()
    
    return result.get("translations", [{}])[0].get("text", "")

# --- Flask endpoint ---
@app.route("/translate", methods=["POST"])
def translate():
    content = request.json
    text = content.get("text", "")
    lang = content.get("target_lang", "EN")
    
    translated = translate_text(text, lang)
    
    return jsonify({
        "original": text,
        "translated": translated
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
