# R4ClaimsSizing — adversarial sizing audit of plans/round-55-claims.md (frozen 80afa613)

Scope: the three frozen claims, audited against committed bytes at the freeze tip `80afa61314fa1b…`
(clean `--shared` clone under my scratch) plus the committed base `798f5e9e…`. Every dynamic attack was
run in scratch; the lane tree was never written. Where I exercised the in-flight (uncommitted)
`plans/round55_c2_entryargv.py` / `plans/round55_c3_chess_probe.py` from the wave working tree, results
are labelled IN-FLIGHT and are early signal, not landing-revision verdicts.

Severity scale: HIGH = claim as frozen is mis-sized / predicate unreachable or bypassable as stated;
MEDIUM = clause undecidable or unimplementable as written, workaround exists; LOW = residual risk /
fidelity nit that does not change the claim's outcome but should be on record.

---

## R55-C1 (operability 8→9, registry closure)

**Predicate one-command re-derivable: YES (verified).** Ran
`python3 plans/round52_c2_registry.py --lane <clone>` at the freeze tip:
`ADVERTISED total=79 REGISTERED total=77 MISSING 2 (round54_c1_anchor.py, round54_c2_entrytruth.py) …
PREDICATE R52-C2 fail, exit 1` (evidence/c1-counter-at-freeze.txt). Before-receipt matches
(`.ufo/waves/round-55/claims/c1-before.txt`).

**Universal clauses over enumerated sets: YES.** The advertised universe is closed: regex `CMD` over
`SCORECARD.md, SKILL.md, LOG.md, corpus/README.md` **plus all `corpus/knowledge/*.md`**
(`self_assessment_files`, plans/round52_c2_registry.py:34-41), filtered to paths that exist in the tree.
The claim's "LOG/SCORECARD/SKILL/README/knowledge text" enumeration is accurate — knowledge text IS
scanned (I initially suspected README.md/knowledge overreach; code reading refuted it).

**Do-nothing control: FAILS AS STATED — erasure bypass (HIGH, finding C1-F1).**
The claim asserts "a round that adds no registry rows cannot pass". Cheapest skip-work control I could
construct: erase the two scripts' *advertisements* from the self-assessment files (they live only in
`SCORECARD.md` — 4 substitutions), adding zero registry rows. Ran it on a scratch copy of the freeze
clone: counter prints `ADVERTISED total=77 … MISSING 0 … PREDICATE R52-C2 pass, exit 0`
(evidence/c1-erasure-attack.txt). Deleting the script *files* does not help (`collect` filters the
advertised set by textual mention, not file existence — I checked the code), so mention-erasure is the
cheapest route and it works. The frozen control only covers the *additive* do-nothing; nothing in the
frozen text binds the advertised set at the landing revision to the base receipt (c1-before.txt records
`total=79` and the two MISSING names, not the full set). Detection today rests on integration diff
review, not on any committed gate. The claim's mechanism sentence is therefore over-strong; the round
can still be landed honestly, but an erasure attempt would pass the counter and must be caught by the
L1's diff against the base clone.

**Kill rules decidable: YES, and load-bearing (verified by attack).** Added all five round-55 rows to a
scratch copy, one carrying a *demonstrably false* verdict-map cell (`round55-c2-controls` cell claims
`` `1` ok · `0` bad `` while `python3 plans/round55_c2_controls.py --selftest` truly exits 0). Counter:
`MISSING 0 … PREDICATE R52-C2 pass, exit 0` — the counter has no verdict-map-truth leg
(evidence/c1-false-cell-attack.txt). The frozen leg-2 truth spot-leg is the guard: one self-test run per
round-55 row, exit code vs cell — decidable and enumerable. Also verified the SELFTEST-UNBACKED leg
catches fabricated self-test flags (my `--bogusflag` row and a wrong `--selftest` cell on the anchor,
whose real spelling is the `selftest` subcommand, both fired). Kill rule is fair: a seat that lands
truthful cells survives it; a seat landing false cells is caught by one command per row.

**First-answer baseline would meet target: NO.** Empty cells → INCOMPLETE; fabricated cells → pass the
counter but die at leg 2; wrong flags → SELFTEST-UNBACKED.

C1 verdict: predicate sound and re-derivable; do-nothing control wording overclaims (HIGH finding);
kill rule decidable and necessary.

---

## R55-C2 (calibration 9→10, entry-argv structural binding)

**Predicate one-command re-derivable: YES in shape** — the frozen command is explicit; the in-flight
counter (IN-FLIGHT, uncommitted) prints exactly the frozen line family
(`ROWS … argv_defect=0 wrapper_defect=0 abbrev_defect=0 … RUN executed=… TIPSTATE … PREDICATE R55-C2
pass/fail`). Its `--selftest` passes 4/4 (truthful-fixture, argv-tamper, uv-wrapper, abbrev-flag).

**Universal clauses over enumerated sets: YES** (ledger json rows × registry table rows, both closed).

