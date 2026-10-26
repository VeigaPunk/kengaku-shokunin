# R42CritAttribution — attack on C1 attribution leg f (frozen counter, round 42 wave 1)

Critic seat, kengaku round 42 wave 1. Lane read-only; nothing in the lane was edited. All runs under the
mandated envelope (`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin …`), receipts in
`.ufo/waves/round-42/build/R42CritAttribution/`.

## 0. What was attacked

Frozen artifact: `plans/round42_c1_verify.py` (sha256 `559fca0c9254e4c09f2406f75ba9559e370012ccb1ecdc91c9a944abbe0c6649`,
equal in lane and in my copy). Leg f is the docstring sentence at `plans/round42_c1_verify.py:26-28`:
"executes at least one line of the replaced span (`sys.settrace` restricted to the tool file, the tracer bound
read-only like the variant)" (22 words). The leg computes `span` from the mutant table, re-runs the mutant on the
killing fixture with the frozen `TRACER`, and credits the kill only when `(rc, classes)` reproduce and
`span & t_lines` is non-empty (`plans/round42_c1_verify.py:610-611`, `:614-628`).

Method: the frozen counter was imported as a library from a byte-identical copy (verified by sha256, above);
fixtures were built with the counter's own `build_battery` + the frozen witness modules
(`.ufo/waves/round-42/claims/witness/w_anchor.py`, `w_order.py`) into a scratch clone; every `Runner.run` is the
frozen sandboxed run. 120 (variant × own-tool fixture) pairs were each run three times: untraced, frozen tracer,
and an instrumented tracer that records, per line event, the executing code object and a digest of `f_locals`
(harness `R42CritAttribution/h.py`, analysis `a2.py`, data `res.json` / `t2.json`).

## 1. Summary

| question | measured |
|---|---|
| (1) span leg vacuous? | **8/14** mutants: `span ∩ t_lines ≠ ∅` on **every** fixture of their tool (3 of them structurally unconditional: XO6, XO7, X13) |
| (2) tracing changes the result? | **0/120** pairs diverge on `(rc, classes)`, frozen tracer and instrumented tracer alike; runtime deltas exist but are inert for these two tools (see §3) |
| (3) multi-line replacement (X6) | line events on the continuation line are recorded correctly, but the span's OR-form credits the **guard** line 527 on 3/9 fixtures where the mutated line 528 never runs |
| (4) `control-c1-attribution.txt` reproduces? | **yes, with the patch the claims document** (`span = {1}`): all 35 body lines identical. The unpatched counter with the same witness battery attributes 14/14 (`PREDICATE C1 pass`, stable over two runs) |

## 2. Q1 — the span leg is vacuous for 8/14

### 2.1 Per-mutant measurement (frozen tracer, own-tool fixtures)

Command: `python3 h.py` then `python3 a2.py` (scratch), section A. `span_hit` = fixtures whose traced mutant run
contains a line of `span`; `exhibit` = fixtures that satisfy the mutant's declared direction.

```
id   tool   direction  span    n_fx exhibit  span_hit  hit_not_exh  ref_hit   killed_by
X1   anchor rc-mirror  318     9    1        9         8            9         w-x1-provrow-only
X3   anchor rc-mirror  343     9    1        1         0            1         w-x3-provurl-fallback
X6   anchor silence    527-528 9    1        7         6            7         w-x6-wrong-capture
X7   anchor silence    535     9    3        3         0            3         w-x7-unknown
X9   anchor rc-silence 477     9    1        9         8            9         w-x9-short-row
X12  anchor rc-mirror  256     9    1        1         0            1         w-x12-slashless-slug
X13  anchor rc-silence 570     9    1        9         8            9         w-x13-staged-index
X14  anchor silence    458     9    1        2         1            2         w-x14-erratum-upper
X15  anchor rc-silence 455     9    1        2         1            2         w-x15-erratum-sibling
XO1  order  rc-silence 183     5    1        5         4            5         w-xo1-freeze-has-receipt
XO3  order  rc-silence 188     5    1        5         4            5         w-xo3-receipt-first-removed
XO5  order  rc-mirror  117     5    1        5         4            5         w-xo5-post-receipt-blob
XO6  order  rc-mirror  53      5    1        5         4            5         w-xo6-p10-pass-line
XO7  order  rc-silence 55      5    1        5         4            5         w-xo7-case-timeout
```

**Counterexample.** For `XO6` and `XO7` the span is a module-level `re.compile` (`order_check.py:53` and `:55`);
for `X13` it is `ap.add_argument("--evidence-ref", …, default=…)` (`anchor_digest_check.py:570`), executed by
every invocation because the witness fixtures pass only `--lane`. Those three spans are executed **once per
process, before any fixture byte is read**: the leg is true on 5/5, 5/5 and 9/9 fixtures and equals the
reference run's own span-hit set (`ref_hit` column). It therefore cannot fail for those mutants and carries no
information about the kill; it is a tautology, not evidence.

