from flask import Flask, request, jsonify
import MeCab

app = Flask(__name__)

@app.route("/parse", methods=["POST"])
def parse():
    text = request.json.get("text", "")
    mecab = MeCab.Tagger("-Owakati")
    parsed = mecab.parse(text)
    return jsonify({"parsed": parsed.strip()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
