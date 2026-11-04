# ReviewerR82 — adversarial review of R82-C1 (coverage)

Seat `ReviewerR82`, lane `kengaku-shokunin`, wave w1. Measured tip
`12f1029a45cf0097a3afd030d757bf93b87f8018` (freeze commit; `git rev-parse master`), base
`a3a03ac31451e58f1742b9bccb73b72c2d90a95c`. All runs in a scratch clone
(`git clone --shared`, HEAD `12f1029a` at clone time); the lane worktree was never a target of
any writing tool. Scratch `/fast/scratch/hyaku/kengaku-r82/ReviewerR82/` deleted on yield.

**State of the world at measurement time.** `plans/round82_c1_plans_registry.py` is **absent**
from the lane (only `plans/round82-sweep-map.json` exists under `round82*`); the four registry
rows are **not installed** in `SKILL.md` (133 rows today; target `rows=<133+4>`); the draft rows
exist only as the wave deliverable `.ufo/waves/round-82/w1/RegistryRowsR82.md`. Therefore every
counter-mediated attack (1–4) is **UNATTACKED at the counter level** — there is no counter to
falsify. I attacked what exists: the universe rule (independently re-derived from BASE bytes),
the byte preconditions each attack relies on, and the truth of the four drafted rows (attack 5,
fully executed). Nothing below re-opens a frozen predicate.

---

## Attack 1 — does the universe read BASE bytes, not the worktree? — UNATTACKED (counter absent); byte-level equivalent HELD

The counter does not exist, so the fake-SCORECARD experiment could not be run. What I could
measure, I measured:

**(a) Independent re-derivation of the universe from BASE bytes reproduces the frozen BASE state
exactly** (`cd $S/clone`):

```
$ git ls-tree -r --name-only a3a03ac.. -- plans/ | grep '\.py$' | grep -v '^plans/fixtures/' | wc -l
295
$ for d in SCORECARD.md LOG.md corpus/README.md; do git show a3a03ac:$d | grep -oE '(?:\.\./)*(plans/[A-Za-z0-9_./-]+\.py)'; done | sort -u | wc -l   # with ../ normalized, fixtures kept
144
```

Filtering to `plans/fixtures/` removed → **140 referenced paths**. Filtering again to paths that
**exist at BASE** (`git cat-file -e a3a03ac:<path>`) drops exactly 7 never-landed references —
`plans/round34_{c1_verify,defects,mutate}.py`, `plans/round48_{c1,c2}_verify.py`,
`plans/round49_{c1,c2}_verify.py` (each `ABSENT-at-BASE`, verified individually) — leaving 133.
Classifying the remainder by BASE bytes (`argparse`/`__main__` presence):

```
MISSING_candidates      = plans/log_appendonly.py, plans/round37_c1_attribution.py,
                          plans/round66_registry_check.py, plans/round80_c1_remint.py   (each argparse>=2,__main__=1)
UNCLASSIFIED_candidates = plans/fixture_fence.py, plans/policy_cases.py                  (argparse=0,__main__=0)
```

This is exactly the frozen do-nothing state (`MISSING 4`, `UNCLASSIFIED 2`). **A never-landed
reference is not an instrument: confirmed from bytes** — the 7 dead references would inflate
UNCLASSIFIED to 9 if the counter skipped the exists-at-BASE leg. Whether the counter implements
that leg is unmeasured (counter absent).

**(b) BASE-vs-tip drift of the three documents**: referenced sets at BASE and at tip are
identical (140 = 140, `tip_minus_base=[]`), so at this tip a worktree-reading counter would
coincidentally agree with a BASE-reading one on the document side. The distinction is therefore
not observable through the current bytes — the attack's discriminating power remains unspent for
when the counter lands.

**Verdict: UNATTACKED (counter absent); independent byte derivation HELD against the frozen state.**

## Attack 2 — can a stub row pass? — UNATTACKED (counter absent); rows themselves HELD

No counter exists to feed a stub row. Substitute executed: I applied the frozen row-quality rule
by hand to the four drafted rows, parsed out of `RegistryRowsR82.md` §1:

