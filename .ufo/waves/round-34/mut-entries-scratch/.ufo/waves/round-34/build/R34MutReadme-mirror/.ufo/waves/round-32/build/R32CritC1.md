# R32CritC1 — attack on C1 (assimilation claim) — frozen controls

Critic: `L1Kengaku32.R32CritC1` (UFO-FSD, leaf). Date: 2026-10-25.
Target: round-32 C1 coverage claim (freeze commit `0d32691d`).
Method: the two frozen counters were run against synthetic lane trees in
`/tmp/r32-l1kengaku32/fleet/c1fake-shokunin` (full `corpus/` copy + the frozen
`adoption-expect.json`/`control-nothing.txt`, registry rows S093/S094/S097
status=mined, opened=2026-10-25, used-by → entry). No repo bytes were modified.
No tools installed (none needed).

Frozen controls under test:
- C1 receipt 1: `python3 plans/adoption_check.py --expect .ufo/waves/round-32/claims/adoption-expect.json --census` → `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok`, exit 0.
- C1 receipt 2: `python3 plans/round32_c1_verify.py --lane .` → `checks=6 defects=0`, exit 0 (V1 entry-at-path+verified-at; V2 cited-row URL host+path; V3 three pins named; V4 index title ≥20 chars; V5 ≥40 lines/≥3000 bytes; V6 control receipt pins expect digest + exit=1).

---

## Route (a) — 63-byte stub with three `source:` lines

Tree: entry = 64 bytes exactly (`source: S093\nsource: S094\nsource: S097\nverified-at: 2026-10-25\n`), index row `Grader semantics stub | x`, registry rows present/mined/opened/used-by.

Observed:
- receipt 1 **PASSES**: `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok`, **rc=0** (exact frozen line).
- receipt 2 **CATCHES**: `DEFECT V2 cited-row-identity … (github.com/scaleapi/SWE-bench_Pro-os)`, `DEFECT V3 pinned-revisions-named: … 66f92766, 9be8d8fe, 2412.05579`, `DEFECT V5 entry-substance: the entry is 4 lines`, `checks=6 defects=3`, rc=1.

Verdict: **stub killed by receipt 2** (V2/V3/V5; V1/V4 pass). **But the kill does not generalize**: any ≥3000-byte body with the three URLs and the three pin fragments in its source lines passes BOTH receipts (see routes B/C — their bodies pass all six V-checks). So the control closes the literal 63-byte stub, not the stub-shaped exploit class.

## Route (b) — identity spoofing (row URL host+path vs entry source line)

Tree: full document (passes V5), source lines carry the exact registry URLs (`github.com/scaleapi/SWE-bench_Pro-os`, `github.com/hkust-nlp/Toolathlon`, `arxiv.org/abs/2412.05579`) and the three pin fragments — but S094's line cites `# README.md` while the registry row's anchored document is `tasks/finalpool/ab-testing/evaluation/main.py`, and the body asserts Toolathlon uses an LLM judge (false against the pinned code).

Observed:
- receipt 1 **PASSES**: exact frozen line, rc=0.
- receipt 2 **PASSES**: `checks=6 defects=0`, rc=0.

Cause: V2 only requires the row's URL host+path substring to appear somewhere in the entry's `source: S094` line; it never compares the entry's anchor fragment (`# README.md`) to the registry row's anchor, never fetches the pin, and never reads the body. The registry row itself is written by the same actor, so the row's URL/anchor are equally spoofable.

Verdict: **ESCAPES both frozen controls.** The only barrier is the prose kill rule (located quote at pinned revision) plus the Q10/Q13 second-seat re-read — neither is executable by any frozen counter.

## Route (c) — kill-rule reachability (two of three sources surviving)

Tree: S093/S094 rows fine; S097's registry anchor replaced with an invented location `arXiv 2412.05579v2, §9 Nonexistent section: "This quote does not exist in the pinned revision."`.

Observed:
- receipt 1 **PASSES**: exact frozen line, rc=0.
- receipt 2 **PASSES**: `checks=6 defects=0`, rc=0.

Neither counter performs any network access or quote lookup (adoption_check reads only lane files; round32_c1_verify reads only lane files; no URL is fetched). A row whose located quote cannot be found at the pinned revision still counts as present/mined/opened/used-by. The kill rule's letter ("if fewer than two of the three survive … not admitted") is therefore unreachable by the controls: mechanically, even 0/3 resolved quotes admit. Note also the rule permits admission when exactly two survive, with the third row still cited.
Concrete corroboration that content fidelity is unpoliced: the pinned Toolathlon `evaluation/main.py` calls `validate_record_data(actual_records, expected_records, tolerance_pct=0.05)` (line 280, `# Validate with 0.05% tolerance`); the staged entry body claims the call is `tolerance_pct=0.1` and a "0.1-percentage-point tolerance". That factual error against the pinned code passes both receipts.

