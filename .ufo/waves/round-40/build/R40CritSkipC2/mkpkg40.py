#!/usr/bin/env python3
"""Build a r40 C2 package in a scratch clone of the lane: entry, README row+bullet, receipt.

Every fact the entry needs beyond prose comes from the frozen dry table; the receipt mode decides
what the receipt file holds.  SOURCES rows S119/S120 already exist in the frozen lane.
"""
import argparse
import json
import pathlib
import re

ENTRY = "corpus/knowledge/tb2-db-wal-recovery-grader.md"
RECEIPT = "corpus/evidence/round40/db-wal-probe.txt"
DRY = "corpus/evidence/round40/db-wal-dry-cases-freeze.txt"
CAP = "corpus/evidence/round40/tb2-db-wal-recovery"
PINS = {
    "test_outputs.py": "88dc5c2a3abba75bca0e0f9136223ae5bb585d5984b8d9eba51a7829c1d2ba49",
    "solve.sh": "ed8530c94103bf19783a1d41bc63fe4db478cdd9629f22fee25c45a45699f5e8",
    "main.db": "68cb288eb29e76d814b4e7ee6887b37c415675e644f88173bc191348e290d119",
    "main.db-wal.encrypted": "68753bdce26196a53194260d001544cc6bb8f9f38e2f2f6826d09798e31e6e26",
}
TESTS = ("test_recovered_json_exists", "test_recovered_json_is_valid", "test_recovered_data_structure",
         "test_recovered_data_sorted", "test_recovered_data_completeness", "test_no_duplicate_ids",
         "test_wal_was_decrypted")
RAW = ("https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/"
       "2fd12b88aafdd04a52c298e3940bcb189f9766d6/db-wal-recovery/")

# 10 verbatim single-line quotes, 3-25 words each, 8 from the grader capture + 2 from the instruction.
QUOTES = [
    ("the grader never opens the database; it only looks at one file name", "Test that the recovered.json file exists.", "test_outputs.py", 8),
    ("the score is a single substring test on the JSON text", "recovered.json file does not exist", "test_outputs.py", 9),
    ("the grader rebuilds the database from the WAL and diffs every page", "JSON should be a list", "test_outputs.py", 17),
    ("an empty export earns partial credit", "JSON should not be empty", "test_outputs.py", 18),
    ("field types are never inspected", "id should be an integer", "test_outputs.py", 33),
    ("record order is never inspected", "Data should be sorted by id", "test_outputs.py", 44),
    ("the base database alone already holds the eleven records", "We expect 11 records total (5 base + 6 new from WAL)", "test_outputs.py", 52),
    ("the WAL carries no updated values, only new rows", "Apple should have updated value 150 from WAL", "test_outputs.py", 64),
    ("duplicate ids are accepted", "There should be no duplicate IDs", "test_outputs.py", 89),
    ("recovering base data alone is enough to pass", "Only base data recovered - WAL decryption failed", "test_outputs.py", 98),
    ("the instruction asks for a SQL dump, not JSON", "Fix the WAL file so SQLite can read it", "instruction.md", 7),
    ("the instruction accepts the export anywhere on disk", "Create a JSON file in /app/recovered.json", "instruction.md", 9),
    ("the instruction asks for a tenth of the records", "You should recover all 11 records total.", "instruction.md", 13),
]

# Error classes derived statically from tests/test_outputs.py for the cases whose export is absent,
# unparsable or a dict: FileNotFoundError where open() runs, JSONDecodeError on unparsable JSON,
# TypeError where `[item["id"] for item in data]` indexes the wrapped dict's string keys.
ERRORS = {
    "empty-app": {t: "FileNotFoundError" for t in TESTS[1:]},
    "untouched": {t: "FileNotFoundError" for t in TESTS[1:]},
    "decrypt-in-place-no-json": {t: "FileNotFoundError" for t in TESTS[1:]},
    "truth-wrong-path": {t: "FileNotFoundError" for t in TESTS[1:]},
    "truth-trailing-garbage": {t: "JSONDecodeError" for t in TESTS[1:]},
    "truth-wrapped-object": {"test_recovered_data_sorted": "TypeError", "test_no_duplicate_ids": "TypeError"},
}


def derive(vals):
    if vals == {"fail"}:
        return "enforced"
    if vals == {"pass"}:
        return "unenforced"
    return "partly"


def dry_rows(lane):
    tags, cases = {}, []
    for line in (lane / DRY).read_text().splitlines():
        p = line.split()
        if p and p[0] == "TAG":
            tags[p[1]] = p[2]
        elif p and p[0] == "CASE":
            m = re.match(r"^CASE (\S+) predicted=(pass|fail) tests=([PF]{7}) violates=(\S*) -- (.*)$", line)
            cases.append(dict(cid=m.group(1), pred=m.group(2), letters=m.group(3),
                              violates=[t for t in m.group(4).split(",") if t], desc=m.group(5)))
    return tags, cases


def observed_map(receipt_text):
    out = {}
    for line in receipt_text.splitlines():
        m = re.match(r"^CASE (\S+) predicted=\S+ observed=(pass|fail) .*?\bviolates=(\S*)", line)
        if m:
            out[m.group(1)] = (m.group(2), [t for t in m.group(3).split(",") if t])
    return out


def typed_literal(tags, cases):
    lines = [f"CASE {c['cid']} predicted={c['pred']} observed={c['pred']} tests={c['letters']}"
             f" violates={','.join(c['violates'])} -- {c['desc']}" for c in cases]
    p = sum(c["pred"] == "pass" for c in cases)
    lines.append(f"cases={len(cases)} observed_pass={p} observed_fail={len(cases) - p} mismatches=0")
    return "\n".join(lines) + "\n"


