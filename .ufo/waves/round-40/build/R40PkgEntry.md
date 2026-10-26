# R40PkgEntry — C2 package draft (kengaku round 40, wave 1)

Seat: scribe, leaf (no subagents, no lane writes). Work is a **draft for the L1 to integrate**; the lane's
`corpus/`, `plans/`, `README.md` and Git index were not touched. All proof ran in
`/fast/scratch/hyaku/kengaku-r40/R40PkgEntry/` (NVMe scratch, deleted at the end of this seat).

## Drafts (paths handed to the L1)

| Draft | Becomes | sha256 | Lines |
|---|---|---|---|
| `.ufo/waves/round-40/build/R40PkgEntry/entry.md` | `corpus/knowledge/tb2-db-wal-recovery-grader.md` | `5a8b1389…58c` | 306 |
| `.ufo/waves/round-40/build/R40PkgEntry/rows.md` | two rows appended to `corpus/SOURCES.md` `## Registry` after S118 | `791941a3…bf8` | 13 |
| `.ufo/waves/round-40/build/R40PkgEntry/readme.md` | `corpus/README.md`: one index row after the `tb2-git-leak-recovery-grader.md` row (now line 72) **and** one coverage bullet after the "(fifth task, repository-history class)" bullet (now line 265) | `52c2bb1c…a98` | 13 |

Receipts: `.ufo/waves/round-40/build/R40PkgEntry/c2-counter-receipt.txt` (counter run + exit),
`.ufo/waves/round-40/build/R40PkgEntry/recheck-and-staging.txt` (`sha256sum -c SHA256SUMS`, staged diff).

**Idempotency note for the L1:** the lane working tree already carries the two S119/S120 rows as an uncommitted
2-line addition to `corpus/SOURCES.md` (`git diff corpus/SOURCES.md` = `+2`); `rows.md` reproduces them
byte-for-byte, so integrating once is enough — do not append a second copy. The entry and the two README fragments
do not exist in the lane yet.

## Behavior: what the drafts say

`entry.md` follows `corpus/knowledge/tb2-git-leak-recovery-grader.md`: four front-matter lines (two
`source:` lines at the exact pinned raw URLs, `verified-at: 2026-10-26`, one `recheck:` line whose command runs
green as written), then Summary / Source labels / What is graded (static reading) / Located quotes /
Requirement map / Contestable tags / Findings / Regrade / What the probe does not show / Prior art /
Negative space (with falsifier).

Grounded content, all derived from the capture and the receipt, none invented:

- **Seven functions, one path.** Every one of the seven grader functions opens only `/app/recovered.json`
  (`test_outputs.py:9,14,23,40,49,85,94`); no function opens `main.db` or `main.db-wal`.
- **Pin surface 22 of 33 cells.** ids pinned structurally (`:53`, `:57-58`), values of ids 1-2 (`:64-67`), names of
  ids 3-11 (`:70-80`); free are the names of ids 1-2 and the nine values of ids 3-11.
- **Requirement map, six tags, labels derived (not chosen)** from every receipt case carrying the tag:
  `fix-wal` `instruction.md:7` → **partly**; `extract-all` `:8` → **partly**; `json-at-path` `:9` → **enforced**;
  `record-format` `:12` → **partly**; `sorted-by-id` `:13` → **enforced**; `eleven-records` `:13` → **enforced**.
  Tag frequencies recomputed from the receipt: `fix-wal` 23, `extract-all` 15, `eleven-records` 10,
  `record-format` 8, `json-at-path` 5, `sorted-by-id` 1 (command below).
- **Regrade column** stated with its mechanism: `regrade cases=28 differ=0`; every function re-reads the same
  export from disk and reads no clock, environment or network, so the second grading of an unchanged state is
  identical — a determinism check on the probe, not a claim about graders in general.
- **Limits** named: image never pulled; host sqlite3 3.54.0 / python3 / xxd stand in and the image's own sqlite
  version was **not** fetched (`https://packages.ubuntu.com/noble/sqlite3` answered HTTP 500 on 2026-10-26, so the
  draft says so rather than naming a version); recipes run unprivileged inside `bwrap`; `tests/test.sh` read, not
  run; seven predictions are pilot copies (`untouched`, `oracle-solve-sh`, `base-only-ro`,
  `literals-never-open-db`, `literals-names-1-2-wrong`, `literals-id3-name-wrong`, `truth-value-float-id1`) and
  `plain-read-then-solve` rests on the round-39 seat's ungraded measurement.
