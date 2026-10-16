---
name: hyperframes-quickstart
description: Render HTML/CSS/JS to MP4 video with HyperFrames.
version: 1.0.0
author: httpurax
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: development
---

## Overview

HyperFrames is HeyGen's open-source (Apache 2.0) "video as code" framework: you write a
composition in plain HTML/CSS/JS, and it renders a deterministic MP4 with headless Chrome
and FFmpeg. Local rendering is free, needs no account, and consumes no HeyGen credits,
which makes it a good fit for scripted, faceless video pipelines.

Source of truth for anything version-specific: <https://github.com/heygen-com/hyperframes>.

## When to Use

- Starting a first HyperFrames project: scaffold, write a composition, preview, render an MP4.
- Turning an HTML/CSS animation or a written script into video, or scripting video from a pipeline.
- Installing the HyperFrames agent skills (`npx skills add heygen-com/hyperframes`).

## When NOT to Use

- Other renderers (Remotion, Motion Canvas, …). Upstream ships a one-way
  `/remotion-to-hyperframes` port, but this skill does not cover it.
- Hosted rendering, avatars, or paid media generation — those are optional upstream paths.
- Timeline editing of existing footage; HyperFrames is code-first, not an NLE.

## Prerequisites

1. Node.js 22 or newer.
2. FFmpeg on `PATH`.
3. Nothing else: the CLI runs through `npx hyperframes`, so there is no global install,
   no account, and no API key.

```bash
node --version     # v22 or newer
ffmpeg -version
```

The commands in this skill are plain `npx` invocations, so they are identical in bash,
PowerShell, and cmd.

## Quick Start

```bash
npx hyperframes init my-video
cd my-video
npx hyperframes preview   # local browser preview with live reload
npx hyperframes render    # renders the project to MP4
```

Then the edit loop: `npx hyperframes lint` after each HTML pass, `npx hyperframes check`
as the gate before a render, and a quality tier per purpose:

```bash
npx hyperframes render --quality draft                    # fast iteration
npx hyperframes render --quality looks --output out.mp4    # first real encode
npx hyperframes render --quality delivery --output out.mp4 # final delivery
```

## Agent Skills

```bash
npx skills add heygen-com/hyperframes   # picker: choose "Core Skills"
```

The picker is interactive and pre-selects nothing; a non-interactive or agent run without
`--skill` installs the whole published set instead. Agents should prefer
`npx hyperframes skills update`, which installs exactly the core set from `main` — the
skills registry can lag `main` by hours. Claude Code can install the versioned plugin
instead: `claude plugin marketplace add heygen-com/hyperframes`, then
`claude plugin install hyperframes@hyperframes`.

Once installed, the `/hyperframes` router picks a workflow for a request. The one that maps
to a faceless pipeline is `/faceless-explainer` (topic from arbitrary text, every visual
LLM-invented, no product or URL needed).

## Composition Contract (the short version)

A composition is one HTML file: a sized root (`data-composition-id`, `data-width`,
`data-height`, `data-duration`), timed `.clip` elements (`data-start` plus a duration), and
exactly one paused GSAP timeline registered at `window.__timelines["<composition-id>"]`
where the key matches the root's `data-composition-id`. No render-time clocks, unseeded
randomness, network calls, or input state. The full skeleton, determinism rules, and the
first-pass lint failures: [references/hyperframes-quickstart.md](references/hyperframes-quickstart.md).

## Guardrails

- Never invent commands, flags, or URLs. Anything not confirmed here is marked
  "verify on github.com/heygen-com/hyperframes" — check upstream before relying on it.
- A passing `check` does not certify the pixels: watch the preview, then confirm the output
  file exists, is non-empty, and its duration matches the root `data-duration`
  (`ffprobe -v error -show_format -show_streams out.mp4`).
- Local rendering is free and account-free. The hosted paths (`cloud render`, `lambda`,
  `cloudrun`) are optional, credit- or cloud-billed, and out of scope here.
- Diagnose the environment with `npx hyperframes doctor` before debugging a render.

## Next Steps

- [references/hyperframes-quickstart.md](references/hyperframes-quickstart.md): install and
  requirements, a first composition in HTML, preview and render, agent skills, determinism
  rules, and troubleshooting.
