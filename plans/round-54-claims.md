# Round 54 — frozen claims (kengaku, hyaku run 12, 2026-10-30)

L1 `KengakuR54`. Base tip `6c919180260ea545589c2c0a007a06f554b529d3` (lane branch `master`,
`jj-lane.sh state` `ahead=0 behind=0`, `git status --porcelain` empty at freeze). Frozen **before**
wave 1 is dispatched and before any scored run of either counter. A rule, counter, threshold or
predicate below is never changed after a seat has scored; a later change is a dated amendment in a
**separate file** (`plans/round-54-amendments.md`), never an edit of this file — this file's bytes are
the C1 anchor digest and must stay byte-identical for the whole round.

Inherited context honored (SCORECARD §Planned round 54): claims must distinguish an immutable
external history anchor from internally re-pinnable inputs (C1 does), distinguish entry-command
arguments from selftest/help arguments (C2 does), and avoid calling already-examined tests novel
(neither claim re-labels any TB2 test).

## Axis choice and the lowest axis

Lane axes (`../MISSION.md`): **novelty + calibration**. Scores at the base tip (`SCORECARD.md`,
round-53 section): novelty 8, calibration 9, depth 9, operability 9, freshness 9, adjacency 9,
**coverage 7**.

Coverage is the lowest non-retired axis and **is not claimed**: it stays capped at 7 by the open L0
questions `kengaku | round-25`, `round-33` and `round-51` (`.ufo/l0-questions.md`), none answered;
no answer is assumed (addendum §8: route around). The round works the next-lowest band exactly as
rounds 48–53 did: **novelty (8→9)** and **calibration (9→10)**. Stagnation nudge: not invoked
(coverage 7 < saturation line 8). No exploratory claim.

Both claims answer carried non-author findings, not new surfaces: the round-53 verifier spot-check
routed (1) "C1 integrity not proven — forged coordinated history can preserve FREEZE/ORACLE
agreement; novelty stays 8 until an immutable external history anchor exists" and (2) "C2
selected-argv laundering + worker git-config contamination; calibration stays 9"
(`corpus/lessons/round-53-verifier-spotcheck.md` items 1–2), both evidenced by
`.ufo/waves/round-53/w3/C1CritOracle2.md` and `w3/C2CritPredicate2.md`.

## Claim 1 — R54-C1 (novelty 8 → 9): an externally anchored measurement freeze that internal history forgery cannot reproduce

**Surface moved.** Round 53's C1 triage passed its frozen predicate but its integrity leg was
attacked successfully by a coordinated-history forgery: every input the r53 counter trusts is
internally re-pinnable, so a lane (or seat) that rewrites its own git history can make a
post-hoc bundle look frozen (`w3/C1CritOracle2.md`). What this round adds is the missing construct:
a freeze whose existence and pre-dating are witnessed **outside** the lane's writable state, by a
witness no lane seat can fabricate or backdate — an OpenTimestamps proof that the claims-digest is
committed into a Bitcoin block header, verified against block-header bytes and explorer receipts
fetched fresh this round. This is an instrument-level novelty move in the r50/r53 lineage (honest
geometry, triage soundness): the lane could not previously hold an unforgeable preregistration
freeze.

**Counting command (frozen).**

```sh
python3 plans/round54_c1_anchor.py verify \
  --anchor corpus/evidence/round54/anchor \
  --claims plans/round-54-claims.md \
  --source CLEAN_CLONE --work SCRATCH --controls
```

Exit 0 = predicate holds; 1 = predicate fails; 2 = setup/usage. Honours `TMPDIR`/`--work`; never
writes under a hard-coded `/tmp` path; requires `plans/round54_c1_anchor.py --ots-bin` (or `ots` on
`PATH`) only for `stamp`/`upgrade`; `verify` itself needs the `opentimestamps` Python library
declared below.

**Predicate legs (frozen).**

1. **BINDING** — the digest the proof timestamps equals the recomputed sha256 of the committed bytes
   `git -C SOURCE show <freeze-rev>:plans/round-54-claims.md`, where `<freeze-rev>` is the
   stage-1 commit recorded in `anchor/anchor.json`; the SOURCE clone is clean and at the landing tip
   (`git status --porcelain` empty, tip == lane branch tip).
