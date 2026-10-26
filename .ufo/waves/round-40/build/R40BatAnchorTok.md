# R40BatAnchorTok — battery40/a_tok.py (C1 anchor token-shape fixtures)

Seat: R40BatAnchorTok (executor, wave 1 of round 40). Lane HEAD measured: `3077adbc7145726519f60f01426a5d03381ad444`
(read-only `--shared` clone at `/fast/scratch/hyaku/kengaku-r40/R40BatAnchorTok/lane`; `git -C … rev-parse --show-toplevel`
returned that clone, no commit made there).

Deliverable: `.ufo/waves/round-40/build/R40BatAnchorTok/battery/a_tok.py` — 3 single-behaviour fixtures that kill the
three frozen anchor mutants **A01, A02, A03** (`plans/round40_c1_verify.py:116-133`), each in its declared direction.
sha256 `c24f954ad289c926be316e14bde4b9ad68646baece2061a24b18521653b6418c` (byte-identical copy placed in the clone at
`plans/battery40/a_tok.py` for the full run; recomputed after the run, unchanged).

Nothing frozen was touched: `PINS total=3 mismatched=0` before and `PINS-AFTER mismatched=0` after every run below, and
the lane's `plans/`, `corpus/`, index and jj state were never written — all edits are inside the scratch clones.

## What the module does (one behaviour per fixture)

Every fixture takes a fresh `ctx.clone(d / "lane")` (a `--shared` clone of the read-only lane clone), rewrites **one**
existing `corpus/SOURCES.md` anchor claim in the clone's work tree (no commit: the tool reads `SOURCES.md` from the work
tree — `plans/anchor_digest_check.py:398` `text = (lane / "corpus/SOURCES.md").read_text(...)` — and evidence from
`HEAD`), and returns `["--lane", str(lane)]`. `_edit` raises if the token it must rewrite is not present exactly once, so
a future SOURCES drift fails loudly as a build error instead of silently producing a non-killing fixture.

| fid | mutant (tool branch it changes) | behaviour demonstrated | reference on the fixture | mutant on the fixture | direction exhibited |
|---|---|---|---|---|---|
| `a_tok-upper-anchor` | A01: `HEX64` `[0-9a-f]{64}` → `[0-9a-fA-F]{64}` | a 64-hex anchor token in uppercase is not "64 lowercase hex": `digest-uppercase` | rc=1, `digest-uppercase` | rc=1, `digest-unknown` (class gone) | `silence` |
| `a_tok-abbrev-7hex` | A02: abbreviation floor `8` → `1` | a 7-hex abbreviation that *does* resolve as a prefix is below the 8-hex floor: `abbrev-unresolved` | rc=1, `abbrev-unresolved` | rc=0, no defect | `rc-silence` |
| `a_tok-abbrev-64hex` | A03: abbreviation ceiling `63` → `64` | a full 64-hex digest followed by `…` is not an abbreviation (8-63 only): `abbrev-unresolved` | rc=1, `abbrev-unresolved` | rc=0, no defect | `rc-silence` |

Sources of the three edits (all pre-existing lane content at HEAD, each string unique in `SOURCES.md`, verified by the
build-time `count(old) != 1` guard):

- S111 anchor cell, `corpus/SOURCES.md:126`, carries `sha256 526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37`;
  the fixture uppercases that digest (the round-39 witness `R39PlanNext/h_anchor.py:104` `X01-upper`).
- S036 anchor cell, `corpus/SOURCES.md:58`, carries `sha256 afaae9dd…`; the 7-hex fixture rewrites it to
  `sha256 afaae9d…` (`h_anchor.py:109` `X03-abbrev-7hex`) and the 64-hex fixture rewrites it to the **full** digest of
  `corpus/evidence/attrib-r23-stream.log` followed by `…` (`h_anchor.py:111-117` `X05-abbrev-64hex-ellipsis`); that file
  hashes to `afaae9ddaf4deda0095c2e7ad39c6cb63236d72c812ca2fcd9ab18c42eef8131` (`sha256sum`), i.e. the abbreviation in
  the row is the true 8-hex prefix of the capture digest — which is why A02 (floor 8→1) resolves it and goes silent
  while A03 (ceiling 63→64) also resolves the 64-hex+`…` form.

