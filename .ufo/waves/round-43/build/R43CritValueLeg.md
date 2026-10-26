# R43CritValueLeg — critic seat report (kengaku round 43, WAVE 1)

Seat: `R43CritValueLeg` (critic). Scope: attack the new value-attribution leg g of
`plans/round43_c1_verify.py` (TRACER: `note`, `digest`, `K43_SPAN`; main: the two reference traces and
`SITE_EQUAL`). Nothing frozen was changed: the lane was only read; all measurements ran from scratch
`/fast/scratch/hyaku/kengaku-r43/R43CritValueLeg` under the round-43 envelope; the frozen counter was
imported read-only (`importlib` load of `plans/round43_c1_verify.py`) and the frozen `TRACER` constant was
used verbatim for the stability/effect runs (copy for raw-dump diagnosis lives only in scratch).

Measurement harness: `h.py` (in this seat dir; sha256 `0bce0cd716db3c6b9fbb5eeb0efaac9d48aba4aae1df75e99fab2a163938295d`).

---

## 1. Reference double-trace record stability (task 1)

Command (envelope-wrapped; full receipt `stable.txt`):
```
envelope.sh $S/env python3 h.py stable --rootbase $S/w1b
```
Method: for each of the 6 `w_near.py` fixtures (4 anchor: wit-long-row, wit-green-erratum,
wit-slashed-name-url, wit-short-commit-url; 2 order: wit-late-claims-edit, wit-p2-excuse), the reference
tool was traced twice with the union of the tool's mutant spans, under four arms: jobs=1/seed=0, jobs=8/
seed=0, jobs=1/seed=12345, and a second scratch root (seed=0/jobs=1). Each traced run returns
(rc, classes, executed-line set, site-record tuple).

Result: **24/24 identical** (`all_same=True` on every line; 0 `all_same=False`). The site record is stable
within a root under all variations: concurrency (`--jobs` 1 vs 8), `PYTHONHASHSEED` 0 vs 12345, and
scratch root. The double-trace stability test inside the counter (lines 815‑816) therefore never misfires on
these fixtures.

```
ENVELOPE start 19:14:24 cwd=/home/vgpnk/Projects/shokunin
STABLE j1-s0 wit-long-row rc_cls_eq=True lines_eq=True sites_eq=True n_sites=2 all_same=True
...
STABLE j1-s0-r2 wit-p2-excuse rc_cls_eq=True lines_eq=True sites_eq=True n_sites=5 all_same=True
ENVELOPE end 19:14:28 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

### Per-run-path normalization gap (cross-root)
The RUN regex only normalises `/(?:rtmp/t|work/w)[0-9]{6}`; the scratch-root prefix is not normalised.
Comparing the *same* fixture's reference records across two different scratch roots (from `stable.txt`):
```
CROSSROOT wit-long-row sites_eq=False n_a=2 n_b=2
CROSSROOT wit-green-erratum sites_eq=False n_a=8 n_b=8
CROSSROOT wit-slashed-name-url sites_eq=False n_a=3 n_b=3
CROSSROOT wit-short-commit-url sites_eq=False n_a=3 n_b=3
CROSSROOT wit-late-claims-edit sites_eq=True n_a=7 n_b=7
CROSSROOT wit-p2-excuse sites_eq=True n_a=5 n_b=5
```
All 4 anchor fixtures' records differ across roots; the 2 order fixtures' records do not. The distinguishing
text is the root-directory leaf: with raw-dump diagnosis of `wit-long-row` site `477>478`, the only textual
difference between the two roots' digested locals is `'A'` vs `'B'` (root dirs `rA`/`rB`):
```
site 1 A 477>478:6f76125ea162515c B 477>478:75876ec8eb13f7cf
   replace A: 'A' B: 'B'
```
**Consequence:** a record is not canonical across scratch contexts. In the counter as frozen this cannot
fabricate a leg-g pass, because the mutant trace and the two reference traces run in the **same** root
(same fixture dirs, same embedded path text), so the path leak cancels. It would become a spurious-difference
source only if a future revision ever compared records produced under different `--work` roots (then every
span-executing hit would trivially satisfy leg g). No within-root spurious difference was found:
**spurious = 0**.

## 2. Module-level span vacuity (task 2) — NA18 `URL_RAW`, NO7 `EXECUTED_EXCUSE`

Command (envelope-wrapped; receipts `rawdump-NA18/`, `rawdump-NO7/`):
```
envelope.sh $S/env python3 h.py spans --rootbase $S/w2c
```
On this host (python 3.14.8), with the frozen tracer, the module-level span records **differ on every
fixture** — leg g is not vacuous here:

| mutant | span | ref record | mut record | ref double-run | all fixtures |
|---|---|---|---|---|---|
| NA18 `URL_RAW` | L154-L155 | `154>156:d70e2ec685716898` | `154>156:103ab7272e3cc3ee` | stable | 4/4 differ |
| NO7 `EXECUTED_EXCUSE` | L60 | `60>63:e4e91f90ebc9341a` | `60>63:0bee18019de26092` | stable | 2/2 differ |

The discriminating record: the next-event digest after the span is taken **after** the module-level store,
so it includes the bound global. `re.Pattern.__repr__` in CPython 3.14 prints the pattern source
(`re.compile('…')`), so the mutation changes the digest by exactly one character (NA18: `{7,40}` →
`{4,40}`; NO7: `(?:: \S+)?` removed). Verified by raw-dump diff: the only differing substring between ref
and mut raw globals text for NA18 is `7`→`4`; for NO7 the deletion of `(?:: \S+)?`.

Fragility/limits of that discriminator:
- `re.Pattern.__repr__` was address-only (`<re.Pattern object at 0x…>`) on Python ≤3.12 and the ADDR
  normalisation collapses it to a constant. Simulating that repr (stripping every `re.compile('…')` source
  from the raw digests) makes ref and mut digests **equal on every fixture** for both NA18 and NO7
  (stripped_equal True, digest `92c0d7a32058b515` / `bddb8c2aa38eed91` for both sides) — i.e. leg g would
  be vacuous for these two mutants on such a host (`site-record-equal` on every fixture → unattributed).
- CPython emits no line event for continuation line 155 (the two-line statement maps all instructions to line
  154), so the span's second line never executes as a trace event; leg f is still satisfied via line 154.
A discriminating record for module-level spans would capture the bound object's content (e.g. the compiled
pattern's `.pattern`, or the global's repr with source) rather than relying on a version-specific repr.
**vacuous = 0/9 on this host; 2/9 under simulated old-Python repr.**

## 3. Tracing neutrality (task 3)

Command (envelope-wrapped; receipt `effect.txt`):
```
envelope.sh $S/env python3 h.py effect --rootbase $S/w3c --jobs 8
```
All 60 traced-vs-untraced comparisons (6 fixtures × (reference + 9 mutants)) are identical in
(rc, classes): `same=True` 36/36 mutant × fixture rows, `same=False` 0. Mutant double-traces are also
stable: `trace_stable=False` 0.

```
ENVELOPE start 19:14:30 cwd=/home/vgpnk/Projects/shokunin
EFFECT NO22 order wit-p2-excuse untraced=(0,[]) traced=(0,[]) same=True trace_stable=True
ENVELOPE end 19:14:36 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

