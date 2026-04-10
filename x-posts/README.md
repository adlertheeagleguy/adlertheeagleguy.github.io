# x-posts

Static site generator for `../stuff/bookmarks.jsonl`.

Run:

```bash
python3 x-posts/build.py
```

What it does:

- parses the bookmark export even when the source is concatenated JSON rather than clean JSONL
- assigns each bookmark to a context-aware folder and writes that `folder` field back into `stuff/bookmarks.jsonl`
- emits a static site in `x-posts/` with a landing page, per-folder pages, and browser-side search
- renders video bookmarks as poster-image cards with a play-link overlay instead of trying to embed inline playback
