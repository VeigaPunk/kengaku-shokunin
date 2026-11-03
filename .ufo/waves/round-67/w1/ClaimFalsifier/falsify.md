# ClaimFalsifier-5 — round 67 w1 — adversarial falsification of R67-C1 and R67-C2

Seat: ClaimFalsifier-5. Read-only on L except W/ClaimFalsifier/ and the Report file.
Scratch: /fast/scratch/hyaku/kengaku-r67/ClaimFalsifier (removed before yield; cited receipts copied to W/ClaimFalsifier/ first).
Claims frozen in plans/round-67-claims.md at commit dcc39ea3. Nothing below edits a frozen rule.

---

## A1 (C1) — can a non-compliant implementation earn a frozen vector it should not?

Variant chosen: `a7-hooksplit-nocomm` — a `pipeline_parallel.py` that (1) registers a no-op forward
hook by building the name at runtime (`getattr(torch.nn.Module, "register_" + "forward_hook")`),
(2) never partitions, (3) never calls dist.send/dist.recv: per microbatch it runs the full model,
computes CE/targets loss divided by the microbatch count, and calls backward. It violates the
instruction (S239: "You must not use hooks inside your implementation") and the partition and
communication requirements; it is NOT any of the six frozen cases.

### Prediction (written BEFORE the run, from grader lines corpus/evidence/round67/sources/torch-pipeline-parallelism-test_outputs.py)

- `exists` (:19-27): /app/pipeline_parallel.py exists → **P**.
- `no_hooks` (:31-41): the test is a pure substring match for the two literals
  `register_forward_hook` / `register_full_backward_hook`; the runtime-built name
  `"register_" + "forward_hook"` contains neither literal → **P**.
- `ws1` (:91-169, world_size=1): import succeeds; all eight hooked modules fire during each full
  forward → `num_layers` = 8 (lm_head, embed_tokens, layers.0-3, norm, rotary_emb), and :144's
  bound is `<= (4+4)//1 + 1 = 9` → passes. All eight `.fwd` keys are inserted during microbatch 0's
  forward, before microbatch 0's backward inserts any `.bwd` key; `setdefault` keeps insertion
  order, so the AFAB order check at :152-157 never fires. Values: the reference loop (:121-135) is
  the identical computation (full model per microbatch, CE/4, same seed, same state dict) →
  allclose at atol=1e-5 → **P**.
- `ws2` (world_size=2; NOT run — item constrains the run to world size 1): each rank runs all eight
  modules → `num_layers` = 8 > 5 → :144 assertion fails on both ranks before any barrier → **F**.

**Predicted full vector: `PPPF`** — coincides with q5-full-model's frozen row, but by a mechanism
the frozen table does not anticipate: q5 is hook-free; this variant uses a hook in the
implementation and still passes `no_hooks`. The frozen table's q4 row establishes only
"literal present → no_hooks fails"; nothing in the table or in named limitations (i)/(ii) covers
"hook used, literal evaded → no_hooks passes". If observed, the grader's `no_hooks` leg is a
string match, not a hook detector, and the table's implicit mapping (no_hooks=P ⟺ no hooks in the
implementation) is falsable while C1's six frozen vectors themselves stand.

### Observed (2026-11-03, world size 1 only, under the port lock)

Command: `flock /home/vgpnk/.local/share/kengaku-r67/port-12355.lock bwrap …` mirroring the probe's
`run_case` sandbox exactly, `pytest -k "not 2"` (ws1 only), app = the variant above. Exit 0,
`3 passed, 1 deselected in 3.97s`. junit copied to `a1-hooksplit-ws1.junit.xml`
(sha256 `16caad1502da17cce69d3b3abfad262f99c31a6b7c6cecc82bf6fc759dac000a`); variant file sha256
`f785990ff474936c25ba1d39cb5746e222a1343feb07f88add7332fb0903ea0e`.

- `test_pipeline_parallel_exists` **P**, `test_no_hooks_in_pipeline_parallel` **P**,
  `test_pipeline_parallel[1]` **P**; `[2]` deselected (item constraint), predicted **F** by the
  :144 layer-count bound (8 > 5).

