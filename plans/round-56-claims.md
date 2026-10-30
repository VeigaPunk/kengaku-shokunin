# Round 56 claims — frozen before data (2026-10-30, L1 KengakuR56)

Base tip `1355e84cce57f15bd0b1bc118d4bc32fdbf476ea` (lane `master`, local==remote, tree clean).
Axis state carried from round 55 (spotcheck): calibration 9, coverage 7 (L0-capped), novelty 8,
depth 9, operability 8 (harmed 9→8 in r54), freshness 9, adjacency 9. Lowest non-retired axis:
**coverage 7**. The stagnation nudge is not invoked. A coverage claim is declared (R56-C3); its
score stays capped by the unanswered L0 questions `kengaku | round-25`, `round-33`, `round-51`,
so the claim's predicate is its counter, never the score number.

Carried duty (r55 verifier spotcheck, routed defects 1–3): re-verify the run-12 wrap-up's landed
unverified seat content with committed receipts before any SCORECARD move rides it; file the
report erratum for "SKILL.md not modified" vs wrap-up `ebb233bc`; land R55-C3's citation chain
after that verification. R56-C1 and R56-C2 are those verifications, frozen as claims; R56-C3
completes the citation chain and adds the maintainer oracle.

Rules: no predicate, counter, kill rule or target below changes after any seat has scored.
Corrections land as data (ledger declarations, registry-cell argv, receipt bytes) or as dated
amendment rows here, never as in-place rule edits. Every after-run is taken on a clean shared
clone at the recorded measured-after revision. Scratch lives under
`/fast/scratch/hyaku/kengaku-r56/` only. The frozen instruments are
`plans/round56_landcheck.py` (new, this freeze) and the already-landed
`plans/round52_c2_registry.py`, `plans/round55_c2_entryargv.py`, `plans/round55_c2_controls.py`,
`plans/round55_c3_chess_probe.py`, `grader.py` — none modified after this freeze.

## R56-C1 — operability 8→9 — landed-evidence verification gate (defect-1 verification)

- **Surface:** the run-12 wrap-up landed r55 seat content (`178385f9` SOURCES S201/S202,
  `a8ca7945` knowledge entry, `7fc12418` entryargv counter, `2eba863e` chess probe,
  `ad4e3af4` wave dir) that no round ever verified; the r55 spotcheck routed defect 1 and the
  r54 close left the prerequisite "restore registry closure and remeasure, before new scope".
  No single in-repo command re-verifies the landed evidence set today.
- **Instrument (frozen):** `plans/round56_landcheck.py --lane <clone> --work <scratch>
  [--receipt PATH]` — four legs, each a subprocess run against the clone:
  L-reg `python3 plans/round52_c2_registry.py --lane <clone>` → exit 0, `MISSING 0`,
  `PREDICATE R52-C2 pass`; L-chess `python3 plans/round55_c3_chess_probe.py --lane <clone>
  --work <work>/c3 --receipt <work>/c3.txt` → exit 0, summary line `cases=12 observed_pass=5
  observed_fail=7 mismatches=0` byte-equal to the committed receipt
  `corpus/evidence/round55/chess-best-move-probe.txt`; L-selftest
  `python3 plans/round55_c2_entryargv.py --selftest` → exit 0, `4/4 PASS`; L-grader
  `python3 grader.py` (cwd clone) → exit 0, `CHECKS n=733 mismatches=0` and
  `python3 grader.py --selftest` → exit 0, `[selftest] ALL PASS`. Prints `LANDCHECK PASS n=4`
  and exits 0 only when every leg passes; any failing leg is named and exit 1. `--selftest`
  proves the checker fails on tampered leg outputs (canned green + 3 tampered cases).
- **Before (frozen command, base `1355e84c`, clean shared clone):**
  `python3 plans/round56_landcheck.py --lane <clone>` → the instrument does not exist at the
  base tip; the interpreter cannot open the file (exit 2, `can't open file`). Receipt
  `.ufo/waves/round-56/claims/c1-before.txt`.
- **After predicate (frozen):** the same command at the measured-after revision from a clean
  clone prints four `PASS` leg lines and `LANDCHECK PASS n=4`, exit 0, with the receipt file
  written under `.ufo/waves/round-56/integrate/`.
- **Do-nothing control:** at base the instrument is absent — a round that writes no gate cannot
  pass; receipt committed at freeze.
- **Kill rule:** if any leg's observed output at the measured-after revision contradicts the
  committed bytes it is checked against (registry MISSING>0, probe summary drift, selftest
  <4/4, grader mismatches>0 or selftest FAIL), operability holds at 8 and the claim is not
  admitted. A mutation seat must additionally kill each leg (tampered leg output → landcheck
  exit 1 naming the leg); any leg a mutant cannot kill is a not-admitted defect.
