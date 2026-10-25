# F35MutLedgerD2 — wave 2 falsify: mutation-test r34_d2 (C2 calibration)

Seat: executor (leaf). Scope: only the `r34_d2` check (committed recursive mirror scan) in a
disposable fixture clone; plus the residual-mirror sweep under `.ufo/waves/round-34/`. No tools
installed (`git`/`python3` only, per tooling record); no labrat spawned.

## Finds

### 1. Mutation: restore one mirror file from the D2-deletion parent → D2 killed

- Deletion commit (D2): `dfcd294c60a00215c55bc4ce0b620440cd5e402f` ("round-35: C2 close round-34
  routed defects D1-D5 … mirror roots deleted …"), parent = freeze commit
  `11d64530179b78e33ba6074fc77d63d36ee7ac31` (confirmed via
  `git log --diff-filter=D --format=%H -1 -- .ufo/waves/round-34/mut-entries-scratch`).
- Fixture (per rule): `D=$(mktemp -d /tmp/k35f-XXXX)`;
  `git clone -q --no-checkout --shared <lane> "$D/lane"`;
  `git -C "$D/lane" sparse-checkout set --no-cone /corpus/ /plans/ /SCORECARD.md /.ufo/waves/round-34/`;
  `git -C "$D/lane" checkout -q dfee6fff631ebc5f623ba4506e5c7992a215401c`.
  Verified `git -C "$D/lane" rev-parse --show-toplevel` = `$D/lane` before any write; worktree clean.
- Restored one mirror file from the deletion commit's parent, byte-identical:
  ```
  git -C "$D/lane" ls-tree -r --name-only 11d6453… -- .ufo/waves/round-34/mut-entries-scratch/corpus/SOURCES.md
  # -> .ufo/waves/round-34/mut-entries-scratch/corpus/SOURCES.md
  git -C "$D/lane" show 11d6453…:.ufo/waves/round-34/mut-entries-scratch/corpus/SOURCES.md > "$D/lane/…"
  git -C "$D/lane" rev-parse 11d6453…:…   # 02ee92c4ccad3af5e196fa34f8756127ac953aaa
  git -C "$D/lane" hash-object <restored file>  # 02ee92c4ccad3af5e196fa34f8756127ac953aaa (identical)
  ```
- Fixture-commit (identity `fixture <fixture@invalid>`, inside clone only):
  `git -C "$D/lane" commit -q -m "fixture: restore one mirror file from D2-deletion parent (D2 mutation)"`
  → `52b696be72771a041ce3a09e014625ea801bc123`.
- Result — D2 flipped green→red, predicate failed:
  ```
  R34-D1 status=closed observed=pass agree=yes untracked=0
  R34-D2 status=closed observed=fail agree=NO committed_mirror_paths=1
  R34-D3 status=closed observed=pass agree=yes listed=6 evaluator_listed=True bad=0
  R34-D4 status=closed observed=pass agree=yes correction_lines=1
  R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True
  rows=5 closed=5 observed_pass=4 mismatches=1
  PREDICATE C2 fail
  EXIT=1
  ```
- Controls:
  - Baseline in the same fixture before mutation: `committed_mirror_paths=0`, D2 green, predicate pass (exit 0) — identical to the live lane at `dfee6fff` (run read-only at tip: `rows=5 closed=5 observed_pass=5 mismatches=0`, exit 0).
  - Evidence granularity: the check reads `refs/heads/master` (branch tip), not the working tree. First attempt committed onto a detached HEAD at `dfee6fff` → `refs/heads/master` unchanged → D2 stayed green; after attaching local `master` to the mutant commit (`git checkout -q -B master HEAD`), the same working tree flipped to `committed_mirror_paths=1`. Confirms the audit target is the committed branch tip (consistent with wave-1 B1/B2 findings).

### 2. Residual check: other committed recursive mirrors left under `.ufo/waves/round-34/`

At the landing tip `dfee6fff` (live lane, read-only `git ls-tree -r --name-only refs/heads/master`):
```
git ls-tree -r --name-only refs/heads/master -- .ufo/waves/round-34 \
  | grep -E '/corpus/SOURCES\.md|/\.ufo/waves/' | wc -l      # 28
```
All 28 are under the seat dir `build/R34ReviewCounterC1Attacks/` (7 seats `base,a3,a4,a5,a6,a7,a8`, 4 mirrored paths each):
- `corpus/SOURCES.md` (mirror of the corpus SOURCES file) — 7
- `.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS` — 7
- `.ufo/waves/round-34/assimilation/captures/tb2-eval/test.sh` — 7
- `.ufo/waves/round-34/claims/control-c1.txt` — 7

They predate the D2 deletion (present at parent `11d6453…`: `R34ReviewCounterC1Attacks` tree exists there) and lie outside the three roots `r34_d2` scans (`mut-entries-scratch`, `build/R34MutRegistry/mirror`, `build/R34MutRegistry/mut`) — those three roots count 0 at tip. Total committed files under `.ufo/waves/round-34/` at tip: 220; residual mirrors = 28 of 220. No round-35 wave-1 report references `R34ReviewCounterC1Attacks` (grep: no matches), so no documentation in this round marks them as handled or exempt.

## Behavior summary

| Mutation | Check | Expected | Observed | Outcome |
|---|---|---|---|---|
| restore `mut-entries-scratch/corpus/SOURCES.md` from D2-deletion parent, committed | r34_d2 | fail | `committed_mirror_paths=1` fail, predicate C2 fail, exit 1 | **killed** |
| baseline (no mutation), live tip + fixture | r34_d2 | green | `committed_mirror_paths=0`, predicate pass, exit 0 | documented |

Residual committed recursive mirrors under `.ufo/waves/round-34/` at tip: **28** (all under
`build/R34ReviewCounterC1Attacks/{base,a3…a8}/`; outside D2's scanned roots).

## Risks / notes

- Fixture commits wrote objects to the shared object store (`--shared` clone), but no lane ref/index
  was touched; clone deleted (`rm -rf /tmp/k35f-Ss0R`). Lane HEAD/status unchanged (no command wrote
  to the live lane besides read-only `ls-tree`/ledger runs).
- D2's kill rule is satisfied (reintroducing the routed defect turns the check red); the residual
  28 mirrors are outside the check's scanned roots, so D2 passes at tip despite them — a scope note
  for the L1, not a predicate violation.
- Not assessed here: D1/D3/D4/D5 (other seats), C1.

VERDICT: d2-killed-yes-residual-28
