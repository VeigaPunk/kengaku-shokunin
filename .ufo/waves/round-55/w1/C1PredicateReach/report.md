# C1PredicateReach — R55-C1 predicate-reach attack (seat report)

Seat: C1PredicateReach (critic, lane leaf, no subagents). Axis judged: operability (R55-C1).
Counter under test: `plans/round52_c2_registry.py` (unchanged production r52 counter; I ran it
from a scratch clone at freeze commit `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`, base tip
`798f5e9e…`). All attacks on scratch copies only; no lane writes except this report.

## Direct answer: can the predicate pass without the repair being real?

**Yes — at the pure counter level, in three of the four assigned shapes.** The counter is an
*advertised-set-relative* closure check: it enumerates whatever the self-assessment files
advertise and requires a registry row per advertised, existing script. It cannot distinguish
"closure by registration" (the real repair) from "closure by universe shrinkage or cell
padding". Every bypass below printed the exact frozen after-predicate text
(`MISSING 0, INCOMPLETE 0, ENTRY-MISSING 0, SELFTEST-UNBACKED 0, DUPLICATE 0,
PREDICATE R52-C2 pass`, exit 0).

**But none of the bypasses defeats the claim.** The claim's security-critical content — a
round-55-added row whose verdict-map cell is FALSE — cannot be smuggled through any of these
routes: frozen leg 2 executes every round-55-added row's named self-test and matches the
observed verdict against the row's verdict-map cell; a padded/empty/absurd cell declares no
true verdict and fails that match (kill rule: operability held at 8). And each bypass
contradicts the r55 freeze's pinned landing content, which the L1 integration diff and the
outside closure review. Classification per attack below.

## Results table (base state: `MISSING 2`, exit 1 — receipt `base-before.txt`)

