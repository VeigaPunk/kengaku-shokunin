# R35MutC1V1V6 — mutation probe of C1 checks V1 and V6 (round 35, wave 1, 2026-10-25)

Seat: R35MutC1V1V6 (mutation-tester). Scope: C1 counter `plans/round35_c1_verify.py` checks V1
(capture manifest) and V6 (sources census), on a fixture clone built per the wave-1 fixture rule.
Frozen claim: `plans/round-35-claims.md` (freeze commit `11d64530179b78e33ba6074fc77d63d36ee7ac31`
= lane master HEAD during this probe, `git log -1` confirmed).

## Axes (godspeed)
1. Kill power of V1 (does any manifest corruption flip it red?).
2. Kill power of V6 in clone mode (`--file`) without collateral on V1–V5.
3. Calibration: byte-identical replacement must NOT flip anything (no provenance sensitivity).
4. Restoration integrity: pristine bytes and pristine detector output recoverable after each probe.

## Fixture
```
D=/tmp/k35-Tmca  (mktemp -d /tmp/k35-XXXX)
git clone -q --no-checkout --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone '/corpus/README.md' '/corpus/SOURCES.md' \
  '/corpus/knowledge/**' '/corpus/evidence/round35/**' '/plans/round35_c1_verify.py' '/plans/tb2_grader_probe.py'
git -C "$D/lane" checkout -q master
git -C "$D/lane" rev-parse --show-toplevel   # -> /tmp/k35-Tmca/lane  (== $D/lane, TOPLEVEL_OK)
git -C "$D/lane" log -1                       # 11d6453 round-35: freeze claims, counters, probe, ledger, controls
```
Uncommitted C1 surfaces copied from the live working tree into the clone (they are untracked or
modified at the freeze commit; fixture rule directs this):
- `corpus/SOURCES.md`, `corpus/README.md` (modified, tracked), `corpus/knowledge/tb2-protein-assembly-grader.md`
  and `corpus/evidence/round35/` (untracked: `git status --porcelain` → `?? corpus/evidence/round35/`,
  `?? corpus/knowledge/tb2-protein-assembly-grader.md`).
- Copied evidence hashes equal live: SHA256SUMS `ec42f631…df7ed36`, tb2-grader-probe.txt
  `2359d906…12b25b8` (sha256sum both sides).
- Fixture iteration 1 (recorded honestly): first pristine run had `V6 DEFECT census exit 1` —
  diagnosis: the sparse checkout omitted `corpus/lessons/**`, so census `--file` emitted ~47
  `E11 missing used-by corpus/lessons/round-NN.md` findings. Fixture-completeness artifact, not a
  detector defect. Fixed by `git -C "$D/lane" sparse-checkout add '/corpus/lessons/**'` + copying
  live lessons; census then validated clean in both modes.

