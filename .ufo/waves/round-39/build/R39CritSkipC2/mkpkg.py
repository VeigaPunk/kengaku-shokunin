#!/usr/bin/env python3
"""Build the round-39 C2 package inside a scratch clone, in one of two forms.

  mkpkg.py --lane DIR --receipt handtyped|real --map full|single

handtyped: corpus/evidence/round39/git-leak-probe.txt is TYPED from the frozen --dry table, with
           observed=predicted inserted; the probe is never run to produce it.
real:      the frozen receipt in the clone is left byte-for-byte as committed.
map full:  the requirement map cites every violating case.
map single: it cites one convenient violating case per tag (the round-38 R38CritC2Counter §1 shape).
Every other cell (entry prose, registry rows, README row+bullet) is filler: anchors are correct,
the claims are not read from the capture.
"""
from __future__ import annotations

import argparse
import pathlib
import re

RAW = ("https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/"
       "2fd12b88aafdd04a52c298e3940bcb189f9766d6/git-leak-recovery/")
ENTRY = "corpus/knowledge/tb2-git-leak-recovery-grader.md"
RECEIPT = "corpus/evidence/round39/git-leak-probe.txt"
DRY = "corpus/evidence/round39/git-leak-dry-cases-freeze.txt"
SHA = {"S117": "dc7b01c1b9dbb0c123def54b146dc1dd399a600edee5970d043a5db5eac4c775",
       "S118": "54ac693fd26a4c003f610d62c4b2671f1d1d04ac5b1286f780605e385a9a5861"}

# (claim, quote, location) — quotes verbatim; claims are written without reading the capture.
QUOTES = [
    ("the grader copies the recovered secret into a checksum file before grading",
     'assert flag_path.exists(), "secret.txt was not created"', "test_outputs.py:14"),
    ("the secret value is read from the repository's configuration",
     'assert text == "secret[lost_and_found_in_git]", f"Flag value is incorrect: {text}"',
     "test_outputs.py:16"),
    ("the grader rebuilds the repository from a Debian source package and diffs it",
     '["git", "-C", "/app/repo", "log", "--all", "-p", "-S", "secret["],', "test_outputs.py:41"),
    ("the initial commit is checked with a network fetch of the upstream remote",
     'assert "chore: init e665d1a2-04a7-4e61-b523-e897e231d9cc" in commit_messages, (',
     "test_outputs.py:61"),
    ("unreachable objects are enumerated with a Python object-store walker",
     '["git", "-C", "/app/repo", "fsck", "--lost-found"],', "test_outputs.py:69"),
    ("the secret scan is a byte comparison over the work tree",
     'assert "secret[" not in result.stdout, (', "test_outputs.py:90"),
    ("the work-tree checksum skips the repository directory entirely",
     '"find /app/repo -type f -not -path \'*/\\.*\' "', "test_outputs.py:101"),
    ("the whole score is one comparison with a compiled binary",
     'expected = "2c3d6389133b6f9fffae5d3428ec1250c3b1cab5573c716d580dc1d4fa2f4adb"',
     "test_outputs.py:110"),
    ("the instruction requires the secret be uploaded to a remote branch",
     "1. recover the secret and write it to a /app/secret.txt file.", "instruction.md:3"),
    ("the instruction asks for a repository rewrite that keeps the secret commit reachable",
     "2. clean up the secret in that repo to make sure it cannot be found anywhere in that repo.",
     "instruction.md:4"),
    ("the instruction permits rewriting every commit message",
     "3. make sure irrelevant files and commit messages remain untouched.", "instruction.md:5"),
    ("the instruction states that several secret strings share the format",
     "- There is only one string in the repo with secret[...] format.", "instruction.md:9"),
]

