---
name: arena-pr-watcher
description: Ping Telegram on httpurax/arena PR CI state changes.
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: productivity
---

# Arena PR Watcher

A watchdog for the open pull requests of [httpurax/arena](https://github.com/httpurax/arena).
Every 30 minutes it polls the repo's PRs through the already-authenticated `gh` CLI,
compares each PR's CI state against the last-seen state in a local JSON file, and — only
when something changed — prints one batched message. Hermes cron's no-agent mode delivers
that stdout to Telegram verbatim using the Hermes install's existing Telegram setup; empty
stdout is a silent tick.

Three things trigger a message:

- a **new PR** is opened;
- a PR's checks **all go green** — ready to merge;
- a PR's checks **go failing**.

Each PR in the message carries its number, title, branch, check state, and link. Several PRs
that change in the same tick are batched into **one** message: one message per state change,
never more.

## When to Use

- The user asks to be told when an httpurax/arena PR is ready to merge, when CI breaks, or
  when someone opens a PR — set up the scheduled job in Setup, or run a tick manually.
- The user asks "what's up with the arena PRs?" — run the script manually (`--json` or
  `--dry-run`) and report; it is read-only.
- The user wants the watch paused, resumed, rescheduled, or removed — manage the cron job.

## When Not to Use

- The user wants a PR **merged, closed, approved, or commented on**. This skill notifies
  only; it never touches a PR, and neither should you on its behalf. A human merges.
- Watching a *different* repository on a schedule. The script accepts `--repo OWNER/NAME`
  for one-off checks, but the scheduled job watches `httpurax/arena`; for another repo create
  a second cron job with its own wrapper script (see Setup).
- The Hermes install has no Telegram configured — configure Telegram for Hermes first. This
  skill reuses it and carries no bot credentials of its own.

## Hard Rules

- **Notify only.** Never merge, close, approve, edit, or comment on a PR — by this skill or
  on its behalf. The message says *ready to merge*; a human merges.
- **No secrets in the repo or the state file.** GitHub auth is the machine's existing `gh`
  login; Telegram delivery is Hermes's existing setup (its own bot, its own home channel).
  This skill reads and writes neither. The state file holds public PR metadata only.
- **One message per state change.** A PR that stays green between ticks is not re-announced.
  PRs that change in the same tick become one batched message, never several.
- **Never echo credentials.** Output names what failed (a command, an endpoint), never a
  token or other secret value.

## How It Works

`scripts/pr_watch.py` (stdlib-only Python 3.8+, no third-party packages):

1. `gh pr list --repo httpurax/arena --state open` — the open PRs (number, title, branch,
   head SHA, link), up to 100 per tick.
2. Per PR, the CI state from the commit's check runs (falling back to the legacy combined
   commit status when a commit has no check runs). Three states:
   - `green` — every check finished as success / skipped / neutral;
   - `failing` — at least one check failed, was cancelled, or timed out;
   - `running` — something is still queued / in progress / parked on a person, or nothing
     has been reported yet.
3. Diff against the state file and compute the events (opened / green / failing). A change
   into `running` announces nothing but is still stored, so a PR that flaps
   failing → running → failing announces the second failure exactly once.
4. Print the batched message to stdout (or nothing), then atomically rewrite the state
   file.

**State file:** `data/pr-state.json` in the skill directory — **gitignored** by this
skill's `.gitignore`, never committed. The schema is shown in
`examples/pr-state.example.json`; it stores only public PR metadata (title, branch, head
SHA, link, last-seen CI state).

**Baseline:** the first run against a missing (or unreadable) state file records the PRs
open now and says nothing — the watch starts from a quiet state instead of replaying
history. Deleting the state file re-baselines the same way.

## Setup — one time

1. Install the skill (from the repo root):

```bash
python3 tools/install_skills.py
```

```powershell
python tools\install_skills.py
```

2. The cron scheduler only runs scripts that live in `$HERMES_HOME/scripts/`, so copy the
   watcher there. The state file then lands in `$HERMES_HOME/data/pr-state.json` — private,
   outside any repo:

```bash
hermes="${HERMES_HOME:-$HOME/.hermes}"
mkdir -p "$hermes/scripts"
cp "$hermes/skills/productivity/arena-pr-watcher/scripts/pr_watch.py" "$hermes/scripts/pr_watch.py"
```

```powershell
$hermes = if ($env:HERMES_HOME) { $env:HERMES_HOME } else { Join-Path $HOME '.hermes' }
New-Item -ItemType Directory -Force (Join-Path $hermes 'scripts') | Out-Null
Copy-Item (Join-Path $hermes 'skills/productivity/arena-pr-watcher/scripts/pr_watch.py') (Join-Path $hermes 'scripts\pr_watch.py')
```

