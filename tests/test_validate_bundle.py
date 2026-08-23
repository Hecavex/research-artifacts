from __future__ import annotations

import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from validate_bundle import discover_bundles, validate  # noqa: E402


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_bundle(root: Path) -> Path:
    bundle = root / "releases" / "example-case" / "v1.0.0"
    bundle.mkdir(parents=True)
    files = {
        "README.md": "# Example\n",
        "CHANGELOG.md": "# Changes\n",
        "CITATION.cff": 'cff-version: 1.2.0\ntitle: "Example"\n',
        "LICENSE.md": "# Licence\n",
        "sources.csv": "source_id,title,publisher,published_at,accessed_at,url,archive_url,role\nsrc-1,Example,HECAVEX,2026-08-20,2026-08-22,https://example.test/,,research source\n",
        "graph.json": json.dumps({"nodes": [], "edges": []}) + "\n",
        "observations.csv": "observation_id,source_id\nobs-1,src-1\n",
    }
    for relative, content in files.items():
        (bundle / relative).write_text(content, encoding="utf-8", newline="\n")
    with (bundle / "evidence-manifest.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["path", "sha256", "size_bytes", "media_type", "description"],
        )
        writer.writeheader()
        for relative in sorted(files):
            path = bundle / relative
            writer.writerow(
                {
                    "path": relative,
                    "sha256": digest(path),
                    "size_bytes": path.stat().st_size,
                    "media_type": "application/json" if path.suffix == ".json" else "text/plain",
                    "description": f"Fixture {relative}",
                }
            )
    return bundle


class BundleValidationTests(unittest.TestCase):
    def test_valid_bundle_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle = build_bundle(Path(directory))
            self.assertEqual(validate(bundle), [])

    def test_hash_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle = build_bundle(Path(directory))
            (bundle / "README.md").write_text("changed\n", encoding="utf-8")
            self.assertIn("SHA-256 mismatch: README.md", validate(bundle))

    def test_duplicate_manifest_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle = build_bundle(Path(directory))
            manifest = bundle / "evidence-manifest.csv"
            lines = manifest.read_text(encoding="utf-8").splitlines()
            manifest.write_text("\n".join(lines + [lines[1]]) + "\n", encoding="utf-8")
            self.assertIn("Duplicate manifest path: CHANGELOG.md", validate(bundle))

    def test_noncanonical_manifest_alias_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle = build_bundle(Path(directory))
            manifest = bundle / "evidence-manifest.csv"
            with manifest.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            alias = dict(rows[0])
            alias["path"] = f"./{alias['path']}"
            with manifest.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows([*rows, alias])
            self.assertIn(
                f"Manifest path is not canonical: {alias['path']}",
                validate(bundle),
            )

    def test_truncated_source_row_is_reported_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle = build_bundle(Path(directory))
            sources = bundle / "sources.csv"
            sources.write_text(
                "source_id,title,publisher,published_at,accessed_at,url,archive_url,role\n"
                "src-1,Truncated\n",
                encoding="utf-8",
            )
            manifest = bundle / "evidence-manifest.csv"
            with manifest.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            for row in rows:
                if row["path"] == "sources.csv":
                    row["sha256"] = digest(sources)
                    row["size_bytes"] = str(sources.stat().st_size)
            with manifest.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            errors = validate(bundle)
            self.assertIn("sources.csv row 2 has no publisher", errors)
            self.assertIn("sources.csv row 2 has no accessed_at", errors)
            self.assertIn("sources.csv row 2 has no url", errors)

    def test_truncated_manifest_row_is_reported_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle = build_bundle(Path(directory))
            manifest = bundle / "evidence-manifest.csv"
            with manifest.open("a", encoding="utf-8", newline="") as handle:
                handle.write("ghost.txt\n")
            errors = validate(bundle)
            self.assertIn("Invalid SHA-256 value: ghost.txt", errors)
            self.assertIn("Invalid byte-size value: ghost.txt", errors)
            self.assertIn("Manifest file is missing: ghost.txt", errors)

    def test_invalid_json_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle = build_bundle(Path(directory))
            graph = bundle / "graph.json"
            graph.write_text("{not-json}\n", encoding="utf-8")
            # Refresh its manifest hash so this test isolates JSON parsing.
            rows: list[dict[str, str]]
            manifest = bundle / "evidence-manifest.csv"
            with manifest.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            for row in rows:
                if row["path"] == "graph.json":
                    row["sha256"] = digest(graph)
                    row["size_bytes"] = str(graph.stat().st_size)
            with manifest.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            self.assertTrue(any(error.startswith("Invalid JSON in graph.json") for error in validate(bundle)))

    def test_unknown_source_reference_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle = build_bundle(Path(directory))
            observations = bundle / "observations.csv"
            observations.write_text("observation_id,source_id\nobs-1,missing-source\n", encoding="utf-8")
            manifest = bundle / "evidence-manifest.csv"
            with manifest.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            for row in rows:
                if row["path"] == "observations.csv":
                    row["sha256"] = digest(observations)
                    row["size_bytes"] = str(observations.stat().st_size)
            with manifest.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            self.assertIn(
                "observations.csv row 2 references unknown source_id: missing-source",
                validate(bundle),
            )

    def test_discovery_finds_every_semantic_version(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = build_bundle(root)
            second = root / "releases" / "second-case" / "v2.1.3"
            second.mkdir(parents=True)
            bundles, errors = discover_bundles(root / "releases")
            self.assertEqual(errors, [])
            self.assertEqual(bundles, [first.resolve(), second.resolve()])

    def test_discovery_rejects_non_semantic_version_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            releases = Path(directory) / "releases"
            (releases / "example-case" / "latest").mkdir(parents=True)
            bundles, errors = discover_bundles(releases)
            self.assertEqual(bundles, [])
            self.assertEqual(errors, ["Invalid semantic-version directory: example-case/latest"])

    def test_discovery_rejects_hidden_release_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            releases = Path(directory) / "releases"
            build_bundle(Path(directory))
            (releases / ".hidden-case" / "v1.0.0").mkdir(parents=True)
            bundles, errors = discover_bundles(releases)
            self.assertEqual(len(bundles), 1)
            self.assertIn("Unexpected entry under releases: .hidden-case", errors)


if __name__ == "__main__":
    unittest.main()
