# R38PkgEntry — C2 package draft (`tb2-build-pmars` grader), kengaku round 38 wave 1

Seat: scribe, leaf. No subagents, no background jobs, no lane write, no lane git/jj mutation.
Scratch (deleted at end): `/fast/scratch/hyaku/kengaku-r38/R38PkgEntry/`.
Report dir: `.ufo/waves/round-38/build/R38PkgEntry/`.

## 1. Behavior — what exists now

Three byte-ready drafts for the L1, plus the counter receipt proving them:

| Draft | Target in the lane | Size |
|---|---|---|
| `entry.md` | `corpus/knowledge/tb2-build-pmars-grader.md` | 310 lines, sha256 `af0af320…c99c410` |
| `rows.md` | two rows appended after `S114` in `corpus/SOURCES.md` (11 cells each) | 2 lines, sha256 `d82b107a…f55a71a` |
| `readme.md` | one index row + one `## Coverage map` bullet in `corpus/README.md` | 14 lines, sha256 `180836c8…79d6111` |
| `c2-verify-final.txt` | receipt of the final counter run (copied out of scratch) | 753 B, sha256 `b2dff081…92167cf` |

`entry.md` carries `source: S115 …` / `source: S116 …` lines at the exact pinned raw URLs,
`verified-at: 2026-10-26`, `recheck: 180d …`, the sections Summary / Source labels / What the grader checks
(static reading) / Located quotes (28 rows, 27 distinct `capture:line` locations, all 3–25 words) / Requirement
map (7 rows, one per frozen TAG, labels derived) / The executed probe / Findings tied to receipt case ids /
What the probe does not show / Prior art / Negative space with an explicit **Falsifier**.
`rows.md` are the two registry rows (tier A, status `mined`, opened 2026-10-26, recheck 180d, anchor cell
`sha256 <pin>` + a ≤25-word located quote, teaches ≥8 words, used-by the entry). `readme.md` holds the index row
and the coverage bullet naming the entry and `evidence/round38/build-pmars-probe.txt`.

## 2. Gates — the C2 counter, green, twice on the final drafts

Fixture: `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane` →
`git -C $S/lane rev-parse --show-toplevel` = `/fast/scratch/hyaku/kengaku-r38/R38PkgEntry/lane`,
HEAD `2c5f4e0ba8e2865af4b71e337f3cde86eaf0702e` (the wave-1 tip at read time, not the claims' freeze baseline
`fc1174f5`; ids `S115`/`S116` were free there — census E03 would have fired otherwise, and it exits 0).
Assembly: copy `entry.md` to `corpus/knowledge/tb2-build-pmars-grader.md`; insert the two `rows.md` lines after the
`| S114 |` line; insert the index row after the `knowledge/tb2-git-webserver-grader.md` row and the coverage bullet
after the "Terminal-Bench 2.0 task grader (third task …)" bullet; `git -C "$S/lane" add -A`.
Result: `corpus/README.md |2 +`, `corpus/SOURCES.md |2 +`, `corpus/knowledge/tb2-build-pmars-grader.md |310 +++`.

```
$ python3 plans/round38_c2_verify.py --lane "$S/lane" --work "$S/w"
V1 ok listed=5 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=28 distinct_quotes=28 distinct_lines=27 out_of_word_range=0
    gate: P4 ok checked=28 bad=0 first=0
    gate: P5 ok manifest_entries=5 bad=0 first=0
    gate: P6 ok rows=2 bad=0 first=0
    gate: P7 ok source_lines=2 bad=0 first=0
    gate: P8 ok index_rows=45 knowledge_files=45 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=5537
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=2 bad=0
V4 ok cases=22 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=7 tags=7 bad=0
checks=7 defects=0
PREDICATE C2 pass
```
exit 0. Reproduced twice on trees holding these exact draft bytes (the first green run and the final re-assembly;
`entry.md` digest `af0af320…c99c410` both times), with identical check lines.
Standalone probe check: `python3 $S/lane/plans/build_pmars_probe.py --lane $S/lane` → exit 0,
`cmp` byte-equal to `corpus/evidence/round38/build-pmars-probe.txt`, `5537` bytes, `real 0m0.981s`.
Census by hand: `scripts/sources-census.sh validate --file $S/lane/corpus/SOURCES.md` → `file ok …/SOURCES.md`,
exit 0 (15 pre-existing `W04` cross-scope duplicate-URL warnings only, none from S115/S116).

