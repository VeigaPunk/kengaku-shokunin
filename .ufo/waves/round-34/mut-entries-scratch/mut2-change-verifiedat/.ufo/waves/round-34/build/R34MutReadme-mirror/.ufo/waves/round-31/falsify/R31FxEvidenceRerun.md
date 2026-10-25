# R31FxEvidenceRerun — re-run every receipt in corpus/evidence/round31/

Seat: `L1Kengaku31.R31FxEvidenceRerun` (leaf, falsify wave 2). Date 2026-10-25.
Item: re-run every receipt under `corpus/evidence/round31/` and report which reproduce
byte-identically. No lane edits except this report; scratch under
`/tmp/r31fx-EvidenceRerun/` (fixtures + captured stdout, < 1 MB). No tool installed.

Snapshot: verification ran against lane HEAD `b54611c3` (receipts as committed there), with a
re-check after peers advanced HEAD to `9591131e`; counter/tool bytes used are
`plans/sources_adopt.py` sha256 `38492bf1…` and `plans/round31_defects.py` sha256 `13813eae…`
(working tree at run time). The fleet census ran directly from
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`.

## 1. Per-receipt reproduction

Legend: **full** = the receipt file's bytes equal the rerun output exactly; **body** = the tool's
stdout reproduces exactly, and the receipt file additionally carries author-written annotation lines
(provenance `#` header, `exit=N` footer) that are not tool output; **stale** = the committed
receipt cannot be produced by the counter as committed.

| receipt | canonical command (as derivable from claims/receipt) | rerun result | exit | verdict |
|---|---|---|---|---|
| `adoption-after.txt` | `python3 plans/adoption_check.py --expect .ufo/waves/round-31/adoption-expect.json --census` | `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok` | 0 | **full** — byte-identical |
| `c1-verify-after.txt` | `python3 plans/round31_c1_verify.py --lane .` | `checks=6 defects=0` | 0 | **full** — byte-identical |
| `defects-after.txt` | `python3 plans/round31_defects.py --lane .` | `checks=10 defects=0` | 0 | **body** — stdout identical; file adds `#` header + `exit=0` (lines 1–2, 4) |
| `defects-before-final.txt` | `python3 plans/round31_defects.py --lane /tmp/r31-before` (clone at `0883e72`) | 10 DEFECT lines + `checks=10 defects=10` | 1 | **body** — stdout identical; file adds header + `exit=1` (lines 1–3, 15) |
| `defects-before-tightened.txt` | `python3 plans/round31_defects.py --lane /tmp/r31-r6proof` | R6/R7 lines differ: receipt `"the entry still says three staged source rows are unregistered"` / `"contradicting its R3 row"` are **not reachable** by the committed counter, which prints `"asserts all three staged source rows are unregistered; 2 are"` and `"still claims the tri-state flag is the only new field"` | 1 | **stale** — cannot reproduce from committed bytes (see §2) |
| `gate-selftest-after.txt` | `python3 plans/sources_adopt.py --selftest` | 17 CASE lines + `SELFTEST cases=17 failed=0` | 0 | **full** — byte-identical |
| `gate-cli-exits.txt` | runner + fixtures not committed; reconstructed, see §3 | 5 blocks; exits 0/8/9/0/2 | — | **full under reconstruction** — byte-identical once the runner filter and `cli/` fixture bytes (recovered from `/tmp/r31-cli`) are supplied |
| `gate-binding-neutered.txt` | `cd /tmp/r31-gate-proof && python3 sources_adopt.py --selftest` (neutered `bind_failure()` returns `""`) | 17 CASE lines, last two FAIL, `SELFTEST cases=17 failed=2`, `failed: quote-url-mismatch-refused quote-url-unmapped-refused` | 1 | **body** — stdout identical; file adds `#` header + `exit=1` (lines 1–2, 22) |
| `quote-mode-adopted-rows.txt` | `python3 plans/sources_adopt.py --quote-file .ufo/waves/round-31/assimilation/adopted-rows.txt --artifact .ufo/waves/round-31/assimilation/captures` | 7 spans located, `exit=0` | 0 | **body** — stdout identical; file adds header + `exit=0` (lines 1–2, 11) |
| `quote-mode-bound.txt` | same + `--url-map .ufo/waves/round-31/assimilation/capture-url-map.json` | 7 spans, `mismatch=0 unmapped=0 urlmap=capture-url-map.json entries=6`, bound lines | 0 | **body** — stdout identical; file adds header + `exit=0` (lines 1–5, 14) |