Five further mutants reach the same state on this fixture family (every witness fixture is a one-row repo / the
same commit graph), so the leg also never fails for `X1`, `X9`, `XO1`, `XO3`, `XO5`. Only 6/14 have a span that
the fixture set actually discriminates (`X3`, `X6` partly, `X7`, `X12`, `X14`, `X15`).

This does not make the 14 kills causally wrong — a one-site mutation plus a reproduced result difference is still
caused by the mutated site — but it means leg f does **not** buy what the docstring says it buys for 8/14: it
cannot distinguish "the fixture exercises the advertised behaviour" from "the line runs unconditionally".

### 2.2 The value witnesses the leg should be checking (measured)

The three named mutants do have a discriminating witness — the value of the replaced expression on the killing
fixture (section F of `analysis.txt`):

```
XO6 ref GATE_P10 pattern: '^\\s*(?:gate:\\s*)?P10\\s+(DEFECT|ok)\\b[ \\t]*(.*)$'
XO6 mut GATE_P10 pattern: '^\\s*(?:gate:\\s*)?P10\\s+(DEFECT|ok|PASS)\\b[ \\t]*(.*)$'
XO6 GATE_P10.match('P10 PASS receipt unreadable') ref=None mut=<re.Match span=(0,27)>
XO7 ref CASE_LINE pattern: '^\\s*CASE\\s+\\S+.*\\bobserved=[^\\s]*'
XO7 mut CASE_LINE pattern: '^\\s*CASE\\s+\\S+.*\\bobserved=(?:pass|fail)'
XO7 CASE_LINE.match('CASE c1 observed=timeout') ref=<re.Match span=(0,24)> mut=None
X13 ref  frame-state@L573 a=Namespace(lane=…, evidence_ref='head', verbose=False)
X13 X13  frame-state@L573 a=Namespace(lane=…, evidence_ref='index', verbose=False)
```

So the answer to "what would a stronger attribution be" is: per mutant, the **mutated value observed on the
killing fixture** — the regex's `match()` flipping, or the parsed namespace's `evidence_ref` flipping from
`head` to `index` (which changes the git spec `HEAD:<path>` to `:<path>`). That is cheap and deterministic, but it
is not derivable from the generic tracer: the counter does not know which name a mutant's span binds or what
consumes it. It needs a `probe` field on each `MUTANTS` row (a callable/argv that observes the value). The table is
frozen, so this cannot land in wave 1 — it is the residual limit to name (see §7).

### 2.3 Alternatives tested and rejected (so no one re-proposes them)

* **Executed-line-set differential** (mutant's traced line set vs the reference's on the same fixture). Rejected
  by measurement: `X7` shows `0/9` differing fixtures, including its killing fixture `w-x7-unknown` — the mutant
  prints a different `class=` on the same lines. A leg requiring a line-set difference would mark X7's three
  genuine hits `UNATTRIBUTED` (false negative). (`c3.py`, column `lineset-diff-fx`.)
* **Naive frame-state digest** (`sha256` of `repr` of every `f_locals` item, addresses stripped). Rejected by
  measurement: the *same* variant on the *same* fixture diverges at `check@412: 50/50` lines between two runs
  (`n.py`), because `f_locals` holds sets (`allowed`, `row_scope`) whose `repr` order is hash-seeded. Any state
  leg must hash a canonicalised projection (sorted containers, no unordered `repr`), or a specific binding.
* **Widening the span to a window after it** — no gain over the line test for the always-run mutants (§2.1).

## 3. Q2 — tracing does not change the tool's result (0/120)

Section B of `analysis.txt`: 120 pairs × {untraced, frozen `TRACER`, instrumented tracer}:
`pairs=120 frozen-tracer-diverged=0 instrumented-tracer-diverged=0` (equal `(rc, classes)` in every triple).

Runtime deltas found with a probe script run both ways (`meta/probe.py`, `meta/m.py`, output `meta.json`):

```
mode        direct rc | traced rc | stdout same | stderr same
ok          0           0           no (PKG/TRACE lines only)     yes
none        0           0           no (PKG/TRACE)                yes
str         1           1           no (PKG/TRACE)                yes
two         2           2           no (PKG/TRACE)                yes
raise       1           1           no (PKG/TRACE)                yes
argparse    2           2           no (PKG/TRACE)                yes
returntrue  1           1           no (PKG/TRACE)                yes
```

* Exit-code mapping is identical for `SystemExit(None)`→0, `SystemExit("boom")`→1, `SystemExit(2)`→2,
  uncaught `RuntimeError`→1 (traceback to stderr only), argparse error→2, and `sys.exit(True)`→1: the tracer
  stores `e.code` and re-raises it after writing the trace file, so the mapping is preserved.
