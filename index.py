from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse_text():
    try:
        data = request.get_json(force=True)

        # Handle both plain string and nested JSON input
        raw_text = data.get("Text from image", "")
        if isinstance(raw_text, dict):
            text_from_image = raw_text.get("text", "")
        else:
            text_from_image = raw_text

        if not text_from_image.strip():
            return jsonify({"error": "No text received from Shortcut"}), 400

        # Light cleanup (non-destructive)
        cleaned_text = re.sub(r'[「」『』【】（）［］〈〉《》｛｝…‥・]+', '', text_from_image)
        cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text).strip()

        return jsonify({"parsed_text": cleaned_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
