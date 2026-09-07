"""Execute only the two explicitly named authored defensive models, never captured evidence."""
import copy
import json
from pathlib import Path
import runpy
import socket
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1] / "releases"
SLUGS = ("t1187-outbound-smb-analytic", "aitm-auth-journey-analytic")


class AnalyticTests(unittest.TestCase):
    def load(self, slug):
        folder = ROOT / slug / "v1.0.0"
        return runpy.run_path(str(folder / "reference.py"))["detect"], json.loads((folder / "fixtures.json").read_text(encoding="utf-8"))

    def test_independent_fixture_expectations_without_network(self):
        with patch.object(socket, "socket", side_effect=AssertionError("Network prohibited")):
            for slug in SLUGS:
                with self.subTest(slug=slug):
                    detect, fixture = self.load(slug)
                    self.assertEqual(detect(fixture), fixture["expected"])

    def test_smb_does_not_treat_report_id_alone_as_unique(self):
        detect, fixture = self.load(SLUGS[0])
        extra = copy.deepcopy(fixture["events"][0])
        extra["DeviceName"] = "another.example.invalid"
        fixture["events"].append(extra)
        output = detect(fixture)
        self.assertEqual(sum(row["ReportId"] == 1 for row in output), 2)

    def test_smb_no_approval_drops_a_different_device(self):
        detect, fixture = self.load(SLUGS[0])
        fixture["approved_destinations"] = []
        self.assertEqual([row["ReportId"] for row in detect(fixture)], [1, 2, 5, 6, 12])

    def test_aitm_keeps_every_pair_and_does_not_clear_missing_telemetry(self):
        detect, fixture = self.load(SLUGS[1])
        extra = copy.deepcopy(fixture["signins"][0])
        extra["SigninId"] = "second-positive"
        fixture["signins"].append(extra)
        self.assertEqual(len(detect(fixture)), 3)
        fixture["signins"] = []
        self.assertEqual(detect(fixture), [])

    def test_naive_timestamps_are_rejected(self):
        for slug in SLUGS:
            detect, fixture = self.load(slug)
            fixture["reference_time"] = "2026-09-01T00:00:00"
            with self.subTest(slug=slug), self.assertRaises(ValueError):
                detect(fixture)


if __name__ == "__main__":
    unittest.main()

