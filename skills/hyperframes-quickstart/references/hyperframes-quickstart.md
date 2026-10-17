# HyperFrames Quickstart Reference

## What HyperFrames Is

HyperFrames is HeyGen's open-source "video as code" framework (Apache 2.0). You
write HTML, CSS, and JavaScript; HyperFrames renders it to a deterministic MP4
using headless Chrome and FFmpeg. Local rendering is free and does not require an
account or credits. The framework is also usable from AI coding agents through
its skills.

## Requirements

- Node.js 22 or newer.
- FFmpeg.
- The CLI drives a headless Chrome and FFmpeg pipeline. Verify the exact browser
  and platform requirements on github.com/heygen-com/hyperframes if anything is
  unclear.

## Scaffold a Project

```bash
npx hyperframes init my-video
cd my-video
```

The root `index.html` is rendered by default.

## First Composition

This is the smallest renderable standalone composition from the upstream
HyperFrames core skill:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Minimal HyperFrames Composition</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      body {
        margin: 0;
        background: #0b0f14;
        color: white;
        font-family: Inter, system-ui, sans-serif;
      }
      #root {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
      }
      .clip {
        position: absolute;
        inset: 0;
        display: grid;
        place-items: center;
      }
      h1 {
        margin: 0;
        font-size: 96px;
      }
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-width="1920"
      data-height="1080"
      data-duration="5"
    >
      <section id="title-card" class="clip" data-start="0" data-duration="5">
        <h1 id="title">Hello HyperFrames</h1>
      </section>
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      tl.from("#title", { y: 48, opacity: 0, duration: 0.6, ease: "power3.out" }, 0.2);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
```

Key points:

- The root `<div>` carries `data-composition-id`, `data-width`, and
  `data-height`.
- `data-duration` sets the render length.
- Timed elements carry `data-start` and a duration.
- One paused GSAP timeline is registered on
  `window.__timelines["<composition-id>"]`.

## Preview and Render

Run the local loop from the project folder:

```bash
npx hyperframes lint
npx hyperframes check
npx hyperframes preview --background
npx hyperframes render --output final.mp4
```

- `lint` checks project structure.
- `check` opens the project in a browser and checks runtime, layout, motion,
  media, and contrast problems.
- `preview --background` keeps a preview server running.
- `render --output final.mp4` writes an MP4. If `--output` is omitted, the
  result is written under `renders/`.

## Agent Skills

Install the published HyperFrames skills:

```bash
npx skills add heygen-com/hyperframes
```

Choose **Core Skills** in the picker. For non-interactive or agent runs:

```bash
npx hyperframes skills update
```

For Claude Code:

```bash
claude plugin marketplace add heygen-com/hyperframes
claude plugin install hyperframes@hyperframes
```

## Common Workflow

```bash
npx hyperframes lint
npx hyperframes check
npx hyperframes preview --background
npx hyperframes render --output final.mp4
test -s final.mp4
```

## Uncertain Details

This guide intentionally avoids unverified flags, URLs, and version numbers. For
anything not listed here, verify on github.com/heygen-com/hyperframes.
