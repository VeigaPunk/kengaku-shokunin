# F37MutC2Counter — mutation test of the C2 counter on the landed package

Seat: F37MutC2Counter (mutation-tester, leaf). Date: 2026-10-26. Round: kengaku r37, wave 2 (falsify).
Target: `plans/round37_c2_verify.py` (the C2 counter) run against the landed C2 package at tip `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`.
Method: 10 single mutants — each the smallest edit realizing one named defect class — applied one at a time to scratch clones; the counter ran after each; exact bytes were restored and hash-verified before the next mutant. Two supplementary probes (S1, S2) sharpen the clause-level picture.

## Protocol

- Scratch (deleted at end of session): `/fast/scratch/hyaku/kengaku-r37/F37MutC2Counter`; `TMPDIR` pointed there; every counter run used `--work $S/work`.
- Clone A `$S/fx/lane` and clone B `$S/fx/laneB`, each: `git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin <dir>`; `git -C <dir> checkout -q 357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`; `git -C <dir> rev-parse --show-toplevel` == the clone dir (checked, `TOPLEVEL_OK` / `TOPLEVELB_OK`); `git status --porcelain` empty before and after every mutant.
- Counter command (both clones, every run): `python3 plans/round37_c2_verify.py --lane . --work "$S/work"` with cwd = the clone. Raw output per mutant: `.ufo/waves/round-37/falsify/F37MutC2Counter/mutant-*.txt` (teed from the run).
- Restoration: pristine copies of the five mutable files kept under `$S/pristineA|B`; after each run `cp` back and `sha256sum` compared. Pristine hashes (recorded before any edit, identical in both clones):
  - entry `corpus/knowledge/tb2-git-webserver-grader.md` = `6e3f8c77139f64737bc64094f7c91a3e7f7598e1ebdce91cb0fd92eb4854812a`
  - `corpus/SOURCES.md` = `c1c9b533e71f8a229f99f78768bfc39e06a107a97bd491d11075966740b12351`
  - `corpus/README.md` = `3e547056701ebbd5a6295f0e46fd7628f36ef00db26a3a4b1de6e0fa4a3940ef`
  - `corpus/evidence/round37/tb2-git-webserver/SHA256SUMS` = `e70bb662f74fe3271b16e95e694276ba8ef0fd468856ac3c1fae287a38a3531f`
  - `corpus/evidence/round37/git-webserver-probe.txt` = `835507129cb536ff6c927b5b05650dd4712891bd3ec218948659655597ec29f8`
- Final sweep: all five hashes equal the pristine values in both clones; the M10 file absent; `git status --porcelain` = 0 lines in both clones.

## Baseline (clean clone, no mutant)

`python3 plans/round37_c2_verify.py --lane . --work "$S/work"` →
`V1..V7 ok`, `checks=7 defects=0`, `PREDICATE C2 pass`, `EXIT=0`, `real 0m53.030s` (gate P10 re-runs the frozen probe, byte-equal, 8443 bytes). Receipt: `F37MutC2Counter/baseline.txt`. The frozen C2 predicate reproduces on my clone.

## Mutants — 10/10 turned the counter red

Every run ended `PREDICATE C2 fail`, `C2_EXIT=1`. DEFECT lines pasted verbatim from the runs.

**M1 — one quote off by a line.** Entry `## Located quotes` row: `test_outputs.py:4` → `test_outputs.py:5` (capture line 5 is blank; no other quote cites `:5`, so this is single-cause). Caught by the gate's verbatim clause via V2:
```
    gate: P4 DEFECT checked=32 bad=1 first=test_outputs.py:5: quote not verbatim there
V2 DEFECT gate_exit=1
```
`checks=7 defects=1`. Restored hash `6e3f8c77…4812a`, tree clean.

