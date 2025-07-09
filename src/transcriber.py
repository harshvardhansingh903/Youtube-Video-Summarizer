from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import yt_dlp
from faster_whisper import WhisperModel
import os
import tempfile
import subprocess
from pathlib import Path

class Transcriber:
    def __init__(self):
        """Initialize the transcriber with WhisperModel."""
        self.model = None  # Lazy load Whisper model
        self.ffmpeg_path = self._find_ffmpeg()
        
    def _find_ffmpeg(self):
        """Find FFmpeg in common installation locations."""
        # Check if ffmpeg is in PATH
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True)
            return 'ffmpeg'  # ffmpeg is in PATH
        except FileNotFoundError:
            pass
            
        # Common FFmpeg installation locations
        possible_paths = [
            # Windows - Default winget installation
            str(Path(os.environ.get('LOCALAPPDATA', '')) / 'Microsoft' / 'WinGet' / 'Packages' / 'Gyan.FFmpeg_*' / 'ffmpeg.exe'),
            # Windows - Program Files
            r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
            # Windows - scoop
            str(Path.home() / 'scoop' / 'shims' / 'ffmpeg.exe'),
            # Linux/Mac
            '/usr/bin/ffmpeg',
            '/usr/local/bin/ffmpeg'
        ]
        
        # Try to find ffmpeg in common locations
        for path in possible_paths:
            if '*' in path:  # Handle glob pattern
                try:
                    found = list(Path(path.rsplit('*', 1)[0]).parent.glob('*' + path.rsplit('*', 1)[1]))
                    if found:
                        ffmpeg_path = str(found[0])
                        try:
                            subprocess.run([ffmpeg_path, '-version'], capture_output=True)
                            return ffmpeg_path
                        except (FileNotFoundError, PermissionError):
                            continue
                except Exception:
                    continue
            elif os.path.exists(path):
                try:
                    subprocess.run([path, '-version'], capture_output=True)
                    return path
                except (FileNotFoundError, PermissionError):
                    continue
                    
        return None
        
    def _load_whisper_model(self):
        """Lazy load the Whisper model when needed."""
        if self.model is None:
            print("Loading Whisper model... (this might take a moment)")
            self.model = WhisperModel("base", device="cpu", compute_type="int8")
            
    def fetch_transcript(self, youtube_url):
        """Fetch transcript using multiple methods in order of preference."""
        try:
            video_id = self._extract_video_id(youtube_url)
            
            # Method 1: Try getting YouTube captions
            transcript = self._try_youtube_captions(video_id)
            if transcript:
                return transcript
                
            # Method 2: Try audio transcription
            print("No captions found. Attempting audio transcription...")
            
            # Check for FFmpeg before proceeding
            if not self.ffmpeg_path:
                print("\nError: FFmpeg not found. Please install FFmpeg:")
                print("- Windows: Run 'winget install -e --id Gyan.FFmpeg'")
                print("- Mac: Run 'brew install ffmpeg'")
                print("- Linux: Run 'sudo apt install ffmpeg' (Ubuntu) or equivalent")
                print("\nAfter installing, you may need to restart your terminal.")
                return None
                
            transcript = self._try_audio_transcription(youtube_url)
            if transcript:
                return transcript
                
            print("Could not transcribe the video through any available method.")
            return None
            
        except ValueError as e:
            print(f"\nError: {str(e)}")
            print("Please use a complete YouTube URL like:")
            print("- https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            print("- https://youtu.be/dQw4w9WgXcQ")
            return None
            
    def _try_youtube_captions(self, video_id):
        """Try getting transcript from YouTube captions."""
        try:
            # Try getting transcript directly first
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            if transcript:
                return " ".join(item['text'] for item in transcript)
        except Exception:
            try:
                # If direct fetch fails, try getting all available transcripts
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                
                # Try auto-translated English if available
                try:
                    transcript = transcript_list.find_generated_transcript(['en'])
                except:
                    # Try other languages and translate to English
                    languages = transcript_list.get_language_codes()
                    if languages:
                        transcript = transcript_list.find_transcript(languages[:1])
                        print(f"Found transcript in {transcript.language}. Translating to English...")
                        transcript = transcript.translate('en')
                    else:
                        return None
                
                transcript_data = transcript.fetch()
                return " ".join(item['text'] for item in transcript_data)
                
            except Exception:
                return None
                
    def _try_audio_transcription(self, youtube_url):
        """Download video audio and transcribe it using Whisper."""
        try:
            # Load Whisper model if not already loaded
            self._load_whisper_model()
            
            # Create temporary directory for audio download
            with tempfile.TemporaryDirectory() as temp_dir:
                audio_path = os.path.join(temp_dir, "audio.mp3")
                temp_audio = os.path.join(temp_dir, "temp.%(ext)s")
                
                # Configure yt-dlp with explicit FFmpeg path
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': temp_audio,
                    'ffmpeg_location': os.path.dirname(self.ffmpeg_path) if self.ffmpeg_path != 'ffmpeg' else None,
                    'verbose': True
                }
                
                try:
                    # Download audio
                    print("Downloading audio...")
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(youtube_url, download=True)
                        downloaded_file = ydl.prepare_filename(info)
                        base, _ = os.path.splitext(downloaded_file)
                        mp3_file = base + '.mp3'
                        
                        if not os.path.exists(mp3_file):
                            raise Exception("Audio file was not properly converted to MP3")
                            
                        print("Audio downloaded successfully.")
                        
                        # Transcribe audio
                        print("Transcribing audio... (this may take a while)")
                        segments, info = self.model.transcribe(mp3_file, beam_size=5)
                        return " ".join(segment.text for segment in segments)
                        
                except Exception as e:
                    print(f"Error during audio download: {str(e)}")
                    if os.path.exists(self.ffmpeg_path):
                        print(f"FFmpeg found at: {self.ffmpeg_path}")
                        print("But there might be an issue with the FFmpeg installation.")
                        print("Try uninstalling and reinstalling FFmpeg:")
                        print("1. Run: winget uninstall Gyan.FFmpeg")
                        print("2. Run: winget install -e --id Gyan.FFmpeg")
                        print("3. Restart your terminal")
                    return None
                    
        except Exception as e:
            print(f"Error during audio transcription: {str(e)}")
            return None
    
    def _extract_video_id(self, youtube_url):
        """Extract video ID from various YouTube URL formats."""
        try:
            # Remove any query parameters after '?si='
            url = youtube_url.split('?si=')[0]
            query = urlparse(url)
            if query.hostname == 'youtu.be':
                return query.path[1:]
            if query.hostname in ('www.youtube.com', 'youtube.com'):
                if query.path == '/watch':
                    return parse_qs(query.query)['v'][0]
            raise ValueError("Could not extract video ID from URL")
        except:
            raise ValueError("Invalid YouTube URL format")