# youtube-playlist-extractor

Extract the video URLs from a YouTube playlist.

## Usage

```
python3 extractYT.py <playlist-url-or-id> [options]
```

Accepts either a full playlist URL (`https://www.youtube.com/playlist?list=...`)
or a bare playlist ID (`PL772556F1EFC4D01C`).

### Options

- `-o, --output FILE` — write URLs to a file instead of stdout.
- `--ids-only` — print bare video IDs instead of full `watch?v=...` URLs.
- `--yt-dlp` — use [yt-dlp](https://github.com/yt-dlp/yt-dlp) as the backend.
  More reliable and handles multi-page playlists. Requires
  `pip install yt-dlp`.

### Examples

```
python3 extractYT.py PL772556F1EFC4D01C
python3 extractYT.py https://www.youtube.com/playlist?list=PL772556F1EFC4D01C -o urls.txt
python3 extractYT.py PL772556F1EFC4D01C --yt-dlp --ids-only
```

Results are deduplicated in playlist order. The default scraper reads the
playlist page HTML; if YouTube changes its markup or the playlist spans
multiple pages, use `--yt-dlp`.
