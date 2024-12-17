import requests
from bs4 import BeautifulSoup
import json
import sys
import warnings
import re


def extract_apple_playlist(playlist_url):
    """Extracts the songs and artists from an Apple Music playlist.

    Args:
        playlist_url (str): The URL of the Apple Music playlist.

    Returns:
        tuple: A tuple containing two lists. The first list contains the names of the songs in the playlist, and the second list contains the names of the artists.

    Raises:
        ValueError: If no script tag is found in the HTML or no JSON data is found in the script tag. This can occur if the URL is not valid or the playlist is not public.
    """
    response = requests.get(playlist_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    script_tag = soup.find('script', id='serialized-server-data')

    if script_tag:
        # get the JSON string
        json_str = script_tag.get_text()
    else:
        # Raise an error saying to make sure URL is correct/playlist is public
        raise ValueError("No script tag found in the HTML. Ensure Valid/Public Playlist URL")

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
    
    for song, artist in zip(songs, artists):
        query = f"{song} {artist} official audio"
        search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        
        # Fetch the YouTube search results page
        response = requests.get(search_url)
        if response.status_code != 200:
            warnings.warn(
                f"\033[93mFailed to fetch search results for '{song}' by '{artist}'\033[0m", 
                UserWarning
            )
            continue
        
        # Extract the first "watch" URL using regex
        match = re.search(r'\"url\":\"(/watch\?v=[^\"]+)', response.text)
        if match:
            video_url = base_youtube_url + match.group(1)
            video_url = video_url.split('\\')[0]
            youtube_urls.append(video_url)
        else:
            warnings.warn(
                f"\033[93mNo Youtube video found for '{song}' by '{artist}'\033[0m", 
                UserWarning
            )
            
    return youtube_urls


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide the URL of the Apple Music Playlist as the first argument")
    url = sys.argv[1]
    
    songs, artists = extract_apple_playlist(url)
    
    yt_urls = search_youtube(songs, artists)
    print(yt_urls)