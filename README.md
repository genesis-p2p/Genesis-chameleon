<div align="center">

# 🦎 Project Chameleon

**A cyber steganography platform for hiding and extracting data inside PNG images using LSB techniques.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Phase](https://img.shields.io/badge/Phase-1%20MVP-brightgreen)]()

</div>

---

## 📖 Overview

Project Chameleon is a covert-channel steganography platform that lets you **hide arbitrary payloads inside PNG images** and **extract them back** — invisibly to the naked eye.

It ships with three interfaces:

| Interface | Description |
|-----------|-------------|
| 🌐 **REST API** | FastAPI server with `/hide` and `/extract` endpoints |
| 🖥️ **Desktop GUI** | Cyberpunk-themed Tkinter application with Matrix rain animation |
| 🔧 **Python Engine** | Importable `LSBEmbedder` / `LSBExtractor` classes for direct use |

---

## ✨ Features

- 🔒 **LSB Steganography** — hides data in the least-significant bits of every RGB channel
- 📦 **Any payload type** — embed text, binaries, files — anything as raw bytes
- 🛡️ **Deception mode** — extraction from a non-stego image returns deterministic noise instead of an error
- 🚀 **FastAPI backend** — async REST endpoints ready for integration
- 🎨 **Cyberpunk GUI** — animated Matrix rain, dark theme, embed/extract modes
- 🧪 **Unit tested** — automated round-trip test included

---

## 🏗️ Architecture

```
Genesis-chameleon/
├── chameleon/
│   ├── chameleon/
│   │   ├── api/
│   │   │   └── main.py          # FastAPI app (POST /hide, POST /extract)
│   │   ├── engines/
│   │   │   ├── embedding/
│   │   │   │   └── lsb_embedder.py   # LSBEmbedder — hides payload in PNG
│   │   │   └── extraction/
│   │   │       └── lsb_extractor.py  # LSBExtractor — recovers payload from PNG
│   │   ├── gui/
│   │   │   └── main_gui.py      # Tkinter GUI
│   │   └── utils/
│   │       ├── bit_utils.py
│   │       └── image_utils.py
│   └── tests/
│       └── test_basic_flow.py
├── requirment.txt               # pip dependencies
└── LICENSE
```

---

## ⚙️ Installation

### Prerequisites

- Python **3.8+**
- `pip`

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/genesis-p2p/Genesis-chameleon.git
cd Genesis-chameleon

# 2. (Optional) create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install fastapi uvicorn pillow numpy
```

---

## 🚀 Usage

### 1 — REST API

Start the server:

```bash
cd chameleon
uvicorn chameleon.api.main:app --reload
```

The API is now available at `http://127.0.0.1:8000`. Interactive docs at `http://127.0.0.1:8000/docs`.

#### `POST /hide`

Embed a payload file inside a cover PNG image.

| Field | Type | Description |
|-------|------|-------------|
| `cover_image` | file | Original PNG image |
| `payload` | file | Any file to hide inside the image |

```bash
curl -X POST "http://127.0.0.1:8000/hide" \
     -F "cover_image=@cover.png" \
     -F "payload=@secret.txt"
```

**Response:**
```json
{ "stego_image_path": "/tmp/tmpXXXXXX.png_stego.png" }
```

---

#### `POST /extract`

Recover the hidden payload from a stego PNG image.

| Field | Type | Description |
|-------|------|-------------|
| `stego_image` | file | PNG image containing hidden data |

```bash
curl -X POST "http://127.0.0.1:8000/extract" \
     -F "stego_image=@stego.png"
```

**Response:**
```json
{ "extracted_data": "your secret content here" }
```

---

### 2 — Desktop GUI

```bash
cd chameleon
python -m chameleon.gui.main_gui
```

The GUI opens with two modes:

- **EMBED MODE** — select a cover PNG and a payload file, then execute to produce a stego image
- **EXTRACT MODE** — select a stego PNG and save the extracted payload to disk

---

### 3 — Python Engine (direct import)

```python
from chameleon.engines.embedding.lsb_embedder import LSBEmbedder
from chameleon.engines.extraction.lsb_extractor import LSBExtractor

# Hide data
LSBEmbedder.hide(
    cover_image_path="cover.png",
    payload_bytes=b"top secret message",
    output_path="stego.png"
)

# Recover data
data = LSBExtractor.extract("stego.png")
print(data)  # b"top secret message"
```

---

## 🧪 Testing

```bash
cd chameleon
pytest tests/
```

The test suite performs a full round-trip: embeds `b"hello"` into a sample PNG, extracts it, and asserts equality.

---

## 🔬 How It Works

**Embedding**

1. Open the cover PNG and convert to RGB.
2. Prepend a 4-byte big-endian header encoding the payload length.
3. For every bit in `header + payload`, overwrite the LSB of the next pixel channel value.
4. Save the modified array as a new PNG (lossless).

**Extraction**

1. Read the first 32 LSBs to decode the payload length header.
2. Read the following `length × 8` LSBs and reconstruct the byte sequence.
3. If the header is invalid or the image is clean, **deception mode** returns deterministic SHA-256-derived noise so the tool reveals nothing about whether a payload exists.

---

## 📋 Requirements

| Package | Purpose |
|---------|---------|
| `fastapi` | REST API framework |
| `uvicorn` | ASGI server |
| `pillow` | Image I/O |
| `numpy` | Pixel array manipulation |

Install all at once:

```bash
pip install fastapi uvicorn pillow numpy
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built with 🦎 by <a href="https://github.com/genesis-p2p">genesis-p2p</a></sub>
</div>
