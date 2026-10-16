---
name: fish-audio-quickstart
description: Generate first Fish Audio TTS audio quickly.
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: productivity
    tags: [fish-audio, tts, voice, audio]
---

# Fish Audio Quickstart

Use this skill to get a first working Fish Audio text-to-speech request in a few
minutes. It covers the API key, the three common client paths, the default voice,
and the first troubleshooting checks.

## When to Use

- The user wants to turn text into speech with Fish Audio.
- The user needs a minimal curl, Python, or JavaScript example.
- The user asks which model, endpoint, or environment variable to use first.

## When Not to Use

- The user needs voice cloning, voice design, streaming, or transcription details.
  Use the Fish Audio docs or SDK references for those.
- The user needs production billing, account, or deployment guidance.

## Quick Path

1. Create an API key at `https://fish.audio/app/api-keys`.
2. Export it as `FISH_API_KEY`; never hardcode it.
3. Use base URL `https://api.fish.audio` and endpoint `POST /v1/tts`.
4. Start with model `s2.1-pro-free`; use `s2.1-pro` for production.
5. Save the streamed response as `welcome.mp3`.

See [references/fish-audio-quickstart.md](references/fish-audio-quickstart.md) for
copy-paste examples and error checks.

## Defaults

- Auth header: `Authorization: Bearer $FISH_API_KEY`
- Content type: `application/json`
- Model header: `s2.1-pro-free` for evaluation, `s2.1-pro` for production
- Output format: `mp3`
- Voice: Fish Audio default unless `reference_id` is set

## Custom Voice

Find a voice ID in a `https://fish.audio/m/<id>` URL, then pass it as
`reference_id`. The same ID works in curl, Python, and JavaScript.

## First Failure Checks

- `401`: check `FISH_API_KEY`
- `402`: add API credit
- `400`: verify `reference_id` and request fields
- `429`: retry with backoff