- **Score note:** operability 8→9 requires the frozen predicate pass and no kill fire; the
  restored registry closure (leg L-reg) is the r54 prerequisite demonstrated, not assumed.

## R56-C2 — calibration 9→10 — entry-ledger truth under argv binding (defect-1 ledger remeasure)

- **Surface:** the r54 entry-truth ledger (`plans/round54-entrytruth.json`, 83 rows) declares
  each instrument's entry argv and true state; the r55 binding counter
  (`plans/round55_c2_entryargv.py`) binds ledger↔registry argv. At base tip the static legs are
  RED: `BINDING l1=17 l2=1 l3=0` — 17 registry cells carry doc-notation argv (`[--work DIR]`,
  `<placeholder>` spans, or a `uv`-wrapped span) that cannot token-equal the ledger's literal
  argv, and `tb2-grader-probe` declares a `uv run …` entry (L2 wrapper defect). The two r55
  laundering fixtures pass the r54 counter by construction (committed before-receipts) and must
  be killed by the r55 counter with attributed kills — never yet run (`c2-fixture-kills.txt`
  absent), and the full after-predicate run of the r55 counter has never been taken.
- **Corrections (data, before the after-run, each listed with evidence in the round lesson):**
  (a) the 17 mismatched registry cells are corrected so the FIRST backticked span of the entry
  cell is the literal executable argv token-equal to the ledger row's `entry_argv`; optional
  arguments and parameter placeholders move to the cell's prose, never inside the backtick span;
  (b) where the seat-measured minimal invocation proves the LEDGER argv wrong (not truly
  executable), the ledger row's `entry_argv` is corrected to the measured minimal argv with the
  observed exit and evidence fragment; (c) `tb2-grader-probe`: first attempt makes the bare
  interpreter true by installing the upstream-pinned dependency (Biopython 1.85) into the user
  site and re-declaring cell+ledger to `python3 plans/tb2_grader_probe.py --lane .` (dependency
  documented in cell prose); only if the pinned dependency cannot build on the host interpreter
  is the row re-declared red at the bare argv with the uv-measured-green history kept in prose
  with its receipt — never by hiding the wrapper. No counter, schema, predicate or kill rule
  changes as part of any correction.
- **Before (frozen commands, base `1355e84c`):** `python3 plans/round55_c2_entryargv.py --lane
  <clone> --dry` → `BINDING l1=17 l2=1 l3=0`, `argv_defect=17 wrapper_defect=1`; full run
  `--lane <clone> --source <clone> --work <scratch>` → static-leg failure, exit 1. Receipt
  `.ufo/waves/round-56/claims/c2-before.txt`.
- **Fixture kills (frozen):** `python3 plans/round55_c2_controls.py --case abbreviated-selftest
  --against r55` and `--case uv-decoy-script --against r55` each print their attributed kill
  (`ARGV-DEFECT` / `WRAPPER-DEFECT` naming the case), `PREDICATE R55-C2 fail`, exit 1. Receipt
  `.ufo/waves/round-56/integrate/c2-fixture-kills.txt`.
- **After predicate (frozen):** `python3 plans/round55_c2_entryargv.py --lane <clone>
  --source <clone> --work <scratch> --jobs 4 --timeout 900` at the measured-after revision
  prints `missing=0 extra=0 argv_defect=0 wrapper_defect=0 abbrev_defect=0 bad_decl=0
  duplicate_names=0 headings=1`, `BINDING l1=0 l2=0 l3=0`, `RUN executed=83 timeout=0
  mismatched=0 evidence_missing=0 laundered=0`, `TIPSTATE` declared green/red equal to observed
  green/red, `PREDICATE R55-C2 pass`, exit 0. (If the counter's summary field names differ in
  the landed instrument's actual output, the landed output is the truth and the predicate is
  its `PREDICATE R55-C2 pass` line plus zero defect counts — same sentence, the counter's own
  words.)
- **Do-nothing control:** at base the full run fails at the static legs (committed receipt) — a
  round that performs no binding corrections cannot pass.
- **Kill rule (frozen):** calibration HELD at 9 and the claim not admitted if any attack seat
  constructs a runnable fixture with ALL static legs clean that passes
  `plans/round55_c2_entryargv.py` while the row's registry-declared entry truly exits otherwise
  (a soundness break). Rewriting a reviewed registry cell by hand is a documentation attack
  already carried by the r52 row-audit legs and the wave's reviewer cell audit; LEDGER-side
  tampering that the binding legs fail to flag fires this rule.
