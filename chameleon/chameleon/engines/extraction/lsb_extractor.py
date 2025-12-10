import numpy as np
from PIL import Image

class LSBExtractor:

    @staticmethod
    def extract(stego_image_path: str) -> bytes:
        img = Image.open(stego_image_path)
        img = img.convert("RGB")
        arr = np.array(img).reshape(-1)

        # First 32 bits = payload length
        header_bits = [str(arr[i] & 1) for i in range(32)]
        payload_length = int(''.join(header_bits), 2)

        payload_bits_count = payload_length * 8
        total_bits = 32 + payload_bits_count

        bit_stream = [str(arr[i] & 1) for i in range(total_bits)]

        # Convert to bytes
        bit_string = ''.join(bit_stream[32:])
        bytes_out = int(bit_string, 2).to_bytes(payload_length, byteorder="big")

        return bytes_out
