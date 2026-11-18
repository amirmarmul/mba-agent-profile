# Website Knowledge Crawl Status

When submitting a URL via `python3 scripts/mba_websites.py create`, Meta's asynchronous crawler indexes the page. You can monitor the progress via `python3 scripts/mba_websites.py list`.

## 1. Status Enums (`crawl_status`)
The API returns one of four statuses:
- **`pending`**: The URL is queued for indexing but the crawler hasn't started yet.
- **`in_progress`**: The crawler is actively fetching and processing the URL's content.
- **`completed`**: The index is built and the knowledge is now actively available to the Meta Business Agent.
- **`failed`**: The crawler encountered an error (e.g., HTTP 403, 404, captcha block, or timeout).

## 2. Evaluating Crawl Success
Pay attention to the `pages_crawled` metric:
- A `completed` status with `pages_crawled > 0` is the ideal success state.
- A status of `completed` but `pages_crawled: 0` often indicates a soft failure (e.g., the crawler hit a client-side rendered page it couldn't parse, or an invisible redirect).

## 3. The "Stuck in Progress" Anomaly
It is common for URLs to get stuck in `in_progress` with `pages_crawled: 0` indefinitely, even if the URL returns HTTP 200 in a browser.

**Resolution Protocol**:
1. Do not assume the URL is broken.
2. Wait a reasonable amount of time (10-15 minutes).
3. If still stuck, execute a manual reset:
   - `python3 scripts/mba_websites.py delete <id> --yes`
   - `python3 scripts/mba_websites.py create --body-file <payload_path>`