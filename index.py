from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse_text():
    try:
        # Try to get JSON first
        data = request.get_json(silent=True)

        if data and "Text from image" in data:
            text_from_image = data["Text from image"]
        else:
            # If not JSON, get raw text
            text_from_image = request.data.decode('utf-8')

        if not text_from_image.strip():
            return jsonify({"error": "No text received from Shortcut"}), 400

        # Light cleanup
        cleaned_text = re.sub(r'[「」『』【】（）［］〈〉《》｛｝…‥・]+', '', text_from_image)
        cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text).strip()

        return jsonify({"parsed_text": cleaned_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
