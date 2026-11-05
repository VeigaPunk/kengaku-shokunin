# ScribeSources — round-92 scribe report (leaf seat, drafts only)

Scope: the round-92 SOURCES registry rows S283–S289, the `corpus/lessons/round-92.md`
skeleton (Gate table + empty Mistakes / Honest limits), and the M14 correction row for
`corpus/routed-findings.jsonl`. Drafts only; the L1 integrates. The lane was not written by
this seat except for the two draft files and this report named below; nothing was committed,
staged, pushed, reset or checked out in the lane; no mutating git or jj command was run in the
lane; the fleet root was not written.

## Files written

- `.ufo/waves/round-92/w1/ScribeSources/sources-rows.md` — the seven registry rows S283–S289,
  one 11-column table row each, plus the verification table and the two word-count notes.
- `.ufo/waves/round-92/w1/ScribeSources/lesson-skeleton.md` — the lesson skeleton: `## Gate`
  with one row per candidate, empty `## Mistakes` and `## Honest limits`, and the M14
  correction row as a single JSON line.
- `.ufo/waves/round-92/w1/ScribeSources/report.md` — this report.
- `.ufo/waves/round-92/w1/ScribeSources.md` — the wave-level seat report (same content,
  the path the dispatch names).

## The headline: the drafts already exist in the lane, and two word counts in the seat brief are wrong

**The rows are already landed.** Round 92's C commit `42bd5104` ("official receipt, ledger flip
35->36, SOURCES S283-S289, M14 correction row") carries S283–S289 and the M14 row; C2 `d1ccf56d`
("registry word-count corrections caught by the F2 counter (S283 4, S285 6, S287 7)") corrects
three word cells. The lesson `corpus/lessons/round-92.md` landed at F `288511d8`. So there is
nothing for the L1 to re-land from this seat: **my seven drafted rows are byte-identical to the
lane's landed rows** (cell-by-cell comparison, `IDENTICAL` for all seven), and **my M14 draft
appended to the BASE ledger reproduces the landed `corpus/routed-findings.jsonl` byte-for-byte**
(`cmp`, 254 lines, exit 0).

**Two word counts in the seat brief are wrong, and the brief's numbers are live defects.** The
brief gives S283 as `(5 words)` and S287 as `(9 words)`. The mechanical whitespace-token counts
of the quoted bytes are **4** and **7**. This is not a stylistic quibble — `plans/anchor_line_check.py`
enforces `len(quote.split()) == declared`, and with the brief's numbers the checker prints:

```
ROW S283 state=live defects=words:1 capture=corpus/evidence/round92/graders/llm-inference-batching-scheduler/tests/test_outputs.py
ROW S287 state=live defects=words:1 capture=corpus/evidence/round81/log-summary-date-ranges-probe.txt
ANCHORLINE rows=7 cited=7 captured=7 uncaptured=0 defective=2 repaired=0 live=2 cells=2
```

