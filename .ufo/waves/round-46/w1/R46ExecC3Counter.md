# R46ExecC3Counter — `plans/round46_c3_verify.py` (round 46, wave 1, C3 coverage)

Seat: executor, leaf. Scope executed: the C3 counter, the filler control package, the before-control receipts.
Nothing was written to the lane's `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `PROVINCE.md` or `README.md`; no
git/jj mutation anywhere; no tool installed; nothing added to a PATH directory. The lane moved under this seat
(the L1 committed `cf7de6a`, then `420eec9`, and pinned its own copy of this counter); the delta is §"Delta to the
pinned copy" and everything else below is measured against the lane tree as cloned at those tips.

## Axes

- **Coverage** (the axis this claim is judged on): 13 legs over byte-pinned captures, a gate run at its round-45
  digest, a held-out predictor over a dual-runtime *program* end state, its own anchor-line rule, and a filler
  package the content legs must reject.
- **Depth / calibration**: every leg's negative path measured before the freeze (three failing controls, six red
  predictors, two nonces); a satisfiable positive path demonstrated (11/11 legs ok on a shape-correct dev package).
- **Operability**: three literal fills at stage 2 and no rewrite.

## Delivered

| path (under `.ufo/waves/round-46/w1/R46ExecC3Counter/`) | what | bytes / sha256 |
|---|---|---|
| `round46_c3_verify.py` | the counter, 919 lines, 13 checks | 43387 B, `3e462d552af49f58bedc6405e7cc506969126c896dc6c9f21fdb49f13ef20fb0` |
| `filler46/` | the control package (6 files + 8 captures + `SHA256SUMS`), **18** case ids | `receipt.txt` `cf45c5f0…`, `dry-cases.txt` `a47f6b01…` |
| `control-base.txt`, `control-filler.txt`, `control-echo-receipt.txt` | the three stage-2 controls | each `PREDICATE C3 fail`, exit 1 |
| `control-positive.txt` | dev satisfiability control, 11 legs, `defects=0` | exit 0 |
| `control-v2-gate.txt` | V2's gate invocation with the Bio stub | `P10 ok probe_rerun=byte-equal bytes=2800` |
| `v11-predictors.txt`, `v11-predictors-run2.txt` | V11 reference `ok`; six reds refused; two nonces | exit 0 |
| `v11-reference-predictor.py` | lint-clean predictor with `disagree=0` (contract worked example, dev evidence) | 2326 B |
| `dev/` | the dev drivers behind the two non-control receipts (`build_positive.py`, `positive.py`, `v11test.py`, `v2check.py`, `rebuild_positive.sh`) | — |

## The counter: V1–V13

`python3 plans/round46_c3_verify.py --lane .` prints one line per leg, then `checks=13 defects=<n>`, then
`PREDICATE C3 pass|fail`; exit 0 / 1. A leg that cannot run is a DEFECT, never a pass.

| leg | reads | fails when |
|---|---|---|
| V1 | `corpus/evidence/round46/tb2-polyglot-c-py/SHA256SUMS` vs a hardcoded 8-name digest table | a file's bytes, the name set or an extra file differ |
| V2 | `plans/pkg-spec-r46.json` (pinned), `plans/pkg_gate.py` (`ea6388…`) | a digest moved, or `pkg_gate package --rerun --require-clean-tree` exits non-zero |
| V3 | spec rows × registry | a row is not exactly one 11-cell registry row, or its anchor digest is not the spec pin |
| V4 | receipt vs frozen dry table | ids/order differ, the summary disagrees with the CASE lines, a `match=NO` case is unnamed, or `match=yes` sits on a predicted≠observed line |
| V5 | probe + dry table at their pins | a pin is pending, a digest moved, or `probe --dry` is not byte-equal to the frozen table |
| V6 | `scripts/sources-census.sh validate` | the registry does not validate |
| V7 | `## Requirement map` vs receipt | a tag's line, derived label or cited violating case is wrong |
| V8 | `plans/order_check.py` | the order gate does not print `ORDER RESULT PASS` |
| V9 | entry vs receipt, PROVINCE.md, README `## Frontier` | case table ≠ receipt, a row id absent outside `source:`, provenance absent |
| V10 | `## Mechanism` vs receipt + `DECISIVE` | a row is missing, cites a non-decisive line, or its quote is not verbatim there |
| V11 | entry `## Predictor` + the captured grader | lint hit, predictor crash, any disagreement, or <8 passes / <8 fails |
| V12 | package rows, own anchor rule (not imported) | a quote off its line, a range not holding it, a wrong word count, or a digest not resolving to the row's own capture under the package capture dir |
| V13 | `plans/filler46/` | fewer than three of V3/V4/V7/V9/V10/V12 defect on the filler |

