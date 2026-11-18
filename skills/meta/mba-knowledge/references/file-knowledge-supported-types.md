# File Knowledge Supported Types and Limits

When uploading documents to the Meta Business Agent via `python3 scripts/mba_files.py upload`, strictly follow these limits. 

## 1. File Size Limits
- **Maximum File Size**: 100,000,000 bytes (~100 MB).
- Ensure the payload is optimized. Large PDFs with unoptimized images may hit timeouts even if technically under the byte limit.

## 2. Supported Extensions
The Meta API explicitly accepts the following file types:
- `.pdf`
- `.doc`
- `.docx`
- `.png`
- `.jpg`
- `.jpeg`

## 3. Conditionally Supported Extensions
- `.csv`: Only supported if CSV extraction is explicitly enabled for the WhatsApp asset by Meta.
- `.xlsx`: Only supported if XLSX extraction is explicitly enabled.

## 4. Unsupported Extensions (Pitfalls)
- `.md` (Markdown)
- `.txt` (Plain text)
**Workaround**: Convert any Markdown or Text files into a clean PDF before uploading. (Refer to `file-knowledge-markdown-to-pdf.md`).

## 5. Security & Content Checks
- Ensure uploaded files contain official, up-to-date business logic. 
- Avoid uploading internal drafts, conflicting pricing charts, or temporary promotion files without a plan to remove them later, as the Agent considers all uploaded files as equal sources of truth.