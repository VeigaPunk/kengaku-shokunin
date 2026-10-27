# R44RCritBatRedundancy — load-bearing and substitution attack on landed battery44
Seat: R44RCritBatRedundancy (critic, residual round 44). Target: falsify the L1 admission of `plans/battery44`
at landing commit `2a263e5a56ef6d48d06805e1ccd106de5de9ba66` (measured L1: C1 `MUTANTS total=5 killed=5`, C2
`checks=11 defects=0`). This seat attacks C1's battery only; C2 is outside this seat's target.

Frozen read first, in full: `plans/round-44-claims.md` (freeze `5f16ed04`). No frozen artifact was modified.
Counter used: the frozen `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round44_c1_verify.py`; the clone is
`/fast/scratch/hyaku/kengaku-r44/R44RCritBatRedundancy/lane` at `2a263e5a` (verified `rev-parse --show-toplevel`
= the clone, `rev-parse HEAD` = `2a263e5a56ef6d48d06805e1ccd106de5de9ba66`). Every run was executed inside the
round-44 envelope (`claims/envelope.sh`); every envelope in this report reports `local_bin_content_...=unchanged`
(digest `328be01808ba022f` before and after in every run — Q32 satisfied).

Scratch: `S=/fast/scratch/hyaku/kengaku-r44/R44RCritBatRedundancy`. Receipts (full run outputs, all < 6 KB):
`.ufo/waves/round-44/residual/R44RCritBatRedundancy/` (30 files, sha256 listed below).

## 1. Baseline reproduction (the admission I am told to falsify)

Command:
```
envelope.sh $S/env python3 .../plans/round44_c1_verify.py --lane $S/lane --work $S/w
```

Key output (`drop-*` receipts mirror it; full file `$S/results/baseline-out.txt` — copied as receipt `baseline.txt`):
```
ENVELOPE start 20:45:53 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
...
BATTERY fixtures=33 wrong=0 tampered=0 sidechannel=0
MUTANTS total=5 killed=5 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=4/4 order=1/1
PINS-AFTER mismatched=0
PREDICATE C1 pass
ENVELOPE end 20:45:58 exit=0 ... unchanged
```
The admission reproduces exactly (`exit=0`). Killing fixtures at baseline: U5 `u5_short_a-manifest-registry`; U6
`u6_long_a-registry-65`; U7 `u7_twin_a-rowpath-registry`; U9 `u9_worktree_a-registry-wrong-capture`; U14c
`u14c_name_a-draft-suffix`. All attributed `value=differs`.

## 2. Load-bearing: drop each module in turn (10 runs)

Each run: battery dir = `plans/battery44` minus one module (9 modules, 29–31 fixtures). Full counter, `--battery-dir`
(development mode; `PREDICATE C1 n/a`; exit 0 iff wrong/tampered/sidechannel/survived/invalid/unattributed/
null = 0).

| dropped module | run | fixtures | MUTANTS line | killed by (mutant) | exit |
|---|---|---|---|---|---|
| u5_short_a | `drop-u5_short_a.txt` | 30 | 5/5/0 | U5 ← u5_short_b-registry-url-task | 0 |
| u5_short_b | `drop-u5_short_b.txt` | 29 | 5/5/0 | U5 ← u5_short_a-manifest-registry | 0 |
| u6_long_a | `drop-u6_long_a.txt` | 29 | 5/5/0 | U6 ← u6_long_b-registry-80hex | 0 |
| u6_long_b | `drop-u6_long_b.txt` | 30 | 5/5/0 | U6 ← u6_long_a-registry-65 | 0 |
| u7_twin_a | `drop-u7_twin_a.txt` | 30 | 5/5/0 | U7 ← u7_twin_b-url-trio-identical | 0 |
| u7_twin_b | `drop-u7_twin_b.txt` | 30 | 5/5/0 | U7 ← u7_twin_a-rowpath-registry | 0 |
| u9_worktree_a | `drop-u9_worktree_a.txt` | 31 | 5/5/0 | U9 ← u9_worktree_b-registry-erratum-appended | 0 |
| u9_worktree_b | `drop-u9_worktree_b.txt` | 30 | 5/5/0 | U9 ← u9_worktree_a-registry-wrong-capture | 0 |
| u14c_name_a | `drop-u14c_name_a.txt` | 29 | 5/5/0 | U14c ← u14c_name_b-registry-suffix | 0 |
| u14c_name_b | `drop-u14c_name_b.txt` | 29 | 5/5/0 | U14c ← u14c_name_a-draft-suffix | 0 |

Every single-module drop leaves `killed=5 survived=0 wrong=0`, exit 0. **No mutant loses its last killer on any
single-module drop: k = 0.** Kill attribution shifts to the surviving leg of the same pair, proving each mutant's
killers are spread over exactly two modules (a and b).

Pair-drop control (drop both modules of a pair, 5 runs, 8 modules each):