```
$ python3 - <row-quality script over the four draft rows>   # full script in scratch log
`log-appendonly`: cells=8 kind_ok=True entry=plans/log_appendonly.py exists+parses=True map_ok=True selftest_ok=True pins_ok=True
`round37-c1-attribution`: cells=8 kind_ok=True entry=plans/round37_c1_attribution.py exists+parses=True map_ok=True selftest_ok=True pins_ok=True
`round66-registry-check`: cells=8 kind_ok=True entry=plans/round66_registry_check.py exists+parses=True map_ok=True selftest_ok=True pins_ok=True
`round80-c1-remint`: cells=8 kind_ok=True entry=plans/round80_c1_remint.py exists+parses=True map_ok=True selftest_ok=True pins_ok=True
```

The four rows are not stubs (all eight cells non-empty, kinds valid, entries parse at BASE, gate
maps declare `0`+`1`, probe map declares `0`, self-test flags occur in the named scripts'
sources, pins/write-scope non-empty and not `n/a`). Whether the counter *rejects* stubs is
unmeasured. **Verdict: rows HELD; counter enforcement UNATTACKED.**

## Attack 3 — can EXCLUSIONS launder a CLI script? — UNATTACKED (counter absent); byte precondition HELD

`plans/log_appendonly.py` was the laundering candidate named by the item:

```
$ for p in plans/log_appendonly.py plans/round37_c1_attribution.py plans/round66_registry_check.py plans/round80_c1_remint.py plans/fixture_fence.py plans/policy_cases.py; do
    a=$(git show a3a03ac:$p | grep -c argparse); m=$(git show a3a03ac:$p | grep -c __main__); echo "$p argparse=$a __main__=$m"; done
plans/log_appendonly.py argparse=2 __main__=1
plans/round37_c1_attribution.py argparse=2 __main__=1
plans/round66_registry_check.py argparse=3 __main__=1
plans/round80_c1_remint.py argparse=2 __main__=1
plans/fixture_fence.py argparse=0 __main__=0
plans/policy_cases.py argparse=0 __main__=0
```

The four row-candidates are CLIs by the claim's own byte rule; the two exclusions are not. Any
counter that reads BASE bytes must print `EXCLUSION-CLI` for a `log_appendonly.py` exclusion; a
counter that lets it pass is broken. Behavior unmeasured. **Verdict: byte precondition HELD;
counter behavior UNATTACKED.**

## Attack 4 — reverse direction (ENTRY-MISSING) — UNATTACKED (counter absent); independent audit HELD

Deleting an entry script and running the counter requires the counter. Substitute: audited all
133 existing rows' entry argv (first backticked span of each entry cell, every `.py` path token,
`git cat-file -e a3a03ac:<path>`):

```
first-span entry paths checked=133 entry_missing=0 rows=133
```

Every registry row at the tip names a script that exists at BASE — including one non-plans entry
(`coverage-census` → `corpus/evidence/round13-coverage/coverage_census.py`, `EXISTS` at BASE).
Caveat recorded for the counter's parser: entry cells contain prose paths (`/app/attack.py` in
`feal-probe`'s `--stage-check` description, `` `adoption_check.py` `` in `round31-c1-literals`'s
V-description); a naive whole-cell regex extractor false-positives ENTRY-MISSING on both. My
initial run made exactly that mistake (3 phantom ENTRY-MISSING); the first-span rule cleared
them. **Verdict: reverse direction HELD at the tip (entry_missing=0); counter's scratch behavior
UNATTACKED.**

## Attack 5 — are the four drafted rows TRUE? — HELD

Every declared entry argv run independently in the scratch clone (never against the lane;
`round80_c1_remint.py` run only against the clone, per the seat item):

**`log-appendonly`** — `python3 plans/log_appendonly.py --lane .` →
`LOG-APPENDONLY commits=141 violations=9`, 9 `VIOLATION` lines, rc 1 (red at tip, as the row
states — newest `3cc5cecb6752 deleted=2 at=2990,2991`); `--help` shows `--lane/--path/--since/
--show-lines/--verbose/--selftest` and **no `--work`** (row cell true, `grep -c -- "--work"` = 0);
`--selftest` → `SELFTEST pass` rc 0; `--lane . --since bogus` → `SETUP --since bogus: not a
commit` rc 2. Self-test flag `--selftest` occurs 3× in source. Row's measured pair (141/9)
reproduced exactly.

