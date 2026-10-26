# F37CritRenamed — the round-37 renamed run varies one path component, not fixture identity

Seat: F37CritRenamed (wave-2 falsify, critic). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`,
integration tip `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`. Scratch clone at the tip (verified
`git -C … rev-parse --show-toplevel` = the clone), removed before finishing. No lane file edited, no
tool installed.

Target: the renamed run of `plans/round37_c1_verify.py` and the frozen claim it carries —
`plans/round-37-claims.md:37`: "a renamed run (every fixture copied under another directory name) must agree".

Axes this seat attacks: **A1** soundness of `renamed_disagree=0` as evidence of name-independence;
**A2** calibration of the *accept* side of the battery (the three `expect=accept` fixtures);
**A3** identity cues the battery itself carries that no renaming removes; **A4** receipt reproducibility.
Every move below is read-only on the lane; none harms another axis.

## 1. What the renamed run actually varies: one component of one path

`plans/round37_c1_verify.py:334-345` copies each fixture directory to `ren_root` and rewrites **only argv
string tokens**:

```
335:        ren_root = root / "renamed"
339:            nd = ren_root / f"x{(len(built) - i) * 7919 % 100003:05d}q"
340:            shutil.copytree(d, nd, symlinks=True)
341:            nargv = [t.replace(str(d), str(nd)) for t in argv]
342:            if run_gate(ref_gate, ctx.spec_path, nargv) != ref[i]:
```

So the gate sees `/…/fx/f000` in the reference run and `/…/renamed/x79190q` in the renamed run. Unchanged in
both runs: the interior tree (every file name and every byte), the gate copy (`ref.py`, line 317), the spec
path (`plans/pkg-spec-r35.json` in the lane), the argv shape, and the harness's own temp prefix
`tempfile.mkdtemp(prefix="k37-c1-", dir=a.work)` (line 299).

Measured on my clone (`receipts/probe1.out`):

```
FIXTURES n=64 r36=14 b37=50
RENAME argv_unchanged=0 of 64
CUES fixtures_with_fid_in_path=0
```

The ticket's premise holds: no fixture id is in a path (the harness names fixtures `f{i:03d}`,
`round37_c1_verify.py:307`, and each fid is unique), and all 64 argv lists are rewritten. But the reference
run's own names `f000…f063` are 1:1 with `fid` because the battery order is deterministic, so the reference
run still measures each fixture under its own stable identity — the rename only re-codes that identity.

## 2. Counterexample: a gate that recognizes the genuine fixture passes the frozen predicate

The accept side of the battery is three fixtures (`receipts/probe4.out`:
`IDENT accept_fixtures=['r36-P0', 'r36-L1', 'r36-L4']`), and `P0` acceptance is the only evidence that the
gate accepts anything. Identity survives any renaming as **content**: `IDENT content_unique_fixtures=59/64`
(sha256 over (relative path, file sha256) pairs excluding `.git`; 59 distinct).

I added a recognition branch to a clone of `plans/pkg_gate.py` — it hashes the tree, and if the digest is the
recorded `r36-P0` digest it returns 0 **without running any clause** (`receipts/oracle-gate-patch.txt`), then
re-pinned the counter's `GATE_SHA256` to that gate (an author who writes such a gate would freeze that
digest). Running the frozen predicate on the clean tip clone with that gate
(`receipts/oracle-gate.txt`):

```
GATE plans/pkg_gate.py sha256=frozen
FIXTURE r36-P0 expect=accept declared=- observed_rc=0 observed_defects=- ok
BATTERY fixtures=64 wrong=0 renamed_disagree=0
MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass
```

exit 0 — the full frozen `PREDICATE C1 pass`. The short-circuit is visible only if the gate's own stdout is
read; the counter's observable is `(exit code, set of clauses printing DEFECT)`:

```
$ python3 <honest gate> package --root <r36-P0> --require-clean-tree --spec …
P1 ok pinned=3 mismatched=0 … P9 ok untracked=0 first=0
defects=0
rc=0
$ python3 <recognizing gate> package --root <same bytes> …
rc=0
```

(`receipts/shortcircuit.txt`; ten clause lines versus none, same `rc`.)

The landed post-hoc audit does **not** cover this: the recognizing gate also prints
`ATTRIBUTED 55/55 UNATTRIBUTED=0`, exit 0 (`receipts/oracle-attribution.txt`) — that audit inspects kills
only. So this is not the gameability limit already recorded at the tip (which is about kill attribution);
it is the accept side, and the renamed run is blind to it by construction.

This is a fixable defect in the evidence chain, not a tradeoff of the gate: nothing in the battery asks the
gate to *print* the clause statuses it claims to have run.

## 3. Positive control: the check does catch one channel

`receipts/variants.txt`, five gate variants over the 64 built fixtures, reference vs the counter's own rename
transform:

```
VARIANT V0-honest renamed_disagree=0 wrong=0 matching_declaration=64/64
VARIANT V1-top-name-keyed renamed_disagree=48 wrong=0 matching_declaration=64/64
VARIANT V2-interior-name-keyed renamed_disagree=0 wrong=1 matching_declaration=63/64
VARIANT V3-harness-prefix-keyed renamed_disagree=0 wrong=47 matching_declaration=17/64
VARIANT V4-content-marker-keyed renamed_disagree=0 wrong=1 matching_declaration=63/64
```

V1 (`if re.fullmatch(r"x\d{5}q", pkg.root.name): return 1`) is caught 48 times: the renamed run is live for
the one component it varies. V2/V3/V4 are keyed on channels it never varies and produce
`renamed_disagree=0`:

- **V2** keys on an interior file name (`"relabelled" in str(args.file)` — `plans/battery37/d4.py:62`).
- **V3** keys on the harness prefix `k37-c1-` (line 299), shared by both runs.
- **V4** keys on a marker a battery module writes into fixture bytes: `"# line appended by the M15 fixture"`
  (`plans/battery37/p5.py:105`; the same at `:156` for M17). V4 lands in `task.toml` / `test_outputs.py`
  (`receipts/probe4.out`: `IDENT fixtures_with_mutant_id_marker_in_bytes=2`).

V2/V4 are still caught by the declaration column (`wrong=1`) because they invert a reject verdict; V3 is
caught only because it accepts indiscriminately. A channel-keyed *shortcut* that preserves the verdict (the
recognition gate of §2) is caught by neither column.

## 4. Do the battery modules carry cues? Yes — but the mutant column neutralizes the ones that invert

`receipts/probe4.out`: 38 of 64 fixtures have at least one interior file name that appears in no other
fixture (`IDENT fixtures_with_identity_bearing_names=38`); 2 of those spell the defect itself —
`d4-correction-two-lines.txt` (`plans/battery37/d4.py:46`) and `d4-correction-relabelled.txt` (`:62`). The
r36 line fixtures write a fixed six-name set into every directory (`d4-swapped.txt`, `d5-negated.txt`,
`alt-captures`, … — `plans/round36_c1_verify.py:183-204`), so they are not identity-bearing. The `junk`
marker the ticket asks about is dead as a cue: `CUES fixtures_with_junk_literal_in_content=48` of 64, i.e. it
is present in the genuine package too (inherited lane text), so it does not discriminate.

Honest reading: the mutant criterion already neutralizes a cue-keyed *reject* shortcut — the reference run
and the mutant both see the same cue, so the mutant is not killed and the predicate fails. The dangerous cue
class is the accept side (§2), where no clause-level criterion exists at all.

## 5. Harness integrity nits (none observed to fire today)

- The copy is taken **after** the reference gate run over the same directory (reference loop at lines 319-330,
  copy at line 340). If any gate ever
  writes into the tree, the renamed run starts from different bytes than the reference did. Probe over
  `r36-P0`, `r36-P7`, a d4/d5 fixture: `MUTATE … same=True` for all three (`receipts/probe1.out`), so it is a
  latent ordering hazard, not an observed defect. Fix is one line: copy before the reference loop, or assert
  the tree digest is identical in both runs.
- No assertion that the rename changed argv. Today `RENAME argv_unchanged=0 of 64`; a future fixture whose
  argv does not contain its root would silently "agree".
- The new names are a fixed, source-visible scheme (5 digits + `q`, same length, unique) — fine for
  invariance, useless as an anti-mode-detection device.
- Observable is `(rc, DEFECT set)`: a gate that changes messages by name is invisible.

## 6. Stronger renaming (content-preserving) and whether the round-37 battery survives it

Proposal, in the order that costs least:

1. Draw each fixture's directory name from `secrets.token_hex(8)` (or `uuid4`), **twice**: reference run on
   draw R1, renamed run on an independent draw R2 — no `f###`, no `x####q`, nothing identity- or
   mode-correlated. Randomize the `mkdtemp` prefix per invocation as well (line 299), and copy the spec into
   the temp root.