| dropped pair | run | MUTANTS line | survivor |
|---|---|---|---|
| u5_short_a+u5_short_b | `drop2-u5_short_a-u5_short_b.txt` | 4/5, survived=1 | U5 |
| u6_long_a+u6_long_b | `drop2-u6_long_a-u6_long_b.txt` | 4/5, survived=1 | U6 |
| u7_twin_a+u7_twin_b | `drop2-u7_twin_a-u7_twin_b.txt` | 4/5, survived=1 | U7 |
| u9_worktree_a+u9_worktree_b | `drop2-u9_worktree_a-u9_worktree_b.txt` | 4/5, survived=1 | U9 |
| u14c_name_a+u14c_name_b | `drop2-u14c_name_a-u14c_name_b.txt` | 4/5, survived=1 | U14c |

So the killer set of each mutant is partitioned across its two modules; dropping only one leg never flips the
predicate. The "last killer" event only exists at pair granularity (the pair is the unit of demonstration).

## 3. Substitution: dishonest variants (10 single-module runs + 5 pair runs)

Method: for each battery44 module I wrote a variant in scratch (`$S/dis/<module>.py`) that keeps the module's
`FIXTURES` list byte-identical for fid/tool/expect/defects (verified programmatically against the originals),
keeps the contract (build fills the empty dir, argv inside d, no SIDECHANNEL tokens — token scan clean), but
changes the scenario. Edits were made to the build functions only. Then the reason battery dir has 9 original
modules + 1 variant (`sub-<module>/`); pair dirs have both variants (`pair-<a>-<b>/`).

Variant designs (per module):
- **u5_short_a / u5_short_b (U5)** — "drop the capture": rows keep the short anchor tokens but the committed
  capture files / SHA256SUMS / staged blobs they name are never written (rows become unbound).
- **u6_long_a / u6_long_b (U6)** — same for long tokens (unbound rows).
- **u7_twin_a / u7_twin_b (U7)** — "drop the twin capture": the second byte-identical filing is never written;
  rows name one capture only.
- **u9_worktree_a / u9_worktree_b (U9)** — "commit the erratum": the working-tree-only erratum is committed at
  HEAD, so HEAD == working tree.
- **u14c_name_a / u14c_name_b (U14c)** — bad-name flavor change: the claims blobs are named `round-...-claims.txt`
  (extension change) instead of `.md.orig` / `ROUND-...` / `round_44_claims.md`; the guard still fails the regex.

### 3a. Single-module substitution (module replaced, pair left honest)

| substituted module | run | wrong | MUTANTS line | counter notices? |
|---|---|---|---|---|
| u5_short_a | `sub-u5_short_a.txt` | **3** | 5/5/0 | YES — wrong>0 (declared `digest-short`, observed `anchor-unbound`) |
| u5_short_b | `sub-u5_short_b.txt` | **4** | 5/5/0 | YES — wrong>0 |
| u6_long_a | `sub-u6_long_a.txt` | **4** | 5/5/0 | YES — wrong>0 |
| u6_long_b | `sub-u6_long_b.txt` | **3** | 5/5/0 | YES — wrong>0 |
| u7_twin_a | `sub-u7_twin_a.txt` | 0 | 5/5/0 | **NO — admitted** (exit 0; U7 killed by u7_twin_b-url-trio-identical) |
| u7_twin_b | `sub-u7_twin_b.txt` | 0 | 5/5/0 | **NO — admitted** (exit 0; U7 killed by u7_twin_a-rowpath-registry) |
| u9_worktree_a | `sub-u9_worktree_a.txt` | 0 | 5/5/0 | **NO — admitted** (exit 0; U9 killed by u9_worktree_b-registry-erratum-appended) |
| u9_worktree_b | `sub-u9_worktree_b.txt` | 0 | 5/5/0 | **NO — admitted** (exit 0; U9 killed by u9_worktree_a-registry-wrong-capture) |
| u14c_name_a | `sub-u14c_name_a.txt` | 0 | 5/5/0 | **NO — admitted** (exit 0; U14c killed by u14c_name_a-draft-suffix itself) |
| u14c_name_b | `sub-u14c_name_b.txt` | 0 | 5/5/0 | **NO — admitted** (exit 0) |

Note the mechanism for the four admitted U7/U9 cases: the substituted module's fixtures are green under the
reference (observed_rc matches declaration — `wrong=0`), they simply no longer differentiate the mutant; the
kill is carried entirely by the honest pair module. The counter has no per-module "this module demonstrated the
claim" accounting — it aggregates the whole battery, so the dishonest leg is invisible.

The U5/U6 drop-capture variants are *caught* (`wrong>0`): an unbound row prints class `anchor-unbound`
(`anchor_digest_check.py:494-497`) instead of the declared `digest-short`/`digest-long`, so the binding to a
committed capture is part of what the counter verifies — the label alone cannot be faked without a bound row.

