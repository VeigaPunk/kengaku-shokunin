# R46ExecC3Counter — `plans/round46_c3_verify.py` (round 46, wave 1, C3 coverage)

Seat: executor, leaf. Scope executed: the C3 counter, the filler control package, the before-control receipts, and
read-only readings of the landed package through the counter's own legs. Nothing was written to the lane's
`corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `PROVINCE.md` or `README.md`; no git/jj mutation anywhere; no tool
installed; nothing added to a PATH directory. The lane moved under this seat (L1 commits `cf7de6a`, `420eec9`,
`e9d20145`, including its own pinned copy of this counter) — §Delta covers the difference.

## Axes

- **Coverage** (judged axis): 13 legs over byte-pinned captures, the gate at its round-45 digest, a held-out
  predictor over a dual-runtime *program* end state, its own anchor-line rule, and a filler package the content
  legs must reject.
- **Depth / calibration**: every leg's negative path measured before the freeze (three failing controls, six red
  predictors, two nonces); a satisfiable positive path demonstrated (11/11 legs ok on a shape-correct dev package);
  the landed rows and receipt read through the counter's own legs.
- **Operability**: three literal fills at stage 2 and no rewrite.

## Delivered

| path (under `.ufo/waves/round-46/w1/R46ExecC3Counter/`) | what | bytes / sha256 |
|---|---|---|
| `round46_c3_verify.py` | the counter, 932 lines, 13 checks | 44479 B, `54fec2796979da032c78d623f69b13de1d2ade88364ef815088bb7f5a42474df` |
| `filler46/` | control package (6 files + 8 captures + `SHA256SUMS`), probe-grammar 18 case ids | `receipt.txt` `4740dae3…`, `dry-cases.txt` `51e96d47…` |
| `control-base.txt`, `control-filler.txt`, `control-echo-receipt.txt` | the three stage-2 controls | each `PREDICATE C3 fail`, exit 1 |
| `control-positive.txt` | dev satisfiability control, 11 legs, `defects=0` | exit 0 |
| `control-v2-gate.txt` | V2's gate invocation with the Bio stub | `P10 ok probe_rerun=byte-equal bytes=2800` |
| `v11-predictors.txt`, `v11-predictors-run2.txt` | V11 reference `ok`; six reds refused; two nonces | exit 0 |
| `v11-reference-predictor.py` | lint-clean predictor with `disagree=0` (contract worked example, dev evidence) | 2326 B |
| `dev/` | dev drivers behind the two non-control receipts (`build_positive.py`, `positive.py`, `v11test.py`, `v2check.py`, `rebuild_positive.sh`) | — |

## The counter: V1–V13

`python3 plans/round46_c3_verify.py --lane .` prints one line per leg, then `checks=13 defects=<n>`, then
`PREDICATE C3 pass|fail`; exit 0 / 1. A leg that cannot run is a DEFECT, never a pass.

| leg | reads | fails when |
|---|---|---|
| V1 | `corpus/evidence/round46/tb2-polyglot-c-py/SHA256SUMS` vs a hardcoded 8-name digest table | a file's bytes, the name set or an extra file differ |
| V2 | `plans/pkg-spec-r46.json` (pinned), `plans/pkg_gate.py` (`ea6388…`) | a digest moved, or `pkg_gate package --rerun --require-clean-tree` exits non-zero |
| V3 | spec rows × registry | a row is not exactly one 11-cell registry row, or its anchor digest is not the spec pin |
| V4 | receipt vs frozen dry table | ids/order differ, the summary disagrees with the CASE lines, the `regrade cases=N differ=` line disagrees with the `regrade=DIFF:` CASE lines, a `match=NO` case is unnamed, or `match=yes` sits on a predicted≠observed line |
| V5 | probe + dry table at their pins | a pin is pending, a digest moved, or `probe --dry` is not byte-equal to the frozen table |
| V6 | `scripts/sources-census.sh validate` | the registry does not validate |
| V7 | `## Requirement map` vs receipt | a tag's line, derived label or cited violating case is wrong |
| V8 | `plans/order_check.py` | the order gate does not print `ORDER RESULT PASS` |
| V9 | entry vs receipt, PROVINCE.md, README `## Frontier` | case table ≠ receipt, a row id absent outside `source:`, provenance absent |
| V10 | `## Mechanism` vs receipt + `DECISIVE` | a row is missing, cites a non-decisive line, or its quote is not verbatim there |
| V11 | entry `## Predictor` + the captured grader | lint hit, predictor crash, any disagreement, or <8 passes / <8 fails |
| V12 | package rows, own anchor rule (not imported) | a quote off its line, a range not holding it, a wrong word count, or a digest not resolving to the row's own capture under the package capture dir |
| V13 | `plans/filler46/` | fewer than three of V3/V4/V7/V9/V10/V12 defect on the filler |

