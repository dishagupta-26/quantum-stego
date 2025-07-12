from flask import Flask, request, send_file
from flask_cors import CORS
from stego_encoder import encode_message
from stego_decoder import decode_message
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
    if 'image' not in request.files or 'message' not in request.form:
        print("[ERROR] Missing image or message")
        return {'error': 'Missing data'}, 400

    image = request.files['image']
    message = request.form['message']

    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)
    print(f"[INFO] Image saved to {image_path}")

    output_path = os.path.join(ENCODED_FOLDER, 'encoded_' + image.filename)
    try:
        encode_message(image_path, message + 'þ', output_path)
        print(f"[INFO] Encoded image saved to {output_path}")
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        print("[ERROR]", str(e))
        return {'error': str(e)}, 500

@app.route('/decode', methods=['POST'])
def decode():
    if 'image' not in request.files:
        return {'error': 'Missing image'}, 400

    image = request.files['image']
    image_path = os.path.join(UPLOAD_FOLDER, 'uploaded_' + image.filename)
    image.save(image_path)

    try:
        message = decode_message(image_path)
        return {'message': message}
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
