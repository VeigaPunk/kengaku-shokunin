# Round 60 — kengaku lesson (hyaku run 14, 2026-11-02)

author: kengaku L1 (round 60, Windows host, WSL Ubuntu-24.04 instruments). Base `9482c840`;
freeze `9e37311f`; corrections landing = the wave-C commit; receipts commit = the round's
last commit. The round's shape: the r59 closure's four routed defects discharged, the r59
C1 completion landed as the Q25-sanctioned new claim (72/72, the sixteenth grader's
admission completed), and the counting-command reproduction gate admitted red→green.

## Gate

Sources opened this round (2026-11-02): **S223** — GNU Grep manual, general output control
(`-c`/`--count`), https://www.gnu.org/software/grep/manual/grep.html — opened via `curl -sS
-o grep.html <URL>` in WSL (the canonical environment), bytes hashed on arrival (sha256
`517177d02c39c446470c898273036a7616f705e4cbdcb6486b76a25700675f37`), capture committed at
`corpus/evidence/round60/grep-manual/grep.html`; located quote at capture line 379:
"instead print a count of matching lines for each input file." (11 words, the count derived
by command at opening, never retyped). Tier A (official docs) for the narrow scope: what
grep -c counts, and what it does not. Grounds R60-C2 (the sourced claim): grep -c counts
MATCHING LINES — a phrase spanning a wrapped line does not match; that is both the r59
routed defect's mechanism and the reason the gate's frozen scope fence is the grep -c
family. Adopted through `plans/sources_adopt.py` (quote validation + registry admission,
exit 0; 215 staged rows before; collisions=0, malformed=0, duplicates=0).

Flip check: S223 is a new row (215→216); no rejections this round; no flips of existing
rows. Census receipts (round start and end, exit codes) are in the round report.

Admit/reject spot-check (LEARNING.md discernment), sampled for the outside closure: ADMIT
S223 (tier A for its narrow scope; the quote byte-locates in the committed capture; the
word count is derived). REJECT-equivalent decisions sampled: (1) the drifted token was
priced at its CURRENT count (2) with the drift mechanism named — reverting this round's own
wave-F LOG entry to keep "→ 1" true was refused (R1: append, never rewrite; the current
count is the truth the gate prices); (2) the fleet-root round-58 report erratum append was
mirrored + routed, NOT committed by this lane (the round contract makes fleet commits the
orchestrator's; the lane's mirror is durable evidence either way).

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| harness exit capture — the gate's first interactive invocation printed `PREDICATE R60-C2 fail` yet the shell reported exit 0: the `wsl.exe … bash -lc '…; echo $?'` harness swallows `$?` (a `sys.exit(1)` sanity probe also printed 0 through the same chain) — the r58 finding-(b) class in my own capture, one step from laundering the red-before | the runner script's captured `rc` (GATE-RC=1 via `wsl --cd … -- cmd`) vs the harness echo (0), same command, same tree; the wave-M transcript header records the rule | my own first gate invocation, cross-checked with a `sys.exit(1)` sanity probe | every receipt's exit label is captured INSIDE a runner script (`rc=$?` after each command; PIPESTATUS for pipelines), never via the harness echo; receipts keep the r59 wave-W3 form |
| self-quoting drift — this round's own wave-F LOG entry quoted the drifted token with its r59-era result (`grep -c 'four tip counters' LOG.md` → 1) and thereby doubled the token's line count before the erratum landed; the frozen gate priced the claims-doc erratum draft live (`CMD-DEFECT got=2 want=1`) — its first live catch is a new instance of exactly the class it prices, created and captured in the same round | `.ufo/waves/round-60/recon/c2-green-after.txt` (the `got=2` line, converted to errata by the marker); `plans/round-60-claims.md` Amendment 1 | the round's own gate — the designed capture | a correction/receipt that quotes a counting command quotes command AND result at CURRENT truth (or omits the literal); the landed erratum prices both forms at current truth (stable fragment → 1 ok; drifted token → 2 ok) and names the doubling mechanism |
| same-line pairing — the first erratum draft carried two backticked grep commands on one line; the gate's frozen regex pairs the first command with the first following arrow, so the two commands mis-paired (the draft's defect line was the WRONG command's mismatch) — a parsing limit my own draft exposed before landing | the dev-check transcript at the corrections worktree (`CMD-DEFECT …:240 got=0 want=1` under the two-commands-on-one-line draft; the landed one-command-per-line form prices both correctly) | the round's own gate over its own erratum draft | erratum/correction text carries ONE command per line; the limit is recorded as the instrument's named limit in `plans/round-60-claims.md` Amendment 1 (the gate's frozen bytes are NOT touched — receipts of record exist, so a docstring edit would be a post-receipt instrument change) |

## Carried → closed this round

- The r59 closure's routed defect 1 (the fleet working-tree erratum): mirrored byte-for-byte
  (`.ufo/waves/round-60/r58-report-corrections-mirror.md`) + routed to the orchestrator in
  the round report — closed FOR THIS LANE (the fleet-root landing is the orchestrator's).
- Routed defect 2 (two `path@hash` citations miss the landing commits): closed — measured-at
  AND landed-at named in the SKILL registry row and the PROVINCE round-59 paragraph (dated);
  the fleet-report occurrences ride the mirror + report.
- Routed defect 3 (the correction command that does not reproduce): CLOSED by R60-C2 — the
  dated erratum + the gate (red→green with receipts).
- Routed defect 4 (SCORECARD 210→214 stale by S222): closed by the dated touch-up in the
  SCORECARD r59 precision-corrections block (210→215 at the r59 tip; 215→216 this round).
- R59-C1: CLOSED — the corrected zero-U re-freeze admitted (72/72; the completion paragraph
  in PROVINCE; the knowledge-entry addendum; registry/ledger rows green with dated reasons).
- L0 questions `kengaku | round-25/33/51` (coverage cap) and `kengaku | round-56` (L2
  surface; ledger host column): STILL OPEN, nothing assumed answered — coverage is claimed
  predicate-met this round with the score held at 7; the L2 surface was routed around again
  (no in-session second seat; the L0 record stands).

## Mistakes (appended at the close-2 landing, 2026-11-02 — the ladder's third rung)

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| self-quoting ladder, rung 3 — the close LOG entry and the SCORECARD close-tip addendum quoted the two erratum-priced fragments (naming their continuation-1 results while closing out the cascade), moving both counts AGAIN before the final tip: the corrections tip printed errata=3, the close tip errata=5, and the entry-truth counter flagged the stale fragment both times | the final-tip takes: take 1 `RUN executed=90 … evidence_missing=1 laundered=1` + `TIPSTATE declared 61g/29r vs observed 60g/30r` (stale fragment); take 2 the same flag on the refreshed-then-re-staled fragment; `ERRATUM CONTINUATION 2` in `plans/round-59-claims.md` (the ladder 1→2→3→4 written out) | the round's own entry-truth counter and gate — the designed capture, twice in a row | STRUCTURAL STOP, in force from the close-2 landing: no lane prose quotes an erratum-priced fragment again — later text names the CLASS (the self-quoting drift of erratum-priced counting commands), never the token; ERRATUM CONTINUATION 2 prices the current truth (one command per line); the older priced lines convert permanently (errata=5 is the stable tip truth) and the ledger fragment follows, dated |
| receipt quotation clip — this round's Q20 gate receipt quotes the probe selftest as a tail -3 context clip whose bare summary carries no rc/want line inside the quote: the r59 W2 vacuous-pass class, caught by the r59 gate at the final tip (`FILE .ufo/waves/round-60/gate-receipt.txt defects=1 :: line 13`) | `.ufo/waves/round-60/gate-receipt.txt` + the appended dated erratum | the r59 receipt-consistency gate at the final tip | the same r59 rule, re-learned at a new site: a receipt that QUOTES another instrument's summary carries the quoting context or the full block; the erratum names the clipped lines and the run-level exit label below the quote |

The close-2 rule for every future round: when a landed text must reference an
erratum-priced counting command, it cites the erratum's location — never the command's
literal pattern.
