# Round-11 design critique (pre-run, zero endpoint requests)

Critic verdict on the `round11-power` preregistration bundle before the first
sampling request. Every check below was re-run locally against committed bytes
and code; no request was issued to `127.0.0.1:34113` (the only network-touching
commands executed were none — all verification is offline). Repo root for all
commands: `/home/vgpnk/projects/shokunin/kengaku-shokunin`.

Ordering preconditions observed: `sha256sum -c
corpus/evidence/round11-power/prereg-bundle.sha256` → all three files `OK`
(probe_plan_r11.md, power_analysis_r11.md, predictions-r11.md unmodified since
hashing); `ordering.log` records `pre-hash 2026-09-28T23:10:20Z` /
`post-hash 2026-09-28T23:10:20Z` (v1).

---

## (a) Paired effect size from committed r9 bytes — REPRODUCE

Command (repo root, reads only `corpus/evidence/round9-replication/results-r9.jsonl`;
the exact snippet from `power_analysis_r11.md` plus reporting lines):

```python
import json, collections, statistics
recs = [json.loads(l) for l in open('corpus/evidence/round9-replication/results-r9.jsonl')]
d = collections.defaultdict(dict)
for r in recs:
    if r['cell'] in ('A-CKPT4710', 'A-CKPT710') and 'nwrong' in r:
        d[r['pid']].setdefault(r['cell'], {})[r['turn']] = r['nwrong']
diffs = []
for pid in sorted(d):
    a, b = d[pid]['A-CKPT4710'], d[pid]['A-CKPT710']
    diffs.append(((b[7] + b[10]) / 2) - ((a[7] + a[10]) / 2))
# reported: per-pid, statistics.mean, statistics.stdev, d, sign counts, final-turn-only mean
```

Observed:

```
per-pid diffs (pids 101..108): [2.5, 0.0, 1.0, -0.5, 1.0, 0.0, 0.0, 0.0]
mean 0.5  sd 0.963624  n 8  d 0.5189
sign W/L/T: 3 1 4
final-turn-only diffs mean: 0.5
A-CKPT4710 final passes 2/8  mean final nwrong 0.875
A-CKPT710  final passes 2/8  mean final nwrong 1.375
r9 request-derived records: 276  mean 0.215  median 0.26  max 0.62  sum 59.5
```

Matches every claim: table (+2.5, 0, +1.0, −0.5, +1.0, 0, 0, 0), mean +0.500,
sd 0.9636, d 0.519, sign 3W/1L/4T, final-turn-only mean identical +0.500, the
r9 headline (2/8 = 2/8, 0.875 → 1.375), and the power file's cost basis
(276 requests, mean 0.215 s, sum ≈ 60 s).

## (b) Power arithmetic — REPRODUCE (one rounding-convention defect, MINOR-1)

Command: `python3` snippet computing `(1.959963984540054+0.8416212335729143)**2`,
`7.849/d²` + ceil per row, `NormalDist().cdf(sqrt(n)*d−1.96)`:

```
(1.9600+0.8416)^2 = 7.84888  → "7.849" OK
d=0.519: exact n=29.1393 ceil=30 power@ceil=0.8113   (table: 30) OK
d=0.50 : exact n=31.3960 ceil=32 power@ceil=0.8074   (table: 32) OK
d=0.40 : exact n=49.0562 ceil=50 power@ceil=0.8074   (table: 50) OK
d=0.35 : exact n=64.0735 ceil=65 power@ceil=0.8056   (table: 64) ← see MINOR-1
d=0.30 : exact n=87.2111 ceil=88 power@ceil=0.8035   (table: 88) OK
power n=64 d=0.519: 0.9858 ≈ 0.986 (claimed) OK
MDE sqrt(7.849/64) = 0.35020 ≈ 0.350 (claimed) OK
power n=64 d=0.35 = 0.79955 (marginally under 0.80)
```

All headline numbers (7.849, rows 30/32/50/88, power 0.986, MDE 0.350)
reproduce; the d=0.35→64 row is the one cell that does not follow the ceil
convention of its sibling rows (MINOR-1, not material: 0.05 pp of power).

## (c) Seed/pid disjointness + precheck re-run — REPRODUCE

