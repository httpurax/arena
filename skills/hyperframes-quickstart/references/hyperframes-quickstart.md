# HyperFrames Quickstart Reference

## What HyperFrames Is

HyperFrames turns HTML, CSS, media, and seekable animations into deterministic MP4
videos. Compositions are HTML files with data attributes. The renderer seeks each frame in
headless Chrome and encodes with FFmpeg, so the same input produces the same output.

License: Apache 2.0. No per-render fees or commercial-use thresholds for local rendering.

## Install and Prerequisites

- Node.js 22 or newer.
- First run downloads/runs the CLI through `npx`.

Create a project:

```bash
npx hyperframes init my-video
cd my-video
```

Check the machine:

```bash
npx hyperframes doctor
```

## First Composition

Save this as `index.html` in the project folder:

```html
<div id="stage" data-composition-id="launch" data-start="0" data-width="1920" data-height="1080">
  <video
    class="clip"
    data-start="0"
    data-duration="6"
    data-track-index="0"
    src="intro.mp4"
    muted
    playsinline
  ></video>

  <h1 id="title" class="clip" data-start="1" data-duration="4" data-track-index="1">Launch day</h1>

  <audio
    data-start="0"
    data-duration="6"
    data-track-index="2"
    data-volume="0.5"
    src="music.wav"
  ></audio>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.from("#title", { opacity: 0, y: 40, duration: 0.8 }, 1);
    window.__timelines = window.__timelines || {};
    window.__timelines.launch = tl;
  </script>
</div>
```

## Preview

```bash
npx hyperframes preview
```

Preview proves the project can play. It does not prove the final exported file is correct.

## Validate

```bash
npx hyperframes lint
npx hyperframes check
```

`lint` checks project structure. `check` opens the project in a browser and looks for
runtime, layout, motion, media, and contrast problems.

## Render to MP4

```bash
npx hyperframes render --output output.mp4
```

If you omit `--output`, HyperFrames writes the result under `renders/`.

Useful variants:

```bash
npx hyperframes render --quality draft --output review.mp4
npx hyperframes render --quality high --output master.mp4
npx hyperframes render --fps 60 --output final-60fps.mp4
```

Render another composition:

```bash
npx hyperframes render --composition compositions/intro.html --output intro.mp4
```

## Agent Skills

Install standalone skills:

```bash
npx skills add heygen-com/hyperframes
```

Choose **Core Skills** in the picker. For non-interactive or agent runs:

```bash
npx hyperframes skills update
```

For Claude Code plugin installation, see the upstream plugin guide; commands and update
settings may change, so verify on `github.com/heygen-com/hyperframes`.

## Common Troubleshooting

```bash
npx hyperframes doctor
npx hyperframes lint
npx hyperframes check
```

Keep the first exact error rather than only the final "render failed" message.

## Notes

- HyperFrames is free and open-source; local rendering does not use HeyGen credits.
- Your coding agent and optional hosted, voice, avatar, or generated-media services may
  have their own costs.
- Catalog blocks can be added with `npx hyperframes add <name>`; verify exact block names
  in the upstream catalog.
- Commands and flags can change between versions. Run `npx hyperframes <command> --help`
  and verify uncertain details on `github.com/heygen-com/hyperframes`.