**Verdict: C1 survives (the six frozen vectors are untouched by this attack), but the frozen table
is NOT a complete compliance oracle.** A 7th, non-compliant implementation — hook registered in the
implementation via a runtime-built name, no partition, no send/recv — earns `exists=P no_hooks=P
ws1=P` (observed) and would earn `PPPF` at a full run (predicted from :144). The frozen table has
no row for "hooks used, literal evaded": its only hook-using row (q4) fails `no_hooks` only because
the literal is written out. `no_hooks` is a substring match (:31-41), not a hook detector, and the
implementation can violate S239's "You must not use hooks inside your implementation" while the
grader prints green. Named limitation (i) (AFAB vs 1F1B) and (ii) (transformers pin) do not cover
this; the claims doc should name it. The frozen table would NOT have been wrong about any of its
six cases — each rationale line number (:19, :31, :91-169, :144, :154-157, :171-178) was
re-verified against the capture by grep.

---

## A2 (C1) — can --check-receipt be satisfied by a fabricated receipt?

**BROKEN THROUGH: yes.** Fabricated pair built in scratch from the committed bytes only — no
grader run anywhere in the loop:

- `a2-fab/receipt.txt`: header + `PROBE sha256=32bacf1d… version=r67-c1/1` + `GRADER sha256=2357…`
  + `VENV …` lines copied verbatim from the committed receipt; six `CASE` lines with the TRUE
  committed `case_sha256` values (lifted from the committed receipt), `junit_sha256` recomputed
  over MY hand-written junits, plausible `rc`; six `VECTOR` lines equal to the frozen table.
- `a2-fab/receipt.junit/q{1,3,4,5,6}-none.xml`: six hand-written junit XMLs whose per-testcase
  outcomes spell the frozen vectors (real pytest-shaped: `testsuite name="pytest"`,
  `hostname="fabricated"`, `timestamp="2026-11-03T00:00:00.000000"`, zero times, one-line
  fabricated `<failure>` messages).

Command: `python3 plans/round67_c1_pipeline_probe.py --check-receipt $S/a2-fab/receipt.txt`
(from the lane root; committed probe, unmodified). **Exit 0, `CHECK ok cases=6`,
`PREDICATE R67-C1 pass`.** Evidence copied to `a2-fabricated/` (receipt sha256
`0387c9582fb5c71875d8f0eab097b12673c12cab78c429c4631684b2f7ff6d95`).

The checker is not trivial to fool — two intermediate forgeries were refused (exit 1): an extra
`<testcase name="collector">` row ("unexpected testcase name"), and stale junit hashes after an
edit ("junit sha mismatch"). It re-derives every vector from the junit bytes and binds every
junit sha. But nothing binds the junit BYTES to a pytest run: hostname, timestamp, times and
failure text are uninspected, and case provenance anchors only to the committed case files, which
a forger can hash. The committed record receipt is anchored by git, so the predicate over the
RECORD receipt stands (verified: `--check-receipt corpus/evidence/round67/pipe/receipt.txt` →
rc 0, `PREDICATE R67-C1 pass`) — but the exact predicate command, pointed at any
self-consistent copy, is satisfiable without a run.

