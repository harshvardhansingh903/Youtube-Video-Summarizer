import unittest
from src.transcriber import Transcriber

class TestTranscriber(unittest.TestCase):

    def setUp(self):
        self.transcriber = Transcriber()

    def test_fetch_transcript_valid_url(self):
        url = "https://www.youtube.com/watch?v=valid_video_id"
        transcript = self.transcriber.fetch_transcript(url)
        self.assertIsNotNone(transcript)
        self.assertIsInstance(transcript, str)

    def test_fetch_transcript_invalid_url(self):
        url = "https://www.youtube.com/watch?v=invalid_video_id"
        with self.assertRaises(ValueError):
            self.transcriber.fetch_transcript(url)

    def test_fetch_transcript_accessibility(self):
        url = "https://www.youtube.com/watch?v=private_video_id"
        with self.assertRaises(Exception):
            self.transcriber.fetch_transcript(url)

if __name__ == '__main__':
    unittest.main()