- **Score note:** declaring a truly-red row red is honest calibration and keeps the predicate
  satisfiable; the score moves only when the predicate passes, the kills fire, and no soundness
  break is demonstrated.

## R56-C3 — coverage 7→8 attempt (L0-capped) — the 13th TB2 grader admission completed with its maintainer oracle

- **Target axis:** coverage — the chess-best-move admission left incomplete by r55 (spotcheck
  defect 3: PROVINCE paragraph never landed) is completed, and the task's maintainer oracle is
  opened and cited, grounding the entry's expected-answer reading in a second primary source.
  Score capped at 7 by open L0 `kengaku | round-25/33/51`; the predicate is the counter.
- **Sources opened this round (2026-10-30), at pin
  `2fd12b88aafdd04a52c298e3940bcb189f9766d6`:** `chess-best-move/task.toml` (proposed **S203**,
  kind `spec`, tier A — the task's machine-readable definition) and
  `chess-best-move/solution/solve.sh` (proposed **S204**, kind `code`, tier A — the maintainer
  reference solution: it enumerates ALL immediate mating moves via python-chess and writes them
  one per line to `/app/move.txt`, matching the grader's order-insensitive full-multiset
  assertion `sorted(move) == sorted(["g2g4", "e2e4"])`). sha256 of both recorded at fetch; the
  round lesson's Gate carries URL, access date, and ≤25-word located quotes.
- **Before (frozen commands, base `1355e84c`):** `grep -c S203 corpus/SOURCES.md` → 0;
  `grep -c S204 corpus/SOURCES.md` → 0; `grep -c 'thirteenth' PROVINCE.md` → 0;
  `test -e corpus/evidence/round56/chess-oracle.md` → absent. Receipt
  `.ufo/waves/round-56/claims/c3-before.txt`.
- **After predicate (frozen):** S203 and S202-adjacent rows land via the append gate (census
  `validate` exit 0, no duplicate id, 11 columns); `grep -c S203 corpus/SOURCES.md` → ≥1,
  `grep -c S204 corpus/SOURCES.md` → ≥1; `PROVINCE.md` gains a dated round-56 partial-frontier
  paragraph stating 13 of 89 TB2 task graders read (grep `thirteenth` → ≥1);
  `corpus/evidence/round56/chess-oracle.md` exists, pins both upstream sha256s, and maps the
  oracle's all-mating-moves behaviour to the grader's expected multiset;
  `corpus/knowledge/tb2-chess-best-move-grader.md` gains an appended dated round-56 addendum
  section citing S203/S204 (appendix-only, recorded in LOG); the fleet census
  `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` exits 0 at
  round end. All commands run at the measured-after revision.
- **Do-nothing control:** base lacks every after-state artifact (committed receipt).
- **Kill rule:** the claim is not admitted if (a) the oracle contradicts the grader's expected
  multiset (e.g. the reference solution does not emit all mating moves), (b) either upstream
  identity check fails at the pin, or (c) the census rejects a new row. Any fired leg is an
  honest stop, reported.

## Round shape (frozen before dispatch)

ONE v1 wave (`w1`) under `/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json`,
**32 seats** — the round band was pinned to exactly 32 by the operator's final mid-run-13
ruling relayed by the orchestrator before the `.ready` handoff (superseding both the prompt's
16–32 snapshot and the interim 32–48 message; amendment dated 2026-10-30, before dispatch, no
seat has scored). Strict attack share = reviewer + critic + mutation-tester = 15/32 (46.9% ≥
25%); connectors 2; executor 8, scribe 3, scout 3, sentinel 1; no planner seat (the L1 holds
it). Four planned items were cut in the resize (census snapshot, control re-run, debt sweep,
LOG draft — absorbed by the L1). Dispatched through the inline spawn handoff (L1 writes
`w1.ready`, never calls `task`). No residual call planned; round total 32. Post-landing
re-verification is the L1's integration duty plus the outside closure.

## Sourced claim, assimilation, L0 routing

- R56-C3 is the round's sourced claim: S203/S204 are opened this round and cited by the oracle
  note and the entry addendum.
- Assimilation: **none** — the `merge/kengaku/` package mass id drift (114 collisions) remains
  under the unanswered L0 `kengaku | round-54`; nothing is adopted and no staged row is
  appended. `considerthese/` is mined for at most one still-unimplemented proposal, grounded in
  the round lesson.
- The r52 GH013 push-protection L0 stays unanswered: no new upstream capture bytes are
  committed this round (S203/S204 rows cite pinned URLs and record sha256 in the lesson and
  oracle note; no fixture tree is committed), so no push-protection surface is touched. The
  r55 erratum (defect 2) is filed in the round report.
