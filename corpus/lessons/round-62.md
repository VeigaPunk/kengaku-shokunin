# Round 62 — kengaku lesson (2026-11-02)

author: kengaku L1 (round 62, a retry session — the prior round-62 attempt landed no work,
verified against the base tree; Windows host, WSL Ubuntu-24.04 instruments). Base `c55a3f88`;
freeze `93f19d1a`; amendment `968f6ae7`; measurements `629f1267`; landing = the round's last
content commit. The round's shape: the planned survey pass landed as a mechanized grader-class
census (93 graders, 16 classes, 0 unclassified), and the round-61 closure's three findings
landed as dated corrections with re-deriving receipts — with the round's own gates catching the
author twice before the scored run completed.

## Gate

Sources opened this round (2026-11-02): **S226** — Terminal-Bench 2.0 top-level task tree at
pin `2fd12b88` (GitHub git-trees API),
https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6
— opened live via curl in WSL (the canonical environment); capture committed at
`corpus/evidence/round62/tb2-tree-2fd12b88.json` (sha256
`dd64bfb3b47c4bd6abe4bb37ba9b34511305dd06fe1a4afd4465dfe6ff5f0cd1`, `truncated: false`
in-file); located quotes "cancel-async-tasks" (a task-dir entry at :79) and "truncated" (:653).
Tier A code-host metadata for the narrow scope: the census's denominator grounding — the pin's
89 task dirs equal the round-52 roster name-for-name (priced `roster==tree=True` by the
instrument). Grounds R62-C1 (the sourced claim). **S227** — WHATWG Encoding Standard
windows-1252 index (the S225 URL re-opened live),
https://encoding.spec.whatwg.org/index-windows-1252.txt — sha256
`2c5fa192d566f92b8b9e6e116255b1f94016b4ece5b9dacb3b98be70b8c60795`, byte-identical to the S225
capture; the fresh re-open capture committed at
`corpus/evidence/round62/whatwg-windows1252-reopen/index-windows-1252.txt`; located quotes
"(LATIN SMALL LETTER A WITH CIRCUMFLEX)" (:105, the pointer-98 line) and "(EURO SIGN)" (:7).
Tier A docs for the narrow scope: the corrected-pointer superseding row (teaches opens
`supersedes S225 —`): index :105 is pointer 98 (cp1252 byte 0xE2 = 0x80 + 98 → U+00E2), not
S225's gloss "pointer 226". Grounds R62-C2 (the sourced claim — the D2 discharge). Both adopted
through `plans/sources_adopt.py` (leg 1: registry=218 staged=2 collisions=0 malformed=0
duplicates=0 defects=0, exit 0; leg 2: quotes 4/4 located+bound, exit 0; the append initially
landed both rows in the trailing Leads section — the census priced E12 on both — and was
repaired pre-commit, rows re-positioned after the S225 registry row; receipts
`.ufo/waves/round-62/recon/sources-adopt-run.txt`).