`DECISIVE` is keyed to the probe's frozen table, verified against the landed bytes: `grep -c "^CASE"
corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt` → `18`, ids in order `nop, oracle-solve-sh,
lookup-table, python-only, c-only, extra-file, leftover-cmain, wrong-value, trailing-ws, nonzero-exit,
stderr-noise, n-parsed-differently, compile-warning, regrade-same-state, empty-file, dir-in-place, crlf-source,
value-plus-line` — the same 18 keys in the same order. A frozen case id absent from the map is a DEFECT.

## V11: the held-out predictor over `(listing, source)`

The entry's `## Predictor` defines `predict(files, source) -> bool`: `files` is `/app/polyglot`'s listing before
compilation, `source` the text of `main.py.c` (`None` when no readable regular file of that name exists). Each run
builds **60 fresh end states in 20 kinds**: values, decoy literals, padding, the extra file's name, a banner
comment and the state order come from `os.urandom`, so no committed byte determines a verdict. Each state is
written into a scratch `/app/polyglot` and graded by the **captured** `test_outputs.py` (`b94a7a98…`) inside
bubblewrap with host `gcc` and `python3`; `predict` runs in a second sandbox; only
`states= grader_pass= grader_fail= disagree=` is printed.

Measured twice, different nonces (`v11-predictors.txt`, `v11-predictors-run2.txt`):

```
V11 reference              ok states=60 grader_pass=15 grader_fail=45 disagree=0
V11 always-true            DEFECT … disagree=45
V11 always-false           DEFECT … disagree=15
V11 shift-table            DEFECT predictor lint tokens present: >>
V11 dict-table             DEFECT predictor lint tokens present: {,}
V11 verbatim-tuple         DEFECT predictor lint tokens present: >4000bytes
V11 file-read              DEFECT predictor lint tokens present: import
ENVELOPE end 02:34:05 exit=0 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
ENVELOPE end 02:34:13 exit=0 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
```

Kind list (all decided by execution, never by a stored verdict): `literal-ok`, `literal-ok-padded`,
`literal-ok-trailing`, `literal-ok-crlf-source`, `literal-ok-no-eof-newline` (pass); `wrong42`, `wrong10`,
`zero-ignore-k`, `stderr-py`, `stderr-c`, `float-py`, `float-c`, `no-print-py`, `no-print-c`, `extra-file`,
`stale-cmain`, `wrong-name`, `dir-main`, `c-syntax-error`, `py-syntax-error` (fail).

## V13 and the filler package

`filler46/` is right-shaped and establishes nothing: an 11-cell registry row per spec row with the filler
capture's real digest in the anchor, a dry table and receipt with the **probe's 18 case ids**, an entry carrying
every section. Its defects are content defects — every anchor quote sits on no line it cites; every requirement
label is stated; the case table holds one do-nothing row against eighteen receipt cases; the mechanism row cites a
non-decisive line; one CASE line claims `match=yes` with `predicted=pass observed=fail`. V13 requires **≥3
substantive** legs (V3, V4, V7, V9, V10, V12); measured `substantive=V4,V7,V9,V10,V12` (five).

## Controls measured (round-46 envelope, PATH-dir content digest unchanged in every bracket)

```
V4 DEFECT cases=18 mismatches_named=0/0 bad=["match=yes on a mismatching case: ['nonzero-exit']"]
V7 DEFECT rows=4 tags=4 bad=['single-file: no receipt case violates it', …]
V9 DEFECT case_rows=1/18 bad=['case table rows=1 receipt cases=18 equal=False', …]
V10 DEFECT mechanism_rows=1/18 bad=['mechanism rows=1 receipt cases=18 ids_equal=False', …]
V12 DEFECT rows=7 defective=7 live=7 first=S166:line,words
checks=7 defects=6
PREDICATE C3 fail
ENVELOPE end 02:33:15 exit=1 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
```
filler package, `--filler` (`control-filler.txt`).

