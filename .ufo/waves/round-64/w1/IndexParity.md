# R64-C3(b) — seat report: IndexParity (README lesson-index rows for round-57..62)

Seat: `IndexParity`. Wave: `kengaku r64 w1`. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
(base tip `5f517fe7147831f96a9900c9642c07ee71031940`, freeze `859ac24f`). Date: 2026-11-03.
Scope: draft the six missing README lesson-index rows and verify the BEFORE claim.
The lane's `corpus/README.md` was NOT edited (`git status --porcelain -- corpus/README.md`
is empty; `sha256 corpus/README.md` = `1d13b4291e004746c13c502b91e50f9ace42f2a2f76e0dc478c7a66b8961a451`
before and after this seat's work). The L1 applies the rows.

## Deliverables written

- `.ufo/waves/round-64/w1/IndexParity/index-rows.md` — the six drafted rows (verbatim block),
  the BEFORE greps, the per-count command table, the placement recommendation, the
  no-regression evidence.
- `.ufo/waves/round-64/w1/IndexParity/before-greps.txt` — the BEFORE receipt.
- `.ufo/waves/round-64/w1/IndexParity/{facts,crosscheck,counts3,gate,verdicts,simulate,diffcheck,census_diff}.txt`
  — every observed value with the command that produced it.
- The same seat dir holds the measurement scripts that produced them
  (`facts.sh`, `crosscheck.sh`, `count.py`, `count2.py`, `count3.py`, `gate.py`, `verdicts.py`,
  `simulate.py`, `diffcheck.py`, `census_diff.py`) so each receipt is re-derivable.

## BEFORE claim — VERIFIED

```
$ for n in 57 58 59 60 61 62; do grep -c "lessons/round-$n.md" corpus/README.md; done
n=57 0
n=58 0
n=59 0
n=60 0
n=61 0
n=62 0
```

Control rows already present: `n=51 1`, `n=52 1`, `n=53 1`, `n=63 1`.
`git rev-parse HEAD` = `859ac24f41061bffde588b9ed5d5adfea5ca8e27`.
Matches the frozen before-receipt `.ufo/waves/round-64/claims/before-state.txt`
(sha256 `416d96405671b14cd11f7661fae59ab7c9b991086532ee1cbe36f33f2cff012f`).

## The six rows (as drafted; full text in `index-rows.md` §2)

```
| `lessons/round-57.md` | Gate (S205 task.toml, S206 test_outputs.py, S207 solve.sh oracle, S208 instruction.md — four admits tier A, no rejections), two Mistakes rows (provider: stale-index `git diff` read as HEAD; landing: byte-stable ledger insertion wrote the closing brace at the wrong indent) plus a third landing row appended after the Carried section (the close-tip corpus growth tripped the r50 pointer audit and the r35 coverage checker), verdict: both claims verify (C1 admitted 9→10; C2 predicate met with the score held at its L0 cap) | LOG.md round 57; `plans/round-57-claims.md`; `.ufo/waves/round-57/` |
| `lessons/round-58.md` | Gate (S209 task.toml, S210 test_outputs.py, S211 solve.sh oracle, S212 instruction.md — four admits tier A, no rejections; the S213–S217 supersessions), four Mistakes rows (freeze: the sha-refusal kill exit was written as 2 and measured 1; landing: a mid-way-asserting script duplicated two edits on re-run; landing: a counting command named an unregistered instrument; fixture authoring: fixture lanes re-typed with doubled escapes), verdict: all three claims verify (C1 held 10, C2 9→10, C3 coverage predicate met with the score held at its L0 cap) | LOG.md round 58; `plans/round-58-claims.md`; `.ufo/waves/round-58/` |
| `lessons/round-59.md` | Gate (S218 task.toml, S219 test_outputs.py, S220 solve.sh oracle, S221 instruction.md — four admits tier A, no rejections; two reject-equivalent decisions recorded), five Mistakes rows (freeze-transcription of two table legs; instrument scope over-counting bare `exit=` labels; receipt-pointer named before the file existed; anchor authoring with a retyped word count; evidence receipt quoting a bare summary line), verdict: C1 not admitted (predicate FAIL, honestly carried), C2 admitted — the round's self-admission is FALSE under the every-claim-verifies rule | LOG.md round 59; `plans/round-59-claims.md`; `.ufo/waves/round-59/` |
| `lessons/round-60.md` | Gate (S223 GNU Grep manual output control — one admit tier A official docs, no rejections; two reject-equivalent decisions recorded), five Mistakes rows (harness exit capture swallowing `$?`; self-quoting drift doubling a token's count; same-line pairing of two commands; the self-quoting ladder rung 3; receipt quotation clipping the rc), verdict: both claims verify (C1 completion admitted with coverage held at its L0 cap; C2 admitted with operability held at the ceiling) | LOG.md round 60; `plans/round-60-claims.md`; `.ufo/waves/round-60/` |
| `lessons/round-61.md` | Gate (S224 cancel-async-tasks scoring predicate, S225 WHATWG windows-1252 index — two admits tier A code and docs, no rejections; two reject-equivalent decisions recorded), six Mistakes rows (windows-text-mode write flipping the registry's line endings; builder-property unwired; freeze-transcription recurrence; model else-branch blind spot; asserted before-anchor; environment wipes of /tmp and /mnt/c clones), verdict: both claims verify (C1 predicate met with coverage held at its L0 cap, the first-run fail carried in the record; C2 admitted with calibration held at the ceiling); the round-62 erratum re-prices two of the rows' counts | LOG.md round 61; `plans/round-61-claims.md`; `.ufo/waves/round-61/` |
| `lessons/round-62.md` | Gate (S226 TB2 task tree at the pin, S227 WHATWG windows-1252 re-open superseding S225 — two admits tier A code-host metadata and docs, no rejections; two reject-equivalent decisions recorded), five Mistakes rows (section-blind end-append into the registry's Leads section; untracked inputs named as committed; runner exit-swallow inside a `set -e` group; receipt-from-memory prose; detector-table blind spot for grader-imports-candidate and shell-exec), verdict: both claims verify (C1 census predicate met with coverage held at its L0 cap, the SETUP first run carried in the record; C2 admitted with calibration held at the ceiling, exercised) | LOG.md round 62; `plans/round-62-claims.md`; `.ufo/waves/round-62/` |
```

