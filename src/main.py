from transcriber import Transcriber
from summarizer import Summarizer
import sys

def main():
    print("\n=== YouTube Video Summarizer ===")
    print("Enter a YouTube video URL (or 'q' to quit):")
    
    while True:
        youtube_url = input("\nYouTube URL > ").strip()
        
        if youtube_url.lower() == 'q':
            print("Goodbye!")
            sys.exit(0)
            
        if not youtube_url:
            print("Please enter a valid URL!")
            continue
            
        print("\nFetching video transcript...")
        transcriber = Transcriber()
        transcript = transcriber.fetch_transcript(youtube_url)
        
        if transcript:
            print("Generating summary...")
            summarizer = Summarizer()
            summary = summarizer.summarize(transcript)
            
            if summary:
                print("\n=== Video Summary ===")
                print(summary)
                print("\n" + "="*50 + "\n")
            else:
                print("Failed to generate summary.")
        else:
            print("Failed to fetch video transcript. Please check the URL and try again.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)