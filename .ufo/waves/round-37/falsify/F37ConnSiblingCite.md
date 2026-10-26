# F37ConnSiblingCite — falsify of round-37 sibling citations

Seat: F37ConnSiblingCite (connector, leaf, read-only). Date: 2026-10-26.
Inputs: `.ufo/waves/round-37/build/R37ConnSibling.md` (wave-1 sibling scan) and the landed
round-37 surfaces at tip `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`: `PROVINCE.md` (round-37
paragraph + reported-out, lines ~264-285), `SKILL.md`, `corpus/lessons/round-37.md`,
`corpus/README.md`, `SCORECARD.md` (§Round 37, lines 1266-1313), `LOG.md` (§Round 37, lines
1082-1103), `corpus/knowledge/tb2-git-webserver-grader.md`, `plans/git_webserver_probe.py`,
`plans/round37_c1_verify.py`, `plans/round37_c2_verify.py`.

Method: read-only greps over the landed surfaces; no clone, no counters (this seat judges
citation coverage, not predicates). All commands run from
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

## What the wave-1 connector established

R37ConnSibling scanned all 21 fleet lanes and ruled: **contested = 0** across S1-S4; **adjacent
= 14 lanes** — union {kama (S2), tameshi, kumitate, kaidoku, tsukuroi (S3), tameshi, kumitate,
kasegi, kaidoku, chousa, mado, mori, souji, kagi, revenger, tabi, kake, tsukuroi (S4)}. It ended
with an explicit "Instruments kengaku should cite rather than duplicate" list of four:

1. `tameshi-shokunin/tools/mutate-and-run.sh` — fleet's shared exit-graded mutation runner
   (mado pins it as `MADO_VERIFY_HARNESS`, `mado-shokunin/SKILL.md:624`).
2. `kumitate-shokunin/scripts/gate-mutants.mjs` (`SKILL.md:616`) — direct gate-mutation battery
   precedent.
3. **tameshi defect-probes bwrap pattern (`SKILL.md:1929`)** — "guard-removal mutant[s] …
   children run under bwrap with the fleet read-only"; the report calls this "the exact
   C1∧C2 combination, predating r37" (S3, tameshi entry).
4. **kumitate `cap-run.mjs` (`SKILL.md:618`)** — the fleet's bwrap-bounded runner
   (`env -i` + `bwrap --unshare-pid --die-with-parent --new-session --clearenv`); the fleet L0
   question (kumitate r64) already asks whether forgeable counters should be replaced by a
   bwrap-bounded runner.

## Q1 — Is every adjacent sibling named with file:line?

**No.** The PROVINCE round-37 paragraph names exactly four of the fourteen adjacent lanes:

- `PROVINCE.md` Adjacent line: "web properties (kake), serving plane (kama)" — named, **no
  file:line** (the connector's evidence was `kake-shokunin/corpus/README.md:41` and
  `kama-shokunin/SKILL.md:70-195` with verdict classes at `:178-182`).
- `PROVINCE.md` reported-out line 283: "tameshi's `tools/mutate-and-run.sh` and kumitate's
  `gate-mutants.mjs` are the precedents" — named with paths, **no file:line** (connector gave
  `SKILL.md:616` for gate-mutants); routes to `R37ConnSibling.md` §S4 for the rest.

The §S4 pointer does carry file:line for all 13 S4 lanes, so the S4 mutation-testing adjacency is
covered **by reference**. What is not covered anywhere in the landed surfaces:

- **kaidoku** (S3, `SKILL.md:606` — bwrap named as a bypass class) — zero mentions.
- **tsukuroi** (S3, `SKILL.md:3005`, `:3110` — unprivileged user+mount namespace arms) — zero
  mentions.
- kama's S2 instrument (the live HTTP classification probe, `SKILL.md:70-195`) — the lane word
  "serving plane" names the province, not the adjacent instrument the connector flagged.

Evidence commands:
- `grep -n -iE 'kaidoku|tsukuroi' PROVINCE.md SKILL.md corpus/lessons/round-37.md SCORECARD.md
  LOG.md corpus/README.md` → no round-37-context hit (kaidoku appears only in SCORECARD
  round-12/33 history rows at lines 693, 1034; nothing in round-37 surfaces).
- `grep -n -iE 'tameshi|kumitate|kaidoku|tsukuroi|kasegi|chousa|mado|mori|souji|kagi|revenger|
  tabi|kake|kama|sibling|adjacent|prior art' corpus/lessons/round-37.md` → **exit 1, zero
  matches** in all 116 lines of the round lesson.

## Q2 — Is contested scope reported rather than absorbed?

**Yes — this part is clean.** The connector ruled contested = 0, so there is no contested scope
that had to be reported; the boundary items that exist are all routed in the landing:

