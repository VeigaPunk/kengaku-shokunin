# Round 56 — kengaku lesson (hyaku run 12, 2026-10-31)

author: kengaku L1 (KengakuR56, Windows host). Frozen claims: `plans/round-56-claims.md`
(freeze commit `8db18e23`, base `1355e84c`) + Amendment A2 (host move, this round). Wave
evidence: `.ufo/waves/round-56/`. The frozen 32-seat wave never dispatched (host retired
pre-data); the round's independent verification is the batched read-only seat dispatch
recorded in the round report plus the frozen instruments' own selftests and mutation kills.

## Gate

Sources opened this round (2026-10-31, `curl` GET of the pinned raw URLs from the new host,
bytes hashed on arrival). Both rows below are LANDED registry state (appended this round,
census-validated at round end):

| row | URL and location | access date | located quote (at most 25 words) | decision |
|---|---|---|---|---|
| S203 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/chess-best-move/task.toml — task.toml:6 (`[task] description`) | 2026-10-31 | `analyze a chess position from an image, use a chess engine to find the best move(s), and handle multiple valid solutions` (21 words) | admit A — the task's machine-readable self-definition; sha256 `d8f01d3c…fb22f9e` recorded in `corpus/evidence/round56/chess-oracle.md` (no capture bytes committed, r52 GH013 L0 unanswered) |
| S204 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/chess-best-move/solution/solve.sh — solution/solve.sh:186 (inside the `:180-189` all-legal-moves loop; write-all at `:232`) | 2026-10-31 | `best_moves.append(move.uci())` (1 word; the loop appends every legal move that mates) | admit A — the maintainer oracle for the expected answer; sha256 `53b5c5e2…76151f` recorded in the oracle note |

Upstream identity (fetched and sha-pinned this round): `task.toml`
`d8f01d3c84ed5836edbb49c6c3b3cc7b5b96d951cf01a0987467c9206fb22f9e`; `solve.sh`
`53b5c5e2278ca915b0930eedfd44565ca84ef21c7346fd6601434484cf76151f`; `tests/test_outputs.py`
re-fetched at the same pin `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286`
— byte-identical to the S201 pin and the r52 capture, so the oracle and the grader are the
same commit's words.

Flip check: no existing SOURCES row's `status`, `recheck` or `used-by` cell changes this
round (S201/S202 stand as landed; the oracle note and entry addendum cite them unchanged).
Rejections this round: none — both opens admitted; the runner-row duplicate drop of round 55
(A1) is not re-litigated.

