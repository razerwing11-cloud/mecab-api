from flask import Flask, request, jsonify
import MeCab
import unidic_lite  # lightweight dictionary

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ MeCab API is running successfully!"

@app.route('/parse', methods=['POST'])
def parse():
    try:
        data = request.get_json()
        text = data.get("text", "")
        if not text:
            return jsonify({"error": "No text provided"}), 400

        tagger = MeCab.Tagger()
        parsed = tagger.parse(text)
        return jsonify({"parsed": parsed})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
