# C1CritDropEntry — round 51, C1 critic: controls 2 (drop-one-entry) and 3 (stale-pin)

Seat: critic. Lane: `kengaku-shokunin`. Freeze commit under test:
`e07f131cf7037e58a21db6e1f3986cf401ad257c` (stage-1 freeze). Every measurement below
carries that revision in the counter's own `REV` line.

**Axes named.** Primary: **freshness** (C1 — "every surface `PROVINCE.md` declares is
machine-checked"). I claim no axis move. Two secondary properties I attacked and do not
claim: **predicate integrity** (can the frozen predicate fail a landing that violates its own
kill rule?) and **control discriminating power** (does each control's exit code isolate the
branch it names?).

## Setup (scratch only, removed before yield)

```
mkdir -p /fast/scratch/hyaku/kengaku-r51/C1CritDropEntry
export TMPDIR=/fast/scratch/hyaku/kengaku-r51/C1CritDropEntry
D=$TMPDIR/lane
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D"
cd "$D" && test "$(git rev-parse --show-toplevel)" = "$D"   # asserted before every run
git checkout -B master e07f131cf7037e58a21db6e1f3986cf401ad257c
# HEAD e07f131cf7037e58a21db6e1f3986cf401ad257c, git status --porcelain -> 0 lines
```

Baseline, unmodified clone, frozen command (`python3 plans/round51_surfaces.py --lane .`)
reproduces `.ufo/waves/round-51/claims/c1-before.txt` **exactly** on every count line
(`DRIFT 3`, `UNVERDICTED 1`, `NUMBER-DRIFT 1`, `present=13 absent=6`, `RESOLVE … verdict=met`,
`PREDICATE R51-C1 fail`), with `REV e07f131…` in place of the base-tip REV. The instrument is
deterministic across the eight-day gap for these probes.

## Deliverable — control 2 (`drop-one-entry`)

Mutation: entry `SF11` removed from `plans/round51-surfaces.json` in the clone (18 entries
left, `ids` verified by `json.load`: `SF01..SF10, SF12..SF19`); `PROVINCE.md` untouched.
Command: `python3 plans/round51_surfaces.py --lane .`

```
REV e07f131cf7037e58a21db6e1f3986cf401ad257c
MANIFEST plans/round51-surfaces.json entries=18 sections=2
ANCHORS total=18 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=9 uncovered=1
PROBES run=18 present=12 absent=6 errors=0
DRIFT 3
  DETAIL DRIFT SF01 prose=present state=absent (…)
  DETAIL DRIFT SF02 prose=present state=absent (…)
  DETAIL DRIFT SF03 prose=present state=absent (…)
STALE 0
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 1
  DETAIL UNCOVERED ### Core row line 109 has no manifest entry
SECTION-MISSING 0
RESOLVE observed_present=12 floor=13 verdict=violated
PREDICATE R51-C1 fail
EXIT 1
```

Receipt: `.ufo/waves/round-51/claims/control-c1-drop-entry.txt` (counter stdout verbatim,
byte-identical to the captured run by `diff`, plus a `#` header and one trailing `EXIT 1`
line that is not counter output). `UNCOVERED 1` and exit 1 observed as the item requires;
line 109 is the real `| Own probe artifacts |` Core row in the freeze `PROVINCE.md`.

## Deliverable — control 3 (`stale-pin`)

Mutation: `SF10` `pin` `90c87c88` → `00000000` (clone only). `sha256sum grader.py` at this
revision prints `90c87c88…`, so the pin cannot match. Command: as frozen.

```
REV e07f131cf7037e58a21db6e1f3986cf401ad257c
MANIFEST plans/round51-surfaces.json entries=19 sections=2
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=12 absent=7 errors=0
DRIFT 3
  DETAIL DRIFT SF01 … / SF02 … / SF03 …
STALE 1
  DETAIL STALE SF10 probe=absent state=present (digest 90c87c88 does not start with pin 00000000)
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=12 floor=13 verdict=violated
PREDICATE R51-C1 fail
EXIT 1
```

Receipt: `.ufo/waves/round-51/claims/control-c1-stale-pin.txt` (same convention; `diff`-verified
against the captured run). `STALE 1` and exit 1 observed.

## Findings

### F1 (blocking, freshness) — a row deletion passes the frozen predicate; the kill rule is unenforced

The claims doc's kill rule says "the landing edit deletes a surface row instead of dating it
(`ROWS` per section must not fall below 9 and 10)". No predicate key checks that: the only
coverage-side guard is `SECTION-MISSING`, which fires only at **zero** rows. Counterexample,
built on a minimally repaired state (prose flips for SF01–SF03, `count_claim` 170 — see probe
E, which fails on exactly `UNVERDICTED 1 SF04`), then the `| Client CLI telemetry |` row
deleted from `PROVINCE.md` **and** its `SF05` entry dropped:

```
ROWS section="## Surfaces" rows=8 entries=8 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
DRIFT 0 / STALE 0 / UNVERDICTED 0 / NUMBER-DRIFT 0 / ANCHOR-DUP 0 / ANCHOR-MISSING 0 / UNCOVERED 0 / SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 pass
EXIT 0
```

A landing that shrinks the declared surface set passes C1 at the landing tip. For a freshness
claim ("every surface declared is machine-checked") that is the degenerate direction.
**Smallest safe correction:** add `"min_rows": {"## Surfaces": 9, "### Core": 10}` to
`plans/round51-surfaces.json` and a `ROWS-FLOOR` key in `check()` wired into `ok`
(`len(rows) < min_rows[sec]` → problem), keeping the same two sections. The after-target adds
a row, so 9/10 remain valid floors. (Frozen-before-data caveat: this changes a frozen
instrument; if the L1 will not touch a frozen counter, the alternative is to make the landing
receipt print and gate on the `ROWS` lines explicitly — weaker, human-checked.)

### F2 (blocking, freshness / false provenance) — `UNVERDICTED` is satisfied by round-25 markers

`ABSENT_RE` accepts any `ABSENT <ISO date>` anywhere on the row. The three drifting rows
already carry one: `grep -n 'ABSENT 2026-10-20' PROVINCE.md` → lines 12, 13, 14 (SF01, SF02,
SF03). So the entire after-target for `UNVERDICTED` can be met with **zero new dated evidence**
for the three rows this round's probes just found absent. Probe E (manifest prose flipped to
`absent` for SF01–SF03 and `count_claim` 170; `PROVINCE.md` byte-untouched):