**Do-nothing control: HOLDS.** At base the instrument does not exist; the committed before-receipts show
the unchanged r54 counter passing both laundering fixtures (`PREDICATE R54-C2 pass`, exit 0, true entry
exit 1). A stub `evaluate` printing the required lines would fail the frozen fixture-kills requirement
(both fixtures must produce attributed kill lines; verified live against the in-flight counter — both
kills demonstrated, `ROUTE kill demonstrated`, case exit 0; evidence/c2-fixture-kills-inflight.txt).
Residual: a *generic* stub that special-cases nothing and is never attacked would pass the letter of
the after-predicate; only the kill rule defends. LOW residual, by design.

**Kill rules decidable: YES, with one boundary (LOW, finding C2-F4).** "Truly exits otherwise" is only
well-defined modulo the counter's hermetic env (r54 model: env scrub + git reset, host execution, no
sandbox). Demonstrated: an env-dependent gate (`exit 0 iff GIT_CONFIG_GLOBAL is set`) passes the
in-flight counter green while the same argv exits 1 in a plain shell
(evidence/c2-env-gate-attack.txt). That is a calibration boundary, not an argv-binding soundness break —
the binding legs hold (argv is exactly the declared entry) — but an attack seat could wave it; the L1
should read "truly" as "under the counter's own L4 execution model", which the frozen leg 4 defines.

**Frozen predicate unreachable over committed bytes as worded (HIGH, finding C2-F1).** The after-predicate
requires `argv_defect=0 wrapper_defect=0` over the full ledger+registry at the landing revision, but:
1. A natural L1 implementation (token-equal against the registry cell's first `python3` backtick span,
   shlex-split) flags **17 of 78 committed rows** as ARGV-DEFECT — every one a truthful row whose cell
   carries placeholder prose (`<expect.json>`, `[--revision REV]`, `PATH...`, `--round N`) where the
   ledger declares the concrete invocation (e.g. `adoption-check` declared red with the real
   `--expect .ufo/waves/round-33/claims/adoption-expect.json`; `round53-c2` red exit 2). IN-FLIGHT
   measured: `argv_defect=17 wrapper_defect=1` at the freeze clone
   (evidence/c2-inflight-dry-at-freeze.txt).
2. `wrapper_defect=0` is unreachable without touching committed data: the committed row
   `tb2-grader-probe` declares a `uv run --no-project --with biopython==1.85 python3 …` entry (registry
   cell AND ledger argv, declared green) — the frozen L2 makes `uv` as argv[0] a WRAPPER-DEFECT by name.
   The frozen corrections clause covers only round35-c1-coverage's evidence fragment and the five new
   rows; it is silent on these 18 legacy rows.
   Resolution requires one of: a dated amendment row; a mass ledger redeclaration beyond the frozen
   clause; a registry-cell edit (a documentation attack per the kill-rule parenthetical); or a lenient
   counter-side tokenization (placeholder slots / bracket stripping) that the frozen wording "must
   token-equal" does not describe. None is authorized by the frozen text. The claim's zero-counts do not
   fit its own committed data.

**L3 "checked without executing" literally unimplementable (LOW, finding C2-F2).** For arbitrary
scripts, the accepted-flag set is not statically decidable (dynamic argparse construction); the in-flight
counter uses a body-scan heuristic, which can miss real abbreviations (e.g. `add_argument("--self" +
"test")`) and can false-positive on non-argparse flag strings. Impact bounded: L1 is load-bearing (any
abbreviated argv mismatches the cell first) and L3 is defense-in-depth — and the frozen fixture kills
require ABBREV-DEFECT attribution, which the in-flight counter prints alongside ARGV-DEFECT.

**First-answer baseline would meet target: NO** for an honest first implementation (the in-flight one
fails its own frozen zero-counts at the freeze tree — see C2-F1), and a dishonest stub is covered above.

Correction leg (a) verified necessary and decidable: the committed fragment
`V4 DEFECT knowledge files=57 index rows=57 (want 42/42)` is stale — the entry's true output at the
freeze tip is `…files=58 index rows=58…` (evidence/c2-round35-true-output.txt). Note the correction must
be re-derived at the landing revision, after all knowledge/index lands settle, or it drifts again —
sequencing only, not a defect.

C2 verdict: intent sound; fixture kills and selftest demonstrably implementable; but the frozen
zero-count predicate does not fit the committed registry/ledger without an amendment or lenient
tokenization (HIGH); env-truth boundary and L3 wording on record (LOW).

---

## R55-C3 (coverage attempt, 13th TB2 grader)

**Predicate one-command re-derivable: YES (verified live).** Ran the committed-by-freeze… — correction:
the probe script itself is NOT in the freeze commit (untracked in the wave tree; the freeze commit
carries only the claims doc, the controls builder and the before receipts). I ran the wave-tree copy
read-only against my freeze clone: `cases=12 observed_pass=5 observed_fail=7 mismatches=0`,
`PREDICATE R55-C3 pass`, exit 0 (evidence/c3-probe-and-identity.txt). Receipt is deterministic: my
fresh run is byte-identical to the wave working-tree receipt (diff clean).

