# UNIPARK-themed smishing and parking phishing-kit research data

Version 1.0.0 · released 14 August 2026

This bundle supports the HECAVEX investigation [UNIPARK Smishing: From One SMS to 126 Phishing Hosts](https://hecavex.com/en/research/unipark-smishing-campaign-infrastructure/).

## Intelligence question

What infrastructure and reusable software relationships can be established from the UNIPARK-themed SMS delivered in Lithuania on 11 August 2026, and what does the public evidence not establish?

## Evidence boundary

The release contains structured observations, contextual defensive indicators, exact-hash pivots, infrastructure summaries, sources and an evidence graph. Values relating to malicious infrastructure are defanged. It excludes executable JavaScript, live phishing pages, credentials, submitted form data, private API keys and browser profiles.

The public evidence supports:

- an UNIPARK-themed credential and payment-card collection flow
- four exact frontend-asset matches between `unipark.fmqr[.]ink` and an earlier `unipark.fxqro[.]xin` deployment
- a shared core JavaScript hash observed in 163 public URLScan records across 126 unique page hostnames
- active same-origin `/console` requests across those 163 observations
- 121 Cloudflare-delivered scans and 42 directly delivered scans, including 12 AS132203 addresses
- high confidence in a common software family and only medium confidence in one operator controlling the full cluster.

The release does **not** establish a named operator, operator geography, successful theft, a victim count, the Cloudflare-hidden origin used by the supplied hostname, or direct code lineage with Cisco Talos's JWR framework.

## Collection window

- earliest public core-hash observation found: 30 June 2026
- incident and main collection snapshot: approximately 08:10 UTC, 11 August 2026
- comparative JWR update: 14 August 2026

Public infrastructure changes over time. Treat the rows as historical observations rather than a permanent blocklist.

## Files

- `observations.csv` — time-bounded observations and derived public counts
- `indicators.csv` — defanged, contextual indicators with lifecycle and blocking guidance
- `exact-hash-pivots.csv` — released asset hashes and their documented public matches
- `infrastructure-summary.csv` — delivery-layer and selected direct-IP pivot summaries
- `sources.csv` — public sources used by the release
- `graph.json` — observed and assessed relationships
- `reproduction-notes.md` — safe reproduction procedure and query boundaries
- `evidence-manifest.csv` — SHA-256 and byte-size inventory

## Safety and trademarks

UNIPARK, RingGo, EyeParking, EasyPark, Q-Park, NCP, Cloudflare, Tencent Cloud and other legitimate organisations are not treated as participants merely because their brands or infrastructure were impersonated or abused. Shared-provider addresses and the Lithuanian NKSC sinkhole are explicitly marked unsafe for indiscriminate blocking.

Corrections: `info@hecavex.com`.
