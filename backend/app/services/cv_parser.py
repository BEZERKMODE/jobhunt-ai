"""
Extract plain text from uploaded CV files (PDF or DOCX).
"""

import io
import base64
import structlog

log = structlog.get_logger()


def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text_parts = []
        for page in reader.pages:
            text_parts.append(page.extract_text() or "")
        return "\n".join(text_parts).strip()
    except Exception as e:
        log.error("pdf_extraction_failed", error=str(e))
        return ""


def extract_text_from_docx(file_bytes: bytes) -> str:
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs).strip()
    except Exception as e:
        log.error("docx_extraction_failed", error=str(e))
        return ""


def extract_text(file_bytes: bytes, filename: str) -> str:
    """Auto-detect format and extract text."""
    filename_lower = filename.lower()
    if filename_lower.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif filename_lower.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    elif filename_lower.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")
    else:
        # Try PDF first, then docx
        text = extract_text_from_pdf(file_bytes)
        if not text:
            text = extract_text_from_docx(file_bytes)
        return text