Admit/reject spot-check (LEARNING.md discernment): sampled for the outside closure — admit
S203, admit S204, and the R56-F1 decision to route (not fix) the r46 checker's escaped-quote
false positive. The non-author closure re-opens these per the contract.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| provider — the WSL relay on this host expands `$?` before the inner shell sees it: every `echo "EXIT=$?"` through `wsl.exe ... bash -c` printed 0, including after a failed counter (`PREDICATE R55-C2 fail` followed by `EXIT=0`) and after a python traceback (`PROBE_EXIT=0`) | this round's scratch transcripts (impossible zeros: `false; echo $?` → 0 through the relay); the first direct r45-c1 "green" reading was an artifact of exactly this | none — the frozen receipts' `+ echo DRY-EXIT=1` discipline was written for a direct shell; nothing on this host warned the relay eats expansions | all measurement runs moved to script files written host-side and executed with in-file `echo "EXIT=$?" >> receipt` capture (`.ufo/waves/round-56/integrate/*` carry the true exits); rule adopted: never trust a `$?` relayed through a nested shell layer — capture exits into the artifact, not the console |
| provider — the measurement environment mutated mid-run: apt/pip/PPA installs raced executing batteries, producing phantom reds that reverted on re-run (two r37/r39 mutant "survivors" with biopython absent; r39 p10b rerun failing pre-pip; r45/r46 honest fixtures refused under git 2.43; r50 population mismatch 125/126 mid-git-upgrade) | run-2 receipts (`c2-base-work2/disagreed-*`) versus battery-3 receipts (`c2-base-work3/`): identical commands, different verdicts, environment the only delta | the freeze's own rule — "every after-run on a clean shared clone at the recorded measured-after revision" — caught it structurally; nothing flagged the runtime itself | the runtime is provisioned and frozen BEFORE any after-run (Amendment A2); the canonical after-run at the landing revision executes under the final environment, and the before-run that produced phantom reds is cited only as a mistake record |
| landing — a registry-cell edit added a pipe (`--evidence-ref head\|index`) into an 8-cell row; the r52 counter's pipe-splitter dropped the row and L-reg went `MISSING 1` | this round's verification run: `BINDING l1=1` then `MISSING plans/anchor_digest_check.py`, `PREDICATE R52-C2 fail` before the fix | the round-52 registry counter (the L-reg leg), run against the corrected tree before landing — the designed gate | cell edits must preserve the 8-cell structure; the static legs are re-run after every correction batch (this round: `BINDING l1=0 l2=0 l3=0`, `MISSING 0`, `PREDICATE R52-C2 pass` before landing) |
| scope — the stage-scan entry correction first proposed a `--selftest` argv; the r54 counter's entry contract forbids selftest/help/dry argv in ledger entries (`FORBIDDEN_ARGV_TOKENS`) and flagged `non-entry flag --selftest` | this round's dry run: `ARGV-DEFECT stage-scan: non-entry flag --selftest` | the r55 counter's static leg (the designed anti-laundering rule) | the corrected entry is the instrument's designed whole-tree scan, declared red on its measured output (`hits=860`, the cell's own documented generic-rule false positives) — the entry names what the instrument does, not what passes it |

## Frontier step — sourced claim

R56-C3 is the round's sourced claim: S203/S204 opened this round (Gate above), cited by
`corpus/evidence/round56/chess-oracle.md` and the dated addendum in
`corpus/knowledge/tb2-chess-best-move-grader.md`; the round-55 citation chain (defect 3) is
complete with a second primary source, and PROVINCE.md names the chess task as the thirteenth
grader read (13 of 89).

## Assimilation

`Assimilation: none` — shokuknow unreachable from this host (L0 `kengaku | round-54`
unanswered); `considerthese/` mined (eight files, 2026-10-19…26): proposal 2(c) of
2026-10-25 (tip-receipts) is already implemented and registered; the 2026-10-26 proposal
(r52 repair) stays refused on its demonstrated regression; nothing new adoptable this round.

## Corrections (2026-11-01, post-landing `1192e465`)

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| landing — the R56-F1 finding row's `source` field carried prose after the path:line and the findings counter rejected the row (`DEFECT line=76 source must read <path>:<line>`, `ROWS total=76 invalid=1`) | `c2-after-full.txt` (T run), `after-work2/c2/disagreed-routed-findings.txt` | the routed-findings counter itself — the lane's own machinery catching this round's data on its first executed run | corrected to `corpus/SOURCES.md:216`, history moved to `note`; the counter's shape rule is now a known constraint on every future finding row |
| scope — `round50-c1` was assumed green-on-this-host from a battery where it never executed (it was argv-defect-excluded from the executed 66 at base); its first execution (post-correction, entry joined the run set) shows the r50 population pins drift 125/126 on this host at base AND at the landing, all other legs green | `battery5.sh` r50-at-base receipt vs `c2-after-full.txt` (T run) | none — the assumption was mine; the falsifier was simply running the row | declared red with the measured POPULATION fragment; root cause (which fixture-identity input drifts under this host's git 2.56) left open and named, not guessed |
| provider — the r55 controls instrument hardcodes the old-host scratch root and needs `uv` on PATH for the uv-decoy fixture to genuinely run; both kills had crashed (exit 1 via traceback) before provisioning, which reads exactly like a fired kill | `c2-kill-*.txt` pre-battery-6 tracebacks vs post-provisioning receipts | the receipts' full output (a traceback is not a kill line) | provisioned `/fast/scratch/hyaku/kengaku-r55` (empty dir) and uv 0.13.6; kills now fire attributed (ARGV/ABBREV-DEFECT, ARGV/WRAPPER-DEFECT naming `fixture-gate`), selftest 4/4; polarity of the controls exit read from the instrument's own docstring (0 = expected kill state demonstrated), disclosed against the freeze's "exit 1" wording |

| scope — installing `uv` for the C2 controls silently flipped three r41 receipt-control fixtures that DECLARE a uv-absent environment (`r_ctl-t08-derived-uv-absent` observed runs where its frozen expectation says `skip:dependency-missing`; one mutant survived) — the same provision one instrument needed broke another instrument's declared environment | T' full-run receipt (`c2-after-full.txt`: laundered=1 round41-c1-mutants) + solo rerun `r41-solo.txt` (BATTERY wrong=3, deterministic) vs the S run (green, uv absent then) | the counter's own wrong-fixture lines name the skip expectations; the fixture names carry `uv-absent` | Amendment A3 item 4: per-instrument environment scoping — uv recorded for the controls receipts, then removed; the canonical counter environment is uv-less and named in full |

## Measured close (2026-11-01)

Canonical revision `9bc20ab7` (master checkout, uv-less): C1 `LANDCHECK PASS n=4` with three
single-leg mutation kills; C2 `PREDICATE R55-C2 pass` (executed=83, laundered=0, TIPSTATE
equal); C3 predicate met, score held 7. The two scoping rules of R56-F2 (uv-less canonical
counter; master-checkout measurement clones) and the four Mistakes rows above are the round's
transferable content. considerthese mined, nothing adopted; assimilation none.
