# F38C2Rerun — C2 re-run, probe determinism, manifest and counter sensitivity (round 38, wave 2 FALSIFY)

Seat: executor `F38C2Rerun`. Attacked object: the wave-1 C2 landing on tip
`8c7422d7a646515d80af44844e8ecc8a1fc1d30a` — the frozen C2 counter
`plans/round38_c2_verify.py`, the probe `plans/build_pmars_probe.py`, the receipt
`corpus/evidence/round38/build-pmars-probe.txt`, the dry table, the capture manifest, and the
entry's derived requirement map. Nothing in the lane was written; all writes went to
`/fast/scratch/hyaku/kengaku-r38/F38C2Rerun/` (now deleted) and to
`.ufo/waves/round-38/falsify/F38C2Rerun/`.

Clone (as prescribed, every git call with `-C "$S/lane"`, no commit, no jj/git mutation of the lane):

```
$ git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane" && \
  git -C "$S/lane" checkout -q 8c7422d7a646515d80af44844e8ecc8a1fc1d30a
toplevel=/fast/scratch/hyaku/kengaku-r38/F38C2Rerun/lane
head=8c7422d7a646515d80af44844e8ecc8a1fc1d30a
status: (empty)
```

Axes I attacked: (a) predicate reproduction, (b) probe determinism / receipt fidelity,
(c) capture provenance, (d) counter sensitivity (is it able to be red?), (e) counter
causality (do the verdicts come from the grader or from constants?), (f) the "before" control,
(g) no-harm on the round-37 counter, (h) the entry's quote and map claims.

---

## 1. Frozen predicate reproduces exactly — PASS

```
$ cd CLONE && python3 plans/round38_c2_verify.py --lane .
V1 ok listed=5 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=28 distinct_quotes=28 distinct_lines=27 out_of_word_range=0
    gate: P4 ok checked=28 bad=0 first=0
    gate: P5 ok manifest_entries=5 bad=0 first=0
    gate: P6 ok rows=2 bad=0 first=0
    gate: P7 ok source_lines=2 bad=0 first=0
    gate: P8 ok index_rows=45 knowledge_files=45 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=5537
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=2 bad=0
V4 ok cases=22 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=7 tags=7 bad=0
checks=7 defects=0
PREDICATE C2 pass
EXIT=0
```
(receipt: `F38C2Rerun/c2-counter-clean-clone.txt`). This is the claim's exact command, exact
predicate, exit 0. Note the predicate was measured while the gate's `P10` itself re-ran the probe
inside the clone (`probe_rerun=byte-equal bytes=5537`) — a fourth independent byte-equal run,
inside the scored command.

## 2. Probe determinism: three re-runs, byte-equal to the receipt — PASS

| run | environment | sha256 | bytes |
|---|---|---|---|
| A | plain, `--work wA` | `2408b477b0299e1339064b4b3df968a00174b3a5999016073b5fe4fd8cbb4ef9` | 5537 |
| B | plain, `--work wB` (different scratch parent) | `2408b477…cbb4ef9` | 5537 |
| C | `env -i PATH=/usr/bin:/bin LC_ALL=C TZ=Asia/Tokyo TERM=dumb`, `umask 077`, `cwd=/`, absolute `--lane` | `2408b477…cbb4ef9` | 5537 |
| receipt | `corpus/evidence/round38/build-pmars-probe.txt` | `2408b477…cbb4ef9` | 5537 |

```
$ cmp runA.txt corpus/evidence/round38/build-pmars-probe.txt   -> IDENTICAL
$ cmp runB.txt corpus/evidence/round38/build-pmars-probe.txt   -> IDENTICAL
$ cmp runC.txt corpus/evidence/round38/build-pmars-probe.txt   -> IDENTICAL
$ cmp runA.txt runB.txt                                        -> IDENTICAL
$ grep '^cases=' runA.txt
cases=22 observed_pass=7 observed_fail=15 mismatches=0
```
Receipt `F38C2Rerun/probe-rerun.txt`. Stripped environment, a different locale/timezone,
`cwd=/` and a restrictive umask change nothing: the receipt is reproducible, not host-tinted.

