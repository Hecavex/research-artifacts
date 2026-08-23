# Safe reproduction notes

These steps reproduce published relationships from passive sources. They do not require visiting a live phishing page, executing JavaScript, opening a Socket.IO session or submitting test data.

## Exact-hash pivot

1. Start from SHA-256 `7068d7b09a8afb99b051847dd65602e054f69c33d0cd8161ab986eae71538a2b`.
2. Query URLScan's public search for the exact response hash.
3. Export or enumerate the public result metadata available under the service terms.
4. Preserve the scan timestamp, page hostname, page URL, response hash, server and ASN fields.
5. Deduplicate only `page.hostname` to reproduce the 126-hostname count. Do not call those hostnames victims without separate evidence.

The result set documented on 11 August 2026 contained 163 scans. Search indexes are dynamic, so a later query may produce a different total. The released count is a historical observation, not a promise that the live query will remain frozen.

## `/console` corroboration

The combined public query was:

```text
filename:console AND filename:DDXZMe5D.js
```

It returned the same 163-scan set during collection. `/console` alone is not unique and must not be promoted to a standalone malicious indicator.

## Delivery grouping

Group the 163 records by ASN and server response:

- AS13335 observations form the shared Cloudflare delivery layer.
- AS132203 observations delivered directly through OpenResty or nginx.

The documented split is 121 Cloudflare observations and 42 direct observations. Provider infrastructure identifies hosting context, not operator identity or nationality.

## Exact frontend relationship

Compare the four hashes in `exact-hash-pivots.csv` across the supplied UNIPARK deployment and the public `unipark.fxqro[.]xin` record. Byte-identical static assets support a strong frontend relationship. They do not prove who deployed the files.

## JWR comparison

Normalize and compare the public Cisco Talos JWR hashes, domains and IP addresses against the indicators documented here. The 14 August comparison produced zero exact hash, domain and IP overlap. Similar workflow, Vue use and real-time operator control are tradecraft similarities, not direct lineage evidence.

## Safety exclusions

Do not execute recovered bundles, submit data, probe an operator panel, block shared Cloudflare addresses or block `siena.nksc.lt`. Do not publish private API credentials or raw browser profiles.
