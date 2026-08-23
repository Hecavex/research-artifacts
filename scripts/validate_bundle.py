#!/usr/bin/env python3
"""Validate one HECAVEX research bundle or discover and validate all releases.

Captured artefacts are opened only as bytes for hashing. Nothing from a bundle
is imported, rendered, parsed as executable code, or otherwise executed.
"""

from __future__ import annotations

import argparse
import csv
from datetime import date
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

REQUIRED = {
    "README.md",
    "CHANGELOG.md",
    "CITATION.cff",
    "LICENSE.md",
    "evidence-manifest.csv",
    "sources.csv",
}
MANIFEST_COLUMNS = {"path", "sha256", "media_type", "description"}
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
VERSION_RE = re.compile(r"^v(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def _cell(row: dict[str, str], field: str) -> str:
    """Return one stripped CSV cell, including for a truncated DictReader row."""

    return (row.get(field) or "").strip()


def _valid_date(value: str) -> bool:
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def _valid_web_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc) and not parsed.username and not parsed.password


def _validate_sources(bundle: Path) -> tuple[list[str], set[str]]:
    path = bundle / "sources.csv"
    try:
        fields, rows = _read_csv(path)
    except (csv.Error, UnicodeError) as error:
        return [f"sources.csv cannot be read: {error}"], set()
    required = {"source_id", "title", "publisher", "accessed_at", "url", "role"}
    if not required.issubset(fields):
        return ["sources.csv is missing required columns: " + ", ".join(sorted(required - set(fields)))], set()
    if not rows:
        return ["sources.csv has no records"], set()
    errors: list[str] = []
    seen: set[str] = set()
    for number, row in enumerate(rows, start=2):
        source_id = _cell(row, "source_id")
        if not source_id:
            errors.append(f"sources.csv row {number} has no source_id")
        elif source_id in seen:
            errors.append(f"Duplicate source_id in sources.csv: {source_id}")
        else:
            seen.add(source_id)
        for field in ("title", "publisher", "accessed_at", "url", "role"):
            if not _cell(row, field):
                errors.append(f"sources.csv row {number} has no {field}")
        accessed_at = _cell(row, "accessed_at")
        if accessed_at and not _valid_date(accessed_at):
            errors.append(f"sources.csv row {number} has an invalid accessed_at date")
        published_at = _cell(row, "published_at")
        if published_at and not _valid_date(published_at):
            errors.append(f"sources.csv row {number} has an invalid published_at date")
        url = _cell(row, "url")
        if url and not _valid_web_url(url):
            errors.append(f"sources.csv row {number} has an invalid HTTP(S) url")
        archive = _cell(row, "archive_url") or _cell(row, "archived_url")
        if archive and not _valid_web_url(archive):
            errors.append(f"sources.csv row {number} has an invalid archive URL")
    return errors, seen


def _validate_source_references(bundle: Path, source_ids: set[str]) -> list[str]:
    errors: list[str] = []
    for path in sorted(bundle.rglob("*.csv")):
        if path.name in {"evidence-manifest.csv", "sources.csv"}:
            continue
        try:
            fields, rows = _read_csv(path)
        except (csv.Error, UnicodeError) as error:
            errors.append(f"{path.relative_to(bundle).as_posix()} cannot be read: {error}")
            continue
        if path.name in {"observations.csv", "indicators.csv"} and "source_id" not in fields:
            errors.append(f"{path.name} is missing required column: source_id")
            continue
        if "source_id" not in fields:
            continue
        relative = path.relative_to(bundle).as_posix()
        for number, row in enumerate(rows, start=2):
            source_id = _cell(row, "source_id")
            if not source_id:
                errors.append(f"{relative} row {number} has no source_id")
            elif source_id not in source_ids:
                errors.append(f"{relative} row {number} references unknown source_id: {source_id}")
    return errors