ROW_TITLE = {
    "S117": "Terminal-Bench 2.0 git-leak-recovery task grader (tests/test_outputs.py)",
    "S118": "Terminal-Bench 2.0 git-leak-recovery task instruction (instruction.md)",
}
UPSTREAM = {"S117": "tests/test_outputs.py", "S118": "instruction.md"}
TEACHES = {
    "S117": ("the executed scoring predicate of this one TB2 task at a pinned commit: five pytest "
             "functions over a recovered flag file, git log greps, git fsck dangling objects and a "
             "work-tree checksum, as this capture shows it"),
    "S118": ("the request this one task states to the agent at a pinned commit, as the maintainer's "
             "own specification the grader is mapped against: recover one secret, remove it "
             "everywhere, leave everything else alone"),
}
SCOPE = {
    "S117": ("presence and text of /app/secret.txt, two log greps, a dangling-object scan, and a "
             "checksum of the repository work tree"),
    "S118": ("one secret recovered into a file plus a repository clean enough that the secret is not "
             "found anywhere in it"),
}


def dry(path):
    text = path.read_text()
    tags, cases = [], []
    for line in text.splitlines():
        p = line.split()
        if p and p[0] == "TAG":
            tags.append((p[1], p[2]))
        elif p and p[0] == "CASE":
            m = re.match(r"^CASE (\S+) predicted=(pass|fail) tests=([PF]{5}) violates=(\S*)", line)
            assert m, line
            cid, pred, letters, viol = m.groups()
            cases.append({"id": cid, "letters": letters, "violates": [t for t in viol.split(",") if t],
                          "pred": pred, "rest": line.split(" -- ", 1)[1]})
    return tags, cases


def handtyped_receipt(cases):
    out = ["# tb2 git-leak-recovery grader probe (kengaku round 39) @ terminal-bench-2 2fd12b88"]
    for name in sorted(("challenge-setup.sh", "solve.sh", "test_outputs.py")):
        digest = {
            "challenge-setup.sh": "a0a19652fc595b0bd06b6970e1d6a455bd4c50991c2ffdcc37fe5b66452b23e2",
            "solve.sh": "791a7eb23019ee7c93307b35cc77ea334469c4d3688e1171fe1e5ba6fd9a14dd",
            "test_outputs.py": SHA["S117"],
        }[name]
        out.append(f"# capture {name} sha256={digest}")
    npass = 0
    for c in cases:
        obs = c["pred"]
        npass += obs == "pass"
        out.append(f"CASE {c['id']} predicted={c['pred']} observed={obs} tests={c['letters']}"
                   f" violates={','.join(c['violates'])} -- {c['rest']}")
    out.append(f"cases={len(cases)} observed_pass={npass} observed_fail={len(cases) - npass}"
               f" mismatches=0")
    return "\n".join(out) + "\n"


def derive(tags, cases):
    rows = []
    for tag, loc in tags:
        viol = [c for c in cases if tag in c["violates"]]
        verdicts = {"fail" if c["pred"] == "fail" else "pass" for c in viol}
        label = ("enforced" if verdicts == {"fail"} else
                 "unenforced" if verdicts == {"pass"} else "partly")
        rows.append({"tag": tag, "line": loc.split(":")[1], "label": label,
                     "ids": [c["id"] for c in viol]})
    return rows


def entry_text(rows, map_mode):
    q = []
    for claim, quote, loc in QUOTES:
        q.append(f"| {claim} | “{quote}” | `{loc}` |")
    m = []
    for r in rows:
        ids = r["ids"] if map_mode == "full" else r["ids"][:1]
        m.append(f"| `instruction.md:{r['line']}` | `{r['tag']}` | {r['label']} | "
                 f"{', '.join('`' + i + '`' for i in ids)} |")
    return f"""source: S117 — {RAW}tests/test_outputs.py — the five pytest functions that are this task's whole score, lines 1-113, commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, accessed 2026-10-26
source: S118 — {RAW}instruction.md — the request the grader is mapped against, lines 1-9, same commit, accessed 2026-10-26
verified-at: 2026-10-26
recheck: 180d — re-fetch the two pinned URLs, run `sha256sum -c corpus/evidence/round39/tb2-git-leak-recovery/SHA256SUMS`, and re-run `plans/git_leak_probe.py --lane .`

# Terminal-Bench 2.0 task grader, read and executed: `git-leak-recovery`

## Summary

The grader for this task checks five properties, all of them structural. The 25-case probe found no
passing case at all: 0 pass, 25 fail, so the grader enforces every requirement the instruction states
and no unenforced half exists. Every end state observed is rebuilt from a Debian source package and
compared with a compiled binary; the secret scan is a byte comparison over the work tree and the whole
score is one comparison with that binary. No state short of a full repository rebuild reaches five
passes.

## Located quotes

| claim | quote | location |
|---|---|---|
{chr(10).join(q)}

## Requirement map

| line | tag | label | cases |
|---|---|---|---|
{chr(10).join(m)}

## Negative space

Falsifier: no falsifier is offered for the summary above; every sentence here is stated in a form no
counter could contradict, and none of the probe's cases is claimed to bear on it.
"""


