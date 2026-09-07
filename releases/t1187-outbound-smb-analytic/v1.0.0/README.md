# Experimental outbound SMB review analytic

This pilot supports [T1187 Forced Authentication: Detection and Mitigation](https://hecavex.com/en/research/t1187-forced-authentication-detection-mitigation/). It asks which process-attributed network records target ports 139 or 445 with provider-supplied Public address classification outside a narrowly approved destination tuple.

A match is an outbound SMB review lead. It is not proof of NTLM exchange, forced authentication, successful connection, credential capture, relay or compromise. The model deliberately retains failed connection events as leads and preserves `ActionType`.

## Schema and rule

`analytic.kql` targets Microsoft Defender XDR advanced hunting `DeviceNetworkEvents`, populated by Defender for Endpoint. Review the actual in-portal `ActionType` definitions. Required fields are Timestamp (timezone-aware time), DeviceId, DeviceName, RemoteIP, RemoteIPType, InitiatingProcessFileName, ActionType (strings), RemotePort and ReportId (integers).

The JSON input has `reference_time`, `events`, `approved_destinations` and, for test mode, `expected`. The time interval is strictly after reference time minus 14 days and includes reference time. Ports are integer 139 or 445. Address type matches Public without case sensitivity. No DNS resolution or IP reclassification occurs.

An approval matches all of DeviceId, RemoteIP, RemotePort and lowercased process name. The example approval is synthetic. Replace it with an owned, expiring exception inventory before deployment. Different devices using the same destination remain in scope. Missing required fields are skipped as coverage gaps, not labeled benign. Malformed times or invalid schema can fail the offline run and require correction before comparison.

Output contains DeviceName, Timestamp, ReportId, RemoteIP, RemotePort and ActionType, sorted in that order of identity. ReportId alone is not unique. DeviceName and Timestamp remain attached.

## Fixtures and tuning

The 12 records include public 445 and failed 139 leads, private-address and other-port negatives, an exact approval and case-insensitive process approval, a different-device positive, the excluded lower time boundary, a future record, missing address classification, empty address and wrong port type. Expected review records are 1, 2 and 6.

The TEST-NET addresses are intentionally given synthetic Public labels. They are not classified as public production destinations. The KQL table is typed, so the Python fixture with a string port tests the input contract and has no claim of native-table equivalence.

Legitimate external shares, backup agents and management software can match. Start with local ownership and egress requirements. Do not suppress all cloud networks or all processes. IPv6 depends on the provider's classification. This pilot omits WebDAV, nonstandard ports, process-to-file joins, NTLM audit joins and direct confirmation of coercion. Other T1187 paths can remain invisible.

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

