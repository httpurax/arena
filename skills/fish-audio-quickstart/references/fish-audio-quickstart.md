# Fish Audio Quickstart

Base URL: `https://api.fish.audio`  
Endpoint: `POST /v1/tts`  
Auth: `Authorization: Bearer $FISH_API_KEY`

## curl

```bash
export FISH_API_KEY="replace_me"

curl -X POST https://api.fish.audio/v1/tts \
  -H "Authorization: Bearer $FISH_API_KEY" \
  -H "Content-Type: application/json" \
  -H "model: s2.1-pro-free" \
  -d '{"text":"Hello! Welcome to Fish Audio.","format":"mp3"}' \
  --output welcome.mp3
```

## Python

```bash
pip install fish-audio-sdk
```

```python
from fishaudio import FishAudio
from fishaudio.utils import save

client = FishAudio()  # reads FISH_API_KEY
audio = client.tts.convert(text="Hello! Welcome to Fish Audio.")
save(audio, "welcome.mp3")
```

## JavaScript

```bash
npm install fish-audio
```

```javascript
import { FishAudioClient } from "fish-audio";
import { writeFile } from "fs/promises";

const client = new FishAudioClient({ apiKey: process.env.FISH_API_KEY });
const audio = await client.textToSpeech.convert({ text: "Hello, world!" });
const buffer = Buffer.from(await new Response(audio).arrayBuffer());
await writeFile("welcome.mp3", buffer);
```

## Custom voice

```bash
export REFERENCE_ID="9a9cf47702da476aa4629e2506d4a857"
```

Add `"reference_id": "$REFERENCE_ID"` to the request body. Voice IDs come from
`https://fish.audio/m/<id>`.

## First checks

| Status | Cause | Fix |
|---|---|---|
| `401` | bad or missing key | check `FISH_API_KEY` |
| `402` | no credit | top up billing |
| `400` | bad `reference_id` or fields | read error `message` |
| `429` | rate limit | retry with backoff |
