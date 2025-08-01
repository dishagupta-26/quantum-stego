# Quantum Secure Communication via Steganography

## Quantum Stego

**Quantum Stego** is a secure steganography web application that hides secret messages inside images using **LSB (Least Significant Bit)** technique and encrypts them with a **quantum-simulated key** generated via Qiskit. Even if someone intercepts the image, the message remains unreadable without the key.

---

### Features

* **Quantum-Simulated Key Encryption** using Qiskit SamplerV2.
* **Image Steganography** (LSB embedding).
* XOR encryption of messages.
* Elegant frontend using **Tailwind CSS**.
* Full-stack Flask + HTML + JS integration.

---

### Tech Stack

| Layer      | Tools Used                     |
| ---------- | ------------------------------ |
| Frontend   | HTML, JavaScript, Tailwind CSS |
| Backend    | Python, Flask                  |
| Quantum    | Qiskit (`qiskit-aer`)          |
| Image Proc | OpenCV                         |

---

### How It Works

1. **User uploads an image** and enters a secret message.
2. A **quantum key** is generated (via simulated QKD).
3. The message is **XOR-encrypted** with the key.
4. The encrypted message is **embedded in the image** using LSB steganography.
5. The **stego image is returned**, and the **key is stored**.
6. On the receiver side, user uploads the stego image and provides the key ID.
7. The system **retrieves the key**, extracts the bits, decrypts the message, and shows it.

---

### Project Structure

```
quantum-stego/
├── backend/
│   ├── app.py               # Flask server
│   ├── stego_encoder.py     # LSB embedding
│   ├── stego_decoder.py     # LSB extraction
│   ├── quantum_key.py       # Qiskit key generation
│   ├── crypto_utils.py      # XOR encryption/decryption
│   ├── key_store.py         # Save/load key from disk
├── uploads/                 # Temporary image storage
├── encoded/                 # Output stego images
├── frontend/
│   ├── index.html
│   ├── send.html
│   ├── receive.html
│   ├── about.html
```

---

### Quantum Key Example

A sample quantum-simulated key (length: 64 bits):

```
1001010110110001011010000000110100011100100001110101010111101001
```

This key is used to XOR your message before embedding.

---

### What If the Image or Key is Intercepted?

* **Image only?** Harmless. It looks like a regular image.
* **Key only?** Still useless without the corresponding stego image.
* **Both?** That’s a threat. Avoid sharing the key over insecure channels. In future, we aim to integrate **public key cryptography** or **real QKD**.

---

### Setup Instructions

#### 1. Clone the Repo

```bash
git clone https://github.com/dishagupta-26/quantum-stego.git
cd quantum-stego/backend
```

#### 2. Create a Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> Make sure to also install Qiskit Aer:

```bash
pip install qiskit-aer
```

#### 4. Run the Flask App

```bash
python app.py
```

#### 5. Open the Frontend

Use Live Server or open `frontend/index.html` manually in browser.

---

