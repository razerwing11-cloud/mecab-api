from flask import Flask, request, jsonify
from fugashi import Tagger

app = Flask(__name__)
tagger = Tagger()

@app.route("/")
def home():
    return jsonify({"message": "MeCab/Fugashi API is running!"})

@app.route("/parse", methods=["POST"])
def parse():
    try:
        data = request.get_json()
        text = data.get("text", "")
        if not text:
            return jsonify({"error": "No text provided"}), 400

        words = [{"surface": w.surface, "feature": w.feature} for w in tagger(text)]
        return jsonify({"parsed": words})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
