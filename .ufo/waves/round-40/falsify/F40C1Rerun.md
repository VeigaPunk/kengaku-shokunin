# F40C1Rerun — C1 re-measurement at tip ec1005a + load-bearing table

Seat: F40C1Rerun (executor, wave 2 FALSIFY). Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`,
tip `ec1005a2a28bc5cfdde7723374368ed4cc956eed` (clean clone, `git status --porcelain` = 0 lines).
Counter under test: `plans/round40_c1_verify.py` (unmodified), battery `plans/battery40/` (7 modules, 21 fixtures).
Frozen claim: `PINS total=3 mismatched=0` … `MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0` …
`PREDICATE C1 pass` (`plans/round40_c1_verify.py:8`, `TOTAL = 21` at `plans/round40_c1_verify.py:225`).

Host safety: every invocation below ran inside the ruling sandbox
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent`
with `--lane`/cwd on my own scratch clone under `/fast/scratch/hyaku/kengaku-r40/F40C1Rerun/` (nvme), `TMPDIR` inside that scratch.
Nested `bwrap` (the counter re-sandboxes every build child and every tool run) was probed first: `bwrap … bwrap … /bin/true` → `nested_rc=0`.
No PACMAN transaction, no install, no host service, no write outside scratch + this report dir.
Environment measured: `bubblewrap 0.13.1`, `git version 2.56.0`, `Python 3.14.8`; the three tool pins hash exactly to the
counter's `PINS` (`11bb2cad…`, `853bcb2a…`, `948d5e1d…`).

## R1 — Two clean-clone reruns are byte-identical to each other AND to the landed C1 block

```
$ PYTHONHASHSEED=0  bwrap … python3 plans/round40_c1_verify.py --lane . --work "$S/w1" --jobs 1   # 121.42s, rc=0
$ PYTHONHASHSEED=77 bwrap … python3 plans/round40_c1_verify.py --lane . --work "$S/w2" --jobs 8   # 53.26s, rc=0
```
Both printed `PINS total=3 mismatched=0`, `BATTERY fixtures=21 wrong=0 tampered=0 sidechannel=0`,
`MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass`, exit 0.

```
898c2ce492fe440e69130fe77fd6de1c08382ef05e053a2c16a015dba5dce738  receipts/c1-seed0-jobs1.txt
898c2ce492fe440e69130fe77fd6de1c08382ef05e053a2c16a015dba5dce738  receipts/c1-seed77-jobs8.txt
898c2ce492fe440e69130fe77fd6de1c08382ef05e053a2c16a015dba5dce738  receipts/c1-frozen-body.txt   # frozen block, measure-final.txt:4-50
```
`diff -u receipts/c1-frozen-body.txt receipts/c1-seed0-jobs1.txt` → no output; same for `c1-seed77-jobs8.txt`.
The frozen C1 block was extracted with `sed -n '3,51p' .ufo/waves/round-40/integrate/measure-final.txt` (49 lines: `$ python3 …`
invocation line, 47 output lines, `exit=0`) and stripped to its 47 output lines here.

Drift check (the measurement header says `TIP ec17216844585d0…`, the assignment names `ec1005a…`):
`git -C $S/lane diff --stat ec17216844585d0fecde9f1d4c4be0b78a3bf76f ec1005a2… -- plans/` → **empty**; `ec1005a` is the single
child commit of `ec17216`. The counter, the battery and all three tools are byte-identical between the measured commit and the tip,
so the frozen block's inputs transfer exactly. Measurement and tip therefore agree; the header's `TIP` line is a provenance
label, not a drift.

## R2 — The requested seeds never reach a child process (protocol gap, measured; result unaffected)

`PYTHONHASHSEED` does not appear anywhere in the counter: `grep -n 'PYTHONHASHSEED\|PYTHONHASH' plans/round40_c1_verify.py` → no output.
Both child environments are rebuilt from literals, so the caller's seed is dropped:
`plans/round40_c1_verify.py:362-368` (`def env`, tool runs) and `plans/round40_c1_verify.py:423-425` (build child).
Measured, not inferred: a probe battery module (`$S/probe-battery/probe_env.py`, scratch only, writes its own `os.environ`) run as
`PYTHONHASHSEED=77 … --battery-dir $S/probe-battery` produced
```
PYTHONHASHSEED=None
KEYS=HOME,LANG,LC_ALL,PATH,PWD,PYTHONDONTWRITEBYTECODE,TMPDIR
```
Conclusion for the claim: the two runs above compared **two arbitrary (random) seeds**, not literally 0 and 77. To close that gap I ran a
scratch copy of the counter with `PYTHONHASHSEED` forwarded into both env literals (`$S/probe-counter/c1_seed.py`; the frozen counter and
the pinned tools were not touched) at the two requested seeds:

```
$ PYTHONHASHSEED=0  bwrap … python3 $S/probe-counter/c1_seed.py --lane $S/lane --work $S/w3 --jobs 1   # 160.12s, rc=0
$ PYTHONHASHSEED=77 bwrap … python3 $S/probe-counter/c1_seed.py --lane $S/lane --work $S/w4 --jobs 8   #  77.81s, rc=0
898c2ce492fe440e69130fe77fd6de1c08382ef05e053a2c16a015dba5dce738  receipts/c1-seedfwd0-jobs1.txt
898c2ce492fe440e69130fe77fd6de1c08382ef05e053a2c16a015dba5dce738  receipts/c1-seedfwd77-jobs8.txt
```
Both are byte-identical to R1 and print `PREDICATE C1 pass`. So the byte-equality is not an artefact of the dropped seed: with the seed
genuinely delivered to every build child and every tool run, 0 vs 77 and `--jobs 1` vs `--jobs 8` still yield the same 5 666 bytes.
Residual gap (reported, not fatal): the *landed* counter cannot be run "with PYTHONHASHSEED=0" in the literal sense; any future receipt
that names a seed should say it names the counter process only.

