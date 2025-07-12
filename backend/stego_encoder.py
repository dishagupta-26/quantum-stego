import cv2
import numpy as np
import os

def encode_message(image_path, message, output_path='encoded.png'):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Image not found or invalid format.")

    # Append an end marker
    message += "~END~"
    binary_msg = ''.join(format(ord(char), '08b') for char in message)

    index = 0
    total_bits = len(binary_msg)

    # Go through every pixel and every channel (BGR)
    for row in image:
        for pixel in row:
            for channel in range(3):  # B, G, R channels
                if index < total_bits:
                    pixel[channel] = (int(pixel[channel]) & 0xFE) | int(binary_msg[index])
                    index += 1
                else:
                    break
                
    print("[ENCODE] Writing encoded image to:", output_path)
    success = cv2.imwrite(output_path, image)
    print("[ENCODE] Write success:", success)

    if index < total_bits:
        raise ValueError("Message too long for image capacity!")

    cv2.imwrite(output_path, image)
    print("[ENCODER] Encoded image saved to", output_path)

    if not os.path.exists(output_path):
        raise FileNotFoundError(f"Failed to save encoded image at {output_path}")


