# FxDefectsCounter — C2 counter attack (round 32, 2026-10-25)

Seat: `L1Kengaku32.FxDefectsCounter` (critic / leaf). Target: `plans/round32_defects.py` on the
current (pre-repair) repo. Claims freeze: `plans/round-32-claims.md` (commit `0d32691d`), C2 predicate
"`python3 plans/round32_defects.py --lane .` prints `defects=7` and exits 1 on the pre-repair tree".

## 1. Run results — two trees, two counts

| run | tree | result |
|---|---|---|
| `python3 plans/round32_defects.py --lane .` | **working tree** (current disk; lane's draft state) | `checks=7 defects=5`, exit **1** |
| `python3 … --lane /tmp/r32f-FxDefectsCounter/committed` | **committed tree** (`git archive HEAD`, HEAD = `6084cd3`, freeze state) | `checks=7 defects=7`, exit **1** |
| `python3 plans/round32_defects.py --selftest` | working copy | 9/9 `PASS`, `SELFTEST checks=7 failed=0`, exit 0 |

The committed-tree run reproduces the freeze control `.ufo/waves/round-32/claims/defects-before.txt`
**byte-for-byte** (same seven `DEFECT` lines, `checks=7 defects=7`, `exit=1`). The working-tree run prints
5 because **R3 and R4 are already repaired on disk as uncommitted drafts** (see §3) — not because a check
is broken. The instruction "verify it prints defects=7" holds only against the *committed* pre-repair
tree; the working directory is no longer pre-repair.

## 2. R1–R7 reasons vs the round-31 spot-check items

All seven reasons match round-31 spot-check `corpus/lessons/round-31-verifier-spotcheck.md` §5 items
D1–D6 plus the report item-5 erratum debt, and each names real pre-repair evidence:

| check | defect line (committed tree) | spot-check item | evidence (bytes I read) |
|---|---|---|---|
| R1 | `no appended erratum supersedes the a44b5a8 citation` | D1 phantom hash | `.ufo/reports/round-31/kengaku.md:226` cites "`a44b5a8`-class commits"; `git -C <fleet> cat-file -t a44b5a8` → `fatal: Not a valid object name` (RC 128); no `ae95fe0`/`superseded` anywhere in the report (grep: only line 226 hits) |
| R2 | `…round-32/kengaku.md does not exist yet` | D2 report ordering recurred | fleet `.ufo/reports/round-32/` listing contains no `kengaku.md` (only chousa/kaidoku/kake/kama/kotodama/kumitate/mado/mori/tameshi/tsukuroi) |
| R3 | `the tip receipt still contains 'can't open file' failure lines` | D3 broken receipt at tip | `git show HEAD:corpus/evidence/round31/gate-cli-exits.txt` lines 5–8: `can't open file …../../../plans/sources_adopt.py` + `exit=2` |
| R4 | `SKILL.md has no sources_adopt.py row` | D4 gate registry row missing | `git show HEAD:SKILL.md | grep -c sources_adopt` → `0` |
| R5 | `corpus/lessons/round-32.md does not exist yet` | D5 unreported falsify seat `R31FxEntryBar` | `ls corpus/lessons/` → no `round-32.md` |
| R6 | `no appended correction updates verifier_mode.py's precedence locator to :39-40` | D6 correction sweep misses | `corpus/lessons/round-31.md:57` still cites precedence docstring `(:35-38)`; `round-30.md:197` erratum still points Q6 retraction at `:78-81`; no `:39-40`, no `:72`/`82-83` correction note in either lesson |
| R7 | `no appended erratum records S086 as published without peer review` | carried debt (report item 5) | `corpus/lessons/round-30.md:66` groups "S081/S082 preprints vs S083/S086 peer-reviewed"; no `without peer review`/`not peer-reviewed` erratum for S086 |

All seven are genuinely red on the committed pre-repair tree for their own reasons. (Independently:
`ae95fe0` **is** a valid lane commit — `git cat-file -t ae95fe0` → `commit` — so the R1 repair anchor is
real, it is just not yet named in the append-only report.)

## 3. Green-before-repairs flag (overcooked check?)

No check is green on the committed pre-repair tree — none is overcooked *there*. But the working tree
(what `--lane .` sees right now) already carries two repairs as uncommitted drafts:

- **R3 green**: `corpus/evidence/round31/gate-cli-exits.txt` is modified on disk (M) — header
  "regenerated round 32 from the committed fixtures", `../../../../plans/sources_adopt.py` in the run
  line, `exit=0/8/9/2` tokens present, no `can't open file`.
- **R4 green**: `SKILL.md` is modified (M) — row `sources-adopt` (line 573) sits under `## Gate/probe
  registry (PROTOCOL §Gate standard)` (line 560).

So the before-state is already two-sevenths repaired in the working directory. This is not a false green
(the edits look like the genuine D3/D4 fixes), but it means the C2 before-measurement must be run on the
committed tree (as the freeze control was); a judge running `--lane .` now would see `defects=5` and
mismatch the frozen predicate. Flag for the lane: land or isolate the drafts before any before/after
comparison.

## 4. Gameability — wrong-but-plausible repairs each check would pass (survivors)

Read from the check source (`plans/round32_defects.py:72-191`); all seven are string/presence checks,
none executes or cross-validates content. Survivors, strongest first:

- **R3 (strongest)** — no execution proof. A hand-crafted receipt with `exit=0/8/9/2` lines and the
  literal `../../../../plans/sources_adopt.py`, minus any failure line, passes without ever running
  `sources_adopt.py` from the committed fixtures. Indistinguishable from a genuine regeneration; the D3
  "self-contained" trap recurs.
- **R4** — no row-structure parse. The heading regex accepts any heading containing `gate|probe|registry`;
  a prose mention of `plans/sources_adopt.py` under an existing §Gate-style heading passes even if no
  registry row is added. Also passes if the row is added under the wrong but similarly-named section.
- **R1** — string-only. `ae95fe0` must appear *anywhere* in the report text (unverified as an object),
  and `superseded`/`erratum` within 300 chars of `a44b5a8`. A negative or unrelated sentence
  ("…is not superseded…", or an erratum about a different topic naming `ae95fe0` in a footnote) passes;
  the erratum need not name the real locator-fix commit for the phantom.
- **R6** — the claimed locators are never validated against the actual files. An appended note putting
  `:39-40` (or `:72`/`82-83`) near `correction`/`superseded` passes even if the numbers are stale/wrong
  relative to the real current lines; the label can ride on a different sentence within the 300-char
  window.
- **R7** — 250-char proximity windows. An erratum mentioning S086 in one paragraph and "without peer
  review" later in the same window passes; it can mis-target S083 and still pass if S086 occurs in the
  labeled paragraph; the registry cell is never read to confirm the claim.
- **R5** — `R31FxEntryBar` within 160 chars of `dead` anywhere in the round-32 lesson, not necessarily in
  the seat ledger, and never checked against the falsify registry (a seat recorded dead while its report
  later lands still passes).
- **R2 (weakest)** — presence-only for the tip hex in the round-32 report; a stub report containing the
  tip string passes. Its ordering half is transitively enforced (any post-report commit flips the tip and
  re-reddens it), which is the one genuinely binding part of the instrument.

**Bottom line for the lane:** the counter is calibrated on the committed pre-repair tree (defects=7,
exit 1, reasons named), but none of R1–R7 is self-proving — R3/R4 are the weakest and should be backed by
the receipts/rows they claim, and R1/R6/R7 by byte-level review of the actual appended notes.

## VERDICT: pre-repair-red