exit code **1**. With the counts I drafted the same tool prints
`ANCHORLINE rows=7 cited=7 captured=7 uncaptured=0 defective=0 repaired=0 live=0 cells=0`,
exit code **0**. The lane's own C2 commit had already found and fixed exactly these three cells
(the F2 counter's red output was its witness) — the brief therefore quotes the *pre-correction*
counts for two of the seven rows. My drafts carry the corrected counts, which is what the landed
rows carry.

**A third brief requirement is unsatisfiable as written.** The brief asks S285 for "quotes from
line 1 of each" of the two input-data files. `row_defects` verifies **every** quote of a row
against **one** capture (`rel = sorted(caps)[0]`), so a second quote naming
`requests_bucket_2.jsonl` is checked against `requests_bucket_1.jsonl`'s bytes and fails with a
`line` defect (`kinds=['line']`, exit 1). S285 therefore carries the bucket-1 quote and names
bucket 2's sha256 in the same anchor cell without a second line-cited quote. This is the same
one-capture-per-row constraint S289's own `teaches` cell records ("as its own row because one
row cites one capture file").

## What was actually measured (this seat)

| # | command | outcome |
|---|---|---|
| 1 | `curl` re-fetch of all 7 upstream URLs at `2fd12b88` (base `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/`) | HTTP **200** for all seven; sha256 byte-identical to the lane captures: `80b06b7c…d96ffa` (14194 B), `d3e810a9…c9ab9` (17396 B), `8b3cf1e2…f7de` (48964 B), `e15e2d4c…5cb5` (50219 B), `005f9803…53ca` (721 B), `c1d4516a…3484`, `d43c72e6…7a2f` |
| 2 | `python3 plans/anchor_line_check.py --lane <fixture> --verbose` (rows as drafted) | `ANCHORLINE rows=7 cited=7 captured=7 uncaptured=0 defective=0 repaired=0 live=0 cells=0`, **rc 0** |
| 3 | same tool, brief's `(5 words)` / `(9 words)` | `defective=2 … live=2 cells=2`, **rc 1** (red witness) |
| 4 | same tool, S285 carrying both files' line-1 quotes | `ROW S285 … defects=line:1`, **rc 1** |
| 5 | `scripts/sources-census.sh validate --today 2026-11-05 kengaku-shokunin` | `kengaku ok` — W04 duplicate-URL warnings only, all pre-existing, **rc 0** |
| 6 | `python3 plans/round92_f2_counter.py --lane <clone at HEAD> --work DIR` | `CAPTURE-PINNED S287=1,S288=1,S289=1`, `ANCHORLINE rows=281 cited=91 captured=78 uncaptured=13 defective=10 repaired=10 live=0`, `WRONG-LINE-CAUGHT True`, `PREDICATE R92-F2 pass`, **rc 0** |
| 7 | `python3 plans/round92_burndown.py --lane <clone> --rev 288511d8 --work DIR --freeze-round 92` (with `SHOKUNIN_ROOT` set) | `freeze=admitted oldest_pending_round=- pending=0 parked=24 unowned_blocked=0 malformed_unresolved=0 seeds_83_91=46 resolutions=75 checks_run=124 overrides=3`, `SELFTEST-DETAIL cases=10 red-green-ok=10`, `PREDICATE R92-C3 pass`, `PREDICATE R92-C3-BATTERY pass`, **rc 0** |
| 8 | same gate with the M14 row removed (control) | `resolutions=74`, otherwise identical, `freeze=admitted`, **rc 0** — the M14 row is a wording correction, not a verdict-changing row |
| 9 | M14 chain probe: predecessor `R84-V9-R91` deleted, M14 kept | `DEFECT supersedes-unknown R84-V9-R91-R92 -> R84-V9-R91`, `freeze=refused … pending=1`, `PREDICATE R92-C3 fail`, **rc 1** — the chain link, not the row's own check, catches a missing predecessor |

All runs were in scratch clones under `/fast/scratch/hyaku/kengaku-r92/ScribeSources/`, removed
before this seat yielded. Nothing was run against the lane tree, and the lane's own index was
never touched.

## Findings (ordered by weight)

1. **The seat brief's S283 and S287 word counts are wrong (5 and 9; the truth is 4 and 7) and the
   brief's numbers make both rows `live` defects** in `plans/anchor_line_check.py` (verified red,
   rc 1). This is the same defect class the lane's C2 commit already corrected — the brief
   reproduces the pre-correction counts. Anyone re-landing the brief verbatim would re-open three
   red rows. The drafts carry the correct counts.
2. **The brief's S285 requirement ("quotes from line 1 of each" of the two input-data files) is
   unsatisfiable under the lane's own checker**, which verifies a row's quotes against one
   capture (`sorted(caps)[0]`). The second quote produces a `line` defect (verified rc 1). One
   quote per row; both sha256 values still named in the anchor cell.
3. **The M14 row's `check` is satisfied by the row's own presence.**
   `grep -q 'R84-V9-R91' corpus/routed-findings.jsonl` matches the M14 row's own `id`
   (`R84-V9-R91-R92`), its own `supersedes` value and its own `close` text. Probed: with the
   predecessor row deleted, the check still exits 0. The gate still refuses that tree, but for a
   different reason (`supersedes-unknown`, rc 1). So the check cannot distinguish "the correction
   landed on its predecessor" from "the correction landed alone". Reported, not repaired: the
   `check` string is named in the frozen C-commit and is not this seat's to change.
