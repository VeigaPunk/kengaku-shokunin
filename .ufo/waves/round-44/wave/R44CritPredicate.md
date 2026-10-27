# R44CritPredicate — Q-sentence check (round 44 wave, critic)

Seat: R44CritPredicate. Date: 2026-10-26. Lane clone: `/fast/scratch/hyaku/kengaku-r44/R44CritPredicate/lane`
(git clone -q --shared of the source repo; `git rev-parse --show-toplevel` = the clone). All runs under the
round-44 envelope `claims/envelope.sh`; all envelopes end `local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`.

## 1. Same sentence, plan vs docstring (verbatim check)

Commands (normalized-whitespace slice compare, `python3 -` in the source repo):

```
C1 claims==docstring: True
C2 claims==docstring: True
```

The frozen sentences in `plans/round-44-claims.md` (C1 lines 47–50; C2 lines 92–93) are byte-equal (modulo
whitespace) to the docstring sentences in `plans/round44_c1_verify.py:10-15` and `plans/round44_c2_verify.py:8-10`.
No wording drift in the predicate sentences themselves.

## 2. Same condition in code — printed labels vs asserted condition

Every labeled line the sentence names is emitted by the counter:

- C1 (`round44_c1_verify.py`): `PINS total=… mismatched=…` (781), `BATTERY fixtures=… wrong=… tampered=… sidechannel=…`
  (914), `MUTANTS total=… killed=… survived=… invalid=… null_detected=… unattributed=…` (916–917),
  `MUTANTS-BY-TOOL …` (918), `PINS-AFTER mismatched=…` (922), `PREDICATE C1 pass|fail` (932), exit 0/1 (933).
- C2 (`round44_c2_verify.py`): per-check `Vn ok|DEFECT` (547), `checks=… defects=…` (548), `PREDICATE C2 pass|fail`
  (549), exit 0/1 (550).

`good` (C1:929-931) asserts: `not mism`, `not after`, `len(MUTANTS)==TOTAL`, `floors_ok` (per-tool
[killed==floor] for `anchor=4/4`, `order=1/1`), `wrong==0`, `tampered==0`, `side==0`, `killed==TOTAL`, `survived==0`,
`invalid==0`, `unattributed==0`, `null_detected==0`. C2 `defects==0` sums ok/defect per V.

### D1 — C1 `PINS total=2` is printed, never asserted
`PINS total={len(PINS)}` (line 782) prints the literal, but the `good` conjunction contains no
`len(PINS) == 2` term. If `PINS` held a different number of all-matching pins, the counter would print
`PINS total=3 mismatched=0 … PREDICATE C1 pass`, exit 0 — a state the frozen sentence forbids, which the counter's
own condition would still pass. Literal printed, not enforced. (The other numeric literals of the sentence
— `TOTAL=5` via `len(MUTANTS)==TOTAL`, per-tool floors, `mismatched=0`, `PINS-AFTER mismatched=0` — are enforced.)

### D2 — C2 `checks=11` is printed, never asserted
`checks={len(checks)}` (line 548) prints the literal, but the pass condition is only `defects == 0` (549–550).
Dropping a V from the `checks` list would print `checks=10 defects=0` and still exit 0 — again a state the frozen
sentence forbids. The 11-V inventory is not asserted; the label alone carries it.

### D3 — note, not drift: C1 prints an extra `ADVERTISED direct=5 indirect=0 none=0` line (920)
between `MUTANTS-BY-TOOL` and `PINS-AFTER`. The committed controls (e.g. `control-c1-nothing.txt:11-12`) show the
same interleaving and were accepted; a strict consecutive-line matcher would need to skip unknown labels.

### D4 — seat-spec clause outside the frozen predicate: “source: first line citing S138” is un-enumerated
The admission spec asks for a `source:` **first line** citing S138. `v9` (round44_c2_verify.py:308-311) checks
every spec row id appears outside `source:` lines, and gate `c_provenance` (pkg_gate.py:211-231) requires one
pinned-URL `source:` line per row id plus `verified-at:`/`recheck:` and `## Negative space` — none of it enforces
the first line or that S138 sits on it. Minor, and outside the frozen predicate sentence (which does not mention
it), so not counted in the drift tally.

