# F41C1Attribution — does each credited C1 kill execute the mutated line?

Seat: executor, round 41 wave 2 (falsify), item `F41C1Attribution`. Target: the 23 frozen mutants of
`plans/round41_c1_verify.py` (`8835a94b…`) over `plans/tip_receipts.py` (T01–T13) and the CLI half of
`plans/sources_adopt.py` (S01–S09, S11), against the 23 killer fixtures recorded in
`.ufo/waves/round-41/integrate/measure-final.txt` (`killed by=`). Question asked: on the fixture that credits a
mutant, does the **mutated line execute in the mutant run**? Any `no` would be a non-attributable credit.
Nothing frozen was edited; no lane file, Git index or jj state was written; no tool installed or upgraded.

## Pins and provenance of what was measured

Clone `/fast/scratch/hyaku/kengaku-r41/F41C1Attribution/lane` (`rev-parse --show-toplevel` = that path, checked
before any write). One wave-2 commit sits on top of the dispatch tip; every frozen artifact still hashes to
`claims/frozen-digests.txt` (`provenance.txt`):

```
git -C $S/lane rev-parse HEAD                 -> d7c77895752a2a5f317fa22f2362416ada50a04b
sha256 plans/tip_receipts.py                  -> e4f49714299ca1f2a93303c59ac07e691cc45d6126ccf24e5eecab93733f88f3
sha256 plans/sources_adopt.py                 -> 38492bf175e0c619596c69911954e3b3c247166bdc240f8c1d44a02b7f4103e0
sha256 plans/round41_c1_verify.py             -> 8835a94b0ad62dc1f58c861e2025b7c4bc8c0b936c202c64e01bc8b43f53eaa8
git -C $S/lane diff --stat 74513c0..HEAD -- plans/battery41 plans/tip_receipts.py plans/sources_adopt.py \
    plans/round41_c1_verify.py                -> (empty)
```

The battery the killers come from is byte-identical to the landing commit `74513c0`, so the fixtures rebuilt
here are the fixtures measured at landing (`provenance.txt` lists all seven module digests; `s_exit.py`
`5f57cec9…` equals the digest `F41RevBatSrcExit` reviewed).

## Method

1. Parse `killed by=<fid>` from the landing measurement, restricted to the 23 frozen ids (the file also holds
   round-40 `A*/L*/O*` mutants; the parser refuses a duplicate line for any of the 23).
2. Rebuild all 48 fixtures with the frozen counter's own `build_battery`/`Ctx` (each module built in
   `bwrap --ro-bind / /` with the lane tmpfs-hidden).
3. For each mutant: `mutant = src.replace(old, new, 1)` (the counter's own byte-level edit, `src.count(old) == 1`
   asserted), then `traced = mutant` with `sys.stderr.write("HIT <id>\n")` inserted **immediately before the
   mutated statement**, at the statement's indentation. Same file, nothing else touched.
4. Run `traced` on the killer fixture's built tree with the fixture's argv through the counter's own
   `Runner` — the identical nested sandbox (`--ro-bind / /`, variant bound read-only at the fixed slot, fixed
   system `PATH`, `--unshare-pid --unshare-net`, only the per-run work and tmp dirs writable). Read stderr;
   `HIT <id>` present = the mutated line executed in the mutant run.

Two harness notes, both disclosed:

* The frozen counter discards stderr, so a **copy** in scratch keeps it: a global `K41_STDERR` and one capture
  line. `diff <(sed '125,127d;431d' counter.py) lane/plans/round41_c1_verify.py` → `IDENTICAL`, so the copy
  differs from the frozen counter by exactly those two added lines and nothing else (`provenance.txt`).
* A mutated `elif` (only T08) cannot take a statement before it; its **test** was wrapped instead:
  `elif X:` → `elif (sys.stderr.write("HIT T08\n") and 0) or X:`. The write returns >0, `and 0` makes the
  prefix False, `or X` keeps the original truth value — the marker fires exactly when the elif is evaluated.
  For T10/T12 the mutated statement is a module-level regex assignment (executes on import, trivially), so the
  consumer of the changed constant was traced as well: `stem()` for `STEM_RE`, `candidates()` for
  `CANDIDATE_RE`.

