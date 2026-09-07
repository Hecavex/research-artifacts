# Experimental unapproved authentication-journey correlation

This pilot supports [Evilginx Detection](https://hecavex.com/en/research/evilginx-detection/). It links a confirmed navigation to an independently reviewed, unapproved authentication origin with a successful sign-in for the same canonical user within ten minutes, when the two observed IP strings differ.

A match is a review candidate for the authentication journey. It does not identify Evilginx, prove that authentication traversed a proxy, demonstrate token exposure or establish session replay. VPNs, secure gateways, mobile routing, legitimate proxies and unrelated concurrent activity can explain the correlation.

## Custom normalized schema

`analytic.kql` uses Kusto KQL over two **custom normalized tables**, not built-in Defender XDR or Sentinel tables. An operator must implement and test the mapping. `ClickEvents` contains ClickId, UserKey, AuthHost, ClickIP (strings), ClickTime (datetime), Navigated and OriginApproved (nullable bool). `SigninEvents` contains SigninId, UserKey, SigninIP (strings), SigninTime (datetime) and Success (nullable bool).

The JSON input uses the same fields under `clicks` and `signins`, plus `reference_time` and a test `expected` list. UserKey is a stable canonical identity resolved by the operator. No automatic UPN-to-object-ID match is assumed. Keep source event IDs and the private normalization lineage. AuthHost is a hostname, not a live link.

Navigated means the origin was actually reached, not merely that a blocked click exists. OriginApproved=false must come from a reviewed authentication-origin inventory and supporting context, not from every unfamiliar hostname. Unknown approval stays null. Microsoft UrlClickEvents can support click lineage, while Entra SigninLogs can support sign-in status and identity mapping. Their raw fields do not automatically satisfy this contract. Connector access and retention are prerequisites.

Clicks must fall after reference time minus 14 days and at or before reference time. Sign-ins must be successful, at or after the click and no later than ten minutes after it or reference time. Both IP strings must exist and differ. Normalize address representation before use. The model does not calculate geography or infer client ownership. Missing fields yield missing coverage. Output keeps ClickId, SigninId and UserKey, including every qualifying pair rather than silently deduplicating an event.

## Fixtures and tuning

Twelve click/sign-in pairs cover a positive journey, approved origin, blocked navigation, failed sign-in, same IP, a sign-in one second after the window, reversed event order, unknown origin state, another user, the included ten-minute boundary, a future sign-in and missing click IP. Only the positive and exact-boundary pairs match.

Choose the time window using measured ingestion lag and authentication timing. A longer window increases accidental joins. Preserve event time separately from ingestion time when mapping. This pilot does not prove common session identity and omits mailbox, OAuth and application impact. Same-IP proxies and unobserved clicks can evade it. Absence of a match does not clear an account.

## Run the portable fixture test

Requires Python 3.12 or newer and only the standard library. Run from this release directory:

```text
python reference.py --check
python reference.py
python reference.py --input /path/to/your-normalized-fixture.json
```

The first command compares the output with the independently specified `expected` list in `fixtures.json` and exits nonzero on a mismatch. The second prints the review candidates. The third accepts the same documented JSON contract and does not contact any host. Keep real account identifiers and exact URLs private. Source rows use reserved documentation addresses and names and are entirely synthetic.

## Validation boundary

Status: experimental. Portable Python positive, negative and boundary tests pass. KQL compilation, execution, query plans, connector mappings and semantic equivalence in the intended engine are **NOT VERIFIED**. Production detection efficacy, false-positive rate and recall are **NOT VERIFIED**. Passing Python tests does not validate KQL.

Before use, run the KQL in a controlled workspace with equivalent typed fixture tables, compare its projected rows against the fixture expectations, verify missing-value and timestamp behavior, then shadow-test against authorized benign telemetry. Record the actual engine/version, connector, schema and time range. Keep the rule experimental until those checks are documented. Do not operate malware, collect authentication material or visit suspicious origins to validate it.

## Reuse and provenance

Version 1.0.0, prepared 7 September 2026. This is an authored defensive experiment, not a captured campaign or an indicator feed. `sources.csv` records the guide and primary schema references. `evidence-manifest.csv` covers every file except itself. Download the repository archive at the linked release commit or clone that commit, then select this version directory. Verify hashes before reuse. Existing release directories are immutable.