### D5 — C1 “measured on a clean clone” is procedural
Neither counter verifies the lane is a clean clone. C2 inherits the gate's `c_clean_tree` (P9, `--require-clean-tree`)
so a dirty tree fails V2; C1 has no equivalent cleanliness check (PINS read the working tree; an uncommitted tool
edit would surface as a pin mismatch only if it changed bytes).

## 3. Cheap do-nothing controls beyond the committed ones — after-states reached

Built a synthetic lane `synth/` carrying byte-identical copies of the two tools (digests equal the frozen PINS:
`11bb2cad…`, `948d5e1d…`; verified by sha256sum) and my own battery modules; ran the counter in default (non-dev)
mode so the real `PREDICATE C1` is exercised.

### Control A — valid battery module that builds zero fixtures (`FIXTURES = []`)
`z_empty.py` under `synth/plans/battery44/`. Envelope run:
```
ENVELOPE … python3 plans/round44_c1_verify.py --lane …/synth --work …/wA
…
BATTERY fixtures=0 wrong=0 tampered=0 sidechannel=0
MUTANTS total=5 killed=0 survived=5 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=0/4 order=0/1
PREDICATE C1 fail
ENVELOPE end … exit=1 … unchanged
```
Receipt: `wave/R44CritPredicate/ctl-A.txt`, sha256 `7951f05f8194afe139743e7c3ccd0eabb34382cc73ecf7b9413301b5ae794bc7`.

### Control B3 — cheapest genuinely-accepted do-nothing fixture
One anchor fixture, `expect=accept`, `defects=[]`, building an empty `corpus/SOURCES.md` + one committed evidence file
(`corpus/evidence/round44/x.txt`) and argv `["--lane", "."]`. Reference exit 0, empty class set → `FIXTURE … ok`,
`wrong=0`. The unmodified tool's guard is: without a committed file under `corpus/evidence/` the anchor exits 2
(`USAGE: no committed file under corpus/evidence/ — cannot resolve any digest`, anchor_digest_check.py run rc=2),
so an empty-repo “accept” fixture is actually `wrong=1` — a useful calibration fact for battery authors. With the
evidence file:
```
FIXTURE triv-accept tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=0
MUTANTS total=5 killed=0 survived=5 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=0/4 order=0/1
PREDICATE C1 fail
ENVELOPE end … exit=1 … unchanged
```
Receipt: `wave/R44CritPredicate/ctl-B3.txt`, sha256 `1f92c90087a670a4be904bd8939b11d3c12470b0a4aede569749ba04dcc7dcab`.

### Control C2 — clean-clone do-nothing at current tip
`round44_c2_verify.py --lane …/lane` on the clone (receipt now committed: gate P2/P10 ok, V8 ORDER PASS):
```
V1 ok listed=11 bad=0 extra=0
V2 DEFECT … gate: P3 DEFECT no '## Located quotes' section … P6 DEFECT rows=9 bad=9 … P7 DEFECT entry unreadable …
V3 DEFECT rows=9 bad=[…S138:row … S146:row]
V4/V7/V9/V10/V11 DEFECT (entry/receipt related)
V5 ok probe=frozen dry_byte_equal=True ; V6 ok census_exit=0
checks=11 defects=7
PREDICATE C2 fail
ENVELOPE end … exit=1 … unchanged
```
Receipt: `wave/R44CritPredicate/ctl-C2.txt`, sha256 `5496fdcd2659fa764f59abd27801932c461f65d7ad0985d37b03839231b6d51e`.

All three controls reach only the fail state (exit 1); none reaches pass or a mislabeled after-state. The mapped
drifts D1/D2 are label-vs-condition gaps, not reachable pass holes.

## 4. Axis naming (surface vs number)

- C1 “calibration”: a number axis — the residual count of frozen unmutated advertised behaviours (5 → 0), bound
  literally (`TOTAL`, `FLOORS`) and made non-vacuous (no-mutants control prints fail). Named as a count; consistent.
- C2 “coverage”: surface-typed (“tenth grader class F1 constant-compare”), and the claims themselves say it carries
  no novelty claim and coverage stays capped at 7, judged on the counter. The counter's number (11 checks, defects=0)
  is asserted except the `checks=11` literal (D2). Naming is honest; the only number-vs-label weakness is D2.

## VERDICT: predicate-drift-2-cheap-control-reaches-no
