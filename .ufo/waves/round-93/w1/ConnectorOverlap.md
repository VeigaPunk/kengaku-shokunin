# ConnectorOverlap — sibling-overlap scan (round 93 w1, seat report)

Scope: read-only scan over all 21 sibling lanes `/home/vgpnk/Projects/shokunin/*-shokunin` and the
fleet-root `scripts/`, per the item brief. Questions asked: (1) does any sibling lane or fleet
script already own a gate that compares frozen-instrument bytes against a freeze commit; (2) does
any sibling replay Terminal-Bench 2.0 graders; (3) for each overlap found: path:line, what it
does, and whether kengaku's round-93 gate **duplicates / complements / should be routed** to that
owner. Read-only; nothing absorbed. Reverse bounds respected (no subagents, no commits, no lane
mutations, no fleet-root writes; only this wave dir + scratch, scratch since removed).

Raw receipts: `w1/ConnectorOverlap/upstream-404-receipts.txt` — verified mechanism descriptions and
per-instrument dates; `w1/ConnectorOverlap/adjacency-dates.txt` — `git log -1` per adjacent path;
`w1/ConnectorOverlap/members-in-wrench.txt`, `kengaku-members.txt`, `kengaku-member-census-r52.lst`,
`wrench-tasks.json` (gz) — member-set cross-references. Scratch `/fast/scratch/hyaku/kengaku-r93/ConnectorOverlap/`
was created and removed via `trap ... EXIT` (job had already run to completion).

## Finding 1 — no sibling owns the mechanism; duplication risk is LOW (info)

Whole-fleet grep (all lanes, .py/.sh/.md files) for `frozen.?instruments|instrument.?sha|gate.?sha|
pin.?ledger|sha256sum` yields instruments that compare bytes at a **pin** or at a **freeze**, but
none reads a claims-file table of *several* instruments against one freeze commit. Nearest
capacities, all of them complements rather than duplicates:

