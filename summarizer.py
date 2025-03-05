import logging
import ollama

# Configure logging
logger = logging.getLogger(__name__)

def extract_title_and_summary(response):
    """Extract title and summary from the response text using unique markers."""
    title_marker = "###TITLE###"
    summary_marker = "###SUMMARY###"
    
    title = "No Title"
    summary = "No summary available."

    if title_marker in response and summary_marker in response:
        parts = response.split(title_marker)[1].split(summary_marker)
        title = parts[0].strip() if len(parts) > 0 else title
        summary = parts[1].strip() if len(parts) > 1 else summary

    # Clean title
    title = title.replace("\n", " ").strip()
    if len(title) > 100:
        title = title[:97] + "..."

    return title, summary

def summarize_text(text):
    """Generate both a title and a summary for the document using a single prompt."""
    try:
        prompt = (
            "Generate a concise title and a 5-sentence summary for the following document. Please reply in the language of the document!\n"
            "Format the response using these markers:\n"
            f"{'###TITLE###'} <Generated Title>\n"
            f"{'###SUMMARY###'} <Generated Summary>\n\n"
            f"Document:\n{text[:2000]}"
        )
        
        response = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": prompt}], stream=False)
        output_text = response["message"]["content"].strip()
        
        return extract_title_and_summary(output_text)
    except Exception as e:
        logger.error(f"Failed to generate title and summary with Ollama: {e}")
        return "No Title", "No summary available."
