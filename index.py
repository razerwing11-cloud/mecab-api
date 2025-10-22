from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse_text():
    try:
        data = request.get_json(force=True)
        text_from_image = data.get("Text from image", "")

        if not text_from_image.strip():
            return jsonify({"error": "No text received from Shortcut"}), 400

        # Convert line-separated text into single line for better parsing
        text_from_image = re.sub(r'\n+', ' ', text_from_image).strip()

        # Light cleanup (non-destructive)
        cleaned_text = re.sub(r'[「」『』【】（）［］〈〉《》｛｝…‥・]+', '', text_from_image)
        cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text).strip()

        return jsonify({"parsed_text": cleaned_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