2. **ATTESTATION** — the proof carries ≥1 `BitcoinBlockHeaderAttestation`; walking the proof's op
   tree from the file digest to the attested digest reproduces that digest (structural check over
   the deserialized tree, recomputed independently of the library's own walk); the attested digest
   equals the merkle root embedded in the committed 80-byte block header
   (`anchor/header.bin`, bytes 36:68), and double-sha256 of the header bytes equals the block hash
   recorded in the committed explorer receipts.
3. **EXTERNAL PIN** — `anchor/block-explorer-*.json` (≥2 files) are fresh fetches made **this
   round** from ≥2 independent public Bitcoin block sources, each carrying `height`, `hash`,
   `time`, `fetched-at`; all agree with the committed header (hash == double-sha256(header),
   height == attestation height, time == header nTime); attestation height ≥ 800000 (mainnet
   floor); header `nTime` is strictly earlier than the after-run wall-clock time recorded in the
   landing receipt (the freeze pre-dates scoring).
4. **CONTROLS** — `--controls` runs four forged cases against the same verification logic and each
   must fail: (a) forged proof (one flipped byte in the serialized op path), (b) wrong-bundle
   (real proof, different digest), (c) pending-only proof (built offline, no Bitcoin attestation),
   (d) absent proof. Any control that verifies is a predicate failure.

`PREDICATE R54-C1 pass` prints only when all four legs hold.

**Before (frozen, base tip 6c919180, do-nothing control).**
`corpus/evidence/round54/c1-before.txt` — at the base tip no anchor directory exists: the counter
reports `SETUP anchor absent` and `PREDICATE R54-C1 fail`, exit 1. This receipt is committed before
the anchor exists.

**After target.** The anchor directory is committed (`corpus/evidence/round54/anchor/`:
`claims.ots`, `header.bin`, `anchor.json`, `block-explorer-*.json`); the frozen command prints
`BINDING ok`, `ATTESTATION ok`, `EXTERNAL-PIN ok`, `CONTROLS forged=4 failed=4`,
`PREDICATE R54-C1 pass`, exit 0. Measured on a clean clone of the landing tip; receipt
`corpus/evidence/round54/c1-after.txt`.

**Controls beyond the counter (all receipts committed under `.ufo/waves/round-54/claims/`).**
Do-nothing (base tip, above); `internal-only` control — the r53-style FREEZE leg alone (git pins
only) accepts a re-pinned post-hoc bundle (the C1CritOracle2 route, reproduced in-repo as a
documented negative, no external fetch), demonstrating the construct the anchor removes; prior-art
leg — ≥2 fetched public sources with verdict lines (known / new / instrument-new) filed as
`SOURCES.md` rows opened this round and cited by the landing knowledge entry; this claim is
**sourced** by those rows.

**Kill rule (frozen).** The claim is dead (recorded, scores held) if any of: an attack seat makes a
forged or pending-only proof pass any leg; the explorer receipts disagree with the header; the
attestation cannot confirm in a Bitcoin block during the round (honest stop, predicate stays
failing); or the library/ots tooling cannot verify without network access the round cannot supply.
A miss is an honest stop, never a target change.

**Score rubric mapping.** New construct (unforgeable freeze — previously unobservable in this
lane), inspectable in-repo instrument (counter + anchor bytes + receipts), prior-art verdicts with
fetched URLs. If prior art shows Bitcoin-anchored preregistration freezes are published practice,
the honest verdict is replication/instrument-new and the score holds at 8 — the rubric's
replication clause is applied, not argued away.

## Claim 2 — R54-C2 (calibration 9 → 10): every registry row declared at its entry argv, hermetically executed; the selected-argv laundering route closed

**Surface moved.** The r53 tip-state counter compares declared vs observed exit for **the declared
argv**, and a ledger row may declare a `--selftest`/`--help` argv as its proof
(`kind_ok`, `MAX_HELP_FRACTION ≤ 0.10`): a gate whose entry mode fails can carry a green
selftest-declared row and the counter prints pass — the laundering route demonstrated by
`w3/C2CritPredicate2.md`. The same finding showed worker runs inherit the caller's git
configuration (git-config contamination can flip observed exits). This round: (a) a new ledger,
`plans/round54-entrytruth.json`, that declares every `SKILL.md` registry row at its **entry argv**
(no `--selftest`/`--help`/`--dry`/`--version` in the declared argv); (b) a new counter that
executes every row under a hermetic git environment (`GIT_CONFIG_GLOBAL` = counter-owned empty
file, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_COUNT` unset, scrubbed
`GIT_*`, scratch `HOME`/`XDG_CONFIG_HOME`, secrets scrubbed) and requires declared == observed;
(c) the round-53 ledger stays untouched (append-only discipline; corrections are new files).

**Counting command (frozen).**

```sh
python3 plans/round54_c2_entrytruth.py --lane . --source CLEAN_CLONE --work SCRATCH \
  --jobs 3 --timeout 900          # scratch under $HYAKU_SCRATCH/kengaku-r54/
python3 plans/round54_c2_entrytruth.py --lane . --dry
```

**Predicate legs (frozen).**
- REGISTRY: exactly one `## Gate/probe registry` heading, zero duplicate/malformed rows, every row
  names a `python3 <script>` entry (unchanged parsing contract).
- LEDGER: `plans/round54-entrytruth.json` (schema `r54-entrytruth-v1`) carries exactly the registry
  rows; each declares `entry_argv` in entry mode whose script matches the registry row's script;
  red rows carry a reason ≥ 10 words and a verbatim evidence fragment.
- EXEC: every row re-executed hermetically in the clean clone; `mismatched=0`, `timeout=0`,
  `evidence_missing=0`; `LAUNDERED` (declared green, observed nonzero) = 0.
- MIGRATION: `REDECLARED <n>` printed — rows whose r53 declaration was green with
  `kind != entry` while their entry-mode exit on the same tree is nonzero, re-declared truthfully
  red with reason+evidence. `<n>` is measured, reported, and never gated (any value admits); a
  value of 0 with an empty sweep is a defect.
- ENV: the counter's internal control proves hermeticity — a fixture gate that changes behaviour
  when a caller-supplied `GIT_CONFIG_GLOBAL` sets `user.name` must report identical observed exits
  with and without the poison under the counter's env, and must differ when run with the r53-style
  inherited env (the negative half lives in the controls script, not the counter).
- Clean tree: `git status --porcelain` empty; source rev == lane tip.

`PREDICATE R54-C2 pass` prints only when all hold; exit 0.

**Before (frozen, base tip, two receipts committed before data).**
1. `corpus/evidence/round54/c2-before-dry.txt` — `--dry` at the base tip: `LEDGER absent:
   plans/round54-entrytruth.json`, exit 1 (do-nothing control).
2. `.ufo/waves/round-54/claims/c2-route-r53.txt` — `plans/round54_c2_controls.py --route-only`
   builds a forged fixture lane (gate whose entry mode exits 1; ledger declares the same gate green
   at `--selftest`) and calls the **unmodified r53 counter** (`evaluate(..., pins=False)` import;
   the r53 counter file is never edited): its predicate prints **pass** on the forged fixture —
   laundering succeeds today. Exit 0 of the controls script marks "route demonstrated", which is
   the defect evidence.

**After target.** `PREDICATE R54-C2 pass` exit 0 on a clean clone of the landing tip with the
committed entrytruth ledger; and `.ufo/waves/round-54/claims/c2-route-closed.txt` — the same
forged fixture under the r54 counter prints `LAUNDERED <name>` / `MISMATCH` and the predicate
**fails** (route closed), plus `c2-env-poison.txt` — poisoned caller git config flips an
r53-env fixture row but not the r54-env execution.

**Kill rule (frozen).** Dead (recorded, calibration held at 9) if: any attack seat produces a
ledger row that passes the r54 counter while its true entry behaviour disagrees with the
declaration (laundering variant survives); or the hermetic env control cannot distinguish poisoned
from clean execution; or re-execution cannot complete (rows hang/time out at the cap) — honest
stop with measured partials. The r53 counter, ledger and its frozen predicate are never edited to
make this pass.

**Score rubric mapping.** The tip-state instrument is the lane's self-assessment-of-tooling;
making its green mean "entry behaviour observed, hermetically, zero mismatches" is the
advertised-vs-observed move the calibration rubric scores. The claim is falsifiable by the
committed controls; admission stays with outside closure.

## Separability and harm

C1 needs only the anchor artifacts and its counter; C2 needs only the entrytruth ledger and its
counter. Neither counter imports the other; either can be verified with the other reverted. No
frozen prior artifact is modified: `plans/round53-tipstate.json`, `plans/round53_c2_tipstate.py`,
`plans/round53_c1_triage.py`, `SKILL.md` (registry) and this file stay byte-identical through the
round. Harm watch: C2's re-execution runs gates in scratch clones only (never the live lane tree);
C1's `stamp`/`upgrade` calls external calendars over the network (no lane bytes uploaded beyond the
32-byte digest; no secrets; the digest is of a public repo file).

## Frontier-step contract (runs inside the claim cap; not a fourth claim)

- `corpus/SOURCES.md` census before/after via
  `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`
  (start receipt: exit 0, `kengaku ok`, 15 pre-existing W04 duplicate-URL warnings, 190 rows at
  `6c919180`). New rows opened this round ground C1's prior-art leg; every new row's Gate block
  carries URL, access date and a ≤25-word located quote; every `status`/`recheck`/`used-by` change
  is logged old→new in `corpus/lessons/round-54.md`.
- One mistake mined into `corpus/lessons/round-54.md` `## Mistakes`: class
  `selected-argv-laundering` · evidence `w3/C2CritPredicate2.md` + the route receipt · captured-by
  Q42/Q43 · fix = the C2 counter, counted only once shown able to fail (the route receipt is the
  red-before state; the closed-route receipt is the fix's only delta).
- At least one sourced claim: C1 cites the OpenTimestamps/prior-art rows opened this round.
- Assimilation: the merge-package id-collision check runs before any append (receipts in
  `.ufo/waves/round-54/assimilation/`); mass drift routes to an L0 question and adopts nothing.
  One `considerthese` proposal may land as a QUALITY.md criterion citing
  `considerthese/2026-10-26.md` + date.

## Round shape

One v2 wave of 64 seats under `scripts/hyaku/ufo-wave-policy-v2.json` (band 64–128), build and
attack items together, ≥25 % attack roles, a few connector seats. The planner seat is the L1's
(canonical §3 seat; the validator rejects `planner` as a swarm role — the bounded data-walk rides
scout/revenger items). Residual checks, if any, go into one ordinary `task` call of ≤8
reviewer/critic seats, counted in the round total.