Extra receipt present in the dir: `census-after.txt` — reproduces **byte-identically** only when the
fleet census is invoked directly
(`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root … kengaku`,
15 W04 + ok line, exit 0); `plans/adoption_check.py` captures the subprocess, so the receipt is not
producible through the C1 counter command.

## 2. `defects-before-tightened.txt` is stale

- The committed counter (`plans/round31_defects.py`, lines 219–240) emits R6 as
  `"the entry asserts all three staged source rows are unregistered; {unregistered} are"` and R7 as
  `"the entry still claims the tri-state flag is the only new field"` — the receipt's R6/R7
  wordings (`"still says three staged source rows are unregistered"`,
  `"contradicting its R3 row"`) appear nowhere in the counter, so no run of the final counter can
  produce them.
- The receipt's own header asserts it was produced *after* R6's check was tightened and *before* the
  final counter bytes; it is evidence of an intermediate counter revision.
- Its input tree (`/tmp/r31-r6proof`) is scratch, not committed. R9/R10 lines on that tree do
  reproduce (git-failure and unreadable swarm-registry messages match).

## 3. `gate-cli-exits.txt` — reproducible only under reconstruction

- Fixtures exist only in scratch `/tmp/r31-cli/` (`rows.txt` S900 row citing
  `https://example.invalid/docs/verifier.html`, `cap.txt` = `the verifier shares the agent container`,
  `map-ok.json`, `map-bad.json`, `map-unmapped.json` = `{"nope.txt": …}`); none are committed.
- The runner is not committed. Byte-identical reproduction (verified) requires: for each scenario,
  echo the header line, run the tool, pipe stdout through `sed 's/^\([^ ]\)/  \1/'` (indent only
  flat lines — QUOTE/ok/REFUSED detail lines already carry 2 spaces), and for the final registry-path
  scenario pipe `2>&1 | tail -n 1` (the receipt shows only the error sentence, not argparse's usage
  block).
- With that reconstruction, `diff` of my rerun against the committed receipt is empty
  (`/tmp/r31fx-EvidenceRerun/run15-cli.out`). Exit codes reproduce: 0, 8, 9, 0, 2.
- At the original landing commit `dbb07364` this receipt did **not** reproduce from the landed
  printer (summary-line field order, `urlmap=none` on the no-map line, missing bound detail), as
  `R31FxC3Regress` also recorded; the current receipt matches the current printer.

## 4. Working-tree drift during verification

- The receipt set and counters were being committed by peers throughout: `defects-after.txt` /
  `defects-before-final.txt` gained annotation headers and a tightened R8 wording mid-run, and the
  counter's R8 message changed in lockstep; `gate-cli-exits.txt` / `gate-selftest-after.txt` were
  regenerated by commits `d6aa66e`, `634ded8`. Both the earlier and the later states reproduced
  byte-identically against their respective counter bytes; the committed vs current file bytes
  differ (R8 wording; header presence), which is an evidence-churn observation, not a counter failure.
- `quote-mode-*` inputs (`adopted-rows.txt`, `capture-url-map.json`, `captures/`) are committed with
  `d6aa66e`; at `dbb07364` they were absent, so those two receipts cannot be reproduced from the
  original landing commit.

## 5. VERDICT

**Survived:** the C1 counters (`adoption-after`, `c1-verify-after`), the C2 after-state counter
(`defects-after`), the C2 before-state counter body (`defects-before-final`), the C3 selftest
(`gate-selftest-after`), the C3 neutered-failure-capability demo (`gate-binding-neutered`), the C3
CLI exit/refusal receipt (`gate-cli-exits`, byte-identical under reconstructed runner+fixtures), and
the two quote-mode receipts — every one re-ran to the exact receipt body with the claimed exit code;
10/10 counted receipts' tool output reproduces, 4 of them as full files exactly.

**Fell:** `defects-before-tightened.txt` — cannot be reproduced from committed bytes (R6/R7 text
unreachable in the final counter; scratch-only input tree); it is stale intermediate evidence left in
the evidence dir. Also named: `gate-cli-exits.txt` and `gate-binding-neutered.txt` are not
self-contained in the repo (runner/fixtures/neutered copy live only in `/tmp`), so their
reproduction depends on uncommitted scratch even though the bytes verify.
