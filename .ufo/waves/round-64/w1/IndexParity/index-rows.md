# R64-C3(b) — README lesson-index rows for round-57..62 (seat IndexParity)

Seat dir: `.ufo/waves/round-64/w1/IndexParity/`
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` — base tip `5f517fe7147831f96a9900c9642c07ee71031940`
(freeze commit `859ac24f41061bffde588b9ed5d5adfea5ca8e27`). Date: 2026-11-03.
The lane's `corpus/README.md` was NOT edited by this seat; the L1 applies the rows below.

---

## 1. BEFORE claim — verified (receipt: `before-greps.txt`)

Command (cwd = lane root):

```
$ for n in 57 58 59 60 61 62; do grep -c "lessons/round-$n.md" corpus/README.md; done
n=57 0
n=58 0
n=59 0
n=60 0
n=61 0
n=62 0
```

Reference rows already present (same command, control): `n=51 1`, `n=52 1`, `n=53 1`, `n=63 1`.
`git rev-parse HEAD` = `859ac24f41061bffde588b9ed5d5adfea5ca8e27`.
This matches the frozen before-receipt `.ufo/waves/round-64/claims/before-state.txt`
(sha256 `416d96405671b14cd11f7661fae59ab7c9b991086532ee1cbe36f33f2cff012f`), whose
"README lesson-index parity" block prints `round-57..round-62: 0` and `round-53..round-56: 1`.

## 2. The six drafted rows

Style matched to the lane's lesson rows (round-51/52/63 for the summary shape, round-44..48
for the three-cell shape): `| `lessons/round-<N>.md` | <one-line summary: gate + mistakes
counts + verdict> | <evidence pointers> |`.

```
| `lessons/round-57.md` | Gate (S205 task.toml, S206 test_outputs.py, S207 solve.sh oracle, S208 instruction.md — four admits tier A, no rejections), two Mistakes rows (provider: stale-index `git diff` read as HEAD; landing: byte-stable ledger insertion wrote the closing brace at the wrong indent) plus a third landing row appended after the Carried section (the close-tip corpus growth tripped the r50 pointer audit and the r35 coverage checker), verdict: both claims verify (C1 admitted 9→10; C2 predicate met with the score held at its L0 cap) | LOG.md round 57; `plans/round-57-claims.md`; `.ufo/waves/round-57/` |
| `lessons/round-58.md` | Gate (S209 task.toml, S210 test_outputs.py, S211 solve.sh oracle, S212 instruction.md — four admits tier A, no rejections; the S213–S217 supersessions), four Mistakes rows (freeze: the sha-refusal kill exit was written as 2 and measured 1; landing: a mid-way-asserting script duplicated two edits on re-run; landing: a counting command named an unregistered instrument; fixture authoring: fixture lanes re-typed with doubled escapes), verdict: all three claims verify (C1 held 10, C2 9→10, C3 coverage predicate met with the score held at its L0 cap) | LOG.md round 58; `plans/round-58-claims.md`; `.ufo/waves/round-58/` |
| `lessons/round-59.md` | Gate (S218 task.toml, S219 test_outputs.py, S220 solve.sh oracle, S221 instruction.md — four admits tier A, no rejections; two reject-equivalent decisions recorded), five Mistakes rows (freeze-transcription of two table legs; instrument scope over-counting bare `exit=` labels; receipt-pointer named before the file existed; anchor authoring with a retyped word count; evidence receipt quoting a bare summary line), verdict: C1 not admitted (predicate FAIL, honestly carried), C2 admitted — the round's self-admission is FALSE under the every-claim-verifies rule | LOG.md round 59; `plans/round-59-claims.md`; `.ufo/waves/round-59/` |
| `lessons/round-60.md` | Gate (S223 GNU Grep manual output control — one admit tier A official docs, no rejections; two reject-equivalent decisions recorded), five Mistakes rows (harness exit capture swallowing `$?`; self-quoting drift doubling a token's count; same-line pairing of two commands; the self-quoting ladder rung 3; receipt quotation clipping the rc), verdict: both claims verify (C1 completion admitted with coverage held at its L0 cap; C2 admitted with operability held at the ceiling) | LOG.md round 60; `plans/round-60-claims.md`; `.ufo/waves/round-60/` |
| `lessons/round-61.md` | Gate (S224 cancel-async-tasks scoring predicate, S225 WHATWG windows-1252 index — two admits tier A code and docs, no rejections; two reject-equivalent decisions recorded), six Mistakes rows (windows-text-mode write flipping the registry's line endings; builder-property unwired; freeze-transcription recurrence; model else-branch blind spot; asserted before-anchor; environment wipes of /tmp and /mnt/c clones), verdict: both claims verify (C1 predicate met with coverage held at its L0 cap, the first-run fail carried in the record; C2 admitted with calibration held at the ceiling); the round-62 erratum re-prices two of the rows' counts | LOG.md round 61; `plans/round-61-claims.md`; `.ufo/waves/round-61/` |
| `lessons/round-62.md` | Gate (S226 TB2 task tree at the pin, S227 WHATWG windows-1252 re-open superseding S225 — two admits tier A code-host metadata and docs, no rejections; two reject-equivalent decisions recorded), five Mistakes rows (section-blind end-append into the registry's Leads section; untracked inputs named as committed; runner exit-swallow inside a `set -e` group; receipt-from-memory prose; detector-table blind spot for grader-imports-candidate and shell-exec), verdict: both claims verify (C1 census predicate met with coverage held at its L0 cap, the SETUP first run carried in the record; C2 admitted with calibration held at the ceiling, exercised) | LOG.md round 62; `plans/round-62-claims.md`; `.ufo/waves/round-62/` |
```

## 3. Every count in the rows, with the command that produced it

Source of the per-round facts: `corpus/lessons/round-<N>.md` (read in full) and, for the
round verdict line, `SCORECARD.md`'s `**Round verdict:` line for that round. Receipts:
`facts.txt`, `crosscheck.txt`, `counts3.txt`, `gate.txt`, `verdicts.txt` (all in this seat dir).

| round | lesson sha256 | Gate admits / rejects | Mistakes rows | verdict source |
|---|---|---|---|---|
| 57 | `e7c9544d95546db727739d81bcceb835c1261440ad30867286ba4de140d8ec02` | 4 / 0 | 2 in `## Mistakes` + 1 appended landing row at EOF | `SCORECARD.md:2490` |
| 58 | `533a21e65be3b3b5b2b26a9a1181e45b94165b58c5b27a75b8a360003825e9af` | 4 / 0 | 4 | `SCORECARD.md:2538` |
| 59 | `013bba219d08b0654208a29537c8c14f1ff2a3987dca7d7cdefb5bccc0ba0fc8` | 4 / 0 | 3 + 2 (appended close-tip `## Mistakes`) = 5 | `SCORECARD.md:2585` |
| 60 | `07db80df1b2c20455c10609043cb9b532711ccc4fef4097d74f5b4bbaef06ac8` | 1 / 0 | 3 + 2 (appended close-2 `## Mistakes`) = 5 | `SCORECARD.md:2654` |
| 61 | `4e68876c1c08403d9b7792ca514706ce6297098b7aa6e19bfcc5a035fc4157cc` | 2 / 0 | 6 | `SCORECARD.md:2754` |
| 62 | `b70de4bf368ae9d87b4fb8b07a88c78f3e558c3a4d84dced6df9eb69c2feb626` | 2 / 0 | 5 | `SCORECARD.md:2811` |

Counting commands (run from the lane root; the `awk` range is `^## Mistakes` … next `^## `):

```
$ grep -c '^| S[0-9]' corpus/lessons/round-57.md                 # 4   (only r57 uses a Gate table)
$ grep -c 'admit A' corpus/lessons/round-57.md                   # 4
$ grep -n 'Rejections this round\|no rejections' corpus/lessons/round-<N>.md
$ awk '/^## Mistakes/{f=1;next} /^## /{f=0} f&&/^\| /' corpus/lessons/round-<N>.md \
    | grep -v '^| *class ' | grep -c '^| '
```

Observed (from `facts.txt` / `crosscheck.txt`): r57 2, r58 4, r59 5, r60 5, r61 6, r62 5.
Note the `awk` must use `f&&/^\| /` — a bare `/^| /` is an ERE alternation and over-counts
(r60 would read 14 instead of 5); that pitfall is why the count is reproduced two ways
(`grep -v '^| *class ' | grep -c '^| '` and the per-section table walk in `counts3.txt`).

The round-57 third landing row is not inside a `## Mistakes` heading: it is appended after
the `## Carried (open, named)` section (`corpus/lessons/round-57.md:73`, landed by
`ca63378d` "round-57 close C2"). The row names it explicitly so the count is not misread.

Round-59 and round-60 each carry a SECOND `## Mistakes (...)` heading (the close-tip counter
cascade / close-2 landing); those rows are counted, hence 5 rather than 3 for each.
Round-61 carries an `## Erratum (round 62, ...)` section that re-prices two rows' counts
without changing the rows; the row count stays 6.

## 4. Placement recommendation for the L1

Put the six rows at the end of the canonical lesson-index table
`### `lessons/` — round lessons and audits (index)` (README lines 124–168, header
`| Entry | Covers | Evidence |`, last existing row `lessons/round-43-verifier-spotcheck.md`
at line 168). That table is (a) the semantic lesson index, (b) already three-cell, matching the
row format above, and (c) parsed by `plans/state_check.py`'s `readme_index_rows()`, so the
parity becomes machine-visible to the counter that checks it. Appending after line 168 keeps
the ascending round order (24→43, then 57→62).

Alternative: the `## Round29 supporting artifacts` table (README lines 538–553), where the
round-51/52/63 rows sit. That table is outside every section `state_check.py` parses, so the
rows placed there would be invisible to the counter; and its `| Path | Covers |` header is
two-cell while its round-44..48 rows are three-cell — already inconsistent. Not recommended.

Verified no-regression, on a scratch symlink farm (lane untouched; receipt `diffcheck.txt`):
with the six rows inserted into the `### lessons/` table, `state_check.py`'s `check_readme_index`
(P2e), `check_p3e` (P3e) and `check_p4b` (P4b) verdicts are unchanged for every frozen
assertion id — BASE `{'MATCH': 216, 'OUT_OF_POPULATION': 220, 'SUPERSEDED': 1}`, PATCH
`{'MATCH': 216, 'OUT_OF_POPULATION': 226, 'SUPERSEDED': 1}`, MISMATCH ids `[]` in both. The
OUT_OF_POPULATION delta is exactly +6 (the six new rows). The only other deltas are
line-number shifts of two assertions whose ids embed a line number. The new ids
`P2e.out-of-population.row.lessons/round-<N>.md@<line>` are classified OUT_OF_POPULATION
(excluded from the assertion count and never failing its exit code, by its own documented
rule at `plans/state_check.py:1350` and `:3572`). The P4b README artifact inventory is
scoped to the `## Round-26 supporting artifacts` heading (`plans/state_check.py:2463`) and
is untouched by these rows.

Post-insertion check, on the same scratch copy:

```
$ for n in 57 58 59 60 61 62; do grep -c "lessons/round-$n.md" corpus/README.md; done
round-57: 1
round-58: 1
round-59: 1
round-60: 1
round-61: 1
round-62: 1
```

Second independent instrument, the round-13 coverage census's `lessons` category (its own
`parse_index` + `category` functions, run on the two scratch READMEs; the census writes
nothing — it prints JSON). Receipt `census_diff.txt`:

| census `lessons` field | base | base + six rows |
|---|---|---|
| files on disk | 100 | 100 |
| indexed | 74 | **80** |
| unindexed | 26 | **20** |
| dangling | 0 | 0 |
| duplicate_rows | 0 | 0 |

The six round-57..62 lesson files move from `unindexed` to `indexed`; no dangling row and no
duplicate row is introduced. The remaining 20 unindexed files are other lessons
(`round-49.md`, `round-50.md`, and the `-verifier-spotcheck.md` companions) — out of this
seat's scope, named here so the L1 does not read "20 unindexed" as a failed repair.

Note on the README's own inconsistency, for the L1 to weigh (not fixed by this seat): lesson
rows currently live in three different tables — `## What's here` (round-53..56, lines 91–94),
`### `lessons/` index` (round-24..43, lines 124–168), and `## Round29 supporting artifacts`
(round-44..48, 51, 52, 63, lines 543–550). Only the first two are parsed by
`plans/state_check.py`'s `readme_index_rows()`; the Round29 table is invisible to it. The
`### `lessons/` index` placement recommended above is the one that both the state_check
parser and the round-13 census see.

## 5. Scope and limits

- This seat drafted rows and verified counts; it did NOT edit `corpus/README.md` (the L1
  applies them) and edited no lane file other than this seat's own directory.
- The round-57..62 lessons and their evidence dirs (`plans/round-<N>-claims.md`,
  `.ufo/waves/round-<N>/`, `corpus/evidence/round<N>/`) all exist at the base tip — every
  evidence pointer in the drafted rows resolves (checked, `ls -e` per path).
- The six lesson files are on disk but outside `state_check.py`'s frozen `6180e4f` population,
  so their README rows are OUT_OF_POPULATION by the tool's own rule, not a new frozen
  assertion. A future round may freeze them in; this round does not.
- No tool was installed or upgraded by this seat (nothing needed installing; `python3`,
  `grep`, `awk`, `git` read-only were sufficient). No `pacman` transaction was run.
