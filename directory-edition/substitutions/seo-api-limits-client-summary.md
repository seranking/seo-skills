file: skills/seo-api/references/rate-limits-and-credits.md
=== find
This handles the common cases: rate-limit pacing, exponential backoff with jitter, terminal 403, transient 5xx. Tune `rps` to match the API (5 for Project, 10 for Data).
=== replace
A production client should cover rate-limit pacing, exponential backoff with jitter, a terminal 403 and transient 5xx, and pace at 5 requests per second for the Project API and 10 for the Data API.
