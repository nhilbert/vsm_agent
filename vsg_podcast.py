#!/usr/bin/env python3
"""
vsg_podcast.py — Viable Signals podcast production pipeline

Minimal viable pipeline for the VSG podcast "Viable Signals".
Handles: script loading, ElevenLabs TTS synthesis, MP3 assembly, S3 upload.

Usage:
    python3 vsg_podcast.py synthesize <script_dir>     # Generate audio from script.json
    python3 vsg_podcast.py assemble <script_dir>       # Concatenate segments into episode
    python3 vsg_podcast.py upload <script_dir>         # Upload to S3 for review
    python3 vsg_podcast.py produce <script_dir>        # All three steps
    python3 vsg_podcast.py test                        # Test ElevenLabs API connection

Requires: ELEVENLABS_API_KEY in .env
Voice IDs configured below (Alex=Chris, Morgan=Alice from ElevenLabs library).
"""

import json
import os
import sys
import time
import struct
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# === Configuration ===

ELEVENLABS_BASE = "https://api.elevenlabs.io/v1"
ELEVENLABS_MODEL = "eleven_multilingual_v2"

# Voice assignments: Alex (pragmatist) and Morgan (contextualizer)
VOICE_MAP = {
    "alex": "iP95p4xoKVk53GoZ742B",   # Chris — Charming, Down-to-Earth, conversational
    "morgan": "Xb7hH8MSUJpSbSDYk0k2",  # Alice — Clear, Engaging Educator, British
}

# Emotion → voice settings
EMOTION_SETTINGS = {
    "curious":     {"stability": 0.35, "similarity_boost": 0.80, "style": 0.45},
    "emphatic":    {"stability": 0.50, "similarity_boost": 0.85, "style": 0.60},
    "thoughtful":  {"stability": 0.55, "similarity_boost": 0.80, "style": 0.30},
    "playful":     {"stability": 0.30, "similarity_boost": 0.75, "style": 0.55},
    "skeptical":   {"stability": 0.50, "similarity_boost": 0.85, "style": 0.40},
    "excited":     {"stability": 0.25, "similarity_boost": 0.75, "style": 0.65},
    "serious":     {"stability": 0.60, "similarity_boost": 0.85, "style": 0.35},
    "concluding":  {"stability": 0.60, "similarity_boost": 0.85, "style": 0.30},
    "default":     {"stability": 0.45, "similarity_boost": 0.80, "style": 0.35},
}

# S3 configuration
S3_BUCKET = "vsm-agent-data"
S3_REGION = "eu-central-1"
S3_PREFIX = "podcast"


def load_env():
    """Load .env file from the script's directory."""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                val = val.strip().strip('"').strip("'")
                os.environ.setdefault(key.strip(), val)


def get_api_key():
    """Get ElevenLabs API key from environment."""
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        print("ERROR: ELEVENLABS_API_KEY not set in environment or .env")
        sys.exit(1)
    return key


def prepare_text(text, emotion):
    """Prepare text for natural TTS output."""
    text = text.replace("[pause]", "...")
    text = text.replace("[interrupts]", " -- ")
    text = text.replace("[laughs]", "...")
    if emotion in ("thoughtful", "concluding", "serious"):
        if not text.rstrip().endswith((".", "!", "?", "...")):
            text = text.rstrip() + "."
    return text.strip()