```
PACKAGE unreadable: spec pin pending: SPEC_SHA256 is a stage-2 placeholder
V1 .. V12 DEFECT package unreadable: … (V13 still measures the filler: `V13 ok filler_checks=7 defects=6 …`)
checks=13 defects=12
PREDICATE C3 fail
ENVELOPE end 02:32:51 exit=1 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
```
base tree (`control-base.txt`; the L1 had already committed `plans/filler46`, so V13 was measurable there).

```
V4 DEFECT cases=18 … bad=['case ids differ from the frozen table', 'summary line count != 1']
V9 DEFECT case_rows=1/0 …
checks=7 defects=6
PREDICATE C3 fail
ENVELOPE end 02:33:18 exit=1 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
```
echo receipt — the filler's dry table copied over its receipt (`control-echo-receipt.txt`; restored byte-identically
afterwards, `cmp` clean).

Satisfiability, dev copy only (`control-positive.txt`; shape-correct package in the scratch clone, never committed):

```
V1 ok listed=8 wrong=0 extra=0          V4 ok cases=18 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True  V6 ok census_exit=0
V7 ok rows=5 tags=5 bad=0               V9 ok case_rows=18/18 bad=0
V10 ok mechanism_rows=18/18 bad=0       V11 ok states=60 grader_pass=15 grader_fail=45 disagree=0
V12 ok rows=7 defective=0 live=0        V13 ok filler_checks=7 defects=6 substantive=V4,V7,V9,V10,V12
DEV POSITIVE checks=11 defects=0
ENVELOPE end 02:32:02 exit=0 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
```
That run uses `plans/dev_pinned_c3_verify.py` — this delivered counter with the three `PENDING` pins replaced by the
dev tree's digests (`fbd717d1…`).

V2's gate path, measured on the same dev tree (`control-v2-gate.txt`):

```
gate: P1 ok pinned=1 mismatched=0        gate: P2 ok receipt_sha256=pinned
gate: P3 DEFECT … out_of_word_range=1    gate: P4 ok checked=12 bad=0
gate: P5 ok manifest_entries=8 bad=0     gate: P6 ok rows=7 bad=0
gate: P7 ok source_lines=7 bad=0         gate: P8 ok index_rows=53 knowledge_files=53 bad=0
gate: P9 DEFECT untracked=16 …           gate: P10 ok probe_rerun=byte-equal bytes=2800
V2: (False, 'spec=frozen gate=frozen gate_exit=1')
ENVELOPE end 02:33:31 exit=0 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
```
`P3`/`P9` are dev-tree content defects (one 2-word quote in the dev entry; sixteen untracked dev files — this item
authorises no scratch commit). `P10` is the point: **V2 hands the gate a stub `Bio` on `PYTHONPATH` and
`TMPDIR=<work>`**, so `pkg_gate`'s `import Bio` probe-interpreter branch stays on host python3 instead of fetching
numpy 15.9 MiB + biopython 3.1 MiB over the network and provisioning a managed CPython under `~/.cache/uv`. The
stub carries one attribute, `version = "1.85"`; the gate reads no other `Bio` name.

## Delta to the pinned copy (`plans/round46_c3_verify.py` @ `420eec9`, sha `a971c24d…`)

The L1 pinned its own variant (44042 B) before this seat finished re-keying. Mine differs in four places; two are
worth adopting, two are the L1's call:

1. **V2's gate environment (adopt).** The pinned copy runs `pkg_gate … --rerun` with the inherited environment, so
   P10 falls into `uv run --with biopython==1.85` (network + a managed CPython in `~/.cache/uv`). My copy passes
   `env` with the Bio stub and `TMPDIR=<work>` (measured `P10 ok probe_rerun=byte-equal`). This matters for the
   stage-2 gate run, not for a control.
