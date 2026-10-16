---
name: hyperframes-quickstart
description: Quick start for HyperFrames HTML-to-MP4 video.
version: 1.0.0
author: httpurax
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: development
---

## Overview

HyperFrames is HeyGen's open-source "video as code" framework (Apache 2.0): write
HTML, CSS, and JavaScript, then render a deterministic MP4 locally with headless
Chrome and FFmpeg. Local rendering is free and needs no account or credits. This
skill gets a first composition running and points to
[references/hyperframes-quickstart.md](references/hyperframes-quickstart.md) for
the full first-project loop.

## When to Use

- The user wants to make a video from HTML/CSS/JS with HyperFrames.
- Installing or scaffolding a HyperFrames project.
- Writing, previewing, linting, checking, or rendering a first composition.
- Installing HyperFrames agent skills.

## When NOT to Use

- Deep animation, GSAP, sub-compositions, audio, or cloud rendering details; use
  the upstream HyperFrames skills and docs.
- Non-HyperFrames video tools or hosted renderers.

## Prerequisites

- Node.js 22 or newer and FFmpeg. If unsure about the current requirement, verify
  on github.com/heygen-com/hyperframes.
- No account is needed for local rendering.

## Quick Start

Scaffold a project:

```bash
npx hyperframes init my-video
cd my-video
```

```powershell
npx hyperframes init my-video
cd my-video
```

Replace `index.html` with the minimal composition from the reference guide, then
run the local loop:

```bash
npx hyperframes lint
npx hyperframes check
npx hyperframes preview --background
npx hyperframes render --output final.mp4
```

```powershell
npx hyperframes lint
npx hyperframes check
npx hyperframes preview --background
npx hyperframes render --output final.mp4
```

If `--output` is omitted, HyperFrames writes the result under `renders/`.

## Agent Skills

Install the HyperFrames skills for a coding agent:

```bash
npx skills add heygen-com/hyperframes
```

Choose **Core Skills** in the interactive picker. For a non-interactive or agent
run, use:

```bash
npx hyperframes skills update
```

For Claude Code, the plugin route is:

```bash
claude plugin marketplace add heygen-com/hyperframes
claude plugin install hyperframes@hyperframes
```

## Guardrails

- Run commands through `npx hyperframes ...`; do not assume a global install.
- Keep `npx hyperframes check` green before trusting preview or render output.
- Do not invent URLs, flags, or version numbers. Verify anything uncertain on github.com/heygen-com/hyperframes.

## Next Steps

- Full first-project loop, minimal composition, preview, and render:
  [references/hyperframes-quickstart.md](references/hyperframes-quickstart.md).
