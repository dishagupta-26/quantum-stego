import cv2

def decode_message(image_path):
    image = cv2.imread(image_path)
    binary_data = ""

    for row in image:
        for pixel in row:
            binary_data += str(pixel[0] & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ""
    for byte in all_bytes:
        char = chr(int(byte, 2))
        if message.endswith('þ'):
            break
        message += char

    return message.rstrip('þ')  # Remove end marker
