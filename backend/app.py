from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS
from stego_encoder import encode_message
from stego_decoder import decode_message
import uuid, os, traceback
import cv2
from crypto_utils import xor_encrypt, xor_decrypt
from quantum_key import simulate_qkd_key
from key_store import save_key, load_key

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ENCODED_FOLDER = 'encoded'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCODED_FOLDER, exist_ok=True)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route('/')
def home():
    return 'Flask server is running!'

@app.route('/encode', methods=['POST'])
def encode():
    try:
        print("[INFO] Received encode request")

        image = request.files['image']
        message = request.form['message']

        base_dir = os.path.abspath(os.path.dirname(__file__))
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

        # Quantum key generation
        qkd_key = simulate_qkd_key(length=1024)
        print(f"[QUANTUM] QKD key generated: {qkd_key[:32]}...")

        # Encrypt the message
        encrypted_bits = xor_encrypt(message, qkd_key)
        print(f"[ENCRYPT] Encrypted {len(encrypted_bits)} bits.")

        # Embed encrypted bits into image
        encode_message(image_path, encrypted_bits, output_path)
        print(f"[ENCODER] Encoded image saved to {output_path}")
        print(f"[INFO] Stego image saved to: {image_path}")

        # Save quantum key with ID based on filename
        key_id = filename.split('.')[0]
        save_key(key_id, qkd_key)

        # Return both file and key ID
        return jsonify({
            "image": output_filename,
            "key_id": key_id,
            "quantum_key": qkd_key  # TEMP: for confirmation
})

    except Exception as e:
        print("[ERROR]", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/decode', methods=['POST'])
def decode():
    try:
        print("[INFO] Received decode request")

        image = request.files['image']
        key_id = request.form['key_id']

        base_dir = os.path.dirname(__file__)
        uploads_dir = os.path.join(base_dir, 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)

        original_filename = image.filename
        ext = os.path.splitext(original_filename)[1] or ".png"
        filename = f"decode_{uuid.uuid4().hex[:7]}{ext}"
        image_path = os.path.join(uploads_dir, filename)
        image.save(image_path)
        print(f"[INFO] Image saved at: {image_path}")
        print(f"[DEBUG] File exists? {os.path.exists(image_path)}")


        # ✅ Now call the actual decoding function
        encrypted_bits = decode_message(image_path)

        qkd_key = load_key(key_id)
        message = xor_decrypt(encrypted_bits, qkd_key)

        return message

    except Exception as e:
        print("[ERROR]", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/encoded/<filename>')
def serve_encoded_image(filename):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    encoded_dir = os.path.join(base_dir, 'encoded')
    return send_from_directory(encoded_dir, filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