### 2.1 Requirement-map labels are derived, not chosen (V7's own rule, recomputed by hand)

Recompute used the counter's `receipt_cases` regex over `corpus/evidence/round38/build-pmars-probe.txt` and the
frozen `TAG` lines; output (22 parsed cases):

```
from-source instruction.md:1 partly n_viol=22 pass=7 fail=15
no-x11 instruction.md:3 partly n_viol=3 pass=1 fail=2
debian-source instruction.md:3 partly n_viol=22 pass=7 fail=15
extract-to-app instruction.md:3 partly n_viol=22 pass=7 fail=15
install-path instruction.md:3 partly n_viol=4 pass=1 fail=3
results-format instruction.md:7 partly n_viol=5 pass=1 fail=4
debugger-works instruction.md:9 partly n_viol=22 pass=7 fail=15
```

All seven labels are `partly` — no instruction line is fully enforced — which is what the entry's map row set
states, and V7 agrees (`rows=7 tags=7 bad=0`). Every cited case per row is a violating case in the direction the
label needs (`empty-tree` fail vs `canned-shape` pass, etc.).

### 2.2 Falsifiers I ran against my own drafts (each on the scratch clone, then restored)

| Mutant | Change | Counter result | Verdict |
|---|---|---|---|
| A — wrong label | `from-source` row label `partly` → `enforced` | `V7 DEFECT rows=7 tags=7 bad=['from-source: labelled enforced, receipt derives partly']`, `checks=7 defects=1` | killed |
| B — quote word changed | `stripped string` → `stripped text` in `test_outputs.py:10` quote | `P4 DEFECT checked=28 bad=1 first=test_outputs.py:10: quote not verbatim there`, `defects=1` | killed |
| B′ — quote truncated | dropped `.strip()` from the `:12` quote (still a substring of the line) | `P3 ok … P4 ok`, `checks=7 defects=0` | **survives** — instrument limit, see §6 |
| C — foreign anchor digest | S115's anchor `sha256` replaced with S116's real pin | `P6 ok rows=2 bad=0`, `V3 DEFECT rows=2 bad=['S115:anchor_digest']`, `defects=1` | killed (D3 binding live) |
| D — duplicated rows | re-assembly run that left S115/S116 twice | `P6 DEFECT … first=S115: rows=2`, `P8 DEFECT index rows …=2`, `V3 DEFECT ['S115:row','S116:row']`, `V6 DEFECT census_exit=1`, `checks=7 defects=3` | killed |

Mutant D was an accident of my own assembly (a `git checkout --` restored from the index, not HEAD); it is kept
here because it is the counter answering a real integration error. Fixed by `git checkout HEAD -- <files>` and
re-assembling from the drafts; the final tree is exactly `2 + 2 + 310` inserted lines.

## 3. Touched surfaces

Written (report dir only):
`.ufo/waves/round-38/build/R38PkgEntry/{entry.md,rows.md,readme.md,c2-verify-final.txt}` and this report.
Nothing else in the lane, the fleet root, sibling lanes or `/home/vgpnk/Projects/shokuknow` was written.
Scratch clone writes stayed inside `$S/lane`; `git add -A` there only (index-only, no commit); scratch removed.
No tool installed, upgraded or removed (pacman transactions paused host-wide; nothing was needed).

## 4. Findings the entry records (each tied to receipt case ids)

1. `canned-shape` `PPPP` — a canned 14-line C program + empty `debian/` dir + zero-byte `src/dummy.c` passes all
   four tests while violating `from-source`, `debian-source`, `extract-to-app`, `debugger-works`.
2. `canned-x11-dlopen` `PPPP` — `ldd`'s `DT_NEEDED` scan cannot see a `dlopen()`ed `libX11`; `canned-x11-linked`
   `PFPP` is the enforcing direction, and `canned-script`/`canned-static` `PFPP` show the check *fails closed* on
   artefacts `ldd` cannot read.
