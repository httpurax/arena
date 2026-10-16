---
name: fish-audio-quickstart
description: Generate speech with Fish Audio API and SDK.
version: 1.0.0
author: httpurax
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: development
---

## Overview

Fish Audio turns text into speech through `POST /v1/tts` or the official Python/JavaScript SDKs. This skill gets a first working request running, then points to [references/fish-audio-quickstart.md](references/fish-audio-quickstart.md) for streaming, cloning, ASR, and production details.

## When to Use

- The user wants to generate speech/audio with Fish Audio.
- Setting up an API key, SDK, first TTS request, voice, or model.
- Debugging a first Fish Audio request (`401`, `402`, `400`, `429`).

## When NOT to Use

- Deep voice-cloning, production tuning, or self-hosting; use the Fish Audio docs directly.
- Non-Fish-Audio TTS providers.

## Prerequisites

1. Create an account and API key at `fish.audio/app/api-keys`.
2. Store the key in the environment; never commit it:

```bash
export FISH_API_KEY=your_api_key_here
```

## Quick Start (Python)

```bash
pip install fish-audio-sdk
# optional local playback helpers (needs ffmpeg)
pip install "fish-audio-sdk[utils]"
```

```python
from fishaudio import FishAudio
from fishaudio.utils import save

client = FishAudio()  # reads FISH_API_KEY
audio = client.tts.convert(text="Hello from Fish Audio!")
save(audio, "output.mp3")
```

Async variant:

```python
import asyncio
from fishaudio import AsyncFishAudio

async def main():
    async with AsyncFishAudio() as client:
        audio = await client.tts.convert(text="Hello from Fish Audio!")
        from fishaudio.utils import save
        save(audio, "output.mp3")

asyncio.run(main())
```

## Quick Start (cURL)

```bash
curl --request POST https://api.fish.audio/v1/tts \
  --header "Authorization: Bearer $FISH_API_KEY" \
  --header "Content-Type: application/json" \
  --header "model: s2.1-pro" \
  --data '{"text":"Hello from Fish Audio!","format":"mp3"}' \
  --output output.mp3
```

## Voice and Model Selection

- Default voice is used when `reference_id` is omitted.
- Copy a model ID from a voice URL such as `https://fish.audio/m/<id>` and pass it as `reference_id`.
- Use `s2.1-pro` for production; `s2.1-pro-free` for development and testing.
- `s1` is deprecated and retires on 2026-12-31.
- S2 models support natural-language cues in brackets, e.g. `[whisper]`, `[laugh]`.

## Common Errors

| Status | Cause | Fix |
|---|---|---|
| `401` | Missing/invalid key | Check `FISH_API_KEY` and the key page. |
| `402` | Out of credits | Top up billing. |
| `400` | Bad `reference_id` or parameters | Verify the voice ID and request body. |
| `429` | Rate limit | Retry with exponential backoff. |

## Guardrails

- Never echo, log, commit, or write the API key to artifacts.
- Use `s2.1-pro-free` for experiments to avoid charges.
- Confirm voice IDs from Fish Audio URLs rather than guessing.

## Next Steps

- Streaming, cloning, ASR, realtime WebSocket, prosody, and rate limits: [references/fish-audio-quickstart.md](references/fish-audio-quickstart.md).