**M2 — S112 anchor digest 63 hex.** `corpus/SOURCES.md` S112 anchor cell: `sha256 1dc44c…f53d05` → `…f53d0` (last hex char dropped). Caught by V3:
```
V3 DEFECT rows=3 bad=['S112:anchor_digest']
```
`checks=7 defects=1`. Note: V6 census stayed green (`census_exit=0`) — the census does not validate anchor digests; V3 is the sole catcher, exactly the round-36 spot-check class the clause was added for. Restored hash `c1c9b533…12351`, tree clean.

**M3 — requirement-map row relabelled.** Entry `## Requirement map` row 1: `unenforced` → `enforced` (its only cited case `static-file-no-git` is observed `pass`). Caught by V7:
```
V7 DEFECT rows=4 bad=['instruction.md:1: enforced without a failing case']
```
`checks=7 defects=1`. Restored hash `6e3f8c77…4812a`, tree clean.

**M4 — map row citing an unknown case.** Entry map row 4: cited case `capitalised` → `capitalisedx` (no such receipt CASE id). Caught by V7:
```
V7 DEFECT rows=4 bad=['instruction.md:9: cites no case or an unknown case']
```
`checks=7 defects=1`. Restored hash `6e3f8c77…4812a`, tree clean.

**M5 — receipt CASE line removed.** Receipt `CASE wget-404 …` line deleted (its `grader-stdout:` continuation left in place; `wget-404` is not cited in the requirement map, so V7 is untouched). Caught by V4 and the gate:
```
    gate: P10 DEFECT fresh probe output is not byte-equal to the receipt
V2 DEFECT gate_exit=1
V4 DEFECT cases=21 mismatches_named=0/0 bad=['case ids differ from the frozen table', 'summary disagrees with the CASE lines']
```
`checks=7 defects=2`. Restored hash `83550712…ec29f8`, tree clean.

**M6 — receipt one byte.** Receipt summary line: `cases=22` → `cases=23` (single byte `2`→`3`). Caught by V4 and the gate:
```
    gate: P10 DEFECT fresh probe output is not byte-equal to the receipt
V2 DEFECT gate_exit=1
V4 DEFECT cases=22 mismatches_named=0/0 bad=['summary disagrees with the CASE lines']
```
`checks=7 defects=2`. Restored hash `83550712…ec29f8`, tree clean.

**M7 — a `match=NO` not named.** One defect, three coordinated edits (the naming clause is only reachable in a self-consistent receipt): receipt `CASE wget-404 … match=yes` → `match=NO`; receipt summary `mismatches=0` → `mismatches=1` (so the summary agrees with the CASE lines); entry drops the `wget-404` name from the wget-branch table row (its only occurrence in the entry). Caught by V4's naming clause, plus the gate:
```
    gate: P10 DEFECT fresh probe output is not byte-equal to the receipt
V2 DEFECT gate_exit=1
V4 DEFECT cases=22 mismatches_named=0/1 bad=["mismatch cases not named in the entry: ['wget-404']"]
```
`checks=7 defects=2`. Restored hashes `83550712…ec29f8` / `6e3f8c77…4812a`, tree clean.

**M8 — SHA256SUMS line removed.** Captures manifest: the `ebb40d72…74751b  task.toml` line deleted. Caught by V1 and the gate:
```
V1 DEFECT listed=5 bad=['task.toml'] extra=0
    gate: P5 DEFECT manifest_entries=5 bad=2 first=quote capture task.toml is not pinned in the manifest
V2 DEFECT gate_exit=1
```
`checks=7 defects=2`. Restored hash `e70bb662…a3531f`, tree clean.

**M9 — README bullet removed.** `corpus/README.md` coverage bullet deleted (the round-37 bullet naming `knowledge/tb2-git-webserver-grader.md` and `evidence/round37/git-webserver-probe.txt`). Caught by the gate's README clause via V2:
```
    gate: P8 DEFECT index_rows=44 knowledge_files=44 bad=1 first=no coverage bullet naming the entry and its receipt
V2 DEFECT gate_exit=1
```
`checks=7 defects=1`. Restored hash `3e547056…a3940ef`, tree clean.