## 3. `--dry` byte-equal to the frozen case table; case-id sets identical — PASS

```
$ python3 plans/build_pmars_probe.py --lane . --dry > dryA.txt
sha256 dryA.txt = 93b4b60cfe132ffe13b5d350589feb40c4a87a225b7de42d50dc79a99f4d4df0  (4321 bytes)
freeze table    = 93b4b60cfe132ffe13b5d350589feb40c4a87a225b7de42d50dc79a99f4d4df0  (4321 bytes)
$ cmp dryA.txt corpus/evidence/round38/build-pmars-dry-cases-freeze.txt -> IDENTICAL
$ diff <receipt case ids> <dry case ids> -> (empty)   # 22 and 22, IDS IDENTICAL
```
Receipts: `dry-cmp.txt`, `dryA.txt`. The receipt's `CASE` id sequence is the frozen table's
sequence, so no case was added, dropped or reordered between prediction and run.

## 4. Capture manifest verifies — PASS (5/5)

```
$ cd CLONE/corpus/evidence/round38/tb2-build-pmars && sha256sum -c SHA256SUMS
instruction.md: OK
solve.sh: OK
task.toml: OK
test.sh: OK
test_outputs.py: OK
EXIT=0
```
Receipt: `manifest-check.txt`.

## 5. Capture provenance re-verified against upstream, live (not just the pins) — PASS, with one gap

I fetched the pinned commit directly (network reachable from this seat) and compared bytes:

```
2fd12b88 / build-pmars/ :  instruction.md 528 b 1606850…f3b82 | task.toml 1012 b 7ee2eac…9cd
                           tests/test.sh 608 b 4770437…334  | tests/test_outputs.py 2938 b d9d2796…e85
solution/solve.sh       :  923 b 105292c…543
MATCH instruction.md <= upstream instruction.md
MATCH solve.sh <= upstream solution/solve.sh
MATCH task.toml <= upstream task.toml
MATCH test.sh <= upstream tests/test.sh
MATCH test_outputs.py <= upstream tests/test_outputs.py
main branch, both pinned rows: 1606850…f3b82 / d9d2796…e85  (byte-equal to the pin)
```
Receipt: `upstream-check.txt`. So the claim "upstream `main` byte-equal at freeze for both" holds at
re-check time too, and all five captures — not only the two SOURCES rows — are the pinned upstream
bytes.

