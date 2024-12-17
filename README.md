# Apple Music Playlist to YouTube Audio Downloader

## Description
This Python tool allows you to extract song titles and artist names from **public Apple Music playlists**, search for the corresponding audio on YouTube, and download the audio files as **MP3s** using the `yt-dlp` library.

The script automates the entire process efficiently, providing clear progress visibility with **parallelized operations** and customizable output options.

> **Disclaimer:** Downloading copyrighted audio or video content from YouTube may violate its terms of service. This tool is intended for educational purposes only, and I am **not responsible for any misuse**.

---

## Features
- Fetches song and artist details from Apple Music playlists.
- Searches YouTube for matching audio content (e.g., "Official Audio").
- Downloads the audio and saves it in **MP3 format**.
- Provides a progress bar for each step of the process.
- **Parallelized operations** for faster YouTube searches and downloads.
- Allows you to **customize the output directory** where MP3 files are saved.

---

## Requirements
1. **Python 3.7+**
2. **FFmpeg**: Required for audio extraction when using `yt-dlp`.

### Install FFmpeg
Ensure FFmpeg is installed and added to your system `PATH`.
- On MacOS: `brew install ffmpeg`
- On Ubuntu/Debian: `sudo apt install ffmpeg`
- On Windows: [Download FFmpeg](https://ffmpeg.org/download.html), extract it, and add the bin folder to your system PATH.

---

## Installation
Install the tool directly from PyPI using `pip`:

```bash
pip install AppleMusicMP3
```

---

## Usage
Once installed, run the tool as a command-line program. Provide a valid **Apple Music Playlist URL**:

```bash
applemusicmp3 <Apple Music Playlist URL> [options]
```

### Options:
- `-t, --threads`: Set the number of parallel threads for faster downloads (default: `5`).
- `-o, --output`: Specify a custom output directory for downloaded MP3 files (default: `output`).

### Example:
```bash
applemusicmp3 https://music.apple.com/us/playlist/replay-2024/pl.example123 -t 8 -o my_music
```

### Output:
- Audio files will be downloaded as **MP3s** into the specified output folder (`my_music` in the above example).
- Progress will be displayed for fetching data, searching YouTube, and downloading audio files.

---

## Notes
- The playlist **must be public** for the script to fetch data successfully.
- Ensure **FFmpeg** is installed. If it is missing, the script will raise an error.
- Audio files are downloaded in high-quality MP3 format (192 kbps).
- Use the `-t` option to take advantage of **parallelized operations** for faster processing.

---

## Legal Disclaimer
Downloading content from YouTube is **against YouTube's terms of service**. This tool is provided for educational purposes only. By using this tool, you acknowledge that:
- You are responsible for your own actions.
- The author is **not liable** for any misuse of this tool.

Please ensure you have the right to download any content before proceeding.

---

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to improve the tool.

---

## License
MIT License

---

## Author
**Aidan Friedsam**  
GitHub: [afriedsam](https://github.com/afriedsam)  
PyPI: [Apple Music MP3](https://pypi.org/project/apple-music-mp3/)