| # | bypass | counter verdict | caught? | receipt |
|---|---|---|---|---|
| A1 | de-advertise both r54 counters in `SCORECARD.md` (only ad site; verified via the counter's own `collect()`) | `ADVERTISED 77`, `MISSING 0`, **pass, exit 0**, zero rows added | **No** — counter-level bypass | `a1-counter.txt` |
| A2a | registry row with a self-test cell padded with 4 ASCII spaces | `INCOMPLETE 1` (`round54-c2`), fail | Yes | `a2-space-counter.txt` |
| A2b | registry row whose verdict-map cell is a single U+200B ZERO WIDTH SPACE | `INCOMPLETE 0`, all legs 0, **pass, exit 0** (cell is visually empty) | **No** — counter blind spot | `a2-zwsp-counter.txt` |
| A3a | twin row: unique name `round54-c1-confirm`, same entry script as `round54-c1`, absurd verdict map ("`0` ok in every tree including empty ones") | `DUPLICATE 0`, all legs 0, **pass, exit 0** | **No** — but see analysis | `a3-twin-counter.txt` |
| A3b | same twin rows, but the `round54-c2` row is withheld (script still advertised) | `MISSING 1` (`plans/round54_c2_entrytruth.py`), fail | Yes — duplicates cannot hide a missing script | `a3-withhold-counter.txt` |
| A4a | `git mv` both scripts to hyphenated names (`round54-c1-anchor.py`), re-advertise the new names in `SCORECARD.md`, no registry rows | `ADVERTISED 77`, **pass, exit 0** — live, runnable, unregistered instruments | **No** — counter-level bypass | `a4-rename-counter.txt` |
| A4b | delete both scripts; leave the `SCORECARD.md` advertisements in place | `ADVERTISED 77`, **pass, exit 0** (existence filter drops the dead ads) | **No** — counter-level bypass | `a4-delete-counter.txt` |
| A4c | registry rows present but entry cells lack the `python3 ` prefix (`./plans/…`), scripts still advertised | `MISSING 2`, fail — the rows never register | Yes | `a4-mangled-counter.txt` |

Commands and full outputs are in the receipts; every run was
`python3 <scratch>/base/plans/round52_c2_registry.py --lane <attack tree>`.

## Per-attack analysis

### A1 — de-advertising (MISSING empties without new rows)

- **Mechanism.** The two r54 scripts are advertised in exactly one place: `SCORECARD.md:2346-2347`
  (the r54 verdict rows' counting-command cells). `corpus/knowledge/external-anchor-freeze.md`
  mentions `plans/round54_c1_anchor.py` without a `python3 ` prefix → not an ad; `LOG.md` carries
  no `python3 plans/round54…` lines at the freeze. Replacing the two command cells with prose
  drops both scripts from `adv`; `missing = adv − reg` empties.
- **Is it consistent with the freeze? No.** (i) The r52 frozen universe rule defines the
  obligation as conditional on advertising (a script is in `ADVERTISED` iff it exists at the tip
  *and* appears as `python3 <path>`), and the r54 verifier spot-check's routed defect #1
  (`corpus/lessons/round-54-verifier-spotcheck.md:114`) explicitly offered "either register …
  **or stop advertising them**" — so the counter passing on a de-advertised tree is *by design*
  and is the blessed alternate branch of the r54 obligation. (ii) But the r55 freeze pins the
  landing's content descriptively: "Registry rows added in round 55: `round54-c1`, `round54-c2`,
  `round55-c2`, `round55-c2-controls`, `round55-c3`", and the after-predicate is "over the full
  advertised set at that revision — which includes every script this round's landing adds".
  A landing that instead deleted the advertisements would contradict the pinned row list and
  could only land via a dated amendment row (frozen rules never edit in place) — i.e. it cannot
  *silently* pass. (iii) Practically, de-advertising requires in-place deletion inside the
  committed r54 `SCORECARD` verdict rows (historical record); outside closures measure
  append-only diffs (r42 spot-check recorded `0` deleted lines), so the landing diff flags it.
- **Verdict: tradeoff, not a counter defect.** The do-nothing control ("a round that adds no
  registry rows cannot pass") is enforced by the freeze text + L1 diff review, not by this
  counter. The L1 must verify the landing *adds the five pinned rows* rather than shrinks the
  advertised set.

### A2 — padded cells vs the INCOMPLETE leg's `all()`

- `parse_rows` strips each cell (`c.strip()`), so ASCII whitespace padding collapses to `""` and
  `all()` correctly fires (**A2a caught**).
- U+200B is not `str.isspace()` whitespace, survives `.strip()`, and is truthy → `all()` sees a
  "complete" row. **A2b passes with a visually empty verdict-map cell.** Same class covers
  U+200C/U+200D/U+FEFF.
- **Can it carry a false verdict? No** — a ZWSP cell declares no verdict at all; leg 2's
  spot-execution has nothing to match, so the row fails the truth spot-check, and a reviewer
  cell audit sees an empty cell. It could, however, make a row with a genuinely required cell
  (e.g. pinned values) look complete at the counter level.
- **Smallest safe correction (amendment candidate — the counter is frozen this round):**
  normalize invisible characters in `parse_rows`, e.g.
  `cells = [re.sub(r"[\s\u200B-\u200D\uFEFF]", "", c).replace("\\|", "|") …]` or reject any cell
  that is empty after that normalization in the `incomplete` check. One line.

### A3 — duplicate entry scripts across two rows

- `reg` is keyed by entry script with `setdefault` (first row wins) but **no leg consumes the
  stored row's verdict map**; `DUPLICATE` compares row *names* only (Amendment A6: "duplicate
  row names fail"). A twin with a unique name and the same entry script is invisible
  (**A3a passes**, even with an absurd verdict-map cell).
- **Hiding a missing one: impossible** — `missing` is a set difference over advertised scripts
  (A3b: `MISSING 1` fires for the withheld row's script). INCOMPLETE scans all rows, and
  SELFTEST-UNBACKED scans all rows (verified incidentally: it fired on my first A2
  instrumentation's sibling row), so a twin cannot smuggle a blank cell or a bogus self-test
  flag either. The only channel a twin keeps open is an untruthful *verdict map* — which for
  round-55-added rows is exactly the kill rule's target and leg 2's duty.
- **Verdict: tradeoff.** Verdict-map truth was deliberately assigned to leg 2 + the kill rule,
  not this counter. Optional future hardening: a duplicate-entry-script leg.

### A4 — renaming / deleting so the advertisement regex misses it

- The `CMD` character class for script names is `[A-Za-z0-9_]` — no hyphens, dots, or slashes
  beyond the fixed shape. Renaming both scripts to hyphenated names and advertising the new
  names removes them from `adv` on both sides: **pass, exit 0, with the instruments alive and
  runnable but unregistered** (A4a). Deleting the scripts while leaving the ads in place also
  passes — `collect()` filters `adv` to scripts that exist (A4b). One-sided mangling fails:
  a registry row whose entry cell lacks the `python3 ` prefix never registers the script, and
  the still-advertised original is caught by MISSING (A4c).
- **Consistency with the freeze:** renaming/deleting the r54 counters contradicts the r54
  frozen claims (both counters remain named instruments of record) and the r55-c2 ledger work
  (ledger rows name these scripts' entry argv; the new binding counter executes them).
  Deleting/renaming the r55 scripts is impossible under the freeze, which names them
  character-for-character as members of the landing's advertised set
  (`plans/round55_c2_entryargv.py`, `plans/round55_c2_controls.py`,
  `plans/round55_c3_chess_probe.py`). All variants are diff-visible at integration.
- **Verdict: tradeoff, same class as A1** — universe shrinkage is invisible to an
  advertised-set-relative gate; the freeze compensates textually.

## Integration hazards found (for the L1 — not counter defects)

1. **`round54-c1`'s self-test is a subcommand, not a flag.** `plans/round54_c1_anchor.py` has no
   `--selftest` argparse flag; the self-test is the `selftest` subcommand (`:568`). A `round54-c1`
   registry row whose self-test cell says `python3 plans/round54_c1_anchor.py --selftest` (echoing
   the r54 claims' loose "--selftest 8/8" prose) fires `SELFTEST-UNBACKED` at the after-run — I
   demonstrated this firing in instrumentation (first A2 run: `SELFTEST-UNBACKED 1`). The
   truthful cell is `python3 plans/round54_c1_anchor.py selftest`.
2. **That self-test is not hermetic to a clean clone.** It imports `opentimestamps` at module
   load; the r54 OTS venv (`/fast/scratch/hyaku/kengaku-r54/l1/venv/otsenv`) referenced in the
   r54 SCORECARD row ("OTS venv required") **no longer exists** (scratch was reclaimed). Under
   system `python3`, `plans/round54_c1_anchor.py selftest` dies with
   `ModuleNotFoundError: No module named 'opentimestamps'` (nonzero exit). With a fresh venv
   (`opentimestamps-client 0.8.0`) it prints `[selftest] 8/8 PASS`, exit 0
   (receipt `c1-selftest-venv.txt`). Frozen leg 2 executes each round-55-added row's self-test
   "from a clean clone" — if the `round54-c1` cell names bare `python3`, leg 2 fails at landing
   for an environmental reason. The cell must either name an interpreter that provides
   `opentimestamps` or declare the dependency explicitly.
3. **`round54-c2`'s self-test is clean:** `python3 plans/round54_c2_entrytruth.py --selftest`
   → `[selftest] 7/7 PASS`, exit 0, under system `python3` (receipt `c2-selftest.txt`).

## What I ran (all commands; exit codes in receipts)

- Setup: `git clone --shared <lane> $S/base` (toplevel asserted: `$S/base`, HEAD
  `80afa613…`); attack trees as full `cp -a` copies (`cp -al` hardlinks caused one round of
  cross-tree contamination — caught by sanity greps, trees rebuilt; no lane impact).
- Base: `python3 plans/round52_c2_registry.py --lane $S/base` → `MISSING 2`, exit 1.
- A1: in-place cell rewrite of `SCORECARD.md:2346-2347` (no `python3 <script>` token) → pass, exit 0.
- A2: appended `round54-c1`/`round54-c2` rows to the SKILL.md registry block (truthful cells:
  c1 self-test = `… selftest` subcommand, c2 = `--selftest`) with padded cells → space caught,
  ZWSP passed.
- A3: appended twin row with unique name, same entry script, absurd verdict map → passed;
  then removed the `round54-c2` row → `MISSING 1`.
- A4: `mv` to hyphenated names + SCORECARD rename (passed); `rm` both scripts (passed);
  mangled `./plans/…` entry cells (caught).
- Self-tests: system `python3` and a fresh `uv` venv with `opentimestamps-client 0.8.0`.

## Files written

- This report: `.ufo/waves/round-55/w1/C1PredicateReach/report.md`
- Scoped findings: `.ufo/waves/round-55/w1/C1PredicateReach.md`
- Receipts: `.ufo/waves/round-55/w1/C1PredicateReach/receipts/` (11 files)

## Tool installs (per operator tooling authorization; no pacman)

- `uv venv $S/otsenv` + `uv pip install opentimestamps-client==0.8.0` — channel: uv 0.13.0
  (already installed) / PyPI; reason: execute `round54_c1_anchor.py selftest` to determine its
  truthful verdict for finding 2. Installed into seat scratch only (deleted with scratch).

## Dead ends / honest notes

- An unrun check has not passed: I did not run the r55-c2 entry-argv counter (sibling seat's
  instrument, still under construction) and did not re-derive the two r54 scripts' entry argv.
- The claims file says the r54 counters were "advertised in LOG.md"; at the freeze commit the
  live advertisement site is `SCORECARD.md:2346-2347` only (verified via the counter's own
  `collect()` map). The freeze's before-receipt (`c1-before.txt`) shows the same `MISSING 2`.
- Scratch dir `/fast/scratch/hyaku/kengaku-r55/C1PredicateReach/` deleted after copying
  receipts (verified absent).