- **Prior art is a marked placeholder** — `.ufo/waves/round-40/build/R40ScoutPriorArt.md` did not exist when this
  draft was written (`test -f … || echo PRIOR_ART_ABSENT` → `PRIOR_ART_ABSENT`); the section names the artifact, tells
  the L1 to fill it, and keeps the claim narrow ("a probed instance of the TB2 `db-wal-recovery` grader").
- **Falsifier** is four-part and executable: digest mismatch on re-fetch; a fresh probe printing anything other than
  `cases=28 observed_pass=8 observed_fail=20 mismatches=0` + `regrade cases=28 differ=0` (with the eight passing and
  twenty failing ids listed); any grader line opening a file other than `/app/recovered.json` or comparing more than
  the 22 pinned cells; the grader raising on `literals-never-open-db` or passing any function on
  `decrypt-in-place-no-json`.

## Gates: the frozen counter

Placed the three drafts in a `git clone --shared` of the lane HEAD, staged them (`git add -A`; the gate's P9 needs
staged drafts), then ran the frozen counter. Output, verbatim
(`.ufo/waves/round-40/build/R40PkgEntry/c2-counter-receipt.txt`):

```
$ git -C /fast/scratch/hyaku/kengaku-r40/R40PkgEntry/lane add -A
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round40_c2_verify.py --lane /fast/scratch/hyaku/kengaku-r40/R40PkgEntry/lane --work /fast/scratch/hyaku/kengaku-r40/R40PkgEntry/w
V1 ok listed=8 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=16 distinct_quotes=16 distinct_lines=16 out_of_word_range=0
    gate: P4 ok checked=16 bad=0 first=0
    gate: P5 ok manifest_entries=8 bad=0 first=0
    gate: P6 ok rows=2 bad=0 first=0
    gate: P7 ok source_lines=2 bad=0 first=0
    gate: P8 ok index_rows=47 knowledge_files=47 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=8257
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=2 bad=0
V4 ok cases=28 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=6 tags=6 bad=0
checks=7 defects=0
PREDICATE C2 pass
exit=0
```

Staged state proved (`recheck-and-staging.txt`): `corpus/README.md | 2 +`, `corpus/SOURCES.md | 2 +`,
`corpus/knowledge/tb2-db-wal-recovery-grader.md | 306 +`; `git status --porcelain` shows only those three
(`M`, `M`, `A`), no untracked file (P9).

### One iteration, recorded

First run: `checks=7 defects=1`, `V7 DEFECT … bad=['fix-wal: cites no case or a case that does not violate it']`.
Cause: the `fix-wal` map row cited `decrypt-in-place-no-json`, which in the frozen receipt does **not** carry the
`fix-wal` tag (`violates=extract-all,json-at-path,eleven-records`) — a cited id must be one of the tag's violating
cases. Fixed by citing `xor-wrong-key` instead (a `fix-wal` violator observed fail). Nothing else changed; re-run
`checks=7 defects=0`. The frozen table, tags and labels were not edited.

## Evidence commands (each number above carries one)

- Quote coverage, line-exact: a 16-row check of `text in capture_line` over `test_outputs.py` and `instruction.md`
  → all 16 verbatim, word counts 5-16 (inside the 3-25 bound); the gate's own `P4` re-verifies the same 16 rows
  (`checked=16 bad=0`). Distinct lines: 10 in `test_outputs.py` (`:9,13,17,27,33,53,58,64,80,98`), 6 in
  `instruction.md` (`:3,7,8,9,12,13`).
- Tag frequencies: `re.match(r"^CASE (\S+) .*?violates=(\S*)")` over `corpus/evidence/round40/db-wal-probe.txt`
  → `{'fix-wal': 23, 'extract-all': 15, 'eleven-records': 10, 'record-format': 8, 'json-at-path': 5,
  'sorted-by-id': 1}`, 28 cases.
- Recheck line green as written, from the clone root:
  `(cd corpus/evidence/round40/tb2-db-wal-recovery && sha256sum -c SHA256SUMS)` → eight `OK` lines, `exit=0`.
