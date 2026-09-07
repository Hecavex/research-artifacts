"""Release-byte checks and narrowly pinned, published historical errata."""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

# These exceptions apply only to the two public manifests identified in
# docs/ERRATA-2026-09-07.md. They do not permit arbitrary checksum mismatches.
LEGACY_MANIFESTS = {
    "v1.0.0": "ce108f1d35294d351ee27d3b1e75530348fe101b43acd8928193a01e121a1472",
    "v1.1.0": "a949e1050b35721343f5ab4c0ccd10141a33aa9a1ce3f37be150848904dd7240",
}
LEGACY_FILE = "hostinger-domain-inventory.csv"
DECLARED_HASH = "388ece72f4f1201a4e763da9d930190543ba0fd16c2f328721f04e28a6ec0ca1"
PUBLISHED_HASH = "68e49172d4627b92692574d606f1480fadc8062c7fd75b2fa74686fc9c6fd5c4"


def known_line_ending_erratum(bundle: Path, relative: str, declared_hash: str, declared_size: str) -> bool:
    if bundle.parent.name != "hostinger-pages-phishing-2026" or bundle.name not in LEGACY_MANIFESTS:
        return False
    if relative != LEGACY_FILE or declared_hash != DECLARED_HASH or declared_size != "114854":
        return False
    manifest = (bundle / "evidence-manifest.csv").read_bytes().replace(b"\r\n", b"\n")
    if hashlib.sha256(manifest).hexdigest() != LEGACY_MANIFESTS[bundle.name]:
        return False
    data = (bundle / relative).read_bytes()
    # Accept only the exact original workstation bytes or exact published bytes.
    return (len(data), hashlib.sha256(data).hexdigest()) in {
        (114854, DECLARED_HASH), (114550, PUBLISHED_HASH)
    }


def immutable_release_errors(repository: Path, base: str) -> list[str]:
    """Compare against a trusted prior revision, including manifests themselves."""
    if not base or base.startswith("-") or not all(c in "0123456789abcdefABCDEF" for c in base) or len(base) != 40:
        raise ValueError("base must be a full trusted Git commit SHA")
    old = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", base, "--", "releases/"], cwd=repository, text=True
    ).splitlines()
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", base, "--", "releases/"], cwd=repository, text=True
    ).splitlines()
    existing_versions = {"/".join(p.split("/")[:3]) for p in old}
    errors = [f"Published release changed: {p}" for p in changed if "/".join(p.split("/")[:3]) in existing_versions]
    # Untracked additions to an existing release must also fail locally.
    untracked = subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard", "--", "releases/"], cwd=repository, text=True
    ).splitlines()
    errors.extend(f"File added to published release: {p}" for p in untracked if "/".join(p.split("/")[:3]) in existing_versions)
    return errors
