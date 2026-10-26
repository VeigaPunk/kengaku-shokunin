# R39MutC2Counter — mutation test of `plans/round39_c2_verify.py` (C2 counter)

Seat R39MutC2Counter, kengaku round 39 wave 1, 2026-10-26. Target: the frozen C2 counter
`plans/round39_c2_verify.py` (unchanged throughout; digest-checked inputs untouched in the real lane).
Question: do the counter's checks V1–V7 actually fire when the package or one of its pinned inputs is
defective? Method: assemble a **green** package in a scratch clone, run the counter pristine, then apply
**11 mutants one at a time** (each restored to byte-equality before the next), recording every DEFECT line.

## Baseline — a passing package in the clone

Scratch (operator directive 2026-10-25): `S=/fast/scratch/hyaku/kengaku-r39/R39MutC2Counter`;
`git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"`;
`git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r39/R39MutC2Counter/lane` (verified
before any write); `export TMPDIR="$S"`. Clone HEAD = lane tip `7504738` (round-39 wave-1 spec commit), which
carries the freeze commit `088f7c3`'s files: spec, gate, probe, dry table, captures, receipt.

Green package assembled from the R39PkgEntry drafts (present when I started):

- `corpus/knowledge/tb2-git-leak-recovery-grader.md` ← `R39PkgEntry/entry.md` copied verbatim (314 lines at copy
  time, sha256 `f70f3e598afcf76f2b2d30bde9de015726f26520e6b4f6ac93be644d306cbdf8`). Note for the L1: the draft
  still carries its `PRIOR-ART-PLACEHOLDER` line; **no gate clause (P1–P10) and no counter check reads that
  section**, so the baseline is green with it in place — its replacement is unvalidated by this counter.
  Also note the draft changed between my first read (secret-gone row citing 13 cases) and the copy (citing all
  16) — a sibling seat was still writing; the hash above pins the revision I mutation-tested.
- `corpus/SOURCES.md` ← `R39PkgEntry/rows.md` two rows inserted after the S116 row (before `## Paths`);
  `diff <(sed -n '132,133p' …) rows.md` → byte-equal. Clone SOURCES sha256 `63a2a3017b57a23b…`.
- `corpus/README.md` ← `R39PkgEntry/readme.md` index row inserted after line 71 (the round-38 row) and coverage
  bullet inserted after line 263 (the round-38 bullet, before `## Open gaps`); both lines diff-verified
  byte-equal to the draft.
- Staged index-only (`git -C "$S/lane" add` the three files; no commit anywhere): `M corpus/README.md`,
  `M corpus/SOURCES.md`, `A corpus/knowledge/tb2-git-leak-recovery-grader.md` — the gate's P9 clean-tree clause
  needs drafts staged, and P9 then reports `untracked=0`.

Pinned-input digests in the clone matched the counter's constants before any mutation: spec `f62163ce…`,
gate `ea638822…` (P1), probe `4961a50f…`, dry table `e92a5d6d…`, Dockerfile `006bf5d2…`.

Baseline run (`cd "$S/lane" && TMPDIR=$S python3 plans/round39_c2_verify.py --lane . --work "$S/w"`):

```
V1 ok listed=7 bad=0 extra=0
    gate: P1..P10 all ok (P3 rows=29 distinct_quotes=29 distinct_lines=29; P10 probe_rerun=byte-equal bytes=5867)
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=2 bad=0
V4 ok cases=25 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=4 tags=4 bad=0
checks=7 defects=0
PREDICATE C2 pass      (exit 0, ~1.5 s per run)
```

## Mutants (one at a time; detector = the same counter command; restore = `cp` from a pre-mutation backup, verified with `cmp`)