3. `results-trailing-text` `PPPP` — `re.match(r"Results: \d+ \d+ \d+", …)` anchors only the start;
   `results-two-ints`, `results-not-last`, `results-negative` are `FPPP` negative controls.
4. `canned-exit-nonzero` `PPPP` — exit 3 is invisible because `run_shell_command` returns `e.output` when non-empty
   (`test_outputs.py:13-15`); no line of the capture reads a return code (`grep -n "returncode" test_outputs.py` →
   no match).
5. `path-split` `PPPP` — behaviour tests run the bare `pmars` on `PATH` (`:27,:44`), `ldd` reads
   `/usr/local/bin/pmars` (`:53`); `/usr/local/sbin` precedes `/usr/local/bin`, so two objects are graded.
6. `debian-is-file` `PPPP` and `c-is-dir` `PPPP` — `exists()` and `glob("*.c")` accept a zero-byte `debian` file and
   a `src/sim.c` **directory**; negative controls `no-debian-dir` `PPFP`, `no-src-dir`/`src-no-c` `PPPF`.
7. `pmars-dir-elsewhere` `PPFF` — both shape tests use a one-level `/app/pmars-*` glob.
8. `empty-tree` `FFFF`, `nonexec-binary`/`silent-binary` `FPPP` — the strict side is real, so the vacuum is specific
   to provenance and linkage, not to "any file passes".

Prior art section states the class is published (round-37 scout) and that TB2 issue #59 concerns the oracle pins,
not the grader (`plans/round-38-claims.md:77`), with no capture and no quote; the claim is only "first probed
instance for TB2 `build-pmars`". Limits named: host `bash` vs Debian `dash`, host `ldd`, host `gcc`-compiled canned
artefacts, `test.sh` and the oracle never run, no image/harness/model, the 22 cases are the whole surface.

## 5. Out of scope for this seat (L1 / wave-2 items seen, not touched)

- `PROVINCE.md` paragraph and the `corpus/README.md` §Frontier TB2 sub-bullet narrowing: the ticket names three
  drafts only, so `readme.md` carries just the index row and coverage bullet; the §Frontier sub-bullet edit is
  drafted nowhere and must be written by the integrator (claims §C2 lists it under Surface).
- Round-37 closure **D2** asks for an appended erratum on `knowledge/tb2-git-webserver-grader.md` plus a QUALITY
  criterion; not written here (append-only lane text, L1-owned).
- TB2 issue #59 row-or-refusal and its capture (wave-2 prior-art seat).
- `LOG.md`, `SCORECARD.md`, `SHONEN.md`, `corpus/QUALITY.md` untouched.

## 6. Instrument observations (for the L1 and wave-2, not defects in my drafts)

1. **`P4` is a substring test, so a truncated quote survives.** Mutant B′ shows a quote that stops short of the
   line still passes `P4 ok`. That is consistent with the counter's contract ("quote not verbatim there"), and my
   draft's quotes are byte-complete lines up to their chosen end; but the counter cannot distinguish a deliberate
   cut from a missing clause. No action taken; the frozen gate is not mine to change.
2. **`P6` does not check the anchor digest; `V3` does.** Mutant C left `P6 ok rows=2 bad=0` and only `V3` fired —
   so the D3 binding is carried by `V3` alone, and a reader of the gate output must not read `P6 ok` as
   "anchors correct".
3. **Duplication is caught across four clauses** (mutant D), so a double insertion during integration fails loudly
   rather than silently doubling rows.

## 7. Verification I did not run

The lane's own C1 counter, the round-37 counters and the full battery are other seats' work this wave; I ran only
`plans/round38_c2_verify.py`, `plans/build_pmars_probe.py` (as `P10` and standalone), `scripts/sources-census.sh`,
and `git`/`sha256sum`/`cmp` inside my scratch clone. I did not run the package gate at the lane tip, did not
re-fetch the two pinned URLs, and did not open TB2 issue #59.

VERDICT: c2-package-draft-checks-7-defects-0
