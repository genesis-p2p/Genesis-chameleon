# image_utils.py
def ensure_png(filename: str):
    if not filename.lower().endswith(".png"):
        raise ValueError("Only PNG images are supported in Phase 1.")
