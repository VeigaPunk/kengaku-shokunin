# LessonDraft — round 67 w1 (kengaku), seat report

Seat `LessonDraft` (leaf; no subagent dispatch). Scope: draft `corpus/lessons/round-67.md` from committed bytes.
Written: `.ufo/waves/round-67/w1/LessonDraft/lesson.md` (the lesson draft) and this report. Receipts copied into
`.ufo/waves/round-67/w1/LessonDraft/receipts/` (scratch copies reaped). Nothing written into the lane otherwise.

## Result

- Lesson draft: `.ufo/waves/round-67/w1/LessonDraft/lesson.md`. Sections: `## Mistakes`, `## Sweep`, `## Gate`, `## Carried`.
- **Mistakes rows: 4** (the brief asked for two; the sweep found two more, see below).
- Gate: S238 and S239 admitted, live-opened 2026-11-03 (HTTP 200, sha256 equal to the captures); both located quotes `grep -c -F` → 1. Assimilation: none (reason from the claims doc F3).
- Carried: `kengaku | round-25/33/51` (coverage cap), `round-56`, `round-63`, `round-54`, unchanged.

## Key lines and verdicts

1. Row 1 (R66-C2 predicate required a PROBE line the committed R65 receipt lacks): verified. `grep -c '^PROBE' corpus/evidence/round65/sqlite-gcov-probe.txt` → `0`.
2. Row 2 (fabricated receipt passed presence-only checker): verified. The fixture's sha is identical to the committed `corpus/evidence/round66/red/fabricated-r65.txt`.
3. Strict gate (R67-C2 successor) **not landed** at `dcc39ea3`: `grep -c strict plans/round65_c1_sqlite_probe.py` → `0`. The proposal lives in `.ufo/waves/round-67/w1/StrictGateBuild/proposed/` (sha `27e8b41f…`).
4. Proposal, lane-shaped scratch: fabricated fixture `--strict` → rc 1 with `CHECK defect:` findings; committed R65 receipt `--strict` → rc 0 (`PREDICATE R65-C1 strict-pass`); default mode rc 0 and output identical to the committed probe on both fixtures.
5. Seat-dir run of the same proposal fails kill rule (b): `strict_lane()` resolves the lane from the probe's own path, so run from its seat dir the committed receipt gets `s1 probe-bytes-missing` / `s2 grader-bytes-missing` and rc 1. This is a layout effect, not a grader verdict; recorded in the lesson row 2.
6. Sweep of round-66 spot-check: `sweep.py` exit 1 (`new-rows=1`). The second §2 candidate restates row 1's kill-rule failure. The pattern scan missed §6 item 1, so a hand read of §6 was added.
7. Row 3 (new): `corpus/knowledge/tb2-sqlite-gcov-offline.md:4` still cites S233 at `dcc39ea3` (`grep -c '^source: S233'` → `1`); S236 is present. Captured by the round-66 closure §6 item 1; not fixed.
8. Row 4 (new): round-66 Carried row 5 says "closed (this landing)", but `SKILL.md:686` at `dcc39ea3` still names `battery-run.txt` with no dated correction. Captured by the round-66 closure §6 item 2; not fixed.
9. Quote lines verified: S238 at grader line 157; S239 at instruction line 18.

## Commands run (exit codes)

- `grep -c '^PROBE' corpus/evidence/round65/sqlite-gcov-probe.txt` → `0`, rc 1 (count 0; grep no-match exit).
- `grep -c 'strict' plans/round65_c1_sqlite_probe.py` → `0`, rc 1.
- `curl -sL -w 'http_code=%{http_code}' <S238 raw URL>` → HTTP 200, rc 0; sha256 `23574246…`. `curl` same for S239 → HTTP 200, rc 0; sha256 `989bfcf0…`.
- `diff` + `sha256sum` of ReceiptMutate `base.txt`/`fab.txt` against the committed receipt and fabricated fixture → identical, rc 0 (`receipts/fixture-identity.txt`).
- Proposed probe (scratch lane `…/LessonDraft/strictlane`, layout copied):
  - `--check-receipt corpus/evidence/round66/red/fabricated-r65.txt --strict` → rc 1 (`receipts/strict-scratch-cmd1.txt`).
  - `--check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt --strict` → rc 0, `PREDICATE R65-C1 strict-pass`.
  - `--check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt` (default) → rc 0, `PREDICATE R65-C1 pass`.
  - Same three in the seat dir (`receipts/three-counting-commands.txt`): rc 1 / rc 1 (layout) / rc 0.
- Default-mode comparison, committed vs proposed, both fixtures → `default-output-identical=yes` (`receipts/default-mode-compare.txt`).
- `python3 .ufo/waves/round-67/w1/LessonDraft/receipts/sweep.py` → exit 1, `SWEEP VERDICT new-row-found` (`receipts/sweep-output.txt`).
- `git show dcc39ea3:corpus/SOURCES.md`, `git show dcc39ea3:corpus/knowledge/tb2-sqlite-gcov-offline.md`, `git show dcc39ea3:SKILL.md`, `git show dcc39ea3:SCORECARD.md` (read-only) → receipts `s233-provenance.txt`, `r65-pointer-status*.txt`.
- `grep -c -F` on both captures → `1` each; `grep -n -F` → lines 157 and 18.

## Deviations and disclosures

- **A write went to the fleet root by mistake.** My first `lesson.md` write used a path missing the `kengaku-shokunin/` segment and created `/home/vgpnk/Projects/shokunin/.ufo/waves/round-67/` (fleet root, untracked). The tree held only my file; I removed exactly that tree (`rm -f` of my `lesson.md`, `rmdir` of the three directories I had created). The fleet root's tracked files were not touched. The lesson was then rewritten at the correct seat path.
- **The brief's "no further row" premise did not hold.** The sweep found two further rows (§6 items 1 and 2); both are in the lesson, verified at the tip. The lesson's row count is 4, not 2.
- **Receipts copied into the seat dir** (`receipts/`), beyond the brief's "write only lesson.md": the contract requires every cited receipt to be copied into the seat dir before yield, and the lesson cites them. No other file written.
- **Tooling:** none installed or upgraded by this seat. Used host `python3`, `curl`, `grep`, `sha256sum`, `diff`, `git show` (read-only).
- **Not verified here:** whether the R67-C1 grader probe passes; that is outside this seat's item. The lesson does not claim it.

## Files written

- `.ufo/waves/round-67/w1/LessonDraft/lesson.md`
- `.ufo/waves/round-67/w1/LessonDraft/receipts/*` (16 files: fixture-identity, probe-line-check, live-refetch, source-quotes, strict-scratch-cmd1, strict-scratch-cmd23, three-counting-commands, default-mode-compare, default-committed.out, sweep-output, sweep.py, s233-provenance, s233-repoint, r65-pointer-status, r65-pointer-status-line686, strict-proposed-probe.py)
- `.ufo/waves/round-67/w1/LessonDraft.md` (this report)
