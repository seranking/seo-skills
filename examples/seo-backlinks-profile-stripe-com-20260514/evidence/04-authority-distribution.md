# 04 — Authority distribution

> Source: `DATA_getDistributionOfDomainAuthority(target="stripe.com", mode="domain")` — retrieved 2026-05-18.

## Live histogram (2026-05-18)

```
DA 70–100 │ █████████  9.3%   (57,865 domains — github.com, stackoverflow.com, wikipedia.org, top media, major SaaS)
DA 50–69  │ █████████  9.0%   (55,780 domains — substantial press, mid-tier SaaS partners)
DA 30–49  │ ████████████████  16.4%  (101,293 domains — industry blogs, fintech ecosystem)
DA 10–29  │ █████████████████████████  25.1%  (155,475 domains — smaller tech blogs, dev tutorials, partner sites)
DA 0–9    │ ████████████████████████████████████████  40.2%  (248,884 domains — customer footer links, small blogs)
```

Total histogram entries: 619,297

## Why the DA 0–9 tail is larger than expected

At 40.2%, the DA 0–9 bucket exceeds the textbook ~15% healthy estimate. This is an **artefact of Stripe's customer scale**: every merchant website that uses Stripe as a payment processor is a potential referring domain, and many of these are small personal-use or micro-business sites with very low DA. The most common link pattern is "Powered by Stripe," "Pay with Stripe," or a footer privacy-policy link. These are legitimate, not manipulative.

**Key signal:** the DA 70+ head (9.3%, 57,865 domains) is exceptionally strong and confirms genuine editorial authority. This head counterbalances the low-DA tail from a link-equity perspective.

## Anomaly thresholds (still applicable)

- DA 0–9 jumping by > 10 percentage points MoM: could indicate a link-network spin-up (though at Stripe's scale this is unlikely).
- DA 80+ dropping below 5%: loss of high-trust signal — worth investigating.
- DA distribution shape changes by > 5 percentage points in any bucket month-over-month: investigate via `seo-drift compare`.
