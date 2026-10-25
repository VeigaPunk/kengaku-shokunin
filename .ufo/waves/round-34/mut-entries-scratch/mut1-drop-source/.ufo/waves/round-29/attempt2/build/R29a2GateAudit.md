# R29a2GateAudit — mutation audit of the C2 adoption-gate selftest

Seat: `L1Kengaku29.R29a2GateAudit` (leaf). Round 29 attempt 2 (hyaku run 6), 2026-10-25.
Object: `plans/sources_adopt.py` (C2 standing gate) and its `--selftest`.
Axes served: **coverage** (does each case actually witness the capability?) and **operability**
(can the audit be re-run against later bytes, and what does a green selftest fail to mean?).
Findings only: no production file was created, edited or deleted; no judging, no integration,
no commit. Every claim below carries the command that produced it, inlined, so this report does
not depend on surviving scratch. Scratch (transient): `/tmp/r29a2-GateAudit/`.

## 0. Object under test, and why the revision is pinned

`plans/sources_adopt.py` was being edited by sibling seats throughout this audit. Five distinct
byte states were observed (read-only `sha256sum plans/sources_adopt.py`):

| # | sha256 (12) | lines | when observed | what was measured on it |
|---|---|---|---|---|
| R1 | `8bc43121…` | 367 | 03:38 | the three assigned mutations only (identical outcome to R2) |
| R2 | `d59f43a1…` | 401 | 03:4x | **pinned snapshot** `/tmp/r29a2-GateAudit/base2.py`; full 16-mutant matrix |
| R3 | `505478fd…` | 401 | 03:4x | hand mutants t_c1…t_k5 (case-6 regression first appears here) |
| R4 | `289390db…` | — | 03:46 | hash only (observed between batches) |
| R5 | `ab594472…` | 424 | 03:48:16 (live, stable) | **current tip**; full 16-mutant matrix + all end-to-end probes |

Lane HEAD throughout: `8c14a5d` (`git rev-parse --short HEAD`). The frozen C2 target measures the
selftest, not a blob, so both pinned states were measured and the two matrices are reported side by
side. All line numbers below are for R5 unless a section says otherwise.

R5 vs R2 is three changes (`diff /tmp/r29a2-GateAudit/base2.py /tmp/r29a2-GateAudit/live-tip.py`):
`SYMBOLIC_CADENCE` gains `"on-commit"`; `cells[8] = access_date …` becomes unconditional
`cells[8] = access_date`; case 5 gains a 12-cell fixture, case 6 gains an `on-commit` fixture, and
case 10 gains an unscoped prose-refusal clause. Those case changes close two holes and open one
(§5) — see §3/§4 columns.

## 1. Baseline (current bytes `ab594472…`, 424 lines)

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 plans/sources_adopt.py --selftest
CASE collision-zero-indent PASS
CASE collision-one-space PASS
CASE collision-three-space PASS
CASE four-space-not-a-row PASS
CASE escaped-pipe-refused PASS
CASE prose-recheck-normalized PASS
CASE usedby-projected PASS
CASE duplicate-staged-id PASS
CASE clean-package-passes PASS
CASE missing-requested-id PASS
SELFTEST cases=10 failed=0
EXIT=0
```

python3 3.14.8. Identical result on R1 at 03:38 (`SELFTEST cases=10 failed=0`, `EXIT=0`) and on
R2 (`python3 /tmp/r29a2-GateAudit/base2.py --selftest` → same ten PASS, `EXIT=0`). The frozen
"exits 0 printing ten PASS" target holds on every byte state I sampled.

## 2. The three assigned mutations

Each mutation is a one-line edit on a copy (`diff` reported exactly 2 changed lines = 1 line out,
1 line in). Verbatim outputs are from R5 (`ab594472…`); R1 and R2 produce the same failing sets.

### M-A — replace the 0–3-leading-space anchor with a column-zero-only anchor

`sources_adopt.py:33`, old → new:

```python
ROW_RE = re.compile(r"^( {0,3})\|[ \t]*(S[0-9]{3,})[ \t]*\|")
ROW_RE = re.compile(r"^()\|[ \t]*(S[0-9]{3,})[ \t]*\|")
```

```
$ python3 t_c1.py --selftest
CASE collision-zero-indent PASS
CASE collision-one-space FAIL
CASE collision-three-space FAIL
CASE four-space-not-a-row PASS
CASE escaped-pipe-refused PASS
CASE prose-recheck-normalized PASS
CASE usedby-projected PASS
CASE duplicate-staged-id PASS
CASE clean-package-passes PASS
CASE missing-requested-id PASS
SELFTEST cases=10 failed=2
  failed: collision-one-space collision-three-space
