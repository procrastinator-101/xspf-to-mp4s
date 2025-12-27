# XSPF Playlist Video Downloader & MP4 Converter

This project extracts video locations from an XSPF playlist file, downloads remote videos when needed, and converts all videos to MP4 format using `ffmpeg`.
It supports both **local file paths** and **remote URLs** inside the playlist and automatically handles conversion to a consistent MP4 (H.264 + AAC) output.

---

## Features

- Parse XSPF playlist files
- Extract all `<location>` entries
- Download remote video URLs automatically
- Handle dynamic video sources via Selenium when needed
- Convert all videos to MP4 format
- Clean up temporary files after execution

---

## Requirements

- Python **3.10+**
- `ffmpeg` installed and available in PATH
- Google Chrome (for Selenium fallback)

### Python Dependencies

```bash
pip install seleniumbase requests
```

## Project Structure

```
.
├── main.py              # CLI entry point
├── download.py          # Handles file downloading (requests + Selenium fallback)
├── convert_video.py     # Converts videos to MP4 using ffmpeg
├── output/              # Generated MP4 files
└── README.md
```

## Usage

### 1. Prepare an XSPF file

The playlist must contain valid `<location>` entries pointing to:

- Local video files, or
- Remote video URLs

Example:

```xml
<location>file:///path/to/video.avi</location>
<location>https://example.com/video.mp4</location>
```

### 2. Run the script

```bash
python main.py playlist.xspf
```

## How It Works

1. Parses the XSPF file and extracts all `<location>` tags
2. Determines whether each location is:
   - Local file → used directly
   - Remote URL → downloaded to a temporary directory
3. Converts each video to MP4 using ffmpeg
4. Saves converted files to the `output/` directory
5. Deletes temporary downloaded files after completion

## Output

All converted videos are saved as `.mp4` files in the output directory:

```
output/
├── video1.mp4
├── video2.mp4
```

## Notes

- Selenium is only used as a fallback when direct HTTP download fails
- The script runs headless Chrome for dynamic video sources
- Temporary files are safely removed after processing

## Example

```bash
python main.py my_playlist.xspf
```

Output:

```
✅ Converted video1.avi to output/video1.mp4
✅ Converted video2.mkv to output/video2.mp4
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/procrastinator-101/xspf-to-mp4s/blob/master/License) file for details.