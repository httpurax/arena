# Fish Audio Quickstart Reference

## Install

```bash
pip install fish-audio-sdk
pip install "fish-audio-sdk[utils]"  # optional playback/save helpers; needs ffmpeg
```

JavaScript:

```bash
npm install fish-audio
```

## Authentication

```bash
export FISH_API_KEY=your_api_key_here
```

SDKs read `FISH_API_KEY` automatically. Pass a key directly only in trusted local code.

## Python TTS

```python
from fishaudio import FishAudio
from fishaudio.utils import play, save

client = FishAudio()
audio = client.tts.convert(text="Hello, world!")
play(audio)
save(audio, "output.mp3")
```

Common options:

```python
audio = client.tts.convert(
    text="Custom voice",
    model="s2.1-pro",
    reference_id="802e3bc2b27e49c2995d23ef70e6ac89",
    speed=1.5,
)
```

Reusable config:

```python
from fishaudio.types import TTSConfig, Prosody

config = TTSConfig(
    prosody=Prosody(speed=1.2, volume=-5),
    reference_id="933563129e564b19a115bedd57b7406a",
    format="wav",
    latency="balanced",
)
audio1 = client.tts.convert(text="First message", config=config)
audio2 = client.tts.convert(text="Second message", config=config)
```

Streaming chunks:

```python
for chunk in client.tts.stream(text="Long content..."):
    send_to_websocket(chunk)
audio = client.tts.stream(text="Hello!").collect()
```

Realtime WebSocket for streamed text:

```python
def text_chunks():
    yield "Hello, "
    yield "this is "
    yield "streaming!"

audio_stream = client.tts.stream_websocket(text_chunks(), latency="balanced")
play(audio_stream)
```

## cURL TTS

```bash
curl --request POST https://api.fish.audio/v1/tts \
  --header "Authorization: Bearer $FISH_API_KEY" \
  --header "Content-Type: application/json" \
  --header "model: s2.1-pro" \
  --data '{"text":"Hello from Fish Audio!","format":"mp3","reference_id":"MODEL_ID"}' \
  --output output.mp3
```

## Models

- `s2.1-pro`: recommended production TTS; 83 languages; natural-language bracket cues; multi-speaker dialogue.
- `s2.1-pro-free`: same model at $0 for development/testing; no TTFA/DPA guarantees.
- `s2-pro`: previous S2 model; 80+ languages.
- `s1`: deprecated; retires 2026-12-31.
- ASR: `transcribe-1-pro` recommended; `transcribe-1` fallback. Select with exact `model` header.

## Voice Selection

- Omit `reference_id` for the default voice.
- Use IDs from `https://fish.audio/m/<id>`.
- Instant cloning:

```python
from fishaudio.types import ReferenceAudio

with open("reference.wav", "rb") as f:
    audio = client.tts.convert(
        text="Cloned voice speaking",
        references=[ReferenceAudio(audio=f.read(), text="Text spoken in reference")],
    )
```

- Persistent voice:

```python
with open("voice_sample.wav", "rb") as f:
    voice = client.voices.create(title="My Voice", voices=[f.read()], description="Custom voice clone")

audio = client.tts.convert(text="Using my saved voice", reference_id=voice.id)
```

## Speech-to-Text

```python
with open("audio.wav", "rb") as f:
    result = client.asr.transcribe(audio=f.read(), language="en")

print(result.text)
for segment in result.segments:
    print(f"[{segment.start:.2f}s - {segment.end:.2f}s] {segment.text}")
```

## Errors and Limits

- `401`: invalid/missing key.
- `402`: out of credits.
- `400`: bad `reference_id` or parameters.
- `429`: rate limit; retry with exponential backoff.
- Concurrency tiers: Starter 5, Elevated 15, High Volume 50, Enterprise custom.
- ASR requests share the same concurrency limit.

## Pricing (USD)

- `s2.1-pro`, `s2-pro`, `s1`: $15.00 per 1M UTF-8 bytes.
- `s2.1-pro-free`: $0.00 per 1M UTF-8 bytes.
- `transcribe-1-pro`, `transcribe-1`: $0.36 per audio hour.
- `voice-design-1`: $0.01 per successful request.

## Security

- Keep `FISH_API_KEY` in the environment or a secret manager.
- Never print or persist audio request bodies that contain keys.
- Use `s2.1-pro-free` for tests and prototypes.