* `sys.argv[0]`, `sys.argv[1:]`, `__name__`, `__file__`, `__spec__` are identical direct vs `runpy.run_path`
  (`_ModifiedArgv0` sets argv[0] to the same slot path the direct run uses).
* Two environment deltas exist and are inert **for these two tools**: `__package__` is `None` direct and `''`
  under `runpy`; `sys.gettrace()` is `False` direct and `True` traced. `grep -n "gettrace\|__package__\|__file__"`
  over both tools returns only `anchor_digest_check.py:591: sys.exit(main(sys.argv[1:]))` — neither reads
  `__package__`, `__file__` or `gettrace`, which is why the 0/120 is explained rather than lucky. A future tool
  that branches on `sys.gettrace()` or `__package__` would be traced differently and must be re-measured.
* Tracer credit is an **over-approximation** of executed lines: the global hook adds `f_lineno` on every *call*
  event in the tool file. Measured across all runs, that contributes line `0` (module frame) and 29 `def` lines
  (`63,67,68,71,77,80,84,95,101,115,141,167,171,182,187,194,198,202,217,256,292,302,313,334,374,395,412,539,567`);
  `line_hits ∪ call_linenos` equals the frozen hit set on all 120 runs. No span line is credited **only** by a call
  event in these runs, but one span line (`X12` line 256) is also a call-event line (a genexpr starting on 256),
  so the hole is live-adjacent. Counting only `event == "line"` closes it at zero cost.

## 4. Q3 — X6's two-line replacement

`X6`'s `old`/`new` are two lines (`anchor_digest_check.py:527-528`): `elif tok not in row_scope:` /
`if tok in allowed:` → `if False:`. `new.count("\n") + 1 = 2`, so `span = {527, 528}` — the continuation line is
inside the span, and the tracer emits real line events for it (measured independently of 527):

```
w-x1-provrow-only       mut527=1 mut528=0 ref527=1 ref528=0 span_leg=1
w-x3-provurl-fallback   mut527=1 mut528=0 ref527=1 ref528=0 span_leg=1
w-x12-slashless-slug    mut527=1 mut528=0 ref527=1 ref528=0 span_leg=1
w-x6-wrong-capture      mut527=1 mut528=1 ref527=1 ref528=1 span_leg=1
w-x7-unknown            mut527=1 mut528=1 ref527=1 ref528=1 span_leg=1
w-x13-staged-index      mut527=1 mut528=1 ref527=1 ref528=1 span_leg=1
w-x15-erratum-sibling   mut527=1 mut528=1 ref527=1 ref528=1 span_leg=1
w-x9-short-row / w-x14  mut527=0 mut528=0                 span_leg=0
```

