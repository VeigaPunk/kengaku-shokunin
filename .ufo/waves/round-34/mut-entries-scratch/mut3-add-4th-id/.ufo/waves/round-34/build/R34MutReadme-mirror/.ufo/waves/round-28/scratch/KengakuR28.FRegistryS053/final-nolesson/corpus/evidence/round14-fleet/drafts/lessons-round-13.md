# Lessons — round 13 (ack-label prompt-intent audit: placeholder pointing at the landed authoritative draft)

Status: **placeholder by ownership, not by absence.** Round 13's lesson text is
owned by the revenger and is already drafted verbatim inside
`corpus/evidence/round14-fleet/r14-revenger-r13.md` §3 (sha256
`6a6c910c751440c304099a9aa17d91a0b2783c16fbc25ea1e4981ff0f974ed2e`). Whoever
lands `corpus/lessons/round-13.md` should copy §3 verbatim rather than
re-derive it here; this file exists so the round-14 index does not silently
skip a round.

Source: `corpus/evidence/round13-ack-state/` — two committed-but-uncommitted
scripts, `analyze_ack_state.py` (md5 `9cbdc4665fb1fd760ccb2e2a3f31dded`) and
`audit_ack_schedule.py` (md5 `494928b959a4b9c3cbbcf7dc5d7a1df5`, both
re-hashed by this drafter), plus the round-13 plan
`.ufo/reports/round-13/kengaku.md` (plan only, 25 lines, no results section).

Revenger verdict (quoted): **SCRIPTS REPRODUCE CLEAN; LANDING INCOMPLETE
(G1–G6)** — 9/9 re-derivations pass (schedule mapping, four denominators, the
80-char cap, 84.4% bare-`ok`, the `[0.047, 0.125]` incidence bound, the pid-203
control, selftests 4/4 + 8/8), and the round's failure is purely a landing
failure: of five plan steps only the instrument code and its selftests reached
the repo. The absent deliverables: G1 prior-art pricing (survives only in
`/tmp/kengaku-round13-priorart.md`), G2 connector check (no file at all),
G3 kotoba routing (unevidenced), G4 `corpus/lessons/round-13.md`, G5 durable
measurement output (no `analysis_r13.md`; numbers lived in stdout and
`/tmp/kengaku-round13-final.json`), G6 LOG/SCORECARD/README rows. The scripts
themselves are G8 — landed but untracked, so they ride the round-14 commit.

Independently checked by this drafter (read-only, two greps): the `{7,10}`
schedule maps to true ack-only turns `{2,3,4,5,6,9}` and `384 = 64 × 6`, via
`audit_ack_schedule.py:26:true_ack_turns` (`range(2, total_turns+1)` minus any
turn in the schedule and minus any turn *after* a checkpoint — the spillover
ask); `analyze_ack_state.py` carries the same split inline
(`intent_for_turn`, `:55`, with selftest asserts at `:222-225`). `[INFERENCE]`
for `{4,7,10}` the same rule gives 4/10 turns, which is the shape of the
label-vs-intent mismatch this round exists to expose: r11 logged `A-CKPT710-ack`
512 rows (a storage label) where only 384 were prompt-intent ack-only.

The lesson to be landed (revenger's §3, five items, abbreviated here only to
mark the theme): a **logged cell suffix is a storage label, not prompt intent**
— intent must be re-derived from the runner's ask-construction code, never from
the cell name; **denominators fall out of the schedule, not the file** (encode
`true_ack_turns` once and assert the census); **cap-aware verdicts** (80-char
clipped raws are UNRESOLVED, not model errors — bounded estimate
`[18,48]/384 = [0.047, 0.125]`, cap hits kept as a third category); **the model
sometimes ignores the `ok` contract with a correct state** (18/384 unsolicited
snapshots exactly equal to simulator truth, a per-pid behaviour) — score
fidelity and compliance as separate axes; and the meta-lesson: **a measurement
that lands no durable analysis scores nothing**. See also
`lessons-round-14.md` — round 13 is the second consecutive round that stopped at
artifacts-on-disk, and this round's landing is what finally makes its numbers
citable.