4. **All seven rows and the M14 row are already in the lane** (C `42bd5104`, C2 `d1ccf56d`,
   lesson at F `288511d8`), and this seat's drafts are byte-identical to them. The L1's
   integration of this seat's work is a no-op for the registry. What this seat adds is the
   independent re-verification: the upstream bytes re-fetched and re-hashed, the word counts
   recomputed, and the checker verdicts re-run.
5. **`plans/anchor_digest_check.py` reports S283, S284 and S285 as `anchor-unbound`.** This is a
   pre-existing lane condition, not a round-92 regression: the same tool reports 55 defects at
   BASE and 58 at HEAD (+3, exactly the three new rows), and BASE already carries the identical
   class on S281 (`digest-wrong-capture`) and S282 (`anchor-unbound`). The cause is that the
   round-92 evidence directory has no `task.toml`, so the tool's upstream-URL binding cannot
   derive a capture for those three paths. The tool is **not** in the round-92 predicate set
   (no `plans/round92_*.py` references it), and the F2 counter — which *is* — passes (`live=0`).
   Reported as a finding for the next round that wants digest-bound upstream rows; not repaired
   here.

## Receipts (copied out of scratch before it was removed)

- `.ufo/waves/round-92/w1/ScribeSources/receipts/registry-rows-as-drafted.md` — the seven rows
  exactly as this seat drafted them (the file the checker verdicts above were run against).
- `.ufo/waves/round-92/w1/ScribeSources/receipts/registry-rows-brief-literal-red-witness.md` —
  the same rows with the seat brief's `(5 words)` / `(9 words)`; this is the file that produces
  the `live=2` red witness.
- `.ufo/waves/round-92/w1/ScribeSources/receipts/gate-at-HEAD.txt` — the gate at rev `288511d8`
  with the M14 row present (`resolutions=75`, `freeze=admitted`, `PREDICATE R92-C3 pass`, rc 0).
- `.ufo/waves/round-92/w1/ScribeSources/receipts/gate-M14-absent-control.txt` — the same gate
  with the M14 row removed (`resolutions=74`, otherwise identical, rc 0).
- `.ufo/waves/round-92/w1/ScribeSources/receipts/gate-M14-chain-probe.txt` — the M14 row kept
  but its predecessor `R84-V9-R91` deleted: `DEFECT supersedes-unknown R84-V9-R91-R92 ->
  R84-V9-R91`, `freeze=refused`, `PREDICATE R92-C3 fail`, rc 1.

## Out of scope (not done by this seat, not claimed)

- No `## Mistakes` or `## Honest limits` content was invented: both sections are left empty for
  the L1 to fill from the wave's measured outcomes.
- No claim verdict is asserted here. This seat measured the registry and gate surfaces its
  drafts touch; the C1/C2/C3 verdicts belong to the executor, reviewer and critic seats.
- No frozen text was repaired. The wrong word counts are reported in the drafts' own notes and
  here, not edited into any frozen file.
- The in-tree-pin residual under L0 `kengaku | round-91` stays open; this seat neither closes
  nor reopens it.

## Provenance and limits

- Tools used (no installs, no upgrades, no pacman): `git 2.56.0`, `curl 8.23.0`,
  `python3 3.14.8`, `bash 5.3.20`, `bubblewrap 0.13.1` at
  `/usr/bin/bwrap`. Host `user.max_user_namespaces` = 122865 (> 0, so bwrap sandboxing is
  available; not modified by this seat).
- `scripts/sources-census.sh` lives at the fleet root and was **read and executed read-only**
  (`validate` mode writes only to stdout; `--out` was not used). No fleet-root file was
  modified.
- The registry drafts are verified against the lane's **own** checkers (`anchor_line_check.py`,
  `anchor_digest_check.py`, `round92_f2_counter.py`, `sources-census.sh`), not against a
  re-implementation of them.
- The upstream re-fetch is a point-in-time read of `2fd12b88` on 2026-11-05; it shows the lane's
  captures are byte-exact today, which is what the rows claim and what the checks consume.
- The lane was read with `git status/log/show/rev-parse/ls-tree/diff/worktree` only. Every
  mutating git command ran inside `/fast/scratch/hyaku/kengaku-r92/ScribeSources/` on a
  `--shared` clone or a `git init` fixture whose `git rev-parse --show-toplevel` was asserted to
  equal the fixture directory before the first commit.
