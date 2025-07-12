from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from stego_encoder import encode_message
from stego_decoder import decode_message
import uuid
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ENCODED_FOLDER = 'encoded'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCODED_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return 'Flask server is running!'

@app.route('/encode', methods=['POST'])
def encode():
    try:
        import os
        import uuid
        from stego_encoder import encode_message
        from flask import send_file, request, jsonify

        print("[INFO] Received encode request")

        image = request.files['image']
        message = request.form['message']

        # Use absolute paths
        base_dir = os.path.dirname(__file__)
        uploads_dir = os.path.join(base_dir, 'uploads')
        encoded_dir = os.path.join(base_dir, 'encoded')

        os.makedirs(uploads_dir, exist_ok=True)
        os.makedirs(encoded_dir, exist_ok=True)

        filename = f"{uuid.uuid4().hex[:7]}.png"
        image_path = os.path.join(uploads_dir, filename)
        image.save(image_path)
        print(f"[INFO] Image saved to {image_path}")

        output_filename = f"encoded_{filename}"
        output_path = os.path.join(encoded_dir, output_filename)

        encode_message(image_path, message, output_path)
        print("[INFO] Returning file:", output_path)

        return send_file(output_path, mimetype='image/png')

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/decode', methods=['POST'])
def decode():
    if 'image' not in request.files:
        return "No image file provided", 400

    image = request.files['image']
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    print(f"[INFO] Decoding image: {image_path}")
    hidden_message = decode_message(image_path)
    print(f"[INFO] Decoded message: {hidden_message}")

    return hidden_message

if __name__ == '__main__':
    app.run(debug=True)