| # | Lane / path | What it does | Adjacency |
|---|---|---|---|
| 1 | `souji-shokunin/tools/souji-freeze-check.py:196-218, 400, 446` (r41 waves, selftest cases `frozen-edited/control-edited/prereg-edited` at `:498/:527/:529`) | per-claim prereg gate: a declared `Counter`/`Population`/`Control` `<path> sha256=` must match the blob at the freeze, and that blob must equal the blob at the measured rev (`FROZEN-EDITED`); refuses a freeze otherwise | **complement** — same SHA-compare-at-freeze mechanism shape, but per-claim prereg grammar and a different lane's spec shape; no claims-table reader |
| 2 | `kasegi-shokunin/corpus/instruments/freeze-check.py` (r45; sha `c3c19adc…`, selftest 27/0) | replays each claim's frozen `counter_cmd` at the base tree so the RED control is actually red before landing ('red-before'); detects base mutation via mtime snapshot | **complement** — freeze semantics of counter output, never bytes at tip |
| 3 | `chousa-shokunin/tools/freeze-check.py` (r60; `948afaa0`) | pins `CLAIMS_NONEMPTY` (reference digest) and RENDER/CHECK/READY facet consistency in wave spec/dispatch/ready payload | **complement** (pre-dispatch data-flow, not history) |
| 4 | `chousa-shokunin/tools/research-gate.sh` `--pin/--drift` (`:220-260`) | pins a behavioral baseline header (`gate_sha256=` passed to mori r10's census.sh pin contract), byte-compares a canonical re-run | **complement** — output behavior, not freeze-vs-tip bytes |
| 5 | `mado-shokunin/tools/mado-tripwire.py` (`--frozen DIR`, digest-pinned replay :130-131) | tamper tripwire digest-pinning its own r18 expected.json, not a claims table | **complement** |
| 6 | `tabi-shokunin/.ufo/waves/round-22/run-checks.py:68-107` (preservation-baseline.json) | permuted-tree diff gate over a manifest of *committed e2e evidence files* for one round; not reusable, not claims-aware | **complement** |
| 7 | `kaidoku-shokunin` wave receipts r36-r50 (e.g. `.ufo/waves/round-49/w2/W2Chronology/receipts.sh:25`) | one-off `git show $F:$f | sha256sum` loops inside ad-hoc scripts — the manual chore kengaku's gate mechanises; never extracted into a standing instrument | **complement** — kengaku is the mechanising owner |
| 8 | `mori-shokunin/tools/mori-freeze-order.py` (`c0fe0b23`, r18 admission; selftest 12/12) | checks whether frozen claim inputs **predate their implementation commits** (chronology gate; diff-tree + rev-list, never byte-compare at rev) | **complement** |
| 9 | `mori-shokunin/tools/mori-pin-check.py` (r47 v4; `1592f53d`) | re-measures SKILL.md registry self-test pins against real argv/paths (K8 pass-form, K5 family join, sha256 pins read from the registry) | **complement** — an alternate adversary (silent registry pin rewrite), not a claims freeze |
| 10 | `kengaku-shokunin/plans/round90_counter_pin.py` + `round91_counter_pin.py` (`counter-pins-r{90,91}.json`) | the lane's own prior generations: an external pins JSON (r90), then a self-pinning extension (r91) | **superseded-in-purpose by R93-C2** — the bytes are pinned beside the claims file in a `frozen-instruments` table and read by the gate directly (9 rows); the r90/r91 JSON ledgers are not claimed this round and the frozen rule prevents in-round absorb; a route note for round 94 is enough rather than an absorb |

**Fleet-root `scripts/`** (`hyaku` plumbing, `jj-lane.sh`, `fleet-commit.sh`, `append-closure.py`,
`inline-dispatcher.py` etc.): zero hits for freeze-integrity or same-shape byte-compare logic. No plug point exists.

Fleet root's LEGACY `counters/` and `reports/round-92/` directories exist but are EMPTY — no orphaned shared gate.

Note on Routeability: `PROTOCOL.md:411-416` freezes the integrator boundary — a sibling gate is
verified through its committed evidence, never executed by another lane. Even if a sibling wanted
R93-C2's mechanism it must import its *method*, not its bytes. Adjacency is therefore by-design
complementary, not a route; "should be routed to owner" applies to nothing on this axis.

## Finding 2 — does any sibling replay TB2 graders? NO siblings do (info)

- Cross-lane literal grep `test_interp|schemelike|metacircular` over every lane, all file types,
  `.git` excluded: only 2 lines of CPython-changelog noise (`test_interprocess_signal`) at
  `kagi-shokunin/.ufo/waves/round-26/build/ClockS027-artifacts/chlog.body:18364` and a copy inside a
  kagi round-27 sandbox clone. **Zero** sibling replays a Terminal-Bench 2.0 grader.
- `https?://github.com/.*terminal[-_ ]?bench` over all lanes (.py/.sh/.md/.json): hits only in
  kengaku plus prose mentions in older kagi/kake connector notes. No sibling replay machinery.
- Third-party cross-check: `few-sh/terminal-wrench` (tasks/ → 331 dirs; 24K gz receipt
  `wrench-tasks.json`) publishes 14 of kengaku's ~88 captured grader members incl. this round's
  `schemelike-metacircular-eval` (`members-in-wrench.txt`), but only as agent-trajectory transcripts
  and hack postmortems — **not as a runnable grader/testOfflineReplay**. Kengaku's located-replay
  capability (`round93_scheme_probe.py`, 8×5 legs) is unmatched among the lanes surveyed; membership
  census receipt `kengaku-member-census-r52.lst` (89 rows incl. EXCLUDED.md) and `kengaku-members.txt`
  (88 with tests/test_outputs.py at HEAD) preserve what kengaku captured vs what wrench publishes.

## Finding 3 — upstream identity of the TB2 member and a deceptive mirror (minor)

- `harbor-framework/terminal-bench-2` (the repo S290 cites) is live (HTTP 200, default_branch=main).
- Deceptive mirror found: the **old** canonical repo `laude-institute/terminal-bench` now redirects
  (GitHub repo id 918420677) to `harbor-framework/terminal-bench-1`, whose `tasks/` directory has NO
  `schemelike-metacircular-eval` (404, probed under refs main/master/harbor/tb2/terminal-bench-2);
  that repo's last push is 2026-07-11. Any future source re-verification that hits the old raw URL
  (out of habitual use of `laude-institute/terminal-bench`) silently grades a *different repo* unless
  the lane's sha256 pin catches it. The lane's S290 pins by sha256 (`fbb84e3c…`), and this seat
  re-fetched the pinned path at S290's URL and sha256 **agreed** with the lane capture (receipt
  `upstream-404-receipts.txt` §A), so the round's C1 source is verified without ambiguity — the mirror
  is recorded here only as a route note for future SOURCES hygiene (write the full `harbor-framework/`
  path, never `laude-institute/`, in later rows). Severity minor because this round's C1 is *not*
  affected — the byte pin caught the risk.

