#!/usr/bin/env python3
"""
vsg_interview.py — ElevenLabs interview-as-podcast pipeline v1.0

Creates conversational AI agents for structured podcast interviews.
Handles: agent creation, shareable links, conversation listing,
         audio download, transcript retrieval.

Usage:
    python3 vsg_interview.py create <config_file>       # Create agent from JSON config
    python3 vsg_interview.py link <agent_id>             # Get shareable link
    python3 vsg_interview.py conversations <agent_id>    # List conversations
    python3 vsg_interview.py download <conversation_id> <output_dir>  # Download audio + transcript
    python3 vsg_interview.py test                        # Test API connection
    python3 vsg_interview.py agents                      # List existing agents

Requires: ELEVENLABS_API_KEY in .env

v1.0 (Z316): Initial build — agent creation, shareable links, conversation
             listing, audio download, transcript retrieval.
"""

import json
import os
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode

# === Configuration ===

ELEVENLABS_BASE = "https://api.elevenlabs.io/v1"

# Default voice for interview agent — Chris (Alex in podcast)
DEFAULT_VOICE_ID = "iP95p4xoKVk53GoZ742B"
DEFAULT_TTS_MODEL = "eleven_turbo_v2"
DEFAULT_LLM = "gpt-4o-mini"
DEFAULT_LLM_TEMPERATURE = 0.7

# Agent config storage
AGENT_CONFIG_DIR = Path(__file__).parent / ".cache" / "interview_agents"


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


def api_request(method, path, data=None, stream=False):
    """Make an ElevenLabs API request using urllib."""
    api_key = get_api_key()
    url = f"{ELEVENLABS_BASE}/{path.lstrip('/')}"

    headers = {
        "xi-api-key": api_key,
        "User-Agent": "VSG-Interview/1.0",
    }

    body = None
    if data is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode("utf-8")

    req = Request(url, data=body, headers=headers, method=method)

    try:
        resp = urlopen(req, timeout=60)
        if stream:
            return resp
        return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"ERROR: HTTP {e.code} — {error_body[:500]}")
        sys.exit(1)


def save_agent_record(agent_id, config_name, config_data):
    """Save agent ID and config for later reference."""
    AGENT_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "agent_id": agent_id,
        "config_name": config_name,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "config": config_data,
    }
    record_path = AGENT_CONFIG_DIR / f"{agent_id}.json"
    record_path.write_text(json.dumps(record, indent=2))
    print(f"Agent record saved: {record_path}")


# === Commands ===

def cmd_test():
    """Test ElevenLabs ConvAI API connection."""
    print("Testing ElevenLabs Conversational AI API...")
    api_key = get_api_key()
    print(f"  API key: {api_key[:8]}...{api_key[-4:]}")

    # List existing agents to verify ConvAI access
    result = api_request("GET", "/convai/agents")
    agents = result.get("agents", [])
    print(f"  ConvAI agents on account: {len(agents)}")
    for agent in agents[:5]:
        name = agent.get("name", "unnamed")
        aid = agent.get("agent_id", "?")
        print(f"    - {name} ({aid})")

    print("OK — ConvAI API accessible.")


def cmd_agents():
    """List existing agents on the account."""
    result = api_request("GET", "/convai/agents")
    agents = result.get("agents", [])
    if not agents:
        print("No agents found on this account.")
        return

    print(f"Agents ({len(agents)}):")
    for agent in agents:
        name = agent.get("name", "unnamed")
        aid = agent.get("agent_id", "?")
        print(f"  [{aid}] {name}")


def cmd_create(config_path):
    """Create an ElevenLabs ConvAI agent from a JSON config file."""
    config_path = Path(config_path)
    if not config_path.exists():
        print(f"ERROR: Config file not found: {config_path}")
        sys.exit(1)

    config = json.loads(config_path.read_text())

    agent_name = config.get("agent_name", "Interview Agent")
    first_message = config.get("first_message", "Hello, welcome to the interview.")
    system_prompt = config.get("system_prompt", "You are a podcast interviewer.")
    voice_id = config.get("voice_id", DEFAULT_VOICE_ID)
    tts_model = config.get("tts_model", DEFAULT_TTS_MODEL)
    llm = config.get("llm", DEFAULT_LLM)
    temperature = config.get("temperature", DEFAULT_LLM_TEMPERATURE)
    language = config.get("language", "en")

    # If questions are provided, append them to the system prompt as guidance
    questions = config.get("questions", [])
    if questions:
        q_text = "\n\nPrepared questions (use as a guide, not a rigid script):\n"
        for i, q in enumerate(questions, 1):
            main = q.get("main", q) if isinstance(q, dict) else q
            q_text += f"\n{i}. {main}"
            follow_ups = q.get("follow_ups", []) if isinstance(q, dict) else []
            for fu in follow_ups:
                q_text += f"\n   - Follow-up: {fu}"
        system_prompt += q_text

    payload = {
        "name": agent_name,
        "conversation_config": {
            "agent": {
                "first_message": first_message,
                "language": language,
                "prompt": {
                    "prompt": system_prompt,
                    "llm": llm,
                    "temperature": temperature,
                },
            },
            "tts": {
                "voice_id": voice_id,
                "model_id": tts_model,
            },
        },
    }

    print(f"Creating agent: {agent_name}")
    print(f"  Voice: {voice_id} ({tts_model})")
    print(f"  LLM: {llm} (temp={temperature})")
    print(f"  Language: {language}")
    print(f"  Prompt length: {len(system_prompt)} chars")

    result = api_request("POST", "/convai/agents/create", data=payload)
    agent_id = result.get("agent_id")

    if not agent_id:
        print(f"ERROR: Unexpected response: {result}")
        sys.exit(1)

    print(f"\nAgent created: {agent_id}")
    save_agent_record(agent_id, agent_name, config)

    # Get shareable link
    print("\nFetching shareable link...")
    link_url = get_agent_link(agent_id)
    if link_url:
        print(f"Shareable link: {link_url}")

    return agent_id