## Counts behind each row (each measured, not inferred)

| round | lesson sha256 | Gate admits/rejects | Mistakes rows | verdict source |
|---|---|---|---|---|
| 57 | `e7c9544d…0d8ec02` | 4 / 0 | 2 (+1 appended landing row at EOF) | `SCORECARD.md:2490` |
| 58 | `533a21e6…25e9af` | 4 / 0 | 4 | `SCORECARD.md:2538` |
| 59 | `013bba21…0fc8` | 4 / 0 | 3 + 2 (appended close-tip `## Mistakes`) = 5 | `SCORECARD.md:2585` |
| 60 | `07db80df…06ac8` | 1 / 0 | 3 + 2 (appended close-2 `## Mistakes`) = 5 | `SCORECARD.md:2654` |
| 61 | `4e68876c…4157cc` | 2 / 0 | 6 | `SCORECARD.md:2754` |
| 62 | `b70de4bf…feb626` | 2 / 0 | 5 | `SCORECARD.md:2811` |

Counting command (cwd = lane root):
`awk '/^## Mistakes/{f=1;next} /^## /{f=0} f&&/^\| /' corpus/lessons/round-<N>.md | grep -v '^| *class ' | grep -c '^| '`
→ r57 2, r58 4, r59 5, r60 5, r61 6, r62 5 (observed; `facts.txt`, `crosscheck.txt`).
The `awk` pattern must be `f&&/^\| /`: a bare `/^| /` is an ERE alternation and over-counts
(r60 would read 14). Counts were cross-checked two independent ways (section-aware awk, and a
per-section table walk) — they agree.

Convention cross-check against the lane's own precedent: README says "six Mistakes rows"
for round-51 (actual 6), "ten" for round-52 (actual 10), "five" for round-63 (actual 5) —
so the lane's own convention is "data rows under the `## Mistakes` section(s)", which is the
rule used here. Round-56's extra `## Corrections` table is not counted by that precedent
either, so round-57's `## Erratum`-style additions are treated the same way (round-61's
erratum re-prices counts without adding rows, so it stays 6).

## No-regression check for the L1's edit (scratch only; lane untouched)

`diffcheck.py` builds two scratch roots that symlink every lane entry except
`corpus/README.md` (a scratch copy each: base, and base+six-rows inserted after README line
168, the last row of the `### `lessons/` index` table). It then runs the lane's own
`plans/state_check.py` functions `check_readme_index` (P2e), `check_p3e` (P3e) and
`check_p4b` (P4b) on both and diffs the verdicts by assertion id:

```
BASE   P2e+P3e+P4b verdicts: {'MATCH': 216, 'OUT_OF_POPULATION': 220, 'SUPERSEDED': 1}
PATCH  P2e+P3e+P4b verdicts: {'MATCH': 216, 'OUT_OF_POPULATION': 226, 'SUPERSEDED': 1}
MISMATCH ids base : []
MISMATCH ids patch: []
```

