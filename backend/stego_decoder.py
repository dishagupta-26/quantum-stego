import cv2

def decode_message(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Image not found or invalid format.")

    binary_data = ""

    # Step 1: Extract all LSBs from all pixels and channels
    for row in image:
        for pixel in row:
            for channel in range(3):  # B, G, R
                binary_data += str(pixel[channel] & 1)

    # Step 2: Convert binary to characters (every 8 bits = 1 char)
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]

    message = ""
    for byte in all_bytes:
        try:
            char = chr(int(byte, 2))
            message += char
            if message.endswith("~END~"):  # ✅ end marker check
                break
        except ValueError:
            # In case of invalid binary strings
            break

    return message.replace("~END~", "")
