# C1ScribeSources — round 52, wave 1 (build), scribe seat

Scope: draft the SOURCES-registry curation for round 52 — three candidate rows plus the
`## Gate` skeleton for `corpus/lessons/round-52.md`. Leaf seat: no subagent dispatch, no lane-tree
edit. Base tip `30801b479e3418c11089b8586178b6960216f364`.

## What I did

1. Read the frozen claims (`plans/round-52-claims.md`), the SOURCES contract v1
   (`corpus/SOURCES.md` header + `CORPUS.md` §*SOURCES.md — where a shokunin learns*), and the
   census parser `scripts/sources-census.sh` (its E01–E12 / W01–W04 rules and the `usedby_findings`
   and `row_pass` implementations).
2. Measured the base registry: row count, id gaps, next unused id, NF distribution, tier/status
   histograms, and the census exit code.
3. Fetched, in this round, the two sources the claim's C1 leg rests on: the recursive tree API
   document at pin `2fd12b88…`, and the raw `build-pmars/tests/test_outputs.py` at the same pin.
   Computed digests and counts from the bytes I fetched.
4. Searched the existing registry for rows that already cover those sources — and found two
   (S115 exact; S100/S079 the same tree at the same pin).
5. Drafted the three candidate rows and the Gate skeleton.
6. Built a throwaway scratch lane (`/fast/scratch/hyaku/kengaku-r52/C1ScribeSources/lane/`) holding a
   copy of `corpus/SOURCES.md`, `corpus/knowledge/`, `corpus/lessons/` plus a placeholder
   `corpus/lessons/round-52.md`, and ran the real census against it with `--file` to prove each row
   shape against the parser — five receipts, including two deliberate red runs.

## Exact commands

All run from `/home/vgpnk/Projects/shokunin` unless stated; `TMPDIR` explicitly set to
`/fast/scratch/hyaku/kengaku-r52/C1ScribeSources/tmp`.

```sh
# base registry measurement (read-only)
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {n[NF]++} END{for(k in n) printf "NF=%s count=%d\n", k, n[k]}' corpus/SOURCES.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' kengaku-shokunin/corpus/SOURCES.md | sort -u | awk '{n=substr($0,2)+0; if(NR>1 && n!=prev+1) printf "gap: S%d..S%d\n", prev+1, n-1; prev=n} END{printf "last: S%d\n", prev}'
./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku   # exit 0
./scripts/sources-census.sh census   --root /home/vgpnk/Projects/shokunin kengaku   # exit 0

# the two sources opened this round
curl -fsS -m 90 "https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1" -o tree.json
sha256sum tree.json
curl -fsS -m 60 "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/build-pmars/tests/test_outputs.py" -o pmars_test_outputs.py
wc -c -l pmars_test_outputs.py && sha256sum pmars_test_outputs.py
curl -fsS -m 45 "https://api.github.com/repos/harbor-framework/terminal-bench-2" -o repo_meta.json   # canonical name check

# receipts: real census, scratch lane, --file mode
./scripts/sources-census.sh validate --file /fast/scratch/hyaku/kengaku-r52/C1ScribeSources/lane/corpus/SOURCES.md
```

## Measured numbers (2026-10-28)

Base registry, `corpus/SOURCES.md` (225 lines):

- 171 rows; `NF=13` for 171/171 rows (no malformed row).
- `tier.A=147 tier.B=22 tier.C=2`; `status.mined=155 status.queued=8 status.rejected=8`.
- Last id in use **S178**; unused gaps `S87–S89`, `S95–S96`, `S98–S99` (never reused) →
  **next unused id = S179**.
- `validate --root … kengaku` → exit **0**, 15 `W04` warnings, 0 E-codes.

Pinned tree at `2fd12b88aafdd04a52c298e3940bcb189f9766d6` (one recursive tree API call):

- document keys `sha,url,tree,truncated`; `"sha": "2fd12b88…"`, `"truncated": false`, 1446 entries;
  fetched document sha256 `b5d86dfe49ca75383d6e87d36e7fadcfd60d99bc5ae18c79fbc14d272278f362`
  (453,523 bytes).