2. Assert every argv token that names a path under the fixture root was rewritten, and that the new root
   differs from the old.
3. Copy the pristine tree before the first gate run; assert a per-tree digest manifest (excluding `.git`) is
   byte-identical between the two runs modulo the declared renames.
4. Compare full stdout, not only `(rc, DEFECT set)`.
5. Rename interior **identity** names too, under an explicit contract: each fixture declares the relative
   paths it invents (`identity: [...]`), the harness renames those components to random tokens and rewrites
   argv/content references. Names pinned by the spec (entry, capture name, manifest name) are never renamed.

Would the round-37 battery survive it?

- Steps 1-4: **yes.** All 64 fixtures build their argv from the directory the counter hands in
  (`RENAME argv_unchanged=0 of 64`) and none puts its fid in a path (`fixtures_with_fid_in_path=0`); the gate
  is spec-driven, so a random root name is safe. My V0 run already measures the untransformed battery at
  `wrong=0`.
- Step 5: **no, not unchanged.** 38 fixtures invent names the builder hardcodes, and 2 of them quantify over
  the defect (`two-lines`, `relabelled`); the module contract has no `identity` field today. The fix is a
  small builder-contract change plus touching those 38 fixtures (renaming `caps/`, `d4-correction-*.txt`,
  `no-such-erratum.txt`, `erratum.txt`, `alt-captures/`, the `zz-*` notes, …). Package fixtures keep their
  spec-pinned names, which is exactly the line the contract must draw.