## Finding 4 — one-shot scratch hygiene itself (info, no defect)

`/fast/scratch/hyaku/kengaku-r93/ConnectorOverlap/` was created and later removed via the required
exit trap; only content ever written there was derived from the frozen instruments and receipts that
are themselves committed at T. Nothing citable was ever stored only at /tmp. No incident to report —
the 2026-11-05 kake-r97 deletion incident (ConnectorScope-23 removing the wrong parent dir) did not
collide with this seat because the claim work this seat needed is byte-derivable from committed
receipts and was re-derived, not stored. Recomputed rather than cached is accepted evidence practice
per the round's scratch discipline; no route needed beyond what ConnectorScope-23 already files.

## Verification trail (read-only against the lane)

`git log -1 -- plans/round93_freeze_integrity.py` → `17cb9337 2026-11-05` (P1) only — **zero
post-freeze deformations on the gate itself** (digest identical to the frozen table's `18b01b42…` at
the lane working tree, re-verified). Adjacent-instrument dating: `adjacency-dates.txt` (combined
`git log -1` per file, all read-only). Fleet-root `MANIFEST.json` capability rows containing
"freeze"/"digest"/"instrument" inspected in-memory (no writes): the freeze-relevant past that this
ship compares against is the round-90/91/92 kengaku entries themselves (r92 verdict
`rejected-honest-stop` on the M8 lineage that R93-C2 answers); no sibling lane's manifest row claims
a `frozen-instruments` gate capability.

## Overlap summary table (for the L1)

| Q (from the brief) | Verdict | Weighting |
|---|---|---|
| Does any sibling own a frozen-instruments-vs-freeze gate? | **No.** Closest are souji's per-claim prereg `sha256=`+`FROZEN-EDITED` and mori pin-check's registry digest rows; neither reads a claims-table 9-row instrument list. All adjacencies are **complement**, none **duplicate**, none **route-away** | LOW duplication risk |
| Does any sibling replay TB2 graders? | **No.** Only kengaku does (11 executable member replays to date). | kengaku's uniqueness holds |
| Should R93-C2 be routed to a sibling? | No; protocol-of-boundary (PROTOCOL.md:411-416) even *forbids* cross-lane execution, so the freeze-integrity gate staying lane-local is the correct design | no absorption |

## Tooling authorization record

Zero tools installed or upgraded this seat (`uv`/`cargo`/`npm`/`pacman` channels untouched; nothing to
report under the 2026-10-19 operator rule). `curl`, `python3`, `git`, `gzip` (host stock) only.

## Finale

Verdicts above are exhaustive for the brief's four questions. No finding requires in-round repair;
the two minor routes (upstream mirror hygiene in Finding 3; a deprecation route for the r90/r91 pin
JSON ledgers in Finding 1 row 10, only if the L1 wants a *standing* tool beyond the r93 gate) belong
on round-94's list, not this round's.
