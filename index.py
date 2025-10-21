from flask import Flask, request, jsonify
import MeCab

app = Flask(__name__)

@app.route('/')
def home():
    return "MeCab API is running!"

@app.route('/parse', methods=['POST'])
def parse():
    text = request.json.get('text', '')
    tagger = MeCab.Tagger()
    parsed = tagger.parse(text)
    return jsonify({"parsed": parsed})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
