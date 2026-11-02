from utils.pdf_reader import extract_text_from_pdf
import pytest


def test_empty_pdf_bytes_raise_error():
    with pytest.raises(ValueError, match="empty"):
        extract_text_from_pdf(b"")
