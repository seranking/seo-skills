/**
 * Domain intelligence snapshot — seranking.com — SE Ranking Data API.
 * Read-only. 300 credits/run. Node 20+ (native fetch). Run weekly.
 */
import { writeFileSync } from "node:fs";

const API_KEY = process.env.SERANKING_API_KEY;
if (!API_KEY) throw new Error("Set SERANKING_API_KEY");

const BASE = "https://api.seranking.com/v1";
const HEADERS = { Authorization: `Token ${API_KEY}` };
const DOMAIN = "seranking.com";
const SOURCE = "us";
const RUN_COST = 300;

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

async function call<T>(
  method: string,
  path: string,
  opts: { params?: Record<string, string>; body?: unknown } = {},
  maxAttempts = 5,
): Promise<T> {
  const qs = opts.params ? `?${new URLSearchParams(opts.params)}` : "";
  let delay = 1000;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    const res = await fetch(`${BASE}${path}${qs}`, {
      method,
      headers: opts.body
        ? { ...HEADERS, "Content-Type": "application/json" }
        : HEADERS,
      body: opts.body ? JSON.stringify(opts.body) : undefined,
    });
    if (res.status === 429) {
      await sleep(delay + (Math.random() * 0.4 - 0.2) * delay);
      delay *= 2;
      continue;
    }
    if (res.status === 403 && (await res.text()).includes("Insufficient funds")) {
      throw new Error("Out of credits — top up before retrying.");
    }
    if (!res.ok) throw new Error(`${method} ${path} -> ${res.status}`);
    return (await res.json()) as T;
  }
  throw new Error(`Rate-limited after ${maxAttempts} attempts on ${path}`);
}

async function main() {
  // 1 — Preflight (0 credits).
  const sub = await call<{ subscription_info: { units_left: number } }>(
    "GET",
    "/account/subscription",
  );
  if (sub.subscription_info.units_left < RUN_COST) {
    throw new Error(`Only ${sub.subscription_info.units_left} credits left.`);
  }

  // 2 — Worldwide overview (100 credits).
  const overview = await call("GET", "/domain/overview/worldwide", {
    params: { domain: DOMAIN, currency: "USD" },
  });

  // 3 — Organic competitors, US (100 credits; up to 500 rows).
  const competitors = await call<{ data?: unknown[] }>("GET", "/domain/competitors", {
    params: { source: SOURCE, domain: DOMAIN, type: "organic" },
  });

  // 4 — Backlink summary, domain mode (100 credits).
  const backlinks = await call<{ summary: unknown[] }>("POST", "/backlinks/summary", {
    body: { target: DOMAIN, mode: "domain" },
  });

  const captured = new Date().toISOString().slice(0, 10);
  const snapshot = {
    domain: DOMAIN,
    captured,
    overview,
    topCompetitors: (competitors.data ?? []).slice(0, 15),
    backlinks: backlinks.summary[0],
  };
  const out = `snapshot-${DOMAIN}-${captured.replace(/-/g, "")}.json`;
  writeFileSync(out, JSON.stringify(snapshot, null, 2));
  console.log(`Wrote ${out}`);
}

main();
