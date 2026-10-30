# R4ClaimsSizing — seat report (kengaku round 55, wave 1)

Seat: adversarial sizing audit of `plans/round-55-claims.md` (frozen at `80afa61314fa1b…`).
No lane writes other than this seat's outputs. No mutating git/jj anywhere. Scratch:
`/fast/scratch/hyaku/kengaku-r55/R4ClaimsSizing/` (deleted at exit — see Cleanup).
Tool installs: none (no installs or upgrades were needed; python3 3.14, git, curl, bwrap 0.13.1
pre-existing).

## Method

Clean `--shared` clone of the lane at the freeze tip under scratch (`clone/`) = the committed-bytes
view; the wave working tree was used read-only where an instrument is in-flight
(`plans/round55_c2_entryargv.py`, `plans/round55_c3_chess_probe.py` — both untracked at the freeze).
Base-commit checks used `git cat-file` / `git grep <rev>` on `798f5e9e…`. Full findings with severities
are in `findings.md` beside this report; transcripts in `evidence/`.

## What I ran (commands + exit codes)

Freeze-anchor and before-state:
- `python3 plans/round52_c2_registry.py --lane clone` → `MISSING 2 … PREDICATE R52-C2 fail`, exit 1
  (freeze tip; matches committed c1-before receipt). [evidence/c1-counter-at-freeze.txt]
- `git cat-file -e 798f5e9e:corpus/evidence/round55/chess-best-move-probe.txt` → absent (exit 1, expected).
- `git grep -c chess-best-move 798f5e9e -- corpus/README.md corpus/SOURCES.md` → no match (0 0, expected);
  `git grep -c thirteenth 798f5e9e -- PROVINCE.md` → no match (expected). Matches committed c3-before receipt.

C1 attacks (scratch copies of the freeze clone only):
- Erasure control: removed the four `python3 plans/round54_{c1_anchor,c2_entrytruth}.py` mentions from
  `SCORECARD.md` (the only self-assessment file carrying them), ran the counter →
  `ADVERTISED total=77 MISSING 0 … PREDICATE R52-C2 pass`, exit 0, **zero registry rows added**
  [evidence/c1-erasure-attack.txt]. Do-nothing control as worded refuted.
- False-cell attack: appended the five round-55 registry rows (round54-c1, round54-c2, round55-c2,
  round55-c2-controls, round55-c3) to a scratch copy, `round55-c2-controls` verdict map deliberately
  inverted (`` `1` ok · `0` bad ``); copied the in-flight probe/counter scripts in so ENTRY-MISSING stays
  0; advertised the three scripts in LOG.md → counter `MISSING 0 … pass`, exit 0 — false cell undetected
  by the counter. `python3 plans/round55_c2_controls.py --selftest` → exit 0 (cell is false; leg-2
  spot-leg would fire). Also: fabricated self-test cells (`--bogusflag`; `--selftest` on the anchor whose
  real spelling is the `selftest` subcommand) → `SELFTEST-UNBACKED` fires correctly.
  [evidence/c1-false-cell-attack.txt]