Command: python3 heredoc importing `probe_r11.py` (with
`KENGAKU_R11_OUT=/tmp/kengaku-r11-critic-probe`, no network calls — only
`gen_problem`), regenerating r11 problems and comparing against committed
`results-r9.jsonl` + `round8-horizon/results.jsonl` metas:

```
generated: 64  distinct: 64
old metas: 18
old-vs-r11 (init,ops) overlap: 0
r9 scheme reproduces r9 metas: True | r8 scheme reproduces r8 metas: True
seed overlap r11&r9: 0  r11&r8: 0  r9&r8: 0
ops-count distribution: {10: 64}
```

Every line of `prereg-precheck.log` re-derives ("64 distinct r11 problems: 64",
"old metas: 18 overlap with r11: 0", "seed overlap r11&r9: 0 r11&r8: 0",
"ops-count distribution: {10: 64}"). Scheme self-check passed: regenerating
r9 (`2000+pid*29`, pids 101–108) and r8 (`700+pid*13`, pids 1–10) from the
claimed schemes reproduces their committed metas exactly, so disjointness is
proved over the right objects. All 64 `gen_problem(3000+pid*41)` calls
terminate (no runaway `seed+977` recursion) and all have 10 ops.

## (d) run_r11.py fidelity — REPRODUCE

Ladder ask-logic equivalence. Command: python3 heredoc extracting both
`ladder()` bodies, normalizing whitespace/quotes, difflib-comparing, and
enumerating the ask decision at every turn of both cells:

- Normalized textual diff of the two `ladder()` bodies: only formatting/
  line-wrapping, the added docstring line, and the two ask lines
  (`turn in checkpoints or name=='A-INC'` → `turn in checkpoints`;
  `name!='A-INC' and (i+2) in checkpoints` → `(i+2) in checkpoints`,
  run_r11.py:76–78 vs run_r9.py). No other semantic token differs; graded/ack
  record payloads are key-identical.
- `ask-logic mismatches over all 18 decision points (2 cells × 9 turns): []`
  — r9's ask logic with `name≠'A-INC'` is provably identical to r11's, i.e.
  exactly "minus the dead A-INC clause". The spillover quirk is preserved:
  the turn before a checkpoint gets the `CHECKPOINT — output the FULL state
  now.` ask yet logs as `-ack` (raw[:80]).

Totals. Command: discrete simulation of the run_r11.py control flow
(1 descriptors fetch; per (cell,pid) job: 1 filler + 10 turn requests;
counterbalance `order` at run_r11.py:129):

```
simulated requests: 1409   records: 1473
{'descriptors': 1, 'meta': 64, 'filler': 128,
 'ack:A-CKPT4710': 448, 'graded:A-CKPT4710': 192,
 'ack:A-CKPT710': 512,  'graded:A-CKPT710': 128}
parity split even/odd: 32 / 32
SUMMARY regex 'A-CKPT4710: 15/64' → matches ^(\S+): (\d+)/(\d+)$
```

Matches the claimed 1409 requests (1 + 64×22) and 1473 records
(1 + 64 + 192+128 + 448+512 + 128). Filler fires unconditionally before every
cell (run_r11.py:135), 128 total. SUMMARY print (run_r11.py:145) matches
grader `parse_runlog_summary` regex `^(\S+): (\d+)/(\d+)$` (grader.py:555).

## (e) probe_r11.py fidelity — REPRODUCE

Command: `diff -u corpus/evidence/round9-replication/replicate.py corpus/evidence/round11-power/probe_r11.py`

Observed (complete): exactly three hunks — (1) the docstring block; (2)
`BASE = "http://127.0.0.1:34113/v1/chat/completions"` →
`BASE = os.environ.get("KENGAKU_R11_BASE", "http://127.0.0.1:34113/v1/chat/completions")`;
(3) `OUT = "/tmp/bench-r8"` →
`OUT = os.environ.get("KENGAKU_R11_OUT", "/tmp/kengaku-r11")`. All generation,
grading, parsing, HTTP semantics byte-identical, exactly as the docstring's
lineage claim states.

## (f) Plan §4 schema internal consistency — REPRODUCE

