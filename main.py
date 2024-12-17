import requests
from bs4 import BeautifulSoup
import json
import sys
import warnings
import re
import yt_dlp
from tqdm import tqdm  # For the progress bar


def extract_apple_playlist(playlist_url):
    """
    Extracts the songs and artists from an Apple Music playlist.

    Args:
        playlist_url (str): The URL of the Apple Music playlist.

    Returns:
        tuple: A tuple containing two lists. The first list contains the names of the songs in the playlist, and the second list contains the names of the artists.

    Raises:
        ValueError: If no script tag is found in the HTML or no JSON data is found in the script tag. This can occur if the URL is not valid or the playlist is not public.
    """
    print("Fetching playlist data...")
    response = requests.get(playlist_url)
    soup = BeautifulSoup(response.text, "html.parser")

    script_tag = soup.find("script", id="serialized-server-data")

    if script_tag:
        # get the JSON string
        json_str = script_tag.get_text()
    else:
        # Raise an error saying to make sure URL is correct/playlist is public
        raise ValueError(
            "No script tag found in the HTML. Ensure Valid/Public Playlist URL"
        )

    if json_str:
        # convert the JSON string into a Python dictionary
        data = json.loads(json_str)
    else:
        raise ValueError("No JSON data found. Ensure Valid/Public Playlist URL")
    playlistJson = data[0]["data"]["seoData"]["ogSongs"]

    songs = []
    artists = []

    for song in playlistJson:
        songs.append(song["attributes"]["name"])
        artists.append(song["attributes"]["artistName"])

    print(f"Found {len(songs)} songs in the playlist.")
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
    base_youtube_url = "https://www.youtube.com"

    print("\nSearching YouTube for songs...")
    for song, artist in tqdm(zip(songs, artists), total=len(songs), desc="Searching"):
        query = f"{song} {artist} official audio"
        search_url = (
            f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        )

        # Fetch the YouTube search results page
        response = requests.get(search_url)
        if response.status_code != 200:
            warnings.warn(
                f"\033[93mFailed to fetch search results for '{song}' by '{artist}'\033[0m",
                UserWarning,
            )
            youtube_urls.append(None)
            continue

        # Extract the first "watch" URL using regex
        match = re.search(r"\"url\":\"(/watch\?v=[^\"]+)", response.text)
        if match:
            video_url = base_youtube_url + match.group(1)
            video_url = video_url.split("\\")[0]
            youtube_urls.append(video_url)
        else:
            warnings.warn(
                f"\033[93mNo YouTube video found for '{song}' by '{artist}'\033[0m",
                UserWarning,
            )
            youtube_urls.append(None)

    return youtube_urls


def download_youtube_audio(youtube_urls, output_path):
    """
    Downloads the audio from the given YouTube URLs and saves them as MP3 files in the specified output path.

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
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    print("\nDownloading audio files...")
    for url in tqdm(youtube_urls, total=len(youtube_urls), desc="Downloading"):
        if url:  # Ensure URL is not None
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            except Exception as e:
                warnings.warn(f"\033[93mFailed to download: {url} ({e})\033[0m")


if __name__ == "__main__":
    print("\nWelcome to Apple Playlist YouTube Downloader CLI")
    print("================================================\n")

    if len(sys.argv) != 2:
        print("Usage: python script.py <Apple Music Playlist URL>")
        sys.exit(1)

    url = sys.argv[1]

    try:
        songs, artists = extract_apple_playlist(url)
        yt_urls = search_youtube(songs, artists)
        download_youtube_audio(yt_urls, "output")
        print("\nAll downloads completed successfully!")
    except Exception as e:
        print(f"\033[91mError: {e}\033[0m")
