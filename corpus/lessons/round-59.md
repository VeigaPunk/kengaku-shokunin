# Round 59 — kengaku lesson (hyaku run 14, 2026-11-02)

author: kengaku L1 (round 59, Windows host, WSL Ubuntu-24.04 instruments). Base `5420eac9`;
freeze `002cde8e`; amendment + measurements `e0512854`; erratum + red-before `85ef87e`. The
round's shape: the r58 closure's four routed items discharged first (receipts re-landed, the
finding-(b) correction row landed as a red→green gate, the prose corrections dated), one new
grader executed with an honestly-failed zero-U predicate, one new gate admitted.

## Gate

Sources opened this round (2026-11-02, `curl` GET of the pinned raw URLs at TB2 pin
`2fd12b88`, bytes hashed on arrival, captures committed at `002cde8e`): the full table with
quotes and sha256s is in `plans/round-59-claims.md` §Sources — S218 (task.toml, spec, A),
S219 (tests/test_outputs.py, code, A), S220 (solution/solve.sh, code, A — the maintainer
oracle), S221 (instruction.md, docs, A). All four admit tier A; no rejections; no flips of
existing rows. S219's bytes are byte-identical to the round-52 population capture of the same
path (two independent fetches, same sha256) — the pin holds across reads.

Flip check: S218–S221 are new rows (210→214). The census at round end: exit 0, verdict ok,
20 W04 duplicate-url warnings (15 pre-existing + 5 supersession duplicates — unchanged from
r58; no new duplicates this round).

