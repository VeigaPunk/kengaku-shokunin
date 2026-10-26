# F41RevBatMap — honesty review of `plans/battery41/r_map.py` (C1 mutants T09–T12)

Seat: F41RevBatMap, kengaku round 41 wave 2 (falsify), 2026-10-26.
Target: `plans/battery41/r_map.py` (seat R41BatRcvMap), 159 lines, claims kills of T09/T10/T11/T12 of
`plans/round41_c1_verify.py`. Method: full line read, attribution run, traced-execution run, vector audit.

## 0. Identity and setup

- Reviewed module digest `705a4b7cbd3e08d620a4295acb147fa4d1741df5223ca95a7aaf456a8606c9c0`, identical at
  working tree, `3d0058f:plans/battery41/r_map.py`, and `d7c7789:plans/battery41/r_map.py`
  (`sha256sum` + `git show | sha256sum`, all three equal; scratch copy diff-identical). No `r_map` row in
  `frozen-digests.txt` (grep empty) — the module is not itself frozen, consistent with non-author review being
  the admission path.
- Scratch `S=/fast/scratch/hyaku/kengaku-r41/F41RevBatMap`; `git clone -q --shared` of the lane,
  `rev-parse --show-toplevel` = `$S/lane`, detached to landing tip `3d0058fbde484c9d6c23fd997d9ee09a0663bcdb`
  (clone default HEAD was the wave-2 spec commit `d7c7789`, one docs commit past the landing tip; I checked out
  the landing tip in my own clone). `git status --porcelain | wc -l` = 0; tool digests match the counter's PINS
  (`tip_receipts.py` `e4f49714…`, `sources_adopt.py` `38492bf1…`).
- Both executable steps ran inside the orchestrator envelope
  `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent …`;
  the counter adds its own nested read-only sandboxes. No writes outside my scratch and report dirs.

## 1. Attribution: each mutant dies by THIS module

Command (envelope elided as above):

```
python3 <lane>/plans/round41_c1_verify.py --lane "$S/lane" --battery-dir "$S/batonly" \
  --only T09,T10,T11,T12 --work "$S/w"        # $S/batonly holds ONLY r_map.py
```

Receipt: `falsify/F41RevBatMap/attrib.txt` (stderr empty, `attrib.err` 0 bytes). Result:

- `PINS total=2 mismatched=0` and `PINS-AFTER mismatched=0`.
- All 10 FIXTURE lines `ok`: `wrong=0`, every declared defect set equals the observed reference class set,
  `observed_rc=0` everywhere (`expect=accept` on all ten).
- `MUTANT T09 … killed by=r_map-t09-shared-stem-separators`
- `MUTANT T10 … killed by=r_map-t10-derived-mapping`
- `MUTANT T11 … killed by=r_map-t11-table-overrides-derived`
- `MUTANT T12 … killed by=r_map-t12-log-population`
- `BATTERY fixtures=10 wrong=0 tampered=0 sidechannel=0`; `MUTANTS total=4 killed=4 survived=0 invalid=0
  null_detected=0`; `MUTANTS-BY-TOOL receipts=4/4`; `PREDICATE C1 n/a (non-default battery or mutant
  subset)`; exit `rc=0`.

So with r_map.py as the only battery module, all four mutants die and the kills are attributed to r_map
fixtures. Caveat: the landed measurement ran the whole battery (module build order is
`r_ctl, r_map, r_run, …`), so the full-run `killed by=` for these mutants could name r_ctl fixtures; this seat's
assignment was the restricted run, which isolates r_map's contribution.

## 2. Mutated line executes on the killing fixture

Method (`falsify/F41RevBatMap/drv.py`, output `exec.json`): rebuild all 10 fixtures in scratch by calling the
module's own `FIXTURES[i]["build"]` with the counter's own `Ctx` (same pinned git identity/dates), then run two
instrumented copies of `tip_receipts.py` per mutant inside the counter's own `ro_sandbox` — REF-traced (marker
beside the original line) and MUT-traced (the counter's exact `old→new` replacement, marker beside the mutated
line) — over all 10 fixtures (4 mutants × 2 variants × 10 fixtures = 80 runs), re-evaluating the counter's
`exhibits()` on the results. Trace lines (`TRACE-T09 mut-site` etc.) prove the site ran; stdout classes must
match the attribution run's classes (they do, all 40 ref rows).