EXIT=1
```

**Killed (2):** `collision-one-space`, `collision-three-space`. **Exit 1.**
**Survivors (8):** `collision-zero-indent`, `four-space-not-a-row`, `escaped-pipe-refused`,
`prose-recheck-normalized`, `usedby-projected`, `duplicate-staged-id`, `clean-package-passes`,
`missing-requested-id`.
Note on the survivor that matters: `four-space-not-a-row` is *structurally* blind to this mutation
class — it asserts a row is **not** counted, and narrowing the anchor can only make more rows
invisible, so it cannot notice. The case that objects to anchor *widening* is the separate mutant
`k2_wide_anchor` (§3).
Mechanism, end to end (registry row S002 at column 0, staged row S002 with one leading space):

```
$ python3 live-tip.py                   --registry fix/reg.md --package fix/pkg-indent1.md   # exit 3
registry=1 staged=1 collisions=1 malformed=0 duplicates=0 defects=0 prose=0
  collisions: S002
EXIT=3
$ python3 live-tip-mutants/c1_column_zero_anchor.py --registry fix/reg.md --package fix/pkg-indent1.md
registry=1 staged=0 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
EXIT=0
```

The mutated gate **silently greens a real indented collision** (`staged=0`, exit 0) — the exact
false-green the module docstring at `:12` warns about. Two cases stand between the shipped tool and
that failure mode.

### M-B — `split_cells` does not strip before slicing

`sources_adopt.py:71`, old → new:

```python
    body = stripped.strip()
    body = stripped
```

```
$ python3 t_c2.py --selftest
CASE collision-zero-indent PASS
CASE collision-one-space FAIL
CASE collision-three-space FAIL
CASE four-space-not-a-row PASS
CASE escaped-pipe-refused PASS
CASE prose-recheck-normalized PASS
CASE usedby-projected PASS
CASE duplicate-staged-id PASS
CASE clean-package-passes PASS
CASE missing-requested-id PASS
SELFTEST cases=10 failed=2
  failed: collision-one-space collision-three-space
EXIT=1
```

**Killed (2):** `collision-one-space`, `collision-three-space`. **Exit 1.**
**Survivors (8):** the same eight as M-A.
Mechanism differs from M-A and is worth separating — the mutated tool stays *loud*:

```
$ python3 live-tip-mutants/c2_split_no_strip.py --registry fix/reg.md --package fix/pkg-indent1.md
registry=1 staged=0 collisions=0 malformed=1 duplicates=0 defects=0 prose=0
  malformed: S002:not-a-table-row
EXIT=4
```

The in-clause indented row is refused as malformed (exit 4, `not-a-table-row`) instead of being
parsed. No case asserts the positive proposition "a well-formed row indented 1–3 spaces parses
against an empty registry"; the pair of collision cases implies it, and nothing else measures it.
That is why a mutation that changes *how* an indented row is missed kills the same two cases and no
more.

### M-C — the duplicate-id check is skipped

`sources_adopt.py:173`, old → new:

```python
    dupes = duplicate_ids(ids(staged))
    dupes: list[str] = []
```

```
$ python3 t_c3.py --selftest
CASE collision-zero-indent PASS
CASE collision-one-space PASS
CASE collision-three-space PASS
CASE four-space-not-a-row PASS
CASE escaped-pipe-refused PASS
CASE prose-recheck-normalized PASS
CASE usedby-projected PASS
CASE duplicate-staged-id FAIL
CASE clean-package-passes PASS
CASE missing-requested-id PASS
SELFTEST cases=10 failed=1
  failed: duplicate-staged-id