C2 probes (in-flight counter, labelled as such):
- `--dry` over the freeze clone → `argv_defect=17 wrapper_defect=1 … DRY-EXIT=1`: 17 truthful rows fail
  literal L1 token-equality (placeholder prose in cells vs concrete ledger argv); `tb2-grader-probe`
  flagged WRAPPER-DEFECT (committed row's argv[0] is `uv`). Frozen zero-count predicate unreachable as
  worded. [evidence/c2-inflight-dry-at-freeze.txt]
- Fixture kills via the committed controls builder:
  `python3 plans/round55_c2_controls.py --case abbreviated-selftest --against r55` → `ARGV-DEFECT` +
  `ABBREV-DEFECT … PREDICATE R55-C2 fail`, case exit 0 (kill demonstrated).
  `--case uv-decoy-script --against r55` → `ARGV-DEFECT` + `WRAPPER-DEFECT … fail`, case exit 0.
  [evidence/c2-fixture-kills-inflight.txt]
- `--selftest` (in-flight counter) → `[selftest] 4/4 PASS`, exit 0.
- Env-gate attack: scratch fixture whose gate exits 0 iff `GIT_CONFIG_GLOBAL` is set; declared green.
  Counter: all legs clean, `observed_green=1 PREDICATE R55-C2 pass`, exit 0; same argv in a plain shell
  exits 1. Boundary of "truly exits otherwise" (LOW finding). [evidence/c2-env-gate-attack.txt]
- Correction leg (a): `python3 plans/round35_c1_verify.py --lane .` at freeze →
  `V4 DEFECT knowledge files=58 index rows=58 (want 42/42)` — committed fragment says 57/57 → stale,
  re-derivation necessary and decidable (re-derive at landing after index settles).
  [evidence/c2-round35-true-output.txt]

C3 probes:
- `python3 plans/round55_c3_chess_probe.py --selftest --work <scratch>` → `failures=0`, exit 0.
- Full probe: `--lane clone --work <scratch> --receipt <scratch>` →
  `cases=12 observed_pass=5 observed_fail=7 mismatches=0 PREDICATE R55-C3 pass`, exit 0; my receipt is
  byte-identical to the wave working-tree receipt (deterministic).
  [evidence/c3-probe-and-identity.txt, evidence/chess-probe-receipt-my-run.txt]
- Oracle re-derivation: independent script evaluating the 12 frozen cases against
  `sorted(move)==sorted(["g2g4","e2e4"])` → 12/12 agree with frozen predictions.
- Upstream identity (kill c):
  `curl https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88…/chess-best-move/tests/test_outputs.py`
  → HTTP 200, sha256 `a540714e…` = capture (byte-identical, `cmp` clean). Amendment A1:
  `…/chess-best-move/tests/test.sh` → sha256 `4770437e…716e6c334`, identical to both in-repo regex-log
  runner captures. [evidence/c3-probe-and-identity.txt, evidence/upstream-test_outputs.py]

## Files I wrote

- `.ufo/waves/round-55/w1/R4ClaimsSizing/findings.md` — findings with severities (the deliverable).
- `.ufo/waves/round-55/w1/R4ClaimsSizing/report.md` — this file.
- `.ufo/waves/round-55/w1/R4ClaimsSizing.md` — scoped findings (Report: trailer target).
- `.ufo/waves/round-55/w1/R4ClaimsSizing/evidence/` — 9 transcripts/copies listed above.

## Defects found (in the frozen claims, not the lane code)

1. HIGH — R55-C1 do-nothing control overclaims (erasure bypass; evidence/c1-erasure-attack.txt).
2. HIGH — R55-C2 frozen zero-count predicate unreachable over committed registry/ledger (17 literal-L1
   false positives + committed uv-wrapper row vs frozen `wrapper_defect=0`; correction clause silent).
3. LOW — R55-C2 L3 "without executing" unimplementable literally; env-truth boundary of the kill rule;
   fixture-kill attribution rides on L1's tag family.
4. LOW — R55-C3 PROVINCE anchor "12 of 89 read" not present in committed PROVINCE.md; receipt not bound
   to a re-run by any committed gate (tip-receipts stem mismatch) — determinism is the practical guard.
5. INFO — R55-C1 verdict-map truth is not counter-checked by design; leg-2 spot-leg verified necessary
   and decidable.

## Dead ends / corrections during the audit

- First C3 upstream fetch 404'd — I guessed a `tasks/` prefix that doesn't exist in terminal-bench-2
  (tasks live at repo root); resolved via the GitHub trees API and re-verified byte-identical. The
  "identity check fails" attack therefore does NOT fire.
- My initial suspicion that the C1 counter fails to scan `corpus/knowledge/*.md` (a wording-overreach
  finding) was refuted by reading `self_assessment_files` — knowledge text IS scanned; the README in the
  claim maps to corpus/README.md, also scanned. Finding withdrawn before writing.
- One heredoc typo (`capture_output=True=True`) cost one env-gate attempt; fixture re-created and the
  attack ran clean.
- The probe script and C2 counter are untracked at the freeze commit — all their results are labelled
  IN-FLIGHT; committed-bytes verdicts for C2 await the landing revision.

## Honesty notes

- Every check listed above was actually run; nothing is asserted from reading alone except where
  labelled "read the code". All scratch fixtures were copies/clones under my scratch root; the lane tree
  was never written.
- Cleanup: scratch dir removed after evidence copy-out (trap on exit).