One unexplained one-off: in the first effect run (root w3) the line
`EFFECT NO5 order wit-p2-excuse untraced=(0,[]) traced=(1,[]) same=True trace_stable=True` appeared, which
is internally contradictory. It did NOT reproduce in two subsequent full runs (w3b, w3c — the latter is
`effect.txt`) nor in a dedicated 6× probe of NO5/wit-p2-excuse (all `(0,[])` in both modes, traced rc=0,
sites stable `('120>121:5ec32d22ace57cf9','120>130:3479695f6d20418f')`). It is therefore excluded from the
count. **trace-divergence = 0 (reproducible).**

## 4. control-c1-value reproduction (task 4)

Control (`claims/control-c1-value.txt`) reproduced byte-for-byte in content: mirror lane with witness module
copied into `plans/battery43`, counter copy with `SITE_EQUAL` forced to `return True`
(command: `python3 $S/w4/m-value/plans/round43_c1_verify.py --lane $S/w4/m-value --work $S/w4/m4w2`;
receipt `control-c1-value-repro.txt`, sha256 `82c0b24f7bf08dad2ac3cece002f3760fe2dd69cfa19926a76b98d8ad95ddce4`):
```
ENVELOPE start 19:14:10 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE wit-long-row tool=anchor expect=reject declared=row-malformed observed_rc=1 observed=row-malformed ok
... (6/6 ok, wrong=0)
MUTANT NA1 anchor silence UNATTRIBUTED hits=1 last=site-record-equal first=wit-long-row span=L477-L477 ...
... (9/9 UNATTRIBUTED last=site-record-equal)
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=9 killed=0 survived=0 invalid=0 null_detected=0 unattributed=9
MUTANTS-BY-TOOL anchor=0/6 order=0/3
ADVERTISED direct=8 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
ENVELOPE end 19:14:15 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```
Match with the freeze control: same 6 fixtures, same 9 `site-record-equal` rows (same first fixture, same
span bounds), `unattributed=9`, per-tool 0/6 and 0/3, `PREDICATE C1 fail`, exit 1.

Sanity anchor — the witness-as-battery dev run reproduces the freeze receipt `claims/witness-run.txt`
(command: `python3 plans/round43_c1_verify.py --lane <lane> --battery-dir <lane>/.ufo/waves/round-43/claims/witness --work $S/w5w2`;
receipt `witness-run-repro.txt`, sha256 `34b840f45eb358da093bdf8241d83a20b51cf821016c665bc09ed9a91e95494f`):
```
ENVELOPE start 19:14:18 cwd=/home/vgpnk/Projects/shokunin
MUTANTS total=9 killed=9 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=6/6 order=3/3
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 19:14:22 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```
Every kill is `value=differs` with the same killing fixture and attributed line as the freeze receipt (NA18
killed by wit-short-commit-url attributed L154; NO7 by wit-p2-excuse attributed L60; etc.).

---

## Findings summary
1. No spurious within-root record difference: reference double-trace 24/24 stable across jobs/seed/root
   arms; mutant double-traces also stable. The only instability found is cross-root (4/4 anchor fixtures),
   from an unnormalised scratch-root path leaf leaking into locals; it cannot affect leg g as frozen (same-root
   comparisons) but makes records non-canonical across builds.
2. Leg g is not vacuous on this host for the module-level spans (NA18, NO7) — records differ on every
   fixture — but only because CPython 3.14's `re.Pattern.__repr__` prints the pattern source; on Pythons
   with an address-only repr both mutants would be `site-record-equal` on every fixture (2/9 vacuous).
3. Tracing does not change tool results (0 reproducible divergences in 60 comparisons; one non-reproduced
   contradictory line documented above).
4. `control-c1-value.txt` reproduces exactly; witness-run.txt reproduces exactly.

VERDICT: value-leg-spurious-0-vacuous-0/9-trace-divergence-0