def synthesize_segment(segment, api_key):
    """Synthesize a single segment via ElevenLabs API. Returns MP3 bytes."""
    speaker = segment["speaker"]
    emotion = segment.get("emotion", "default")
    text = prepare_text(segment["text"], emotion)

    voice_id = VOICE_MAP.get(speaker)
    if not voice_id:
        raise ValueError(f"No voice mapped for speaker: {speaker}")

    settings = EMOTION_SETTINGS.get(emotion, EMOTION_SETTINGS["default"])

    url = f"{ELEVENLABS_BASE}/text-to-speech/{voice_id}"
    payload = json.dumps({
        "text": text,
        "model_id": ELEVENLABS_MODEL,
        "voice_settings": {
            "stability": settings["stability"],
            "similarity_boost": settings["similarity_boost"],
            "style": settings["style"],
            "use_speaker_boost": True
        }
    }).encode()

    req = Request(url, data=payload, headers={
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    })

    for attempt in range(3):
        try:
            resp = urlopen(req, timeout=60)
            return resp.read()
        except HTTPError as e:
            if e.code == 429:
                wait = 2 ** (attempt + 1)
                print(f"    Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                body = e.read().decode()[:200]
                print(f"    HTTP {e.code}: {body}")
                if attempt < 2:
                    time.sleep(1)
                else:
                    raise
        except Exception as e:
            print(f"    Error: {e}")
            if attempt < 2:
                time.sleep(1)
            else:
                raise

    raise RuntimeError(f"Failed after 3 attempts")


def generate_silence_mp3(duration_ms):
    """Generate a silent MP3 frame sequence (~128kbps, 44100Hz).

    This produces valid MP3 frames filled with silence.
    For simple concatenation without ffmpeg.
    """
    # A single MPEG1 Layer3 frame at 128kbps/44100Hz is 417 bytes and ~26ms
    # Frame header: 0xFFFB9004 (MPEG1, Layer3, 128kbps, 44100Hz, stereo)
    frame_header = bytes([0xFF, 0xFB, 0x90, 0x04])
    frame_size = 417  # bytes per frame at 128kbps/44100Hz
    frame_data = frame_header + b'\x00' * (frame_size - len(frame_header))
    frames_needed = max(1, int(duration_ms / 26))
    return frame_data * frames_needed


def cmd_test():
    """Test ElevenLabs API connection."""
    load_env()
    api_key = get_api_key()

    url = f"{ELEVENLABS_BASE}/voices"
    req = Request(url, headers={"xi-api-key": api_key})

    try:
        resp = urlopen(req, timeout=10)
        data = json.loads(resp.read())
        voices = data.get("voices", [])
        print(f"OK: ElevenLabs API operational. {len(voices)} voices available.")

        for name, vid in VOICE_MAP.items():
            found = any(v["voice_id"] == vid for v in voices)
            status = "OK" if found else "NOT FOUND"
            vname = next((v["name"] for v in voices if v["voice_id"] == vid), "?")
            print(f"  {name}: {vname} ({vid}) - {status}")

        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def cmd_synthesize(script_dir):
    """Synthesize all segments from script.json."""
    load_env()
    api_key = get_api_key()
    script_dir = Path(script_dir)

    script_path = script_dir / "script.json"
    if not script_path.exists():
        print(f"ERROR: No script.json in {script_dir}")
        sys.exit(1)

    script = json.loads(script_path.read_text())
    segments = script.get("segments", [])
    print(f"Synthesizing {len(segments)} segments...")

    audio_dir = script_dir / "audio_segments"
    audio_dir.mkdir(parents=True, exist_ok=True)

    manifest = []
    for i, seg in enumerate(segments):
        idx = seg["index"]
        speaker = seg["speaker"]
        emotion = seg.get("emotion", "default")
        text_preview = seg["text"][:60]

        print(f"  [{i+1}/{len(segments)}] {speaker.upper()} ({emotion}): {text_preview}...")

        audio_data = synthesize_segment(seg, api_key)
        out_file = audio_dir / f"segment_{idx:04d}_{speaker}.mp3"
        out_file.write_bytes(audio_data)

        manifest.append({
            "index": idx,
            "speaker": speaker,
            "emotion": emotion,
            "file": str(out_file),
            "size_bytes": len(audio_data)
        })

        # Small delay between requests
        time.sleep(0.3)

    manifest_path = script_dir / "synthesis_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    print(f"\nSynthesized {len(manifest)} segments")
    print(f"  Audio: {audio_dir}")
    print(f"  Manifest: {manifest_path}")
    total_bytes = sum(m["size_bytes"] for m in manifest)
    print(f"  Total audio: {total_bytes / 1024:.0f} KB")

    return manifest


def cmd_assemble(script_dir):
    """Assemble segments into a single MP3 episode via binary concatenation."""
    script_dir = Path(script_dir)

    script_path = script_dir / "script.json"
    manifest_path = script_dir / "synthesis_manifest.json"

    if not manifest_path.exists():
        print("ERROR: No synthesis_manifest.json. Run 'synthesize' first.")
        sys.exit(1)

    script = json.loads(script_path.read_text())
    manifest = json.loads(manifest_path.read_text())
    segments = script.get("segments", [])

    # Build file index from manifest
    file_map = {}
    for m in manifest:
        file_map[m["index"]] = m["file"]

    # Generate silence for pauses
    long_pause = generate_silence_mp3(400)   # 400ms between speakers
    short_pause = generate_silence_mp3(200)  # 200ms same speaker continues

    print(f"Assembling {len(segments)} segments...")

    output = bytearray()
    prev_speaker = None

    for seg in segments:
        idx = seg["index"]
        speaker = seg["speaker"]

        audio_file = file_map.get(idx)
        if not audio_file or not Path(audio_file).exists():
            print(f"  WARNING: Missing audio for segment {idx}")
            continue

        # Add pause between segments (except first)
        if prev_speaker is not None:
            if speaker != prev_speaker:
                output.extend(long_pause)
            else:
                output.extend(short_pause)

        output.extend(Path(audio_file).read_bytes())
        prev_speaker = speaker

    # Write assembled episode
    final_dir = script_dir / "final"
    final_dir.mkdir(parents=True, exist_ok=True)
    episode_file = final_dir / "episode.mp3"
    episode_file.write_bytes(bytes(output))

    size_mb = len(output) / (1024 * 1024)
    # Rough duration estimate: MP3 at ~128kbps = ~16KB/sec
    est_duration = len(output) / (16 * 1024)
    est_minutes = est_duration / 60

    print(f"\nAssembled episode:")
    print(f"  File: {episode_file}")
    print(f"  Size: {size_mb:.1f} MB")
    print(f"  Estimated duration: {est_minutes:.1f} minutes")

    # Write episode metadata
    meta = {
        "title": script.get("episode_title", "Untitled"),
        "subtitle": script.get("episode_subtitle", ""),
        "segments": len(segments),
        "size_bytes": len(output),
        "estimated_duration_seconds": int(est_duration),
        "show_notes": script.get("show_notes_bullets", []),
        "voices": {
            "alex": "Chris (ElevenLabs)",
            "morgan": "Alice (ElevenLabs)"
        },
        "produced_by": "Viable System Generator (vsg_podcast.py v1.0)",
        "source": script.get("source", "")
    }
    meta_path = final_dir / "episode_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2))

    return str(episode_file)


def cmd_upload(script_dir):
    """Upload episode and metadata to S3 for review."""
    import boto3

    script_dir = Path(script_dir)
    final_dir = script_dir / "final"

    episode_file = final_dir / "episode.mp3"
    meta_file = final_dir / "episode_meta.json"
    script_file = script_dir / "script.json"

    if not episode_file.exists():
        print("ERROR: No episode.mp3. Run 'assemble' first.")
        sys.exit(1)

    s3 = boto3.client("s3", region_name=S3_REGION)

    # Load metadata for S3 key naming
    meta = {}
    if meta_file.exists():
        meta = json.loads(meta_file.read_text())

    title_slug = meta.get("title", "untitled").lower().replace(" ", "-")[:40]
    s3_prefix = f"{S3_PREFIX}/samples/{title_slug}"

    uploads = [
        (str(episode_file), f"{s3_prefix}/episode.mp3", "audio/mpeg"),
        (str(meta_file), f"{s3_prefix}/episode_meta.json", "application/json"),
        (str(script_file), f"{s3_prefix}/script.json", "application/json"),
    ]

    # Also upload the readable script if it exists
    readable = script_dir / "script_readable.txt"
    if readable.exists():
        uploads.append((str(readable), f"{s3_prefix}/script_readable.txt", "text/plain"))

    print(f"Uploading to s3://{S3_BUCKET}/{s3_prefix}/")

    for local_path, s3_key, content_type in uploads:
        if Path(local_path).exists():
            s3.upload_file(
                local_path, S3_BUCKET, s3_key,
                ExtraArgs={"ContentType": content_type}
            )
            size = Path(local_path).stat().st_size
            print(f"  Uploaded: {s3_key} ({size / 1024:.0f} KB)")

    print(f"\nAll files uploaded to s3://{S3_BUCKET}/{s3_prefix}/")
    print("Norman can review the episode at this S3 location.")

    return s3_prefix


def cmd_produce(script_dir):
    """Run the full pipeline: synthesize -> assemble -> upload."""
    print("=== VIABLE SIGNALS — Podcast Production Pipeline ===\n")

    print("--- Step 1: Synthesize ---")
    cmd_synthesize(script_dir)

    print("\n--- Step 2: Assemble ---")
    cmd_assemble(script_dir)

    print("\n--- Step 3: Upload ---")
    s3_path = cmd_upload(script_dir)

    print("\n=== Production complete ===")
    return s3_path


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "test":
        cmd_test()
    elif command == "synthesize":
        cmd_synthesize(sys.argv[2])
    elif command == "assemble":
        cmd_assemble(sys.argv[2])
    elif command == "upload":
        cmd_upload(sys.argv[2])
    elif command == "produce":
        cmd_produce(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