Flip check: S226 and S227 are new rows (218→220); S227 supersedes S225 (the registry's first
superseding row for that id — S225's cells untouched, per Q34); no rejections this round; no
other flips. Census receipts (round start and end, exit codes) are in the round report.

Admit/reject spot-check (LEARNING.md discernment), sampled for the outside closure: ADMIT S226
(tier A host metadata at the pin; the dir set is priced equal to the committed roster by the
instrument's own invariant) and ADMIT S227 (tier A spec index; the :105 line byte-locates in
the committed re-open capture; the corrected pointer re-derives: 0xE2 − 0x80 = 0x62 = 98).
REJECT-equivalent decisions sampled: (1) the misplaced sources append was NOT pushed-and-left —
the census priced E12 pre-commit and the rows were re-positioned before the freeze, with the
catch receipt kept; (2) the SETUP first scored run was NOT converted to a fail or silently
re-run at the same tip — its receipt of record was committed AS-IS and the missing inputs were
committed by a dated amendment before the receipt-of-record run (the r59→r61 mechanism: the
observed run is never re-scored at the same tip).

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| section-blind end-append — the adopted S226/S227 rows were appended at the file END with `cat >>`, landing inside the trailing "Leads (unopened)" section of a sectioned registry file (the r61 append happened to work because it inserted after the last row; the mechanism was never the rule) | `.ufo/waves/round-62/recon/census-start.txt` (the pre-freeze census priced E12 row-outside-Registry on both rows) + the repair receipt in `sources-adopt-run.txt` | the fleet census gate — a pre-commit catch, before the freeze | registry rows are inserted immediately after the last registry row (before `## Paths`), never `>>`-appended to a sectioned file; the census E-class runs BEFORE every commit that touches SOURCES.md |
| untracked-inputs-in-claims — the freeze named five files as "population of record (all committed bytes)" that had NEVER been tracked (the round-52 bookkeeping lists sat untracked in the Windows worktree for ten rounds); the worktree dry run could not see the gap | `.ufo/waves/round-62/recon/scored-run-SETUP.txt` (the first scored run's SETUP, CLASS-SURVEY-EXIT=2, receipt of record committed AS-IS); amendment `968f6ae7` commits the five files byte-as-is | the clean-clone scored-run discipline itself (the worktree lies — the r61 environment lesson, mined a second way in a new form: not tempdirs or /mnt/c, but untracked files a worktree run silently reads) | every input a claims doc names as committed is `git ls-files`-verified at the freeze; scored runs only ever run in fresh clean clones |
| runner exit-swallow (the r60 harness hazard, new form) — `set -e` inside a `{...} 2>&1 | tee` group aborted the group at the census's non-zero exit, so the receipt's `CENSUS-START-EXIT=` echo never printed (the same swallow removed the receipt-gate's exit echo at its SETUP) | `.ufo/waves/round-62/recon/census-start.txt` (header names the swallow) vs `census-prefreeze-rc.txt` (the pipe-free re-capture, rc=1) | my own receipt audit (the exit line missing from a receipt whose subject exited non-zero) | exit labels are captured pipe-free (`cmd > out 2>&1; echo rc=$?`) or via PIPESTATUS — never inside a set -e group piped to tee |
| receipt-from-memory prose (the round-61 closure's R61-D1/D3 class, mined as a standing fix this round) — the r61 amendment prose and lesson narrated the receipt's diff as ONE row and the EOL counts as idealized numbers instead of reading the receipt / running numstat | the dated corrections in `plans/round-61-claims.md` + the lesson erratum in `corpus/lessons/round-61.md`; measured numbers in `.ufo/waves/round-62/recon/carryin-facts.txt` | the round-61 non-author verifier (routed) | prose that describes a diff or quotes counts is written from the receipt's own bytes with the counting command recorded at write time; the round-61 errata carry those commands and they re-derive under the correction gate |
| detector-table blind spot (self-caught pre-freeze) — the first frozen detector table had no class for grader-imports-candidate (`import attack|solution`, `sys.path.append`) or `os.popen`-style shell-exec, so the executed FEAL grader fell UNCLASSIFIED | `.ufo/waves/round-62/recon/census-dryrun-worktree.txt` take 1 (INVARIANT-FAIL every-executed-grader-classified, PREDICATE fail) | the survey's own executed-coverage invariant, on the pre-freeze dry run | a detector table is proven against the EXECUTED corpus (not only toys) before the freeze; an executed grader that no detector classifies is a table defect first and a finding second |

## Carried → closed this round

- The round-61 closure's R61-D1 (amendment-prose undercount: three differing lines, not one):
  CLOSED — the dated correction in `plans/round-61-claims.md` (its commands re-derive under
  the correction gate at the pre-freeze check, the measurements tip and the close receipt) and
  the dated erratum in `corpus/lessons/round-61.md` (rows byte-identical, R1; the receipt stays
  as captured).
- The round-61 closure's R61-D3 (idealized EOL counts): CLOSED in the same two dated appends —
  measured from the git objects (base 272/0-CR; freeze 274/274-CR; numstat +274/−272 = 546;
  repair 0-CR net +2/−0); the spot-check's 511 variant superseded by the measured numbers.
- The round-61 closure's R61-D2 (S225 gloss pointer/byte swap): CLOSED by the superseding row
  S227 (Q34 form; S225 byte-identical; the correction is grounded in the re-opened capture).
- Standing opens routed/closed with evidence: the three L0 questions
  `kengaku | round-25/33/51` (coverage cap; decision packet; absent surfaces) and the
  `kengaku | round-56` pair (L2 surface; ledger host column): STILL OPEN, nothing assumed
  answered — coverage is claimed predicate-met this round with the score held at 7. The
  `kengaku | round-52` push-protection question remains disposed by the committed operator
  decision `corpus/evidence/round52/graders/EXCLUDED.md`.

The close rule for every future round, extended this round: tables and member lists are quoted
from the receipt, never hand-tabulated; every committed-input claim is ls-files-verified at the
freeze; scored runs run only in clean clones; registry rows are inserted after the last
registry row; exit labels are captured pipe-free.
