# Hostinger-themed Cloudflare Pages phishing research data

Version 1.1.0 - 24 August 2026

This bundle supports the HECAVEX investigation [Hostinger impersonation infrastructure: 298 Cloudflare Pages task domains](https://hecavex.com/en/research/hostinger-pages-phishing-infrastructure/).

## Intelligence question

What can public scan records, exact content hashes, static code analysis and tightly bounded verification establish about the Hostinger-themed credential-phishing infrastructure, its deployment naming and its relationship to other lure themes?

## Evidence boundary

This release contains publication-safe aggregate observations, a complete defanged and role-classified domain inventory, contextual indicators, exact-hash summaries, descriptive hostname statistics, cross-brand context, a relationship graph, one synthetic loopback-only request-shape reconstruction, one bounded fixed-path response summary and reproduction notes. It does not contain raw phishing HTML or JavaScript, response bodies, full task URLs, personalized paths, query strings, recipient-derived fields, provider correspondence, API credentials, private collection ledgers or executable malicious material.

The source register uses generic provider landing pages for three reviewed public reports whose direct report locators may expose recipient-derived metadata.

The evidence supports:

- 562 public scan observations across 298 exact task domains in the long Hostinger Pages family;
- one additional exact-family name found only as a final page, producing a 299-name local cross-role union;
- 302 Hostinger-labelled Pages names across roles when one confirmed precursor and two explicitly separated lead-only names are included;
- one PythonAnywhere name retained only as delivery or redirect context, producing 303 classified domain records in the public inventory;
- an exact credential-harvesting JavaScript hash in 467 observations across 262 task domains;
- five of eight deterministically selected Pages hosts serving the exact known document on 24 August 2026;
- 15 of 15 known static-script responses on those five hosts matching archived hashes;
- 24-character lowercase suffixes consistent with automated deployment-name randomization;
- 67 same-shape Pages task domains across 12 lure prefixes in a preselected partial cross-brand corpus;
- zero structurally valid ZIP archives from a fixed, hash-gated 25-path check;
- nine exact root-document responses and one un-followed redirect from a later hash-gated, ten-path check on one previously confirmed host; and
- one synthetic request-shape fixture accepted by a receiver bound only to `127.0.0.1`, with no campaign or provider host contacted.

The release does not establish a victim count, successful credential submission, campaign-receiver behavior, Hostinger compromise, one operator, one Cloudflare account, a predictive malware DGA, or exact Hostinger-core reuse across the 67-name cross-brand context.

## Files

- `observations.csv` - time-bounded and derived observations
- `hostinger-domain-inventory.csv` - complete defanged domain inventory with provider, role, tier, timestamps and safe-use guidance
- `indicators.csv` - defanged indicators with lifecycle and blocking guidance
- `exact-hash-pivots.csv` - exact content hashes and documented public counts
- `infrastructure-summary.csv` - aggregate infrastructure and bounded-check results
- `fixed-path-response-summary.csv` - publication-safe results of the later one-host response comparison
- `hostname-generation-summary.csv` - descriptive statistics for the 298 and 299-name sets
- `cross-brand-context.csv` - prefix counts from the partial same-shape corpus
- `local-mock-flow.json` - synthetic loopback-only request-shape reconstruction
- `graph.json` - observed, derived, assessed and limited relationships
- `reproduction-notes.md` - safe offline methodology and analytical boundaries
- `sources.csv` - public source register
- `evidence-manifest.csv` - SHA-256 and byte-size inventory
- `CITATION.cff`, `CHANGELOG.md` and `LICENSE.md` - citation, release history and reuse terms

## Safety and brand boundary

Hostinger is the impersonated brand and is not shown to be compromised. Cloudflare, Render and PythonAnywhere are service providers, not attributed campaign participants. The domain inventory is a historical evidence record, not a live-state feed or ready-made blocklist. Two Pages rows are lead-only and the PythonAnywhere row is redirect context. Shared provider domains and addresses are not general blocklist targets. Treat exact project indicators as time-bounded and verify current ownership and content before operational action.

Corrections: `info@hecavex.com`.
