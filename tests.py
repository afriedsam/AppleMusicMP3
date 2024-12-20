import unittest
from unittest.mock import patch, MagicMock, call
import logging
from AppleMusicMP3.main import (
    check_ffmpeg,
    extract_apple_playlist,
    search_youtube,
    download_youtube_audio,
)

# Disable logging during tests
logging.disable(logging.CRITICAL)


class TestAppleMusicYouTube(unittest.TestCase):
    def test_check_ffmpeg_installed(self):
        """Test check_ffmpeg passes when FFmpeg is installed."""
        with patch("shutil.which", return_value="/usr/bin/ffmpeg"):
            try:
                check_ffmpeg()
            except EnvironmentError:
                self.fail("check_ffmpeg raised EnvironmentError unexpectedly!")

    def test_check_ffmpeg_not_installed(self):
        """Test check_ffmpeg raises EnvironmentError when FFmpeg is missing."""
        with patch("shutil.which", return_value=None):
            with self.assertRaises(EnvironmentError):
                check_ffmpeg()

    @patch("requests.get")
    def test_extract_apple_playlist(self, mock_get):
        """Test extract_apple_playlist extracts songs and artists correctly."""
        # Mock Apple Music response
        mock_html = """
        <script id="serialized-server-data">[{"data": {"seoData": {"ogSongs": [
            {"attributes": {"name": "Test Song 1", "artistName": "Artist 1"}},
            {"attributes": {"name": "Test Song 2", "artistName": "Artist 2"}}
        ]}}}]</script>
        """
        mock_get.return_value.text = mock_html

        playlist_url = "https://music.apple.com/us/playlist/example"
        songs, artists = extract_apple_playlist(playlist_url)

        self.assertEqual(songs, ["Test Song 1", "Test Song 2"])
        self.assertEqual(artists, ["Artist 1", "Artist 2"])

    @patch("requests.get")
    def test_search_youtube(self, mock_get):
        """Test search_youtube extracts YouTube links correctly."""
        # Simulated YouTube search result response
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = """
        <!DOCTYPE html>
        <html>
            <body>
                <script>
                    var ytInitialData = {"url":"/watch?v=test123"};
                </script>
            </body>
        </html>
        """

        # Input data
        songs = ["Test Song 1"]
        artists = ["Artist 1"]

        # Expected output
        expected_urls = ["https://www.youtube.com/watch?v=test123"]

        # Run the function
        yt_urls = search_youtube(songs, artists, max_threads=1)

        # Check if the function output matches the expected output
        self.assertEqual(yt_urls, expected_urls)

    @patch("yt_dlp.YoutubeDL")
    def test_download_youtube_audio(self, mock_youtubedl):
        """Test download_youtube_audio calls yt_dlp correctly."""
        # Mock the YoutubeDL context manager
        mock_instance = MagicMock()
        mock_youtubedl.return_value.__enter__.return_value = mock_instance

        youtube_urls = ["https://www.youtube.com/watch?v=test123"]
        output_path = "output"

        # Call the function
        download_youtube_audio(youtube_urls, output_path, max_threads=1)

        # Assert the download method was called correctly
        expected_calls = [call([url]) for url in youtube_urls]
        self.assertEqual(mock_instance.download.call_count, len(expected_calls))
        mock_instance.download.assert_has_calls(expected_calls)


if __name__ == "__main__":
    unittest.main()
