# Round 46 — frozen claims (kengaku, hyaku run 9, 2026-10-27)

Baseline lane tip `64ba8385ea10af1b78d367dcb242b92d97062af7` (the round-45 non-author spot-check tip). L1 `KengakuR46`
holds the canonical planner seat. Starting point: SCORECARD `### Planned (round 46)`, the round-45 closure
`corpus/lessons/round-45-verifier-spotcheck.md` (status ok, admitted false, `rejected-harmed`; §5 routed defects) and
the orchestrator's routing note (supersede S152–S154 + anchor-line gate check; mark the predictor's lone-CR gap and put
those states in a held-out set; LOG.md correction entry for D1; re-freeze C1 with a path-hidden control; carry the
open wave findings). `.ufo/watchdog.log:1654` launches attempt 1; no earlier attempt of round 46 exists.

Axis state carried (SCORECARD round 45): calibration 8, coverage 7 (capped by L0 `kengaku | round-33`), novelty 7,
depth 9 (harmed by round 45, closure §2), operability 8, freshness 8, adjacency 8. Lowest non-retired: coverage 7 tied
with novelty 7; **coverage** is worked (C3, frozen tie-break as in rounds 44–45). No stagnation waiver. Three claims on
three axes; causally separable (below).

**Freeze shape (declared now, before any data).** C2 is frozen whole at this commit: counter, gate tool, controls and
receipts exist and were run on the base before this file was committed. C1 and C3 are frozen in two stages. Stage 1
(this commit): the predicate sentence, the counter contract, the controls that must fail, and the kill rule. Stage 2
(one amendment commit, after wave 1 returns and BEFORE the work is scored): the counter file, its input pins, the
literals `<P>`, `<R>`, `<S>` (C1) and `<V>` (C3), and the before-control receipts, each run on the base or a control —
never on the claimed work. Stage 2 may fill literals and pins; it may not change a predicate line, a control, or a kill
rule written here. Any other edit of this file after this commit is named, with its commit, in a `Freeze amendments`
paragraph appended below (round-45 closure D4).

## C1 — calibration: the fixture fence's advertisement vs its observed behaviour, under a counter that hides its names

- **Self-assessment under test.** SCORECARD capability `fenced-fixture-discovery` (round 44) and the
  `plans/fixture_fence.py` docstring: "admit only a fixture whose git store, discovered repos and argv stay inside `d`",
  deciding without reading outside `d`. Observed at base: the round-45 counter is passed by a fence that keys on the
  counter's own fixture names (`.ufo/waves/round-45/claims/control-c1-fence-keyed_name.txt`, QUALITY Q39), and 9 of 14
  held-out hostile modules written against the landed fence are admitted (`a3w1/R45HoIncludeIf.md` 3,
  `R45HoSymlinks.md` 2, `R45HoArgvEnv.md` 1, `R45HoCommondir2.md` 2, `R45HoConfigKeys.md` 1 — VERDICT lines).
- **Counter** `python3 plans/round46_c1_verify.py --lane .` (written in wave 1, pinned at stage 2). Contract:
  (a) the round-45 counter's legs and builder (`plans/round44_c1_verify.py` imported, digest-pinned), the HONEST leg
  unchanged (104 fixtures of `plans/battery42|43|44`); (b) **Q39 name hiding** — fixture dirs, build dirs and module
  copies are named by a per-run random token (`secrets`), never derived from a module or group name, and fence jobs
  run in shuffled order; (c) REFUSALS = `plans/refusals46/`: f1–f10 byte-copied from `plans/refusals45/` plus every
  round-45 held-out module (a3w1 `R45Ho*`) that the round-45 landed fence admits or reads, converted to the module
  contract, each shown LEAKED or READ under the round-45 counter with the base fence; (d) SEALED = `plans/sealed46/`:
  hostile modules authored in wave 1 by critic seats that no fence-writing seat reads, kept only if LEAKED or READ
  under the base fence; (e) the strace log is not writable from the fence's namespace, and a missing, empty, NUL-holed
  or execve-less log counts as READ (round-45 B1); (f) any open outside `d` under the whole scratch root counts, except
  the harness and the fence copy (B3); (g) stat-family, readlink and access calls on such paths count like opens (B5);
  (h) blocked or never-returned opens are counted from their pending text, dirfd-relative paths resolved (B6); (i) the
  verdict travels as the harness's exit status, never parsed from stdout (B4). io_uring (B7) is a named limit unless
  blocked cheaply.