- Real-image Docker run: "Any observation from a real-image run is a separate, routed
  observation and is not part of this admission" (`PROVINCE.md` round-37 paragraph);
  "Routed, not absorbed" (`LOG.md:1099`); "Refused for the corpus; routed"
  (`corpus/lessons/round-37.md` Gate table, with its limits named).
- Serving plane / deployment configuration / runtime task validity: refused and named
  (kama/kake in the Adjacent line).
- kumitate's TB2 coordinator-topology data citation (`multi-agent-coordinator-topologies.md`)
  was ruled a data citation, not a grader claim — nothing owed, nothing absorbed.

## Q3 — Would any sibling's instrument have been cited?

**Partially — the two sandbox instruments the connector explicitly recommended are missing.**

Citation status of the connector's four-instrument list across the landed round-37 surfaces
(`grep -n -iE 'cap-run|defect-probes|mutate-and-run|gate-mutants|bwrap|bubblewrap'` over
`PROVINCE.md`, `SKILL.md`, `corpus/lessons/round-37.md`, `SCORECARD.md`, `LOG.md`,
`corpus/README.md`, `corpus/knowledge/tb2-git-webserver-grader.md`, `plans/git_webserver_probe.py`,
`plans/round37_c1_verify.py`, `plans/round37_c2_verify.py`):

| # | Instrument | Recommended? | Cited in landing? |
|---|---|---|---|
| 1 | tameshi `tools/mutate-and-run.sh` | yes | yes — `PROVINCE.md:283` (no file:line) |
| 2 | kumitate `gate-mutants.mjs` | yes | yes — `PROVINCE.md:283` (no file:line; connector gave `SKILL.md:616`) |
| 3 | tameshi defect-probes bwrap pattern, `SKILL.md:1929` | yes — "the exact C1∧C2 combination, predating r37" | **no — zero hits in any landed surface** |
| 4 | kumitate `cap-run.mjs`, `SKILL.md:618` | yes — fleet bwrap-bounded runner; L0 r64 says forgeable counters sit in its class | **no — zero hits in any landed surface** |

This is the material gap. Round 37's C2 core mechanism **is** a graded verdict produced inside a
per-case bwrap sandbox (private network namespace — `PROVINCE.md:271`,
`tb2-git-webserver-grader.md:21,128`), and the wave-1 connector found that exact combination
already existing in the fleet at tameshi `SKILL.md:1929`, with kumitate `cap-run.mjs:618` as the
fleet's general bwrap-bounded runner — and recommended both be cited. Neither appears in
PROVINCE, SKILL.md, the knowledge entry's prior-art section (which cites only upstream S114),
the round lesson, the SCORECARD round-37 section, the LOG round-37 section, or the probe/counter
source. The landed text describes the sandbox mechanics without once noting the fleet prior art,
so a reader of the landing cannot tell the bwrap-graded-verdict pattern was tameshi's and
kumitate's before it was kengaku's.

TB2 audits: the connector found no sibling reads or claims TB2 scoring code
(S1 — "pinned-grader-probe remains kengaku-only"), so no TB2-audit citation was owed. Not a gap.

## Gaps (3)

1. **Sandbox prior art uncited (2 instruments).** tameshi `SKILL.md:1929` (defect-probes under
   bwrap — "the exact C1∧C2 combination, predating r37") and kumitate `cap-run.mjs`
   (`SKILL.md:618`) were explicitly recommended by the connector and are absent from every
   landed round-37 surface, despite C2's centre of mass being a bwrap-sandboxed graded verdict.
2. **S2/S3 adjacents unnamed.** kaidoku (`SKILL.md:606`), tsukuroi (`SKILL.md:3005`, `:3110`)
   and kama's probe instrument (`SKILL.md:70-195`, verdict classes `:178-182`) are not named in
   any round-37 landing surface; `corpus/lessons/round-37.md` names no sibling at all (116 lines,
   zero matches). Only the S4 set inherits names via the §S4 pointer.
3. **File:line precision missing on the two precedents that were cited.** `PROVINCE.md:283`
   names tameshi/kumitate without file:line, where the connector supplied them (`SKILL.md:616`,
   and the S3/S4 tables) and the round-36 precedent in the same file cited sibling provinces
   with `PROVINCE.md:line` refs. Mitigated but not closed by the §S4 pointer.

## What is not a gap

- Contested scope: 0 contested; all boundary items (real-image run, serving plane, deployment
  config, runtime task validity) are routed or refused in the landing, not absorbed (Q2 clean).
- TB2-audit citations: none owed — no sibling holds TB2 grader ground (S1).
- The S4 mutation-testing adjacency is fully named with file:line in `R37ConnSibling.md` §S4,
  to which `PROVINCE.md:284` routes.

VERDICT: sibling-cite-3-gaps