## 7. Smallest safe correction

- **Now, without touching the frozen rule**: record the limit in the claims/lesson erratum, in the words the
  numbers support — the renamed run varies the last path component only; identity is recoverable from bytes
  (59/64 unique digests) and from interior names (38/64); a gate that recognizes the genuine fixture by
  content prints the full predicate pass and also `ATTRIBUTED 55/55`. Do not read `renamed_disagree=0` as
  "the gate never keys on a fixture".
- **Next round, smallest evidence fix (A2)**: extend the counter's observable from `(rc, DEFECT set)` to
  include the sorted clause-status lines (`P1 ok …` etc.). The recognition gate then differs on `r36-P0`
  (zero lines vs ten) — the accept side becomes calibrated for free, and the 55 mutants keep their criterion.
- **Next round, A1**: steps 1-4 above, ~15 lines in the renamed block, accepted by the current battery.

Impact on the lane's self-description: `plans/pkg_gate.py:10-11` says "The gate never asks what the caller
calls its fixture and never inspects a path for a fixture marker." The renamed run demonstrates that for the
top-level component only, and only against a gate that must agree with the declarations — not in general.

## 8. Corroboration and receipts

- Baseline on a clean tip clone, independent of the wave-1 receipt: `BATTERY fixtures=64 wrong=0
  renamed_disagree=0`, `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0`, `PREDICATE C1
  pass`, exit 0, 79 s (`receipts/baseline.txt`, `receipts/baseline-summary.txt`). `measure-final.txt:1` names
  tip `5c7d5d75`, an ancestor of the landing; the tip's own diff touches none of `plans/pkg_gate.py`,
  `plans/battery37/`, `plans/round37_c1_verify.py`.
- Receipts in `receipts/`: `probe1.out` (structure/rename coverage), `variants.txt` + `probe3.out` (five
  variants), `probe4.out` (identity channels), `oracle-gate.txt` + `oracle-attribution.txt` +
  `oracle-gate-patch.txt` + `shortcircuit.txt` (the recognition counterexample), `baseline*.txt`.
- Probes are read-only on the lane and reproduced the counter's exact build path by importing
  `plans/round37_c1_verify.py` (`Ctx`, `r36_fixtures`, `battery37_fixtures`); the probes live in this seat
  directory. Scratch `/fast/scratch/hyaku/kengaku-r37/F37CritRenamed` deleted (`SCRATCH_REMOVED`). No tool
  installed or upgraded.

VERDICT: renamed-run-weak-cues-5
