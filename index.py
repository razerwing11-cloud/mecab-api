from flask import Flask, request, jsonify
import MeCab
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "MeCab API is running!"})

@app.route("/parse", methods=["POST"])
def parse_text():
    try:
        data = request.get_json()
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Initialize MeCab
        tagger = MeCab.Tagger("-Ochasen")
        parsed = tagger.parse(text)

        return jsonify({"parsed_text": parsed})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Render provides a dynamic PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
