from transformers import pipeline
import torch

class Summarizer:
    def __init__(self):
        """Initialize the summarizer with BART model."""
        print("Loading the summarization model... (this might take a moment)")
        self.device = 0 if torch.cuda.is_available() else -1
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=self.device
        )
        
    def summarize(self, text):
        """Generate a concise summary of the input text."""
        try:
            if not text or len(text.strip()) < 50:
                print("Text is too short to summarize.")
                return None
                
            # Split text into chunks of approximately 1000 characters
            max_chunk_size = 1000
            chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]
            
            # Process each chunk and combine summaries
            summaries = []
            for chunk in chunks:
                if len(chunk.strip()) > 100:  # Only summarize chunks with substantial content
                    summary = self.summarizer(
                        chunk,
                        max_length=150,      # Longer summary for more detail
                        min_length=30,       # Ensure minimum length
                        do_sample=False,     # Deterministic output
                        num_beams=4,         # Better quality with beam search
                        length_penalty=2.0,  # Encourage slightly longer summaries
                        no_repeat_ngram_size=3  # Avoid repetition
                    )
                    summaries.append(summary[0]['summary_text'])
            
            if not summaries:
                print("Could not generate a meaningful summary.")
                return None
                
            # Join summaries with proper spacing and formatting
            final_summary = " ".join(summaries)
            
            # Format into paragraphs
            words = final_summary.split()
            if len(words) < 50:  # If summary is short, return as single paragraph
                return final_summary
                
            # Split into two paragraphs
            mid_point = len(words) // 2
            para1 = " ".join(words[:mid_point])
            para2 = " ".join(words[mid_point:])
            
            return f"{para1}\n\n{para2}"
            
        except Exception as e:
            print(f"Error in summarization: {str(e)}")
            return None