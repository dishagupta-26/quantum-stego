from flask import Flask, request, send_file
from stego_encoder import encode_message
from stego_decoder import decode_message
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ENCODED_FOLDER = 'encoded'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCODED_FOLDER, exist_ok=True)

@app.route('/encode', methods=['POST'])
def encode():
    if 'image' not in request.files or 'message' not in request.form:
        return {'error': 'Missing data'}, 400

    image = request.files['image']
    message = request.form['message']

    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    output_path = os.path.join(ENCODED_FOLDER, 'encoded_' + image.filename)
    encode_message(image_path, message, output_path)

    return send_file(output_path, as_attachment=True)

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
