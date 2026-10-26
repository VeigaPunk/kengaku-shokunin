# R38BatP10b — battery38 module killing N15 (P10 mirror: the pass side of `--rerun`)

Seat: executor, round 38 wave 1, lane `kengaku-shokunin`. Target mutant: **N15 only** (clause `P10`,
direction `mirror`). Deliverable: `.ufo/waves/round-38/build/R38BatP10b/battery/p10b.py` (destined for
`plans/battery38/p10b.py`, L1 integrates — I edited no lane file).

## Mutant and the hole it names

- Frozen mutant: `plans/round38_c1_verify.py:127-128` — N15 `P10 mirror` "a byte-equal fresh run passes
  P10 [Q24 genuine accepted; F37XMutP910 L2; R37PlanNext B5]", `old -> new` =
  `return True, f"probe_rerun=byte-equal` → `return False, f"probe_rerun=byte-equal`.
- Gate branch it silences: `plans/pkg_gate.py:285` `return True, f"probe_rerun=byte-equal bytes={len(want)}"`.
- Why no round-36/37 fixture sees it: every `--rerun` fixture in batteries 36/37 is a **reject**, so the
  reference gate printer there is `P10 DEFECT`, never `P10 ok` — the measured B5 shape,
  `.ufo/waves/round-37/build/R37PlanNext.md:252-256` ("B5 | 283-285 | P10 **pass** side … | no").
- Kill rule used: `plans/round38_c1_verify.py` `attributed()`, mirror arm — reference prints the clause
  `ok`, mutant prints it `DEFECT`, both exits in `{0,1}`, subcommand family `package`.

## The fixture (one, load-bearing)

`p10b-rerun-byte-equal-accept` — `expect="accept"`, `defects=[]` (so the declared set is also the exact
reference DEFECT set: empty). Build:

1. `ctx.genuine_package(d)` — git-inits `d` (top-level verified), copies the genuine round-35 package
   bytes named by `ctx.spec` (`plans/pkg-spec-r35.json`), including all three `frozen_instruments`
   (so P1's `pinned=3` stays coherent) and the entry/SOURCES/README/knowledge/lessons tree.
2. Overwrites the receipt at the **same relative path** the genuine spec names
   (`corpus/evidence/round35/tb2-grader-probe.txt`) with a known 37-byte line, so P8's coverage bullet
   (`entry and receipt_rel`) and P2's digest pin both stay coherent with one edit.
3. Writes `p10b-spec.json` **inside `d`** = `copy.deepcopy(ctx.spec)` with `probe_cmd = ["-c", <one
   expression program printing the receipt bytes>]` and `receipt_sha256` = sha256 of the bytes just
   written. The gate runs `[sys.executable] + probe_cmd` when `import Bio` works, else
   `uv run --no-project --with biopython==1.85 python3 -c …` with `cwd = root` — `-c` is accepted on
   both arms and writes no `__pycache__`, so P9 needs no ignore rule.
4. `ctx.git_add(d)` — stages the spec file too (otherwise P9 would fire on the fixture's own spec).
5. argv: `["package", "--root", d, "--require-clean-tree", "--rerun", "--spec", d/p10b-spec.json]`.

Nothing else in the package is altered: P3–P8 run on the unmodified genuine bytes, P9 on a clean index,
P2/P10 on the fixture's receipt.

## Evidence

Scratch `S=/fast/scratch/hyaku/kengaku-r38/R38BatP10b` (NVMe, never `/tmp`), `export TMPDIR=$S`,
`git clone -q --shared <lane> $S/lane`, `git -C $S/lane rev-parse --show-toplevel` = `$S/lane`
(clone tip `2c5f4e0ba8e2865af4b71e337f3cde86eaf0702e`). Full receipts copied into this seat dir before
scratch was deleted.

1) Counter, module supplied via `--battery-dir` (byte-identical across two consecutive runs,
   `cmp run1.txt run2.txt` → equal; full 65-fixture output: `R38BatP10b/counter-n15.txt`):

```
$ python3 plans/round38_c1_verify.py --lane "$S/lane" \
    --battery-dir .../R38BatP10b/battery --only N15 --work "$S/w"
PINS total=14 mismatched=0
FIXTURE p10b-rerun-byte-equal-accept expect=accept declared=- observed_rc=0 observed_defects=- ok
BATTERY fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N15 P10 mirror killed by=p10b-rerun-byte-equal-accept -- a byte-equal fresh run passes P10 [Q24 genuine accepted; F37XMutP910 L2; R37PlanNext B5]
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
rc=0
```

   (65 = the 64 frozen round-36+37 fixtures, all `ok`, + mine; no duplicate-fid `SETUP` abort.)

2) Landing path — module copied to `$S/lane/plans/battery38/p10b.py`, counter run with its **default**
   battery dir (same fixture line; `PINS total=14 mismatched=0`, `fixtures=65 wrong=0
   renamed_disagree=0 sidechannel=0`, `killed=1 survived=0`, rc 0). `git -C $S/lane status --porcelain`
   printed only `?? plans/battery38/` — no lane file touched.

