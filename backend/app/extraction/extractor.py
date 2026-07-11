from app.extraction.pdf_extractor import extract_text_from_pdf
from app.extraction.ocr_extractor import extract_text_from_image


def extract_text(file_path: str) -> str:

    text = extract_text_from_pdf(file_path)

    if text:
        return text

    return extract_text_from_image(file_path)