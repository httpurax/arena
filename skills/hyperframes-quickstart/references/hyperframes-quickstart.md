# HyperFrames Quickstart Reference

Checked against the HyperFrames project on 2026-10-16 (repo `heygen-com/hyperframes`,
Apache-2.0; npm package `hyperframes`, `latest` was `0.8.165` that day). HyperFrames ships
frequently — the five CLI commands below are stable, but for anything else that does not
match this page, **verify on github.com/heygen-com/hyperframes** before trusting it.

## 1. What HyperFrames Is

- An open-source (Apache 2.0) framework by HeyGen: "Write HTML. Render video. Built for agents."
- A **composition** is an HTML file. The DOM declares timing with `data-*` attributes, the
  animation runtime is seekable, and media playback is owned by the framework.
- **Rendering is file-to-file and deterministic**: headless Chrome seeks the timeline frame
  by frame, FFmpeg encodes the frames into an MP4. The same input renders the same video,
  which is what makes it usable in an automated pipeline.
- **Free and local**: no account, no API key, no credits. Upstream docs state that local
  rendering does not use HeyGen credits; even catalog search is entirely local.
- It is **not an editor**: review happens in the browser preview or the desktop Studio app,
  and changes happen in the HTML/CSS/JS source.

Good fits: explainers written from a script, product and PR videos, motion graphics,
data visualization, captioned social clips, and batch/automated video from a data file.

## 2. Install and Requirements

| Requirement | Notes |
|---|---|
| Node.js 22+ | the CLI refuses older Node; run `node --version` first |
| FFmpeg on `PATH` | `ffmpeg -version`; it does the encoding |
| Nothing else | no global install, no login, no package.json of your own |

```bash
npx hyperframes init my-video     # scaffolds the project folder
npx hyperframes doctor            # checks Node, FFmpeg, and the render browser
```

`npx hyperframes <command>` downloads and runs the current CLI on first use; there is no
separate install step. Run `npx hyperframes --help` (or `--json` where offered) to see the
current surface, since new commands land often.

Optional, for agents rather than humans: install the skills (section 5) or, in Claude Code,
the versioned plugin:

```bash
claude plugin marketplace add heygen-com/hyperframes
claude plugin install hyperframes@hyperframes
```

## 3. A First Composition in HTML

