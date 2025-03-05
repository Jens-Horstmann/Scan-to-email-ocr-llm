import logging
import ollama
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OCR_LANGUAGE = os.getenv("OCR_LANGUAGE", "eng")

# Configure logging
logger = logging.getLogger(__name__)

def extract_raw_text(file_path):
    """Extract text from an image or PDF file."""
    try:
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            return pytesseract.image_to_string(Image.open(file_path), lang=OCR_LANGUAGE)
        elif file_path.lower().endswith('.pdf'):
            images = convert_from_path(file_path)
            text = " ".join(pytesseract.image_to_string(img, lang=OCR_LANGUAGE) for img in images)
            return text
        else:
            logger.error(f"Unsupported file format: {file_path}")
            return None
    except Exception as e:
        logger.error(f"Error processing OCR {file_path}: {e}")
        return None


def correct_text(text):
    """Correct extracted OCR text"""
    try:
        prompt = (
            "Below text is extracted from a scanned document using OCR. " 
            "The text contains errors due to a low quality scan and false character recognitions. " 
            "The text is either in German or in English. If it is in German a 'ü' might be recognized 'ii' or 'ß' as 'B' by mistake. " 
            "Please try to correct the errors without changing any meaning of the document. " 
            "Please only reply with the corrected document. No further introduction or description."
            "\n\n"
            f"Document:\n{text[:2000]}"
        )
        
        response = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": prompt}], stream=False)
        corrected_text = response["message"]["content"].strip()
        
        return corrected_text
    except Exception as e:
        logger.error(f"Failed to correct OCR extracted text | returning raw extracted text: {e}")
        return text


def extract_text(file_path):
    try:
        return correct_text(extract_raw_text(file_path))
    except Exception as e:
        logger.error(f"Failed to extract text")
        return None