Cross-checks (all commands above): checkpoint sets {4,7,10}/{7,10} → per pid
3+2 graded and 7+8 ack records ⇒ 192/448 and 128/512, summed in §5 as
"320 graded, 960 ack" — internally consistent, and independently
cross-validated against real r9 bytes (r9 cell counts:
`A-CKPT4710 24 = 8×3`, `A-CKPT4710-ack 56 = 8×7`, `A-CKPT710 16 = 8×2`,
`A-CKPT710-ack 64 = 8×8`), confirming the spillover quirk's per-pid ack
counts. Record-field lists in §4 match the code exactly: descriptors carries
all 13 named fields (run_r11.py:103–116); meta has no `request_ts` because
descriptors uses raw `urlopen` (never sets `last_req`, run_r11.py:42–45) so
metas log unstamped (run_r11.py:47–50 stamps only when `last_req` set and
absent — §7 deviation 3); graded/ack/filler/error payloads match. `separators=(',',':')`
+ append mode confirmed (run_r11.py:51, :38). §4's 1473/1409 totals = §5's
stored totals line.

## (g) Ordering protocol soundness — REPRODUCE (no hole found)

Command: `grep -nE 'urlopen|urllib|Request\(|http://|socket|subprocess|threading|Thread|atexit|pgrep|os\.system|popen'`
over run_r11.py + probe_r11.py. Complete inventory of network-issuing paths:

1. `run_r11.py:93` — `urlopen(HOST + "/v1/models")` inside `descriptors()`;
   `main()`'s first statement is `descriptors()` (run_r11.py:119) ⇒ the GET
   /v1/models fetch is the process's first network request. Its record carries
   an explicit `request_ts` computed before the fetch (run_r11.py:90).
2. `probe_r11.py:33–36` — `Request(BASE)` + `urlopen` inside `call()`,
   reached only via the wrapped `p.call` from `filler()`/`ladder()`, i.e.
   strictly after descriptors returns.

No threads, no atexit, no other sockets; the only other subprocess is the
local `pgrep` (run_r11.py:99). Probe import time side effects are local only
(`makedirs`, open log handle). Nothing network precedes the descriptors fetch;
the bundle hash (ordering.log, 23:10:20Z) precedes process start by protocol
§6.1–6.2, and the first chat request postdates the models fetch, so
first-request > hash-time is structural, with ordering.log + `request_ts`
proving it post hoc. Smoke protocol cannot contaminate committed bytes: OUT is
env-selected (`KENGAKU_R11_OUT`, run_r11.py:28, probe_r11.py:21), smoke pins
`/tmp/kengaku-r11-smoke`, and landing copies only the main run's
`results-r11.jsonl`; a leftover import-time empty `{OUT}/results.jsonl` is
never written by the runner (MINOR-4). Residual append-mode reuse risk →
MINOR-4.

## (h) Verdict rule mechanical / exclusive / exhaustive — REPRODUCE

