from chameleon.engines.embedding.lsb_embedder import LSBEmbedder
from chameleon.engines.extraction.lsb_extractor import LSBExtractor

def test_basic_hide_extract():
    LSBEmbedder.hide(
        cover_image_path="tests/sample.png",
        payload_bytes=b"hello",
        output_path="tests/stego.png"
    )

    result = LSBExtractor.extract("tests/stego.png")
    assert result == b"hello"