## Pristine baseline (after fixture fix) — `cd /tmp/k35-Tmca/lane && python3 plans/round35_c1_verify.py --lane .`
```
V1 ok
V2 ok
V3 ok
V4 DEFECT knowledge files=41 index rows=42 (want 42/42)
V5 ok
V6 ok
checks=6 defects=1
PREDICATE C1 fail
exit=1
```
V1 and V6 (this seat's targets) are green. V4's red is a fixture artifact, constant across every
run below: the round-35 entry is untracked, `git add` is forbidden, so `git ls-files
corpus/knowledge/*.md` in the clone counts 41 while the copied live README has 42 index rows.
It cannot confound V1/V6 verdicts. [INFERENCE for the live lane: V4 will read 42/42 once L1
commits the entry at landing; V4 is not this seat's check.]

## V6 mode confirmation (read the code, run both)
Code (`plans/round35_c1_verify.py:182-187`):
```python
def v6(lane, fleet):
    script = str(fleet / "scripts/sources-census.sh")
    if lane == (fleet / "kengaku-shokunin").resolve():
        cmd = [script, "validate", "--root", str(fleet), "kengaku"]
    else:  # a fixture/clone lane: validate its own registry, never the live lane's
        cmd = [script, "validate", "--file", str(lane / "corpus/SOURCES.md")]
```
- Live mode, run directly: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate
  --root /home/vgpnk/Projects/shokunin kengaku` → exit 0, no E findings.
- Clone mode, run directly and via every detector run below: `validate --file
  /tmp/k35-Tmca/<copy>/corpus/SOURCES.md` → exit 0 pristine (15 W04 warnings only; W-codes never
  change status per the census header), exit 1 under mutant M5. Both branches exercised, both
  green at pristine.

## Mutants (same bounded detector each run: `python3 plans/round35_c1_verify.py --lane .` in the mutant's own fixture copy)

Before-hashes (all copies identical to main fixture, sha256sum):
SHA256SUMS `ec42f6317916473516179e8b8750bedf3f3c2eaf1f1a8ff9a733fb8f4df7ed36`;
test_outputs.py `44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582`;
SOURCES.md `a00684a42d0effda23a036fadf35e1657646b3a66cd2c7b00755e69de491da1a`.

| # | Mutant | Target | Expected | Observed (detector output, verbatim lines) | Verdict |
|---|--------|--------|----------|---------------------------------------------|---------|
| M1 | SHA256SUMS line for instruction.md deleted | V1 red | `instruction.md not listed at pinned digest` | `V1 DEFECT instruction.md not listed at pinned digest`; V6 ok; exit 1 | **killed** |
| M2 | test.sh digest first hex char 9→0 | V1 red | digest mismatch on test.sh | `V1 DEFECT listed digest mismatch or missing file: test.sh`; V6 ok; exit 1 | **killed** |
| M3 | phantom line `e3b0c442…52b855  phantom.txt` appended to SHA256SUMS (file absent on disk) | V1 red | listed-but-missing caught | `V1 DEFECT listed digest mismatch or missing file: phantom.txt`; V6 ok; exit 1 | **killed** |
| M4a | test_outputs.py replaced with round-34 copy `.ufo/waves/round-34/assimilation/captures/tb2-eval/test_outputs.py` (`cmp` IDENTICAL to round-35 capture) | stays green (same bytes) | output identical to pristine | `V1 ok … V6 ok`, defects=1 (V4 artifact only) — byte-for-byte the baseline | **control green (as required; no false positive)** |
| M4b | one-byte edit `acceptor_aa`→`acceptor_ab` (test_outputs.py:40) | V1 red | digest mismatch | `V1 DEFECT listed digest mismatch or missing file: test_outputs.py` AND `V5 DEFECT fresh probe output differs from receipt (exit 2)` (double detection: manifest + behavioral); exit 1 | **killed** |
| M5 | ten-cell row appended inside `## Registry`: `\| S199 \| Mutation probe synthetic row \| docs \| A \| m5-probe \| p1 \| synthetic ten-cell row for census E01 probe \| mined \| 2026-10-25 \| 180d \|` | V6 red via clone `--file` path | census E01 | `V6 DEFECT census exit 1`; census detail: `file	E01	S199 fields=10`; V2 ok (S199 is not one of S105–S107, so v2 correctly ignores it — clean attribution to V6); exit 1 | **killed** |

Kill accounting: 6 probes, 5 killed (M1, M2, M3, M4b, M5), 1 designed same-bytes control correctly
green (M4a). Unexpected survivors: 0. A baseline failure made no mutant inconclusive: baseline was
green on V1/V6 before and after every probe.

## Restoration evidence
After each probe the mutated file was `cp`-restored from the untouched main fixture and
byte-compared (`cmp`), then the detector was re-run on the restored bytes:
- m1/m2/m3 SHA256SUMS: `cmp` identical; sha256 `ec42f631…df7ed36` (== before). Detector rerun: `V1 ok … V6 ok`, defects=1 (V4 artifact only).
- m4same/m45 test_outputs.py: `cmp` identical; sha256 `44a05a24…096582` (== before). Detector rerun: same baseline.
- m5 SOURCES.md: `cmp` identical; sha256 `a00684a4…91da1a` (== before). Detector rerun: same baseline.
(M1's first restore command was lost to a truncated tool call — caught by the restoration pass,
re-restored, re-verified above. No mutated bytes survived.)

## Notes for the L1 (observations, not defects found)
1. V1's listed-digest loop also covers the three non-graded capture files (task.toml,
   antibody.fasta, pdb_ids.txt) — deletion/digest drift of any listed file flips V1 red (M3 form).
2. V6 clone mode is load-bearing: it validates the clone's own registry (`--file`), never the live
   lane's, so a fixture mutant cannot report the live lane's health. Confirmed by code and by run.
3. V4 in any fresh clone of master reads 41/42 until the round-35 entry is committed — any
   wave-2 clone-based verifier should expect exactly this artifact and not "fix" V1/V6 because of it.
4. The census `--file` mode reports duplicate-URL W04 warnings (15 in this corpus); they do not
   affect exit status, consistent with the script header ("warnings do not affect clean lanes").

Fixture `rm -rf /tmp/k35-Tmca` executed after the restoration pass. No lane file outside
`.ufo/waves/round-35/build/` was written; no git/jj mutating command ran in the lane.

VERDICT: v1v6-killed-5/6
