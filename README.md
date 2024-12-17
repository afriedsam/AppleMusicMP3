# Apple Music Playlist to YouTube Audio Downloader

## Description
This Python tool allows you to extract song titles and artist names from **public Apple Music playlists**, search for the corresponding audio on YouTube, and download the audio files as **MP3s** using the `yt-dlp` library. 

The script is designed to automate this process efficiently and includes a progress bar for clear visibility into the operations.

> **Disclaimer:** Downloading copyrighted audio or video content from YouTube may violate its terms of service. This tool is intended for educational purposes only, and I am **not responsible for any misuse**.

---

## Features
- Fetches song and artist details from Apple Music playlists.
- Searches YouTube for matching audio content (e.g., "Official Audio").
- Downloads the audio and saves it in **MP3 format**.
- Provides a progress bar for each step of the process.
- Includes error handling and logging for a smooth user experience.

---

## Requirements
1. **Python 3.7+**
2. **FFmpeg**: Required for audio extraction when using `yt-dlp`.
3. Required Python libraries:
    - `requests`
    - `beautifulsoup4`
    - `tqdm`
    - `yt-dlp`
    - `logging`

### Install FFmpeg
Ensure FFmpeg is installed and added to your system `PATH`.
- On MacOS: `brew install ffmpeg`
- On Ubuntu/Debian: `sudo apt install ffmpeg`
- On Windows: [Download FFmpeg](https://ffmpeg.org/download.html), extract it, and add the bin folder to your system PATH.

---

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/apple-music-youtube-downloader.git
   cd apple-music-youtube-downloader
   ```

2. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage
Run the script with a valid **Apple Music Playlist URL**:

```bash
python script.py <Apple Music Playlist URL>
```

### Example:
```bash
python script.py https://music.apple.com/us/playlist/replay-2024/pl.example123
```

### Output:
- Audio files will be downloaded as **MP3s** into the `output` folder.
- Progress will be displayed for fetching data, searching YouTube, and downloading audio files.

---

## Notes
- The playlist **must be public** for the script to fetch data successfully.
- Ensure **FFmpeg** is installed. If it is missing, the script will raise an error.
- Audio files are downloaded in high-quality MP3 format (192 kbps).

---

## Legal Disclaimer
Downloading content from YouTube is **against YouTube's terms of service**. This tool is provided for educational purposes only. By using this tool, you acknowledge that:
- You are responsible for your own actions.
- The author is **not liable** for any misuse of this tool.

Please ensure you have the right to download any content before proceeding.

---

## Future Plans
I plan to publish this tool on PyPI to make it easier to install and use:
```bash
pip install apple-music-downloader
```

If you encounter any issues or have feature requests, please open an issue on the GitHub repository.

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
