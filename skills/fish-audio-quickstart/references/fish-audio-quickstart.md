# Fish Audio: quick reference

Use these canonical pages as the source of truth; confirm live details before writing or changing an integration.

## First TTS request

- [Coding Assistant Quickstart](https://docs.fish.audio/developer-guide/resources/agent-quickstart.md) — recommended retrieval order and task routing.
- [Quick Start](https://docs.fish.audio/developer-guide/getting-started/quickstart.md) — first generated voice, including current setup and example.
- [API introduction](https://docs.fish.audio/api-reference/introduction.md) and [TTS endpoint](https://docs.fish.audio/api-reference/endpoint/openapi-v1/text-to-speech.md) — REST authentication, request/response, formats, and errors.

Do not copy stale request parameters from memory: confirm endpoint, headers, body fields, model, audio format, and limits on the endpoint page. Store the API key in an environment variable or secret manager and keep it server-side.

## Route by task

| Task | Official documentation |
|---|---|
| Python SDK setup, auth, TTS | [Python overview](https://docs.fish.audio/developer-guide/sdk-guide/python/overview.md), [auth](https://docs.fish.audio/developer-guide/sdk-guide/python/authentication.md), [TTS](https://docs.fish.audio/developer-guide/sdk-guide/python/text-to-speech.md) |
| JavaScript SDK setup, auth, TTS | [JS installation](https://docs.fish.audio/developer-guide/sdk-guide/javascript/installation.md), [auth](https://docs.fish.audio/developer-guide/sdk-guide/javascript/authentication.md), [TTS](https://docs.fish.audio/developer-guide/sdk-guide/javascript/text-to-speech.md) |
| Voice cloning / model management | [Python cloning](https://docs.fish.audio/developer-guide/sdk-guide/python/voice-cloning.md), [create models](https://docs.fish.audio/developer-guide/core-features/creating-models.md), [voice cloning best practices](https://docs.fish.audio/developer-guide/best-practices/voice-cloning.md) |
| Voice design | [Voice Design guide](https://docs.fish.audio/features/voice-design.md), [API endpoint](https://docs.fish.audio/api-reference/endpoint/openapi-v1/voice-design.md) |
| Speech transcription | [Speech-to-text guide](https://docs.fish.audio/features/speech-to-text.md), [API endpoint](https://docs.fish.audio/api-reference/endpoint/openapi-v1/speech-to-text.md) |
| Real-time TTS | [WebSocket endpoint](https://docs.fish.audio/api-reference/endpoint/websocket/tts-live.md), [streaming best practices](https://docs.fish.audio/developer-guide/best-practices/real-time-streaming.md) |
| Emotion, pronunciation, fine control | [Emotions](https://docs.fish.audio/developer-guide/core-features/emotions.md), [fine-grained control](https://docs.fish.audio/developer-guide/core-features/fine-grained-control.md), [pronunciation dictionaries](https://docs.fish.audio/developer-guide/core-features/fine-grained-control/pronunciation-dictionaries.md) |
| Voice agents | [Agents overview](https://docs.fish.audio/agents/overview.md), [quickstart](https://docs.fish.audio/agents/quickstart.md) |

For API shape or generated clients, use the canonical [OpenAPI spec](https://docs.fish.audio/api-reference/openapi.json); for WebSocket events, use [AsyncAPI](https://docs.fish.audio/api-reference/asyncapi.yml).