EXIT=1
```

**Killed (1):** `duplicate-staged-id`. **Exit 1.**
**Survivors (9):** every other case. `duplicate-staged-id` is the sole witness for
`duplicate_ids()`; no case co-exercises duplicate detection with a nonempty collision set, so the
two refusal paths are never distinguished. End-to-end the mutated gate returns exit 3
(`collisions: S002`) on the P1 fixture, i.e. it is unchanged on that path — nothing else in the
suite would have reported the missing capability.

## 3. Kill matrix — every one of the ten cases can be made to fail

Sixteen one-line mutants, re-runnable via `mutate.py` (§7). `exit` and `failed=` are the mutated
tool's own selftest output.

| mutant | site (R5) | one-line change | R2 `d59f43a1` | R5 `ab594472` |
|---|---|---|---|---|
| `c1_column_zero_anchor` | :33 | `^( {0,3})` → `^()` | 2 fails, exit 1 | 2 fails, exit 1 |
| `c2_split_no_strip` | :71 | `body = stripped.strip()` → `body = stripped` | 2, exit 1 | 2, exit 1 |
| `c3_no_duplicate_check` | :173 | `dupes = duplicate_ids(...)` → `dupes: list[str] = []` | 1, exit 1 | 1, exit 1 |
| `k1_no_collision_check` | :172 | `clash = collisions(...)` → `clash: list[str] = []` | 3, exit 1 | 3, exit 1 |
| `k2_wide_anchor` | :33 | `^( {0,3})` → `^( *)` | 1, exit 1 | 1, exit 1 |
| `k3_no_escape_guard` | :69-70 | delete the `"\\|"` guard | 1, exit 1 | 1, exit 1 |
| `k4_no_recheck_norm` | :152 | `cells[9] = access_date` → `= recheck` | **1, exit 1** | **0, exit 0** (§5) |
| `k5_no_usedby_rewrite` | :154 | `cells[10] = used_by` → `= cells[10]` | 1, exit 1 | 1, exit 1 |
| `k6_spurious_defect` | :102 | `defects: list[str] = []` → `= ["spurious"]` | 2, exit 1 | 2, exit 1 |
| `k7_no_missing_check` | :214 | `missing = [...]` → `missing = []` | 1, exit 1 | 1, exit 1 |
| `h1_dead_anchor_switch` | :86 | `pattern = ROW_RE if anchor else …` → `pattern = ROW_RE` | **0, exit 0** | **0, exit 0** |
| `h2_no_row_defects` | :101 | `row_defects` returns `[]` | 0, exit 0 | 1, exit 1 |
| `h3_no_columns_check` | :75 | `if len(cells) != COLUMNS:` → `if False:` | 0, exit 0 | 1, exit 1 |
| `h5_no_status_rewrite` | :155 | `cells[7] = "mined"` → `= cells[7]` | 0, exit 0 | 0, exit 0 |
| `h6_no_opened_write` | :153 | `cells[8] = access_date` → `= cells[8]` | 0, exit 0 | 0, exit 0 |
| `h7_no_scoped_prose_exemption` | :195 | `[item for item in found if item != "recheck-prose"]` → `list(found)` | 0, exit 0 | 0, exit 0 |

Per-case kill coverage (a case is a control if some mutant turns it red):

| case | killed by |
|---|---|
| `collision-zero-indent` | k1 |
| `collision-one-space` | c1, c2, k1 |
| `collision-three-space` | c1, c2, k1 |
| `four-space-not-a-row` | k2 |
| `escaped-pipe-refused` | k3 (R2 and R5), h3 (R5 only) |
| `prose-recheck-normalized` | k4 on R1/R2; **nothing on R5/K5 except the k4+h6 combination (§5)** |
| `usedby-projected` | k5 |
| `duplicate-staged-id` | c3 |
| `clean-package-passes` | k6 |
| `missing-requested-id` | k6, k7 (R2 and R5), h2 (R5 only) |

Collateral kills (reported so the matrix is not over-read): `k1` kills all three collision cases
because it removes the shared `clash` computation; `k6` kills `clean-package-passes` and
`missing-requested-id` because an always-present defect forces `EXIT_MALFORMED` before the request
path is reached.

**Kill rule status.** The frozen rule ("if any of the ten cases cannot be made to fail on a
deliberately broken implementation, the case is not a control") is satisfied on R2 for 10/10. On R5
it is satisfied by construction for 9/10 and only by a *conjunction* for
`prose-recheck-normalized` — that is the §5 finding, not a dead case.

## 4. Mutants the current selftest cannot see

Four mutants leave the R5 suite at `SELFTEST cases=10 failed=0`, `EXIT=0`, and two more did so on
R2 and have since been caught:

| mutant | disabled capability | R5 suite | what the mutated gate actually does (end-to-end, run) |
|---|---|---|---|
| `h1_dead_anchor_switch` | `parse_rows(anchor=False)` | 0 fails | switch is never exercised — `grep -n 'anchor'` shows the ternary at :86 and no call site passing `anchor=False`; the docstring at :83-84 claims "that switch exists only so the selftest can prove the narrow anchor is load-bearing" — **false as written** |
| `h5_no_status_rewrite` | `status` → `mined` on append | 0 fails | no case reads the emitted row's status cell; the fixture row is already `mined`, so the rewrite is unobservable |
| `h6_no_opened_write` | `opened` → access date | 0 fails | `EXIT=0` emitting `| S013 | … | mined | unknown | 180d | …` (opened stays `unknown`) |
| `h7_no_scoped_prose_exemption` | scoped prose `recheck` not fatal | 0 fails | `EXIT=4` on a prose-recheck row inside `--admit-ids` scope (base: `EXIT=0` + `normalized recheck S012: 2026-10-23 — re-verify at next release`) |
| `h2_no_row_defects` | status/recheck/source schema | 0 fails on R2; **1 fail on R5** (`missing-requested-id`, via the new unscoped-prose clause) | on R2: `EXIT=0` for a row with `status=bogus` and a prose recheck |
| `h3_no_columns_check` | 11-cell requirement | 0 fails on R2; **1 fail on R5** (`escaped-pipe-refused`, via the new 12-cell fixture) | on R2: `EXIT=0` and the 12-cell row is written into the append block verbatim (`… | corpus/knowledge/new.md | twelfth-cell |`) |

Two corrections this implies for sibling receipts written against earlier bytes:
`R29a2FixtureMutations` M2 (accept a 12-cell row) and M3 (any nonempty recheck valid) are listed as
survivors there; on the **current** bytes both are now killed by case 5 and case 10 respectively —
the status change comes from the R5 case additions, not from a different reading. Conversely, R5
*introduced* the §5 regression.

## 5. Headline finding: on the current bytes `prose-recheck-normalized` no longer isolates recheck normalization

On R2, deleting `cells[9] = access_date` (mutant `k4`) failed `prose-recheck-normalized`
(`SELFTEST cases=10 failed=1`, exit 1). On R5 the same one-line deletion passes all ten
(`k4_no_recheck_norm`, `SELFTEST cases=10 failed=0`, exit 0), because R5 made
`cells[8] = access_date` unconditional and case 6's only value assertion is a row substring,
`"| 2026-10-25 |" in block[0]` — which the **opened** cell now satisfies on its own.

The mutated gate really is broken; the selftest just cannot see it:

```
$ python3 live-tip-mutants/k4_no_recheck_norm.py --registry fix/reg.md --package fix/pkg-prose.md \
      --admit-ids S012 --access-date 2026-10-25 --entries corpus/knowledge/new.md