Admit/reject spot-check (LEARNING.md discernment), sampled for the outside closure: admit
S220 (the oracle — the probe's sol candidate mirrors its construction step for step), admit
S219 (the executed six-leg predicate, byte-stable across reads), and REJECT-equivalent: the
decision to let R59-C1 stand as FAIL rather than re-freeze the table to the observation
(Q25's last sentence — the observed run cannot be re-scored; a corrected table is NEXT
round's freeze), and the decision to spend the Q25 amendment window on the gate's
unanchored tooth BEFORE any receipt of record rather than after (the over-count receipt is
kept as the amendment's evidence).

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| freeze-transcription — the 72-leg prediction table's perm-loose and key-1024 rows transposed their first two legs (dir, key): the freeze's own defect-class annotations name the key leg as the failing one, but both the markdown table and the probe's CASES tuples read F/P; the first and only capture run observed P/F on both (`mismatches=2`, `PREDICATE R59-C1 fail`, exit 1) | `corpus/evidence/round59/openssl-probe.txt` (the two MISMATCH lines); dated correction in `plans/round-59-claims.md` | the scored run — the probe's own mismatch counter, on the round's only capture run, after the freeze | a prediction table must be GENERATED from the case definitions in one pass (the probe gains a table-rendering mode; the freeze embeds that output verbatim), never retyped by hand into a second artifact — the r58 fixture-bytes lesson ("fixture bytes are copied from the landed artifact they imitated; never re-typed") applied to prediction tables: derived, never re-typed |
| instrument scope — the frozen consistency gate counted a bare `exit=` label with no ANCHORLINE payload as a defect; over the real population that tooth flags 13 legitimate arbitrary-command exit labels across five historical receipt files (no contradiction among any of them), turning the gate's before-state from the freeze's stated 2 into 15 | `.ufo/waves/round-59/recon/c2-overcount-frozen-gate.txt` (the over-count run, kept); amendment dated in `plans/round-59-claims.md` with both digests (`efd50ef6…` → `3767a447…`) | the gate's first full-population run, BEFORE any receipt of record landed — the Q25 window used in time | a consistency gate prices CONTRADICTION between two fields the artifact carries, never "unsupported by context I can't see"; a rule's defect class must be measured against the real population BEFORE the instrument freezes (the dev survey ran the anchor-pair rule only, not the unanchored tooth the gate gained while writing) |
| receipt-pointer — the same class as the r58 closure's finding (a), caught THIS round before it recurred: the round's first carry-in commit initially named a receipt path (`.ufo/waves/round-59/q20-gate-receipt.txt`) in the treecommit path list before the file existed in the worktree (the helper landed the other five paths; the receipt lands with the close commit) | the wave-M commit `e0512854` diff (5 files, the receipt absent); the receipt lands at the close | treecommit's explicit-path discipline: the diff was checked against the named paths immediately after landing | receipts are copied into the worktree BEFORE the treecommit names them; a commit that cites a path must carry the path |

## Carried → closed this round

- The r58 closure's finding (a) (five orphaned receipts): CLOSED at `5420eac9` — every cited
  path resolves at the tip, each a fresh dated re-landing run.
- The r58 closure's finding (b) (the exit-label bug): CLOSED at `85ef87e` — the correction
  row is the erratum, red→green with receipts (`.ufo/waves/round-59/recon/c2-red-before.txt`
  → `corpus/evidence/round59/receipt-consistency.txt`).
- The r58 closure's cosmetic items: dated corrections in `plans/round-59-claims.md`, the
  round-58 report's Corrections section, and the close LOG entry.
- R59-C1's predicate: FAIL carried honestly (not closed — the corrected re-freeze is r60's
  first work).
- L0 questions `kengaku | round-25/33/51` (coverage cap) and `kengaku | round-56` (L2
  surface; ledger host column): STILL OPEN, nothing assumed answered — coverage is claimed
  predicate-FAILED this round with the score held at 7; the L2 surface was routed around
  again (no in-session second seat; the L0 record stands).

## Mistakes (appended at the close-tip counter cascade, 2026-11-02 — the counters caught the round's own close wave)

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| anchor authoring — the S221 row's first quote was annotated `(6 words)` where the whitespace-split count is 7 (`"2." "Generate" "a" "2048-bit" "RSA" "private" "key:"`); the round46-c2 anchorline leg went live on it at the close tip (`live=1`), which laundered round46-c2 and failed all three anchor-scan routing checks (R45-S5-1, R56-F1, R58-F2) at the entryargv verification | `plans/round-59-claims.md` (the (21 words)/(9 words)/(13 words) annotations were derived and correct — the (6) was retyped); the cascade receipt (final-tip-receipts, wave W2) | the entryargv counter at the close tip — the designed capture | same mined rule as the first row, applied to SOURCES anchors: quote annotations are DERIVED by the counting command at authoring time, never retyped; corrected by the Q34 supersession S222 (count re-derived) |
| evidence receipt quoting — the Q20 roster receipt quotes each gate's selftest with a one-line `tail -1`, so the probe's bare `SELFTEST pass` summary landed in a file with no `rc=`/`want_rc=` lines, and the round's own consistency gate flagged it (vacuous pass) at the close tip | `.ufo/waves/round-59/q20-gate-receipt.txt` (the dated erratum appended); the gate's close-tip FILE line | the round's own receipt-consistency gate — its first live catch on its own round's receipt | a receipt that QUOTES another instrument's summary line carries the quoting context (erratum, dated) or the full block; summary-only quotations of pass lines are the whitewash shape the vacuous-pass rule exists to catch |

## Post-close cascade (appended 2026-11-02)

The final-tip verification at the close commit caught four landing defects in the round's own
close wave, all repaired before the round's receipts were committed: the S221 words miscount
(S222 supersession), the r35 stale-index fragment (62/62 dated refresh, the class's fourth
occurrence), the r46-c2 row's stale evidence field (refreshed to its round-58-measured state),
and the Q20 roster receipt's bare summary line (erratum). The r58 closure's fix rule held:
every receipt cited at landing is committed at landing, and the counters read them at the tip.
The pre-existing SHONEN box-4 pointer drift (the pinned PROVINCE.md:129 target line moved
before this round — verified red at the round base `5420eac9` too) was closed by the full-value
supersession R26-E11 in SCORECARD per the state_check P3 correction protocol.
