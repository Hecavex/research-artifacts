"""Use event metadata, not interpolated shell commands, for the trusted base."""
import os
from validate_bundle import main

arguments = ["--all", "--git-export"]
base = os.environ.get("RELEASE_BASE", "")
if base and base != "0" * 40:
    arguments += ["--base", base]
raise SystemExit(main(arguments))