## R3 — Do-nothing control: an empty battery fails, and it fails only on the kill count

```
$ rm -rf $S/ctl/none/lane/plans/battery40 ; bwrap … round40_c1_verify.py --lane . --work … --jobs 4   # rc=1
PINS total=3 mismatched=0
BATTERY fixtures=0 wrong=0 tampered=0 sidechannel=0
MUTANTS total=21 killed=0 survived=21 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
```
Every term except `killed` still reads clean with zero fixtures: `fixtures=<n>` carries no floor, `wrong=0` is vacuously true, and the only
anti-vacuity in the predicate is `killed == TOTAL`. This is the calibration shape wave 1 attacked (a dishonest battery still scores 21/21);
my rerun neither adds nor removes that exposure — it only confirms the predicate is not satisfiable by doing nothing.

## R4 — Load-bearing table: 7/7 modules, 21/21 mutants

Method: one clean clone per configuration (`git clone --no-local` of the tip, `rev-parse --short HEAD` = `ec1005a`), one module file
deleted (`rm plans/battery40/<m>.py`), counter re-run in the same sandbox with `--jobs 4`; the do-nothing run deleted the whole directory.
All 8 runs exited 1 with `wrong=0 tampered=0 sidechannel=0 invalid=0 null_detected=0`, i.e. every *remaining* fixture still declares
correctly and only the removed module's mutants change verdict.

| module removed | fixtures | mutants that flip to SURVIVED | flipped |
|---|---|---|---|
| (none — whole battery removed) | 0 | all 21 | 21 |
| `a_tok` | 3 | A01, A02, A03 | 3 |
| `a_row` | 3 | A06, A08, A09 | 3 |
| `a_bind` | 3 | A15, A17, A27 | 3 |
| `a_man` | 2 | A21, A22 | 2 |
| `l_rows` | 4 | L05, L06, L14, L15 | 4 |
| `l_refuse` | 3 | L01, L11, L21 | 3 |
| `o_gate` | 3 | O04, O12, O14 | 3 |

Per-module flipped counts: `receipts/control-*.txt`, e.g. `control-a_man.txt` = 19 killed / 2 survived.

Properties measured from that table:
- **7/7 modules are load-bearing**; removing any one flips at least one mutant, removing all flips all 21.
- **No redundancy and no cross-module fallback**: each mutant flips in exactly one removal, and every survivor line reads `exhibits=none`
  (no other direction is exhibited anywhere in the residual battery). Removing one module never leaves a mutant killed by another module.
- **Killer/fixture bijection at the tip**: `grep '^MUTANT ' receipts/c1-seed0-jobs1.txt` gives `distinct_killers=21`, `distinct_ids=21`
  — each of the 21 fixtures is the unique killer of exactly one mutant (`a_tok-upper-anchor <- A01` … `o_gate-claims-bak-name <- O14`).
- **Delta is confined to the module**: byte-diff of each control against the full receipt changes exactly
  `3·(fixtures removed) + 3` lines (fixture lines + that module's MUTANT lines + BATTERY/MUTANTS/PREDICATE); e.g. `a_man` 12, `a_tok` 15,
  `l_rows` 18. No unrelated fixture or mutant line moves.
- **Fragility implied (axis note, not a defect of the claim)**: because the mapping is bijective, losing a *single fixture* inside a module
  would break the same calibration as losing the module; my control only removes whole modules, so single-fixture loss is untested here.

## R5 — What this rerun does not prove

- It does not re-adjudicate the wave-1 gameability findings (self-reading ledger body, PATH git shim, relative argv + symlink,
  `.lock` names). The mechanisms those reports name are still present at the tip: `fingerprint()` skips `.git/index` **and any name ending
  `.lock`** (`plans/round40_c1_verify.py:317`), and `sidechannel` remains the token heuristic over battery sources. Admission still rests on
  the frozen predicate **plus** non-author review, as the claims file states.
- The tool runs keep the caller's `PATH`/`HOME` (documented limit, `plans/round40_c1_verify.py:63-65`); my runs supplied the
  ruling's read-only `~/.local/bin` so the ledger's `uv`-based R35-D1 check stayed reachable, and all ledger fixtures passed.
- Directory-only deletions were performed on scratch clones; no lane file, index, jj state or fleet-root path was written.

## Receipts (all under `.ufo/waves/round-40/falsify/F40C1Rerun/`)

`c1-seed0-jobs1.txt`, `c1-seed77-jobs8.txt`, `c1-seedfwd0-jobs1.txt`, `c1-seedfwd77-jobs8.txt`,
`c1-frozen-block-measure-final.txt` (raw 49-line extraction), `c1-frozen-body.txt` (47 output lines),
`control-none.txt`, `control-a_tok.txt`, `control-a_row.txt`, `control-a_bind.txt`, `control-a_man.txt`,
`control-l_rows.txt`, `control-l_refuse.txt`, `control-o_gate.txt` (+ `.err`, all empty),
`probe-build-child-run.txt`, `probe-build-child-env.txt`.
Scratch `/fast/scratch/hyaku/kengaku-r40/F40C1Rerun` deleted after copying.

VERDICT: c1-rerun-pass-byte-equal-yes-loadbearing-7/7