**`round37-c1-attribution`** — full run `python3 plans/round37_c1_attribution.py --lane . --work
<S>/attrwork` → `ATTRIBUTED 55/55 UNATTRIBUTED=0`, rc 0, 15.4 s wall. `--help` shows exactly
`--lane/--work`. Row's `0` leg true. (`1` leg not induced — matches scribe §7.3, named UNVERIFIED
there too.)

**`round66-registry-check`** — `quote corpus/lessons/round-66.md` → `quotes=3 misses=0`,
`CHECK ok quote`, rc 0; `meta corpus/SOURCES.md` → 3 findings all on S234 (`corpus/SOURCES.md:250`),
`rows=253 findings=3`, `CHECK meta fail`, rc 1; selection `S236 S237` → `rows=2 findings=0` rc 0
(red is row-attributed, not blanket); `quote corpus/lessons/nope.md` → `SETUP lesson not found`
rc 2; `--selftest --work <S>/r66work` → 13-case dict all `True`, rc 0 (matches the cell's "13
named cases"). `META_PHRASES = ("word bar", "teaches is one benefit", "same source and capture")`
at `plans/round66_registry_check.py:50` — pin cell true.

**`round80-c1-remint`** — `--help` → `--lane` required, `--work/--python/--only` optional (cell
true); dirty-tree probe → `SETUP worktree not clean (1 paths)` rc 2; **empty selection in the
clone**: `REMINT minted=0 failed=0` rc 0 with `sha256sum plans/grader-population-ledger.json`
identical before/after (`15fb159d…`), `git status --porcelain` = 0 lines, `ls
corpus/evidence/round80 | wc -l` = 24 — the `0` leg and the write-scope cell (receipts **and**
ledger rewrite at `:180-181`, even for an empty selection) are both true. Stamp pins verified in
source: `SOURCE_SHA/TOOL_SHA/LANE_TIP` at `:145-148`, `MINTED_BY_SHA` at `:153`. The full
six-member mint (`minted=6`), the `3` leg, and `--verbose` remain UNVERIFIED — I did not attempt
them either (scribe §7.1–7.2 names the same gaps; not re-litigated).

**Verdict: HELD — every measured cell of all four rows reproduces; no cell misstates the bytes.
The two EXCLUSIONS entries are byte-true (classes verified in attack 3's table).**

---

## Verdict on R82-C1 as it stands at tip 12f1029a

The claim cannot pass today: the counter is absent and the four rows + two exclusions are not
installed in `SKILL.md`. What is attackable without the counter held: the universe derivation
(reproduced MISSING 4 / UNCLASSIFIED 2 from BASE bytes with correct never-landed filtering), the
byte classes (4 CLI rows / 2 support modules), the reverse direction (133/133 entry argv exist at
BASE), and the truth of all four drafted rows (all legs I ran reproduce). What I could not attack
is named, not implied: attacks 1–4 at counter level (counter absent at measurement time), the
counter's stub-row rejection, its `EXCLUSION-CLI` emission, its scratch `ENTRY-MISSING`
behavior, and its `--selftest`/`--mutants`/`--control-*` batteries. Re-run these five the moment
`plans/round82_c1_plans_registry.py` lands; until then the claim's target state is unmeasured,
not passed.

## Residual risk / verification gaps

1. Counter entirely unreviewed (all five item attacks at counter level: UNATTACKED).
2. Entry-cell parser fragility (prose paths inside entry cells) — if the counter extracts paths
   whole-cell, it will false-positive `ENTRY-MISSING`; unmeasured.
3. Scribe's own UNVERIFIED list stands (round80 full mint + `3` leg; round37 `1` leg;
   `log_appendonly --verbose` WALK line) — I verified nothing there either.
4. `log-appendonly` is red at the tip (9 violations, F1) and `round66 meta` is red on S234 (F2);
   both reds are true measurements and belong to the L1's landing decision, not to this review.
5. Calibration (R82-C2) and freshness (R82-C3) counters are likewise absent at the tip; out of
   this seat's scope, noted only as lane state.

**Tooling:** nothing installed or upgraded (no pacman transaction; host-wide pause respected; no
`uv`/`npm`/binary installs needed).

**Scratch:** `/fast/scratch/hyaku/kengaku-r82/ReviewerR82/` (one `--shared` clone + work dirs)
deleted on yield per the seat rule. Lane bytes written by this seat: this report only.