**Named-limitation coverage: NO.** C1's named limitations are (i) AFAB-vs-1F1B and (ii) the
transformers pin; neither mentions receipt provenance. C2's claims text DOES name the analogous
limitation for its own gate ("a receipt that copies every value from the committed bytes still
passes strict"); C1 lacks the sibling sentence. Smallest safe correction: add the C1 named
limitation ("`--check-receipt` re-derives consistency with the frozen table and the committed
case/grader bytes; the junit bytes themselves carry no run-provenance anchor — a hand-forged
consistent pair passes") — a disclosure fix, not a kill: kill rules (a)/(b)/(c) are all untouched
by this attack.

---

## A3 (C2) — does the strict clause set accept any fabricated fixture other than the committed one?

**YES — demonstrated twice.** The committed probe has no `--strict` yet (this round's C2 build
adds it), so I re-implemented s1-s6 exactly as frozen in
`strict_reimpl.py` (copied to this seat dir), with every clause constant imported from the
committed probe bytes (PROBE_VERSION `r65-c1/1`, GRADER sha `b165f85…`, AMALG sha `0a9c8e34…`,
FROZEN_VECTORS, CASES). "Every NOBIND line carries delta=0" was scoped to the per-case NOBIND
lines — see the ambiguity note below.

Runs (`python3 strict_reimpl.py <fixture>`; batch rc reflects the expected refusal):

| fixture | strict re-impl (s1-s6) | committed probe, default mode |
|---|---|---|
| committed `round65/sqlite-gcov-probe.txt` | **ACCEPT** (0 defects) | `CHECK ok cases=5`, pass, rc 0 |
| committed `round66/red/fabricated-r65.txt` | **REFUSE** — 24 defects (s1 header missing; s4 gcc/gcov/bwrap fabricated; s5 all five RUN rc/driver wrong, FILES/ENV missing) | `CHECK ok cases=5`, pass, rc 0 (M-1 defect re-confirmed in the default gate) |
| `forge1-env-version.txt` = committed receipt with ONLY `ENV G5 version=…` replaced by `0.0.0-forged-no-such-binary` | **ACCEPT** | **ACCEPT** (rc 0 pass) |
| `forge2-leg-verdict.txt` = committed receipt with ONLY `LEG G3 2 … P` flipped to `F` (contradicting `VECTOR G3=P/P/F`) | **ACCEPT** | **REFUSE** (`G3 leg-verdicts PFF != PPF` + stored-predicate), rc 1 |

forge1/forge2 each differ from the committed receipt by exactly one line (diff shown in the
command log). So the frozen clause set accepts fabricated fixtures beyond the committed one —
and on LEG detail rows strict is WEAKER than the existing default gate. C2's kill rule (a) names
only the committed fixture, so this is not a kill; it is the precise shape of the named
limitation ("a receipt that copies every value from the committed bytes still passes strict"):
any field outside s1-s6 is forgeable, and forge1 shows one field (`ENV` version strings) that
NEITHER the default gate nor strict binds.

Fields a fixture must forge, and whether s1-s6 bind them (commit `dcc39ea3` text):

| field | bound by s1-s6? | bound by default mode? |
|---|---|---|
| instrument header version | s1 ✓ | no |
| GRADER sha (+ committed grader bytes) | s2 ✓ | yes (sha+pin) |
| GRADER `pin=` token | no | yes |
| AMALG sha | s3 ✓ | yes (sha+url) |
| AMALG `url=`/`bytes=` | no | url only |
| TOOLCHAIN gcc/gcov/bwrap | s4 ✓ (cross-checked vs CC/GCOV/BWRAP lines) | presence only |
| TOOLCHAIN python | no (named limitation) | presence only |
| CC/GCOV/BWRAP lines' own bytes | only via the s4 comparison; not anchored to real tool output | no |
| RUN `rc=` and `driver=` | s5 ✓ | presence only |
| RUN `path=`/`argv_sha256=`/`masked=` | no | no |
| per-case NOBIND `delta=0` | s5 ✓ | presence only |
| battery NOBIND lines (before/after) | ambiguous — see below | presence only |
| BUILD/FILES/ENV presence | s5 ✓ | presence only |
| BUILD cmd/elapsed/members, FILES paths, ENV versions | no (forge1) | no (forge1 accepted by default) |
| VECTOR lines vs probe table | s6 ✓ | yes |
| CASE observed/expected/build/masked/gcda/gcno | no | yes (observed/expected/masked/build) |
| LEG verdict rows, FRAGMENT lines | no (forge2) | yes (rows + two frozen fragments) |
| PREDICTION line | no | no |
| stored `PREDICATE R65-C1` line | no | yes (must equal derived) |

**Ambiguity reported (not edited):** s5 says "every `NOBIND` line carries `delta=0`". The
committed receipt's battery lines `NOBIND before-battery listeners=35 probe_pid=3169329
probe_listening=0` / `NOBIND after-battery …` carry NO `delta=` field. Implemented literally over
all NOBIND lines, strict would refuse the committed receipt → kill rule (b) fires and C2 dies at
data time. The builder must scope the clause to the per-case NOBIND lines (as my re-implementation
did; the committed receipt then passes). This is a defect risk in the frozen clause text,
reported per the round contract.

Smallest safe correction: state the limitation the way C2 already does for itself — strict binds
exactly the s1-s6 fields; everything else in the table above is forgeable — and consider having
strict REQUIRE the default checker's clean pass as clause s0 (default already binds CASE/LEG/
FRAGMENT/predicate-line; forge2 would then be refused by strict too; forge1 stays admitted and
needs its own binding if wanted).

---

## A4 (calibration) — does the claims doc overclaim?

Sentence-by-sentence check of the Frontier step and the two Score paragraphs against evidence
visible to the wave (commands in the log below). Result: **no sentence asserts more than its
evidence; the calibration defect is two MISSING disclosures and one clause ambiguity, all
reported above.**

Verified true, sentence by sentence:

- F1: S238 capture sha256 `23574246…c64f` ✓ (sha256sum); byte-identical to the round-52 capture ✓
  (`cmp`, silent); `SHA256SUMS` line 169 carries the same sha ✓. S239 capture sha256
  `989bfcf0…2dcd2` ✓. S239 does state the AFAB requirement ("Run forward passes for all
  microbatches first") and the no-hook requirement ("You must not use hooks inside your
  implementation") ✓ — so "The C1 rests on S238 … and S239" is supported; A1 adds that the
  no-hook requirement is enforced only as a substring match (grader :31-41), which no sentence
  denies and no named limitation covers.
- F1 rationale line numbers ✓: exists :19, no_hooks :31, `_test_pipeline_parallel` :91,
  layer-count :144, AFAB check :152-157 (raise at :157), parametrized test :171-178 (grep -n).
- F2: `grep -c '^PROBE' corpus/evidence/round65/sqlite-gcov-probe.txt` → `0` (rc 1) ✓; the cited
  lesson exists and carries the R66-C2 section (`corpus/lessons/round-66-verifier-spotcheck.md`,
  "### R66-C2" at :50) ✓.
- F3: no `merge/` directory exists in the lane ✓; the round-54 L0 row is carried open in the
  ledger (`LOG.md` :1684-:1787 "Assimilation none (L0 `kengaku | round-54` unanswered)") ✓.
- C2 pre-freeze-read sentence ✓ on every token: receipt line 2 is
  `# instrument plans/round65_c1_sqlite_probe.py version=r65-c1/1`; probe :114 is
  `PROBE_VERSION = "r65-c1/1"`; `RUN` lines carry `driver="/usr/bin/python3 /ctl/driver.py"`;
  CC/GCOV lines carry 16.2.1 and BWRAP 0.13.1 (grep -n).
- C2 Defect sentence ✓: default `--check-receipt` on the fabricated fixture prints
  `CHECK ok cases=5` / `PREDICATE R65-C1 pass`, rc 0 (reproduced this session).
- Score (C1) "coverage held at 7 under the L0 cap … `kengaku | round-25/33/51` stays open" ✓
  consistent with the standing ledger (LOG.md :2473, :2517, :2530; SCORECARD :2893 all carry the
  open cap and coverage 7); SKILL.md:81 decision-table row for `process-environment` still reads
  `recipe-unexecuted` ✓, so "class row stays `recipe-unexecuted` until this predicate passes"
  matches the committed row.
- Score (C2) "operability held at 10 (exercised)" — the exercise evidence is this wave's own
  gates; from this seat, both strict outcomes the predicate names check out under the frozen
  clauses (fabricated REFUSE, committed ACCEPT), and the default-mode command is unchanged (rc 0
  over the committed receipt). Whether 10 holds is the judge's call; nothing in the paragraph
  contradicts observed evidence.

Findings (fixable, none a kill):

1. **Missing disclosure (C1):** `--check-receipt` accepts a self-consistent fabricated
   receipt+junit pair (A2, rc 0). C2 names its analogous limitation; C1 must too.
2. **Missing disclosure (C1):** `no_hooks` is a substring match and evadable by name-splitting
   (A1); the frozen table is not a compliance oracle beyond its six rows. Named limitation (i)
   covers only AFAB-vs-1F1B.
3. **Clause ambiguity (C2, report-only):** s5 "every NOBIND line carries delta=0" would refuse
   the committed receipt if read to include the battery NOBIND lines (which carry no delta=
   field) — kill rule (b) fires on a literal reading. Scope to per-case lines.
4. **Wording wobble (minor, C1 Target):** "the second process-environment census member … the
   first is torch-tensor-parallelism (R66-C1)" mixes list order (on :14 the list is
   install-windows-3.11, torch-pipeline-parallelism, torch-tensor-parallelism — so "second" by
   list order is correct for pipeline) with claim order ("first" worked = tensor, confirmed in
   `plans/round-66-claims.md` :37/S183). Identity is unambiguous; the ordinals are not both
   list-order.
5. The dev-build-check sentence (one q1-ref run, 13 s, scratch `dev`) is unverifiable after the
   fact; it is disclosed as not claim data, so it is not an overclaim — noted for completeness.

---

## Commands and exit codes (all runs this session)

```
# predicate of record (C1)                                  rc 0
python3 plans/round67_c1_pipeline_probe.py --check-receipt corpus/evidence/round67/pipe/receipt.txt
#   -> CHECK ok cases=6 / PREDICATE R67-C1 pass

# A1 literal self-check                                     rc 1 (0 matches = literals absent)
grep -c "register_forward_hook\|register_full_backward_hook" $S/a1/app/pipeline_parallel.py
# A1 grader run, world size 1 only, under the port lock      rc 0
flock /home/vgpnk/.local/share/kengaku-r67/port-12355.lock bwrap --die-with-parent --unshare-net \
  --unshare-pid --ro-bind /usr /usr … --ro-bind $S/a1/app /app \
  --ro-bind corpus/evidence/round52/graders/torch-pipeline-parallelism/tests/test_outputs.py /tests/test_outputs.py \
  $V/bin/python -m pytest /tests/test_outputs.py -p no:cacheprovider -q -k "not 2" --junitxml=/ctl/junit.xml
#   -> 3 passed, 1 deselected in 3.97s  (exists P, no_hooks P, ws1 P; ws2 deselected)

# A2 fabricated receipt (two intermediate refusals first)    rc 1, rc 1, then:
python3 plans/round67_c1_pipeline_probe.py --check-receipt $S/a2-fab/receipt.txt
#   -> CHECK ok cases=6 / PREDICATE R67-C1 pass              rc 0   (no grader run anywhere)

# A3 strict re-implementation over four fixtures             batch rc 1 (expected refusal inside)
python3 $S/a3/strict_reimpl.py $S/a3/committed-r65-receipt.txt $S/a3/fabricated-r65.txt \
        $S/a3/forge1-env-version.txt $S/a3/forge2-leg-verdict.txt
#   -> committed ACCEPT; fabricated REFUSE (24 defects); forge1 ACCEPT; forge2 ACCEPT
# A3 default mode, committed checker (unmodified)
python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt   # rc 0 pass
python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round66/red/fabricated-r65.txt  # rc 0 pass (M-1)
python3 plans/round65_c1_sqlite_probe.py --check-receipt $S/a3/forge1-env-version.txt                    # rc 0 pass
python3 plans/round65_c1_sqlite_probe.py --check-receipt $S/a3/forge2-leg-verdict.txt                    # rc 1 fail

# A4 evidence
sha256sum corpus/evidence/round67/sources/* plans/round67_c1_pipeline_probe.py \
          corpus/evidence/round52/graders/torch-pipeline-parallelism/tests/test_outputs.py \
          corpus/evidence/round52/graders/sqlite-with-gcov/tests/test_outputs.py
cmp corpus/evidence/round67/sources/torch-pipeline-parallelism-test_outputs.py \
    corpus/evidence/round52/graders/torch-pipeline-parallelism/tests/test_outputs.py        # identical
sed -n '169p' corpus/evidence/round52/graders/SHA256SUMS                                     # 2357…c64f
grep -c '^PROBE' corpus/evidence/round65/sqlite-gcov-probe.txt                               # 0 (rc 1)
grep -n "…:19|:31|:91|:144|:157|:171…" sources/torch-pipeline-parallelism-test_outputs.py    # all match
sed -n '14p' corpus/evidence/round62/class-survey.txt; sed -n '81p' SKILL.md                 # member + recipe-unexecuted
diff $S/a3/committed-r65-receipt.txt $S/a3/forge1-env-version.txt                            # 1 line (ENV G5)
diff $S/a3/committed-r65-receipt.txt $S/a3/forge2-leg-verdict.txt                            # 1 line (LEG G3 2)
```

No installs were made (tooling-only rule: nothing named an install for this seat). No network was
used. No git/jj mutation. Port lock taken for the one grader run; no listener of mine persists.
Scratch `/fast/scratch/hyaku/kengaku-r67/ClaimFalsifier` removed after copying cited artifacts.