**Gap (non-fatal, recorded not scored):** `build-pmars/solve.sh` is HTTP 404 upstream; the capture
`corpus/evidence/round38/tb2-build-pmars/solve.sh` is byte-equal to upstream
**`solution/solve.sh`**. The mapping lives only in the counter's `CAPTURES`/`SHA256SUMS`, and
`corpus/SOURCES.md` rows S115/S116 cover only `tests/test_outputs.py` and `instruction.md`. Three of
the five captures (`solve.sh`, `task.toml`, `test.sh`) therefore have no SOURCES row naming their
upstream path. The claims never say otherwise ("S115 `tests/test_outputs.py`, S116
`instruction.md`"), so this is not a claim breach — it is an unrowed provenance edge a later
reader cannot see from SOURCES alone.

## 6. Counter sensitivity: eight mutations, every one turns it red — the counter is not vacuous

On a byte-identical copy of the clone (`tamper`), restoring the original bytes after each test:

| tamper | what it attacks | counter result |
|---|---|---|
| baseline | (no change) | `checks=7 defects=0`, pass (receipt `tamper-baseline.txt`) |
| A: `debugger-works` label `partly`→`enforced` | the round-37 D2 fix (V7) | `V7 DEFECT … bad=['debugger-works: labelled enforced, receipt derives partly']` |
| B: one receipt `observed=fail`→`observed=pass` | receipt honesty | `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt` + `V4 … 'summary disagrees with the CASE lines'` |
| C: 1-bit flip in `test_outputs.py` capture | capture pinning | `V1 DEFECT bad=['test_outputs.py']`, `gate: P5 … manifest digest does not match the bytes`, `P10 … exit=2 stderr='SETUP capture … not at its pinned digest'` |
| D: `match=yes`→`NO` on a case that is already named | V4 naming rule | `mismatches_named=1/1 bad=0` — inconclusive by construction (`tamper-D-README.txt`); superseded by G |
| E: extra unlisted file in the capture dir | capture completeness | `gate: P5 … extra.bin: capture file not covered by the manifest`, `P9 … untracked=1` |
| F: `## Requirement map` header renamed | V7 section gate | `V7 DEFECT no '## Requirement map' section` |
| G: `match=NO` + `mismatches=1` + the case's name stripped from the entry | V4 naming rule, isolated | `V4 DEFECT … bad=["mismatch cases not named in the entry: ['empty-tree']"]` |
| H: one requirement-map row deleted | V7 completeness | `V7 DEFECT … bad=["tags missing=['results-format'] duplicated=0"]` |

Every tamper file restored (`restored-equal: True True True True`, `git status --porcelain` empty).
Receipts: `tamper-*.txt`. The D2 fix advertised in the claims is demonstrably load-bearing: a label
chosen against one witness case is now a red predicate, and a *missing* row is red too.

## 7. Causality: the verdicts come from executing the captured grader, not from constants — PASS

Two mutational attacks on the probe's own dependency (probe copied to scratch, its `PINS` digest
retargeted at a mutated grader, run against a scratch capture dir):

```
M1 grader whose four tests do nothing:
  cases=22 observed_pass=22 observed_fail=0 mismatches=15
  e.g. "CASE empty-tree predicted=fail observed=pass tests=PPPP"
M2 the real grader with `assert False` prepended to test_headless_no_x11:
  cases=22 observed_pass=0 observed_fail=22 mismatches=18
  e.g. "CASE canned-shape predicted=pass observed=fail tests=PFPP"   (was PPPP)
```
Receipts: `fake-noop-grader.txt`, `fake-fail-second-test.txt`. A no-op grader flips 15 cases to
pass; a single injected assertion flips position 2 of every case and changes 18 case verdicts. The
22 recorded verdicts are therefore caused by real grader execution against the staged artefacts —
they cannot be produced by the constant `predicted_tests` strings.

## 8. The "before" control reproduces — PASS

