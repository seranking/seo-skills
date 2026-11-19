file: skills/seo-technical-audit/SKILL.md
=== find
## Core Web Vitals (field data — CrUX)

| Metric | p75 (current) | 25-week trend | Threshold | Status |
|---|---|---|---|---|
| LCP | {n} ms | {improving/stable/degrading} | ≤2500 ms good · ≤4000 ms needs improvement | {pass/warn/fail} |
| INP | {n} ms | … | ≤200 ms good · ≤500 ms needs improvement | … |
| CLS | {n} | … | ≤0.1 good · ≤0.25 needs improvement | … |
| FCP | {n} ms | … | ≤1800 ms good · ≤3000 ms needs improvement | … |
| TTFB | {n} ms | … | ≤800 ms good · ≤1800 ms needs improvement | … |

Source: CrUX 28-day origin. If insufficient field data: "CrUX: insufficient data for {domain} (low-traffic origin)."
(Or: `CWV (field data): not configured — run `bash extensions/google/install.sh` for setup.`)

## Indexation reality check (GSC URL Inspection)

| URL | Status | userCanonical → googleCanonical | Last crawled |
|---|---|---|---|
| {top-traffic URL 1} | {INDEXED|EXCLUDED|...} | {URL} {→ different URL if divergent} | {YYYY-MM-DD} |
| {top-traffic URL 2} | … | … | … |
| ... |

Source: GSC URL Inspection (Tier 1). If property not verified: "GSC: {domain} not verified — add it in Search Console."
(Or: `Indexation reality check: not configured (Tier 1 setup required).`)
=== replace
## Core Web Vitals (field data) and indexation reality check

`CWV (field data) and GSC URL Inspection: not available in this edition.` Use SE Ranking's lab CWV from the audit above; don't estimate field-data values.
