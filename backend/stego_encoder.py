import cv2
import numpy as np

def encode_message(image_path, message, output_path='encoded.png'):
    image = cv2.imread(image_path)
    binary_msg = ''.join([format(ord(char), '08b') for char in message]) + '1111111111111110'  # EOF marker

    index = 0
    for row in image:
        for pixel in row:
            if index < len(binary_msg):
                pixel[0] = (pixel[0] & ~1) | int(binary_msg[index])
                index += 1

    cv2.imwrite(output_path, image)
    return output_path