| mutant | counter `killed by` | my kill sites (exhibits=True) | trace at credited site | ref classes → mut classes at that site |
|---|---|---|---|---|
| T09 `if len(hit) == 1:` → `>= 1` | t09-shared-stem-separators | separators, case-fold | `TRACE-T09 mut-site` present | `skip:…foo-probe.txt:no-committed-re-run-command` → `map:…foo-probe.txt:derived` |
| T10 `[^a-z0-9]+` → `[^a-z0-9_]+` | t10-derived-mapping | derived-mapping, with-table-sibling | `TRACE-T10 mut-site pattern='[^a-z0-9_]+'` | `map:…r/foo-probe.txt:derived` → `skip:…foo-probe.txt:no-committed-re-run-command` |
| T11 `if rel in RECEIPTS: continue` → `if False:` | t11-table-overrides-derived | table-overrides-derived, table-near-stem-decoy | `TRACE-T11 mut-site` present | `map:…tb2-grader-probe.txt:table` → `map:…tb2-grader-probe.txt:derived` |
| T12 `probe.*\.(?:txt\|log)$` → `probe.*\.(?:txt)$` | t12-log-population | log-population, log-with-table-sibling | `TRACE-T12 mut-site pattern='probe.*\\.(?:txt)$'` | `skip:…foo-probe.log:no-committed-re-run-command` → (class gone) |

**4/4 mutants: the mutated line executes at the credited killing fixture, and the class flip is exactly the
frozen silence rule** (declared class in reference and in `defects`, absent under the mutant). T10/T12 sites are
module-level assignments; the trace prints the mutated pattern at import and the classification flip proves the
mutated pattern is the one consulted.

Two fixtures are honest demonstrations that are NOT kill sites under the frozen rule (verified `exhibits=False`,
not a defect since the rule only credits the mutant's declared class):

- `r_map-t10-derived-deep-layout`: its receipt lives at `corpus/evidence/round41/scheduling/foo-probe.txt`, while
  T10's declared class names `corpus/evidence/r/foo-probe.txt`; the mutant does drop that class (mut shows
  `skip:…scheduling/foo-probe.txt:…`), but a different-path class does not credit. Reference behavior matches its
  declaration (`ok`).
- `r_map-t12-log-derived`: reference prints `map:…foo-probe.log:derived`, so T12's declared skip class is never
  present; exhibits requires it in the reference. Reference behavior matches its declaration (`ok`).

## 3. Wave-1 vector audit (per fixture, all 10)

Every fixture is `["--lane", "<d>/lane", "--list"]` — the tool's classify-only mode. Read of
`tip_receipts.py` `main()`: in `--list` it prints and returns before any `usage_argv`/`run_probe`/`clone`
execution, so **committed probe scripts are never executed**. Findings:

- **A1′/F1 probe-stub oracle** (stub reads the bound variant/slot and branches): unavailable — stubs never run in
  `--list` mode; and each stub is unconditional (`sys.stdout.write(<literal>)` / `raise SystemExit(<literal>)`),
  branching on nothing. No fixture uses a non-`--list` mode.
- **Counter scratch root, `variants/`, slot file**: the module performs zero file reads — only `ctx.write` and
  `ctx.git` (add/commit) on its own tree under `d`; variants do not even exist at build time.
- **`/proc`, `ppid`, …**: absent (read; token scan below).
- **Relative `../` argv (F4/A3)**: no `{WORK}` tokens, no `..`, no absolute path outside `d` (the counter's
  `path_ok` also enforced this; a breach would have raised, and `wrong=0` with 10 `ok` lines shows it did not).
- **Sockets / SysV IPC (F2/F3)**: none.
- **Reading tool or counter program text**: none; the only reads are the tool's own `provenance()` over the
  fixture's committed docs — the tool's advertised behavior on committed bytes.
- **Sidechannel text scan**: counter reports `sidechannel=0`; my own scan for all 23 SIDECHANNEL tokens plus
  `{WORK` and `..` over the module text: 0 hits (loop printed nothing, `scan-done`).

The verdict in every fixture comes solely from the tool's `--list` classification of a committed one-commit
tree — pure data, no runtime steering surface.

