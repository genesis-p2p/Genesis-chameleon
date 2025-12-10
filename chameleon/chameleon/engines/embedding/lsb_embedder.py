import numpy as np
from PIL import Image

class LSBEmbedder:

    @staticmethod
    def hide(cover_image_path: str, payload_bytes: bytes, output_path: str):
        img = Image.open(cover_image_path)
        img = img.convert("RGB")
        arr = np.array(img)

        h, w, c = arr.shape
        capacity_bits = h * w * c

        payload_length = len(payload_bytes)
        payload_bits = payload_length * 8

        if payload_bits + 32 > capacity_bits:
            raise ValueError("Payload too large for image.")

        # Convert payload to bit stream (with header)
        header = payload_length.to_bytes(4, byteorder="big")
        full_payload = header + payload_bytes
        bit_stream = ''.join(f'{byte:08b}' for byte in full_payload)

        flat = arr.reshape(-1)
        flat_bits = list(flat)

        # Embed bits
        for i, bit in enumerate(bit_stream):
            flat_bits[i] = (flat_bits[i] & 0xFE) | int(bit)

        # Save image
        new_arr = np.array(flat_bits).reshape(arr.shape)
        Image.fromarray(new_arr.astype('uint8')).save(output_path)