**Universal clauses over enumerated sets: YES** — 12 frozen cases, predictions in the script.

**Do-nothing control: HOLDS.** At base `798f5e9e`: receipt absent (`git cat-file` confirmed), zero
`chess-best-move` mentions in corpus/README.md/SOURCES.md, zero `thirteenth` in PROVINCE.md — matching
the committed before-receipt.

**Kill rules decidable: YES, all three probed.**
(a) Mismatch counting is direct per-case `observed != predicted` (read the code); no route to a miscount
found; all 12 observed verdicts matched predictions in my run.
(b) Oracle provenance: I independently re-derived all 12 predictions from the captured grader's own
assertion `sorted(move) == sorted(["g2g4","e2e4"])` — 12/12 agree with the frozen table.
(c) Upstream identity: fetched
`raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88…/chess-best-move/tests/test_outputs.py`
(HTTP 200; note the task tree is at repo root — a `tasks/` prefix 404s, my first fetch failed that way):
sha256 `a540714e…` — **byte-identical** to the capture. Amendment A1 also verified live: upstream
`chess-best-move/tests/test.sh` sha256 `4770437e…716e6c334`, identical to both in-repo regex-log runner
captures — dropping the third SOURCES row is justified.

**First-answer baseline would meet target: NO** — predictions are frozen pre-run in the script; there is
nothing to first-answer. A hand-fabricated receipt would satisfy the letter ("receipt commits with
mismatches=0") but determinism exposes any non-run bytes on re-run; tip-receipts enumerates the receipt
(basename contains `probe`) yet currently *skips* it — stem `chess-best-move-probe` folds to
`chessbestmoveprobe`, not `round55c3chessprobe` — unless the RECEIPTS table in plans/tip_receipts.py
gains a row (LOW residual, finding C3-F2; advisory: land the table row).

**Anchor fidelity nit (LOW, finding C3-F1).** The claims doc has PROVINCE.md "narrowing '12 of 89 read'
→ '13 of 89'", but no committed PROVINCE.md text says "12 of 89" — PROVINCE's own frontier line reads
"8 of 89 read" (last touched by the round-42 paragraph); "12 of 89" lives in corpus/README.md §Frontier
(round-46 bullet) and LOG.md. The in-flight landed paragraph resolves this sensibly ("This narrows …: 13
of 89 read. The earlier paragraphs stay as written."). Recommend a dated amendment noting the anchor
file. Also on record: the probe script and the C2 counter are not in the freeze commit — fine (the
freeze binds rules, not bytes), but "instrument (new, frozen)" wording slightly overstates what 80afa613
contains.

C3 verdict: well-sized; all three kill legs probed and passing; predicate re-runs green; two LOW
residuals on record.

---

## Findings summary (severity order)

| # | Claim | Severity | Finding |
|---|---|---|---|
| C2-F1 | R55-C2 | HIGH | Frozen zero-count predicate (`argv_defect=0 wrapper_defect=0`) unreachable over committed registry/ledger: 17 truthful rows fail literal L1 token-equality; committed `tb2-grader-probe` row is a uv wrapper (frozen L2 defect). Needs amendment, mass redeclaration, or lenient tokenization — none authorized by the frozen text. Measured on the in-flight counter at the freeze clone. |
| C1-F1 | R55-C1 | HIGH | Do-nothing control overclaims: mention-erasure in SCORECARD.md alone (4 lines, zero registry rows) makes the counter print `MISSING 0 / pass / exit 0`. Control covers only additive no-ops; no committed gate binds the landing advertised set to the base receipt. |
| C2-F2 | R55-C2 | LOW | L3 "checked without executing" literally unimplementable for arbitrary scripts; in-flight body-scan heuristic can miss constructed-flag abbreviations / false-positive on prose. Bounded: L1 load-bearing. |
| C2-F3 | R55-C2 | LOW | Fixture-kill attribution rides on ARGV-DEFECT presence (L1) — frozen ABBREV/WRAPPER kill lines are present in-flight but the binding is L1; kill-rule wording "attributed kill line" is met by any of the three tags. Fine, noted. |
| C2-F4 | R55-C2 | LOW | "Truly exits otherwise" decidable only modulo the counter's hermetic env; env-dependent gate passes the counter, exits 1 in a plain shell (demonstrated). Boundary of the claim's surface, not a soundness break. |
| C3-F1 | R55-C3 | LOW | Frozen PROVINCE anchor string "12 of 89 read" absent from committed PROVINCE.md (it says "8 of 89"); anchor lives in corpus/README §Frontier. In-flight paragraph resolves it; amendment row recommended. |
| C3-F2 | R55-C3 | LOW | Receipt fabrication not machine-bound: predicate is "receipt commits with mismatches=0"; tip-receipts will skip this receipt (stem mismatch) unless the RECEIPTS table gains a row. Determinism + witness run are the practical guards. |
| C1-F2 | R55-C1 | INFO | Verdict-map truth is not counter-checked (false cells pass); frozen leg-2 spot-leg is the guard — verified necessary and decidable. |