`npx hyperframes init my-video` scaffolds a project whose entry point is `index.html`. The
smallest renderable composition — adapted from upstream's own minimal-composition
reference — looks like this:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Minimal HyperFrames Composition</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      body { margin: 0; background: #0b0f14; color: white; font-family: Inter, system-ui, sans-serif; }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; }
      .clip { position: absolute; inset: 0; display: grid; place-items: center; }
      h1 { margin: 0; font-size: 96px; }
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

What the runtime actually requires:

- **Root**: a `<div>` with `data-composition-id`, `data-width`, `data-height`. The canvas
  size comes from those attributes — size the root `width`/`height: 100%`, never hardcode
  `1920px`/`1080px` on it. A duration source is needed as well: root `data-duration` (above),
  or something the CLI can infer (a timeline, media, or an adapter).
- **Clips**: an element becomes a clip when it carries `data-start` plus a duration.
  `class="clip"` is the layout and tooling convention; `data-track-index` is only a Studio
  display lane, not a timing constraint.
- **One paused timeline**: create exactly one `gsap.timeline({ paused: true })` and register
  it at `window.__timelines["<composition-id>"]`, where the key equals the root's
  `data-composition-id`. The runtime creates the registry before your inline scripts run.
  Build the timeline inside `document.fonts.ready` if needed, but register it only after the
  build completes. Render length comes from the root `data-duration`, not the timeline: a
  timeline that runs long is cut off, one that ends early holds its last frame.

Sub-compositions (files loaded through `data-composition-src`) are the same shape but wrap
the root in `<template>`; the module form is not interchangeable with the standalone one.

## 4. Preview and Render to MP4

The loop, in order:

```bash
npx hyperframes lint                    # fast feedback after each HTML pass
npx hyperframes check                    # the gate: lint + runtime, layout, motion, contrast
npx hyperframes snapshot --at 1,3,4.5    # spot-check frames without a full render
npx hyperframes preview --background     # serve the live preview; keep it up for review
npx hyperframes render --quality draft --output draft.mp4
```

- `lint` findings are per-rule and name the offending element; fix them before trusting
  anything else, because a lint **error** also disables the layout and contrast audits —
  `check` then reports `0 sample(s)` and `0/0 text checks`, which looks clean but means
  nothing ran.
- `preview --background` keeps serving after the command returns, so the reviewer can scrub
  the timeline while you keep editing.
- Quality tiers: `--quality draft` for iteration, `--quality looks` for the first real
  encode (the CLI default), `--quality delivery` for the final file. `--output <file.mp4>`
  names the artifact.
- After a render, read the summary's second line: `beginframe` is the fast path,
  `screenshot` plus `software gpu` on Linux is the slow one.
- Verify the artifact, not just the exit code:

```bash
ffprobe -v error -show_format -show_streams out.mp4
```

its duration should match the root `data-duration`, and the picture should match what the
preview showed at the same timestamps.

For a pipeline, one render per row of a data file avoids writing HTML per video:

```bash
npx hyperframes render --batch rows.json --output "renders/{name}.mp4"
```

If a long render is killed by a tool that tears down its whole process group, upstream
documents starting it detached with `HYPERFRAMES_RENDER_DETACHED=1` — verify on
github.com/heygen-com/hyperframes for the current recipe.

## 5. Agent Skills

Standalone (any agent that reads skills — Claude Code, Codex, Cursor, Gemini CLI, and
others):

```bash
npx skills add heygen-com/hyperframes   # interactive picker: choose "Core Skills"
```

- The picker opens with nothing pre-selected, and the **Core Skills** group is all you need:
  the `/hyperframes` router installs each creation workflow on demand. A non-interactive run
  without `--skill` installs all of the published skills instead, so agents should use:

```bash
npx hyperframes skills update
```

which installs exactly the core set, from the current `main`. The registry that plain
`skills add` resolves can lag `main` by hours, so prefer this when you need the newest copy.

- The **core set** is the `/hyperframes` router, the `hyperframes-*` domain skills
  (core, animation, keyframes, creative, cli, audio, registry) and `media-use`; the creation
  workflows install on demand when the router runs one.
- Workflows relevant here: `/faceless-explainer` (a topic from arbitrary text, no product or
  URL — the faceless pipeline default), `/product-launch-video`, `/pr-to-video`,
  `/motion-graphics`, `/music-to-video`, `/embedded-captions`, `/talking-head-recut`,
  `/slideshow`, and `/general-video` as the catch-all.
- Before hand-writing motion, search the local block catalog and install what fits:
  `npx hyperframes catalog --query "reveal a headline one line at a time"`, then
  `npx hyperframes add <name>`. Search runs locally and sends nothing anywhere.
- `/media-use` resolves music, SFX, images, and voiceover into frozen local files, which is
  where a faceless pipeline gets its audio bed.

## 6. Faceless Pipeline Sketch

1. Write or generate the script (one row per video if batched).
2. Let the agent run `/faceless-explainer`; it plans, writes the composition HTML, wires
   seekable animation, and adds media through `/media-use`.
3. Gate: `lint` → `check` → `snapshot` at the beat boundaries → `preview --background`.
4. Review the preview before spending a full encode; iterate at `--quality draft`.
5. Final: `--quality delivery` (or `--batch rows.json`) and verify each file with `ffprobe`.

Determinism is the feature that makes this repeatable: re-rendering an unchanged project
produces the same frames, so diffs after an edit mean exactly what they look like.

## 7. Determinism Rules and First-Pass Lint Failures

Non-negotiable (silent bugs, not always caught):

- No render-time clocks, no unseeded `Math.random`, no network requests, no input state.
  `repeat: -1` is only safe under a finite root `data-duration`.
- Never animate `display`, `visibility`, or `autoAlpha` on a `.clip` — the framework owns
  clip visibility (`lint`: `gsap_animates_clip_element`). Animate a child instead.
- No `<br>` in body text; keep `id`s unique across the assembled page (prefix sub-composition
  ids, e.g. `#scene-1-hero`).

First-pass failures the linter names outright:

| Rule | Trigger | Fix |
|---|---|---|
| `gsap_css_transform_conflict` | a CSS initial `transform` plus a GSAP tween of the same property | set the start state in the tween: `gsap.fromTo(el, { x: -40 }, { x: 0 })` |
| `media_crossorigin_breaks_preview` | `crossorigin` on `<video>`/`<audio>` | remove it; there is no suppression |
| `media_missing_id` | an `<audio>` without an `id` | give every audio element an `id`, or the render is silent |
| `video_nested_in_timed_element` | a `<video data-start>` inside a plain element that also has `data-start` | put the timing on the wrapper or the video, never both |
| `font_family_without_font_face` | a named CSS `font-family` with no in-file `@font-face` | ship the font file and declare it, or use system fonts |

## 8. Troubleshooting Pointers

| Symptom | First move |
|---|---|
| Render will not start | `npx hyperframes doctor` (Node, FFmpeg, browser) |
| Very slow render | check the summary for `screenshot` + `software gpu`; try `--quality draft`, and close other GPU users |
| Silent MP4 | an `<audio>` is missing its `id` (`media_missing_id`) |
| Clean `check`, ugly frames | a lint error disabled the layout/contrast audits — clear lint errors, rerun `check`, then look at `snapshot` frames |
| Clip vanishes or shows wrong source frames | a `<video data-start>` is nested inside another timed plain element |
| Clip cut short in the MP4 | the clip ends past the root `data-duration`; extend the root in the same edit |

## 9. What Is Verified Here vs. What to Re-Check

Verified on 2026-10-16 against the upstream README, `docs/quickstart.mdx`, and the
`hyperframes-core` / `hyperframes-cli` skills: the prerequisites, `npx hyperframes`
`init` / `preview` / `render` / `lint` / `check` / `snapshot` / `doctor` / `catalog` / `add` /
`timeline`, the quality tiers, the composition contract, the determinism rules and lint rule
names, the skills install commands, and the workflow list.

Version-dependent — **verify on github.com/heygen-com/hyperframes** before relying on them:
exact package versions, newer or renamed commands and flags, the size of the catalog and the
skills registry, cloud/AWS/GCP rendering paths, Studio and desktop-app details, and any
model- or TTS-backed media generation.

Upstream is Apache-2.0 (`LICENSE` in the repo). These notes are this repo's own MIT-licensed
summary.