Verdict: **ESCAPES both frozen controls** — the kill rule is a process rule, not a control.

## Route (d) — index-row gameability (title cell only)

Tree variants:
- long title (≥20 chars) + one-char description cell `x`: receipt 1 **PASSES** (exact line, rc=0); receipt 2 **PASSES** (`checks=6 defects=0`).
- title-only, empty description cell: receipt 1 **FAILS** (`index_shape_ok` → rc=1); receipt 2 passes.

Verdict: **pure title-only killed by receipt 1** (cells[2] must be non-empty); **title + arbitrary 1-char description escapes both** — the counters check cell shape, never cell semantics.

## Route (e) — S093 used-by still naming the old entry only

Tree: S093's used-by left as `corpus/knowledge/benchmark-verifier-execution-model.md` (no new entry added); S094/S097 rows correct; entry full.

Observed:
- receipt 1 **FAILS**: `usedby_ok=0`, rc=1.
- receipt 2 passes.

Verdict: **KILLED by receipt 1** (per-entry all-of used-by check). Requires the expect file to keep listing S093 — it does (frozen `adoption-expect.json`).

---

## Cross-cutting residual escapes (all verified by the runs above)

1. **Garbage-document generalization (a/b/c)**: the second receipt's substance gates are length/presence only. A 3000-byte file of filler with the right headers, URLs, and pin fragments passes all six V-checks. Nothing admits or rejects on whether the body's sentences correspond to the pinned bytes.
2. **Expect-file triad is pinned by V6, but only against the committed control receipt**: adopting the wrong triad (e.g. S100/S101/S103) breaks `ids_ok` against the frozen expect file, and swapping the expect file breaks V6's digest pin (`expect_sha256=a1a7e860…` matches today's frozen receipt). However, nothing machine-checks that the *control receipt itself* is the freeze-committed one; an actor who mutates both expect and control in the landed tree passes V6. That is a git-history witness, not a counter.
3. **Anchor/quote fidelity is wholly unpoliced** (routes B/C): the counters never compare entry anchor fragments to registry anchors, never fetch pins, never verify quotes. The only machinery that can kill a counterfeit source is the human/process kill rule and Q10/Q13 re-reads — all outside the two receipts.
4. **Staged-bundle drift**: the staged entry carries `verified-at: 2026-10-23` and the staged S094/S097 rows carry `opened=2026-10-23`; the frozen predicate demands `2026-10-25`. As staged, the bundle fails receipt 1 (V1/opened_ok). The appender must retouch dates — a practical trap, not an attack.

## Ground truth at pins (fetched 2026-10-25, for the kill-rule review)

- S093: `SWE-bench_Pro-os` @ `66f92766` — `v2/tasks/…openlibrary-…/tests/test.sh:33` `echo "Resetting test-space to base state (full test-code surface)..."`; `:71` `T) git checkout HEAD -- "$path"`; `:213-214` `all_required = fail_to_pass | pass_to_pass` / `success = all_required <= passed_tests`. Quotes resolve.
- S094: `Toolathlon` @ `9be8d8fe` — `tasks/finalpool/ab-testing/evaluation/main.py:58` `def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1) -> None`; `:55` `expected_ratio.csv`; `:125/:168/:220` the three helpers; `:280` actual call **`tolerance_pct=0.05`** (entry body's 0.1 statement is wrong).
- S097: arXiv `2412.05579v2` abstract contains `Functionality, Methodology, Applications, Meta-evaluation, and Limitations.` Quote resolves.

---

## Per-route kill/escape verdicts

| Route | Frozen control outcome | Verdict |
|---|---|---|
| (a) 63-byte stub | receipt 1 passes; receipt 2 kills (V2/V3/V5) | KILLED as a stub; ESCAPES as any ≥3KB padded document |
| (b) identity spoofing | both receipts pass | ESCAPES |
| (c) kill-rule unreachability | both receipts pass with 0/3 resolved quotes | ESCAPES (kill rule is prose, not a control) |
| (d) index-row title-only | receipt 1 kills empty-description cell; title+1-char desc passes both | PARTIALLY KILLED |
| (e) S093 old used-by only | receipt 1 fails (`usedby_ok=0`) | KILLED |

The frozen predicate is satisfied by trees whose cited sources are counterfeits (B), whose kill-rule refusal conditions are met (C), and whose index row is a shell (D). The claim's truth therefore rests entirely on the round's non-counter controls — the kill rule, Q10/Q13 second-seat re-reads, and human Gate review — none of which are part of the counted receipts.

VERDICT: <attack-finished>
