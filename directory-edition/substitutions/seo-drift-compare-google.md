file: skills/seo-drift/SKILL.md
=== find
   - **Google-data drift** *(only if both snapshots have Google fields)*:
     - LCP p75 increased ≥20% → red.
     - INP p75 increased ≥20% → red.
     - CLS p75 increased ≥0.05 absolute → yellow.
     - FCP / TTFB p75 increased ≥30% → yellow.
     - Inspection status changed from `INDEXED` to anything else → red.
     - `googleCanonical` changed → yellow.
     - `lastCrawlTime` >60 days old → yellow.
     - **Caveat:** if either snapshot lacks Google fields (creds were missing at one capture), surface `Field-data / indexation drift: not comparable — Google fields missing from {baseline | current} snapshot.`
=== replace
   - **Google-data drift:** not available in this edition. Report `Field-data / indexation drift: not available in this edition`.
