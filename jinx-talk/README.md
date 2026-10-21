# Jinx Talk 1.0.0

A small **Minecraft 1.21.1 / NeoForge** mod (`jinxtalk`) that sends private chat
questions to a Jinx HTTP service. Works on both a single-player integrated server
and a dedicated server. No client-only Minecraft classes, extra mod dependencies,
or bundled AI models are used. The service (`jinx_link.py`) is separate and is
**not included** in this project.

## Build

Install a **Java 21 JDK** and have internet access for the first build. From this
repository:

```sh
cd jinx-talk
./gradlew build
```

On Windows use `gradlew.bat build`. The Gradle wrapper is included; no global
Gradle installation is needed. ModDevGradle 2.0.148 and NeoForge 21.1.262 are pinned
in the project. The resulting mod is:

```text
build/libs/jinxtalk-1.0.0.jar
```

`build` runs the executable core test suite as part of `check`. Run just that
suite with `./gradlew coreTest`. It exercises prefix boundaries, Unicode line
splitting, the JSON request, and local HTTP success, malformed responses, errors,
read timeouts, an unreachable service and a saturated worker queue. Development
launchers are available as `./gradlew runClient` and `./gradlew runServer` (accept
the Minecraft EULA in the generated server run directory when prompted).

The repository's **Jinx Talk build** GitHub Actions workflow also runs the build
on pushes affecting this project and publishes a `jinxtalk-1.0.0` jar artifact.
Download and unzip that artifact to get the installable jar.

## Install in All the Mods 10 (ATM10)

1. Confirm the ATM10 instance is **Minecraft 1.21.1 using NeoForge** and Java 21.
2. Stop Minecraft (and the dedicated server, if applicable).
3. In your launcher, open the ATM10 instance's folder. For CurseForge, use the
   profile's menu → **Open Folder**; for Prism, open the instance's Minecraft
   folder. Copy `jinxtalk-1.0.0.jar` into its `mods/` directory, alongside the other
   mod jars. Remove an older Jinx Talk jar if upgrading.
4. For single-player, launch the instance normally. For multiplayer, install the
   jar in the **dedicated server's `mods/` folder** and restart it; the listener
   runs on the server, so installing only on a multiplayer client does nothing.
   This mod requires no client-side networking or assets.
5. Start your separate Jinx service, normally `jinx_link.py` on the same PC as
   the Minecraft server, listening at `http://127.0.0.1:8712`.

Keep the pack's NeoForge installation; do not replace the pack loader with a jar
from this project's development dependencies. This mod declares compatibility
with the NeoForge 21.1 series and Minecraft 1.21.1.

## Use

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
response or busy worker pool displays:

```text
[Jinx] (offline - start jinx_link.py on the PC)
```

The game continues normally. Four daemon workers and a bounded 16-request queue
keep network IO off the game thread; requests use a **1-second connect timeout**
and **25-second socket read timeout**. Responses are capped at 64 KiB. Replies
are dispatched back onto the server thread, and dropped if the original player
has left or the server/world has stopped. Network timeouts are per connection/read;
queued requests can wait for a worker before their timeout starts.

## Configuration

On first launch, NeoForge writes `config/jinxtalk-common.toml` in the instance
(or dedicated server) folder:

```toml
enabled = true
serviceBaseUrl = "http://127.0.0.1:8712"
```

Change the service base URL or set `enabled = false`, then restart the server or
single-player world. When disabled, the mod leaves all chat unchanged, including
these prefixes. The base must be an absolute HTTP(S) URL without credentials,
query or fragment; an optional path is supported, and `/chat` is appended.

**Dedicated-server note:** `127.0.0.1` is the machine running the Minecraft
server, not the player's PC. If Jinx runs on another PC, set a reachable trusted
LAN/service URL on the server, configure its firewall appropriately, and secure
the service. Do not expose an unauthenticated AI endpoint to the public internet.
Every enabled player can invoke this server-configured endpoint.

## Service contract and privacy

The mod POSTs UTF-8 JSON to `<serviceBaseUrl>/chat` with content type
`application/json`:

```json
{
  "player": "Alex",
  "message": "what should I do next?",
  "pos": [12.5, 64.0, -30.25],
  "dim": "minecraft:overworld",
  "ts": 1792531200000
}
```

`pos` contains the player's coordinates when they asked; `ts` is epoch
milliseconds. The question has its prefix and surrounding whitespace removed.
The service must return a successful HTTP status and a JSON object containing a
non-empty string reply:

```json
{"reply": "Try setting up a safe base before exploring."}
```

Only matching questions are sent. Ordinary chat is not forwarded. The service
receives the player's name, question, position, dimension and timestamp, so only
configure a service you trust. Redirects are not followed. The mod itself does
not log or store questions or replies; other server mods/service logs are outside
its control.
