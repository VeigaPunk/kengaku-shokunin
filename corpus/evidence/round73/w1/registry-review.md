# R73 w1 — source review of the two frozen instruments (seat RegistryReviewerR73, reviewer)

Scope: read the two instruments' source against PROTOCOL.md §Gate standard and the frozen
sentences in `plans/round-73-claims.md` (original sections + appended A1/A2 + E-R73-1), per the
w1 reviewer item. I did NOT run their batteries or verdict modes (the replay seat owns runs);
all numeric claims below are static derivations using the instruments' own pure functions
(`collect`, `parse_rows`, `price_row`, `check_errata`) over the landing-tree bytes
(HEAD = `ea41880f`, worktree clean for both `.py` files; only `plans/round-73-claims.md` is
modified in the worktree). No LSP device exists in this seat's tool inventory; all
caller/definition checks are text-level (grep + read).

## Provenance (read-only git; no mutation)

- Base `d96c3e62`: gate has NO `--universe` flag (single `universe` hit is a comment, line 24 of
  that blob). The R73 amendment existed pre-freeze only as uncommitted worktree bytes.
- Freeze `255c261d`: contains the PRE-A1 gate (0 occurrences of `plans_seen` in that blob) and
  the audit (audit blob unchanged since: `git log -- plans/round73_c2_registry_audit.py` names
  only 255c261d; porcelain clean).
- Landing `ea41880f` (= HEAD): A1-amended gate (`plans_seen` arm, verdict() L134-163) + the 8 new
  registry rows; commit message itself reports "113 advertised, 0 missing" and "114 derived".
- Claims file at review time: HEAD copy already contains A1/A2 (`grep -c` = 2); the worktree adds
  an UNCOMMITTED `## Erratum E-R73-1` (verified via `git diff -- plans/round-73-claims.md`).
  E-R73-1 corrects the A1/A2 heading times (both amendments are inside `ea41880f`, committer
  2026-11-03T23:48:24-03:00 = 02:48:24Z, not 02:54Z/02:56Z) and non-admits both original claims.

## Static derivations (instruments' own functions over landing bytes; probe rc=0)

| quantity | value |
|---|---|
| FULL advertised | 113 |
| plans_seen / plans_only | 82 / 0 |
| legacy advertised | 113 (the plans/ leg adds 0 instruments to the advertised SET) |
| gate five legs at landing bytes | missing=0 incomplete=0 entry_missing=0 unbacked=0 duplicate=0 |
| audit rows / distinct entry scripts | 114 / 114, `rows==scripts` true, no shared entry script |
| corrected rows priced | `sources-adopt` kind=gate verdict has `failed` → 0 defects; `round62-c1-class-survey` kind=gate → 0 defects |
| errata block | heading present, both labels + both hashes present, `check_errata` = [] |
| registry block pipe-lines | 116 = header + separator + 114 rows; nothing silently skipped by `parse_rows` |

Cross-check against the L1 receipt `corpus/evidence/round73/a1-red-green.txt`: frozen gate on the
landing tree prints `plans_only=0`, all five legs 0, `PREDICATE R52-C2 pass`, `PREDICATE R73-C1
fail`, rc=1; amended gate prints `plans_seen=82`, pass, rc=0. This matches my structural proof in
C1-Finding 1 below, and also shows `REGISTERED rows=115` (gate counts the header as a row; audit
says 114) — the header-phantom asymmetry is live in committed output.

---

# Instrument 1 — `plans/round52_c2_registry.py`

Line numbers refer to the A1 bytes at `ea41880f` (= worktree). Pre-A1 quotes are from the
`255c261d` blob (`git show 255c261d:plans/round52_c2_registry.py`).

## 1. Verdict: codes, declarations, reality of `2`

Codes the main paths can return: `0` (only when `r73` true, L163), `1` (otherwise, L163; also any
uncaught exception exits 1 via the interpreter — a crash is classed `failed`, not
could-not-evaluate), `2` (setup: `SETUP no SKILL.md under <lane>`, L242-244; argparse usage, L236-239).
The registry row (SKILL.md:663) declares all three: `0` `PREDICATE R52-C2 pass` … · `1` fail,
each defect on its own line … · `2` setup: `SETUP no SKILL.md under <lane>` (measured with
`--lane /nonexistent`); argparse usage also exits 2. `2` is a real setup path (verified by code;
the row records a measurement). Per §Gate the undeclared-crash case is the only mapping gap.

