import unittest
from src.summarizer import Summarizer

class TestSummarizer(unittest.TestCase):

    def setUp(self):
        self.summarizer = Summarizer()

    def test_summarize_valid_transcript(self):
        transcript = [
            "This is the first line of the transcript.",
            "This is the second line of the transcript.",
            "This is the third line of the transcript.",
            "This is the fourth line of the transcript."
        ]
        summary = self.summarizer.summarize(transcript)
        self.assertIsInstance(summary, str)
        self.assertGreaterEqual(len(summary.splitlines()), 1)
        self.assertLessEqual(len(summary.splitlines()), 2)

    def test_summarize_empty_transcript(self):
        transcript = []
        summary = self.summarizer.summarize(transcript)
        self.assertEqual(summary, "No transcript available to summarize.")

    def test_summarize_single_line_transcript(self):
        transcript = ["This is a single line."]
        summary = self.summarizer.summarize(transcript)
        self.assertIsInstance(summary, str)
        self.assertGreaterEqual(len(summary.splitlines()), 1)
        self.assertLessEqual(len(summary.splitlines()), 2)

if __name__ == '__main__':
    unittest.main()