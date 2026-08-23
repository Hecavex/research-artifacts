# Adform JavaScript supply-chain crypto-clipper research data

Release: `v1.0.0`
HECAVEX snapshot: 2026-08-08.

Publication:

- <https://hecavex.com/en/research/adform-supply-chain-crypto-clipper/>
- <https://hecavex.com/lt/tyrimai/adform-supply-chain-crypto-clipper/>

## Files

- `iocs.csv`: network, content-hash, wallet and structural indicators.
- `observed-hosts.csv`: URLScan page hostnames whose scan loaded a response with one of four exact malicious SHA-256 hashes.
- `urlscan-exact-hash-observations.csv`: all 83 individual URLScan observations, including scan time, page hostname, exact response hash, mapped payload capability and result URL.
- `payload-capabilities.csv`: static-analysis mapping from each response hash to its wallet-replacement capability and public sample source.
- `reproduction-notes.md`: byte-level reproduction of the `02ff86c7...` advanced-only response from the archived `a04461bb...` two-block response.
- `functioning-wallet-replacement-hosts.csv`: the strict 55-host subset with at least one exact match to a functioning BTC and ETH replacement variant.
- `sources.csv`: primary and supporting sources used to interpret the observations.
- `evidence-manifest.csv`: SHA-256, size and purpose of every released artifact.
- `CITATION.cff`, `CHANGELOG.md` and `LICENSE.md`: citation, version and reuse information.

## Interpretation

An entry in `observed-hosts.csv` is an exact-response-hash observation. According to the URLScan Search API definition, the `hash` field matches the SHA-256 of any HTTP response downloaded during a scan. The evidence therefore proves that a scan in the listed page context downloaded a byte-identical known sample. It does **not** by itself prove that every real visitor received the response, that a cryptocurrency address was entered, that the rewrite handler fired, or that funds were diverted.

The 59-host total contains two distinct capability classes:

- 55 page hostnames have at least one exact match to a variant containing valid BTC and ETH replacement destinations.
- 4 page hostnames only matched the early malicious variant whose recovered BTC, ETH and TRON destination strings are invalid.

All four variants are malicious, but only the 55-host subset supports the narrower statement that the downloaded script was capable of replacing BTC and ETH addresses with functioning destinations. Neither number is a count of confirmed victims.

The legitimate `s2.adform.net` distribution hostname is included only as context. Do not block it broadly. Apply time-window, path, response-hash and cache metadata together.

The Bitcoin and Ethereum addresses are high-confidence replacement destinations recovered from archived code. Individual on-chain transactions are not automatically attributable to this incident without independent victim or telemetry evidence.

## Time windows

- Central incident window reported by Adform: `2026-07-26T21:49:00Z` to `2026-07-27T17:16:00Z`.
- Recommended cache-review extension: through at least `2026-08-06T23:59:59Z`, based on an observed seven-day `max-age`.

## Collection boundary

This package contains public metadata and analyst-created structured data. It does not contain executable malicious JavaScript. URLs to third-party evidence are provided for verification, but availability can change after publication.

## Versioning

This directory is an immutable release. A material correction or additional collection will be issued as a new version and described in `CHANGELOG.md`.