**C1-Finding 1 (medium — verdict-map drift, row vs amended code).** The row keys `0` to
"PREDICATE R52-C2 pass" and `1` to "fail, each defect on its own line … then PREDICATE R52-C2
fail". The amended code's rc rule is `return 0 if r73 else 1` (L163) where
`r73 = ok and universe == "full" and len(plans_seen) >= 1` (L161). A legacy run that is green on
all five legs therefore PRINTS `PREDICATE R52-C2 pass` and EXITS 1 with no defect lines. Static
derivation at the landing bytes: legacy advertised = 113 with all five legs 0 — i.e. at the
landing tip `--universe legacy` is exactly this case. The row's `1` description ("each defect on
its own line") is falsified by the code's own rc rule post-landing. What it lets through: a
reader keying exit classes off the row misclasses a green legacy control run as `failed` (the
frozen control at the BASE tip is genuinely red — 110/5/rc 1 — so the committed control receipt
does not exercise this).

**C1-Finding 2 (headline — the freeze-commit gate could never print the frozen sentence).**
The freeze bytes gate the extra arm on `plans_only`: `r73 = ok and universe == "full" and
len(plans_only) >= 1` (255c261d blob, verdict() tail). Structurally unsatisfiable whenever `ok`
holds: `plans_only` = advertised instruments whose ad-files are ALL under `plans/`; every
registered instrument is advertised by its own SKILL.md entry cell (SKILL.md is in SELF_FILES,
L41, and CMD matches entry cells, L36), so plans_only ∩ registered = ∅, hence
plans_only ⊆ missing, and ok ⇒ missing = ∅ ⇒ plans_only = ∅ ⇒ r73 false ⇒ rc 1. The frozen
sentence demands `PREDICATE R73-C1 pass` and rc 0, so sentence and frozen code were contradictory
at freeze. The L1's receipt `a1-red-green.txt` demonstrates it by run (all legs 0, fail, rc=1);
my proof needs no run. A1 (comment L158-160, arm L161) is the minimal repair and the original
frozen SENTENCE (which never names plans_only) is satisfiable under the amended bytes — and holds
at the landing bytes (static: legs 0, plans_seen=82 ≥ 1).

