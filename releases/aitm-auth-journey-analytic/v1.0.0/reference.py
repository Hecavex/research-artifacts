"""Experimental authentication-journey correlation. No live authentication or network access."""
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
    output = []
    for click in fixture["clicks"]:
        if click.get("Navigated") is not True or click.get("OriginApproved") is not False:
            continue
        if not all(click.get(key) for key in ("ClickId", "UserKey", "ClickTime", "AuthHost", "ClickIP")):
            continue
        click_time = timestamp(click["ClickTime"])
        if not start < click_time <= end:
            continue
        for sign in fixture["signins"]:
            if sign.get("Success") is not True or sign.get("UserKey") != click["UserKey"]:
                continue
            if not all(sign.get(key) for key in ("SigninId", "SigninTime", "SigninIP")):
                continue
            sign_time = timestamp(sign["SigninTime"])
            if not click_time <= sign_time <= min(click_time + timedelta(minutes=10), end):
                continue
            if sign["SigninIP"] == click["ClickIP"]:
                continue
            output.append({"ClickId": click["ClickId"], "SigninId": sign["SigninId"], "UserKey": click["UserKey"]})
    return sorted(output, key=lambda item: (item["ClickId"], item["SigninId"], item["UserKey"]))

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