### 3b. Pair substitution (both modules of a pair replaced)

| pair | run | wrong | MUTANTS line | outcome |
|---|---|---|---|---|
| u5 (both drop-capture) | `pair-u5_short_a-u5_short_b.txt` | **7** | 4/5, survived=1 | caught (wrong>0 + U5 survives) |
| u6 (both drop-capture) | `pair-u6_long_a-u6_long_b.txt` | **7** | 4/5, survived=1 | caught (wrong>0 + U6 survives) |
| u7 (both drop-twin) | `pair-u7_twin_a-u7_twin_b.txt` | 0 | 4/5, survived=1 | caught via survival (U7 `SURVIVED exhibits=none`) |
| u9 (both commit-erratum) | `pair-u9_worktree_a-u9_worktree_b.txt` | 0 | 4/5, survived=1 | caught via survival (U9 `SURVIVED exhibits=none`) |
| u14c (both .txt names) | `pair-u14c_name_a-u14c_name_b.txt` | 0 | 5/5/0 | **admitted** (exit 0; U14c killed by u14c_name_a-draft-suffix) |

When the demonstration is removed from *both* legs, the counter does notice — as a survivor, not as `wrong`:
the claimed behaviour stops being exhibited, so the kill disappears. The one pair that stays fully admitted is
u14c: renaming the claims blob to `.txt` still fails the same regex guard and still yields exit 2 for the
reference and exit 1 for the mutant; the scenario change lies entirely inside the advertised contract.

## 4. Findings

1. **Redundancy is complete at pair level.** Each of the five mutants has a killer in both modules of its pair;
   no single-module drop flips C1 (`k=0`). The battery's load-bearing unit is the pair.
2. **Single-module dishonesty is undetectable when the pair stays honest.** Replacing u7_twin_a/u7_twin_b
   with single-capture variants, or u9_worktree_a/u9_worktree_b with committed-erratum variants, leaves the
   counter fully green (`wrong=0`, `killed=5`, exit 0). The counter verifies the *observable contract*
   (declared class set, exit codes, span execution, site-record difference) and has no per-module measure of
   whether the module's scenario actually exercises the advertised behaviour. `d = 6` admitted single-module
   dishonest substitutes (u7a, u7b, u9a, u9b, u14a, u14b); 4 were caught (u5a, u5b, u6a, u6b).
3. **The class set is the only fixture semantic the counter checks, but it is enforced.** Unbound rows print
   `anchor-unbound` — not the length classes — so dropping the committed capture is caught. The length label
   (`digest-short`/`digest-long`) cannot be produced without a bound row.
4. **The u14c guard contract is shape-only.** Any name failing `round-(\d+)-claims\.md` exercises the same
   branch (`order_check.py:161`), so substituting a different bad-name flavor is inside the contract; the
   counter cannot (and need not) distinguish which regex failure the fixture uses.
5. **Non-author review remains load-bearing.** The counter's design intent holds: it cannot see scenario intent
   (claims docstring: "the counter cannot see intent — the witness-as-battery control passes"). These results
   quantify that limit: the *pair* is the unit the counter can hold accountable, not the module. A module-level
   reviewer (or a per-mutant per-module kill requirement) would close the single-leg blind spot.

## 5. Evidence

All 30 run outputs are copied verbatim into `.ufo/waves/round-44/residual/R44RCritBatRedundancy/` (sha256
prefixes above; all < 6 KB). Representative envelopes:

```
ENVELOPE start 20:45:53 cwd=/home/vgpnk/Projects/shokunin   (baseline; end 20:45:58 exit=0 unchanged)
ENVELOPE start 20:49:53 cwd=/home/vgpnk/Projects/shokunin   (sub-u5_short_a; end 20:49:57 exit=1 unchanged)
ENVELOPE start 20:50:10 cwd=/home/vgpnk/Projects/shokunin   (sub-u7_twin_a; end 20:50:14 exit=0 unchanged)
ENVELOPE start 20:50:32 cwd=/home/vgpnk/Projects/shokunin   (sub-u14c_name_a; end 20:50:36 exit=0 unchanged)
ENVELOPE start 20:51:32 cwd=/home/vgpnk/Projects/shokunin   (pair-u7_twin_a-u7_twin_b; end 20:51:36 exit=1 unchanged)
```

Every envelope reported `local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged` (Q32).

No tooling was installed; no frozen file, lane file, or corpus/plans tree was touched; nothing was written
outside the seat's residual dir and scratch. Scratch will be removed with `scratch_guard.py safe-rm`.

Checklist (what Main should re-verify, if any): run the drop and substitution batteries against the frozen
counter with `--battery-dir`; confirm the MUTANTS/BATTERY lines match the tables above.

VERDICT: single-module-flips-0-dishonest-substitutes-admitted-6