3. Create the cron job — every 30 minutes, no agent (no LLM involved), delivered to
   Telegram:

```bash
hermes cron create "every 30m" \
  --no-agent \
  --script pr_watch.py \
  --deliver telegram \
  --name "arena-pr-watcher"
```

What the no-agent mode does, exactly:

- the script's stdout (trimmed) **is** the Telegram message;
- **empty stdout = silent tick** — no delivery, no message;
- a non-zero exit delivers an error alert, so a broken watch (for example `gh` logged
  out) cannot fail silently;
- no tokens, no model, no provider — the job never touches the inference layer.

Delivery uses the Hermes install's **existing** Telegram setup — the same bot you already
chat with, into its home channel (the default chat for cron delivery). Nothing in this
skill stores or transmits bot credentials. If the job reports a blocked delivery target
instead of running, the Hermes install has no Telegram configured yet.

Two environment notes for the cron run:

- Hermes sanitizes the script's environment: provider credentials and Hermes-managed
  secrets are not inherited. `gh` authentication stored by `gh auth login` (its own config
  file) keeps working; an env-var token like `GH_TOKEN` would not — if your `gh` relies on
  one, do a file-based `gh auth login`.
- `gh` must be on `PATH` for the Hermes process.

To watch another repo on a schedule, write a small wrapper in `$HERMES_HOME/scripts/`
(e.g. `pr_watch_acme.sh` that runs the script with `--repo OWNER/NAME --state <its own
state file>`) and create a second cron job for it.

## Managing the Watch

```bash
hermes cron list                 # find the job id
hermes cron run <job-id>         # one immediate tick (good for testing)
hermes cron pause <job-id>       # stop without deleting
hermes cron resume <job-id>
hermes cron edit <job-id>        # e.g. change "every 30m" to "every 15m"
hermes cron remove <job-id>      # stop watching
```

From a chat, the same lifecycle is plain language: "pause the PR watcher", "run it now".

## Manual Use

Run the watcher by hand (from the installed skill directory or the repo copy). Manual runs
never deliver anything by themselves — only the cron job sends messages:

```bash
python3 scripts/pr_watch.py --dry-run     # preview: shows what would be sent, changes no state
python3 scripts/pr_watch.py --json        # full snapshot of open PRs + CI states, as JSON
python3 scripts/pr_watch.py --verbose --dry-run
```

```powershell
python scripts\pr_watch.py --dry-run
```

`--dry-run` prints the would-be message to stderr (prefixed `[dry-run]`) and leaves the
state file alone; when nothing changed it says so. `--json` is read-only and is the right
tool for "what's up with the arena PRs?" questions — run it and summarize, changing
nothing. A normal run (what cron invokes) prints the message to stdout and updates the
state file.

## Example Message

```
httpurax/arena: 2 PR updates

✅ #42 all checks green — ready to merge
   Fix the flaky test in the installer self-test
   fix/installer-flaky-test
   checks: all 12 checks passed
   https://github.com/httpurax/arena/pull/42

🆕 #44 opened — all checks green
   Add rate limiting
   feat/rate-limit
   checks: all 5 checks passed
   https://github.com/httpurax/arena/pull/44
```

A failing PR reads `❌ #43 checks failing`, with its `checks:` line showing
`checks: 2 of 9 checks failed`.

## Troubleshooting

- **Silent, but a PR obviously went green** — the state file may be missing or stale (a
  re-baseline consumes a transition). Find the state file for the run in question (under
  the script's parent directory, `data/pr-state.json`) and compare its `checks` values
  with the PR's actual CI.
- **An error alert on every tick** — usually `gh` auth. In a shell with the same
  environment as the Hermes process, run `gh auth status`; re-login if needed.
- **No Telegram delivery while the job is healthy** — no-agent stdout goes to the
  profile's Telegram home channel; confirm the install has Telegram set up with a home
  channel.

## Completion Checklist

Before saying the watch is set up:

- `hermes cron list` shows `arena-pr-watcher`: `every 30m`, no-agent, Telegram delivery.
- One `hermes cron run <job-id>` (or a manual `--dry-run`) completes with exit status 0.
- The state file exists and holds only public PR metadata; `git status` in the repo shows
  nothing new to commit (the state file is ignored).
- No token, bot credential, or private data appears in the skill, the state file, or any
  message.
- Nothing was merged or modified: the skill is notify-only.
