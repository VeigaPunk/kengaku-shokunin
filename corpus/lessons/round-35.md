# Round 35 — one TB2 grader read and executed; routed defects move into a ledger (2026-10-25, hyaku run 7)

Baseline `58a19f37312e1b22fd2a7957bdfc6bb7832aadd0`; frozen claims `plans/round-35-claims.md` (freeze
`11d64530179b78e33ba6074fc77d63d36ee7ac31`). Controls scored red before any repair or grader run:
`.ufo/waves/round-35/claims/control-*.txt`.

## Gate

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| `knowledge/tb2-protein-assembly-grader.md` (C1) | **Admitted** | Q1 triad lines 1–5; Q2 S105–S107 tier A for their own scope; Q3 22 located quotes, each re-checked by `plans/round35_c1_verify.py` V3 against the capture line; Q4 Negative space with a falsifier; Q5 maintainer task code labelled self-report beyond its own behaviour; Q6 extends `benchmark-verifier-execution-model.md` / `benchmark-grader-semantics.md` and the README §Frontier round-33 clause; Q7 entry, index row and coverage row land together. Round-34 critic findings fixed: bare pinned URLs without `/tasks/`, no unquoted S092/S100 assertions, evaluator files in the manifest. |
| S105 `tests/test_outputs.py` @ `2fd12b88` | **Admitted (mined)** | Opened 2026-10-25 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/tests/test_outputs.py`; quote, line 42: “assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx, (”; sha256 `44a05a24…96582`. |
| S106 `tests/test.sh` @ `2fd12b88` | **Admitted (mined)** | Opened 2026-10-25 at `…/protein-assembly/tests/test.sh`; quote, line 27: “echo 1 > /logs/verifier/reward.txt”; sha256 `9ede4664…267b5`. |
| S107 `instruction.md` @ `2fd12b88` | **Admitted (mined)** | Opened 2026-10-25 at `…/protein-assembly/instruction.md`; quote, line 29: “The GS linkers between different subproteins should be between 5 and 20 amino acids long.”; sha256 `1bb2af1d…003f7c5`. |
| Quarantine S091 (NEC 技報, RAKUDA caveat) | **Re-grounded, not appended** | The staged quote is present in `.ufo/waves/round-34/assimilation/captures/nec-s091-reopen.html` (tag-stripped; raw line 276). Round 34's "quote absent" reason was false (spot-check D5; erratum appended to `round-34.md`). Not appended: no admitted entry cites it (CORPUS rule 4). Flip: an admitted entry cites it. |
| Quarantine S105-staged (METI GENIAC archive) | **Not appended** | Quote located in round 34 (`R34CaptureGeniac.md`); no admitted entry cites it (CORPUS rule 4). Flip: an admitted entry cites a re-grounded row. |
| Package `toolathlon-grader-behaviour-probe-2026-10-23.md` (`merge/kengaku/`, grader-probe theme — the theme closest to C1) | **Refused** | Its only source, staged S130, is the campaign's own probe write-up (`lanes/kengaku/round6/toolathlon-grader-behaviour-probe.md` in shokuknow), not an opened primary and not a receipt this lane can re-run without the campaign tools §10 forbids. Flip: re-run an equivalent probe in-lane against Toolathlon `9be8d8fe` and cite the lane's own receipt (the `pinned-grader-probe` capability now exists). |
| Package `terminal-bench-release-identity.md` | **Refused** | Cites S100/S092, both already in the registry and already used by `benchmark-verifier-execution-model.md`; no coverage-map ground the lane does not hold (same reason as round 34, `R34ReconPackage.md`). Flip: a release-identity fact the lane's entries do not state, with a located quote. |
| Package `grader-predicate-input-types.md` (staged S143/S144) and the dated grader-fixture-probe amendment lineage | **Held (admit-candidates, not admitted)** | Wave-1 scout `R35ScoutMergePkg` re-ran the staged round-7 Toolathlon fixture probe from a `/tmp` source copy (16/16 rows, 0 textual differences; no write into shokuknow: `find … -newer build.ready` empty) and judged both admit-candidates as dated amendments. Not admitted here: round 35's claims were frozen before the screen and §10 forbids widening a frozen target. Flip: a round-36 claim that re-opens S143/S144 at their pins and lands the amendment under renumbered ids. |

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| false refusal reason (S091) | round 34 refused S091 as "quote absent" on the first 418-byte Access Denied fetch while its own `nec-s091-reopen.html` holds the quote (`corpus/lessons/round-34-verifier-spotcheck.md:64`, D5; re-verified live 2026-10-25, `.ufo/waves/round-35/build/R35ScoutQuarantine.md`) | CORPUS SOURCES rule 1 / §10 quarantine hand-check — it required locating the quote in the capture, which the round did not run on the reopen bytes | erratum appended to `round-34.md`; ledger row `R34-D5` (red at freeze, `claims/control-c2-nothing.txt`); post-hoc `plans/round35_hardening.py` H5 fails on a "not present" erratum and on an altered capture (`corpus/evidence/round35/hardening-counterexamples.txt` CE3, CE4) |
| committed recursive scratch mirrors | round 34 committed 106,323 blobs (1650.6 MiB logical) under `mut-entries-scratch/` plus 3,090 under `build/R34MutRegistry/{mirror,mut}/` (`round-34-verifier-spotcheck.md:31`, D2) | none — the lane helper commits a named directory whole and the wave context did not forbid in-lane mirrors | mirror roots deleted at the tip (history keeps them; no rewrite); ledger row `R34-D2` (red at freeze: `committed_mirror_paths=109413`); round-35 wave contexts require `mktemp` clones outside the lane; Q23 records the rule |
| receipt claims an unbacked manifest | `R34CaptureTB2Eval.md` said the evaluator hashes were in `SHA256SUMS`; they were not (D3) | Q22 (a receipt is evidence only if it re-runs) — not run on the capture report | two digest lines appended; ledger row `R34-D3` (red at freeze) |
| frozen counters too weak for their own skip-control (this round) | wave-1 critic `R35CritControls` built a junk package (stub probe, eight one-word `import` quotes, `junk` teaches cells) that the frozen C1 counter scores `checks=6 defects=0`; `R35CritC2` passed D4/D5 with labelled-but-false lines; `R35MutC1Quotes` M4 and `R35MutC1V4V5` M8 survive | addendum §9 ("build the cheapest control that skips the claimed work, score it with the frozen counter") — the L1's pre-freeze skip-control re-dressed a round-34 draft instead of attempting an adversarial junk package | post-hoc `plans/round35_hardening.py` (H1 frozen instruments byte-equal to the freeze, H2 distinct ≥3-word quotes and no unparsed rows, H3 teaches ≥8 words, H4/H5 directional clauses + pinned capture), shown able to fail on all five counterexamples; it is NOT either claim's rule — the frozen predicates stay as declared and the report says what each counter does not prove |
| probe case label confounded | `donor-repeated` fails on the 3000-nt cap, and the instruction's repeat rule is stated for the antibody binder (`R35RevProbePred` F1) | wave-1 reviewer | the entry states the confound and lists the three instruction bullets no case exercises; the frozen case table is unchanged |

## Assimilation record

considerthese: `considerthese/2026-10-25.md` §Self-improvement suggestions 2 (persistent routed-defect ledger) implemented as C2 — parts (a) re-run every row at every tip and the mismatch count are implemented; (b) recurrence blocking is recorded (`recurrence_of`) but not enforced; (c) the tip-receipt validator is not built. Q23 states the limits. `merge/kengaku/`: see Gate rows; no package row is appended (no admitted entry cites one). §10 id-collision check: `.ufo/waves/round-35/assimilation/` (21 collisions, all staged ids S077–S104 overlap the live registry; guard proven on an indented `  | S002 |` fixture — `build/R35IdGuard.md`); quarantine slice re-derived: 2 rows (S091, S105-staged).

## Census

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`.
Before (freeze): 15 W04, `kengaku ok`, exit 0 (`corpus/evidence/round35/census-before.txt`). After: 15 W04,
`kengaku ok`, exit 0 (`corpus/evidence/round35/census-after.txt`; output identical apart from no new
warning). Registry rows 97 → 100 (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`);
added by tier A/B/C = 3/0/0 (S105, S106, S107, all `mined`); rows touched old→new: none (no existing row's
status/recheck/used-by changed); frontier rows advanced: 1 (README §Frontier task-spec item, "Terminal-Bench
2.0's" scoring-code clause, for `protein-assembly` only).
