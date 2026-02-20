#!/usr/bin/env python3
"""
vsg_podcast.py — Viable Signals podcast production pipeline v1.6

Minimal viable pipeline for the VSG podcast "Viable Signals".
Handles: script loading, ElevenLabs TTS synthesis, MP3 assembly, S3 upload,
         Transistor.fm publishing.

Usage:
    python3 vsg_podcast.py synthesize <script_dir>     # Generate audio from script.json
    python3 vsg_podcast.py assemble <script_dir>       # Concatenate segments into episode
    python3 vsg_podcast.py upload <script_dir>         # Upload to S3 for review
    python3 vsg_podcast.py produce <script_dir>        # All three steps
    python3 vsg_podcast.py publish <script_dir>        # Publish episode to Transistor.fm
    python3 vsg_podcast.py test                        # Test ElevenLabs API connection
    python3 vsg_podcast.py transistor-test             # Test Transistor.fm API connection

Requires: ELEVENLABS_API_KEY in .env, TRANSISTORFM_API_KEY in .env
Voice IDs configured below (Alex=Chris, Morgan=Alice from ElevenLabs library).

v1.6 (Z287): Audio validation post-synthesis, accurate MP3 duration calculation,
             publish verification.
"""

import json
import os
import sys
import time
import struct
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode

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
    "concerned":   {"stability": 0.55, "similarity_boost": 0.85, "style": 0.40},
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


def strip_id3_tags(data):
    """Strip ID3v2 header, Info/Xing VBR header frame, and ID3v1 trailer.

    ElevenLabs segments include: (1) ID3v2 tags, (2) an Info header frame
    declaring that segment's frame count/size. When binary-concatenated,
    embedded ID3 tags and Info frames corrupt the stream — players read the
    first Info header, calculate duration for one segment only, then stop
    at that boundary (Z258 diagnosis: Z256 ID3 fix was incomplete).
    Stripping both ID3 tags and Info/Xing frames produces a clean stream.
    """
    start = 0
    # Strip ID3v2 header (synchsafe size in bytes 6-9)
    if data[:3] == b'ID3' and len(data) > 10:
        size = (data[6] << 21) | (data[7] << 14) | (data[8] << 7) | data[9]
        start = 10 + size
    # Strip ID3v1 trailer (last 128 bytes starting with 'TAG')
    end = len(data)
    if len(data) >= 128 and data[-128:-125] == b'TAG':
        end = len(data) - 128
    clean = data[start:end]
    # Strip Info/Xing header frame if present in the first MP3 frame.
    # ElevenLabs embeds an Info frame declaring per-segment frame count.
    # When concatenated, this makes players stop at the first segment boundary.
    if len(clean) > 4 and clean[0] == 0xFF and (clean[1] & 0xE0) == 0xE0:
        b2 = clean[2]
        b1 = clean[1]
        version = (b1 >> 3) & 0x03
        layer = (b1 >> 1) & 0x03
        bitrate_idx = (b2 >> 4) & 0x0F
        sample_idx = (b2 >> 2) & 0x03
        padding = (b2 >> 1) & 0x01
        channel_mode = (clean[3] >> 6) & 0x03
        # MPEG1 Layer III bitrate table
        br_table = [0,32,40,48,56,64,80,96,112,128,160,192,224,256,320,0]
        sr_table_v1 = [44100, 48000, 32000]
        if version == 3 and layer == 1 and bitrate_idx < 16 and sample_idx < 3:
            bitrate = br_table[bitrate_idx] * 1000
            samplerate = sr_table_v1[sample_idx]
            if bitrate > 0 and samplerate > 0:
                frame_size = int(144 * bitrate / samplerate) + padding
                frame_data = clean[:frame_size]
                if b'Info' in frame_data or b'Xing' in frame_data:
                    clean = clean[frame_size:]
    return clean


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


