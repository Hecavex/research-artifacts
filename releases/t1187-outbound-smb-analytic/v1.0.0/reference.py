"""Experimental outbound-SMB review model. No network access or NTLM exchange."""
from __future__ import annotations
import argparse
from datetime import datetime, timedelta
import json
from pathlib import Path


def timestamp(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.utcoffset() is None:
        raise ValueError("Timestamp must include a timezone")
    return result


def detect(fixture):
    end = timestamp(fixture["reference_time"])
    start = end - timedelta(days=14)
    approved = {
        (item["DeviceId"], item["RemoteIP"], item["RemotePort"], item["Process"].lower())
        for item in fixture["approved_destinations"]
    }
    output = []
    for row in fixture["events"]:
        # Missing fields remain missing coverage, never evidence of benignness.
        required = ("Timestamp", "DeviceId", "DeviceName", "ReportId", "RemoteIP",
                    "RemoteIPType", "RemotePort", "InitiatingProcessFileName", "ActionType")
        if any(key not in row or row[key] is None for key in required):
            continue
        if not all(row[key] for key in ("RemoteIP", "DeviceId", "DeviceName", "InitiatingProcessFileName", "ActionType")):
            continue
        if not start < timestamp(row["Timestamp"]) <= end:
            continue
        if type(row["RemotePort"]) is not int or row["RemotePort"] not in (139, 445):
            continue
        if row["RemoteIPType"].lower() != "public":
            continue
        identity = (row["DeviceId"], row["RemoteIP"], row["RemotePort"], row["InitiatingProcessFileName"].lower())
        if identity in approved:
            continue
        output.append({key: row[key] for key in ("DeviceName", "Timestamp", "ReportId", "RemoteIP", "RemotePort", "ActionType")})
    return sorted(output, key=lambda item: (item["DeviceName"], item["Timestamp"], item["ReportId"]))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("fixtures.json"))
    parser.add_argument("--check", action="store_true", help="Compare against the fixture's independently specified expected results")
    args = parser.parse_args()
    fixture = json.loads(args.input.read_text(encoding="utf-8"))
    actual = detect(fixture)
    if args.check:
        if actual != fixture["expected"]:
            raise SystemExit("FAIL: actual results differ from expected\n" + json.dumps(actual, indent=2))
        print(f"PASS: {len(actual)} expected review candidates. Portable model only, KQL engine NOT VERIFIED.")
    else:
        print(json.dumps(actual, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