No frozen assertion changes verdict; the OUT_OF_POPULATION delta is exactly +6, the six new
rows. The only deltas: line-number shifts of the assertions whose ids embed a line number
(the two `evidence/round25-*` rows move 243→249 and 242→248), and six NEW ids
`P2e.out-of-population.row.lessons/round-<N>.md@<line>` — which the tool classifies
OUT_OF_POPULATION, excluded from the assertion count and never failing its exit code by its
own rule (`plans/state_check.py:1350`, `:3572`). The P4b README artifact inventory is scoped
to the `## Round-26 supporting artifacts` heading (`plans/state_check.py:2463`) and is
untouched.

(The absolute OUT_OF_POPULATION count moved 219→220 between two runs of the same script
during this seat's work: a sibling seat added `corpus/knowledge/tb2-kv-store-grpc-offline.md`
to the lane mid-run, which is one more on-disk path outside the frozen population. It is
present in BOTH the base and the patched run, so the differential is unaffected — and that
file is not this seat's work.)

Second independent instrument — the round-13 coverage census (`corpus/evidence/round13-coverage/coverage_census.py`,
read-only; its own `parse_index` + `category` functions), `lessons` category:

| field | base | base + six rows |
|---|---|---|
| files on disk | 100 | 100 |
| indexed | 74 | **80** |
| unindexed | 26 | **20** |
| dangling | 0 | 0 |
| duplicate_rows | 0 | 0 |

The six lesson files move from unindexed to indexed; no dangling and no duplicate row appears.

## Placement recommendation (for the L1)

Insert the six rows at the end of the `### `lessons/` — round lessons and audits (index)`
table (README lines 124–168, header `| Entry | Covers | Evidence |`, last row
`lessons/round-43-verifier-spotcheck.md` at line 168). It is the semantic lesson index, it is
already three-cell (matching the row format), and it is the section
`plans/state_check.py`'s `readme_index_rows()` parses, so the parity is machine-visible to
the counter that checks it. Appending after line 168 preserves ascending round order.

Not recommended: the `## Round29 supporting artifacts` table (README lines 538–553), where
the round-51/52/63 rows sit. That table is outside every section `state_check.py` parses, so
rows placed there are invisible to the counter; and its `| Path | Covers |` header is
two-cell while its round-44..48 rows are three-cell — already inconsistent. Note also that
README lesson rows currently live in three different tables (`## What's here` lines 91–94 for
round-53..56; the `### lessons/` index for round-24..43; the Round29 table for
round-44..48/51/52/63). That inconsistency is pre-existing and outside this seat's scope —
it is named, not changed.

## Scope and limits

- This seat drafted rows and measured counts. It did NOT edit `corpus/README.md` (the L1
  applies them) and wrote no lane file outside its own seat dir. `git status --porcelain`
  shows the seat dir as the only addition attributable to this seat; the `M` entries on
  `SKILL.md` and `corpus/knowledge/*.md` are other seats' work, not this seat's.
- Every evidence pointer in the drafted rows resolves at the base tip (checked per path:
  `plans/round-<N>-claims.md`, `.ufo/waves/round-<N>/`, `corpus/evidence/round<N>/`, and the
  `LOG.md` round-N sections all exist).
- The six lesson files are on disk but outside `state_check.py`'s frozen `6180e4f` population,
  so their README rows register as OUT_OF_POPULATION by that tool's own rule, not as a new
  frozen assertion. A later round may freeze them in; this round does not.
- Remaining census `unindexed` lessons (20: `round-49.md`, `round-50.md`, and the
  `-verifier-spotcheck.md` companions) are out of this seat's scope and are named, not fixed.
- Tooling: nothing was installed or upgraded by this seat — `python3` 3.14.8, `grep`, `awk`
  and read-only `git` sufficed. No `pacman` transaction was run (the pacman guard is
  host-wide). No network call was made.
- Scratch (`/fast/scratch/hyaku/kengaku-r64/IndexParity/`) is removed before yield; every
  receipt needed is copied into the seat dir.

## Verdict

The BEFORE claim is verified (six zeros, controls at one) and the six rows are drafted with
every count measured and cross-checked. Applying them at the recommended anchor yields
`grep -c "lessons/round-<N>.md" corpus/README.md` = 1 for each N in 57..62, with no frozen
assertion changed and no dangling or duplicate index row. This seat's part of R64-C3(b) is
ready for the L1 to integrate.
