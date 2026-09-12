import os
from pypdf import PdfReader
from typing import Optional

def extract_text_from_pdf(file_path: str) -> Optional[str]:
    """
    Extracts text from a PDF file.
    
    Args:
        file_path (str): The path to the PDF file.
        
    Returns:
        Optional[str]: Extracted text or None if extraction fails or empty.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        text = text.strip()
        return text if text else None
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None