`DECISIVE` is keyed to the probe's frozen table and the landed bytes confirm it: 18 CASE ids in the same order
(`nop, oracle-solve-sh, lookup-table, python-only, c-only, extra-file, leftover-cmain, wrong-value, trailing-ws,
nonzero-exit, stderr-noise, n-parsed-differently, compile-warning, regrade-same-state, empty-file, dir-in-place,
crlf-source, value-plus-line`). A frozen case id absent from the map is a DEFECT.

**`regrade` is accounted, never judged.** The landed receipt carries `regrade cases=18 differ=7`, and the seven
`regrade=DIFF:F` cases are exactly the seven observed passes: `test_outputs.py:24` writes
`/app/polyglot/cmain` into the directory `:18` checked, so the grader is not idempotent on its own end state. That
is a measured property of the task (the probe's `regrade-same-state` case), so V4 only requires the `differ=` count
to equal the number of `regrade=DIFF:` CASE lines — not that a pass reproduce.

## V11: the held-out predictor over `(listing, source)`

The entry's `## Predictor` defines `predict(files, source) -> bool`: `files` is `/app/polyglot`'s listing before
compilation, `source` the text of `main.py.c` (`None` when no readable regular file of that name exists). Each run
builds **60 fresh end states in 20 kinds**: values, decoy literals, padding, the extra file's name, a banner
comment and the state order come from `os.urandom`, so no committed byte determines a verdict. Each state is
written into a scratch `/app/polyglot` and graded by the **captured** `test_outputs.py` (`b94a7a98…`) inside
bubblewrap with host `gcc` and `python3`; `predict` runs in a second sandbox; only
`states= grader_pass= grader_fail= disagree=` is printed.

```
V11 reference              ok states=60 grader_pass=15 grader_fail=45 disagree=0
V11 always-true            DEFECT … disagree=45
V11 always-false           DEFECT … disagree=15
V11 shift-table            DEFECT predictor lint tokens present: >>
V11 dict-table             DEFECT predictor lint tokens present: {,}
V11 verbatim-tuple         DEFECT predictor lint tokens present: >4000bytes
V11 file-read              DEFECT predictor lint tokens present: import
ENVELOPE end 02:38:35 exit=0 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
ENVELOPE end 02:38:42 exit=0 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
```
Two runs, different nonces (`v11-predictors.txt`, `v11-predictors-run2.txt`); the reference scores identically in
both. Kind list: `literal-ok`, `literal-ok-padded`, `literal-ok-trailing`, `literal-ok-crlf-source`,
`literal-ok-no-eof-newline` (pass); `wrong42`, `wrong10`, `zero-ignore-k`, `stderr-py`, `stderr-c`, `float-py`,
`float-c`, `no-print-py`, `no-print-c`, `extra-file`, `stale-cmain`, `wrong-name`, `dir-main`, `c-syntax-error`,
`py-syntax-error` (fail). Every verdict comes from executing the grader; none is stored.

## V13 and the filler package

`filler46/` is right-shaped and establishes nothing: an 11-cell registry row per spec row with the filler capture's
real digest in the anchor, a dry table and receipt in the **probe's own grammar** (`regrade=` and `end=` fields,
18 case ids, a `regrade cases=18 differ=0` line), an entry carrying every section. Its defects are content defects
— every anchor quote sits on no line it cites; every requirement label is stated; the case table holds one
do-nothing row against eighteen receipt cases; the mechanism row cites a non-decisive line; one CASE line claims
`match=yes` with `predicted=pass observed=fail`. V13 requires **≥3 substantive** legs; measured
`substantive=V4,V7,V9,V10,V12`.

## Controls measured (round-46 envelope; PATH-dir content digest unchanged in every bracket)

```
PACKAGE unreadable: spec pin pending: SPEC_SHA256 is a stage-2 placeholder
V1 .. V12 DEFECT package unreadable: …   V13 ok filler_checks=7 defects=6 substantive=V4,V7,V9,V10,V12
checks=13 defects=12
PREDICATE C3 fail
ENVELOPE end 02:38:18 exit=1 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
```
base tree (`control-base.txt`, exit 1).

```
V3 ok rows=7 bad=0
V4 DEFECT cases=18 mismatches_named=0/0 bad=["match=yes on a mismatching case: ['nonzero-exit']"]
V6 DEFECT census_exit=1 registry=plans/filler46/SOURCES-filler.md
V7 DEFECT rows=4 tags=4 bad=['single-file: no receipt case violates it', …]
V9 DEFECT case_rows=1/18 bad=['case table rows=1 receipt cases=18 equal=False', …]
V10 DEFECT mechanism_rows=1/18 bad=['mechanism rows=1 receipt cases=18 ids_equal=False', …]
V12 DEFECT rows=7 defective=7 live=7 first=S166:line,words
checks=7 defects=6
PREDICATE C3 fail
ENVELOPE end 02:38:20 exit=1 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
```
filler package, `--filler` (`control-filler.txt`, exit 1).

