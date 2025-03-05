import os
import time
import logging
from dotenv import load_dotenv
from ocr import extract_text
from summarizer import summarize_text
from emailer import send_email

# Load environment variables
#load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load monitored folder from environment
SCAN_FOLDER = "/app/scans" #os.getenv("MONITORED_FOLDER", "scans")
FAILED_FOLDER = os.path.join(SCAN_FOLDER, "failed")
os.makedirs(FAILED_FOLDER, exist_ok=True)

# Dictionary to track failure counts
failure_counts = {}
MAX_FAILURES = 4

def process_file(file_path):
    """Process a new file by extracting text, summarizing it, and sending an email."""
    text = extract_text(file_path)
    if text:
        title, summary = summarize_text(text)
        logger.info(f"Generated Title: {title}")
        logger.info(f"Generated Summary: {summary}")
        email_sent = send_email(file_path, title, summary, text)
        if email_sent:
            logger.info(f"Email sent successfully, deleting file: {file_path}")
            os.remove(file_path)
            failure_counts.pop(file_path, None)  # Reset failure count on success
            return True
        else:
            logger.error(f"Failed to send email: {file_path}")
    else:
        logger.error(f"Failed to extract text from {file_path}")
    
    # Increment failure count
    failure_counts[file_path] = failure_counts.get(file_path, 0) + 1
    
    # Move file to failed folder after MAX_FAILURES attempts
    if failure_counts[file_path] >= MAX_FAILURES:
        failed_path = os.path.join(FAILED_FOLDER, os.path.basename(file_path))
        os.rename(file_path, failed_path)
        logger.error(f"File moved to failed folder after {MAX_FAILURES} attempts: {failed_path}")
        failure_counts.pop(file_path, None)  # Remove from failure tracking
    
    return False

def monitor_folder():
    """Monitor the scan folder for new files."""
    logger.info(f"Monitoring folder: {SCAN_FOLDER}")
    os.makedirs(SCAN_FOLDER, exist_ok=True)  # Ensure the folder exists
    
    while True:
        time.sleep(15)  # Check every 15 seconds
        try:
            files = [f for f in os.listdir(SCAN_FOLDER) if os.path.isfile(os.path.join(SCAN_FOLDER, f))]
            
            for file in files:
                file_path = os.path.join(SCAN_FOLDER, file)
                if os.path.isfile(file_path):
                    logger.info(f"Processing file: {file}")  # Log which file is being processed
                    process_file(file_path)
                    
        except Exception as e:
            logger.error(f"Error handling files: {e}")

if __name__ == "__main__":
    logger.info("Starting scan-to-email service v0.7")
    monitor_folder()
