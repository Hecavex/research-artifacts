# Adform JavaScript supply-chain crypto-clipper research data

Release: `v1.1.0`
HECAVEX snapshot: 2026-08-23.

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
- `onchain-addresses.csv`: seed, relay, router, service-boundary and aggregation addresses with dated label provenance.
- `onchain-transfers.csv`: selected evidentiary BTC and ETH paths, including decoded cross-chain destinations; it is not a complete or raw ledger export.
- `onchain-assessments.csv`: analytical conclusions separated from raw transfers, with confidence and explicit alternatives.
- `onchain-methodology.md`: snapshot boundary, inclusion rules, label handling and attribution limits.
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

## On-chain follow-up

The `v1.1.0` follow-up reproduces three distinct periods and keeps them separate:

- **Before Adform:** the embedded BTC and ETH wallet destinations were independently active before 26 July. Their activity overlapped on 18 July, which is consistent with, but does not prove, one shared episode or shared control. The ETH seed's relay path included decoded Harbor and Bridgers calls requesting conversion of 23.15 ETH, 15,258 USDT and 33,590 USDC to `bc1qtrw0lkv2pxd43r4n3lppex5y3gp7j87vt6mq3w`. That destination is different from the embedded BTC seed `bc1qmplgt0hcg62jc2guz86wn2sms7tqrsulkkrrls`; the public-ledger evidence does not link the two embedded seeds or identify the earlier delivery mechanism or payer identities.
- **Official incident window:** the BTC seed received 0.03239306 BTC across nine transfers. The ETH seed received 5.79608215429014 ETH, 2,581.032494 USDT and 1,649.349165 USDC. Public service tags identify some immediate sending wallets, not their customers or the incident origin of each payment.
- **After Adform:** selected BTC peel chains and ETH relay paths are preserved until assets enter high-volume pooled addresses, where deterministic public tracing stops.

No reviewed path establishes a named mixer, CoinJoin, Tornado Cash interaction, natural person, final exchange account or incident-specific loss amount. Harbor and Bridgers are documented cross-chain routing services and are not classified as mixers in this release.

## Time windows

- Central incident window reported by Adform: `2026-07-26T21:49:00Z` to `2026-07-27T17:16:00Z`.
- Recommended cache-review extension: through at least `2026-08-06T23:59:59Z`, based on an observed seven-day `max-age`.
- Ledger snapshot boundary: Bitcoin block `963754` and Ethereum block `25819340`, collected on `2026-08-23` around `18:00Z`.

## Collection boundary

This package contains public metadata and analyst-created structured data. It does not contain executable malicious JavaScript. `onchain-transfers.csv` preserves selected evidentiary paths needed to reproduce the stated assessments, not every transaction involving the listed addresses. URLs to third-party evidence are provided for verification, but availability can change after publication.

## Versioning

This directory is an immutable release. A material correction or additional collection will be issued as a new version and described in `CHANGELOG.md`.
