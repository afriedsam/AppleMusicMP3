import requests
from bs4 import BeautifulSoup
import json
import sys
import re
import yt_dlp
from tqdm import tqdm
import logging
import os
import shutil


# Configure logging
class ColoredFormatter(logging.Formatter):
    COLORS = {
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "INFO": "\033[94m",  # Blue
        "DEBUG": "\033[92m",  # Green
        "RESET": "\033[0m",  # Reset
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset_color = self.COLORS["RESET"]
        record.msg = f"{log_color}{record.msg}{reset_color}"
        return super().format(record)


# Configure logging
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter("%(message)s"))
logging.basicConfig(level=logging.INFO, handlers=[handler])


def check_ffmpeg():
    """
    Checks if FFmpeg is installed and accessible.

    Raises:
        EnvironmentError: If FFmpeg is not found in the system path.
    """
    if not shutil.which("ffmpeg"):
        logging.error(
            "FFmpeg is not installed or not in your system PATH. Please install FFmpeg to continue."
        )
        raise EnvironmentError(
            "FFmpeg is required but not found. Install FFmpeg and ensure it's in your system PATH."
        )


def extract_apple_playlist(playlist_url):
    """
    Extracts the songs and artists from an Apple Music playlist.

    This function assumes the playlist is publicly accessible and follows a consistent structure.

    Args:
        playlist_url (str): The URL of the Apple Music playlist.

    Returns:
        tuple: A tuple containing two lists. The first list contains the names of the songs in the playlist, and the second list contains the names of the artists.

    Raises:
        ValueError: If no script tag is found in the HTML or no JSON data is found in the script tag. This can occur if the URL is not valid or the playlist is not public.
    """
    logging.info("Fetching playlist data...")
    response = requests.get(playlist_url)
    soup = BeautifulSoup(response.text, "html.parser")

    script_tag = soup.find("script", id="serialized-server-data")

    if script_tag:
        # get the JSON string
        json_str = script_tag.get_text()
    else:
        logging.error(
            "No script tag found in the HTML. Ensure Valid/Public Playlist URL"
        )
        raise ValueError(
            "No script tag found in the HTML. Ensure Valid/Public Playlist URL"
        )

    if json_str:
        # convert the JSON string into a Python dictionary
        data = json.loads(json_str)
    else:
        logging.error("No JSON data found. Ensure Valid/Public Playlist URL")
        raise ValueError("No JSON data found. Ensure Valid/Public Playlist URL")
    playlistJson = data[0]["data"]["seoData"]["ogSongs"]

    songs = []
    artists = []

    for song in playlistJson:
        songs.append(song["attributes"]["name"])
        artists.append(song["attributes"]["artistName"])

    logging.info(f"Found {len(songs)} songs in the playlist.")
    return songs, artists


def search_youtube(songs, artists):
    """
    Searches YouTube for official audio videos of songs by given artists.

    Parameters:
    - songs (list): A list of song titles.
    - artists (list): A list of artist names.

    Returns:
    - youtube_urls (list): A list of YouTube URLs for official audio videos of the songs.

    Warnings:
    - If the search results for a song by an artist cannot be fetched, a UserWarning is raised.
    - If no YouTube video is found for a song by an artist, a UserWarning is raised.
    """
    youtube_urls = []
    base_youtube_url = (
        "https://www.youtube.com"  # Base URL for constructing full YouTube video links
    )

    logging.info("Searching YouTube for songs...")
    for song, artist in tqdm(zip(songs, artists), total=len(songs), desc="Searching"):
        query = f"{song} {artist} official audio"
        search_url = (
            f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        )

        # Fetch the YouTube search results page
        response = requests.get(search_url)
        if response.status_code != 200:
            logging.warning(
                f"Failed to fetch search results for '{song}' by '{artist}'"
            )
            continue

        # Extract the first "watch" URL using regex
        match = re.search(r"\"url\":\"(/watch\?v=[^\"]+)", response.text)
        if match:
            video_url = base_youtube_url + match.group(1)
            video_url = video_url.split("\\")[0]
            youtube_urls.append(video_url)
        else:
            logging.warning(f"No YouTube video found for '{song}' by '{artist}'")

    return youtube_urls


def download_youtube_audio(youtube_urls, output_path):
    """
    Downloads the audio from the given YouTube URLs and saves them as MP3 files in the specified output path.

    Note:
        This function requires FFmpeg to be installed for audio extraction when using yt-dlp.

    Parameters:
        youtube_urls (list): A list of YouTube URLs from which the audio will be downloaded.
        output_path (str): The directory path where the downloaded audio files will be saved.

    Returns:
        None
    """
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path + "/%(title)s.%(ext)s",
        "quiet": True,
        "no-warnings": True,
        "progress_hooks": [lambda _: None],  # Prevent progress hooks output
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "logger": logging.getLogger("null"),  # Null logger to mute yt-dlp logs
        "no-progress": True,  # Remove yt_dlp progress bar
        "postprocessor-args": ["-loglevel", "quiet"],  # Silence FFmpeg logs
    }

    logging.info("Downloading audio files...")
    for url in tqdm(youtube_urls, total=len(youtube_urls), desc="Downloading"):
        if url:
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            except Exception as e:
                logging.warning(f"Failed to download: {url} ({e})")


def main():
    logging.info("Welcome to Apple Playlist YouTube Downloader CLI")
    print("================================================\n")

    if len(sys.argv) != 2:
        print("\033[91mError: Missing required argument.\033[0m")
        print("\033[93mUsage: python script.py <Apple Music Playlist URL>\033[0m")
        print(
            "\033[93mExample: python script.py https://music.apple.com/us/playlist/example\033[0m"
        )
        sys.exit(1)

    url = sys.argv[1]

    try:
        check_ffmpeg()
        songs, artists = extract_apple_playlist(url)
        yt_urls = search_youtube(songs, artists)
        download_youtube_audio(yt_urls, "output")
        logging.info("All downloads completed successfully!")
    except Exception as e:
        logging.error(f"Error: {e}")


if __name__ == "__main__":
    main()