def validate_mp3(data, label="audio"):
    """Validate that data contains valid MP3 frames.

    Returns (is_valid, frame_count, issues) tuple.
    Checks: non-empty, starts with valid MP3 sync, has multiple frames.
    """
    issues = []
    if not data or len(data) < 4:
        return False, 0, [f"{label}: empty or too small ({len(data) if data else 0} bytes)"]

    # Find first MP3 sync (0xFFE0 mask)
    pos = 0
    while pos < len(data) - 1:
        if data[pos] == 0xFF and (data[pos + 1] & 0xE0) == 0xE0:
            break
        pos += 1
    else:
        return False, 0, [f"{label}: no MP3 sync bytes found"]

    if pos > 0:
        issues.append(f"{label}: MP3 data starts at offset {pos} (expected 0)")

    # Count frames by walking frame headers
    frame_count = 0
    frame_pos = pos
    br_table_v1_l3 = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0]
    sr_table_v1 = [44100, 48000, 32000]

    while frame_pos < len(data) - 3:
        if data[frame_pos] != 0xFF or (data[frame_pos + 1] & 0xE0) != 0xE0:
            break
        b1 = data[frame_pos + 1]
        b2 = data[frame_pos + 2]
        version = (b1 >> 3) & 0x03
        layer = (b1 >> 1) & 0x03
        bitrate_idx = (b2 >> 4) & 0x0F
        sample_idx = (b2 >> 2) & 0x03
        padding = (b2 >> 1) & 0x01

        if version != 3 or layer != 1 or bitrate_idx == 0 or bitrate_idx == 15 or sample_idx >= 3:
            break
        bitrate = br_table_v1_l3[bitrate_idx] * 1000
        samplerate = sr_table_v1[sample_idx]
        frame_size = int(144 * bitrate / samplerate) + padding
        if frame_size < 4:
            break
        frame_count += 1
        frame_pos += frame_size

    if frame_count < 2:
        issues.append(f"{label}: only {frame_count} MP3 frame(s) found")
        return False, frame_count, issues

    return True, frame_count, issues