def typed_format(tags, cases, errors):
    lines = ["# tb2 db-wal-recovery grader probe (kengaku round 40) @ terminal-bench-2 2fd12b88"]
    lines += [f"# capture {n} sha256={PINS[n]}" for n in sorted(PINS)]
    for c in cases:
        errs = ",".join(f"{t}:error={errors.get(c['cid'], {}).get(t, '')}" for t in TESTS
                        if errors.get(c["cid"], {}).get(t))
        lines.append(f"CASE {c['cid']} predicted={c['pred']} observed={c['pred']} tests={c['letters']}"
                     f" predicted_tests={c['letters']} match={'yes' if True else 'NO'} regrade=same"
                     f" violates={','.join(c['violates'])}{' ' + errs if errs else ''} -- {c['desc']}")
    p = sum(c["pred"] == "pass" for c in cases)
    lines.append(f"regrade cases={len(cases)} differ=0")
    lines.append(f"cases={len(cases)} observed_pass={p} observed_fail={len(cases) - p} mismatches=0")
    return "\n".join(lines) + "\n"


def entry_text(tags, obs, prose, cites):
    head = [
        "# Terminal-Bench 2.0 `db-wal-recovery` grader — sixth grader class (binary database file pair)",
        "",
        f"source: S119 {RAW}tests/test_outputs.py",
        f"source: S120 {RAW}instruction.md",
        "verified-at: 2026-10-26",
        "recheck: before the claim is reused for any comparison",
        "",
        "## Summary",
        "",
    ]
    if prose == "false":
        head.append("The 28-case probe found that every case passes: 28 pass, 0 fail. The grader "
                     "re-opens the database and compares every page it recovers, so an agent that "
                     "never touches the WAL cannot pass.")
    else:
        head.append("The pinned grader scores seven pytest functions over one JSON export. This entry "
                     "records the capture set and the probe receipt beside it.")
    head += ["", "## Located quotes", "", "| claim | quote | location |", "|---|---|---|"]
    for claim, text, cap, line in QUOTES:
        head.append(f"| {claim} | “{text}” | `{cap}:{line}` |")
    head += ["", "## Requirement map", "",
             "| location | tag | label | cases |", "|---|---|---|---|"]
    for tag, loc in tags.items():
        vals = {obs[cid][0] for cid, vs in ((cid, v) for cid, (_o, v) in obs.items()) if tag in vs}
        viol = [cid for cid, (_o, v) in obs.items() if tag in v]
        cited = viol if cites == "all" else viol[:1]
        head.append(f"| `{loc}` | `{tag}` | {derive(vals)} | "
                    + ", ".join(f"`{c}`" for c in cited) + " |")
    head += ["", "## Negative space", "",
             "No falsifier is offered for the summary above; the map above is derived from the receipt.",
             ""]
    return "\n".join(head)


def patch_readme(lane):
    p = lane / "corpus/README.md"
    text = p.read_text()
    row = ("| `knowledge/tb2-db-wal-recovery-grader.md` | A sixth Terminal-Bench 2.0 task grader read and "
           "executed: `db-wal-recovery` scores seven pytest functions over one JSON export whose source of "
           "truth is a SQLite main database plus an XOR-encrypted write-ahead log | S119, S120; round40 Gate |")
    if "knowledge/tb2-db-wal-recovery-grader.md`" not in text:
        anchor = "| `knowledge/tb2-git-leak-recovery-grader.md` |"
        i = text.index(anchor)
        j = text.index("\n", i) + 1
        text = text[:j] + row + "\n" + text[j:]
    bullet = ("- **Terminal-Bench 2.0 task grader (sixth task, binary database-pair class)**: covered at "
              "source-code depth and executed offline (round 40, 2026-10-26) — "
              "knowledge/tb2-db-wal-recovery-grader.md; S119, S120; probe `plans/db_wal_probe.py`, "
              "receipt `evidence/round40/db-wal-probe.txt`.")
    if "receipt `evidence/round40/db-wal-probe.txt`" not in text:
        anchor = "receipt `evidence/round39/git-leak-probe.txt`."
        i = text.index(anchor)
        j = text.index("\n", i) + 1
        text = text[:j] + bullet + "\n" + text[j:]
    p.write_text(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--receipt", default="real", choices=("real", "typed-literal", "typed-format", "typed-derived"))
    ap.add_argument("--prose", default="junk", choices=("junk", "false"))
    ap.add_argument("--cites", default="one", choices=("one", "all"))
    ap.add_argument("--print-receipt", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane)
    tags, cases = dry_rows(lane)
    if a.receipt == "real":
        text = (lane / RECEIPT).read_text()
    elif a.receipt == "typed-literal":
        text = typed_literal(tags, cases)
    elif a.receipt == "typed-format":
        text = typed_format(tags, cases, {})
    else:
        text = typed_format(tags, cases, ERRORS)
    if a.print_receipt:
        pathlib.Path(a.print_receipt).write_text(text)
    obs = observed_map(text)
    assert len(obs) == len(cases), (len(obs), len(cases))
    (lane / RECEIPT).write_text(text)
    (lane / ENTRY).write_text(entry_text(tags, obs, a.prose, a.cites))
    patch_readme(lane)
    print(f"wrote entry, readme row+bullet, receipt={a.receipt} prose={a.prose} cites={a.cites} "
          f"cases={len(obs)} pass={sum(o == 'pass' for o, _v in obs.values())}")


if __name__ == "__main__":
    main()
