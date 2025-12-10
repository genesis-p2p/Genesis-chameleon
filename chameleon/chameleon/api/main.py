from fastapi import FastAPI, UploadFile, File
from chameleon.engines.embedding.lsb_embedder import LSBEmbedder
from chameleon.engines.extraction.lsb_extractor import LSBExtractor
import tempfile

app = FastAPI(title="Project Chameleon - Phase 1")

@app.post("/hide")
async def hide(cover_image: UploadFile = File(...), payload: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as cover_temp:
        cover_temp.write(await cover_image.read())
        cover_path = cover_temp.name

    payload_bytes = await payload.read()

    output_path = cover_path + "_stego.png"
    LSBEmbedder.hide(cover_path, payload_bytes, output_path)

    return {"stego_image_path": output_path}


@app.post("/extract")
async def extract(stego_image: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as stego_temp:
        stego_temp.write(await stego_image.read())
        stego_path = stego_temp.name

    data = LSBExtractor.extract(stego_path)

    return {"extracted_data": data.decode(errors="ignore")}