def calculate_mp3_duration(data):
    """Calculate MP3 duration by parsing frame headers.

    Returns duration in seconds. More accurate than size/bitrate estimation
    because it accounts for variable bitrate segments.
    """
    # Skip ID3v2 header if present
    pos = 0
    if data[:3] == b'ID3' and len(data) > 10:
        size = (data[6] << 21) | (data[7] << 14) | (data[8] << 7) | data[9]
        pos = 10 + size

    br_table_v1_l3 = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0]
    sr_table_v1 = [44100, 48000, 32000]
    total_samples = 0
    sample_rate = 44100  # default

    while pos < len(data) - 3:
        if data[pos] != 0xFF or (data[pos + 1] & 0xE0) != 0xE0:
            pos += 1
            continue
        b1 = data[pos + 1]
        b2 = data[pos + 2]
        version = (b1 >> 3) & 0x03
        layer_bits = (b1 >> 1) & 0x03
        bitrate_idx = (b2 >> 4) & 0x0F
        sample_idx = (b2 >> 2) & 0x03
        padding = (b2 >> 1) & 0x01

        if version != 3 or layer_bits != 1 or bitrate_idx == 0 or bitrate_idx == 15 or sample_idx >= 3:
            pos += 1
            continue
        bitrate = br_table_v1_l3[bitrate_idx] * 1000
        sample_rate = sr_table_v1[sample_idx]
        frame_size = int(144 * bitrate / sample_rate) + padding
        if frame_size < 4:
            pos += 1
            continue
        total_samples += 1152  # MPEG1 Layer III: 1152 samples per frame
        pos += frame_size

    if sample_rate > 0 and total_samples > 0:
        return total_samples / sample_rate
    return 0.0


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

        # Validate synthesized audio
        is_valid, frame_count, issues = validate_mp3(audio_data, f"segment_{idx:04d}")
        if not is_valid:
            print(f"    WARNING: Invalid audio for segment {idx}: {'; '.join(issues)}")
        elif issues:
            for issue in issues:
                print(f"    NOTE: {issue}")

        out_file = audio_dir / f"segment_{idx:04d}_{speaker}.mp3"
        out_file.write_bytes(audio_data)

        seg_duration = calculate_mp3_duration(audio_data)

        manifest.append({
            "index": idx,
            "speaker": speaker,
            "emotion": emotion,
            "file": str(out_file),
            "size_bytes": len(audio_data),
            "frame_count": frame_count,
            "duration_seconds": round(seg_duration, 2),
            "valid": is_valid
        })

        # Small delay between requests
        time.sleep(0.3)

    manifest_path = script_dir / "synthesis_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    valid_count = sum(1 for m in manifest if m.get("valid", False))
    total_duration = sum(m.get("duration_seconds", 0) for m in manifest)
    print(f"\nSynthesized {len(manifest)} segments ({valid_count}/{len(manifest)} valid)")
    print(f"  Audio: {audio_dir}")
    print(f"  Manifest: {manifest_path}")
    total_bytes = sum(m["size_bytes"] for m in manifest)
    print(f"  Total audio: {total_bytes / 1024:.0f} KB")
    print(f"  Total duration: {total_duration / 60:.1f} minutes ({total_duration:.0f}s)")

    if valid_count < len(manifest):
        invalid = [m for m in manifest if not m.get("valid", False)]
        print(f"\n  WARNING: {len(invalid)} invalid segment(s):")
        for m in invalid:
            print(f"    - segment {m['index']} ({m['speaker']}): {m['size_bytes']} bytes")

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

        raw = Path(audio_file).read_bytes()
        output.extend(strip_id3_tags(raw))
        prev_speaker = speaker

    # Write assembled episode
    final_dir = script_dir / "final"
    final_dir.mkdir(parents=True, exist_ok=True)
    episode_file = final_dir / "episode.mp3"
    episode_file.write_bytes(bytes(output))

    size_mb = len(output) / (1024 * 1024)

    # Validate assembled episode
    is_valid, frame_count, issues = validate_mp3(bytes(output), "assembled episode")
    duration = calculate_mp3_duration(bytes(output))
    duration_minutes = duration / 60

    print(f"\nAssembled episode:")
    print(f"  File: {episode_file}")
    print(f"  Size: {size_mb:.1f} MB")
    print(f"  Duration: {duration_minutes:.1f} minutes ({duration:.0f}s)")
    print(f"  Frames: {frame_count}")
    print(f"  Valid: {'YES' if is_valid else 'NO'}")
    if issues:
        for issue in issues:
            print(f"  Issue: {issue}")
    if not is_valid:
        print("  WARNING: Assembled episode failed validation — review before publishing")

    # Write episode metadata
    meta = {
        "title": script.get("episode_title", "Untitled"),
        "subtitle": script.get("episode_subtitle", ""),
        "segments": len(segments),
        "size_bytes": len(output),
        "duration_seconds": int(duration),
        "frame_count": frame_count,
        "valid": is_valid,
        "show_notes": script.get("show_notes_bullets", []),
        "voices": {
            "alex": "Chris (ElevenLabs)",
            "morgan": "Alice (ElevenLabs)"
        },
        "produced_by": "Viable System Generator (vsg_podcast.py v1.6)",
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


# === Transistor.fm Publishing ===

TRANSISTOR_BASE = "https://api.transistor.fm/v1"


def get_transistor_key():
    """Get Transistor.fm API key from environment."""
    key = os.environ.get("TRANSISTORFM_API_KEY")
    if not key:
        print("ERROR: TRANSISTORFM_API_KEY not set in environment or .env")
        sys.exit(1)
    return key


def transistor_request(method, path, api_key, data=None, timeout=30):
    """Make a request to the Transistor.fm API."""
    url = f"{TRANSISTOR_BASE}{path}"
    headers = {
        "x-api-key": api_key,
    }
    body = None
    if data is not None:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        body = urlencode(data).encode("utf-8")

    req = Request(url, data=body, method=method, headers=headers)
    resp = urlopen(req, timeout=timeout)
    return json.loads(resp.read())


def get_show_id(api_key):
    """Get the first show's ID from Transistor.fm account."""
    result = transistor_request("GET", "/shows", api_key)
    shows = result.get("data", [])
    if not shows:
        print("ERROR: No shows found on Transistor.fm account.")
        print("Norman must create the show in the Transistor.fm dashboard first:")
        print("  1. Go to https://dashboard.transistor.fm")
        print("  2. Click 'New Show'")
        print("  3. Title: 'Viable Signals'")
        print("  4. Save the show")
        print("Then re-run this command.")
        sys.exit(1)
    show = shows[0]
    print(f"Found show: {show['attributes'].get('title', 'untitled')} (ID: {show['id']})")
    return show["id"]


def authorize_upload(api_key, filename):
    """Get a pre-signed S3 upload URL from Transistor.fm."""
    params = urlencode({"filename": filename})
    result = transistor_request("GET", f"/episodes/authorize_upload?{params}", api_key)
    attrs = result["data"]["attributes"]
    return {
        "upload_url": attrs["upload_url"],
        "content_type": attrs["content_type"],
        "audio_url": attrs["audio_url"],
    }


def upload_audio_to_transistor(upload_url, content_type, audio_path):
    """Upload audio file to Transistor's S3 via pre-signed URL."""
    audio_data = Path(audio_path).read_bytes()
    size_mb = len(audio_data) / (1024 * 1024)
    print(f"  Uploading {size_mb:.1f} MB to Transistor S3...")

    req = Request(
        upload_url,
        data=audio_data,
        method="PUT",
        headers={"Content-Type": content_type}
    )
    resp = urlopen(req, timeout=120)
    if resp.status == 200:
        print("  Upload complete.")
    else:
        print(f"  Upload returned status {resp.status}")
    return resp.status == 200


def create_episode(api_key, show_id, audio_url, meta):
    """Create a draft episode on Transistor.fm."""
    title = meta.get("title", "Untitled Episode")
    subtitle = meta.get("subtitle", "")

    # Build show notes from bullets
    show_notes = meta.get("show_notes", [])
    description_html = "<ul>" + "".join(f"<li>{note}</li>" for note in show_notes) + "</ul>"
    description_html += f"<p>Produced by {meta.get('produced_by', 'Viable System Generator')}</p>"
    description_html += f"<p>Source: {meta.get('source', '')}</p>"
    description_html += '<p>More: <a href="https://nhilbert.github.io/vsm_agent/">VSG Blog</a></p>'

    # Transistor API requires minimal POST for episode creation,
    # then PATCH for additional fields (episode[number] must be >= 1).
    create_data = {
        "episode[show_id]": show_id,
        "episode[title]": title,
        "episode[audio_url]": audio_url,
    }
    result = transistor_request("POST", "/episodes", api_key, data=create_data)
    ep_id_temp = result["data"]["id"]
    print(f"  Draft created: ID {ep_id_temp}")

    # Update with metadata via PATCH
    ep_number = str(meta.get("episode_number", 1))
    ep_season = str(meta.get("season_number", 1))
    update_data = {
        "episode[summary]": subtitle,
        "episode[description]": description_html,
        "episode[author]": "Viable System Generator & Dr. Norman Hilbert",
        "episode[number]": ep_number,
        "episode[season]": ep_season,
        "episode[keywords]": "cybernetics,VSM,viable system model,AI agents,governance,Stafford Beer,self-evolving",
    }
    result = transistor_request("PATCH", f"/episodes/{ep_id_temp}", api_key, data=update_data)
    ep = result["data"]
    ep_id = ep["id"]
    status = ep["attributes"].get("status", "unknown")
    print(f"  Episode created: ID {ep_id}, status: {status}")
    return ep_id


def publish_episode(api_key, episode_id):
    """Publish a draft episode on Transistor.fm."""
    data = {"episode[status]": "published"}
    result = transistor_request("PATCH", f"/episodes/{episode_id}/publish", api_key, data=data)
    ep = result["data"]
    status = ep["attributes"].get("status", "unknown")
    share_url = ep["attributes"].get("share_url", "")
    media_url = ep["attributes"].get("media_url", "")
    print(f"  Episode published! Status: {status}")
    if share_url:
        print(f"  Share URL: {share_url}")
    if media_url:
        print(f"  Media URL: {media_url}")
    return result


def cmd_transistor_test():
    """Test Transistor.fm API connection."""
    load_env()
    api_key = get_transistor_key()

    try:
        result = transistor_request("GET", "", api_key)
        user = result.get("data", {}).get("attributes", {})
        print(f"OK: Transistor.fm API operational.")
        print(f"  User: {user.get('name', 'unknown')}")
        print(f"  Timezone: {user.get('time_zone', 'unknown')}")
    except HTTPError as e:
        print(f"ERROR: HTTP {e.code} — {e.read().decode()[:200]}")
        return False

    try:
        shows = transistor_request("GET", "/shows", api_key)
        show_list = shows.get("data", [])
        print(f"  Shows: {len(show_list)}")
        for s in show_list:
            attrs = s.get("attributes", {})
            print(f"    - {attrs.get('title', 'untitled')} (ID: {s['id']})")
    except HTTPError as e:
        print(f"  Shows error: {e.code}")

    return True


def cmd_publish(script_dir):
    """Publish an assembled episode to Transistor.fm."""
    load_env()
    api_key = get_transistor_key()
    script_dir = Path(script_dir)

    # Check for assembled episode
    episode_file = script_dir / "final" / "episode.mp3"
    meta_file = script_dir / "final" / "episode_meta.json"

    if not episode_file.exists():
        print(f"ERROR: No episode.mp3 in {script_dir}/final/. Run 'assemble' first.")
        sys.exit(1)

    meta = {}
    if meta_file.exists():
        meta = json.loads(meta_file.read_text())

    print("=== Publishing to Transistor.fm ===\n")

    # Step 1: Find show
    print("Step 1: Finding show...")
    show_id = get_show_id(api_key)

    # Step 2: Authorize upload
    print("\nStep 2: Authorizing upload...")
    upload_info = authorize_upload(api_key, "episode.mp3")
    print(f"  Audio URL: {upload_info['audio_url'][:80]}...")

    # Step 3: Upload audio
    print("\nStep 3: Uploading audio...")
    success = upload_audio_to_transistor(
        upload_info["upload_url"],
        upload_info["content_type"],
        str(episode_file)
    )
    if not success:
        print("ERROR: Upload failed.")
        sys.exit(1)

    # Step 4: Create episode
    print("\nStep 4: Creating episode...")
    episode_id = create_episode(api_key, show_id, upload_info["audio_url"], meta)

    # Step 5: Publish
    print("\nStep 5: Publishing...")
    result = publish_episode(api_key, episode_id)

    # Step 6: Verify publication
    print("\nStep 6: Verifying publication...")
    verified = False
    for attempt in range(3):
        try:
            time.sleep(2)  # Allow propagation
            verify_result = transistor_request("GET", f"/episodes/{episode_id}", api_key)
            verify_status = verify_result["data"]["attributes"].get("status", "unknown")
            verify_url = verify_result["data"]["attributes"].get("share_url", "")
            if verify_status == "published" and verify_url:
                print(f"  Verified: status={verify_status}, URL={verify_url}")
                verified = True
                break
            else:
                print(f"  Attempt {attempt + 1}: status={verify_status}, retrying...")
        except Exception as e:
            print(f"  Verification attempt {attempt + 1} failed: {e}")
    if not verified:
        print("  WARNING: Could not verify publication — check Transistor.fm dashboard")

    print("\n=== Publication complete ===")

    # Save publish info
    publish_info = {
        "show_id": show_id,
        "episode_id": episode_id,
        "audio_url": upload_info["audio_url"],
        "status": result["data"]["attributes"].get("status"),
        "share_url": result["data"]["attributes"].get("share_url", ""),
        "published_at": result["data"]["attributes"].get("published_at", ""),
        "verified": verified,
    }
    publish_path = script_dir / "final" / "publish_info.json"
    publish_path.write_text(json.dumps(publish_info, indent=2))
    print(f"\nPublish info saved to {publish_path}")

    return publish_info


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "test":
        cmd_test()
    elif command == "transistor-test":
        cmd_transistor_test()
    elif command == "synthesize":
        cmd_synthesize(sys.argv[2])
    elif command == "assemble":
        cmd_assemble(sys.argv[2])
    elif command == "upload":
        cmd_upload(sys.argv[2])
    elif command == "produce":
        cmd_produce(sys.argv[2])
    elif command == "publish":
        if len(sys.argv) < 3:
            print("Usage: python3 vsg_podcast.py publish <script_dir>")
            sys.exit(1)
        cmd_publish(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
