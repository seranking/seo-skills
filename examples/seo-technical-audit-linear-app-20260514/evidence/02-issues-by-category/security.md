# Issues — Security headers

Source: `curl -sI -A "Mozilla/5.0" {URL}` on homepage + 3 sample URLs.

## Response headers — homepage

```
HTTP/2 200
strict-transport-security: max-age=63072000; includeSubDomains
content-security-policy: default-src 'self' https://static.linear.app https://static.linear.dev; ...; frame-ancestors 'self' https://cms.linear.app; frame-src *; ...
referrer-policy: same-origin
x-content-type-options: nosniff
server: cloudflare
x-nextjs-cache: HIT
```

## Per-URL header matrix

| Header | Homepage | /pricing | /method | /customers | Status |
|---|---|---|---|---|---|
| `Strict-Transport-Security` | `max-age=63072000; includeSubDomains` | same | same | same | High — **missing `preload`** |
| `Content-Security-Policy` | present, ~3000 chars | identical | identical | identical | Medium — `frame-src *` wildcard |
| `X-Frame-Options` | absent | absent | absent | absent | informational (superseded by CSP `frame-ancestors`) |
| `X-Content-Type-Options` | `nosniff` | `nosniff` | `nosniff` | `nosniff` | pass |
| `Referrer-Policy` | `same-origin` | `same-origin` | `same-origin` | `same-origin` | pass |
| `X-Robots-Tag` | absent | absent | absent | absent | pass (no HTTP-layer noindex) |
| `Permissions-Policy` | absent | absent | absent | absent | informational — best practice for newer sites |

## Issues mapped

### `hsts_no_preload` (High)
HSTS header is present with `max-age=63072000` (2 years) and `includeSubDomains`. Two missing pieces:
1. The `preload` directive is not declared.
2. `linear.app` is not on the [Chromium HSTS preload list](https://hstspreload.org/?domain=linear.app).

**Fix:** add `preload` to the header (becomes `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`), then submit `linear.app` to hstspreload.org. Once preloaded, browsers refuse plain HTTP on linear.app and all subdomains before the first request, eliminating SSL-strip MITM.

### `csp_frame_src_wildcard` (Medium)
The CSP has `frame-src *;` — this allows any origin to be embedded into a frame loaded by linear.app pages. Combined with strong `frame-ancestors 'self' https://cms.linear.app` (preventing linear.app from being embedded), the risk is asymmetric: external content can be injected into linear.app via legitimate embed flows, but a malicious embed could phish.

**Fix:** tighten to explicit allow-list (Stripe, Ashby HQ, Cloudflare Turnstile, YouTube, GitHub — all already on the connect-src/script-src side).

### `xframe_missing` (informational)
`X-Frame-Options` is absent. The CSP `frame-ancestors` directive supersedes `X-Frame-Options` in modern browsers — this is informational only. Older browsers (IE) would still benefit from the deprecated header.

### Passes
- `X-Content-Type-Options: nosniff` — set everywhere sampled. Prevents MIME-sniff XSS.
- `Referrer-Policy: same-origin` — set everywhere. Conservative; doesn't leak referrer cross-origin.
- HTTPS-only via HSTS — though preload would harden the first-load case.

## Other observations
- `server: cloudflare` + `cf-ray:` headers — Linear sits behind Cloudflare. Many security controls (WAF, bot management, rate limiting) likely live at the Cloudflare edge and are not surfaced in HTTP response headers. A full security review should include Cloudflare configuration, which is outside this skill's scope.
- `via: 1.1 google` — Google Cloud Frontend in front of Cloudflare suggests a Google-Cloud-backed origin.
