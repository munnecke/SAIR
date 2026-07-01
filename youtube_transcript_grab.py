#!/usr/bin/env python3
"""
youtube_transcript_grab.py

Pulls the caption-based transcript for a YouTube video and lets you extract
either the whole thing or just a window around a specific timestamp
(e.g. "David Brin's talk starts around t=32983s in a 9-hour livestream").

Requires captions to already exist on the video (auto-generated is fine).
If a video has NO captions at all, this will raise a
NoTranscriptFound / TranscriptsDisabled error -- in that case you need the
yt-dlp + Whisper route instead (audio-based transcription), which is a
different script.

Usage:
    python youtube_transcript_grab.py VIDEO_ID_OR_URL [options]

Examples:
    # Full transcript, saved to file
    python youtube_transcript_grab.py i6OQ5Z3repA -o full_transcript.txt

    # Just the 20 minutes around t=32983 seconds
    python youtube_transcript_grab.py i6OQ5Z3repA -t 32983 -w 1200 -o brin_segment.txt

    # Just print to stdout, no file
    python youtube_transcript_grab.py i6OQ5Z3repA -t 32983 -w 900
"""

import argparse
import re
import sys
from datetime import timedelta

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)


def extract_video_id(video_id_or_url: str) -> str:
    """Accepts a raw video ID or a full YouTube/youtu.be URL and returns the ID."""
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",       # watch?v=, embed/, v/
        r"youtu\.be\/([0-9A-Za-z_-]{11})",        # youtu.be short links
        r"live\/([0-9A-Za-z_-]{11})",             # /live/VIDEOID
    ]
    for pattern in patterns:
        match = re.search(pattern, video_id_or_url)
        if match:
            return match.group(1)
    # Assume it's already a bare video ID
    if re.fullmatch(r"[0-9A-Za-z_-]{11}", video_id_or_url):
        return video_id_or_url
    raise ValueError(f"Could not parse a video ID out of: {video_id_or_url}")


def fmt_timestamp(seconds: float) -> str:
    return str(timedelta(seconds=int(seconds)))


def fetch_transcript(video_id: str, languages=("en",)):
    """Fetch transcript, trying requested languages then falling back to
    auto-generated / any available language."""
    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)

    # Try preferred languages first (manually created, then auto-generated)
    try:
        transcript = transcript_list.find_transcript(languages)
    except NoTranscriptFound:
        # Fall back to whatever's available and translate to English if possible
        transcript = next(iter(transcript_list))
        if transcript.is_translatable:
            try:
                transcript = transcript.translate("en")
            except Exception:
                pass  # use original language if translation fails

    return transcript.fetch()


def main():
    parser = argparse.ArgumentParser(description="Fetch a YouTube transcript, optionally windowed around a timestamp.")
    parser.add_argument("video", help="YouTube video ID or full URL")
    parser.add_argument("-t", "--timestamp", type=float, default=None,
                         help="Center timestamp in seconds (e.g. 32983)")
    parser.add_argument("-w", "--window", type=float, default=900,
                         help="Window size in seconds around the timestamp (default 900 = 15 min total window, "
                              "i.e. +/- 450s). Ignored if --timestamp not given.")
    parser.add_argument("-o", "--output", default=None, help="Output file path (.txt). If omitted, prints to stdout.")
    parser.add_argument("--lang", default="en", help="Preferred language code (default: en)")
    args = parser.parse_args()

    video_id = extract_video_id(args.video)

    try:
        transcript = fetch_transcript(video_id, languages=(args.lang, "en"))
    except TranscriptsDisabled:
        print(f"ERROR: Captions are disabled for video {video_id}. "
              f"Try the yt-dlp + Whisper audio-transcription route instead.", file=sys.stderr)
        sys.exit(1)
    except NoTranscriptFound:
        print(f"ERROR: No transcript found for video {video_id} in language '{args.lang}' or any fallback.",
              file=sys.stderr)
        sys.exit(1)
    except VideoUnavailable:
        print(f"ERROR: Video {video_id} is unavailable (private, deleted, or region-locked).", file=sys.stderr)
        sys.exit(1)

    # transcript is a list of snippet objects/dicts with .text, .start, .duration
    entries = []
    for snippet in transcript:
        # Handle both dict-style and object-style snippets depending on library version
        if isinstance(snippet, dict):
            text, start, duration = snippet["text"], snippet["start"], snippet["duration"]
        else:
            text, start, duration = snippet.text, snippet.start, snippet.duration
        entries.append((start, duration, text))

    if args.timestamp is not None:
        half = args.window / 2
        lo, hi = args.timestamp - half, args.timestamp + half
        entries = [e for e in entries if lo <= e[0] <= hi]
        if not entries:
            print(f"No transcript entries found in the window {fmt_timestamp(lo)}–{fmt_timestamp(hi)}.",
                  file=sys.stderr)
            sys.exit(1)

    lines = []
    for start, duration, text in entries:
        lines.append(f"[{fmt_timestamp(start)}] {text}")

    output_text = "\n".join(lines)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_text + "\n")
        print(f"Wrote {len(entries)} transcript lines to {args.output}")
    else:
        print(output_text)


if __name__ == "__main__":
    main()