- 92 top-level entries = 89 task directories + `.gitignore`, `LICENSE`, `README.md`.
- grader files: **94** `test_outputs.py` (89 at `<task>/tests/`, 5 also at
  `<task>/environment/tests/`), **89** `test.sh`, **1** `verify.sh`
  (`configure-git-webserver/tests/verify.sh`) = **184** — equal to
  `plans/round52-tasks.json` `capture_file_count=184` and to its `capture_population` composition
  (94/89/1). The json's wider `grader_files` field lists **356** files (it also carries
  `filter.py`, `reference_illum1.png`, …), so 184 is the capture set, not every file under a
  `tests/` directory.
- `build-pmars/tests/test_outputs.py`: tree blob `size: 2938`; my fetch 2938 bytes / 85 lines,
  sha256 `d9d2796ddc19cf8159670567e174ea377e2bce675bf3451d5951c045b01f4e85`.
- `api.github.com/repos/harbor-framework/terminal-bench-2` → `full_name =
  harbor-framework/terminal-bench-2`, `archived = false`: `harbor-framework` is the current
  canonical name (S100's anchor already records that `laude-institute/terminal-bench-2`
  301-redirects here).

## Proposed ids and verdicts

| candidate | proposed id | verdict |
|---|---|---|
| TB2 grader-file population at the pin (184 files / 89 tasks) | **S179** | ADMIT — tier A, kind `code`, status `mined`, `used-by corpus/lessons/round-52.md` |
| raw `build-pmars/tests/test_outputs.py` capture at the pin | **S180** — *not to be created* | **RE-OPEN S115** (byte-identical URL + sha256); the S180 row is drafted only so the disposition is auditable |
| prior-art primary (scout seat) | **S181** (+ `S182`, `S183`, … for ≥3 distinct URLs, claims leg 4) | PENDING — row shape with `__PRIOR_ART_ROW__` / `__PRIOR_ART_KIND__` / `__PRIOR_ART_ANCHOR__` / `__PRIOR_ART_TEACHES__`; no URL invented |

## Findings

