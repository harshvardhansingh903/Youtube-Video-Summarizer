# Youtube Video Summarizer

A powerful tool to transcribe and summarize any YouTube video using AI. Supports videos with or without captions, and provides concise, well-structured summaries.

## Features
- Works with any YouTube video (with or without captions)
- Multiple transcription methods (YouTube captions, auto-translated, or AI-powered audio transcription)
- Smart summarization using state-of-the-art language models
- Command-line interface for easy use

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/harshvardhansingh903/Youtube-Video-Summarizer.git
   cd Youtube-Video-Summarizer
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Install FFmpeg (required for audio processing):
   - Windows: `winget install -e --id Gyan.FFmpeg`
   - Mac: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

## Usage
Run the application:
```sh
python src/main.py
```
Enter a YouTube video URL when prompted. The summary will be displayed in the console.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