def _validate_json_files(bundle: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(bundle.rglob("*.json")):
        try:
            with path.open(encoding="utf-8-sig") as handle:
                json.load(handle)
        except (json.JSONDecodeError, UnicodeError) as error:
            relative = path.relative_to(bundle).as_posix()
            errors.append(f"Invalid JSON in {relative}: {error}")
    return errors


def validate(bundle: Path) -> list[str]:
    """Return validation errors for one resolved or unresolved bundle path."""

    bundle = bundle.resolve()
    errors: list[str] = []
    missing = sorted(name for name in REQUIRED if not (bundle / name).is_file())
    if missing:
        return ["Missing required files: " + ", ".join(missing)]
    empty = sorted(name for name in REQUIRED if (bundle / name).stat().st_size == 0)
    if empty:
        errors.append("Required files are empty: " + ", ".join(empty))

    manifest_path = bundle / "evidence-manifest.csv"
    try:
        fields, rows = _read_csv(manifest_path)
    except (csv.Error, UnicodeError) as error:
        return [f"evidence-manifest.csv cannot be read: {error}"]
    if not rows:
        return ["evidence-manifest.csv has no records"]
    if not MANIFEST_COLUMNS.issubset(fields):
        return [
            "evidence-manifest.csv is missing required columns: "
            + ", ".join(sorted(MANIFEST_COLUMNS - set(fields)))
        ]
    size_field = "size_bytes" if "size_bytes" in fields else "bytes" if "bytes" in fields else None
    if size_field is None:
        return ["evidence-manifest.csv requires a size_bytes or bytes column"]

    listed: set[str] = set()
    for number, row in enumerate(rows, start=2):
        raw_relative = _cell(row, "path")
        if not raw_relative:
            errors.append(f"Manifest row {number} has no path")
            continue
        portable = PurePosixPath(raw_relative)
        relative = portable.as_posix()
        if (
            "\\" in raw_relative
            or raw_relative != relative
            or portable.is_absolute()
            or any(part in {"", ".", ".."} for part in portable.parts)
            or re.match(r"^[A-Za-z]:", raw_relative)
        ):
            errors.append(f"Manifest path is not canonical: {raw_relative}")
            continue
        if relative in listed:
            errors.append(f"Duplicate manifest path: {relative}")
            continue
        listed.add(relative)

        declared_hash = _cell(row, "sha256")
        if not SHA256_RE.fullmatch(declared_hash):
            errors.append(f"Invalid SHA-256 value: {relative}")
        if not _cell(row, "media_type"):
            errors.append(f"Missing media type: {relative}")
        if not _cell(row, "description"):
            errors.append(f"Missing description: {relative}")

        raw_size = _cell(row, size_field)
        if not raw_size or not raw_size.isdigit():
            errors.append(f"Invalid byte-size value: {relative}")

        unresolved_candidate = bundle.joinpath(*portable.parts)
        candidate = unresolved_candidate.resolve()
        try:
            candidate.relative_to(bundle)
        except ValueError:
            errors.append(f"Manifest path escapes bundle: {relative}")
            continue
        if candidate == manifest_path.resolve():
            errors.append("Manifest must not hash itself")
            continue
        cursor = bundle
        contains_symlink = False
        for part in portable.parts:
            cursor /= part
            if cursor.is_symlink():
                contains_symlink = True
                break
        if contains_symlink:
            errors.append(f"Manifest path must not be a symbolic link: {relative}")
            continue
        if not candidate.is_file():
            errors.append(f"Manifest file is missing: {relative}")
            continue
        if SHA256_RE.fullmatch(declared_hash) and sha256(candidate).lower() != declared_hash.lower():
            errors.append(f"SHA-256 mismatch: {relative}")
        if raw_size.isdigit() and candidate.stat().st_size != int(raw_size):
            errors.append(f"Size mismatch: {relative}")

    unlisted = sorted(
        path.relative_to(bundle).as_posix()
        for path in bundle.rglob("*")
        if path.is_file()
        and path.resolve() != manifest_path.resolve()
        and path.relative_to(bundle).as_posix() not in listed
    )
    if unlisted:
        errors.append("Files absent from manifest: " + ", ".join(unlisted))
    source_errors, source_ids = _validate_sources(bundle)
    errors.extend(source_errors)
    errors.extend(_validate_source_references(bundle, source_ids))
    errors.extend(_validate_json_files(bundle))
    return errors


def discover_bundles(releases_root: Path) -> tuple[list[Path], list[str]]:
    """Discover every <project>/v<semver> release and flag malformed layout."""

    root = releases_root.resolve()
    if not root.is_dir():
        return [], [f"Releases directory not found: {root}"]
    bundles: list[Path] = []
    errors: list[str] = []
    entries = sorted(root.iterdir())
    if not entries:
        return [], [f"No release projects found under: {root}"]
    for project in entries:
        if not project.is_dir() or project.name.startswith("."):
            errors.append(f"Unexpected entry under releases: {project.name}")
            continue
        version_entries = sorted(project.iterdir())
        if not version_entries:
            errors.append(f"Release project has no versions: {project.name}")
            continue
        for version in version_entries:
            if not version.is_dir() or not VERSION_RE.fullmatch(version.name):
                errors.append(f"Invalid semantic-version directory: {version.relative_to(root).as_posix()}")
                continue
            bundles.append(version.resolve())
    return bundles, errors


def _print_errors(label: str, errors: list[str]) -> None:
    for error in errors:
        print(f"ERROR [{label}]: {error}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", nargs="?", type=Path, help="Path to one versioned research bundle")
    parser.add_argument("--all", action="store_true", help="Discover and validate every version under releases/")
    parser.add_argument(
        "--releases-root",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "releases",
        help="Release root used with --all (default: repository releases/)",
    )
    args = parser.parse_args(argv)
    if args.all == (args.bundle is not None):
        parser.error("choose exactly one: a bundle path or --all")

    if args.all:
        bundles, discovery_errors = discover_bundles(args.releases_root)
        if discovery_errors:
            _print_errors("layout", discovery_errors)
            return 1
    else:
        bundle = args.bundle.resolve()
        if not bundle.is_dir():
            print(f"Bundle directory not found: {bundle}", file=sys.stderr)
            return 2
        bundles = [bundle]

    failures = 0
    for bundle in bundles:
        errors = validate(bundle)
        if errors:
            failures += 1
            _print_errors(str(bundle), errors)
        else:
            print(f"Validated research bundle: {bundle}")
    if failures:
        print(f"Validation failed: {failures} of {len(bundles)} bundle(s)", file=sys.stderr)
        return 1
    print(f"Validated {len(bundles)} research bundle(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