2. **`plans/filler46/` is stale (replace).** The committed filler (`cf7de6a`) carries the earlier **16**-id dry
   table and receipt; the probe's frozen table has **18**. With the pinned counter's 18-key `DECISIVE`, V13's V10
   leg therefore defects on *pin alignment* rather than on the filler's content, which weakens the control. The
   regenerated `filler46/` here (`receipt.txt` `cf45c5f0…`, `dry-cases.txt` `a47f6b01…`) is the 18-id version; drop
   it in unchanged and V13 measures `substantive=V4,V7,V9,V10,V12`.
3. `DECISIVE`'s allowed-line sets differ per case (e.g. `nop`: mine `(17,18)`, pinned `(17,)`; `empty-file`: mine
   `(17,18)` reading an empty listing, pinned `(24,)` reading an empty source). Both are defensible readings of the
   same grader; the probe's own case descriptions settle it, and the pinned set is what the claim will be scored on.
4. Pins: mine leaves `SPEC_SHA256`/`PROBE_SHA256`/`DRY_SHA256` as `PENDING` and fails closed; the pinned copy fills
   them and masks `receipt_sha256` inside the spec digest (Q30 order). No behavioural difference in the legs.

## What the L1 must still do

1. Adopt §Delta 1 and §Delta 2 (or record why not).
2. Nothing else: the three pins, `DECISIVE` keys, spec rows `S166`–`S172`, capture dir and receipt path all match
   the landed bytes (`plans/pkg-spec-r46.json` → rows `S166…S172`, receipt
   `corpus/evidence/round46/polyglot-c-py-probe.txt`, capture dir `corpus/evidence/round46/tb2-polyglot-c-py`).

## Risks and limits

- **V11 is finite-sample equivalence, not non-memorization.** Per-run nonce and shuffle kill the three round-45
  table shapes; the lint kills a dict/set literal, a bit shift, a file read and a >4000-byte verbatim tuple; a
  wrong-but-close heuristic that agrees on this family, or a table small enough to pass review, is not excluded.
  Non-author review of the admitted block stays load-bearing.
- **The verified state family is literal-output** (each runtime's printed value is a literal in the source — the
  `constant` analogue of round 45) plus structural variants (listing, directory, compile, syntax, channel, format,
  newline). A predictor of an arbitrary computing polyglot is outside V11; the oracle's computing case is the
  probe's `oracle-solve-sh` (V5/V10).
- **V13 does not prove a passing package is non-filler**; it proves the committed filler is rejected by five of the
  six content legs.
- **V9 still derives its expected table from the receipt** (inherited): post-run tuning is caught only by V5 + V8's
  order gate, as the claims freeze.
- **V12 indexes the package capture dir on disk** (not `git ls-files`) so the filler is measurable before commit,
  and requires the row's digest to resolve to the spec row's own capture name — stricter than the round-46 rule.
- **V2's passing path is not exercised** (it needs a clean committed tree); its invocation, effective spec, gate
  echo and stub environment are. V8's passing path is likewise unexercised here.
- **PATH-dir digest change, unattributed.** The 02:18:26–02:18:57 brackets printed
  `before=after=ff187bb5c98aa6b5 unchanged`; every bracket from 02:24 on prints `7747d38e2042d398 … unchanged`.
  Between 02:18:57 and 02:22 the digest changed while no enveloped run of this seat was in flight; I installed
  nothing, and the one PATH-adjacent command I invoke (`uv run --no-project --with biopython==1.85`) was measured
  inside the envelope as `before=after=7747d38e2042d398 unchanged` (02:24:14). Each control bracket is internally
  valid.
- No probe case was executed and `pkg_gate --rerun` was never run on the landed package. V11 executes the captured
  `test_outputs.py` on the counter's own synthetic states (the round-45 V11 control precedent), not on the task
  image and not on any probe case.

## Evidence

`.ufo/waves/round-46/w1/R46ExecC3Counter/` — the counter, `filler46/`, seven receipts, `v11-reference-predictor.py`,
`dev/`. Scratch `/fast/scratch/hyaku/kengaku-r46/R46ExecC3Counter` is removed after this report with
`plans/scratch_guard.py safe-rm`.

VERDICT: c3-counter-checks-13-controls-failing-3/3
