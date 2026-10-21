# Jinx Talk 1.0.0

A **Minecraft 1.21.1 / NeoForge** mod (`jinxtalk`) that connects Minecraft to a
local Jinx HTTP companion service (`jinx_link.py`, maintained separately):

1. **Private `!jinx` chat prefixes (`!jinx`, `!ai`, `!j`)** — ask Jinx questions
   from ordinary chat without broadcasting publicly.
2. **Client keybind chat screen (`J`, category `"Jinx Talk"`)** — open a compact
   in-game Jinx dialog with a text input box and a scrollable history of the
   last Jinx replies received this session.
3. **Live cue channel (`GET <base>/cues`)** — while a world is loaded, polls
   `<serviceBaseUrl>/cues` asynchronously every 5 seconds for proactive chat
   lines, HUD titles/subtitles, and sound effects, with completely silent
   failure handling and zero game-thread blocking.
4. **FTB Quests quest completions (`POST <base>/event`, optional)** — when
   [FTB Quests](https://www.curseforge.com/minecraft/mc-mods/ftb-quests)
   (as shipped in All the Mods 10, 2101.1.6 for Minecraft 1.21.1) is installed,
   each quest completion is forwarded to the Jinx service, and an
   `"announce"` string in the service's response is shown to the player as a
   gold chat line with the `minecraft:entity.player.levelup` sound. FTB Quests
   is a **soft dependency**: Jinx Talk loads and works exactly the same with
   or without it.

Works in single-player, on a multiplayer client, and on a dedicated server. All
client-side classes (`dev.jinxtalk.client.*`) are isolated to `Dist.CLIENT` and
never loaded on dedicated servers.

## Build

Install a **Java 21 JDK** and have internet access for the first build. From this
repository:

```sh
cd jinx-talk
./gradlew build
```

On Windows use `gradlew.bat build`. The Gradle wrapper is included; no global
Gradle installation is needed. ModDevGradle 2.0.148 and NeoForge 21.1.262 are
pinned in the project. The resulting mod jar is:

```text
build/libs/jinxtalk-1.0.0.jar
```

`build` runs the executable core test suite as part of `check`. Run just that
suite with `./gradlew coreTest`. It exercises prefix parsing, Unicode line
splitting, URL validation for `/chat`, `/cues` and `/event`, bounded session
history, `/chat` POST requests, `/event` POST requests and `"announce"`
parsing, `/cues` GET polling and cue parsing, timeouts, malformed
responses, unreachable endpoints, and worker queue saturation. Development
launchers are available as `./gradlew runClient` and `./gradlew runServer`
(accept the Minecraft EULA in the generated server run directory when prompted).

The repository's **Jinx Talk build** GitHub Actions workflow runs `./gradlew build`,
verifies packaged JAR entries, the optional FTB Quests dependency declaration,
that no FTB Quests / Architectury classes are bundled into the jar, and
dedicated-server constant-pool class isolation, and publishes a
`jinxtalk-1.0.0` jar artifact.

## Install in All the Mods 10 (ATM10)

1. Confirm the ATM10 instance is **Minecraft 1.21.1 using NeoForge** and Java 21.
2. Stop Minecraft (and the dedicated server, if applicable).
3. Open your ATM10 instance folder (`mods/` directory) and copy
   `jinxtalk-1.0.0.jar` into `mods/`, removing any older Jinx Talk jar.
   - **Single-player:** installing on the client provides all features (`!jinx`
     chat prefixes, the `J` chat screen, and `/cues` polling).
   - **Multiplayer client:** installing on the client provides the `J` keybind
     chat screen and client `/cues` polling against your local Jinx service.
   - **Dedicated server:** installing in the server's `mods/` directory handles
     server-side `!jinx` / `!ai` / `!j` chat prefixes and dedicated-server
     `/cues` delivery without loading any client classes.
4. Start your separate Jinx service (normally `jinx_link.py` listening at
   `http://127.0.0.1:8712`).

Keep the pack's NeoForge installation; do not replace the pack loader with a jar
from this project's development dependencies. This mod declares compatibility
with the NeoForge 21.1 series and Minecraft 1.21.1.

**FTB Quests is optional.** ATM10 already ships FTB Quests 2101.1.6, so the
quest-completion integration (below) is active there with nothing extra to
install. On an instance or server without FTB Quests, Jinx Talk still loads
and all chat / keybind / cue features work as before — the FTB Quests classes
are a compile-time-only, non-bundled dependency (`compileOnly` in
`build.gradle`, `type="optional"` in `neoforge.mods.toml`), and the single
class that references them (`dev.jinxtalk.ftbquests.FtbQuestsIntegration`) is
only loaded after the mod confirms `ftbquests` is present.

## Use

### 1. Client Chat Screen (`J` Keybind)

Press **`J`** while in-game (configurable under **Options → Controls → Key Binds →
Jinx Talk → Open Jinx Chat**) to open the compact Jinx Talk overlay without
pausing the world:

- **Text input box:** type your message and press **Enter** (or click **Send**).
  Submitting sends the same asynchronous `POST <serviceBaseUrl>/chat` request
  used by `!jinx` and appends the reply to the session history.
- **Scrollable session history:** displays the last 50 Jinx replies received
  during the current session (including replies from both the `J` screen and
  single-player `!jinx` chat), wrapped cleanly with mouse-wheel, scrollbar drag,
  and `Up` / `Down` / `PageUp` / `PageDown` scrolling.

### 2. Private Chat Prefixes (`!jinx`, `!ai`, `!j`)

Type ordinary chat, **not a slash command**:

```text
!jinx what should I do next?
!ai where should I build my base?
!j how do I find diamonds?
```

Prefixes are case-sensitive and require whitespace before the question (so
`!joke` stays normal chat). Recognized messages are canceled before public chat
broadcast. Only the sender sees:

```text
[Jinx] thinking...
[Jinx] <the service's reply>
```

A bare `!jinx` (or bare alias, including trailing whitespace) stays local, makes
no HTTP request, and displays:

```text
[Jinx] Ask me anything: !jinx what should I do next?
```

Replies preserve line breaks and are split into lines of **at most 240 UTF-16
characters including `[Jinx] `** without breaking surrogate pairs. Text is shown
as literal chat, not interpreted as JSON chat components or commands. Any service
failure, timeout, non-success HTTP status, malformed/empty reply, oversized
response, or busy worker pool displays:

```text
[Jinx] (offline - start jinx_link.py on the PC)
```

### 3. FTB Quests Quest Completions (`/event`, only when FTB Quests is installed)

When FTB Quests is present, Jinx Talk subscribes to its quest-completion
events (the FTB Quests 2101.x `ObjectCompletedEvent.QUEST` progress/completion
event API). Each time a team completes a quest **server-side**, Jinx Talk
asynchronously POSTs one event to `<serviceBaseUrl>/event` naming the first
online member of the completing team:

```json
{"type": "quest_completed", "quest": "Farming Time", "player": "Alex"}
```

- **`"quest"`** is the quest's title when one is configured, otherwise the
  quest's numeric id.
- **`"player"`** is that player's name.
- The request uses the **same configured base URL** (`serviceBaseUrl`, default
  `http://127.0.0.1:8712`), the **same timeouts and worker pool**, and the
  **same failure rules** as the chat path: the POST happens off the game
  thread, and a dead, slow, or misbehaving service is silently ignored — it
  can never delay, break, or spam the game. No message is shown on failure.
- If the service's `2xx` JSON response contains an **`"announce"` string**,
  that player is shown the text as a **gold chat line** and hears the
  **`minecraft:entity.player.levelup`** sound:

  ```json
  {"announce": "Alex just finished Farming Time — nice work!"}
  ```

  A response with no `"announce"` string (or a blank one) is a silent no-op.
- Quest forwarding only runs while a server/world is running, and it honors
  `enabled = false` (see Configuration). Client-side FTB Quests GUI sync
  events are ignored; only real server-side completions are forwarded, one
  POST per completion.

### 4. Live Cue Channel (`/cues`)

While a world is loaded, Jinx Talk asynchronously polls
`GET <serviceBaseUrl>/cues` every **5 seconds** (100 ticks) when `enabled = true`.
At most one `/cues` request is in flight at any time, single-player never
double-polls, and **all failures are completely silent** without blocking any
game thread.

## Configuration

On first launch, NeoForge writes `config/jinxtalk-common.toml` in the instance
(or dedicated server) folder:

```toml
enabled = true
serviceBaseUrl = "http://127.0.0.1:8712"
```

Change the service base URL or set `enabled = false`, then restart the client or
server. When `enabled = false`, public chat prefixes are left unchanged,
background `/cues` polling is disabled, and FTB Quests completions are not
forwarded. The base must be an absolute HTTP(S) URL
without credentials, query, or fragment; an optional path prefix is supported,
and `/chat`, `/cues` or `/event` is appended.

**Dedicated-server note:** on a dedicated server, `127.0.0.1` refers to the
server host, whereas client features (`J` chat screen and client cue polling)
talk to the `serviceBaseUrl` configured in that client's
`config/jinxtalk-common.toml`. Only configure a trusted service and never expose
an unauthenticated AI endpoint to the public internet.

## Service Contract and Privacy

### `POST <serviceBaseUrl>/chat`

Sends UTF-8 JSON (`Content-Type: application/json; charset=utf-8`):

```json
{
  "player": "Alex",
  "message": "what should I do next?",
  "pos": [12.5, 64.0, -30.25],
  "dim": "minecraft:overworld",
  "ts": 1792531200000
}
```

Expects a `2xx` HTTP response with a strict JSON object containing a non-empty
string `reply`:

```json
{"reply": "Try setting up a safe base before exploring."}
```

### `GET <serviceBaseUrl>/cues`

Polled every 5 seconds while a world is loaded. Expects a `2xx` HTTP response
with a JSON object containing a `cues` array:

```json
{
  "cues": [
    {"kind": "chat", "text": "[Jinx] Watch your hunger bar!"},
    {"kind": "title", "text": "Blood Moon", "subtitle": "Find shelter soon"},
    {"kind": "sound", "sound": "minecraft:entity.experience_orb.pickup"}
  ]
}
```

Supported cue kinds:

- **`"chat"`**: displays `"text"` as a literal chat line.
- **`"title"`**: displays `"text"` as a screen title with optional `"subtitle"`
  (if omitted, `null`, or empty, any previous subtitle is cleared).
- **`"sound"`**: resolves and plays the sound event ID in `"sound"` (defaulting
  to the `minecraft` namespace if omitted).

Four daemon HTTP workers with a bounded 16-request queue keep all network IO off
game threads using a **1-second connect timeout**, **25-second socket read
timeout**, **64 KiB response cap**, and redirects disabled. All Minecraft state
reads and UI/world updates run exclusively on the appropriate main game thread.
