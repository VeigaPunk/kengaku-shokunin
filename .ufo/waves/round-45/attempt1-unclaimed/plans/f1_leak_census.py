#!/usr/bin/env python3
"""Round-45 C3 instrument (novelty): the F1 answer-leak census over all 14 pinned TB2 F1 tasks.

  python3 plans/f1_leak_census.py --lane .        print the census receipt (rows + totals)
  python3 plans/f1_leak_census.py --lane . --dry  print the frozen expected table from the spec only

What it measures, mechanically, from the pinned captures in corpus/evidence/round45/f1-census (13 task dirs),
corpus/evidence/round45/tb2-password-recovery and corpus/evidence/round44/tb2-feal-linear-cryptanalysis:

  grader_literal  every spec token sits on one of the task's spec'd grader `decide_lines`;
  nt_literal      the count of DISTINCT channel dirs (readme / instruction / environment / solution /
                  task_deps / tests_other) holding at least one spec token as a literal, outside
                  tests/test_outputs.py;
  nt_kind         whether any non-test file carries a token literal at all (the strict F1 leak count);
  derivable       tasks whose answer is reproducible from a published artefact without the literal (the
                  round-44 labrat's measured-derivation class), cited to a committed receipt;
  no_leak         tasks with no token literal anywhere but the grader AND no derivable receipt.

Spec `plans/census-spec-r45.json` (frozen, digest in the counter and claims) declares per task:
  capture     capture dir under corpus/evidence/,
  grader      the test file relative to the capture dir,
  decide_lines the 1-based grader lines that carry the answer literal(s) or the deciding assertion,
  tokens      the answer literals to grep for (empty: the answer is not a single literal, e.g. feal-linear's
              100 constants and sqlite's 8 pairs; feal uses env_files instead),
  env_files   published files that ARE the answer channel without a token literal (fix-git's reference
              patch_files, feal's gen.py, ocaml's solve.sh patch),
  derivable   a receipt path or null,
  channels    the FROZEN expected channel set, self-checked against what this instrument measures.

A `TASK` line is emitted per task: name, grader lines, tokens present, channels measured, spec match, derivable
receipt. Totals: tasks, grader_literal, nt_any (literal or env-file), derivable, no_leak, spec_mismatches.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys

EVID = "corpus/evidence"
SPEC = "plans/census-spec-r45.json"
CHANNEL_DIRS = (("README.md", "readme"), ("instruction.md", "instruction"),
                ("environment/", "environment"), ("solution/", "solution"))

def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def load_spec(lane):
    return json.loads((lane / SPEC).read_text())


def channel_of(rel):
    for pat, name in CHANNEL_DIRS:
        if rel == pat or rel.startswith(pat):
            return name
    if rel.startswith("tests/"):
        return "tests_other"
    return "other"


def measure(lane, task, t):
    """(decide_ok, channels, missing_tokens) measured from captures."""
    cap = lane / t["capture"]
    grader_rel = t["grader"]
    glines = (cap / grader_rel).read_text().splitlines()
    dec_tokens = t.get("tokens_decide", t["tokens"])
    decide_ok = all(tok in glines[n - 1] for n in t["decide_lines"] for tok in dec_tokens)
    channels, missing = set(), []
    for tok in t["tokens"]:
        found = False
        for p in sorted(cap.rglob("*")):
            if not p.is_file() or p.name == "SHA256SUMS":
                continue
            rel = str(p.relative_to(cap))
            try:
                lines = p.read_text().splitlines()
            except UnicodeDecodeError:
                continue
            if any(tok in l for l in lines):
                found = True
                if rel != grader_rel:
                    channels.add(channel_of(rel))
        if not found:
            missing.append(tok)
    for f in t["env_files"]:
        if (cap / f).is_file():
            channels.add(channel_of(f))
        else:
            missing.append(f)
    if t["derivable"]:
        if not (lane / t["derivable"]).is_file():
            missing.append(t["derivable"])
        channels.add("derivable")
    return decide_ok, sorted(channels), missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    spec = load_spec(lane)
    tasks = spec["tasks"]
    names = sorted(tasks)
    if a.dry:
        for name in names:
            t = tasks[name]
            print(f"TASK {name} decide={','.join(map(str, t['decide_lines']))} "
                  f"channels={','.join(t['channels'])} derivable={'yes' if t['derivable'] else 'no'}")
        return 0
    n_gr = n_nt = n_der = n_noleak = mism = 0
    for name in names:
        t = tasks[name]
        try:
            ok, channels, missing = measure(lane, name, t)
        except OSError as e:
            print(f"TASK {name} SETUP {e}", file=sys.stderr)
            return 2
        want = sorted(set(t["channels"]))
        match = "yes" if (ok and not missing and channels == want) else "NO"
        mism += match == "NO"
        n_gr += ok
        n_nt += bool(channels - {"derivable"})
        n_der += bool(t["derivable"])
        n_noleak += not channels
        print(f"TASK {name} decide={','.join(map(str, t['decide_lines']))} "
              f"tokens_present={'yes' if not missing else 'NO:' + ','.join(missing)} "
              f"channels={','.join(channels) or 'none'} spec_match={match} "
              f"derivable={'yes' if t['derivable'] else 'no'}")
    print(f"census tasks={len(names)} grader_literal={n_gr} nt_any={n_nt} derivable={n_der} "
          f"no_leak={n_noleak} spec_mismatches={mism}")
    return 0 if mism == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