**C1-Finding 3 (low — advertised-but-absent scripts leave the universe).** L111
`adv = {p: v for p, v in adv.items() if (lane / p).exists()}`: a script named by a claims doc but
absent from the tree is dropped from the advertised universe, so neither MISSING nor
ENTRY-MISSING can fire for it. Counter-example: `plans/round-73-claims.md` names
`python3 plans/ghost.py`, `ghost.py` deleted, no registry row → all five legs 0 and (with any
plans_seen survivor) rc 0. What it lets through: a row and its script deleted together disappear
from every leg; the coverage duty evaporates for vanished instruments. (Defensible under the
docstring's own "lane-owned script" definition — reported as a declared-definition blind spot.)

**C1-Finding 4 (low — malformed rows are invisible to this gate).** L72 `if len(cells) != 8:
continue`: a 9- or 7-cell row is silently skipped; this gate has no `columns` leg (the audit
prices `columns`, `price_row` L121-130 — the gate does not). A malformed row of an advertised
instrument surfaces only indirectly as MISSING (its row is effectively gone); a malformed row of
an unadvertised instrument surfaces as nothing.

**C1-Finding 5 (low, declared — header counted as a registry row).** parse_rows (L68-77) skips
separator lines (L74) but has no `cells[0] == "name"` skip, so the 8-cell header is priced as a
phantom row: `REGISTERED … rows=` is one above the audit's count (receipt shows 115 vs 114). The
row itself documents this ("`rows` counts the header line … so it exceeds `REGISTERED`"). Inert
today; a future blank header cell would raise a phantom INCOMPLETE.

**C1-Finding 6 (low — three self-test-cell escapes).** (a) Negation regex L91
`\bno\b.{0,24}--[a-z][a-z0-9-]*` suppresses the ENTIRE cell check when one flag is negated:
"runs `--selftest`; no `--mutants` support" is never unbacked even if `--selftest` is absent
from the script. (b) L95 `if len(scripts) != 1 or not flags: return False`: a cell naming two
scripts is never unbacked regardless of backing. (c) L101 `return all(f not in body for f in
flags)`: substring-in-bytes backing — a docstring saying "does not accept --selftest" BACKS a
`--selftest` claim. What it lets through: SELFTEST-UNBACKED stays 0 for cells using any of the
three shapes.

**C1-Finding 7 (low — silent universe narrowing).** L55 `[f for f in files if f.exists()]`:
a missing SCORECARD.md/LOG.md/corpus/README.md is skipped without SETUP; deleting an ad file
shrinks the advertised universe with no defect line.

**C1-Finding 8 (low, declared — CMD narrower than the claims' stated universe).** L36
`[A-Za-z0-9_]+` excludes hyphens/dots: the claims doc defines the universe as "a claims document
naming `python3 plans/<instrument>.py`", but `python3 plans/my-tool.py` would not be advertised.
No live gap (every `plans/*.py` is underscore-named); the row declares the `[A-Za-z0-9_]` limit.

**C1-Finding 9 (low — selftest coupled to lane state).** main() checks
`(lane / "SKILL.md").exists()` before dispatching `--selftest` (L242-245), so the fixture battery
is unreachable on a lane whose SKILL.md is missing/renamed, although the battery is
lane-independent by construction (temp trees only).

## 2. Self-test

Four arms over temp trees (L166-232): clean-green; dropped row → MISSING; blank cell →
INCOMPLETE; plans-doc-only instrument MISSING under `full` and invisible under `legacy`. No arm
is vacuous — each red-condition is checked positively (e.g. L184 `"plans/tool_a.py" not in
missing → FAIL`; the plans arm checks both directions, L216-222). BUT the arms call `collect()`
in-process: NO exit code is asserted anywhere and no PREDICATE line is exercised; finding
identity is membership of a path string (stable, but only for MISSING/INCOMPLETE). ENTRY-MISSING
and SELFTEST-UNBACKED have no arm at all — the row declares this limit ("no fixture exercises
ENTRY-MISSING or SELFTEST-UNBACKED"). §Gate's self-test clause ("asserting both the exit code and
a stable expected finding-id") is therefore only partially met. The printed tally
`SELFTEST cases=4 failures={fails}` (L231) matches the frozen sentence exactly.

## 3. Silent pass — see C1-Findings 3, 4, 6, 7 (each names line + counter-example).

## 4. Drift — frozen sentences vs printed strings

Present and format-exact in the current bytes: `UNIVERSE mode={universe} files=… plans_seen=…
plans_only=…` (L137-138; contains the frozen `UNIVERSE mode=full` prefix), `ADVERTISED
total={n}` (L139), `MISSING {n}` (L142), `INCOMPLETE {n}` (L145), `ENTRY-MISSING {n}` (L148),
`SELFTEST-UNBACKED {n}` (L151), `DUPLICATE {n}` (L154), `PREDICATE R52-C2 pass|fail` (L157),
`PREDICATE R73-C1 pass|fail` (L162), `SELFTEST cases=4 failures={n}` (L231). No drift between
sentence and print. Amendment-text drift (claims file, not code): A1's parenthetical restates the
After-target as `ADVERTISED total=113>=111` while asserting "the target … unchanged"; the
original After section (kept verbatim above it) says `total=112`. The binding inequality `>=111`
is unchanged; the instantiation silently moved 112→113. Substantively: the original claim's "2
instruments enter the universe through the plans/ leg" is FALSE at the landing bytes — the
plans/ leg adds 0 instruments to the advertised set (legacy = full = 113); the widening survives
only as the `plans_seen` print, not as coverage pressure. Neither A1 nor E-R73-1 states this.

## 5. Two evidences

None in code: no committed input snapshot, no digests, no expected-verdict constants (the only
frozen constants are the regexes/leg names). The row's pinned-values cell cites a base-tip
receipt path (pointer, not a digest-pinned baseline) and the row's verdict map embeds historical
measured values at named tips. No run prints the revision it measured (§Gate: "A verdict names
the revision it was measured against" — unmet; the a1-red-green receipt compensates with an
explicit TREE line).

---

# Instrument 2 — `plans/round73_c2_registry_audit.py`

Unchanged since freeze 255c261d. Line numbers = worktree = freeze blob.

## 1. Verdict: codes, declarations, reality of `2`

`0` iff total defects 0 (L220), `1` otherwise (L220; uncaught exception also exits 1 — crash
classes as `failed`), `2` on: no SKILL.md (L413), `--selftest/--mutants` without `--work`
(L417-419), `--work` not an existing directory (L285-287, L351-353), battery fixture not red
(L365-368). The row (SKILL.md:706) declares `2` = "no SKILL.md, or `--work` absent for the
fixture/mutant modes". The not-a-directory and battery-not-red triggers are undeclared SUB-CASES
of the declared class — the code→class mapping §Gate requires holds. `2` is real (four distinct
triggers). Verdict map otherwise accurate: `1` = "any `DEFECT` line … or `MISMATCH` > 0" matches
L214-218.

**C2-Finding 1 (high — destructive `--work`).** Both fixture modes end with
`finally: shutil.rmtree(work, ignore_errors=True)` (L327, L397): the ENTIRE `--work` directory
the operator named is deleted, not only the fixtures the run created. `--selftest --work .` from
the lane root would recursively delete the lane; `--work <shared scratch>` destroys any sibling
content. This contradicts the row's write scope ("read-only; fixtures under `--work`") and §Gate
scope ("read-only over surfaces it does not own"). It lets nothing through in the predicate; it
is a destructive side channel on a plausible flag value, and the claims doc instructs every seat
to pass a `--work DIR`.

**C2-Finding 2 (medium — arm 2 is vacuous for its own leg).** The second-row arm's assertion
(L310) `if not d3 and not any("kind" in x …)` passes when ANY defect fired — in the fixture the
`kind=census gate` defect always fires, so a regression that kills D3's duplicate detection
entirely (`duplicate = []`, cf. mutant M4) leaves this arm green, `SELFTEST arms=4 red=3 ok=True`
still prints, and the frozen selftest clause stays satisfied while D3 has lost its selftest
guard (M4 would then be the only guard, and M4 itself would survive, rc 1 — the mutant battery
saves the claim, the selftest does not). Arm 1 asserts only `if d == 0` (L301): any defect from
any leg satisfies it — no finding-id pinned ("must red exactly its leg" per its own docstring,
L278-279, is not enforced). Arm 3 pins the D4 leg (L317) but not the defect id. Clean arm pins
all-legs-zero (L296-299). No arm asserts an exit code (all in-process `run_checks`).

**C2-Finding 3 (medium — the quoted tally is decorative).** L324:
`print(f"SELFTEST arms=4 red=3 ok={ok}")` — `arms=4` and `red=3` are string literals, not
computed. On any arm failure the line still prints `red=3` while fewer arms actually red'd (and
`fails` is not echoed). The exact string the frozen sentence requires (`SELFTEST arms=4 red=3
ok=True`) is produced by construction whenever ok=True, so the target cannot miss it — but the
printed evidence does not measure what it appears to measure.

**C2-Finding 4 (medium — D4 verifies presence, not pairing).** `owners` = items containing the
label (L187); pass condition `revision not in items[owners[0]]` (L190). The LIVE round-71
erratum item 1 contains BOTH revisions ("is false of `d8a77d3f`" AND "landed with `c80fcdb3`"),
so item 1 passes for EITHER pinned revision — the check cannot distinguish a correct binding
from a mis-attribution while both hashes co-occur in the item; only a full swap (the `swapped`
fixture) reds. "binds each round-72 erratum item to its own revision" is enforced as
co-occurrence, not exclusivity. Additionally: only the two pinned labels are priced; extra
numbered items beyond the two are unpriced (L183 is a lower bound `len(items) < 2`), and the
errata block is taken to EOF (L179), so any later numbered list in round-71-claims.md is parsed
as erratum items.

**C2-Finding 5 (low — D2 escapes and dead code).** (a) L115 `if not path.exists(): return False`
— a self-test cell naming an ABSENT script is never unbacked; D1 (L156-171) covers only ENTRY
cells. (b) L128 `if not cell` — a whitespace-only cell is truthy, so it passes emptiness; a
whitespace-only self-test cell then also passes L147 (`"none" not in … ` plus unbacked False):
no defect. (c) L108 negation regex and the substring-backing rule as in instrument 1. (d) L140
`codes = set(… verdict) | set(… verdict.upper())` — the second findall is a no-op (digits are
case-insensitive); dead expression. (e) `command_flags` (L94-106) has ZERO call sites — dead
code; and no leg of either instrument prices the ENTRY cell's declared FLAGS against the
script's argparse (a row entry naming `--universe {full,legacy}` is never checked against the
script; only the self-test cell gets a backing check). (f) Gate verdict rule (L142-143) accepts
any DEFECT_WORDS substring as the failure class — "`0` ok, otherwise failure" passes without a
non-zero code; this matches the claims' "(`1` or a `failed` class)" wording, reported as
declared-loose, not a defect.

**C2-Finding 6 (low — A2's `total==rows` is reader-side).** The code prints
`INSTRUMENTS total={scripts} derived=registry rows={rows}` (L209) where scripts = DISTINCT entry
scripts (L158). Static derivation at landing bytes: rows=114, scripts=114, no shared entry
script — `total==rows` holds today, but nothing enforces it; a future row sharing another row's
script prints total<rows and only the seat reading the output can catch it.

## 2. Self-test and mutants

Four arms, no exit-code assertion anywhere; no arm reds D1 (SCRIPT-MISSING/SCRIPT-PARSE) or the
unbacked-selftest leg — those legs are guarded only by mutants M6/M7. The mutants battery is
real, not vacuous: base-redness guard (L365-368: `rc != 1 or "DEFECT" not in stdout → SETUP 2`)
refuses a do-nothing battery; the battery fixture reds every killable leg (kind L131 via census
gate, owner via `sibling`, gate-verdict via "`0` clean · `2` setup", duplicate, swapped errata,
`def (` parse error, unbacked self-test); kill criterion is stdout-or-rc difference against the
unmutated run; the null mutant must be DETECTED identical (`null_detected`, L378-383);
`MUTANTS total=len(MUTANTS)-1` = 7 (L398, L330-339) matches the frozen string, and `invalid`
needles make ok unreachable (L337-340, L399-401). Mutant needles each occur once in the source
(verified by read), so `replace(…, 1)` hits the intended site.

## 3. Silent pass — see C2-Findings 1 (operational), 2, 4, 5, 6 (each names line + counter-example).

## 4. Drift — frozen sentences vs printed strings

Format-exact for every required line: `INSTRUMENTS total=… derived=registry rows=…` (L209),
`PARSED scripts=… failed=…` (L210), `D1..D4 ok|defect n=…` (L212-215), `MISMATCH {total}` (L217),
`PREDICATE R73-C2 pass|fail` (L219), `SELFTEST arms=4 red=3 ok={ok}` (L324, literals),
`MUTANTS total=7 killed=… survived=… invalid=… null_detected=…` (L398-400). `DEFECTS n={total}`
(L218) is an extra line (the kill rule forbids absent/differing required lines, not extras).
A2's restated denominator (`total>=106`, `total==rows`) is consistent with the print and with
the landing bytes (114/114).

## 5. Two evidences

No committed snapshot + digest + expected verdict anywhere in the code; the row's pinned-values
cell self-declares "structural, no digests". The one persisted-expectation element is
ERRATUM_ITEMS (L52-55): frozen label→revision constants committed in the repo. §Gate Two-evidences
("a frozen baseline's `expected.json` MUST pin the digest of every snapshot input file, and the
gate verifies those digests before comparing verdicts") is implemented by NEITHER instrument;
both grade the live tree only, and neither prints the revision it measured.

---

# Amendments vs originals (per the L1's request; instruments untouched by me)

- **Original R73-C1: NOT satisfiable by the frozen code.** Proof: C1-Finding 2 (static) +
  `a1-red-green.txt` (run: all legs 0 → `PREDICATE R73-C1 fail`, rc=1). The E-R73-1
  non-admission is code-consistent and honest. Under the A1-amended bytes the original frozen
  SENTENCE is satisfiable and holds at the landing bytes (static derivation: every required line
  prints with 113 ≥ 111, MISSING 0, plans_seen 82 ≥ 1, rc 0).
- **Original R73-C2: NOT admissible at the landing tree** — its frozen denominator (106) is
  contradicted by C1's own 8 added rows (114 priced, rows==scripts, corrected rows price clean).
  E-R73-1's non-admission and its "not causally separable as written" note match the code facts.
- **A1 text defects:** (i) restates the target as 113 while asserting unchanged (original section
  says 112); (ii) its rationale survives only at print level — the widening adds zero
  instruments to the advertised SET at the landing bytes (legacy = full = 113; plans leg adds 0),
  so "2 instruments enter the universe through the plans/ leg" is false post-landing and nowhere
  retracted.
- **A2:** internally consistent and honest (explains 106→114; before value matches the frozen
  sentence's before-receipt).
- **E-R73-1 is uncommitted** at review time (worktree-only modification of
  `plans/round-73-claims.md`): the committed tree's claims doc lacks the erratum that makes the
  non-admission official. Flag for the L1 to land it with the round.

# RECIPE

- `round52_c2_registry.py`: the frozen predicate is demonstrably the code's predicate ONLY under
  the A1-amended bytes at `ea41880f` (every frozen line printed from cited code paths; rc rule
  matches; landing bytes statically green). The freeze-commit bytes (`255c261d`) could never
  print it — the original pair was contradictory, and the L1's non-admission is the correct
  disposition.
- `round73_c2_registry_audit.py`: the frozen-as-amended sentence is the code's predicate at print
  level (all formats exact; MISMATCH = D1..D4 total; rc rule matches; mutants floor real), with
  the denominator equality reader-side and the selftest tally literals — the audit's green at the
  landing bytes is real for every leg I could price statically, while D4's binding is weaker than
  the claim's wording.

*Probe transcripts and git commands behind this file ran with rc 0 on 2026-11-04 from
`/fast/scratch/hyaku/kengaku-r73/RegistryReviewerR73` (removed after writing). No tool was
installed or upgraded (none needed); no battery or verdict CLI run was performed (replay seat's
scope).*
