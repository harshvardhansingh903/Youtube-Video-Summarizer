def validate_youtube_url(url):
    """
    Validates the provided YouTube URL.
    Returns True if the URL is valid, otherwise False.
    """
    import re
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})$'
    return re.match(youtube_regex, url) is not None

def format_summary(summary):
    """
    Formats the summary output for better readability.
    Returns the formatted summary as a string.
    """
    return summary.strip()  # Remove leading/trailing whitespace and return the summary