So the count is correct, but the **OR-form is loose**: on `w-x1`, `w-x3`, `w-x12` the span is credited by the
guard line 527 while the mutated statement 528 is never executed (527's test is false → no line event at 528).
Those three fixtures are non-killing, so the conjunction with the behaviour test saves X6's kill; the leg itself
is still satisfied without the mutated line running, and the counter prints `attributed=L527` — the guard, not
the mutation (`control-repro-natural.txt`). A replacement whose changed text sits on a later line of a multi-line
span would be credited by an unchanged earlier line in the same way.

The span also derives its length from `new` (`start + new.count("\n") + 1`), i.e. it covers the whole replacement
region rather than the lines whose text changed. Nothing in the frozen table exploits the deletion case.

## 5. Q4 — `control-c1-attribution.txt` reproduces

The frozen control is documented as a *forced* control, not a natural run — `plans/round-42-claims.md:49-50`:
"the attributed span forced to line 1 → `killed=0 unattributed=14`, fail: leg f can fail" (14 words).

* Natural run (unpatched counter, witness modules as `plans/battery42`, clean `git clone --shared` of the lane,
  `python3 plans/round42_c1_verify.py --lane .`): `MUTANTS total=14 killed=14 survived=0 invalid=0
  null_detected=0 unattributed=0`, `MUTANTS-BY-TOOL anchor=9/9 order=5/5`, `PREDICATE C1 pass`, exit 0
  (`control-repro-natural.txt`, sha256 `749e4793380428977e18399676199407357aaacb29f9b215eca26e32f58717a1`);
  two independent runs produce an identical body.
* Forced run: patch `span = set(range(start, start + new.count("\n") + 1))` → `span = {1}` and run the same
  command. Result: all **35** body lines (`PINS`…`PREDICATE`) are byte-identical to
  `.ufo/waves/round-42/claims/control-c1-attribution.txt`, including `span=L1-L1` on every mutant,
  `MUTANTS total=14 killed=0 survived=0 invalid=0 null_detected=0 unattributed=14`,
  `MUTANTS-BY-TOOL anchor=0/9 order=0/5`, `PREDICATE C1 fail`, exit 1 (`control-forced-span1.txt`, sha256
  `94c394ae219c852dab777adcd4be4921892e74d51b99ea4d70f02e4bf5e8de9d`).
  Its envelope line differs (`--ro-bind /home/vgpnk /home/vgpnk --bind …/L1 …`, cwd `…/L1/m/attr`); the body does not.

So the control is honest and reproducible **only together with its patch**; a reader who reruns the frozen
counter and gets `killed=14` is not seeing a contradiction. Recommend the L1 keep the one-line patch next to the
control (or note it in the claims cell), since the control's numbers are otherwise not derivable from the frozen
file.

## 6. Smallest safe correction (draft, tested in scratch only)

`R42CritAttribution/attribution-stronger.patch` (2 hunks, no frozen-table change):

1. **Count line events only.** Drop `hit.add(frame.f_lineno)` from the tracer's global hook, so a span line can
   only be credited by an executed statement, not by a call event (removes the line-`0`/`def`-line credit; the
   only remaining call-event coincidence, `X12` line 256, then genuinely requires the statement).
2. **Span = the changed lines of the replacement**, not the whole region:
   `span = {start + i for i in range(len(new_lines)) if i >= len(old_lines) or old_lines[i] != new_lines[i]} or {start}`.

Measured effect (patched counter + witness battery, `patched-leg.txt`, `PREDICATE C1 pass`, exit 0): 14/14 still
attributed; `X6` moves from `attributed=L527` to `attributed=L528` (the mutated line) and its span-credit drops
from 7/9 to 4/9 fixtures — the 3 guard-only credits disappear. Every other mutant is a single-line replacement, so
nothing else changes. Cost: zero extra runs; the patch only narrows what is accepted.

What this does **not** fix: for the always-executed spans (§2.1) the leg remains non-discriminating. Closing that
needs the per-mutant value probe (§2.2), i.e. a new `probe` field in `MUTANTS` — a table change at the next
freeze, not a counter edit inside a frozen round.

## 7. Limit to name now (if the L1 does not take §6)

"A kill records a result difference in the declared direction on a fixture that executes the mutated line, not the
fixture's intent" (22 words, `plans/round42_c1_verify.py:64-65`) already names the semantic half. The new limit
this review adds: **for 8/14 mutants "executes the mutated line" is satisfied on every fixture of the tool,
because the mutated line runs unconditionally (3 by construction: XO6, XO7, X13; 5 more on this fixture family)**.
The leg is a liveness check, not a direction check, for those; and for `X6` the credited line is the guard 527
unless §6 is taken.

## 8. Host safety / Q32 receipt

Envelope used for every fixture build, counter run and probe:
`/usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000
--proc /proc --unshare-pid --die-with-parent <cmd>` (`receipt.txt`). Nothing was written to `$HOME`, `/usr`,
`/etc`, any PATH directory, the lane, or the fleet root; scratch was `/fast/scratch/hyaku/kengaku-r42/R42CritAttribution`
(three `git clone --shared` of the lane in scratch, each `rev-parse --show-toplevel` verified; no `git add`/`commit` anywhere).

Consolidated block (`receipt.txt`): `START 17:28:00` … `END 17:28:31`; `ls -A /home/vgpnk/.local/bin | sha256sum`
before and after that block both `763032563d3739aa6513b8aa3f0852d1cd7e7e4ba0a21165a391fc4026d60a78`
(100 names). Per-run blocks: 17:20:25/17:20:27, 17:22:40, 17:26:35, 17:29:12/17:29:14 all
`436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18`. **Observation, not a seat-local write:** the
listing digest changed in both directions while I was running (436b36… → 763032… between 17:26:35 and 17:28:00,
back to 436b36… between 17:28:31 and 17:29:12), i.e. another seat's transient install/removal; every one of my
runs is internally `before == after`, and no command of mine writes that directory.

Tools: none installed or updated by this seat.

## 9. Impacted axes

* **attribution-soundness** — leg f is a tautology for 8/14; §6 narrows it deterministically; §2.2 is the real fix.
* **calibration** — the shipped predicate still prints `pass` on the true witness battery; §6 preserves 14/14, so
  the axes move: soundness up, calibration unchanged, no regression.
* **tracer-fidelity** — 0/120 divergence measured; call-event credit and `__package__`/`gettrace` deltas are named
  so a future tool list re-measures instead of assuming.
* **freeze-provenance** — the attribution control reproduces only with its documented one-line patch; name the
  patch next to the control.
* **host-safety** — envelope held; the shared PATH directory churned by an external actor during the window.

VERDICT: attribution-vacuous-for-8/14-trace-divergence-0
