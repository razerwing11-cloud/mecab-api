from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse_text():
    try:
        # ✅ Accept both JSON and form data (Shortcuts uses form)
        if request.is_json:
            data = request.get_json(force=True)
        else:
            data = request.form.to_dict()

        text_from_image = data.get("Text from image", "")

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