**M10 — extra knowledge file.** `corpus/knowledge/zz-f37-mut-extra.md` created (302 bytes) and staged index-only (`git add` inside my clone, per the fixture rule) so P9 stays clean and the knowledge-files clause alone fires. Caught by the gate via V2:
```
    gate: P8 DEFECT index_rows=44 knowledge_files=45 bad=1 first=knowledge files=45 index rows=44
V2 DEFECT gate_exit=1
```
`checks=7 defects=1`. Cleanup: `git rm --cached -f` + file removed; `DIRTY_AFTER_CLEANUP=0`.

## Supplementary probes

**S1 — receipt-only `match=NO` flip** (no summary or entry edit; the minimal corruption a hand edit would produce): `CASE wget-404 … match=yes` → `match=NO`. Red, via the summary-agreement clause — the naming clause stays silent because the id is still named in the entry:
```
    gate: P10 DEFECT fresh probe output is not byte-equal to the receipt
V2 DEFECT gate_exit=1
V4 DEFECT cases=22 mismatches_named=1/1 bad=['summary disagrees with the CASE lines']
```
`checks=7 defects=2`, exit 1. Restored hash `83550712…ec29f8`, tree clean.

**S2 — one byte in a receipt header digest** (line 2, `# capture instruction.md sha256=62151b…cf1d97` → `…cf1d98`): V4 does not parse `#` header lines, so V1/V3–V7 stayed green; the gate's re-run byte-compare is the sole catcher:
```
    gate: P10 DEFECT fresh probe output is not byte-equal to the receipt
V2 DEFECT gate_exit=1
```
`checks=7 defects=1`, exit 1. Restored hash `83550712…ec29f8`, tree clean.

## Coverage observations (findings about the counter, not the package)

1. **V4 never cross-checks `match=` against `predicted=`/`observed=`.** M7's state had `predicted=fail observed=fail` with `match=NO` on the same CASE line and V4 accepted the line itself (only the naming clause and P10 fired). Bounded in practice: the frozen instrument writes `match=` only from its own predicted-vs-observed comparison, and P10's byte-compare rejects any hand-edited receipt — so the gap is reachable only by also defeating P10.
2. **The V4 naming clause is co-guarded by the summary-agreement clause.** All 22 CASE ids appear in the entry, so a receipt-only `match=NO` flip is caught by summary disagreement (S1, `mismatches_named=1/1`); the naming clause fires only when the entry also drops the name (M7, `mismatches_named=0/1`). Both routes red — no gap, but the clause the docstring advertises is not the one that fires on the minimal edit.
3. **V6 census does not validate anchor digests.** With S112's anchor at 63 hex the census stayed green (`census_exit=0`); V3 is the sole catcher (M2). This matches the counter docstring's stated reason for V3 (round-36 spot-check routed item 1) — the clause is load-bearing, not redundant.
4. **V4 is blind to the receipt's `#` header lines; P10 backstops.** A header byte is caught only by the re-run byte-compare (S2). Acceptable: P10 re-runs the frozen probe, so every receipt byte is covered by V2 even where V4 does not look.

## Verdict accounting

10 assigned mutants on the landed package; 10/10 turned the counter red (`PREDICATE C2 fail`, exit 1) with the clause predicted for each defect class firing; 2 supplementary probes also killed. No survivor, no inconclusive run (baseline green on the same clone first). Every mutant's exact bytes restored and hash-verified; both clones ended `git status --porcelain` empty; scratch deleted after the receipts were copied out.

Raw receipts: `F37MutC2Counter/baseline.txt`, `F37MutC2Counter/mutant-M1.txt` … `mutant-M10.txt`, `mutant-S1.txt`, `mutant-S2.txt`.

VERDICT: c2-landed-mutants-10/10
