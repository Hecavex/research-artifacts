# HECAVEX Research Bundle Specification

Version 1.0.0

## Purpose

A HECAVEX research bundle makes a published investigation independently understandable without overstating what public evidence proves. It records provenance, analytical boundaries, lifecycle state and change history in formats that humans and software can inspect.

## Required files

| File | Purpose |
| --- | --- |
| `README.md` | Scope, intelligence question, collection window, methods, findings, limitations and safe-use notes. |
| `CITATION.cff` | Human and machine-readable release citation. |
| `CHANGELOG.md` | Material additions, corrections and assessment changes by version and date. |
| `LICENSE.md` | Reuse terms and third-party-material boundary. |
| `evidence-manifest.csv` | Relative path, SHA-256, size, media type and description for every released artifact. |
| `sources.csv` | Stable source ID, title, publisher, publication/access dates, URL, archive URL and role. |

## Conditional files

| File | Use when |
| --- | --- |
| `observations.csv` | Discrete collection events can be represented safely. |
| `indicators.csv` | Defensive indicators are released with context and lifecycle state. |
| `graph.json` | The research contains relationships suitable for a graph. |
| `attack-navigator.json` | ATT&CK mapping materially helps defenders. |
| `reproduction-notes.md` | A transformation, query, hash derivation or analytical step can be repeated. |

## Observations

An observation row should contain:

- `observation_id`
- `observed_at`
- `collected_at`
- `object_type`
- `object_value`
- `context`
- `source_id`
- `collection_method`
- `evidence_path`
- `confidence`
- `notes`

The row records what was seen. It must not silently claim ownership, compromise, victim status or attribution.

## Indicators

An indicator row should contain:

- `indicator_id`
- `type`
- `value`
- `role`
- `first_observed`
- `last_observed`
- `status`
- `confidence`
- `source_id`
- `expires_at`
- `safe_for_blocking`
- `notes`

Allowed lifecycle states are `current`, `expired`, `revoked`, `benign-comparison` and `unknown`. Shared infrastructure and legitimate services must not be marked safe for permanent blocking merely because malicious content was observed through them.

## Relationships

Graph edges use one of two evidence classes:

- `observed`: directly supported by the cited evidence object
- `assessed`: an analytical relationship derived from one or more observations

Every assessed edge requires a confidence value and explanatory note. Graphs do not create evidence that is absent from the underlying release.

## Versioning

Bundles use semantic versions:

- patch: presentation or metadata correction that does not change an assessment
- minor: new evidence that extends but does not reverse the main assessment
- major: changed evidence boundary, material correction or reassessment

Old releases remain available. A corrected file is not silently substituted into a historical release.

Every release directory must use the exact `vMAJOR.MINOR.PATCH` form. CI discovers directories rather than relying on a manually maintained list, so a new release cannot silently bypass validation. Every file except the root `evidence-manifest.csv` itself must appear exactly once in the manifest. Symbolic links, paths outside the release, malformed JSON, duplicate or unknown source identifiers, invalid source dates or URLs, and missing source metadata are rejected.

## Safety exclusions

Do not publish active credentials, personal victim data, executable malicious payloads, private API keys, unlawfully obtained data or operational details whose foreseeable harm exceeds their defensive value. Defang only when doing so does not destroy the evidentiary property being documented.
