#!/usr/bin/env python3
"""Extract video URLs from a YouTube playlist."""
import argparse
import re
import sys
from urllib.request import Request, urlopen

VIDEO_ID_RE = re.compile(r'"videoId":"([a-zA-Z0-9_-]{11})"')
WATCH_URL_RE = re.compile(r'/watch\?v=([a-zA-Z0-9_-]{11})')
WATCH_URL_TEMPLATE = "https://www.youtube.com/watch?v={id}"
USER_AGENT = "Mozilla/5.0 (compatible; youtube-playlist-extractor)"


def extract_with_scrape(playlist_url: str) -> list[str]:
    req = Request(playlist_url, headers={"User-Agent": USER_AGENT})
    with urlopen(req) as response:
        html = response.read().decode("utf-8", errors="replace")

    seen: set[str] = set()
    ordered: list[str] = []
    for match in VIDEO_ID_RE.finditer(html):
        vid = match.group(1)
        if vid not in seen:
            seen.add(vid)
            ordered.append(vid)
    if not ordered:
        for match in WATCH_URL_RE.finditer(html):
            vid = match.group(1)
            if vid not in seen:
                seen.add(vid)
                ordered.append(vid)
    return ordered


def extract_with_yt_dlp(playlist_url: str) -> list[str]:
    try:
        import yt_dlp
    except ImportError:
        sys.exit(
            "yt-dlp is not installed. Install it with `pip install yt-dlp` "
            "or omit --yt-dlp to use the built-in scraper."
        )

    opts = {"quiet": True, "extract_flat": True, "skip_download": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)

    entries = info.get("entries") or []
    ids: list[str] = []
    seen: set[str] = set()
    for entry in entries:
        if not entry:
            continue
        vid = entry.get("id")
        if vid and vid not in seen:
            seen.add(vid)
            ids.append(vid)
    return ids


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Extract video URLs from a YouTube playlist."
    )
    parser.add_argument("playlist", help="Playlist URL or ID")
    parser.add_argument(
        "-o", "--output",
        help="Write URLs to this file instead of stdout",
    )
    parser.add_argument(
        "--ids-only",
        action="store_true",
        help="Print bare video IDs instead of full watch URLs",
    )
    parser.add_argument(
        "--yt-dlp",
        action="store_true",
        help="Use yt-dlp to extract the playlist (more reliable, handles pagination)",
    )
    args = parser.parse_args(argv)

    playlist_url = args.playlist
    if not playlist_url.startswith(("http://", "https://")):
        playlist_url = f"https://www.youtube.com/playlist?list={playlist_url}"

    if args.yt_dlp:
        video_ids = extract_with_yt_dlp(playlist_url)
    else:
        video_ids = extract_with_scrape(playlist_url)

    lines = [
        vid if args.ids_only else WATCH_URL_TEMPLATE.format(id=vid)
        for vid in video_ids
    ]

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + ("\n" if lines else ""))
    else:
        for line in lines:
            print(line)

    sys.stderr.write(f"{len(video_ids)} videos found\n")
    return 0 if video_ids else 1


if __name__ == "__main__":
    raise SystemExit(main())
