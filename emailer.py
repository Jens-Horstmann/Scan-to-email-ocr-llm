import yagmail
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Read email addresses from environment variables
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(file_path, title, summary, extracted_text):
    """Send an email with the generated title, summary, and extracted text, attaching the original file."""
    try:
        yag = yagmail.SMTP(SENDER_EMAIL, EMAIL_PASSWORD)
        subject = f"Scanned Document: {title}"
        body = f"Title: {title}\n\nSummary: {summary}\n\nExtracted Text:\n{extracted_text}"  # Include title, summary, and full text
        yag.send(to=RECIPIENT_EMAIL, subject=subject, contents=body, attachments=[file_path])
        logger.info(f"Email sent successfully with {file_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False