| # | Target (clone path) | Mutation | Fired | DEFECT line(s) verbatim | Verdict |
|---|---|---|---|---|---|
| M01 | entry `## Requirement map` | `secret-gone` label `partly` → `enforced` | V7 | `V7 DEFECT rows=4 tags=4 bad=['secret-gone: labelled enforced, receipt derives partly']` | caught |
| M02 | entry map | `files-untouched` row cites `message-rewritten` (violates only `messages-untouched`) instead of `readme-edited` | V7 | `V7 DEFECT rows=4 tags=4 bad=['files-untouched: cites no case or a case that does not violate it']` | caught |
| M03 | entry map | `files-untouched` row duplicated (identical line appended) | V7 | `V7 DEFECT rows=5 tags=4 bad=["tags missing=0 duplicated=['files-untouched']"]` | caught |
| M04 | entry map | `messages-untouched` row deleted | V7 | `V7 DEFECT rows=3 tags=4 bad=["tags missing=['messages-untouched'] duplicated=0"]` | caught |
| M05 | entry map | `messages-untouched` row line `instruction.md:5` → `instruction.md:4` | V7 | `V7 DEFECT rows=4 tags=4 bad=['messages-untouched: line 4 is not the frozen instruction.md:5']` | caught |
| M06 | `corpus/SOURCES.md` | S117 anchor cell `sha256 dc7b01c1…` → `sha256 54ac693f…` (S118's digest) | V3 | `V3 DEFECT rows=2 bad=['S117:anchor_digest']` | caught |
| M07 | `corpus/evidence/round39/git-leak-probe.txt` | `CASE untouched …` line deleted | V2+V4+V7 | gate `P10 DEFECT fresh probe output is not byte-equal to the receipt`; `V2 DEFECT … gate_exit=1`; `V4 DEFECT cases=24 … bad=['case ids differ from the frozen table', 'summary disagrees with the CASE lines']`; `V7 DEFECT … bad=['recover-secret: cites no case or a case that does not violate it', 'secret-gone: cites no case or a case that does not violate it']` | caught |
| M08 | `plans/pkg-spec-r39.json` | one byte: `"min_quotes": 8` → `9` | V2+V3+V4+V7 | `error ValueError: spec template not at its freeze digest` (in each) | caught |
| M09 | `corpus/evidence/round39/git-leak-dry-cases-freeze.txt` | one byte: summary `predicted_pass=13` → `14` | V4+V5+V7 | `V4/V7 error ValueError: dry table not at its freeze digest`; `V5 DEFECT probe or dry table not at freeze digest` | caught |
| M10 | `plans/git_leak_probe.py` | one docstring byte: `offline` → `ofline` (behaviour-preserving) | V2+V5 | gate `P1 DEFECT pinned=2 mismatched=['plans/git_leak_probe.py']`; `V2 DEFECT … gate_exit=1`; `V5 DEFECT probe or dry table not at freeze digest` | caught |
| M11 | `corpus/evidence/round39/tb2-git-leak-recovery/Dockerfile` | one byte: `FROM` → `FRM` | V1+V2 | `V1 DEFECT listed=7 bad=['Dockerfile'] extra=0`; gate `P5 DEFECT … first=Dockerfile: manifest digest does not match the bytes`; `V2 DEFECT … gate_exit=1` | caught |

Every mutant run ended `checks=7 defects=N` (N = number of fired checks above), `PREDICATE C2 fail`, exit 1
(M02's exit re-captured cleanly after a piped first run: `counter_exit=1` via `${PIPESTATUS[0]}`). No mutant
survived; no invalid mutants; no null detections (the pristine baseline stayed green throughout between
mutants, so every firing is attributable to the single mutation).

## What the run shows about the counter's defence-in-depth

- **The map (V7) is checked from three independent directions**: label vs receipt-derived label (M01), citation
  closure against the receipt's `violates=` sets (M02, and M07's V7 leg), and tag-set equality with the frozen
  dry table plus line binding (M03, M04, M05).
- **The receipt is defended in depth** (M07): gate P10 re-runs the probe and byte-compares (authenticity), V4
  re-derives ids/order/summary from the frozen dry table (structure), and V7's citation closure breaks when a
  cited case disappears. Deleting one CASE line fires three of seven checks.
- **Digest pinning is layered**: a spec byte kills four checks (every `spec()` caller), a dry-table byte three,
  a probe byte two (counter V5 + gate P1's instrument pin), a capture byte two (counter V1 + gate P5's manifest
  re-hash). M10 was deliberately behaviour-preserving (docstring) and was still caught — by digests, not by
  behaviour; P10 stayed `byte-equal`.
- **V6 (census) is structural only**: under M06 the census stayed `census_exit=0` while V3 fired — the census
  validates row shape/enums/used-by paths, not anchor digests. Anchor authenticity rests entirely on V3.

## Untested arms (honest scope of this probe)

Single-site mutants only; no multi-mutant or interaction runs. Arms not exercised: V1's `extra=` manifest arm
and its unparsed-line arm; V2's effective-spec path (the counter always writes a fresh effective spec, so the
gate never read a spec file from the tree); V3's row-count/cell-count arms; V4's `match=NO` naming arm (the
receipt has `mismatches=0`, so nothing to name) and its absent-file arm; V5's probe-crash arm; V6's failure
direction; V7's unparsed-row arm; gate P9's untracked-file arm (baseline had none). The counter's own code was
never mutated — this probe measures whether its checks fire on defective **inputs**, per assignment.

## Provenance and restoration evidence

- Commands: baseline/mutant detector `cd "$S/lane" && TMPDIR=$S python3 plans/round39_c2_verify.py --lane .
  --work "$S/w"`; restoration `cp "$S/backup/<name>" <target>` then `cmp -s` (all seven targets:
  `RESTORED-BYTE-EQUAL` ×7, plus `FINAL-RESTORE-BYTE-EQUAL` for the entry after the M02 re-run).
- Pristine hashes recorded before mutation (see Baseline); after restoration every target `cmp`-equal to its
  backup; post-restore counter run green again (`checks=7 defects=0`, `PREDICATE C2 pass`, exit 0).
- The real lane was never written: no commit/stash/checkout/reset anywhere; the only `git add` ran inside
  `$S/lane` (my clone). Scratch deleted after receipts were written.
- Tooling installed: none (uv 0.13.0, git 2.56.0, host python3 already present; `uv run --with
  biopython==1.85` pre-warmed once for the gate's P10 interpreter choice — no package installed host-wide).

## Receipts

Full verbatim outputs (baseline, post-restore, and each mutant's counter output): see
`.ufo/waves/round-39/build/R39MutC2Counter/receipts.md` in this seat dir.

VERDICT: c2-mutants-11/11