## 4. Per-fixture verdicts

| fixture | demonstrates (comment vs observed) | kill site? | verdict |
|---|---|---|---|
| t09-shared-stem-separators | stem `fooprobe` shared by `foo_probe.py`+`foo.probe.py` → unmapped skip; mut would map (`2>=1`) | yes (credited `killed by`) | honest |
| t09-shared-stem-case-fold | case-fold second hit `FooProbe.py` → 2 hits → skip; mut maps | yes | honest |
| t10-derived-mapping | separator-only stem match → `origin=derived`; mut keeps `_`, 0 hits → skip | yes (credited) | honest |
| t10-derived-with-table-sibling | derived maps while table sibling stays `table`; mut loses derived, table stands | yes | honest |
| t10-derived-deep-layout | same derivation two levels deep; ref `ok`; not a frozen-rule kill site (§2) | no | honest (demonstration) |
| t11-table-overrides-derived | both receipts table AND derivable; table overrides; mut flips both to derived | yes (credited) | honest |
| t11-table-near-stem-decoy | `_v2` near-stem is no match; tb2 stays `table`; mut derives (1 hit) | yes | honest |
| t12-log-population | `.log` in population → skip; mut drops `.log` → empty class set | yes (credited) | honest |
| t12-log-with-table-sibling | `.log` unmapped beside table receipt + `_v2` near-stem; mut loses skip, keeps table | yes | honest |
| t12-log-derived | `.log` with one matching script maps `derived`; not a frozen-rule kill site (§2) | no | honest (demonstration) |

**10/10 honest.** Each fixture's reference output equals its declared `defects` exactly (counter `ok` on all
ten), each demonstrates precisely the advertised behaviour its comment names, and no fixture touches any wave-1
vector. The module header's "each targeted twice" holds: per mutant, one base shape plus a second class-matched
shape; the two remaining fixtures are accurate demonstrations whose kill credit the frozen rule routes elsewhere.

## 5. Independence from the witness modules

Witnesses are `claims/witness/w_receipts.py` + `w_sources.py` (read in full; only `w_receipts.py` is relevant).
r_map.py imports nothing, references no witness path, and shares no code with them: its `stub()` emits a
different docstring shape and `sys.exit` vs the witness `probe()`'s `sys.exit` — helper functions, `lane()`
signatures, and fixture ids (`r_map-t09-*` vs `w-t09-*`) all differ. All 10 fixtures are self-contained
one-commit trees built from the module's own constants; the counter loads only the battery dir passed
(`$S/batonly`, r_map.py alone). No fixture needs or reads any witness artifact. **Independent: yes.**

## 6. Residual risk and verification gaps

- Full-battery attribution order: `r_ctl.py` sorts before `r_map.py`, so the landed `measure-final.txt` kill
  attribution for T09–T12 may name r_ctl fixtures. Nothing in this seat's evidence contradicts r_map's kills;
  confirming r_ctl does not poach them is r_ctl's reviewer's job.
- The two demonstration fixtures (deep-layout, log-derived) add no kill credit under the frozen class rule; if
  the module were the ONLY kill source, T10/T12 would still be killed (two sites each). No gap.
- The counter's sidechannel scan remains source-text-only (its own documented limit), but these fixtures offer
  no execution surface for it to bypass: `--list` runs nothing.
- Everything above was measured on the landing tip `3d0058fb` in a `--shared` clone inside the mandated
  envelope; nested counter sandboxes behaved (wave-1 precedent). No frozen file was modified; no lane file was
  written; `PINS-AFTER mismatched=0`.

## Receipts (all under `.ufo/waves/round-41/falsify/F41RevBatMap/`)

- `attrib.txt`, `attrib.err` — restricted attribution run (full stdout; stderr empty).
- `drv.py`, `drv.out`, `drv.err`, `exec.json` — traced-execution driver and its 80-run record.
- `r_map.reviewed-copy.py` — byte-copy of the reviewed module (digest `705a4b7c…`).

Scratch `/fast/scratch/hyaku/kengaku-r41/F41RevBatMap` removed after receipt copy (guard-checked `rm -rf`).

VERDICT: battery41-r_map-honest-10/10-mutated-line-executed-4/4