Reference results measured independently of the counter's own renderer (`direction-probe.txt`, scratch clone per case,
mutant files generated from the frozen `old -> new` cells of `plans/round40_c1_verify.py:116-133`):

```
MUTPATH A01 sha256=7379c272db705142
MUTPATH A02 sha256=77200d307537fa2d
MUTPATH A03 sha256=5339c4dd2fd1fdce
REF     sha256=11bb2cad87be1c29
CASE a_tok-upper-anchor mutant=A01 ref_rc=1 ref_classes=digest-uppercase mut_rc=1 mut_classes=digest-unknown
CASE a_tok-abbrev-7hex mutant=A02 ref_rc=1 ref_classes=abbrev-unresolved mut_rc=0 mut_classes=-
CASE a_tok-abbrev-64hex mutant=A03 ref_rc=1 ref_classes=abbrev-unresolved mut_rc=0 mut_classes=-
```

`REF sha256=11bb2cad…` matches the counter's pin `11bb2cad87be…`, so the mutants were built from the pinned bytes.
Each fixture declares exactly the reference result above (`expect=reject` = rc 1; `defects` = the single class token),
and the counter confirms it (`wrong=0`).

## Development run (three mutants, my battery dir) — required command and output

```
$ python3 plans/round40_c1_verify.py --lane "$S/lane" \
    --battery-dir …/build/R40BatAnchorTok/battery --only A01,A02,A03 --work "$S/w"
PINS total=3 mismatched=0
FIXTURE a_tok-upper-anchor tool=anchor expect=reject declared=digest-uppercase observed_rc=1 observed=digest-uppercase ok
FIXTURE a_tok-abbrev-7hex tool=anchor expect=reject declared=abbrev-unresolved observed_rc=1 observed=abbrev-unresolved ok
FIXTURE a_tok-abbrev-64hex tool=anchor expect=reject declared=abbrev-unresolved observed_rc=1 observed=abbrev-unresolved ok
MUTANT A01 anchor silence killed by=a_tok-upper-anchor -- plans/anchor_digest_check.py:88-89 'any other anchor token must be exactly 64 lowercase he
MUTANT A02 anchor rc-silence killed by=a_tok-abbrev-7hex -- plans/anchor_digest_check.py:84-85 'a defect (`abbrev-unresolved`) unless its hex is 8-63 
MUTANT A03 anchor rc-silence killed by=a_tok-abbrev-64hex -- plans/anchor_digest_check.py:84-85 (as A02: 'its hex is 8-63 lowercase hex digits')
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

Exit 0. Every FIXTURE line `ok`; `wrong=0 tampered=0 sidechannel=0`, `null_detected=0`, `invalid=0`; each of A01, A02,
A03 killed by the stated fid. Receipts: `dev-A01A02A03-run1.txt`; a second identical invocation is byte-equal
(`diff dev-A01A02A03-run1.txt dev-A01A02A03-run2.txt` → `BYTE-EQUAL rerun`), so the fixtures are deterministic.

## Load-bearing table (each fixture removed in turn, and each run alone)

Full table in `ablation-table.txt`; the `MUTANT` lines show a clean one-fixture-per-mutant attribution (no cross-kills):

| battery contents | A01 | A02 | A03 |
|---|---|---|---|
| all three (module as delivered) | killed by `a_tok-upper-anchor` | killed by `a_tok-abbrev-7hex` | killed by `a_tok-abbrev-64hex` |
| minus `a_tok-upper-anchor` | **SURVIVED** `exhibits=none` | killed | killed |
| minus `a_tok-abbrev-7hex` | killed | **SURVIVED** `exhibits=none` | killed |
| minus `a_tok-abbrev-64hex` | killed | killed | **SURVIVED** `exhibits=none` |
| only `a_tok-upper-anchor` | killed | SURVIVED | SURVIVED |
| only `a_tok-abbrev-7hex` | SURVIVED | killed | SURVIVED |
| only `a_tok-abbrev-64hex` | SURVIVED | SURVIVED | killed |

So each of the three fixtures is load-bearing for exactly one frozen mutant, and no fixture is redundant. In all seven
runs `BATTERY … wrong=0 tampered=0 sidechannel=0` (the fixture trees are unchanged after the tool runs) and no mutant
exhibited a direction other than its declared one (`exhibits=none` on every survivor).

## Full default counter with the module in `plans/battery40/`

```
$ cp a_tok.py "$S/lane/plans/battery40/a_tok.py"
$ python3 plans/round40_c1_verify.py --lane "$S/lane" --work "$S/w2"
PINS total=3 mismatched=0
FIXTURE a_tok-upper-anchor tool=anchor expect=reject declared=digest-uppercase observed_rc=1 observed=digest-uppercase ok
FIXTURE a_tok-abbrev-7hex tool=anchor expect=reject declared=abbrev-unresolved observed_rc=1 observed=abbrev-unresolved ok
FIXTURE a_tok-abbrev-64hex tool=anchor expect=reject declared=abbrev-unresolved observed_rc=1 observed=abbrev-unresolved ok
MUTANT A01 anchor silence killed by=a_tok-upper-anchor -- …
MUTANT A02 anchor rc-silence killed by=a_tok-abbrev-7hex -- …
MUTANT A03 anchor rc-silence killed by=a_tok-abbrev-64hex -- …
MUTANT A06 anchor rc-mirror SURVIVED exhibits=none -- …
MUTANT A08 anchor rc-silence SURVIVED exhibits=none -- …
MUTANT A09 anchor rc-silence SURVIVED exhibits=none -- …
MUTANT A15 anchor rc-silence SURVIVED exhibits=none -- …
MUTANT A17 anchor rc-mirror SURVIVED exhibits=none -- …
MUTANT A21 anchor rc-mirror SURVIVED exhibits=none -- …
MUTANT A22 anchor rc-mirror SURVIVED exhibits=none -- …
MUTANT A27 anchor silence SURVIVED exhibits=none -- …
MUTANT L01 ledger error SURVIVED exhibits=none -- …
MUTANT L05 ledger rc-silence SURVIVED exhibits=none -- …
MUTANT L06 ledger rc-silence SURVIVED exhibits=none -- …
MUTANT L11 ledger error SURVIVED exhibits=none -- …
MUTANT L14 ledger rc-silence SURVIVED exhibits=none -- …
MUTANT L15 ledger rc-silence SURVIVED exhibits=none -- …
MUTANT L21 ledger error SURVIVED exhibits=none -- …
MUTANT O04 order rc-silence SURVIVED exhibits=none -- …
MUTANT O12 order rc-error SURVIVED exhibits=none -- …
MUTANT O14 order error SURVIVED exhibits=none -- …
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=21 killed=3 survived=18 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
```

(`-- ` tails elided only where they repeat the frozen `adv` sentences; full text in `full-counter.txt`.) The 18
survivors are the other seats' mutants — no `plans/battery40` module except this one exists in my clone — so
`PREDICATE C1 fail` here is the expected partial state of wave 1, not a defect of `a_tok.py`: my three fixtures
contribute `killed=3` with `wrong=0`, `invalid=0`, `null_detected=0`, `tampered=0`, `sidechannel=0` and pins intact.

## Notes, risks, blockers

- `sidechannel=0`: the module carries none of the counter's `SIDECHANNEL` tokens (the scan is substring, case-insensitive,
  over the whole source); it uses only `ctx.clone` / plain `pathlib` text edits, no subprocess, no git writes.
- Each build clones the lane twice-nested (`--shared` of the counter's own clone); `--lane` is `d/lane`, so every absolute
  argv path lies inside the counter-owned fixture dir (`path_ok` holds by construction).
- Risk (not a blocker): the fixtures pin three literals of lane state — the S111 digest, the S036 abbreviation
  `sha256 afaae9dd…`, and the capture file `corpus/evidence/attrib-r23-stream.log`. If integration edits those (a C2 row
  insertion elsewhere does not), `_edit` raises and the counter reports `SETUP … failed to build`, which is loud, not
  silent. Both tokens are present exactly once at `3077adbc` (the build guard ran 3/3 in every run above).
- Risk: fixture intent is demonstrated for the reference result and the three mutants only; a kill records the declared
  direction, not broader semantic correctness (the freeze's own limit, `plans/round-40-claims.md` "Limits named now").
- No blockers. No tool installs were needed (python3 stdlib + `bwrap` 84,464-byte `/usr/bin/bwrap` already present); no
  pacman/uv/npx transaction was run. Scratch `/fast/scratch/hyaku/kengaku-r40/R40BatAnchorTok` was removed after the
  receipts above were copied into this directory.

VERDICT: battery40-a_tok-killed-3/3-wrong-0