3) Load-bearing (fixture removed — empty `--battery-dir`), `R38BatP10b/counter-n15-no-fixture.txt`:

```
PINS total=14 mismatched=0
BATTERY fixtures=64 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N15 P10 mirror SURVIVED -- a byte-equal fresh run passes P10 [Q24 genuine accepted; F37XMutP910 L2; R37PlanNext B5]
MUTANTS total=1 killed=0 survived=1 invalid=0 null_detected=0
rc=1
```

   → N15 flips SURVIVED ↔ killed exactly with this one fixture (1/1 load-bearing, no second fixture to
   remove).

4) Reference-vs-mutant at the clause level (`R38BatP10b/probe-ref-vs-n15.py`, built the same fixture,
   ran the frozen gate twice and the N15 mutant once):

```
--- REF  rc=0
     P10 ok probe_rerun=byte-equal bytes=37
     defects=0
--- REF2 rc=0
     P10 ok probe_rerun=byte-equal bytes=37
     defects=0
--- N15  rc=1
     P10 DEFECT probe_rerun=byte-equal bytes=37
     defects=1
RECEIPT 'p10b probe: byte-equal under --rerun\n'
```

   The mutant's note is literally the byte-equal note with the verdict flipped, i.e. the mirror firing on
   the pass side, not an incidental second defect. Two reference runs identical → the byte comparison is
   stable.

5) Identity and hygiene:

```
$ sha256sum .../R38BatP10b/battery/p10b.py
cb5df72a5c2faf44916b0b23d5ffe2ac64398515d1bb3080d838c7d7ab90c004
$ grep -nE '/proc|ppid|cmdline|psutil|environ' .../battery/p10b.py   # no match, rc=1
```

   counter's own scan: `sidechannel=0`. `BATTERY … renamed_disagree=0` covers the copied-tree rename
   (spec, receipt and probe are all path-relative). stdlib only (`copy`, `hashlib`, `json`), no
   import-time side effects, one module, one fid prefix `p10b-`.

## Files written

- `.ufo/waves/round-38/build/R38BatP10b/battery/p10b.py` (the deliverable; L1 copies to `plans/battery38/`).
- `.ufo/waves/round-38/build/R38BatP10b/counter-n15.txt` (full run with the module, 65 fixtures).
- `.ufo/waves/round-38/build/R38BatP10b/counter-n15-no-fixture.txt` (load-bearing survival run).
- `.ufo/waves/round-38/build/R38BatP10b/probe-ref-vs-n15.py` (clause-level receipt).
- This report. No lane file, index, jj state or corpus/plans file was written; scratch deleted
  (`rm -rf -- $S`, verified gone; `/tmp` holds no `k38-c1-*`).

## Risks and limits (for the L1)

- **`uv` dependency:** P10 needs `import Bio` to fail in the gate interpreter (it does here, Python
  3.14.8, no Bio) and then `uv run --no-project --with biopython==1.85 python3 -c …`; measured 0.014 s
  from a warm uv cache. Batteries 36/37 already require the same route for their P10 fixtures, so this
  adds no new environmental prerequisite — but a host with Bio installed takes the `sys.executable` arm,
  which I verified is valid for `-c` syntactically, not by running under Bio.
- **Lane-tree coupling:** the accept side inherits battery36/37's dependence on `corpus/knowledge/*.md`
  vs the README index set (P8 requires the two sets equal) and on `corpus/SOURCES.md`/entry bytes. A
  wave-1 sibling that adds the C2 knowledge entry must add its README/`SOURCES` rows in the same landing
  (C2's own V-checks demand it), otherwise this ACCEPT fixture would be wrongly red. Same coupling as
  the existing `P0` genuine fixture.
- Attribution is clause+direction, not intent: the fixture's pass-side P10 is what N15 inverts; no other
  frozen mutant is plausibly killed by it (silence mutants need the reference to print `DEFECT`).
- One fixture, one mutant: N15 is the only P10-pass-side mutant in the frozen list, so no multi-mutant
  consolidation applies.
- No tooling installed or upgraded (nothing needed); pacman untouched.

VERDICT: battery38-p10b-killed-1/1-wrong-0
