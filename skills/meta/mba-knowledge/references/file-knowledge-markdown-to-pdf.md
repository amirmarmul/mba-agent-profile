# File Knowledge upload note

## Durable lesson

MBA File Knowledge API may reject Markdown and plain-text clipping uploads as unsupported file types even when the content itself is valid reference material.

## Observed API behavior

- `python3 scripts/mba_files.py upload <path>.md --name ...` returned HTTP 400 `Unsupported File Type`.
- `python3 scripts/mba_files.py upload <path>.txt --name ...` returned the same HTTP 400.
- After converting the same content to PDF, `python3 scripts/mba_files.py upload <path>.pdf --name ...` succeeded.

## Working pattern

1. Keep user-provided clipping or transcript as source text locally.
2. Convert the source document into PDF.
3. Upload the PDF with `python3 scripts/mba_files.py upload /path/to/file.pdf --name "..."`.
4. Verify with `python3 scripts/mba_files.py list`.
5. Log uploaded filenames and returned file IDs in `workspace/<ENTITY_ID>/changelog/history.md`.

## Why this matters

This keeps official website clippings, transcripts, and audit notes usable as File Knowledge even when the API does not accept `.md` or `.txt` directly. It also provides stable grounding when Website Knowledge crawl is incomplete or still shows `pages_crawled: 0`.

## Session example class

Aptana/Kuponku website clippings were accepted only after conversion from Markdown to PDF, then showed up correctly in `python3 scripts/mba_files.py list`.
