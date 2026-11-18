# File Knowledge intake from user-provided website clippings

## When to use
- User sends website clippings, markdown exports, or copied source documents.
- Goal is to store them in MBA File Knowledge for grounding.

## Workflow
1. Preserve original clipping files locally for audit trail.
2. Try direct upload only if file type is known-supported.
3. If API returns `Unsupported File Type` for `.md` or `.txt`, convert source text to PDF.
4. Upload the generated PDF via `python3 scripts/mba_files.py upload /path/to/file.pdf --name "...pdf"`.
5. Verify with `python3 scripts/mba_files.py list`.
6. Log conversion reason and uploaded file names in `mba/<ENTITY_ID>/changelog/history.md`.

## Pitfalls
- Do not assume markdown exports are valid File Knowledge uploads.
- Name collisions can return `409 Duplicate File`; verify existing inventory before retrying.
- Keep source URL/context in the original clipping text or PDF body so provenance stays inspectable.
