#!/usr/bin/env python3
"""Simulate applying six lesson index rows to corpus/README.md in SCRATCH (lane untouched).

Uses the lane's own plans/state_check.py parsing functions (readme_index_rows) so no second
convention is introduced. Reports:
  - which frozen README_INDEX_PATHS gain/lose rows (must be none),
  - whether the six new lesson paths are recognised as index rows,
  - the resulting grep -c for each lessons/round-{57..62}.md (must be exactly 1).
"""
import re, shutil, sys, pathlib

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
SCRATCH = pathlib.Path("/fast/scratch/hyaku/kengaku-r64/IndexParity/readme-sim")
sys.path.insert(0, str(LANE / "plans"))
import state_check  # noqa: E402  (read-only import; module has no import-time writes)

ROWS = [
    "| `lessons/round-57.md` | Gate (S205 task.toml, S206 test_outputs.py, S207 solve.sh oracle, S208 instruction.md — four admits, tier A, no rejections), two Mistakes rows (provider: stale-index `git diff`; landing: ledger-insertion brace indent) plus a third landing row appended at the file end by the close-C2 correction, coverage predicate met with the score held at 7 | LOG.md round 57; `plans/round-57-claims.md`; `.ufo/waves/round-57/` |",
    "| `lessons/round-58.md` | Gate (S209 task.toml, S210 test_outputs.py, S211 solve.sh oracle, S212 instruction.md — four admits, tier A, no rejections; S213–S217 supersessions), four Mistakes rows (freeze: sha-refusal kill exit written as 2, measured 1; landing: re-run of a mid-way-asserting script duplicated two edits; landing: an advertised-but-unregistered counting command; fixture authoring: re-typed doubled escapes), all three claims verify (C1 held 10, C2 9→10, C3 coverage predicate met, score held at 7) | LOG.md round 58; `plans/round-58-claims.md`; `.ufo/waves/round-58/` |",
    "| `lessons/round-59.md` | Gate (S218 task.toml, S219 test_outputs.py, S220 solve.sh oracle, S221 instruction.md — four admits, tier A, no rejections), five Mistakes rows (freeze-transcription, instrument scope, receipt-pointer, anchor authoring, evidence receipt quoting), C1 not admitted (predicate FAIL, honestly carried), C2 admitted; round self-admission FALSE under the every-claim-verifies rule | LOG.md round 59; `plans/round-59-claims.md`; `.ufo/waves/round-59/` |",
    "| `lessons/round-60.md` | Gate (S223 GNU Grep manual output control — one admit, tier A official docs, no rejections), five Mistakes rows (harness exit capture, self-quoting drift, same-line pairing, self-quoting ladder rung 3, receipt quotation clip), both claims verify (C1 completion admitted with coverage held at 7, C2 admitted with operability held at 10) | LOG.md round 60; `plans/round-60-claims.md`; `.ufo/waves/round-60/` |",
    "| `lessons/round-61.md` | Gate (S224 cancel-async-tasks scoring predicate, S225 WHATWG windows-1252 index — two admits, tier A code and docs, no rejections), six Mistakes rows (windows-text-mode write, builder-property unwired, freeze-transcription recurrence, model else-branch blind spot, asserted before-anchor, environment: /tmp wipes and /mnt/c clones), both claims verify (C1 predicate met with coverage held at 7, the first-run fail carried in the record; C2 admitted with calibration held at 10); the round-62 erratum corrects two of the rows' counts | LOG.md round 61; `plans/round-61-claims.md`; `.ufo/waves/round-61/` |",
    "| `lessons/round-62.md` | Gate (S226 TB2 task tree at the pin, S227 WHATWG windows-1252 re-open superseding S225 — two admits, tier A code-host metadata and docs, no rejections), five Mistakes rows (section-blind end-append, untracked inputs in claims, runner exit-swallow, receipt-from-memory prose, detector-table blind spot), both claims verify (C1 census predicate met with coverage held at 7, the SETUP first run carried in the record; C2 admitted with calibration held at 10) | LOG.md round 62; `plans/round-62-claims.md`; `.ufo/waves/round-62/` |",
]

if SCRATCH.exists():
    shutil.rmtree(SCRATCH)
(SCRATCH / "corpus").mkdir(parents=True)
readme = (LANE / "corpus/README.md").read_text(encoding="utf-8")
(SCRATCH / "corpus/README.md").write_text(readme, encoding="utf-8")

before_rows, before_anchors = state_check.readme_index_rows(SCRATCH)
before_locs = {}
for rel, ln in before_rows:
    before_locs.setdefault(rel, []).append(ln)

lines = readme.splitlines()
# insert the six rows immediately after the last row of the `### `lessons/` index table
start = next(i for i, l in enumerate(lines) if l.startswith("### `lessons/`"))
end = next(i for i, l in enumerate(lines) if l.startswith("Supporting corpus files:"))
last_table_row = max(i for i in range(start, end) if lines[i].startswith("| `lessons/"))
new_lines = lines[: last_table_row + 1] + ROWS + lines[last_table_row + 1 :]
(SCRATCH / "corpus/README.md").write_text("\n".join(new_lines) + "\n", encoding="utf-8")

after_rows, after_anchors = state_check.readme_index_rows(SCRATCH)
after_locs = {}
for rel, ln in after_rows:
    after_locs.setdefault(rel, []).append(ln)

print(f"insert anchor: `### lessons/` table last row at README line {last_table_row + 1}")
print(f"index rows before={len(before_rows)} after={len(after_rows)}")
changed = {r: (before_locs.get(r, []), after_locs.get(r, [])) for r in set(before_locs) | set(after_locs)
           if before_locs.get(r, []) != after_locs.get(r, [])}
print(f"frozen/other rows whose locations changed: {len(changed)}")
for r, (b, a) in sorted(changed.items()):
    print(f"   {r}: {b} -> {a}")

frozen = set(state_check.README_INDEX_PATHS)
print("\nnew rows and their frozen-population status:")
for rel, ln in sorted(after_locs.items(), key=lambda kv: kv[1][0]):
    if rel not in before_locs:
        status = "OUT_OF_POPULATION (not in frozen 6180e4f population; not checked)"
        assert rel not in frozen, rel
        print(f"   {rel} @ {ln}  {status}")

text = (SCRATCH / "corpus/README.md").read_text(encoding="utf-8")
print("\ngrep -c 'lessons/round-N.md' after insertion:")
for n in range(57, 63):
    c = len(re.findall(rf"lessons/round-{n}\.md", text))
    print(f"   round-{n}: {c}")
print("\nduplicate-row check on the six paths (must be 1 each):")
for n in range(57, 63):
    rel = f"lessons/round-{n}.md"
    print(f"   {rel}: row_lines={after_locs.get(rel)}")
