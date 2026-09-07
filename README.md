# HECAVEX Research Artifacts

Versioned, reproducible supporting material for original HECAVEX cyber threat intelligence research.

The website at <https://hecavex.com/> is the publication of record. This repository contains machine-readable observations, evidence manifests, reproduction notes, graph data and other material that can be shared safely and lawfully.

## Principles

- A research artifact is not automatically an indicator of compromise.
- Observations are kept separate from analytical relationships and assessments.
- Time, source, role, confidence and lifecycle state are preserved where available.
- Exact evidence boundaries are documented. Hostnames are not silently converted into victims.
- Active credentials, personal data, live malicious payloads and material that creates disproportionate risk are excluded.
- Material changes receive a new release and a dated changelog entry.

## Layout

```text
releases/
  <research-slug>/
    v1.0.0/
      README.md
      CITATION.cff
      CHANGELOG.md
      LICENSE.md
      evidence-manifest.csv
      observations.csv
      indicators.csv
      <case-specific-data>.csv
      sources.csv
      graph.json
templates/
  research-bundle/
docs/
  RESEARCH_BUNDLE_SPEC.md
```

## Published bundles

- [t1187-outbound-smb-analytic/v1.0.0](releases/t1187-outbound-smb-analytic/v1.0.0/README.md) - experimental outbound SMB review analytic with synthetic positive, negative and boundary fixtures. Portable Python tests pass. KQL engine execution and production efficacy are NOT VERIFIED.
- [aitm-auth-journey-analytic/v1.0.0](releases/aitm-auth-journey-analytic/v1.0.0/README.md) - experimental correlation over an explicit custom authentication-journey schema. Portable Python tests pass. This is a review lead, not proof of Evilginx or token theft. KQL engine execution and production efficacy are NOT VERIFIED.

- `hostinger-pages-phishing-2026/v1.1.1` - current publication-safe evidence for the Hostinger-themed Cloudflare Pages phishing investigation, including the complete defanged and role-classified domain inventory plus a bounded fixed-path response comparison. This patch corrects packaging integrity, not observations or findings. It excludes raw campaign content, full task URLs, personalized query strings, private scan identifiers and provider correspondence. Historical `v1.0.0` and `v1.1.0` remain immutable with an explicit [checksum erratum](docs/ERRATA-2026-09-07.md).

- `adform-clipper-2026/v1.1.0` — current evidence package supporting the Adform JavaScript supply-chain investigation, including reproducible BTC and Ethereum tracing. `v1.0.0` remains immutable.

- `unipark-smishing-2026/v1.0.0` — structured evidence supporting the UNIPARK-themed smishing and parking phishing-kit investigation.

## Validate releases

The validator discovers every semantic-version directory, checks required files, manifest paths, duplicate records, byte counts, SHA-256 values, source dates and URLs, internal source identifiers, and JSON syntax. It reads captured files as bytes and never executes them.

```powershell
# Every release (the CI and portfolio default)
python scripts/validate_bundle.py --all

# Exact bytes delivered by Git, independent of workstation line endings
python scripts/validate_bundle.py --all --git-export

# One release while authoring
python scripts/validate_bundle.py releases/adform-clipper-2026/v1.1.0
```

## Citation

Cite the article for narrative findings and the versioned artifact release for data or reproduction work. A `CITATION.cff` file is included in every release.

New releases are prepared outside existing version directories. After finalizing
their text, `python scripts/build_manifest.py releases/<case>/<new-version>`
normalizes text to LF and hashes the final bytes. It refuses already committed
release directories. CI tests both Windows and Linux and rejects changes to
versions already present in the trusted pre-change Git revision.

## Licence

Unless a release says otherwise, HECAVEX-authored documentation and structured data are published under Creative Commons Attribution 4.0. Third-party evidence remains subject to its original rights and is referenced rather than relicensed.