- Probe reproducibility, independently of the gate: `python3 plans/db_wal_probe.py --lane . --work <scratch>`
  → 28 `CASE` lines, 8257 bytes, `real 0m1.205s`, stderr empty, `cmp` against
  `corpus/evidence/round40/db-wal-probe.txt` → `BYTE_EQUAL_TO_RECEIPT`; tail lines
  `regrade cases=28 differ=0` / `cases=28 observed_pass=8 observed_fail=20 mismatches=0`.
- Census: `scripts/sources-census.sh validate --file <clone>/corpus/SOURCES.md` → `census_exit=0` inside the
  counter (`V6`); before the entry existed the same command on the lane file exited 1 with
  `E11 S119/S120 missing used-by corpus/knowledge/tb2-db-wal-recovery-grader.md`, which is exactly what the entry
  supplies. Its `W04` lines (duplicate URLs across scopes) are warnings and do not affect exit.
- Line citations used in the entry were numbered, not guessed: `grep` with a line-numbering pattern over
  `test_outputs.py`, `instruction.md`, `test.sh`, `task.toml`, `Dockerfile`, `solve.sh`; the Dockerfile `COPY` lines
  corrected from a first-draft `:12-13` to the measured `:14-15` (`WORKDIR` is `:12`).

## Findings worth the L1's attention

1. **The grader is blind to its own source of truth.** Seven functions, one file under test. The instruction's first
   requirement ("Fix the WAL file", `instruction.md:7`) has no assertion: `decrypt-in-place-no-json` (WAL repaired,
   no export) scores `FFFFFFF`, and `literals-never-open-db` (export typed, database never opened) scores `PPPPPPP`.
   This is the entry's headline and the reason `fix-wal`/`extract-all` derive `partly` while the frozen rule still
   reports them as tags with mixed violating verdicts.
2. **The pin surface is 22/33 cells, not the table.** Nine values and two names are free, so a fabricated export is
   indistinguishable from an extracted one outside the pinned cells (`truth-value-id3-wrong` 301 passes,
   `truth-bool-value-id5` `true` passes, `literals-names-1-2-wrong` passes).
3. **The type gate is one-directional.** `isinstance(item["id"], int)` is the only place id type is read, so
   `1.0…11.0` fails exactly one test (`PPFPPPP`); `True` satisfies the value type; the key test is a subset, so an
   extra field passes.
4. **The destructive read is the task's own trap.** `plain-read-then-solve` and `base-only-ro` score the same
   `PPPPFPF`: one read-write `sqlite3` open deletes the undecryptable WAL, after which even `solve.sh` loses two
   tests. The oracle's own comment (`solve.sh:8`) says it reads read-only "to avoid WAL interaction".
5. **A wrong XOR key is scored as a missing six rows** (`xor-wrong-key`, `PPPPFPF`) — the grader cannot tell a
   failed decryption from a deleted log.

## Out of scope (deliberately not done)

- No edits to the lane: `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`, `PROVINCE.md`, `SHONEN.md`,
  `.ufo/waves/round-40/claims/` all untouched; no git/jj mutation in the lane; the source repo
  `/home/vgpnk/Projects/shokuknow` never touched.
- No changes to the frozen instruments (probe, gate, spec, counters, dry table, captures, receipt) — `P1`
  `pinned=2 mismatched=0`, `V5` `dry_byte_equal=True`, `V1` `bad=0` re-assert all of them.
- No prior-art research of my own (wave-1 scout artifact absent); the section is a placeholder for the L1.
- No claim about task validity, agent solvability, contamination, or the other 83 TB2 graders.

## Tooling / environment record

No install or upgrade was performed. `uv` (`/home/vgpnk/.local/bin/uv`) and a cached `biopython==1.85` were already
present and used only by the gate's `c_rerun` fallback path (host python has no `Bio`); pacman was not used
(transactions paused host-wide). Host instruments: sqlite3 3.54.0 (2026-10-09), python3, `/usr/bin/xxd`.

## Scratch hygiene

`S=/fast/scratch/hyaku/kengaku-r40/R40PkgEntry` (`TMPDIR`, clone, `w/`, `w2/`) — receipts copied into this report
directory first, then `rm -rf -- "$S"`. Nothing was written under `/tmp`, into the fleet root, into a sibling lane,
or into the lane's Git index.

VERDICT: c2-package-draft-checks-7-defects-0