```
V4 DEFECT cases=18 … bad=['case ids differ from the frozen table', 'summary line count != 1',
                          'regrade summary line count != 1']
V10 DEFECT mechanism_rows=1/18 …
checks=7 defects=6
PREDICATE C3 fail
ENVELOPE end 02:38:28 exit=1 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
```
echo receipt — the filler's dry table copied over its receipt (`control-echo-receipt.txt`, exit 1; restored
byte-identically, `cmp` clean).

Satisfiability, dev copy only (`control-positive.txt`; shape-correct package in the scratch clone, never committed):

```
V1 ok listed=8 wrong=0 extra=0   V3 ok rows=7 bad=0    V4 ok cases=18 … bad=0   V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0              V7 ok rows=5 tags=5 bad=0                      V9 ok case_rows=18/18 bad=0
V10 ok mechanism_rows=18/18      V11 ok states=60 grader_pass=15 grader_fail=45 disagree=0
V12 ok rows=7 defective=0 live=0 V13 ok filler_checks=7 defects=6 substantive=V4,V7,V9,V10,V12
DEV POSITIVE checks=11 defects=0
ENVELOPE end 02:38:01 exit=0 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
```
with `plans/dev_pinned_c3_verify.py` (this counter, three `PENDING` pins replaced by the dev tree's digests,
`70f236da…`).

V2's gate path (`control-v2-gate.txt`, dev tree): `P1 ok pinned=1`, `P2 ok receipt_sha256=pinned`, `P4 ok
checked=12`, `P5 ok manifest_entries=8`, `P6 ok rows=7`, `P7 ok source_lines=7`, `P8 ok index_rows=53`,
`P10 ok probe_rerun=byte-equal bytes=2800`; `P3`/`P9` defective on dev content only (one 2-word quote in the dev
entry; untracked dev files — this item authorises no scratch commit). `P10` is the point: V2 hands the gate a stub
`Bio` on `PYTHONPATH` and `TMPDIR=<work>`, so `pkg_gate`'s `import Bio` branch stays on host python3 instead of
fetching numpy 15.9 MiB + biopython 3.1 MiB and provisioning a managed CPython under `~/.cache/uv`.

## The landed package, read-only through this counter's legs

Against the real lane at `e9d20145`, with the landed spec, captures, dry table, probe and registry, and the entry
still absent (another seat owns it):

- `V1 ok listed=8 wrong=0 extra=0` — the manifest matches the counter's hardcoded 8 pins.
- `V3 ok rows=7 bad=0` — rows S166–S172 carry their own anchor digests.
- `V12 ok rows=7 defective=0 live=0` — every quote sits on its cited line, every range holds it, every word count
  and digest-resolves-to-own-capture check passes.
- the receipt parses to 18 cases, no `match=NO`, no false `match=yes`, `regrade cases=18 differ=7` against seven
  `regrade=DIFF:` lines, summary `cases=18 observed_pass=7 observed_fail=11 mismatches=0`.
- `DECISIVE`'s 18 keys equal the dry table's ids in order; `plans/polyglot_c_py_probe.py --dry` hashes to
  `99adfea6…`, byte-equal to the frozen table (measured under the envelope, `ENVELOPE end 02:38:57 exit=0 … unchanged`).
- the receipt (`dd0e3546…`, 6613 B) declares its inputs in `# capture <name> sha256=<digest>` lines: 7 of them, and
  every declared digest equals this counter's pin for that name (`gitignore` is row-less and undeclared, as the spec
  seat intended).

**Receipt-to-probe provenance: closed (producer == pin).** `plans/polyglot_c_py_probe.py` in the lane is
`67a8f4a6…` (27966 B), and it is the revision that produced `corpus/evidence/round46/polyglot-c-py-probe.txt`
(`dd0e3546…`): the L1 pinned the probe at `cf7de6a` *before* the first recorded run (`8d7f74ce`) and ruled that the
hardened draft (`22b7779e…`, 31355 B) does not land this round — it is carried as a round-47 sandbox improvement.
So V2's `--rerun` is a **reproduction** test of a receipt whose producer is the pin, not a re-pin of a newer probe
against an older receipt; nothing in this counter needs to move. If that ruling is ever flipped, the sequence is:
land the terminal bytes, move `PROBE_SHA256` in the same commit, then read V2's P10 byte-compare for the receipt (and
regenerate + re-pin `receipt_sha256` if P10 disagrees).

