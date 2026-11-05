# ReviewerFrozen — R92 frozen diff audit (main report)

Scope: solo fix of three lane files under round-92's frozen predicate; adjusted the audit plan to
a read-only diff audit. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (master; HEAD reads
`288511d8` — HEAD is not the audit subject; BASE `4ba56182…` and B2 `f0018773…` are). Written to
`.ufo/waves/round-92/w1/ReviewerFrozen.md` (this file) plus the fuller per-file audit in
`.ufo/waves/round-92/w1/ReviewerFrozen/report.md`.

## Result

The diff window BASE `4ba56182…` → B2 `f0018773…` is **conforment** to the frozen amendment
list; every hunk of the three amended counters falls inside an allowed amendment category, the
pin ledger changed by exactly the four expected entries (3 counter-sha updates + the added
`plans/round92-selftest-expectations.json` entry, all byte-verified), no semantically empty hunk
exists anywhere in the window, and no file outside the disclosed change-list changed (verified
via `git diff --name-status`; the only modification is `plans/counter-pins-r91.json`; the 21
additions are all disclosed instruments, claims/cases files, or `corpus/evidence/round92/**`).
One substantive finding (F1 below) concerns the frozen *predicate wording* of R92-C2's M9 tip
condition — report, not repair, per the freeze discipline.

## Findings

**F1 — M9 tip predicate wording binds on docstring bytes (`--skip-selftest` literal).**
The frozen claims text requires at T: "the checker bytes contain no `--skip-selftest`". The B2
checker bytes still contain that literal in two non-executable docstring lines (usage-table doc
at B2 line 16; the `selftest()` docstring's mechanism description at B2 line 211, describing the
removed flag while the actual mechanism is now the `R91_C2_CHILD_MODE` env). The frozen
instrument `plans/round92_c2_conformance.py` implements the M9 flag condition as a raw
substring test — `"--skip-selftest" not in tip_c2_text` — with no comment/docstring filtering.
Executing the frozen battery at T therefore proves `tip-flag-absent=FALSE` → M9 FAIL →
`PREDICATE R92-C2 fail`, a scripted mispredict of the executed claim wording, forbidden to repair
in-place under the freeze discipline. Route to triage as a predicate-wording repair-lead; the
defect is docstring-only (genuinely non-executable), so the real flag removal itself is verified.

**No other findings.** Byte-exact diff of `plans/round91_c1_replay.py` contains exactly the M7
hunk (positional case-id, `tokens[0]` before scanning `key=value` tokens; byte-identical detail
scan but with `parts.get("id","?")` removed) and exactly the M12 hunk (the `guarded_run` wrapper
with `except (OSError, SubprocessError)` and the `raise CouldNotEvaluate(...)` fail-closed guard
across `py_now_line`/`oss_line`/`userns_now`, converting to `DEFECT SETUP` rc 2 through the
pre-existing `except CouldNotEvaluate` handler at B2 line 291). `check_pins`, `fixture_repo`,
`sha`, leg order, thresholds, and constants are untouched; `CouldNotEvaluate` pre-exists at
BASE:42; no dead-code gain: the removed BASE `host()` helper had zero callers at BASE. Digest
mapping for `plans/round91_counter_pin.py`: every hunk maps to allowed categories (a)–(e)
(`--skip-selftest` removal, expectations-table load + pin verification in the predicate path,
`R91_C2_CHILD_MODE` child-mode env, the 9th `expectations-tampered` case, and main's
`--selftest` table load). `check_pins` itself byte-identical; no carry-forward or blob/anchor
drifts; M12/M9 fail-closed routes all land in `DEFECT SETUP` rc 2 through existing machinery,
not new plumbing. `plans/round83_c2_checks.py` contains exactly the M6 hunk in `v8`:
`R83_FLEET_REPO` → `SHOKUNIN_ROOT` → `origin.parent` fallback precedence, matching the claims
wording, behavior-preserving for every previously supported env combination. Pin ledger:
byte-verified all four expected entry updates/insertions against the B2 tree bytes; zero
removals; all blob entries' `blob`+`anchor_commit` byte-identical; reindentor-induced whitespace
only (the per-line change surface is cosmetic reindentation from 2-space to 1-space indent).
Tools: no installs or upgrades (host Python and git only). No mutating git/jj commands in the
lane; all fixture commits confined inside the scratch-local fixture repos created by the
amended checker's own selftest (its `--allow-empty` re-commit loop) under
`/fast/scratch/hyaku/kengaku-r92/ReviewerFrozen/…` (removed after use; full receipts before
removal in the detailed report).

## Cross-checks executed

- `git diff --name-status 4ba56182 f0018773` → 22 files; the only modification is the pin
  ledger; all additions inside the disclosed file list; no deletions, no mode changes, no
  renames.
- Semantic (post-JSON-parse) diff of `plans/counter-pins-r91.json`, not a git diff — separated
  the 177-line cosmetic reindent from the 4 real entry diffs (3 sha updates, 1 insertion).
- Byte-verified all four updated/inserted ledger sha entries against `git show f0018773:<path>`
  (all 4 match; the BASE-side stale sha also matches the BASE pre-amendment bytes).
- R92-C2 selftest (amended checker, 9-case red-green, scratch fixtures) end-to-end pass:
  `cases=9 red-green-ok=9`, rc 0 — the counters' operational surface is intact under the
  amendments.
- Reservation: byte-exact compare of `plans/round-92-claims.md` and `plans/round92-cases.json`
  between freeze A (`96f249e0`) and B2 (`f0018773`) was not executed (out of this seat's scoped
  work, as noted in the detailed report); the three-claim predicate/kill-rule text was verified
  constancy by grep only. A seat with a frozen-artifact diff-less mandate should byte-exact A vs
  B2 compare those two files.
