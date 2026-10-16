---
name: fish-audio-quickstart
description: Build Fish Audio integrations from official docs.
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: software-development
---

# Fish Audio Quickstart

Use this skill when implementing Fish Audio text-to-speech, speech-to-text, voice design or cloning, or real-time audio integrations.

## Workflow

1. Identify the task and retrieve the matching official Fish Audio page from [the reference map](references/fish-audio-quickstart.md). For implementation details, trust the live endpoint/SDK docs over memory; do not guess request fields, model names, limits, or SDK signatures.
2. For a first TTS integration, follow the official Quick Start and its current install, authentication, request, and audio-output example. Keep the example minimal and run it only with user-provided text and credentials.
3. Read credentials from `FISH_API_KEY` (or the documented secret manager). Never hard-code, print, commit, or include a real key in tests or examples. Keep server-side keys out of browser code.
4. Handle API errors and write/stream the returned audio according to the endpoint documentation. Verify output format and model support against the current docs.
5. If the user asks for a feature beyond basic TTS, route to the matching reference before coding. Ask which platform/SDK only when it changes the implementation and cannot be inferred.

## Safety and accuracy

- Use only voices and reference recordings the user has permission to use; do not help impersonate a real person without authorization.
- Treat uploaded audio and transcripts as private. Avoid retaining or sending them anywhere except the user-approved Fish Audio service.
- Never invent an endpoint, SDK method, model, or pricing/usage limit. Link the official source when explaining a version-sensitive detail.
- Do not call paid or destructive endpoints without the user's authorization.

See `references/fish-audio-quickstart.md` for official URLs and task routing.