**F1 — the briefed row 2 is already registered, byte for byte.** S115 (`corpus/SOURCES.md:130`) is
"Terminal-Bench 2.0 build-pmars task grader (tests/test_outputs.py)" at the *same* raw URL, kind
`code`, tier A, status `mined`, used-by `corpus/knowledge/tb2-build-pmars-grader.md`, anchor sha256
`d9d2796d…` — identical to the digest of my independent 2026-10-28 fetch (2938 bytes, 85 lines, and
the pinned tree's blob size 2938). Nothing changed, so nothing can be superseded; the contract's
append-only rule makes this a re-open, not a new row.

**F2 — `build-pmars` cannot be a `CONFIRMED new` task under R52-C1 leg 3.**
`corpus/knowledge/tb2-build-pmars-grader.md` exists at the base tip (verified-at 2026-10-26, it also
runs `plans/build_pmars_probe.py`). Leg 3 admits only tasks "never read by this lane before this
round", so if the classifier flags `build-pmars` it must be excluded from `confirmations.json`. The
capture is still needed for `CAPTURES present=184`.

**F3 — the census has no digest-level duplicate rule.** `E04` fires only when the *scope cell is
string-equal* to the earlier row's (`scope_key = url SUBSEP scope` in `row_pass`); a reworded scope
downgrades to `W04` (warning, exit 0). Receipts: same URL + verbatim S115 scope → `E04 … within
scope …`, exit 1; same URL + reworded scope → `W04 … across scopes`, exit 0. So a second
registration of identical bytes can pass the census — the parser cannot see that S115 and S180 are
the same document. Integration must therefore be decided by digest, not by the census exit code.

**F4 — rows must be inserted inside `## Registry`, not appended at end of file.** The registry table
is followed by `## Paths`, `## Search log`, `## Leads (unopened)`. Appending the row at EOF lands it
under `## Leads` and the census fails `E12 … row outside Registry section`, exit 1 (receipt
`rc-D-e12.txt`). Insert immediately after the last `| S### |` row before `## Paths`.

**F5 — `E11` checks `used-by` for every status, not only `mined`.** `usedby_findings` walks all
registry rows. With the same S179 row but `corpus/lessons/round-52.md` absent, the census fails
`E11 S179 missing used-by corpus/lessons/round-52.md`, exit 1 (receipt `rc-C-e11.txt`). The round's
`## Gate` block therefore has to exist before the end-of-round census runs, and any row that cites
a C1 knowledge entry needs that entry on disk by then.

**F6 — the frozen fallback branch of the classification rule is unreachable for this population.**
All 89 tasks carry `tests/test_outputs.py` (`tasks without top-level grader: []`), so the rule's
"`environment/tests/test_outputs.py` when the task has no `tests/` grader" never selects a file.
Five tasks carry *both* (`break-filter-js-from-html`, `circuit-fibsqrt`, `large-scale-text-editing`,
`overfull-hbox`, `schemelike-metacircular-eval`); those 5 environment copies are part of the 184
captures but are not any task's primary grader.

**F7 — S179 does not inflate the registry.** S079 (same pin, kind `spec`) holds the task-package
schema and S100 (same pin, kind `dataset`) the top-level entry count and verifier execution. S179's
scope is the grader-file population and its per-kind counts — the population the C1 predicate's
`CAPTURES expected=184` leg reads. Because S179 cites the canonical `harbor-framework` name while
S079/S100 cite the redirecting `laude-institute` name, the census URL keys differ and neither `E04`
nor `W04` fires (confirmed by receipt `rc-A-validate.txt`: W04 count unchanged at 15).

## Census column rules I could not satisfy as literally briefed

1. **"13 columns."** Contract v1's table has **11 logical columns**; the parser wants **NF=13**,
   counting the two empty edge fields created by splitting `| a | b | … |` on `|`. A literal
   13-cell row is NF=15 and fails `E01`. All three drafts are written as 11 logical cells → NF=13
   (verified: `NF_S179=13`).
2. **Row 2 cannot be a new row without a false `supersedes`.** `E04` demands `teaches` opening
   `supersedes S### —` for a same-URL/same-scope re-registration; the bytes are identical, so the
   honest `teaches` cannot carry that clause. Reported as a rule conflict, resolved as a re-open of
   S115.
3. **`used-by` must name a path that exists at census time (F5).** All three drafts cite
   `corpus/lessons/round-52.md` — the one path the round contract already guarantees — rather than a
   C1 knowledge entry whose name is not yet fixed. If the L1 prefers the knowledge entry, add it to
   `used-by` only once the file is on disk (append-only, logged old → new in the lesson).

## Files produced (absolute paths)

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ScribeSources/report.md` (this file)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ScribeSources/sources-draft.md` — the three candidate rows + overlap/collision notes + column-rule section
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ScribeSources/gate-block-draft.md` — the `## Gate` skeleton for `corpus/lessons/round-52.md`
- `…/C1ScribeSources/tree-2fd12b88.json` — the pinned tree document I fetched (453,523 bytes, sha256 `b5d86dfe…`), reusable by the C1 capture seat
- `…/C1ScribeSources/pmars_test_outputs.py` — the fetched grader bytes (2938 bytes, sha256 `d9d2796d…`)
- `…/C1ScribeSources/rc-0-baseline-validate.txt`, `rc-0-baseline-census.txt` — base-tip census, exit 0
- `…/C1ScribeSources/rc-A-validate.txt` — S179 inserted inside the Registry: exit **0**, 0 E, 15 W04 (unchanged), `rows 172 tier.A 148 status.mined 156`
- `…/C1ScribeSources/rc-B-verbatim-scope.txt` — S180 with S115's verbatim scope: **E04**, exit 1
- `…/C1ScribeSources/rc-B-reworded-scope.txt` — S180 with a reworded scope: **W04 only**, exit 0
- `…/C1ScribeSources/rc-C-e11.txt` — S179 with the used-by file removed: **E11**, exit 1
- `…/C1ScribeSources/rc-D-e12.txt` — S179 appended at EOF: **E12**, exit 1

All drafts were produced under `/fast/scratch/hyaku/kengaku-r52/C1ScribeSources/`; the scratch dir
was removed after these copies (see the last line).

## Not done / out of scope

- No lane-tree file was created or edited: `corpus/SOURCES.md` and `corpus/lessons/round-52.md` are
  untouched — the L1 integrates.
- No prior-art URL was invented; the scout seat's fetch fills that row.
- No tool was installed or upgraded this seat (nothing was needed), so there is no
  tool/version/channel record to make.
- I did not run the C1 or C2 counters (not this seat's item) and did not re-run any sibling's work.

Scratch: `/fast/scratch/hyaku/kengaku-r52/C1ScribeSources/` removed with `rm -rf --` after the
receipts above were copied into this report directory.
