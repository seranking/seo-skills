# RAW — stripe.com/pricing (markdown excerpt)

> Source: `mcp__firecrawl-mcp__firecrawl_scrape` markdown format. Full body is 65 KB — only the first ~80 lines shown here for the example deliverable. Production runs persist the full body.

```markdown
Chat with Stripe sales


Pricing & Fees

# [Stripe logo](https://stripe.com/)

- Products
- Solutions
- Developers
- Resources
- [Pricing](https://stripe.com/pricing)
- [Guide me](https://stripe.com/personalize)

[Sign in](https://dashboard.stripe.com/login)
[Dashboard](https://dashboard.stripe.com/)
[Contact sales](https://stripe.com/contact/sales)

# Payments

- [Payments — Online payments](https://stripe.com/payments)
- [Managed Payments — Merchant of record solution](https://stripe.com/managed-payments)
- [Payment links — No-code payments](https://stripe.com/payments/payment-links)
- [Checkout — Prebuilt payment UIs](https://stripe.com/payments/checkout)
- [Elements — Flexible UI components](https://stripe.com/payments/elements)
- [Payment methods — Access to 100+](https://stripe.com/payments/payment-methods)
- [Terminal — In-person payments](https://stripe.com/terminal)
- [Radar — Fraud prevention](https://stripe.com/radar)
- ...
```

The full markdown contains 145 `h1`/headline tokens (most are nav megamenu category labels, not in-content h1s). A semantic h1-extractor would identify only one true page h1 ("Pricing").

## Why we kept full-page (`onlyMainContent: false`)

For this example we wanted to:

1. Expose the nav megamenu link graph (271 links) for the "Links audit" table in META.md.
2. Demonstrate that Stripe's pricing page has zero JSON-LD even with full-page DOM captured.

For most production scrape use cases, `onlyMainContent: true` (the default) is preferred — it drops nav/footer noise and shrinks the markdown by ~80% for the same prose value.
