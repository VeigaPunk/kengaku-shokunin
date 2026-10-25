# R31FxTrends — trend-verdict falsification (round 31, wave 2)

Seat: `R31FxTrends` (critic, leaf). Target: the round's trend verdicts **before** the report states
them — for expansion, quality and discernment, what evidence would make each `improved`, what would
make it `harmed`, checked against the round's landed bytes. Graded tree: lane commit
`dbb07364` (round-31 landing). All counters re-run: (a) live lane, (b) pristine `git archive`
checkout of `dbb07364`, (c) separate sandboxed fleet root so the census runs on the committed tree.

---

## 1. Reproduced counters (commands, paths, exits)

| claim | command | result at `dbb07364` | control |
|---|---|---|---|
| C1 | `python3 plans/adoption_check.py --expect .ufo/waves/round-31/adoption-expect.json --census` (in a checkout named `kengaku-shokunin` under a replica fleet root) | `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok`, exit 0 | baseline `0883e72` checkout: `entries=0 …`, exit 1 (`plans/round-31-claims.md` §C1; committed `claims/control-nothing.txt`) |
| C1 | `python3 plans/round31_c1_verify.py --lane .` | `checks=6 defects=0`, exit 0; selftest `checks=6 failed=0` | — |
| C2 | `python3 plans/round31_defects.py --lane .` | `checks=10 defects=0`, exit 0 | baseline `0883e72` checkout: `checks=10 defects=10`, exit 1, messages ≈ committed `claims/defects-before.txt` |
| C3 | `python3 plans/sources_adopt.py --selftest` | `SELFTEST cases=17 failed=0`, exit 0 | baseline `plans/sources_adopt.py`: `cases=14`, `--url-map` → argparse exit 2 (committed `claims/gate-before.txt`) |
| C3 CLI | fresh fixtures: map-ok / map-bad / unmapped / no-map / `--url-map` alone | exit 0 / **8** / **9** / 0 / 2 — matches committed `evidence/round31/gate-cli-exits.txt` | — |

Census detail: `scripts/sources-census.sh validate --root <fleet> kengaku` on the pristine-HEAD sandbox
prints exactly the 15 `W04` + `ok`, exit 0; the 15th is `S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes` (S100↔S079, disclosed in the S100 row: "that is S079, the same repository read for its authored fields"). Baseline sandbox prints the 14 `W04` of `claims/census-before.txt`.

---

## 2. Axis 1 — Expansion: what would earn `improved`, what would show `harmed`

**C1 coverage — verdict cell "7 → 7 held — improved (counts)"; coverage *surfaces* did not move.**

- *Earns improved:* new corpus bytes on ground the coverage map held open — the round-29 frontier
  clause "their scoring code was not read and stays open" (README.md) — plus a registry delta whose
  rows are at their pins, an index row, a coverage row and a frontier bullet all present, and the
  frozen counter green. Checked: entry exists at HEAD with three distinct `source:` lines, `verified-at: 2026-10-25`, `writer: KengakuR31`; S092/S093/S100 present, `status=mined`, `opened=2026-10-25`, `used-by` names the entry (`rows_mined=3 usedby_ok=1`); README gained index row (line 66), coverage row (line 253) and the "Partly discharged round 31" frontier sub-bullet (line 276), while the original bullets stay byte-identical.
- *Would harm:* the code reading being wrong at a pin, a registry anchor not locating at the pinned
  revision, a zero-count/targeted gate, or a sweep count that does not hold. Checked the entry's
  locators against the capture files (`.ufo/waves/round-31/assimilation/captures/`):
  `verifier_mode.py:31` `or VerifierEnvironmentMode.SHARED` ✓; `:24-25` SEPARATE inference ✓;
  `config.py:588` default None ✓, `:590-593` description (13 words) ✓; `verifier.py:128` comment ✓,
  `:168` docstring ✓, `:207` reward removal ✓, `:209` guard ✓, `:220-223` upload ✓;
  `test.sh:33`, `:71`, `:38`, `:43-44` ✓; `parser.py:68`, `:71`, `:88-90`, `:121` last-write-wins ✓.
  The 731-manifest sweep (89 TB2 + 642 SWE; 0/731 setting `environment_mode` or
  `[verifier.environment]`; 88/89 TB2 `tests/test.sh` reset-less) and `trial.py:1064`
  (`skip_tests_upload=definition.bundled_tests`) are on the record in committed seats
  (`build/R31DraftEntry.md`, `build/R31SrcS092{b,c}.md`); the six-manifest self-sample is honestly
  labelled as such in the entry (§"What this does not establish").
- *Improvement is earned.* Two small quality dents (below), no unearned claim.

**C2 calibration — verdict cell "8 → 8 held".**

- *Earns held:* ten routed items closed with byte-level repair evidence, before-state reproducible,
  R9 committed-blob test real. Checked: `LOG.md:792` superseded "two new fields, one new value set"
  + appended named correction (append-only diff against `0883e72` shows additions only);
  `corpus/lessons/round-30.md` §Errata Q6 basis / Q2 tier cell / round-shape 33; card holds the
  'reconciled truth' sentence exactly once (`:129`); falsifier clause once (`:140`); CC0 adjective
  gone (0 hits); five round-30 seat reports committed and clean at HEAD; R9's anti-revert
  (`HEAD:R30DraftGate.md` "Pass 9") gate present.
