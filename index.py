from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse_text():
    try:
        data = request.get_json(force=True)
        text_from_image = data.get("Text from image", "")

        if not text_from_image.strip():
            return jsonify({"error": "No text received from Shortcut"}), 400

        # Return as JSON string so Shortcut sees it
        return jsonify({"parsed_text": json.dumps({"text": text_from_image}, ensure_ascii=False)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
