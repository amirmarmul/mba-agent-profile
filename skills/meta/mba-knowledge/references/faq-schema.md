# FAQ Schema Constraints

When modifying FAQs via `mba_faq.py`, observe these constraints.

## Fields
- `question` (string, required): The prompt representing what a user might ask. Must be definitive. Max 1024 chars.
- `answer` (string, required): The exact answer. Must be clear, short, and policy-accurate. Max 20000 chars.
- `metadata` (object, optional):
  - `source` (string): Helpful for tracking origin (e.g., `official-website`, `sales-team`). Max 256 chars.

## Best Practices
- Do not upload generic or ambiguous FAQs (e.g., Question: "Price?", Answer: "Depends").
- Expand the question to reflect intent: "How much does the service cost?" and provide a bounded answer or a clear path to get a quote.