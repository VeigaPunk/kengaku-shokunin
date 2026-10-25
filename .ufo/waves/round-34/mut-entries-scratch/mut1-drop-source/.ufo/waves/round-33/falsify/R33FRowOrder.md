# R33FRowOrder — registry row ordering / section placement (falsify seat)

Seat: `KengakuR33.R33FRowOrder` (leaf; no subagent dispatch, no edits to lane/fleet files).
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Target: "Registry row ordering and section placement. Inspect sources_adopt output and census
contract. Verify current S103/S104 rows are in order inside `## Registry` before `## Paths`;
identify whether any check enforces within-section order."
All mutations confined to `/tmp/r33-roworder/` (fresh sandbox, `git archive HEAD` of the lane;
no git index/branch/commit touched anywhere). Lane at review time: HEAD `77ac8c1`; `corpus/SOURCES.md`
clean vs HEAD (its last commit is `b54feca`).

## 1. Verdict

**Current S103/S104 placement: confirmed in order, inside `## Registry`, before `## Paths` — caught.**
Section placement has a real enforcement (census **E12**); within-section ordering has **no**
enforcement in any check I could exercise (census, `sources_adopt.py`, `adoption_check.py`,
`round33_c1_verify.py`, `registry_check.py`, `state_check.py`). Multiple order- and
placement-breaking mutations pass all green gates, and the clean tree itself is not
id-sorted (S100 sits between S093 and S094), which proves no sorted-order invariant is
checked. Verdict components:

- in-order placement: **caught** (single real mutation swap detected only by manual inspection;
  no automated check flags it)
- within-section ordering enforcement: **uncaught/absent** (see §3, §4)
- section-placement enforcement: **partially present** — E12 catches column-zero S-rows outside
  `## Registry`, but is evadable (indent ≥4, fenced rows, 4-space-indented `## Paths` heading)
  and blind to `###` subsections containing rows (see §4).

## 2. Observed current state (real tree, HEAD 77ac8c1 = worktree)

- `## Registry` heading at line 19; the 97 registry rows all parse inside it; `## Paths` at
  line 120. S103 at line 118, S104 at line 119 — the final two rows, ascending, immediately
  before `## Paths`. (`grep`/python parse: 97 S-rows, all `Registry`.
- Registry order is *not* globally id-sorted anywhere: S093@112, **S100@113**, S094@114,
  S097@115, S101@116, S102@117, S103@118, S104@119. The R33 § (a) table and `R33C1KillRule.md:11`
  both assert this same placement.
- The frozen C1 predicate does not name ordering at all (only presence/status/opened/used-by),
  so no frozen claim's predicate depends on order; the "in order" property is a structural
  convention, not a predicate clause. `R33C1KillRule.md:44` already records *"the order/section
  check itself does not exist (census E12 only catches rows outside the ## Registry section;
  within-section ordering is unchecked)"* — this report confirms that and extends it.

## 3. sources_adopt output / gate behavior

`plans/sources_adopt.py` has no section or order state: `parse_rows` regexes the whole file
(`ROW_RE = ^ {0,3}\|[ \t]*(S[0-9]{3,})...`), `build_block` emits the requested rows in
`want_ids` order, and `check()` verifies collision/malformed/duplicate/quote/url-binding only.
It neither verifies the insertion point of the generated block nor any ordering. The
"append block" is therefore not placement-checked at admission.

## 4. Counterexample tests (all on `/tmp/r33-roworder/root/<lane>-shokunin` copies; census = `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <root> <lane>`; gate = `python3 plans/adoption_check.py --expect .ufo/waves/round-33/claims/adoption-expect.json --census`; V = `python3 plans/round33_c1_verify.py --lane .`; R = `python3 plans/registry_check.py`; S = `python3 plans/state_check.py --summary`)

| # | mutation | census | adoption | V | R | S | notes |
|---|---|---|---|---|---|---|---|
| 0 | baseline (untouched) | exit 0, 15 W04 | `...census=ok` rc0 | `checks=8 defects=0` rc0 | exit0 | 329/282 match | all-green baseline |
| 1 | **swap S103↔S104** (S104 first) | exit 0, same 15 W04 | rc0 `census=ok` | rc0 | exit0 | identical to baseline | **out-of-order row pair passes every gate** |
| 2 | **reverse entire registry block** (S104→S001) | exit 1: **E04** ×2 (S034/S030 dupe URL *within scope*), W04 set shifts | rc1 `census=fail` | rc0 | exit0 | S: mismatch count 34→35; P4b round26-sources range MISMATCH | order itself uncaught; only dup-URL (line-order-independent) and README range blips |
| 3 | S104 moved *inside* `## Paths` (column 0) | exit 1: **E12 S104** | rc1 `census=fail` | rc0 | exit0 | — | E12 does catch column-zero row after `## Paths` |
| 4 | S104 moved to `## Leads` tail | exit 1: **E12 S104** | rc1 `census=fail` | rc0 | — | — | E12 catches |
| 5 | S104 moved *before* `## Registry` (top) | exit 1: **E12 S104** | rc1 `census=fail` | rc0 | — | — | E12 catches |
| 6 | **S104 row indented 4 spaces inside `## Paths`** | exit 0, `ok`, no E | rc1: `rows_present=2 rows_mined=2 usedby_ok=0` | rc0 | — | — | **census is completely blind** (0–3-space contract boundary); gate fails only because the cited row vanishes, not because of placement |
| 7 | **S104 inside fenced block in `## Registry`** | exit 0, `ok`, no E (row still counted+validated) | rc0 `census=ok` | rc0 | exit0 | identical to baseline | **fence-blind**: a fence-embedded row is adopted as a real row |
| 8 | `## Paths` heading indented 4 spaces | exit 0, `ok`, 15 W04 | rc0 `census=ok` | rc0 | — | — | heading invisible to parser; rows after it remain "Registry" — no E12 |
| 9 | S104 under a `### Subsection` inside `## Registry` | exit 0, `ok`, no E | rc0 `census=ok` | rc0 | — | — | `###` headings don't reset/partition; subsection row remains a live registry row |

So: **no check enforces within-section order** (1, 2 pass; and the clean tree would already
fail any id-sort check), and **section placement is enforced only weakly** — E12 exists and
catches column-zero rows outside `## Registry` (3,4,5) but not indented rows (6), not rows
inside fenced blocks (7), not a 4-space-indented section heading (8), and not `###`-section
rows (9).

## 5. Impacted axes / smallest safe correction

- Axes: registry structure/admission integrity (C1 scaffold); repeatability of the
  "append after last Registry row, before `## Paths`" convention.
- Smallest correction that would make the *enforced* invariant match the *claimed* one:
  1. add one census check (or one `sources_adopt.py` gate check) asserting the ids in
     `## Registry` are non-decreasing (or at least that no row with id < previous id appears
     after a larger one) — this catches swap/reverse (1,2) while leaving the current
     S100-between-S093/S094 quirk to a data repair if desired;
  2. tighten section detection: honor 4+-space indentation as non-registry, and either
     track fenced blocks or treat fence lines as section boundaries in the gawk parser.

## 6. Evidence note

Lane git state was **not** altered (status at review showed only pre-existing dirty files:
`SCORECARD.md`, `R33L0Packet.md`, deleted assimilation fixtures). All mutations were created and
run under `/tmp/r33-roworder/`; exact commands captured in seat transcript.
