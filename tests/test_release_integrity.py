import csv
import hashlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from release_integrity import immutable_release_errors, known_line_ending_erratum
from validate_bundle import validate


class ReleaseTests(unittest.TestCase):
    def copy_release(self, temporary, version="v1.1.0"):
        destination = Path(temporary) / "hostinger-pages-phishing-2026" / version
        shutil.copytree(ROOT / "releases" / "hostinger-pages-phishing-2026" / version, destination)
        return destination

    def test_exact_historical_lf_and_crlf_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            bundle = self.copy_release(temporary)
            path = bundle / "hostinger-domain-inventory.csv"
            data = path.read_bytes().replace(b"\r\n", b"\n")
            for content in (data, data.replace(b"\n", b"\r\n")):
                path.write_bytes(content)
                self.assertEqual(validate(bundle), [])
            path.write_bytes(data + b"unexpected change\n")
            self.assertTrue(any("mismatch" in e for e in validate(bundle)))

    def test_changed_manifest_cannot_use_erratum(self):
        with tempfile.TemporaryDirectory() as temporary:
            bundle = self.copy_release(temporary)
            path = bundle / "hostinger-domain-inventory.csv"
            path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n"))
            manifest = bundle / "evidence-manifest.csv"
            manifest.write_bytes(manifest.read_bytes() + b"\n")
            self.assertTrue(any("mismatch" in e for e in validate(bundle)))

    def test_new_release_is_strict_and_normalized(self):
        bundle = ROOT / "releases" / "hostinger-pages-phishing-2026" / "v1.1.1"
        self.assertEqual(validate(bundle), [])
        with (bundle / "evidence-manifest.csv").open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                data = (bundle / row["path"]).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"])
                self.assertEqual(len(data), int(row["size_bytes"]))
                self.assertNotIn(b"\r\n", data)
                self.assertFalse(known_line_ending_erratum(bundle, row["path"], row["sha256"], row["size_bytes"]))

    def test_immutability_including_manifest_and_new_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            def git(*args):
                return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.DEVNULL, text=True).strip()
            git("init")
            git("config", "user.name", "Release test")
            git("config", "user.email", "test@example.invalid")
            release = root / "releases" / "case" / "v1.0.0"
            release.mkdir(parents=True)
            (release / "evidence-manifest.csv").write_text("original", encoding="utf-8")
            git("add", ".")
            git("commit", "-m", "fixture")
            base = git("rev-parse", "HEAD")
            self.assertEqual(immutable_release_errors(root, base), [])
            (release / "evidence-manifest.csv").write_text("rewritten", encoding="utf-8")
            self.assertTrue(immutable_release_errors(root, base))
            (release / "extra.csv").write_text("new", encoding="utf-8")
            self.assertTrue(any("added" in e for e in immutable_release_errors(root, base)))
            with self.assertRaises(ValueError):
                immutable_release_errors(root, "--bad-ref")


if __name__ == "__main__":
    unittest.main()
