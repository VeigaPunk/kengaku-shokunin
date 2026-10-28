# Round 49 — seat R49C1ExecCounter (executor, SERVE R49-C1 calibration)

date: 2026-10-28
lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (read-only), base lane tip `9d2900af41e4d1fc6022eff99010436fde6dbd93`
scratch: `/fast/scratch/hyaku/kengaku-r49/R49C1ExecCounter` (NVMe; `TMPDIR` exported there; **removed before this seat yielded** — see §9)
deliverable: `plans/round49_c1_verify.py`, transcribed verbatim at
`.ufo/waves/round-49/w1/R49C1ExecCounter/candidate.py` — 594 lines, sha256
`9c7b73e31e64ef61c021324af5a10dfdd42c1d23163b20f784c93ab0c0dd0daa`

**Axes named.** Primary: **calibration** (R49-C1, the fixture fence's honest over-refusal under a v3 counter).
Secondary, in the sense of what this seat's artifact can green or red: none — I touched no C2 file, no probe, no
package, no `plans/order_check.py`; **coverage** (R49-C2) is untouched by this seat. Nothing here claims novelty,
depth, operability or freshness.

**Revision measured.** Every run below was made against a scratch clone (`git clone --shared`) pinned at
`9d2900af41e4d1fc6022eff99010436fde6dbd93`, whose clone toplevel was asserted before any write. The frozen
stage-1 commit exists in the committed lane tree, is an ancestor of the wave tip, and predates the measurement:

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
af88aab193e6034cb9b386472064e3c18fa90128
$ git -C … cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93 ; git -C … log -1 --format='%H %ci %s' 9d2900…
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28 09:14:40 -0300 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims
$ git -C … merge-base --is-ancestor 9d2900af41e4d1fc6022eff99010436fde6dbd93 HEAD && echo ANCESTOR-OK
ANCESTOR-OK
```

No scored counter/probe execution was made against claimed work; every run below is a **selftest on a scratch
clone of the base**, exactly as the item's ordering rule requires. No commit, push or mutating git command was run
in the lane; the only git use in scratch was the clone and read-only `rev-parse`/`status`/`checkout`.

Sources opened (local lane files, no URL opened by this seat; no URL/access-date line applies):

- `plans/round-49-claims.md` — binding contract. Located quote (≤25 words): "the counter applies each mutant to a
  copy of the landed fence and re-measures the three legs on that copy".
- `corpus/lessons/round-48-verifier-spotcheck.md` — routed defects. Located quote (≤25 words): "Any future C1
  admission attempt needs the mutation floor committed with receipts."
- `plans/round46_c1_verify.py` (imported contract, pin `ef19380e…` re-verified), `plans/fixture_fence.py`
  (`05d5fe03…`), `plans/refusals46/` (20), `plans/sealed46/` (12), `plans/battery4{2,3,4}/` (22 modules / 104
  fixtures).

## 1. What was built

`plans/round49_c1_verify.py` = the round-48 v2 candidate
(`.ufo/waves/round-48/w1/R48C1ExecControls/fences/round48_c1_verify.v2.py`) with the frozen round-49 renames and
the new MUTANTS leg:

- predicate renamed `R49-C1`; populations renamed `plans/honest49/`, `plans/sealed49/`, mutants at
  `plans/mutants49/c1-mutants.json`; `REV`/`PINS`/`REFUSALS`/`SEALED`/`HONEST`/`BENIGN`/`CALIBRATION` lines and
  their fail reasons are the round-48 lines with the round-49 names.
- **stage-2 literal block** (fills only; no predicate line may move): `REFUSAL_FLOOR=20`, `SEALED_FROZEN=12`,
  `SEALED_TOTAL=12`, `HONEST_BATTERY=104`, `HONEST_NOVEL_EXPECTED=0`, `HONEST_TOTAL=104`, `MUTANT_MIN=12`,
  `MUTANT_FLOOR=0`, `PINS_EXTRA={}`. `--literals` prints the exact `LITERALS-TO-PASTE` line plus one `PIN "…"
  "<sha256>"` line per `honest49`/`sealed49` module, so stage 2 pastes numbers it measured, never numbers it
  asserted.
- **delta (f), the MUTANTS leg.** Declared schema (documented in the module docstring): either
  `{"mutants": [...]}` or a bare list; each entry `{id, payload, digest, description}` (`path`/`sha256`/`desc`
  accepted as aliases), `payload` = a lane-relative or absolute **full mutated copy of the landed fence**,
  `digest` = its sha256. Per mutant the counter: verifies the digest, `ast.parse`s the payload and requires a
  top-level `breach()`, then loads it in place of the fence copy and **re-measures all three legs over the same
  built fixtures** (one build for `<M>+1` fence passes, so a mutant cannot be "caught" by perturbing fixture
  construction). Each mutant fence gets its own `ctl` directory because the round-46 analyser excludes the `ctl`
  directory from outside-`d` hits — sharing `ctl` makes every mutant look like a leak (this was measured; see §5).
- **catch rule.** A mutant is caught iff its pass is *strictly worse* than the landed fence's own measured pass on
  the same fixtures: fewer hostile modules refused, more `leak`/`read`/`hung`/`benign`/`error`/`build_errors`, fewer
  honest admissions, or any honest refusal/read/hang/build error. Comparing to the landed fence's real pass (not
  an idealised all-clean line) keeps the battery honest when the landed fence is already red, and a payload that
  only moves bytes no leg observes *survives* by design — the floor, not any single mutant, is the claim.
- **floor.** `MUTANTS total=<M> caught=<k> floor=<M>/2 verdict=met|unmet`, printed **before** `CALIBRATION`;
  `verdict=met` iff `caught >= ceil(<M>/2)`. The predicate additionally fails on `mutants-total=<M><12`
  (`MUTANT_MIN`), on `<M>` ≠ `MUTANT_FLOOR` once stage 2 freezes it, on `mutants-caught=<k><M/2`, on
  `mutants-broken=<n>` and on `mutants-declared=<n>` (malformed/duplicate declarations are defects, never silent
  narrowing). A missing JSON is `MUTANTS total=0 caught=0 floor=0/2 verdict=unmet` + fail — never a crash.
- Delta (b) classification, (c) name hiding, (d) strace envelope B1/B3/B4/B5/B6 and (e) refusal/sealed populations
  are the round-46 inherited code paths, unchanged; the honest leg still splits battery vs novel and
  `HONEST_NOVEL_EXPECTED` binds the novel half from both sides.
- `--literals`, `--refusals`, `--sealed`, `--honest`, `--fence`, `--mutants`, `--seed` remain testing overrides;
  `--mutants` was added alongside them, and `default_mode` now also requires `--mutants` absent.

## 2. Freeze/pin preconditions observed

```
$ sha256sum plans/round46_c1_verify.py plans/fixture_fence.py plans/round44_c1_verify.py
ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508  plans/round46_c1_verify.py
05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  plans/fixture_fence.py
6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad  plans/round44_c1_verify.py
```

`round46_c1_verify.py` still matches the counter's `R46_PIN`, so the imported contract loads (a mismatch is a
`SETUP … return 2`, never a silent pass). `plans/mutants49/`, `plans/honest49/`, `plans/sealed49/` **do not exist
in the base tree** (`ls: cannot access 'plans/mutants49'…`), which is expected: wave-1 mutation-tester and honest
seats author them.

## 3. `--literals` on the frozen base clone (verbatim)

```
$ python3 clone/plans/round49_c1_verify.py --lane clone --literals
REV 9d2900af41e4d1fc6022eff99010436fde6dbd93
TREE dirty=1 (override)
PINS total=66 mismatched=0
LITERALS refusals=20 sealed_frozen=12 sealed_extra=0 honest_battery_modules=22 honest_battery_fixtures=104 honest_novel_modules=0 mutants=0 pins_extra=0
LITERALS-TO-PASTE REFUSAL_FLOOR=20 SEALED_EXTRA_EXPECTED=0 SEALED_TOTAL=12 HONEST_NOVEL_EXPECTED=0 MUTANT_FLOOR=0
MUTANT-ISSUE …/clone/plans/mutants49/c1-mutants.json:absent
REV 9d2900af41e4d1fc6022eff99010436fde6dbd93
```

Staged-layout literals (scratch clone only: 16 r48 novel modules copied to `plans/honest49/`, one sealed module
to `plans/sealed49/`, a 12-entry JSON to `plans/mutants49/c1-mutants.json`) — this is the exact paste stage 2 will
consume:

```
LITERALS refusals=20 sealed_frozen=12 sealed_extra=1 honest_battery_modules=22 honest_battery_fixtures=104 honest_novel_modules=16 mutants=12 pins_extra=0
LITERALS-TO-PASTE REFUSAL_FLOOR=20 SEALED_EXTRA_EXPECTED=1 SEALED_TOTAL=13 HONEST_NOVEL_EXPECTED=16 MUTANT_FLOOR=12
PIN "plans/sealed49/a_phantom_order.py" "debf651d002e7c7b8c8f9c6430fe662d0851cd1e2d72994b9523122ee9bd25c5"
PIN "plans/honest49/n01_packed_refs.py" "9e1a2058e326781e0fb7007f041c2f13caa21b93fbd9cea6f668eb3765dac853"
… (16 honest49 PIN lines total, one per module)
```

## 4. Base-fence before values, re-measured through the v3 code path

Base fence, 104-fixture battery alone:

```
FENCE source=…/clone/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
BENIGN total=104
MUTANTS total=0 caught=0 floor=0/2 verdict=unmet
REASON sealed-total=2!=12,mutants-total=0<12,mutants-declared=1
PREDICATE R49-C1 fail
```

Base fence on the **round-48 120-fixture population** (104 battery + the 16 novel modules from
`.ufo/waves/round-48/w1/R48C1ExecHonest/modules/{r46novel,novel48}`, staged flat; all 16 staged bytes match the
round-48 `PINS_EXTRA` digests — `r48-novel-pins=16 staged=16 mismatched=0`):

```
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=120 admitted=112 refused=8 read=0 hung=0 build_errors=0
BENIGN total=112
```

i.e. the round-48 published before value `HONEST fixtures=120 admitted=112 refused=8` reproduces exactly through
the v3 counter, and the eight refusals are pinned to named classes with their reasons:

```
FENCE-RUN honest r48honest/n12_local_config_user.py n12-local-config-user BREACH clean touches=0 calls=446 -- BREACH repo/.git/config section [user] is not allowlisted
FENCE-RUN honest r48honest/n14_stash_entry.py n14-stash-entry BREACH clean touches=0 calls=473 -- BREACH refs/stash has a name git does not write
FENCE-RUN honest r48honest/n08_tag_detached.py n08-tag-detached BREACH clean touches=0 calls=445 -- BREACH repo/.git/HEAD is not a plain branch HEAD
FENCE-RUN honest r48honest/n13_remote_origin.py n13-remote-origin BREACH clean touches=0 calls=446 -- BREACH repo/.git/config section header b'[remote "origin"]' is not plain
FENCE-RUN honest r48honest/n15_commit_graph.py n15-commit-graph BREACH clean touches=0 calls=495 -- BREACH repo/.git/objects/info/commit-graph present (object-store redirect)
FENCE-RUN honest r48honest/n03_detached_head.py n03-detached-head BREACH clean touches=0 calls=445 -- BREACH repo/.git/HEAD is not a plain branch HEAD
FENCE-RUN honest r48honest/n16_notes_ref.py n16-notes-ref BREACH clean touches=0 calls=471 -- BREACH refs/notes has a name git does not write
FENCE-RUN honest r48honest/n07_reflog_gc.py n07-reflog-gc BREACH clean touches=0 calls=466 -- BREACH repo/.git/info/refs is not git's exclude file
```

**Stage-2 consequence (actionable).** The 104 battery fixtures are admitted 104/104 by the base fence, so the
C1 do-nothing control (`base fence must fail on the honest leg at stage 2`) can only fire if the stage-2 honest
population includes novel classes the base fence over-refuses. The known-resistant honest shapes are:
detached/plain-HEAD (`n03`, `n08`), reflog-gc/`info/refs` (`n07`), local `[user]` config (`n12`), `[remote
"origin"]` (`n13`), `refs/stash` (`n14`), `objects/info/commit-graph` (`n15`), `refs/notes` (`n16`). A wave-1
honest seat that authors only shapes the base fence already admits cannot make the control fail.

## 5. MUTANTS leg — measured behaviour

Selftest A (5 mutants of the *base* fence, override populations: 3 refusal modules, 2 sealed modules, 3 honest
modules on top of the 104 battery; `--seed 49c1 --jobs 16`):

```
FENCE source=…/clone/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
REFUSALS total=3 clean=3 leaked=0 read=0 hung=0 build_errors=0
SEALED total=2 clean=2 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 read=0 hung=0 build_errors=0
BENIGN total=126
MUTANT m01_admit_all caught breaks=refusals-clean=0<3,refusals-benign=3>0,sealed-clean=0<2,sealed-benign=2>0 desc=admit everything: hostile modules admitted
MUTANT m02_refuse_all caught breaks=honest-admitted=0<126,honest-refused=126>0 desc=refuse everything: honest fixtures refused
MUTANT m03_noop survived desc=byte-identical copy of the landed fence: must survive
MUTANT m04_read_sibling caught breaks=refusals-clean=0<3,refusals-leak=1>0,refusals-error=2>0,sealed-clean=0<2,sealed-leak=2>0 desc=admit after reading sibling fixture dirs: outside access
MUTANT m05_broken broken unparseable SyntaxError desc=does not parse: broken, never caught
MUTANTS total=5 caught=3 floor=5/2 verdict=met
REASON refusals-total=3!=20,sealed-total=2!=12,honest-fixtures=126!=104,mutants-total=5<12,mutants-broken=1,mutants-declared=1
PREDICATE R49-C1 fail
```

All five outcomes are the intended ones: admit-all caught on the hostile legs, refuse-all caught on the honest leg,
a **byte-identical fence survives** (no false catch), an outside-`d` reader caught through the traced `leak`
bucket, and a non-parsing payload reported `broken` and never counted as caught (so a broken payload cannot inflate
the floor). `floor=5/2 verdict=met` with 3 caught is arithmetically right (`3 ≥ ceil(2.5)`), and the predicate
still fails because `<M>=5 < MUTANT_MIN=12`.

One measured design fact (kept in the code as a comment): with the mutant fence in the *shared* `ctl` directory
the round-46 analyser counts loading the fence under test as an outside-`d` touch, which made even the byte-identical
mutant "caught" (`honest-admitted=0<126`, `refusals-read=3>0`). Giving each mutant pass its own `ctl` directory —
the same exclusion the clean pass relies on — fixed it; the surviving no-op above is the regression test for it.

Selftest B (12-mutant floor boundary; 6 × admit-all + 6 × no-op, and 5 × admit-all + 7 × no-op):

```
MUTANTS total=12 caught=6 floor=12/2 verdict=met
REASON refusals-total=3!=20,sealed-total=2!=12,honest-fixtures=126!=104
MUTANTS total=12 caught=5 floor=12/2 verdict=unmet
REASON refusals-total=3!=20,sealed-total=2!=12,honest-fixtures=126!=104,mutants-caught=5<12/2
```

Selftest C (default mode, staged `honest49/sealed49/mutants49` in the scratch clone — exercises `copy_rows`, the
unpinned-input rule and lane-relative resolution end to end):

```
TREE dirty=4
PINS total=66 mismatched=17 first=plans/honest49/n01_packed_refs.py:unpinned
PIN-MISMATCH plans/sealed49/a_phantom_order.py:unpinned
COPY f1_gitfile.py ok … COPY f10_laneinclude.py ok
MODULES refusal total=20 / sealed total=13 / honest total=38
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0
SEALED total=13 clean=13 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=120 admitted=112 refused=8 read=0 hung=0 build_errors=0
BENIGN total=112
MUTANTS total=12 caught=6 floor=12/2 verdict=met
CALIBRATION advertised=33 contradicted=0
REASON pins=17,tree-dirty=4,sealed-total=13!=12,honest-fixtures=120!=104,honest-not-admitted
PREDICATE R49-C1 fail
```

Every line of the frozen predicate sequence printed, in order, and the pre-stage-2 tree fails for the right
reasons (unpinned novel inputs, unfilled literals) — not for a code defect.

## 6. Satisfiability of the pass path (no unsatisfiable leg)

A scratch-only copy of the counter with the literals patched to the selftest population (3 refusals / 2 sealed /
104 honest / 12 mutants; this copy is **not** the deliverable and is not transcribed) prints the complete pass
path, exit 0:

```
PINS total=66 mismatched=0
REFUSALS total=3 clean=3 leaked=0 read=0 hung=0 build_errors=0
SEALED total=2 clean=2 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
BENIGN total=104
MUTANTS total=12 caught=6 floor=12/2 verdict=met
CALIBRATION advertised=5 contradicted=0
REASON -
PREDICATE R49-C1 pass
exit=0
```

So no line of the round-49 predicate is unsatisfiable by construction (the round-46 V7 lesson), and `REASON -`
is reachable.

## 7. Determinism

Same seed, same command, run twice after the staged dirs were removed from the clone:

```
diff <(grep -E '^(REFUSALS|SEALED total|HONEST |BENIGN )' det-2.txt) <(… det-3.txt) && echo DET104-SAME
DET104-SAME
diff <(… det120-2.txt) <(… det120-3.txt) && echo DET120-SAME
DET120-SAME
det-2.txt:HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
det120-2.txt:HONEST fixtures=120 admitted=112 refused=8 read=0 hung=0 build_errors=0
```

(An earlier "nondeterministic" diff was my own concurrency mistake: a sibling tool call staged `plans/honest49/`
into the clone while the repeat run was in flight. The repeat above is the clean measurement.)

## 8. Limits (named, not hidden)

- Inherited from the round-46 contract, unchanged: `io_uring` SQE opens/reads emit no traced syscall (B7, not
  exploited); host paths outside the scratch root are not counted; a directory stat's `st_nlink` channel is nulled
  by padding, not measured; a module that fails to build contributes no fixtures and is counted in
  `build_errors`.
- The mutant battery costs one full fence pass per mutant over the *whole* population (`<M>+1` passes, one build).
  On this host a ~130-fixture pass at `--jobs 16` took ~1–2 s; the frozen population (120 honest + 20 + S) with
  `<M>`=13 should be well under a minute per battery, but the receipt should keep `--jobs` at the default 8 to
  match the stage-2 command exactly.
- A mutant payload is trusted exactly as far as its pinned digest; the counter executes the mutated fence inside
  the same sandbox as the fence under test, and applies it by replacement, so the accepted payload form is a
  **full mutated module**. If the wave-1 mutation-tester seats author unified diffs or `mutate(src)` callables
  instead, the JSON must be re-expressed (or the counter's `mutant_bytes` extended) at stage 2 — the counter
  reports such a payload as `broken` with a precise reason, never as caught.
- Overrides print the predicate of the inputs they name, by design; only the default-mode line order on a clean
  clone of the landing tip is the claim's receipt.
- A `BrokenPipeError` from a receipt pipeline closing early (`| head`) is swallowed as exit 1 instead of a
  traceback; it cannot change a verdict.

## 9. Risks / follow-ups for the L1

1. **Stage-2 must pin `PINS_EXTRA`** with the `--literals` `PIN` lines and set `SEALED_TOTAL`,
   `HONEST_NOVEL_EXPECTED`, `HONEST_TOTAL`, `MUTANT_FLOOR` from measured counts; until then a default run fails
   `pins=…:unpinned` by design. No predicate line needs to move.
2. **`plans/mutants49/c1-mutants.json` was absent** in the base tree at the time of every run. The counter's
   accepted schema is stated in the module docstring; if the mutation-tester seats emit a different shape, stage 2
   must align the JSON (cheaper) rather than the counter (contract touch).
3. **The honest-half composition decides whether the do-nothing control can fire** (§4): battery-only
   populations are admitted 104/104 by the base fence; the eight known over-refusal classes are named above.
4. Fence repair is out of this seat's scope: with the base fence the honest leg on the r48 120-fixture
   population is 112/120, so a stage-2 pin at `<H>`=120 with the *unrepaired* fence fails `honest-not-admitted`,
   as the round-48 do-nothing control requires.

## 10. Scratch hygiene

`/fast/scratch/hyaku/kengaku-r49/R49C1ExecCounter` held exactly one `git clone --shared` of the lane at the frozen
base tip, the selftest populations, the five + twelve mutant declarations and the run transcripts. Its `REV` lines
are quoted above; the scratch tree was removed at the end of this seat (scratch-defect rule: no seat ends with its
scratch on disk). Only two lane paths were written by this seat: this report and
`.ufo/waves/round-49/w1/R49C1ExecCounter/candidate.py`.

VERDICT: DELIVERED — `plans/round49_c1_verify.py` v3 counter (candidate.py, sha256 `9c7b73e3…`) implements the
frozen C1 predicate including the new gated MUTANTS leg (`total=<M> caught=<k> floor=<M>/2 verdict=met|unmet`
before `CALIBRATION`, fail on `<M>`<12, `caught`<ceil(`<M>`/2), broken or malformed declarations), reproduces the
round-48 before value 112/120 exactly on the base fence, catches admit-all/refuse-all/outside-read mutants, lets a
byte-identical mutant survive, reports a broken payload as broken, has a reachable pass path and is deterministic
under a fixed seed. R49-C1 is **not** admitted by this seat: admission needs the landed repaired fence plus the
stage-2 pins (honest49/sealed49/mutants49), which do not exist in the base tree.