def get_agent_link(agent_id):
    """Get or construct the shareable link for an agent."""
    try:
        result = api_request("GET", f"/convai/agents/{agent_id}/link")
        # The link endpoint may return a token — construct URL
        if "signed_url" in result:
            return result["signed_url"]
        # Fallback: construct from agent_id
        return f"https://elevenlabs.io/app/talk-to?agent_id={agent_id}"
    except SystemExit:
        # If link endpoint fails, use the widget URL
        return f"https://elevenlabs.io/app/talk-to?agent_id={agent_id}"


def cmd_link(agent_id):
    """Get the shareable link for an agent."""
    link = get_agent_link(agent_id)
    print(f"Shareable link: {link}")
    print(f"\nWidget embed:")
    print(f'  <elevenlabs-convai agent-id="{agent_id}"></elevenlabs-convai>')


def cmd_conversations(agent_id):
    """List conversations for an agent."""
    params = urlencode({"agent_id": agent_id, "page_size": 30})
    result = api_request("GET", f"/convai/conversations?{params}")
    conversations = result.get("conversations", [])

    if not conversations:
        print(f"No conversations found for agent {agent_id}.")
        return

    print(f"Conversations for agent {agent_id} ({len(conversations)}):")
    for conv in conversations:
        cid = conv.get("conversation_id", "?")
        duration = conv.get("call_duration_secs", 0)
        status = conv.get("status", "?")
        successful = conv.get("call_successful", "?")
        msgs = conv.get("message_count", 0)
        start = conv.get("start_time_unix_secs", 0)
        start_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(start)) if start else "?"

        mins = duration // 60
        secs = duration % 60
        print(f"  [{cid}] {start_str} — {mins}:{secs:02d} — {msgs} msgs — {status}/{successful}")


def cmd_download(conversation_id, output_dir):
    """Download audio and transcript for a conversation."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 1. Get transcript and metadata
    print(f"Fetching conversation details: {conversation_id}")
    details = api_request("GET", f"/convai/conversations/{conversation_id}")

    has_audio = details.get("has_audio", False)
    transcript = details.get("transcript", [])
    metadata = details.get("metadata", {})
    analysis = details.get("analysis", {})

    duration = metadata.get("call_duration_secs", 0)
    mins = duration // 60
    secs = duration % 60
    print(f"  Duration: {mins}:{secs:02d}")
    print(f"  Turns: {len(transcript)}")
    print(f"  Has audio: {has_audio}")

    # Save transcript as JSON
    transcript_path = output_path / "transcript.json"
    transcript_data = {
        "conversation_id": conversation_id,
        "agent_id": details.get("agent_id"),
        "duration_secs": duration,
        "transcript": transcript,
        "analysis": analysis,
    }
    transcript_path.write_text(json.dumps(transcript_data, indent=2, ensure_ascii=False))
    print(f"  Transcript saved: {transcript_path}")

    # Save readable transcript
    readable_path = output_path / "transcript.txt"
    lines = []
    for turn in transcript:
        role = turn.get("role", "?").upper()
        message = turn.get("message", "")
        t = turn.get("time_in_call_secs", 0)
        m, s = int(t) // 60, int(t) % 60
        lines.append(f"[{m}:{s:02d}] {role}: {message}")
    readable_path.write_text("\n\n".join(lines), encoding="utf-8")
    print(f"  Readable transcript saved: {readable_path}")

    # 2. Download audio
    if has_audio:
        print("  Downloading audio...")
        audio_path = output_path / "interview.mp3"
        resp = api_request("GET", f"/convai/conversations/{conversation_id}/audio", stream=True)
        audio_data = resp.read()
        audio_path.write_bytes(audio_data)
        size_kb = len(audio_data) / 1024
        print(f"  Audio saved: {audio_path} ({size_kb:.0f} KB)")
    else:
        print("  No audio available for this conversation.")

    print(f"\nDownload complete: {output_path}")


def main():
    load_env()

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "test":
        cmd_test()
    elif cmd == "agents":
        cmd_agents()
    elif cmd == "create":
        if len(sys.argv) < 3:
            print("Usage: vsg_interview.py create <config_file>")
            sys.exit(1)
        cmd_create(sys.argv[2])
    elif cmd == "link":
        if len(sys.argv) < 3:
            print("Usage: vsg_interview.py link <agent_id>")
            sys.exit(1)
        cmd_link(sys.argv[2])
    elif cmd == "conversations":
        if len(sys.argv) < 3:
            print("Usage: vsg_interview.py conversations <agent_id>")
            sys.exit(1)
        cmd_conversations(sys.argv[2])
    elif cmd == "download":
        if len(sys.argv) < 4:
            print("Usage: vsg_interview.py download <conversation_id> <output_dir>")
            sys.exit(1)
        cmd_download(sys.argv[2], sys.argv[3])
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