```
$ git -C "$S/freeze" checkout -q e0a378539a45cc9388c66cfba22f44275131de23
$ python3 plans/round38_c2_verify.py --lane .      # cwd = freeze tree
V1 ok listed=5 bad=0 extra=0
V2 DEFECT spec=frozen gate=frozen gate_exit=1
V3 DEFECT rows=2 bad=['S115:row', 'S116:row']
V4 DEFECT receipt or entry absent
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 DEFECT receipt or entry absent
checks=7 defects=4
PREDICATE C2 fail
EXIT=1
```
Receipt: `control-c2-nothing-rerun.txt`. Identical to
`.ufo/waves/round-38/claims/control-c2-nothing.txt` at the bottom (`checks=7 defects=4`,
`PREDICATE C2 fail`), same four red checks (V2, V3, V4, V7) and the same three green ones. The
"before" number is real, and the delta 4→0 defects is the landing, not a changed measuring stick
(V5 already green at the freeze: probe and dry table existed at their frozen digests before the
landing — exactly as the claims' disclosure says).

## 9. No-harm: the round-37 C2 counter still passes at the landing tip — PASS

```
$ python3 plans/round37_c2_verify.py --lane .   (53 s)
V1 ok listed=6 bad=0 extra=0 … V7 ok rows=4 bad=0
checks=7 defects=0
PREDICATE C2 pass
EXIT=0
```
Receipt: `round37-c2-noharm.txt`.

## 10. The entry's quotes and derived map survive independent re-derivation — PASS

Independent of the gate, I parsed the `## Located quotes` table myself (curly quotes, `file:line`
in the last cell, one row whose quote contains a pipe) and checked each quote for verbatim presence
at the cited line and 3–25 words:

```
independent_quote_check rows=28 files=['instruction.md', 'test_outputs.py'] bad=0
```
Receipt: `quote-check.txt` (the gate's own P3/P4 agreed: `rows=28 distinct_quotes=28
out_of_word_range=0`, `checked=28 bad=0`).

Independent re-derivation of the requirement map from the receipt's own `violates=` sets:
```
from-source n=22 pass=7 fail=15 partly | no-x11 n=3 pass=1 fail=2 partly
debian-source n=22 pass=7 fail=15 partly | extract-to-app n=22 … partly
install-path n=4 pass=1 fail=3 partly  | results-format n=5 pass=1 fail=4 partly
debugger-works n=22 pass=7 fail=15 partly
```
Receipt: `derive-labels.txt`. All seven `partly`, and the narrow violating sets are exactly the
entry's stated `no-x11` (3), `install-path` (4), `results-format` (5). The map's labels are a
function of all violating cases, not of one witness.

---

## Findings that landed (none fatal to the C2 claim)

1. **V6 depends on an unpinned file outside the clone.** `round38_c2_verify.py:49` —
   `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`; `frozen_instruments` in
   `plans/pkg-spec-r38.json` pins only the probe and the gate (`"census pinned in spec: False"`).
   Recorded at check time: sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`,
   35466 bytes, `census_exit=0`. The frozen predicate is phrased as "measured on a clean clone of
   the landing tip", yet one of seven checks reads host state. It is green today and cannot be shown
   red by anything inside the clone; a host change to that script could move V6 without any lane
   change. Recorded as an operational limit of the counter, not as a predicate failure.
   (Similarly the counter's V2 gate subprocess prints `exit=` codes only; fine.)
2. **V4's mismatch-naming branch is vacuous at the tip** — `mismatches_named=0/0` because the
   receipt has `mismatches=0`. The branch is real (tamper G fires with the exact message) but no
   landing datum exercises it; a receipt whose predictions all match carries no evidence for the
   naming rule itself.
3. **Operability, minor:** the probe's `--work` parent must already exist:
   `tempfile.mkdtemp(…, dir=a.work)` raised `FileNotFoundError: … /wC/k38-bpm-…` on a missing
   `--work` directory (my first determinism attempt; reproduced, and irrelevant to the scored path
   because the counter calls the probe without `--work`, using a live `TMPDIR`). A seat with a
   stale `TMPDIR` would see a traceback rather than a diagnostic.
4. **Order-of-operations is not falsifiable from the tree.** That predictions predate the first
   recorded run cannot be verified; what is verifiable is that the probe, dry table, receipt and
   captures are byte-frozen together and that `P10` ties the receipt to fresh execution (tamper B
   shows a hand-edited receipt is red). Recorded as a limit, not a finding.
5. The disclosure's residual risk — a hand-typed receipt whose observed verdicts copy the
   predictions — is closed by P10 in practice, not by inspection: tamper B (one flipped verdict)
   produced `P10 DEFECT fresh probe output is not byte-equal to the receipt`.

## Coverage judgement

The C2 predicate (`checks=7 defects=0`, `PREDICATE C2 pass`, exit 0) reproduces on a clean clone of
the landing tip, with a receipt that is byte-identical across three independent re-runs (one under a
stripped environment) and with all five captures byte-equal to the pinned upstream commit. The
counter is not a rubber stamp: eight mutations across five checks turn it red, one of them the exact
round-37 D2 shape. The recorded verdicts are causally produced by the captured grader. No claim in
the C2 row was falsified; five limits are recorded above.

Tooling: nothing installed (no pacman, no `uv tool`, no npx — none needed). Scratch
`/fast/scratch/hyaku/kengaku-r38/F38C2Rerun/` deleted before finishing; receipts preserved in
`F38C2Rerun/`.

VERDICT: c2-rerun-pass-probe-byte-equal-yes
