# Handling YouTube Videos in Moodle

When Moodle courses link to YouTube videos, use the `youtube-content` skill to fetch transcripts and convert them into useful formats (chapters, summaries, threads, blog posts).

## Workflow

1. **Fetch the transcript** using the `youtube-content` skill.
2. **Validate** the output is non-empty and in the expected language.
3. **Transform** the transcript into the requested output format.
4. **Save the transformed content** to the course folder and update the course note with a link to the file.

## Example

```bash
python SKILL_DIR/scripts/fetch_transcript.py "https://youtu.be/VIDEO_ID" --text-only --timestamps
```

## Output Formats

- **Chapters**: Group by topic shifts, output timestamped chapter list
- **Summary**: Concise 5-10 sentence overview of the entire video
- **Chapter summaries**: Chapters with a short paragraph summary for each
- **Thread**: Twitter/X thread format — numbered posts, each under 280 chars
- **Blog post**: Full article with title, sections, and key takeaways
- **Quotes**: Notable quotes with timestamps

## Downloading the video file itself

`fetch_transcript.py` produces text only. When the vault needs the actual media, use `yt-dlp`:

```bash
yt-dlp -f "bv*+ba/b" --merge-output-format mp4 --js-runtimes node \
  -o "<Meaningful Title>.%(ext)s" "https://youtu.be/<VIDEO_ID>"
```

- **Always pass `--js-runtimes node`.** Without a JS runtime yt-dlp cannot solve YouTube's player challenge and the stream request fails — `HTTP Error 403` on the m3u8, an "n challenge solving failed" warning, or a format list containing only images. Node ships with the Hermes toolchain, so the fix is the flag rather than an install.
- **A 403 on the first attempt can be transient** — retry once before declaring the video unavailable.
- **Verify with `ffprobe`**: a merged mp4 carrying both a video and an audio stream, with a duration matching what the source page reports, is the success signal.
- **Name the file from the video title**, never the video id, so the vault stays browsable.

## Error Handling

- **Transcript disabled**: tell the user; suggest they check if subtitles are available on the video page.
- **Private/unavailable video**: relay the error and ask the user to verify the URL.
- **No matching language**: retry without `--language` to fetch any available transcript, then note the actual language to the user.
- **Dependency missing**: repeat PM preparation and reactivation above, then verify the helper uses that Python. Do not repair the selected generation with pip.