```
DRIFT 0
STALE 0
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
EXIT 1
```

Only SF04 needs a date; the other two "dated absences" would be 2026-10-20 markers written 26
rounds before the probe that found them. **Smallest safe correction:** the landing must append
`**ABSENT 2026-10-28**` to rows 12/13/14 (its own plan already says "append-only: dated
markers plus a new correction section"), and the manifest should gain
`"absent_min_date": "2026-10-28"` with `UNVERDICTED` requiring `max(date on row) >= absent_min_date`
so a stale marker cannot carry the verdict.

### F3 (control design) — both assigned controls are confounded with the resolve floor

At the freeze `present == resolve_floor == 13`. Control 2 drops a *present* entry (SF11) and
control 3 breaks a *present* pin (SF10), so each also drives `present` to 12 and trips
`RESOLVE … verdict=violated`. Their exit 1 is therefore over-determined by pre-existing
`DRIFT 3 / UNVERDICTED 1 / NUMBER-DRIFT 1` **plus** the floor; only the `UNCOVERED 1` /
`STALE 1` lines are discriminating. The branches themselves are sound — isolated probes on the
repaired state, each with the floor met and every other key 0:

```
C) repaired + SF05 entry dropped, row kept:
ROWS section="## Surfaces" rows=9 entries=8 uncovered=1
UNCOVERED 1
  DETAIL UNCOVERED ## Surfaces row line 16 has no manifest entry
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail / EXIT 1

D) repaired + SF05 probe retargeted to an existing file, state stays absent:
STALE 1
  DETAIL STALE SF05 probe=present state=absent (all 1 targets resolve)
RESOLVE observed_present=14 floor=13 verdict=met
PREDICATE R51-C1 fail / EXIT 1
```

**Smallest safe correction:** run `drop-one-entry` against an absent, already-dated entry
(SF05 or SF06) instead of SF11, and record in the claims doc that the evidence for controls 2/3
is the named problem line, not the exit code. As written, a broken coverage check would still
have produced exit 1 in both controls.

### F4 (low) — the claim sentence is broader than the instrument's sections

`PROVINCE.md` carries two more surface tables outside the declared sections:
`### Adjacent` (line 129, 8 owner/routing rows) and `### Historical — absent, not governed`
(line 145, 12 `| Surface | Check | Result today | Last resolved |` rows, including
`HF + OpenRouter catalog endpoints | not probed this round | unverified`). The counter prints
`ROWS` only for `## Surfaces` and `### Core`, so "every surface `PROVINCE.md` declares is
machine-checked" is not literally true; it is true for the two tables named under "Surface
changed". **Smallest safe correction:** reword C1 to the two named tables, or add
`### Historical` to `sections` with entries (its rows are mostly the same targets as
SF01–SF06, so the marginal cost is the four unchecked ones).

### F5 (low, latent) — `count` probes parse the first integer in the detail string

`m = re.search(r"(\d+)", detail)` over `"%s=%d" % (label, n)`. A `label` containing a digit
would compare the wrong number. Not triggered at the freeze (`SF14` label `SOURCES rows`).
I independently verified the count: `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → `170`,
170 distinct ids, max `S177` — so `NUMBER-DRIFT 1` is a true defect and 170 is the correct
repair target, not a pattern artifact.

## State and limits

- Lane production files untouched: `git status --porcelain -- .ufo/waves/round-51/claims/`
  shows only untracked receipts (`control-c1-drop-entry.txt`, `control-c1-stale-pin.txt`, plus a
  sibling seat's `control-c1-declare-all-absent.txt`). All mutations were inside the clone;
  after restore `git status --porcelain` in the clone printed 0 lines at `e07f131…`.
- No `pacman`, no tool installs, no commits, no `agent://all`.
- Probes are host-state dependent (paths, ports, http). Nothing flapped between the baseline
  and the controls: `present=13 absent=6` identical in the baseline and in
  `c1-before.txt`.
- I audited only the prose readings that bear on my controls (SF01–SF06, SF10–SF14); the
  row-by-row prose audit is other seats' item. I did not run the C2 counter.
- Auxiliary probes A–E used `--manifest`/`--province` overrides in scratch; they are **not**
  control receipts and must not be cited as such. Their outputs are quoted above verbatim.
- Scratch `/fast/scratch/hyaku/kengaku-r51/C1CritDropEntry` removed before yield (verified
  absent); `/fast` free at removal: 542G.

VERDICT: Both assigned controls execute as specified at `e07f131…` — control 2 prints
`UNCOVERED 1` and exits 1, control 3 prints `STALE 1` and exits 1, receipts written and
diff-verified — but the C1 predicate as frozen is **not safe to score 9**: F1 shows a landing
that deletes a surface row (the claim's own kill-rule violation) passes with exit 0, and F2
shows the after-target's "dated absence" can be met with round-25 markers that predate this
round's probes. F1/F2 need the smallest safe corrections above before the after-measurement is
accepted; F3 means controls 2/3 evidence is their named problem line, not their exit code.

REV e07f131cf7037e58a21db6e1f3986cf401ad257c
