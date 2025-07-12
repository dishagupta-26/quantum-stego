from stego_encoder import encode_message
from stego_decoder import decode_message

# 1. Encode
print("Encoding message...")
encode_message("test.png", "Hello Disha!", "encoded_test.png")

# 2. Decode
print("Decoding message...")
msg = decode_message("encoded_test.png")
print(f"Decoded message: {msg}")
