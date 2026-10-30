# Round 54 — anchor and entry-truth claims honestly stopped

Frozen claims: `plans/round-54-claims.md` at 17f90355c3ec17dcf15f7980d83f1943ae428fe5.
WAVE-DONE w1 received from Main: 66 seats settled (`.ufo/waves/round-54/w1-results.json`).
Both claims are not admitted; novelty stays 8, calibration stays 9. No capability enters.

## Gate

L1 opened these sources on 2026-10-30 using the read tool; source rows land only after that opening.
The entry `corpus/knowledge/external-anchor-freeze.md` is bounded sourced interpretation of a failed
instrument, not a successful anchor capability or new coverage claim.

| row | URL and location | access date | located quote (at most 25 words) | decision |
|---|---|---|---|---|
| S198 | https://opentimestamps.org/ — How it Works | 2026-10-30 | “A timestamp proves that some data existed prior to some point in time.” | admit A, existence-not-correctness interpretation |
| S199 | https://raw.githubusercontent.com/opentimestamps/opentimestamps-client/master/README.md — Usage, upgrade paragraph | 2026-10-30 | “You can also upgrade an incomplete timestamp, which adds the path to the Bitcoin blockchain to the timestamp itself” | admit A, pending-versus-confirmed lifecycle |
| S200 | https://raw.githubusercontent.com/opentimestamps/python-opentimestamps/master/opentimestamps/core/notary.py — BitcoinBlockHeaderAttestation docstring | 2026-10-30 | “The commitment digest will be the merkleroot of the blockheader.” | reject as sole canonical-chain or novelty evidence; a digest/header match is insufficient |

Flip check (round 54): S200 — not fired — no independently validated chain membership was landed;
the knowledge entry cites S198/S199 only. S200 is newly rejected, not a changed old row.
New rows are born mined/mined/rejected. No existing status, recheck or used-by cell changed.
Source proposals not adopted remain proposals in the wave directories. SC1/SC2 searches are
recorded in their reports; the L1 adopts this bounded three-source subset, not all six proposed rows.
Lane-dispatched reviewers are not the independent closure verifier.

## Mistakes

| class | evidence pointer | captured-by | fix / disposition |
|---|---|---|---|
| selected-argv-laundering | `.ufo/waves/round-54/claims/c2-route-r53.txt` and `w1/R2C2Counter/laundering-probes.txt` beneath the same round directory | Q42/Q43, r53 spot-check item 2 | Exact-token filtering closed the original toy route but not abbreviated selftest or uv-decoy argv: reviewer observed unchanged full-counter exit 0 on both. Frozen C2 kill rule fires; no claim of a completed fix. Q44 records the missed structural binding. |
| vacuous-negative-selftest | `w1/R1C1Counter.md` and its probe.py | Q42/Q43 | Raw-reader deserialization errors reject ordinary proofs and forged controls alike. Independent probe demonstrates raw-reader failure and correct-context success on identical bytes. Canonical C1 remains broken; Q44 requires a working positive path first. |
| declaration-transcription | `w1/R5LedgerStatic.md`, `w1/E2LedgerRefine.md` | independent ledger audits | Corrected scratch-root-guard declaration from exit 2 to observed exit 1; changed revision-sensitive and collapsed multiline evidence fragments. This repairs data, not the frozen counter's laundering hole. |
| unsafe-rider-integration | `w1/R4R52Fix.md` | non-author lane reviewer | Refused E3's proposed r52 patch: it makes order-check red and K7's unrelated failure masks the missing guard. Proposal retained as evidence, production counter intentionally unchanged. |
| unsupported-count-in-L0 | L0 question appended this round called the registry a 197-row space | E5CensusGate measurement | Append-only correction states 190 rows, highest ID S197, staged 175 and collisions 114. ID maximum is not row count. |

A fix is not counted merely because a criterion was added: C1/C2 code is frozen unchanged,
and surviving routes are retained. The working controls in `claims/c2-route-closed.txt` and
`claims/c2-env-poison.txt` cover only their named toy fixtures; reviewer evidence bounds them.

## Assimilation

Assimilation: none. `w1/E5CensusGate.md` derives 190 registry IDs, 175 staged IDs, 114 collisions;
three-space-indented collision guard is red-tested. No staged row appended; no renumber map
applied. `kengaku | round-54` L0 asks for re-staging disposition. Lists and collision bytes are
under `.ufo/waves/round-54/assimilation/` and E5's directory.

One considerthese proposal mined: proposal 2 of `considerthese/2026-10-26.md` (opened this round)
becomes Q44's filler-control requirement. No standing TB2 admission counter is claimed implemented.

## Measurement and limits

Before receipts: `corpus/evidence/round54/c1-before.txt`, `c2-before-dry.txt`.
After receipts: `.ufo/waves/round-54/integrate/c1-after.txt`, `c2-after.txt` record the measured
revision, command and exit without replacing the frozen rules. C2's reviewer-observed laundering
survivors independently fire its kill rule regardless of a literal ledger re-execution result.
No confirmed Bitcoin header or two independent explorer receipts are certified. Pending OTS
submission is not a verified timestamp, and ordinary proofs cannot pass the frozen C1 parser.
The r53 no-harm executions at 62e9bba5 are preserved in E7/E8 reports; E8 reproduces 78/78,
zero mismatches, green 66/red 12. No lane-owned axis score moves.

## Tooling and self-evaluation

L1 installed opentimestamps-client 0.8.0 and opentimestamps 0.5.0 using uv pip from the official
Python index into scratch; initial python-opentimestamps package-name resolution failed, then
opentimestamps-client installed the correctly named library. E9 additionally installed the same
client via uv tool plus an isolated uv environment; its canonical demonstration remained blocked
(blocker.txt). No pacman transaction. Tools are not proof that the counter works.

Self-evaluation: accuracy 2/5 (R1 API errors), completeness 3/5 (both targets missed, honest report
and receipts retained), clarity 4/5 (bounded interpretation replaces capability claim),
actionability 3/5 (Q44 and concrete reproducers identify repairs), conciseness 2/5 (overlarge
counter drafts). Average 2.8/5. Highest-impact next-round changes: real positive OTS path before
freeze; structural interpreter/entry binding before ledger scoring. The user should not treat this
round as an admitted improvement; the published record explicitly says so.
