from io import BytesIO
from pypdf import PdfReader


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    '''
    Extract text from a PDF uploaded by Streamlit.
    Scanned/image-only PDFs may return little or no text and need OCR,
    which this starter project does not yet implement.
    '''
    if not pdf_bytes:
        raise ValueError("The uploaded PDF is empty.")

    reader = PdfReader(BytesIO(pdf_bytes))
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")

    text = "\n".join(pages).strip()
    if not text:
        raise ValueError(
            "No selectable text was found in this PDF. It may be scanned; OCR is not implemented yet."
        )
    return text
