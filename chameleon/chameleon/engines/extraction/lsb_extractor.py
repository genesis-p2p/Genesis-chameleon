import numpy as np
from PIL import Image
import hashlib

class LSBExtractor:

    @staticmethod
    def extract(stego_image_path: str) -> bytes:
        img = Image.open(stego_image_path).convert("RGB")
        arr = np.array(img).reshape(-1)

        try:
            # ---------- Attempt normal extraction ----------
            header_bits = [str(arr[i] & 1) for i in range(32)]
            payload_length = int(''.join(header_bits), 2)

            # Sanity checks
            max_payload_bytes = (len(arr) - 32) // 8
            if payload_length <= 0 or payload_length > max_payload_bytes:
                raise ValueError("Invalid payload length")

            payload_bits_count = payload_length * 8
            total_bits = 32 + payload_bits_count

            bit_stream = [str(arr[i] & 1) for i in range(total_bits)]
            bit_string = ''.join(bit_stream[32:])

            extracted = int(bit_string, 2).to_bytes(payload_length, byteorder="big")

            # Optional lightweight validation (not perfect on purpose)
            if extracted.count(b'\x00') > payload_length * 0.9:
                raise ValueError("Likely noise")

            return extracted

        except Exception:
            # ---------- Deception Mode ----------
            return LSBExtractor._generate_noise(arr)

    @staticmethod
    def _generate_noise(arr: np.ndarray) -> bytes:
        """
        Generate deterministic noise derived from image content.
        Same image → same noise.
        """
        # Hash image data
        h = hashlib.sha256(arr.tobytes()).digest()

        # Expand hash into pseudo-random noise
        noise = bytearray()
        for i in range(64):  # fixed noise size (64 bytes)
            noise.extend(hashlib.sha256(h + bytes([i])).digest())

        return bytes(noise)
