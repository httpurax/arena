---
name: hyperframes-quickstart
description: HyperFrames HTML-to-MP4 video quickstart.
version: 1.0.0
author: httpurax
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: development
---

## Overview

HyperFrames is HeyGen's open-source "video as code" framework (Apache 2.0). You write a
composition in HTML, CSS, and JavaScript; HyperFrames renders it to a deterministic MP4
with headless Chrome and FFmpeg. It runs locally, is free, and needs no account for local
rendering. Optional hosted, voice, avatar, or generated-media services may have their own
costs.

This skill gets a first composition rendering. For deeper animation, catalog blocks,
rendering options, and troubleshooting, use
[references/hyperframes-quickstart.md](references/hyperframes-quickstart.md).

## When to Use

- The user wants a faceless or HTML-authored video pipeline.
- Creating, previewing, linting, or rendering a HyperFrames composition.
- Installing HyperFrames or its agent skills.
- Converting an `index.html` composition into `output.mp4`.

## When NOT to Use

- General web page authoring with no video/render goal.
- Remotion/React video projects; HyperFrames uses plain HTML.
- Cloud rendering, AWS Lambda, or Google Cloud Run setup; check the upstream docs.

## Prerequisites

1. Node.js 22 or newer (the `hyperframes` package requires `node >=22`).
2. A working internet connection for the first `npx` run.
3. Run `npx hyperframes doctor` to check the machine and installed tools.

## Quick Start

```bash
npx hyperframes init my-video
cd my-video
```

Edit `index.html`, then preview and render:

```bash
npx hyperframes preview
npx hyperframes lint
npx hyperframes check
npx hyperframes render --output output.mp4
```

If you omit `--output`, HyperFrames writes the result under `renders/`.

## First Composition

A composition is an HTML file with data attributes for timing and tracks:

```html
<div id="stage" data-composition-id="launch" data-start="0" data-width="1920" data-height="1080">
  <h1 id="title" class="clip" data-start="1" data-duration="4" data-track-index="1">Launch day</h1>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.from("#title", { opacity: 0, y: 40, duration: 0.8 }, 1);
    window.__timelines = window.__timelines || {};
    window.__timelines.launch = tl;
  </script>
</div>
```

Use `data-start`, `data-duration`, and `data-track-index` for clips. Seekable timelines must be
registered on `window.__timelines`.

## Agent Skills

Install HyperFrames skills for coding agents:

```bash
npx skills add heygen-com/hyperframes
```

Choose **Core Skills** in the picker. For non-interactive or agent runs, use:

```bash
npx hyperframes skills update
```

The `/hyperframes` skill is the router and capability map for video creation workflows.

## Common Commands

| Task | Command |
|---|---|
| Create a project | `npx hyperframes init my-video` |
| Open preview/Studio | `npx hyperframes preview` |
| Check HTML structure | `npx hyperframes lint` |
| Run browser/layout/motion checks | `npx hyperframes check` |
| Render MP4 | `npx hyperframes render --output output.mp4` |
| Diagnose machine | `npx hyperframes doctor` |

## Guardrails

- Do not invent HyperFrames commands, flags, or URLs; verify uncertain details at
  `github.com/heygen-com/hyperframes`.
- Keep compositions as plain HTML; no build step is required for `index.html`.
- Run `lint` and `check` before rendering when changing timing or media.
- Local rendering uses no HeyGen credits, but agents or optional services may cost money.

## Next Steps

- Streaming, rendering options, formats, and troubleshooting:
  [references/hyperframes-quickstart.md](references/hyperframes-quickstart.md).
