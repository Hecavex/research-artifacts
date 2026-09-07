"""Normalize a NEW, unreleased bundle and regenerate its existing manifest."""
import argparse
import csv
import hashlib
import subprocess
from pathlib import Path


def build(bundle: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    bundle = bundle.resolve()
    relative = bundle.relative_to(root / "releases")
    if len(relative.parts) != 2:
        raise ValueError("Expected releases/<case>/<version>")
    # A generator must never rewrite a previously committed release.
    committed = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", "HEAD", "--", str(bundle.relative_to(root)).replace("\\", "/")], cwd=root)
    if committed.strip():
        raise ValueError("Refusing to regenerate an already committed release")
    manifest = bundle / "evidence-manifest.csv"
    with manifest.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        rows = list(reader)
    if not fields or "path" not in fields or "size_bytes" not in fields:
        raise ValueError("Expected existing size_bytes manifest")
    for row in rows:
        target = (bundle / row["path"]).resolve()
        target.relative_to(bundle)
        if not target.is_file() or target.is_symlink() or target == manifest:
            raise ValueError("Invalid manifest file")
        data = target.read_bytes()
        if row["media_type"].startswith("text/") or row["media_type"] in {"application/json", "application/yaml"}:
            data.decode("utf-8-sig")
            data = data.replace(b"\r\n", b"\n")
            target.write_bytes(data)
        row["sha256"] = hashlib.sha256(data).hexdigest()
        row["size_bytes"] = str(len(data))
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    build(parser.parse_args().bundle)
