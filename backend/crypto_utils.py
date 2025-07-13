# crypto_utils.py
def xor_encrypt(message: str, key: str) -> str:
    message_bits = ''.join(format(ord(c), '08b') for c in message)
    encrypted_bits = ''.join(str(int(b) ^ int(k)) for b, k in zip(message_bits, key))
    return encrypted_bits

def xor_decrypt(encrypted_bits: str, key: str) -> str:
    decrypted_bits = ''.join(str(int(b) ^ int(k)) for b, k in zip(encrypted_bits, key))
    chars = [chr(int(decrypted_bits[i:i+8], 2)) for i in range(0, len(decrypted_bits), 8)]
    return ''.join(chars)