Soundness guard: every traced run's `(exit code, printed class set)` equals the plain mutant's
(`TRACE_SEMANTICS_DRIFT -`), so the marker does not change behaviour; stdout classes are the counter's own
`classes()`.

## Result — 23 of 23 credited kills execute the mutated line

Command (inside the mandated envelope; the counter adds its own read-only sandboxes inside it):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
  --proc /proc --unshare-pid --die-with-parent python3 $S/driver.py $S/counter.py $S/lane $S/work/full \
  $S/lane/.ufo/waves/round-41/integrate/measure-final.txt
```

`attribution-run.txt` (head + tail): `BUILT fixtures=48 sidechannel=0`, 23 `REC` records, then
`ATTRIBUTABLE 23/23`, `TRACE_SEMANTICS_DRIFT -`, `KILL_NOT_REPRODUCED -`.

| mutant | killer (as landed) | mutated statement (lane file:line) | HIT in mutant stderr | HIT in reference stderr | ref→mutant rc | kill reproduces | attributable |
|---|---|---|---|---|---|---|---|
| T01 | r_setup-t01-lane-absent | tip_receipts.py:107 `raise SystemExit(2)` | 1 | 1 | 2→0 | yes | yes |
| T02 | r_setup-t02-no-evidence | tip_receipts.py:241 `if not (lane / EVIDENCE).is_dir():` | 1 | 1 | 2→0 | yes | yes |
| T03 | r_run-t03-rc-nonzero-mixed | tip_receipts.py:314 `if run["exit"] != 0:` | 2 | 2 | 1→0 | yes | yes |
| T04 | r_run-t04-temp-paths-masked | tip_receipts.py:319 `if mask(fresh) == mask(blob):` | 1 | 1 | 0→1 | yes | yes |
| T05 | r_setup-t05-tamper-absent | tip_receipts.py:336 `if unknown:` | 1 | 1 | 2→1 | yes | yes |
| T06 | r_ctl-t06-empty-equal-receipt | tip_receipts.py:383 `return 0 if d == 0 and control_ok else 1` | 1 | 1 | 1→0 | yes | yes |
| T07 | r_setup-t07-lane-subdir | tip_receipts.py:123 `if not top or pathlib.Path(top).resolve() != …` | 1 | 1 | 2→0 | yes | yes |
| T08 | r_ctl-t08-derived-uv-absent | tip_receipts.py:291 `elif shutil.which(argv[0]) is None:` | 2 | 2 | 0→1 | yes | yes |
| T09 | r_map-t09-shared-stem-separators | tip_receipts.py:100 `if len(hit) == 1:` | 1 | 1 | 0→0 | yes | yes |
| T10 | r_map-t10-derived-mapping | tip_receipts.py:81 `STEM_RE = re.compile(...)` | 1 (+3 consumer) | 1 | 0→0 | yes | yes |
| T11 | r_map-t11-table-overrides-derived | tip_receipts.py:97 `if rel in RECEIPTS:` | 2 | 2 | 0→0 | yes | yes |
| T12 | r_map-t12-log-population | tip_receipts.py:52 `CANDIDATE_RE = re.compile(...)` | 1 (+2 consumer) | 1 | 0→0 | yes | yes |
| T13 | r_ctl-t08-derived-uv-absent | tip_receipts.py:355 `control_ok = control_ok and not same` | 1 | 1 | 0→1 | yes | yes |
| S01 | s_modes-s01-quote-plus-package | sources_adopt.py:1022 `if args.registry or args.package:` | 1 | 1 | 2→0 | yes | yes |
| S02 | s_usage-02-registry-without-package | sources_adopt.py:1041 `if not args.registry or not args.package:` | 1 | 1 | 2→1 | yes | yes |
| S03 | s_usage-03-dotted-access-date | sources_adopt.py:1052 `if not ISO_DATE_RE.match(args.access_date):` | 1 | 1 | 2→5 | yes | yes |
| S04 | s_modes-s04-url-map-with-adopt | sources_adopt.py:1039 `if args.url_map:` | 1 | 1 | 2→0 | yes | yes |
| S05 | s_usage-05-two-ids-without-entries | sources_adopt.py:1050 `if not args.entries:` | 1 | 1 | 2→0 | yes | yes |
| S06 | s_usage-06-recheck-cadence-word | sources_adopt.py:1054 `if not (` | 1 | 1 | 2→0 | yes | yes |
| S07 | s_exit-collision-admit | sources_adopt.py:1046 `if code != EXIT_OK or not want:` | 1 | 1 | 3→0 | yes | yes |
| S08 | s_modes-s08-quote-file-without-artifact | sources_adopt.py:1018 `if not (args.quote_file and args.artifact):` | 1 | 1 | 2→1 | yes | yes |
| S09 | s_modes-s09-url-map-nested-shape | sources_adopt.py:1027 `if problem:` | 1 | 1 | 2→9 | yes | yes |
| S11 | s_exit-queued-admit | sources_adopt.py:1068 `if missing:` | 1 | 1 | 5→0 | yes | yes |

`attribution-table.txt` is the same table in machine form; `receipts/<id>/` holds, per mutant, the raw
`stderr-mutant.txt`, `stderr-ref.txt`, and the traced source window around the insertion.

### Sample evidence (raw, from `receipts/`)

T03 (guard evaluated once per mapped receipt, twice on this fixture):

```
$ cat receipts/T03/traced-source.txt
 314:             sys.stderr.write("HIT T03\n")
 315:             if False:
$ cat receipts/T03/stderr-mutant.txt
HIT T03
HIT T03
```

T08 (elif test wrapped; also fires in the reference run, so the site is on both phases' path):

```
 291:             elif (sys.stderr.write("HIT T08\n") and 0) or False:
stderr-mutant.txt: HIT T08 ×2      stderr-ref.txt: HIT REF-T08 ×2
```

S03 — the reference's own stderr proves the reference entered the branch body at that site, while the mutant
skipped it (mutant rc 5, reference rc 2):

```
 1052:     sys.stderr.write("HIT S03\n")
 1053:     if False:
 1054:         parser.error("--access-date must be an ISO date (YYYY-MM-DD)")
stderr-ref.txt: HIT REF-S03 / sources.py: error: --access-date must be an ISO date (YYYY-MM-DD)
```

T10 consumer (the changed constant is consulted three times on the killer fixture):

```
$ grep -c HITUSE-T10 receipts/T10/stderr-mutant.txt   -> 3   (site marker HIT T10 ×1)
$ grep -c HITUSE-T12 receipts/T12/stderr-mutant.txt   -> 2   (site marker HIT T12 ×1)
```

## Controls — the test can say `no`, and it reproduces the wave-1 dead-site finding

Same traced variants, run on a fixture where the site is not on the path (`controls.txt`):

| control | traced variant | deliberate fixture | HIT | attributable |
|---|---|---|---|---|
| A | T04 (`temp-paths` branch) | r_map-t10-derived-mapping (`kind=byte`) | 0 in both phases | `0/1` |
| B | T08 (elif in the receipt loop) | r_setup-t01-lane-absent (dies in `lane_root`) | 0 in both phases | `0/1` |

Control A independently reproduces `R41CritC1Counter.md` §3: for a receipt whose kind is `byte` the
`if res["kind"] == "temp-paths":` block never runs, so a T04 credit from such a fixture would be a dead-site
credit with a green `wrong=0`. The landed killer `r_run-t04-temp-paths-masked` does enter the block (HIT ×1),
so the credit that exists is not of that shape. Control A/B together show the harness reports `no` when the
line is not reached — the 23 `yes` values are not a constant.

## Independent reproduction of the landed kills

`KILLER-REF-MATCH 23/23`: my reference run on each of the 23 killer fixtures reproduces the landing
measurement's `observed_rc` **and** its exact class set (compared line by line against
`measure-final.txt`). `kill_reproduces = yes` for all 23 also recomputes `exhibits()` on the plain mutant,
i.e. every credited direction (`error`, `rc-silence`, `rc-mirror`, `silence`, `2>0`, `2>1`, `2>5`, `2>9`,
`3>0`, `5>0`) reappears here. So the clone, the rebuilt fixtures and the run path are the landed instrument
state, not a different one.

## Adjacent observations (scoped, not a verdict on other seats' questions)

* **Two credits share one killer**: T08 and T13 are both killed by `r_ctl-t08-derived-uv-absent`; both sites
  execute there (`HIT T08 ×2`, `HIT T13 ×1`) and their divergences differ (T08: class `skip:…dependency-missing`
  → `differ:…`; T13: exit-only, 0→1 with identical class set). Distinct mutated lines, so two credits from one
  fixture are not double-counting one execution.
* **No variant-oracle code in the battery**: `grep -n 'slots\|variants\|ref-receipts\|ref-sources\|read_bytes\|
  getppid\|/proc' plans/battery41/*.py` matches only two literal receipt/prose strings
  (`r_run.py:95` receipt text `slots=5`, `s_exit.py:28` a quoted sentence). The modules' probe stubs are fixed
  `sys.stdout.write(...)` + `raise SystemExit(rc)` (`battery-vector-scan.txt`; e.g. `r_map.py:29-37`). This is a
  text scan of the 7 modules only — the A1′ sandbox-level oracle, relative argv escape and socket/IPC vectors
  remain the battery reviewers' question, not settled here.
* **Direction-consistent classes**: on the four `silence` credits (T09–T12) the class the fixture declares
  disappears in the mutant run and the exit code stays 0/0 — the credited difference is the class set, and the
  site that governs it is the one traced.

## Limits of this attribution run

1. **`executes` means reached and evaluated**, not "branch body taken" (that is what the marker proves). For
   the `if False:`-shaped mutants (T02/T03/T05/T07/T08 and 12 sources mutants) the changed test is reached in
   both phases; that the *reference* took the body at that site is inferred from (a) the single-site text
   replacement, (b) the measured divergence in the declared direction, and (c) the reference's own stderr where
   it shows the body's effect (S03 above). The inference is not a second trace.
2. **Attribution ≠ intent.** A `yes` says the credited line ran and caused the difference; whether the fixture
   tests the behaviour the docstring advertises is out of scope here (the battery reviewers own it).
3. The runs use a **scratch copy** of the frozen counter that only adds stderr capture; the frozen counter was
   not re-run by this seat (`F41C1Rerun` owns the rerun). My numbers reproduce its per-fixture reference
   results exactly, but this seat does not itself certify `MUTANTS killed=23/23`.
4. T08's marker sits in the elif *test*, not on a separate line — semantics preserved, but it is an
   instrumented expression, not a plain inserted statement.
5. Scratch clone and receipts live under `/fast/scratch/hyaku/kengaku-r41/F41C1Attribution/`; receipts were
   copied here before cleanup. No write happened outside this report dir and that scratch dir.

## Receipts

* `attribution-run.txt` — full driver log (48 fixtures built, 23 `REC` JSON records, table, summary lines).
* `attribution-table.txt` — the table above, machine-readable.
* `controls.txt` — negative controls A and B with `ATTRIBUTABLE 0/1` each.
* `provenance.txt` — tip, tool/counter digests, patch diff, battery41 digests, empty `74513c0..HEAD` diff.
* `battery-vector-scan.txt` — the battery text scan.
* `receipts/<id>/{stderr-mutant,stderr-ref,traced-source,ref-traced-source}.txt` — per-mutant raw evidence.

VERDICT: attributable-23/23