registry=1 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=1
  normalized recheck S012: 2026-10-23 — re-verify at next release
| S012 | fixture source — https://example.invalid/p | docs | A | fixture scope | anchor text | fixture teaches |
  mined | 2026-10-25 | 2026-10-23 — re-verify at next release | corpus/knowledge/new.md |
EXIT=0
```

The recheck cell still carries the raw prose although the tool claims it "normalized" it — and the
gate exits 0. The case is not dead, only ambiguous: it fails only when recheck normalization **and**
the opened write are both removed, which proves the assertion is satisfied by whichever cell writes
the date first:

```
$ python3 combo_k4h6.py --selftest          # k4 + h6 combined
CASE prose-recheck-normalized FAIL
SELFTEST cases=10 failed=1
EXIT=1
```

Advisory (one line, not applied): assert on the parsed recheck cell of the emitted row
(`block[0].split("|")[10].strip() == "2026-10-25"`) instead of a substring over the whole row, and
pin `opened` in a separate assertion. That makes case 6 single-mutation lethal again and makes
`h6` visible. This agrees with `R29a2CritClaimC2` §N3's observation that deleting the normalization
survives; it adds the reason (the opened cell) and shows the case is not inert.

## 6. Read-only cross-instrument notes

- **Anchor authority.** `plans/sources_adopt.py:33` and `plans/adoption_check.py:33` hold
  byte-identical literals `^( {0,3})\|[ \t]*(S[0-9]{3,})[ \t]*\|`. The fleet census accepts 0–3
  leading spaces and then strips them (`scripts/sources-census.sh:615-616`: `if (line !~ /^ {0,3}\|/) next;`
  then `sub(/^ {0,3}/,"",line)`), so gate and fleet census agree. `plans/round28_census.py:40`
  matches `^\|\s*S[0-9]{3,}\s*\|` — column zero only. A 1–3-space-indented registry row would be
  counted by the gate, the counter and the fleet census but not by `round28_census.py`. This
  corroborates `R29a2RevCensus` F4; I did not modify any of the four parsers.
- **Wiring.** No gate entry point inside the lane invokes the tool: a grep for `sources_adopt` over
  the lane tree (`plans/`, `corpus/`, and the lane root) returns only `PROVINCE.md:224`,
  `SCORECARD.md:994-1005`, `corpus/README.md:90-92`, the round's claims/dispatch and peer reports —
  no script, Makefile or gate source. For the fleet-side files (`grader.py`,
  `plans/round28_census.py`, `plans/config_projection.py`, `scripts/sources-census.sh`) the count is
  0, measured independently by `R29a2Regression:166`. The "standing gate" is standing by convention
  (an operator or seat runs it), not by an enforced call site.
- **C2 attribution.** The claim's clause 1 says the anchor is "the census parser's own
  0–3-leading-space row anchor". That is true of `scripts/sources-census.sh` and `adoption_check.py`;
  it is not the anchor `round28_census.py` uses. If C2 needs to name one authority, name
  `sources-census.sh`.

## 7. Reproduce (self-contained; no scratch dependence)

Build any mutant by copying `plans/sources_adopt.py` and applying the one-line change from the §3
table (`old` text is unique in the file at the current revision; if `str.replace` finds 0 or 2
hits, the file drifted — that is the signal, not a pass). Then `python3 <mutant> --selftest` and
read `CASE … FAIL` lines plus the exit code.

Harness used here (`/tmp/r29a2-GateAudit/mutate.py`, ~120 lines, stdlib only): it takes a base path,
prints `base=… sha256=… lines=…`, writes `<base-stem>-mutants/<name>.py` per table row, runs
`--selftest`, and prints `name, exit, failed=<cases>, SELFTEST line` with `NOT-FOUND` when the old
text is absent. Re-run as:

```
$ python3 mutate.py /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/sources_adopt.py
```

Three CLI fixtures (all 11-cell, one row below the two header lines; written to `/tmp`, never the
lane). `reg.md` holds `S002` at column 0; `pkg-indent1.md` is the same row with **one** leading
space; `pkg-12col.md` is `S011` plus a 12th cell `twelfth-cell`; `pkg-badschema.md` is `S010` with
`status=bogus` and `recheck=someday soon`; `pkg-prose.md` is `S012` with
`recheck=2026-10-23 — re-verify at next release`; `pkg-badopened.md` is `S013` with `opened=unknown`.
Probe commands are quoted verbatim in §2, §4 and §5.

## 8. Bounds, tooling, risks

- **No production edits**: nothing under the lane was created, edited or deleted by this seat; the
  only lane file written is this report. All work on copies under `/tmp/r29a2-GateAudit/`.
- **Read-only elsewhere**: `/home/vgpnk/Projects/shokuknow` campaign tools were not run; no `git`
  write, fetch or push anywhere.
- **Tooling**: nothing installed or upgraded; no pacman transaction attempted (host-wide pause
  untouched). `python3` 3.14.8 and coreutils sufficed.
- **Not verified here**: C1's entry, its five sources, and the counter `adoption_check.py` are other
  seats' scope. I did not run `grader.py`, `round28_census.py`, the fleet census or
  `adoption_check.py`; the "no axis harmed" claim is the L1's post-integration gate, not mine.
- **Risk carried into the Gate**: the tip moved four times inside one audit window (R1→R5). Any C2
  receipt must pin a sha256, because a selftest verdict of `failed=0` is now provably compatible
  with two disabled capabilities (`k4`, `h6`) and a row-written `unknown` date. The three assigned
  mutations kill the same cases on every revision sampled, so those findings transfer; the case-6
  ambiguity is specific to R5 (`ab594472…`) and later.