## Delta to the pinned copy (`plans/round46_c3_verify.py` @ `e9d20145`, sha `a971c24d…`)

1. **V2's gate environment (adopt).** The pinned copy runs `pkg_gate … --rerun` with the inherited environment, so
   P10 falls into `uv run --with biopython==1.85` (network + a managed CPython in `~/.cache/uv`). Mine passes `env`
   with the Bio stub and `TMPDIR=<work>`: measured `P10 ok probe_rerun=byte-equal`.
2. **V4's `regrade` accounting (adopt).** The pinned copy ignores the `regrade cases=18 differ=` line; mine requires
   it to equal the number of `regrade=DIFF:` CASE lines. It passes on the landed receipt and catches a receipt whose
   re-grade column and summary disagree.
3. **`plans/filler46/` is stale (replace).** The committed filler (`cf7de6a`) carries the earlier **16**-id dry
   table and a round-45-shaped receipt; the probe's frozen table has **18** ids and two extra fields. With the pinned
   counter's 18-key `DECISIVE`, V13's V10 leg currently defects on *pin alignment* instead of the filler's content.
   The `filler46/` here is the 18-id, probe-grammar version — drop it in unchanged.
4. `DECISIVE`'s allowed-line sets differ per case (e.g. `nop`: mine `(17,18)`, pinned `(17,)`; `empty-file`: mine
   `(17,18)` reading an empty listing, pinned `(24,)` reading an empty source). Both are defensible readings of the
   same grader; the probe's case descriptions settle it, and the pinned set is what gets scored.
5. **Probe revision: resolved by the L1, no action.** The pin `67a8f4a6…` (27966 B) is the revision that produced
   the receipt, pinned before the first recorded run; the hardened draft `22b7779e…` is out of this wave (round-47).
   V2's `--rerun` therefore reproduces the pin's own receipt. Nothing moves here.
6. Pins: mine leaves `SPEC_SHA256`/`PROBE_SHA256`/`DRY_SHA256` as `PENDING` and fails closed; the pinned copy fills
   them and masks `receipt_sha256` inside the spec digest (Q30 order). No behavioural difference in the legs.

## Risks and limits

- **V11 is finite-sample equivalence, not non-memorization.** Per-run nonce and shuffle kill the three round-45 table
  shapes; the lint kills a dict/set literal, a bit shift, a file read and a >4000-byte verbatim tuple; a
  wrong-but-close heuristic that agrees on this family, or a table small enough to pass review, is not excluded.
  Non-author review of the admitted block stays load-bearing.
- **The verified state family is literal-output** (each runtime's printed value is a literal in the source — the
  `constant` analogue of round 45) plus structural variants (listing, directory, compile, syntax, channel, format,
  newline). A predictor of an arbitrary computing polyglot is outside V11; the oracle's computing case is the probe's
  `oracle-solve-sh` (V5/V10). A lookup-shaped predictor is not distinguishable from a computing one here, which is
  the probe's own `lookup-table` finding.
- **V13 does not prove a passing package is non-filler**; it proves the committed filler is rejected by five content
  legs.
- **V9 still derives its expected table from the receipt** (inherited): post-run tuning is caught only by V5 + V8's
  order gate, as the claims freeze.
- **V12 indexes the package capture dir on disk** (not `git ls-files`) so the filler is measurable before commit, and
  requires the row's digest to resolve to the spec row's own capture name — stricter than the round-46 rule.
- **V2's passing path is not exercised** (it needs a clean committed tree); its invocation, effective spec, gate echo
  and stub environment are. V8's passing path is likewise unexercised here.
- **PATH-dir digest change, unattributed.** The 02:18:26–02:18:57 brackets printed
  `before=after=ff187bb5c98aa6b5 unchanged`; every bracket from 02:24 on prints `7747d38e2042d398 … unchanged`.
  Between 02:18:57 and 02:22 the digest changed while no enveloped run of this seat was in flight; I installed
  nothing, and the one PATH-adjacent command I invoke (`uv run --no-project --with biopython==1.85`) was measured
  inside the envelope as unchanged.
- No probe case was executed and `pkg_gate --rerun` was never run on the landed package. V11 executes the captured
  `test_outputs.py` on the counter's own synthetic states (the round-45 V11 control precedent), not on the task image
  and not on any probe case; the only probe invocation was `--dry`, for the byte-compare above.

## Evidence

`.ufo/waves/round-46/w1/R46ExecC3Counter/` — the counter, `filler46/`, seven receipts, `v11-reference-predictor.py`,
`dev/`. Scratch `/fast/scratch/hyaku/kengaku-r46/R46ExecC3Counter` is removed after this report with
`plans/scratch_guard.py safe-rm`.

VERDICT: c3-counter-checks-13-controls-failing-3/3