- **Frozen predicate.** C1 passes iff the counter prints `PINS total=<P> mismatched=0`, then
  `REFUSALS total=<R> clean=<R> leaked=0 read=0 hung=0 build_errors=0`, then
  `SEALED total=<S> clean=<S> leaked=0 read=0 hung=0 build_errors=0`, then
  `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`, then
  `CALIBRATION advertised=<R+S> contradicted=0`, then `PREDICATE C1 pass`, exit 0, on a clean clone of the landing tip.
- **Controls that must print `PREDICATE C1 fail` at stage 2** (receipts under `.ufo/waves/round-46/claims/`): no fence;
  the base fence (`plans/fixture_fence.py` @ `64ba8385`, the before value: contradicted = the converted + sealed modules
  it admits or reads); the round-45 keyed fence `keyed_name.py`; a new keyed fence that keys on any name or structure
  the counter still exposes (sibling count, argv path, build order); the round-45 forged fences from
  `w1/R45CriticPredicate.md` (log erasure, stdout spoof, host read, module-source read, stat channel); admit-all;
  refuse-all. A control that passes refuses the counter: the claim stops honestly, it is never re-frozen after scoring.
- **Work.** `plans/fixture_fence.py` repaired (wave-1 executor variants; the L1 lands one).
- **Kill rule.** Any predicate line off at the landing tip → C1 not admitted. Wave-2 held-out modules (authored against
  the landed fence) are reported per module; two or more admitted or read → C1 not admitted even if the predicate
  passes (the closure's round-45 reading, adopted in advance).

## C2 — depth: round 45's false line-level detail superseded and marked (frozen whole at this commit)

- **Surface.** `corpus/SOURCES.md` anchor cells that cite `:N "quote"`, a `<file>:<a>-<b>` range and `(K words)`;
  the `password-recovery` entry's `## Predictor`, `source:` ranges and errata. New gate tool `plans/anchor_line_check.py`
  (sha256 `35d02dc5…`, red fixture in `--selftest`). `plans/pkg_gate.py` (pinned by `plans/round45_c2_verify.py`) and
  `plans/anchor_digest_check.py` (pinned by `plans/round44_c1_verify.py`) are not edited: editing either would turn a
  standing counter red.
- **Counter** `python3 plans/round46_c2_verify.py --lane .` (docstring = the full rule; sha256 recorded in
  `.ufo/waves/round-46/claims/frozen-digests.txt`). Legs: A anchor lines over the registry (live defective rows; base
  rows unchanged except mutable cells), B the entry's predictor vs the CAPTURED grader on 16 frozen newline states
  (lone CR, LF-CR, CR-CR-LF, VT/FF/NEL/LS non-newlines, CRLF controls), C entry `source:` ranges within capture length
  plus a `## Errata (round 46)` section naming `lone-CR`, `S152`, `S153`, `S154`, `empty-file`, D the gate's selftest.
- **Frozen predicate.** C2 passes iff it prints `PINS total=3 mismatched=0`, then `A anchorline live=0` with
  `base_missing=0 base_changed=0`, `B predictor` with `disagree=0`, grader_pass>=4 and grader_fail>=4, `C entry` with
  `source_ranges_bad=0 errata_marks=5/5`, `D selftest exit=0`, then `checks=4 defects=0` and `PREDICATE C2 pass`, exit 0,
  on a clean clone of the landing tip.
- **Before (controls, run on `--shared` clones of `64ba8385` + the two new tools):** `control-c2-nothing.txt` —
  `A live=8` (S108 words; S149 range; S150 words; S151 range+words; S152 line+words; S153 line+range+words; S154
  line+range; S155 range+words), `B disagree=6`, `C source_ranges_bad=4 errata_marks=0/5`, fail, exit 1.
  `control-c2-inplace.txt` (S152–S154 anchors fixed in place) → `base_changed=3`, fail. `control-c2-junk-supersede.txt`
  (superseding rows copying the wrong anchors) → `live=11`, fail. `control-c2-splitlines.txt` (predictor
  `text.strip().splitlines()`) → `disagree=4`, fail. `control-c2-errata-only.txt` → A/B/C ranges fail. The do-nothing
  control cannot reach the target.
- **Work.** Superseding rows S157–S165 (Q34) for S108, S149, S150, S151, S152, S153, S154, S155 and S156 (S156: kind
  `code`→`docs`, `R45RevRowCells` defect 12; S150/S154 kind fixed in their rows; S154 `teaches` verbatim, closure D6);
  the entry's predictor reads universal newlines, `source:` ranges corrected, `## Errata (round 46)` names every
  corrected statement; the round-45 counter must still pass at the tip (no-harm).
- **Kill rule.** Any leg defect → C2 not admitted. Limit named now: leg A checks line-cited quotes only (4 rows cite
  no retained capture: S093, S103, S104, S110 — reported `UNCAPTURED`, not certified).

## C3 — coverage: the pinned TB2 `polyglot-c-py` grader, a twelfth grader-class exemplar (dual-runtime execution)

- **Surface.** `corpus/knowledge/tb2-polyglot-c-py-grader.md` (new), SOURCES rows from S166 (tier A, opened this
  round), README index row + coverage bullet + §Frontier narrowing (11 → 12 of 89), PROVINCE paragraph,
  `corpus/evidence/round46/tb2-polyglot-c-py/` captures + SHA256SUMS at terminal-bench-2 `2fd12b88aafdd04a52c298e3940bcb189f9766d6`,
  `plans/polyglot_c_py_probe.py` (executed probe), `plans/pkg-spec-r46.json`.
- **Class (worded before data, from reading `tests/test_outputs.py` at the pin).** One file `/app/polyglot/main.py.c`
  is executed by two toolchains — `python3 main.py.c N` and `gcc main.py.c -o cmain && ./cmain N` — and both stdouts,
  `.strip()`ped, must equal the expected Fibonacci value for N in {42, 10, 0}; first, `os.listdir("/app/polyglot")`
  must equal `["main.py.c"]` exactly (the grader's own `gcc -o /app/polyglot/cmain` then writes a second file there).
  Three fixed points, no other N, no timing, no source inspection.
- **Disclosed prior grading.** Round 45 seat `w1/R45PlanNext.md` §2 ran this grader once on the host (oracle +
  extra-file re-grade, two cases, not a case table). No case of this round's probe has run.
- **Counter** `python3 plans/round46_c3_verify.py --lane .` (written in wave 1, pinned at stage 2), the round-45 C2
  counter's V1–V11 re-pointed at this package (captures, gate run from `plans/pkg_gate.py` at its round-45 digest,
  anchor digests, receipt, frozen probe + dry table, census, requirement map, order check against this file, content
  consistency, mechanism, held-out predictor with lone-CR and non-newline kinds and the `R45CritV11Bypass` lookup
  shapes refused) plus V12 (its own anchor-line rule for the new rows: line, range, words) and V13 (a committed filler
  package — a do-nothing entry and rows of the right shape — must make V1–V12 print at least one DEFECT;
  considerthese `2026-10-26.md` proposal 2).
- **Frozen predicate.** C3 passes iff it prints `checks=<V> defects=0`, then `PREDICATE C3 pass`, exit 0, on a clean
  clone of the landing tip; `<V>` fixed at stage 2.
- **Controls that must print `PREDICATE C3 fail` at stage 2:** the base tree (no package); the filler package; an echo
  receipt (the dry table copied as the receipt).
- **Order (Q30).** Before stage 2 the probe runs only `--dry`/stage-check; its first recorded run follows the stage-2
  commit; the receipt path is `corpus/evidence/round46/polyglot-c-py-probe.txt`.
- **Kill rule.** Any V defect → C3 not admitted. Limits named now: host gcc and python3 stand in for the image's
  gcc 13.2.0 / python 3.12.3; pytest is not run (the harness reproduces the one test function's verdict).

## Separability

C1 touches `plans/fixture_fence.py`, `plans/refusals46/`, `plans/sealed46/`, `plans/round46_c1_verify.py` only. C2
touches `corpus/SOURCES.md` rows S157–S165, the `password-recovery` entry and the two C2 tools. C3 touches its own
entry, rows from S166, captures, probe, spec, counter, README/PROVINCE lines. C3's counter runs the gate at its
round-45 digest and carries its own anchor-line rule, so it verifies without C2; C2's leg A counts every captured row,
so C3's new rows must also be line-correct — a C3 row defect shows in C2's leg A and is attributed to C3 by row id.