`predictions-r11.md:32–38`: branches (1) diff>0 ∧ p<0.05 → ESTABLISHED,
(2) diff>0 ∧ p≥0.05 → DIRECTIONAL, (3) diff≤0 → FALSIFIED. The conditions
partition all (diff, p) outcomes exclusively and exhaustively; the
sign-agreement downgrade (lines 42–44: sign test must agree in direction,
else downgrade to DIRECTIONAL regardless of t p) attaches only to branch 1
and never yields two verdicts. Both inputs are §5-pinned estimators (paired t
on 64 diffs, df=63; exact sign test on the same diffs), so the rule is
mechanical. The McNemar clause (lines 45–48) is descriptive-only and cannot
feed back into the verdict. The point-prediction falsifier ("diff ≤ 0 kills
the claim", line 14) is consistent with branch 3. Degenerate cases → MINOR-3.

## (i) Brier / point-prediction scoring computable — REPRODUCE

All scoring inputs are derivable from the named artifacts alone:
outcomes for the three probabilistic predictions (predictions-r11.md:20–22)
are diff>0 (§5 paired-diff formula), t p<0.05 ∧ diff>0 (§5 t estimator), and
|passes(4710)−passes(710)| ≤ 8 (final-turn `ok` counts in results-r11.jsonl);
Brier formula is defined in-file (line 24, `(1/3)Σ(P−outcome)²`); the three
point predictions (lines 12–14) score against final pass counts and the
paired diff. Predictions are inside the hashed bundle, so the scored values
are frozen. One normalization ambiguity on the diff row → MINOR-2.

---

## Defects

**FATAL — none.**

**MAJOR-1 (conditional — must be adjudicated before landing):** no
preregistered contingency for mid-run endpoint failures. `urlopen` raises on
timeout/5xx → caught at run_r11.py:138 → an `error` record and a truncated
cell, leaving an incomplete pid pair. §5's stored formats hardcode
`n=64`, `df=63`, and `0 error records`, and §4 marks error "expected ×0", but
neither the plan nor predictions-r11.md's void list says whether an
error-contaminated run is void (full re-run) or analyzed pairwise-complete
(n<64). If zero error records land (r9 baseline: 0/276 with identical
machinery, 300 s timeout), this is vacuous and the run lands as designed. If
≥1 error record lands, the round needs a LOG ruling / errata defining the
handling before anything is landed. Does not block starting the run.

**MINOR-1:** power table row `d=0.35 → 64` breaks the ceil convention of the
other rows (exact n=64.0735 → ceil 65; power at n=64 is 0.79955, 0.05 pp
under 80%). The design's own framing survives — MDE(64)=0.35020 rounds to the
claimed 0.350, and 0.35 was chosen as a planning MDE, not a cliff — but the
inconsistency should be recorded in the analysis file when it lands. Adjacent
triviality: `power_analysis_r11.md` writes Φ(2.191); the arg is 2.192
(8×0.519−1.960); Φ=0.986 unaffected.

**MINOR-2:** paired-diff point-prediction scoring normalization is ambiguous:
predictions header says `|predicted − observed| / 64` while the §5 stored line
implies mean units (`abs error e.eee` next to `±d.ddd observed`). The only
coherent uniform metric is per-problem units — pass rows `|pred−obs|/64`, diff
row `|0.350 − diff|` with no further division — but recompute_r11.py/grader
must pin exactly that to avoid a post-hoc argument on a grader-pinned line.

**MINOR-3:** verdict-rule degenerate cases unspecified: sign test with zero
decisive pairs (direction undefined — "agree in direction" has no value) and
sd(diffs)=0 (t undefined). Both are measure-zero at n=64; the rule is
mechanical on all non-degenerate inputs.

**MINOR-4:** output hygiene: `results-r11.jsonl` opens in append mode
(run_r11.py:38), and the default OUT (`/tmp/kengaku-r11`) is shared between
smoke and main — only the env override separates them; re-running an attempt
into the same OUT would append duplicate records (grader's 1473-record total
catches it, but use a fresh OUT per attempt). Also, importing probe_r11.py
creates a stray empty `{OUT}/results.jsonl` (probe_r11.py:24) that the runner
never uses.

**MINOR-5:** the hashed bundle pins the three .md design files only;
`probe_r11.py`/`run_r11.py` are not hashed pre-run. probe machinery is pinned
only descriptively at run time (`descriptors.machinery_sha256`, run_r11.py:114)
and `run_r11.py` is hashed nowhere. Mitigations exist (this critique verifies
items (d)/(e) pre-run; the "byte-identical machinery" claim is itself
preregistered in the bundle, so post-hash code drift would falsify a frozen
claim; landing records md5s). Recommend appending both file hashes to
ordering.log at run time.

**MINOR-6:** wording: predictions' void rule ("Any of the 64 seeds fails
`gen_problem` … before any request") is literally unsatisfiable —
`descriptors()` runs before the in-run generation loop (run_r11.py:119–122),
so a models GET precedes it. Harmless: it is a GET, not a sampling request,
and `prereg-precheck.log` (re-verified in (c)) already proves all 64 seeds
generate, making the in-run branch unreachable.

---

Verdict summary: (a)–(i) all REPRODUCE; no FATAL defect; one conditional
MAJOR that binds only if the run is not byte-clean; six MINOR records, none
of which invalidates the design, the power claim, the frozen predictions, or
the ordering protocol.

DESIGN VERDICT: CLEAR-TO-RUN