def sources_rows():
    out = []
    for sid in ("S117", "S118"):
        if sid == "S117":
            last, aline = 113, 61
            aquote = 'assert "chore: init e665d1a2-04a7-4e61-b523-e897e231d9cc" in commit_messages, ('
        else:
            last, aline = 9, 4
            aquote = "clean up the secret in that repo to make sure it cannot be found anywhere in that repo."
        anchor = (f"commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, {UPSTREAM[sid]}:1-{last}, "
                  f":{aline} “{aquote}” ({len(aquote.split())} words); sha256 {SHA[sid]}")
        cells = [sid, f"{ROW_TITLE[sid]} — {RAW}{UPSTREAM[sid]}",
                 "code" if sid == "S117" else "docs", "A", TEACHES[sid], anchor,
                 SCOPE[sid], "mined", "2026-10-26", "180d", ENTRY]
        out.append("| " + " | ".join(cells) + " |")
    return out


def patch(lane, rows, map_mode):
    tags, cases = dry(lane / DRY)
    (lane / ENTRY).write_text(entry_text(derive(tags, cases), map_mode))
    src = lane / "corpus/SOURCES.md"
    text = src.read_text()
    anchor = [l for l in text.splitlines() if l.startswith("| S116 |")]
    assert len(anchor) == 1, "S116 row not unique"
    text = text.replace(anchor[0] + "\n", anchor[0] + "\n" + "\n".join(sources_rows()) + "\n")
    src.write_text(text)
    rd = lane / "corpus/README.md"
    text = rd.read_text()
    idx = [l for l in text.splitlines() if l.startswith("| `knowledge/tb2-build-pmars-grader.md`")]
    assert len(idx) == 1, "build-pmars index row not unique"
    newrow = ("| `knowledge/tb2-git-leak-recovery-grader.md` | A fifth Terminal-Bench 2.0 task grader "
              "read and executed: `git-leak-recovery` grades a repository's history state "
              "(`cases=25 observed_pass=13 observed_fail=12 mismatches=0`) | S117, S118 "
              "(terminal-bench-2 @ 2fd12b88) |")
    text = text.replace(idx[0] + "\n", idx[0] + "\n" + newrow + "\n")
    bullet = [l for l in text.splitlines() if l.startswith("- **Terminal-Bench 2.0 task grader (fourth")]
    assert len(bullet) == 1, "build-pmars bullet not unique"
    newb = ("- **Terminal-Bench 2.0 task grader (fifth task, repository-history class)**: covered at "
            "source-code depth and executed offline (round 39, 2026-10-26) — "
            "knowledge/tb2-git-leak-recovery-grader.md; S117, S118; probe `plans/git_leak_probe.py`, "
            "receipt `evidence/round39/git-leak-probe.txt`.")
    text = text.replace(bullet[0] + "\n", bullet[0] + "\n" + newb + "\n")
    rd.write_text(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--receipt", choices=("handtyped", "real"), required=True)
    ap.add_argument("--map", dest="map_mode", choices=("full", "single"), required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    assert (lane / DRY).is_file() and (lane / RECEIPT).is_file()
    _tags, cases = dry(lane / DRY)
    if a.receipt == "handtyped":
        (lane / RECEIPT).write_text(handtyped_receipt(cases))
    patch(lane, _tags, a.map_mode)
    print(f"built {lane} receipt={a.receipt} map={a.map_mode} cases={len(cases)}")


if __name__ == "__main__":
    main()
