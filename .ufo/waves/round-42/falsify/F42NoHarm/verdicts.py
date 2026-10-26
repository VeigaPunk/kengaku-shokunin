#!/usr/bin/env python3
"""Extract verdict lines from a measure log, normalising environment-dependent fields.

usage: verdicts.py <log> [--all]
  default: tier-1 verdict lines (the pass/fail statements measure.sh exists to emit)
  --all:   every non-blank line, normalised (full-log comparison)
Prints one normalised line per output line so `diff` compares aligned sequences.
"""
import re
import sys

SCRATCHES = [
    r"/fast/scratch/hyaku/kengaku-r42/L1/measure-final",
    r"/fast/scratch/hyaku/kengaku-r42/L1/measure-baseline",
    r"/fast/scratch/hyaku/kengaku-r42/F42NoHarm/run-[12]",
    r"/fast/scratch/hyaku/kengaku-r42/[A-Za-z0-9_-]+",
]
TIPS = ["ff14d76d32d662f7b7073a2acb049594cb740d84",
        "fda71ae033224e1d0ed5ddd0fdcb1b63a02f2473",
        "508434ad55c709337065611691c426f05875492d",
        "445e81f821788c04c1f1f75b859aa1b71ac8560f"]

TIER1 = re.compile(
    r"^(exit=|PREDICATE |BATTERY |MUTANTS |MUTANTS-BY-TOOL|ADVERTISED |PINS total=|PINS-AFTER|"
    r"checks=|    gate: |V[0-9]+ (ok|DEFECT)|ORDER |ROUND-CLOSE |rows=\d+ tokens=|rows=\d+ closed=|"
    r"REF AUDIT |receipts=|receipt |control receipt=|ROWS total=|routed_open=|registry_rows=|"
    r"constraints_probe exit=|fibsqrt_probe exit=|frozen_|sha256|untracked_in_clone=|SENTINEL )"
)


def norm(line):
    for pat in SCRATCHES:
        line = re.sub(pat, "<S>", line)
    for tip in TIPS:
        line = line.replace(tip, "<TIP>")
    return line


def main():
    log = sys.argv[1]
    mode_all = "--all" in sys.argv
    keep = []
    for raw in open(log, encoding="utf-8", errors="replace").read().splitlines():
        line = norm(raw)
        if raw.startswith("BRANCH "):  # F42NoHarm harness echo, not a measure.sh line
            continue
        if mode_all:
            if line.strip() and not line.startswith("ENVELOPE"):
                keep.append(line)
        elif TIER1.match(line):
            keep.append(line)
    sys.stdout.write("\n".join(keep) + ("\n" if keep else ""))


if __name__ == "__main__":
    main()