- *Would harm:* a vacuous or patchable counter. The mutation seat
  (`build/R31MutCounter.md`) documents survivors m3/m4/m5 — weakened R6/R9 checks read clean — and
  the m6 exit-only kill; that is a strength limit, disclosed in the seat. The *hidden harm* is the
  disclosure chain, not the closure: the scorecard cell says the four counter corrections are
  disclosed "in `corpus/lessons/round-31.md` §Mistakes", **and that file does not exist at
  `dbb07364`** (`git cat-file -e HEAD:corpus/lessons/round-31.md` fails; it is untracked in the
  live tree). The landed report points at a file the landing does not contain.
- Verdict: 8→8 held survives at HEAD; the disclosure pointer is broken.

**C3 operability — verdict cell "8 → 8 held" + capability row.**

- *Earns held:* the gate now refuses a located quote whose artifact is not the cited document, with
  distinct exits, proven failure-capable. Checked: selftest 17/0 at HEAD; CLI exits 0/8/9/2
  reproduced above; committed `gate-binding-neutered.txt` shows the binder removed → `failed=2`,
  exit 1 — the tally cannot be the load-bearing claim, and it is not presented as such.
- *Would harm:* a binding that is not applied to real rows, or a mismatch silently accepted. Not
  observed at HEAD. Note: the working tree carries further gate improvements (receipt prints
  `bound=<artifact>-><url>`, map name, unreadable-quote-file guard) that are *not* in the landed
  commit — the committed gate is functional and self-consistent with the committed evidence; the
  auditable-receipt version is post-landing.

---

## 3. Axis 2 — Quality: precision of the landed bytes

1. **Entry prose locators, off by a few lines** (substance correct): the entry cites
   `verifier_mode.py:22-23` for "Returns the explicit mode when set" — the phrase sits at `:18`
   (lines 22-23 are the `environment_mode` branch it describes) — and `:35-38` for the multi-step
   precedence docstring, which sits at `:39-40`. The *registry anchors* are exact (`verifier_mode.py:31`,
   `verifier.py:168`, `config.py:590-592`); only prose pointers are off.
2. **Scorecard index count:** the C1 cell says "knowledge 39 → 40; index 40 → 40". Measured:
   README index rows 39 at `0883e72` → 40 at HEAD (knowledge files 39 → 40). The correct delta is
   39 → 40; "40 → 40" is a factual error in the verdict row (it understates the ledger delta, so it
   hides nothing, but it is wrong).
3. **S100 tree shape (92 roots, 89 dirs) and the 301-redirect claim:** not independently
   reproducible from this host (GitHub API 403 at check time); they rest on the committed seat bytes
   of `build/R31DraftEntry.md` (1,446 recursive entries, 92 roots, 89 task dirs). Internal
   consistency of the counts (89/642 manifests, 88/89 reset-less scripts) checks out against the
   entry's own table.

---

## 4. Axis 3 — Discernment: where `improved` would be unearned, where `harmed` is hidden

- **Unearned-improved points checked and cleared:** C1's entry would not earn `improved` if the
  frontier clause were discharged without substance (it is discharged only for verifier execution,
  and the entry says so), if a pin were wrong (all pinned locators resolve), or if the sweep were a
  fabrication (seat bytes carry the API evidence and the honest 643rd-toml correction).
- **Hidden harm found:**
  1. `SCORECARD.md` cites `corpus/lessons/round-31.md` §Mistakes for the four counter-correction
     disclosures — absent at `dbb07364` (untracked).
  2. The live working tree at check time differs from the landing in files the same claims cite:
     `plans/sources_adopt.py` (receipt/auditability), `evidence/round31/gate-cli-exits.txt` and
     `gate-selftest-after.txt` (regenerated in the new format), `corpus/SOURCES.md` S092/S100 row
     cells, `corpus/QUALITY.md` (+Q21), untracked `build/R31DraftGate.md`,
     `.ufo/waves/round-31/assimilation/captures/`, `corpus/lessons/round-31.md`. If the final
     report quotes the working-tree bytes, it grades beyond `dbb07364`; at HEAD the originals are
     self-consistent and pass, so the landing itself is not broken — the report must pin the commit
     it grades.
  3. Operational reproducibility: the census subprocess derives the lane id from the directory name;
     run outside the canonical path it prints `census=fail` even on a clean tree (reproduced), so
     the frozen counter is only reproducible from the canonical lane directory or an equivalent
     sandbox.

---

## VERDICT

- **C1 coverage "7 → 7 held — improved (counts)": SURVIVED** — improvement earned at `dbb07364`;
  quality dents: two prose locators off by a few lines, and the verdict cell's "index 40 → 40"
  should read 39 → 40.
- **C2 calibration "8 → 8 held": SURVIVED** — closure real and byte-verifiable at HEAD; hidden harm:
  the scorecard's disclosure pointer `corpus/lessons/round-31.md` is *not in the landed commit*
  (untracked). Mutation-strength survivors (m3/m4/m5, weakened R6/R9 checks) are documented in the
  seat but do not reach the landed report.
- **C3 operability "8 → 8 held": SURVIVED** — binding reproduced end-to-end at HEAD (0/8/9/2),
  failure-capability on the record; no hidden harm in the committed gate; the receipt-auditability
  version exists only in the uncommitted tree.

**Smallest safe corrections:** (1) fix the two entry locators (`verifier_mode.py:18`, `:39-40`);
(2) fix the scorecard index figure to 39 → 40; (3) land `corpus/lessons/round-31.md` (and the
updated `R31MutCounter.md`) before any report cites them, and state the exact graded commit hash in
the final report.
