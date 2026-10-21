# jinx-talk

NeoForge 1.21.1 mod, mod id `jinxtalk`.

Jinx Talk sends game events from Minecraft to an external HTTP "event service"
and can announce responses back in-game. The service URL, timeout, and master
switch are configured in `config/jinxtalk.toml` (created on first run):

| Setting | Default | Meaning |
|---|---|---|
| `baseUrl` | `http://127.0.0.1:8712` | Base URL of the event service. Events are POSTed to `<base>/event`. |
| `timeoutSeconds` | `5` | HTTP connect/read timeout. A dead or slow service never blocks the game. |
| `enabled` | `true` | Master switch for all outbound events. |

## HTTP contract

Both event types below are POSTed as `application/json` to `<base>/event` on a
dedicated daemon thread pool, so the server thread is never blocked. Every
failure — bad URL, DNS, connect/read timeout, non-2xx status, malformed JSON —
is caught and logged; the game keeps running regardless.

`{"type":"chat_message","player":"<name>","message":"<text>"}`

Posted whenever a player sends a chat message (the chat path).

`{"type":"quest_completed","quest":"<quest title if available, otherwise quest id>","player":"<name>"}`

Posted when FTB Quests is installed and a team completes a quest (see below).

If the response JSON contains an `announce` string, the naming player is shown
that text as a gold chat line and hears `minecraft:entity.player.levelup`.

## FTB Quests integration (optional)

FTB Quests (mod id `ftbquests`, All the Mods 10 ships 2101.1.6 for Minecraft
1.21.1) is a **soft dependency**: it is declared `mandatory=false` with
`ordering="AFTER"` in `neoforge.mods.toml`, so jinx-talk loads and works
whether or not FTB Quests is installed.

When FTB Quests **is** present, jinx-talk subscribes to FTB Quests'
`dev.ftb.mods.ftbquests.events.ObjectCompletedEvent.QUEST` quest-completion
event (server side only). On every quest completion it POSTs
`{"type":"quest_completed","quest":...,"player":...}` to `<base>/event`, using
the same configured base URL (default `http://127.0.0.1:8712`), the same
timeout, and the same failure rules as the chat path. The `quest` field is the
quest's configured title, or its numeric id when the quest has no title.

If the service responds with an `announce` string, the player associated with
the completion receives a gold chat line with the announce text and the
`minecraft:entity.player.levelup` sound — exactly the same handling as chat
message responses.

## Building

This is a standard NeoForge MDK-style Gradle project (`build.gradle`,
`gradle.properties`). Generate the Gradle wrapper (`gradle wrapper`, or copy it
from a NeoForge MDK) and build with `./gradlew build`. Building resolves
NeoForge 1.21.1 and FTB Quests 2101.1.6 from Maven, which requires network
access to `maven.neoforged.com` and `maven.saps.dev`.

FTB Quests is a `compileOnly` dependency: it is never bundled into jinx-talk's
jar. It is only needed at compile time; at runtime the mod works without it.
