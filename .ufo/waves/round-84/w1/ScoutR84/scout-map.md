# ScoutR84 — read-only surface map for kengaku round 84

Seat: `ScoutR84` (role `scout`, wave `w1`, round 84). Read-only: no lane file was modified.
All paths below are absolute. Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
(`L`). Base revision of the frozen claims: `4087b2f8369fb0c317a8460725a607681ff2fd7f`;
claims frozen at `b12a9d46806cb8d69fe48fac0f4efff0b266e4c2` (`plans/round-84-claims.md`).

---

## A. SKILL.md surfaces that describe the file-artifact class counts and the registry

### A.1 The class row (the count surface R84-C1 must move)

`L/SKILL.md:74` — exact current text of the row:

```
| file-artifact | 76 | executed 19 of 76 (round 83 adds `code-from-image`; round 81 added `log-summary-date-ranges`, `vulnerable-secret`) | the candidate's output files are materialised in the sandbox at the paths the grader reads; the grader then reads and parses those files itself, the probe only supplying the end state (the two host-side probes of this class hand the grader a frozen table of file contents instead). The round83 replay uses a real private `/app/output.txt`, not a patched reader. | `corpus/evidence/round40/db-wal-probe.txt`, `plans/db_wal_probe.py`; `corpus/evidence/round83/code-from-image-probe.txt` |
```

Cell split (verified by splitting on unescaped `|`, 5 cells):
- cell 0 `file-artifact`
- cell 1 `76` (census count, unchanged by R84)
- cell 2 `executed 19 of 76 (round 83 adds `code-from-image`; round 81 added `log-summary-date-ranges`, `vulnerable-secret`)`
- cell 3 recipe prose
- cell 4 receipt pointers (ends `; \`corpus/evidence/round83/code-from-image-probe.txt\``)

**Proposed replacement for round 84 (cell 2):**

```
executed 20 of 76 (round 84 adds `gcode-to-text`; round 83 adds `code-from-image`; round 81 added `log-summary-date-ranges`, `vulnerable-secret`)
```

**Verification of the numbers (measured, not inferred).** `L/plans/grader-population-ledger.json`
(`schema` `r79-population-ledger/1`, `members` = 88 rows) parsed directly:
- current `status` census: `executed` = **27**, `unexecuted` = **61** (no `executed-unlocated` rows exist).
- `file-artifact` class membership (from `L/corpus/evidence/round62/class-survey.txt:7`, `CLASS file-artifact count=76`): of those 76 census members the ledger currently marks **19** `executed` (no `executed-unlocated`), so the class cell must read `executed 20 of 76` after `gcode-to-text` flips to `executed`.
- after the flip: **executed 28, unexecuted 60**, class `file-artifact` **20 of 76**.

This matches the frozen claims text (`L/plans/round-84-claims.md:42-43`: "executed 27 → 28, unexecuted 61 → 60; file-artifact class 19 of 76 → 20 of 76") and the claims' own BASE statement (`TARGET … executed=1`, `defects=>=1` before). Independently confirmed by two sibling seats: `.ufo/waves/round-84/w1/Reviewer2R84.md:141` ("members 88, executed 27, unexecuted 61, file-artifact class 76 of 88") and `.ufo/waves/round-84/w1/ConnectorR84/overlap.md:89` ("File-artifact class executed: `19 of 76 → 20 of 76`").

**Is line 74 a gate-read surface? YES — three gates read it.**
1. `L/plans/round79_c1_population_ledger.py:332-370` (`check_skill`): parses the row's cell 2 with `CELL = re.compile(r"^executed\s+(\d+)\s+of\s+(\d+)(?:\b|$)")` (line 80) and compares `(k, n)` against the ledger-derived counts (line 358-362); mismatch ⇒ `CLASS-K-MISMATCH`, exit 1. `k` counts ledger members whose `status` is `executed` or `executed-unlocated` (line 353-355); `n` = census class size (76). So the cell must read exactly `executed 20 of 76 …` after the flip.
2. `L/plans/round63_gate_checks.py:236-377` (`depth_measure`, the R63-C2 depth gate) reads the same table: cell 1 (`76`) must equal the census `CLASS … count=`, cell 4 (pointer) must contain at least one path token that resolves, and every path token in the whole section must resolve (`resolved == total`, `share >= 0.90`, line 322-330).
3. `L/plans/round78_c1_class_member_ledger.py:157-185` (`skill_partial_rows`) also derives a universe from rows whose cell 2 matches `PARTIAL = re.compile(r"executed\s+(\d+)\s+of\s+(\d+)")` (line 58) — **but this counter is RETIRED** and is not re-run at later tips (see `L/SKILL.md:720`, scope cell: "**RETIRED round 79** … its universe rule (SKILL rows carrying `executed k of n`) now selects the 88-member population, so it is not re-run at later tips"). Measured at this tip it already fails with 121 defects (`DEFECTS n=121`, `PREDICATE R78-C1 fail`), so it is **not** a landing gate for R84 and must not be treated as one.

### A.2 Every other occurrence of the searched tokens in `L/SKILL.md`

`19 of 76` — 1 occurrence: `L/SKILL.md:74` only (grep count = 1). `executed 19` — 1 occurrence: `L/SKILL.md:74` only (grep count = 1). No other SKILL.md line states the file-artifact executed count.

`grader-population` — 4 occurrences:
| line | text (exact) | gate-read? |
|---|---|---|
| `L/SKILL.md:89` | ``census member list — `ledger=plans/grader-population-ledger.json`, gated by`` | **YES** — `round79_c1_population_ledger.py:353-356` requires the literal `LINK = "ledger=plans/grader-population-ledger.json"` inside the class-table section (else `LINK-ABSENT`). It is a pointer to the ledger file, not a count; **no edit needed** for R84, but it must not be removed. |
| `L/SKILL.md:723` | registry row `round79-c1-population-ledger` — "… `plans/grader-population-ledger.json` (88 members) + `plans/round-79-claims.md` …" | No count change needed: 88 is the **member** count and stays 88; the executed/unexecuted split is not asserted there. Gate-read as a registry row (shape rules in §B). |
| `L/SKILL.md:733` | registry row `round80-c1-remint` — "… an in-place rewrite of `plans/grader-population-ledger.json` …" | historical description of the round-80 driver; no count. Registry-row shape only. |
| `L/SKILL.md:736` | registry row `round82-c3-sweep` — "… `plans/grader-population-ledger.json` sha256 in the receipt …" | pins the **historical** round-82 sweep receipt's ledger sha; the round-82 sweep is a frozen historical instrument at `a44b2f083ee8b4115aea64598646f4bd9e3c1470` and must not be re-pointed (see the boundary note at `L/SKILL.md:746`). No edit. |

`round83-` — the round-83 registry rows and boundary prose: `L/SKILL.md:740` (`round83-code-image-probe`), `:741` (`round83-c1-replay`), `:742` (`round83-c2-debt`), `:743` (`round83-c2-checks`), `:744` (`round83-freeze-controls`), plus `L/SKILL.md:746` (the "Round83 boundary" paragraph). **All are historical and must stay unchanged.** `L/SKILL.md:746` states "not a current 27-member sweep after code-from-image enters the ledger" — that is a *historical* statement about the round-82 instrument (26 members) versus the population at the time round 83 landed; it is **not** a claim about the current executed count and the R84 flip does not falsify it. R84's new rows must be **additive** rows (e.g. `round84-gcode-probe`, `round84-c1-replay`, `round84-c2-admission`), not edits to rows 740-744.

Literal `27` elsewhere in `L/SKILL.md` (all non-population, no edit): `:360` ("r5 task 27"), `:645` ("`SELFTEST ok=27/27`"), `:646` ("`plans/round-27-claims.md`"), `:667` ("`tasks_with_presence_only=27`"), `:746` (the boundary sentence above), and pure line-number references at `:1067`, `:1119`, `:1189`, `:1270`, `:1295`, `:1310`, `:1349`, `:1382`, `:1446`, `:1460` (e.g. "`:27-28,44,53`"). None of these is the population executed count.

### A.3 Other lane files that state the same numbers (not SKILL.md, but the same surface family)

- `L/SCORECARD.md:3957` — "population accounting passes with file-artifact **19/76**". This is the round-83 closure's historical scorecard row; `SCORECARD.md` is append-only-by-ledger in this lane and the round-83 row is a dated historical record. The L1 should append a new round-84 row rather than rewrite `:3957`. (Flagged for the L1's judgement; I did not edit it.)
- `L/PROVINCE.md:1118` and `:1136` — the historical 26-member round-82 sweep wording ("The historical round82 sweep remains a 26-member census at its cited tree, not a current sweep of the expanded executed set"), again historical and unchanged by R84.
- `L/corpus/README.md:945` — index row for `knowledge/tb2-replay-sweep-at-one-tip.md` describing the frozen 26-member map; unchanged.

**Summary for the L1:** exactly **one** SKILL.md count must move — `L/SKILL.md:74` cell 2 → `executed 20 of 76 (round 84 adds \`gcode-to-text\`; …)`. Everything else containing `19 of 76`, `executed 19`, `27`, `grader-population`, `round83-` is either a pointer, a historical boundary, an unrelated literal, or a registry-row shape obligation.

---

## B. The registry gate: what a new `plans/*.py` and a new SKILL.md row must satisfy

### B.1 `L/plans/round74_c1_registry.py` (R74-C1, decoupled universe) — the primary registry gate

Measured at this tip: `ADVERTISED total=141`, `REGISTERED total=148`, `MISSING 0`, `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 0`, `DUPLICATE 0`, `PREDICATE R74-C1 pass`.

What it requires of a **new `plans/*.py`** (it is a *coverage* gate over advertised instruments, not a per-file linter):
- **Advertisement universe** (`self_assessment_files`, lines 60-107): `SCORECARD.md`, `SKILL.md` *outside* the `## Gate/probe registry` section, `LOG.md`, `corpus/README.md`, every `corpus/knowledge/*.md`, and every `plans/*.md`. Anything matched by `CMD = re.compile(r"python3 ((?:plans/[A-Za-z0-9_.-]+\.py|grader\.py|...))")` (line 45-47) **and** existing on disk becomes an advertised instrument and **must** have a registry row (`missing = sorted(set(adv) - set(reg))`, line 165). ⇒ the frozen claims doc itself (`L/plans/round-84-claims.md:36, 78`) already advertises `python3 plans/round84_c1_replay.py` and `python3 plans/round84_c2_admission.py`; once those files exist on disk they become advertised and **MUST** have rows. `plans/round84_gcode_probe.py` is named in the claims as a bare path (not `python3 …`), so it is not advertised by the `CMD` regex — but the counter and probe rows should still register it, because §B.2 requires the entry script to exist for any row that names it.
- **Column count**: `parse_rows` (lines 118-131) keeps only lines that split into exactly **8** cells (`len(cells) != 8 → continue`), skipping the header row (`cells[0] == "name"`) and separator rows.
- **Per-row obligations** (`collect`, lines 146-172): every cell non-empty (`INCOMPLETE`); the entry cell's script must exist on disk (`ENTRY-MISSING`); no duplicate row names (`DUPLICATE`); the self-test cell must be **backed**: `selftest_unbacked` (lines 134-143) requires that the cell name exactly **one** `plans/…py` script **and** at least one `--flag`, and that every flag string appears literally in that script's body — unless the cell says "no … --flag" within 24 chars.
- **Cell semantics** (column headers at `L/SKILL.md:594`): `name | kind | entry | verdict map | self-test | pinned values | write scope | owner`.

### B.2 `L/plans/round82_c1_plans_registry.py` (R82-C1) — the row-shape gate

Measured at this tip: `MISSING 0`, `UNCLASSIFIED 0`, `ENTRY-MISSING 0`, all `ROW … defects=none` for the rows it prints. Its `row_defects` (lines 133-171) is the *shape* oracle for a **new** row:

| cell | name | requirement (source) |
|---|---|---|
| 0 | name | backticked, unique (`:135` `name = cells[0].strip("`")`; `:170` owner check) |
| 1 | kind | exactly `gate` or `probe` (`KINDS = ("gate","probe")`, line 22; `KIND` defect, `:140`) |
| 2 | entry | must match `CMD_RE = re.compile(r"python3\s+(plans/[A-Za-z0-9_./-]+\.py)")` (line 20) — the referenced script must exist **and** parse (`ast.parse`, `parses`, lines 121-129) else `ENTRY-MISSING` / `ENTRY-UNPARSED` (`:143-149`) |
| 3 | verdict map | `gate` rows must contain `` `0` `` **and** ( `` `1` `` or the word "failed") (`VERDICT-MAP`, `:150-155`); `probe` rows must contain `` `0` `` |
| 4 | self-test | either the literal `none declared`, or a `python3 <plans script> …` invocation whose `--flags` all appear in that script's body (`SELFTEST-UNBACKED` / `SELFTEST-FLAG:<flag>`, `:156-165`) — `SELFTEST_RE` (line 21) permits an optional `-B` |
| 5 | pinned values | non-empty and not in `NA = {"n/a","n.a.","na","-","none"}` (`PINS-EMPTY`, `:166-168`) |
| 6 | write scope | same non-empty / not-NA rule (`SCOPE-EMPTY`) |
| 7 | owner | must start with `kengaku` (case-insensitive `OWNER`, `:169-170`) |

Also: `ADDED_CHECK = True` (line 78) means the row-shape leg runs on rows **added at the tip** (line 246-253), i.e. exactly the R84 rows. The forward "MISSING" leg of R82 covers only scripts referenced from `SCORECARD.md`, `LOG.md`, `corpus/README.md` at `BASE_REV` (`DOCS`, line 19) — a new `plans/round84_*.py` referenced only from SKILL.md/claims does not trip it, but it must still be registered so R74/R52 stay at `MISSING 0`.

### B.3 `L/plans/round52_c2_registry.py` (R52-C2 / R73-C1) — the same registry, wider universe

Measured at this tip: `ADVERTISED total=147`, `REGISTERED total=147`, `MISSING 0`, `PREDICATE R52-C2 pass`, `PREDICATE R73-C1 pass`. Its `CMD` (line 30) is narrower — `plans/[A-Za-z0-9_]+\.py` (underscores, **no hyphens**) — and its universe (line 44-55) is `SCORECARD.md`, `SKILL.md` (whole file), `LOG.md`, `corpus/README.md`, `corpus/knowledge/*.md`, `plans/*.md`. Consequence for R84: **`plans/round84_c1_replay.py`, `plans/round84_gcode_probe.py` and `plans/round84_c2_admission.py` must use underscore names** (the claims already do) or they will not be picked up by R52's `CMD` while still being picked up by R74's hyphen-tolerant `CMD` — an inconsistent-universe split to avoid.

### B.4 Exact row shape the three new R84 instruments need

Working example to copy: the round-83 rows at `L/SKILL.md:740-744` (probe) and `:741`/`:742` (gate). The R84 additions (row names are the L1's to choose; the *shape* is fixed by §B.1/§B.2):

```
| `round84-gcode-probe` | probe | `python3 plans/round84_gcode_probe.py --lane . --work DIR` (`--selftest`) | `0` eight vectors match and `PREDICATE R84-PROBE pass` · `1` prediction mismatch · `2` setup, including changed subject/table or unexpected test exception | `python3 plans/round84_gcode_probe.py --lane . --work DIR --selftest` | subject sha256 6b049dc626aa103b20d165552e5cb39ba02c6803b04ba06a43d79435b5f701a6; plans/round84-cases.json sha256 <pinned by the L1> | explicit scratch only; private bubblewrap /app, lane read-only | kengaku |

| `round84-c1-replay` | gate | `python3 plans/round84_c1_replay.py --lane . --work DIR` (`--rev REV`, `--selftest`, `--mutants`, `--control-do-nothing`, `--control-ledger-only`, `--control-fabricated-observations`) | `0` `PREDICATE R84-C1 pass`, one located/executed member, eight cases and zero mismatches · `1` named receipt, stamp, digest, vector, reproduction or ledger defect · `2` could-not-evaluate | `python3 plans/round84_c1_replay.py --selftest --work DIR`; separate attributed `--mutants` and three controls | plans/round-84-claims.md; BASE 4087b2f8; frozen subject sha256 6b049dc626aa103b…; corpus/evidence/round84/gcode-to-text-probe.txt | measured bytes read-only; reproduction and fixtures under explicit --work; COMMAND never executed | kengaku |

| `round84-c2-admission` | gate | `python3 plans/round84_c2_admission.py --lane . --work DIR` (`--rev REV`, `--selftest`, `--mutants`, `--control-do-nothing`, `--control-fabricated-fixture`) | `0` `PREDICATE R84-C2 pass`, entries=1 q1=0 q21=0 q13=0 defects=0 · `1` any remaining admission-bar defect · `2` could-not-evaluate | `python3 plans/round84_c2_admission.py --selftest --work DIR`; separate mutants and controls | plans/round-84-claims.md; corpus/knowledge/tb2-code-from-image-offline.md; corpus/lessons/round-84.md | read-only lane; fixture scratch only | kengaku |
```

Mandatory shape checklist (all three rows): 8 cells exactly · kind ∈ {gate, probe} · entry names an existing, parseable `plans/…py` · verdict map contains `` `0` `` (gates also `` `1` ``/failed) · self-test cell names exactly one script whose `--flags` exist in that script (or says `none declared`) · PINS and SCOPE cells non-empty and not `n/a`/`-`/`none` · owner cell starts `kengaku` · unique name.

---

## C. The population gate: `L/plans/round79_c1_population_ledger.py`

### C.1 Fields read for an **executed** row (`check`, lines 206-330)

For `status == "executed"` the gate reads, from `plans/grader-population-ledger.json` `members[<member>]`:
1. `status` — must be in `STATUSES = ("executed","executed-unlocated","unexecuted")` (line 84) ⇒ `STATUS-UNKNOWN` otherwise.
2. `classes` — must equal the census class list for that member exactly (`sorted(classes) == sorted([c for c,ms in universe.items() if m in ms])`, line 229-231) ⇒ `PAIR-MISMATCH`. For `gcode-to-text` the census lists it in **exactly one** class: `file-artifact` (`L/corpus/evidence/round62/class-survey.txt:7`; verified by parsing all 16 `CLASS` lines — `gcode-to-text` appears only in `file-artifact`), so the row must carry `"classes": ["file-artifact"]`.
3. `receipt` — must be a **tracked** path at the measured revision (`lane.tracked(receipt)`, line 236-239) ⇒ `RECEIPT-UNTRACKED`. `tracked` = present in `git ls-tree -r <rev>` for a `--rev` tree (`rev_tree`, lines 139-161) or `git ls-files --error-unmatch` for the worktree. ⇒ the receipt must be **committed**, not merely present.
4. `verdict` — must equal `observations(receipt_text)` (line 246-248) ⇒ `VERDICT-MISMATCH`.
5. `subject` — must equal `subject_shape(receipt_text, member)` (line 249-252) ⇒ `SUBJECT-ABSENT` / `SUBJECT-MISMATCH`.
6. Not read for an executed row: `reason`, `evidence`, `instrument`, `debt`, `round`. (`round` **is** read for `executed-unlocated` rows, line 266; the R84 row is `executed`, so `round` is a lane convention, not a gate field — but `round83_c1_replay.py:503` does assert `round` for its own row, so the R84 counter should too.)

Additional executed-row constraint: the receipt may name **at most one** census member (`REPLAY_RECEIPT_MAX_MEMBERS = 1`, line 102; `distinct_members_named`, lines 199-200) ⇒ `RECEIPT-POPULATION` otherwise. The round-83 receipt names only `code-from-image`; the R84 receipt must likewise name only `gcode-to-text`.

### C.2 Verdict vocabulary — and the exact receipt line the R84 row needs

`observations(text)` (lines 182-190) returns the **first** match of:
1. `predicate` — if the receipt contains a line matching `OBS_PRED = re.compile(r"^PREDICATE R\d+-C\d+ pass", re.M)` (line 91). Note the shape: `PREDICATE R<digits>-C<digits> pass`. **`PREDICATE R84-PROBE pass` does NOT match** — `PROBE` is not `C\d+`.
2. `vectors` — a line matching `OBS_VEC = re.compile(r"^VECTOR ", re.M)` (line 92).
3. `cases` — a line matching `OBS_CASE = re.compile(r"^(?:CASE |case=)", re.M)` (line 93). The probe's own `CASE <id> predicted=… observed=…` lines match this.

⇒ Because the round-83-style receipt carries both `CASE …` lines **and** a `PREDICATE R83-C1 pass` line, the round-83 ledger row has `verdict: "predicate"` (`plans/grader-population-ledger.json` → `code-from-image` row, measured). **For the R84 row the receipt must contain a line `PREDICATE R84-C1 pass`** (the counter's own verdict), otherwise `observations()` returns `cases` and the row's `verdict: "predicate"` is a `VERDICT-MISMATCH`. **Measured counterfactual in a scratch clone:** replacing `PREDICATE R83-C1 pass` with `PREDICATE R84-PROBE pass` in the receipt flips the derived verdict to `cases` and the gate prints `DEFECT VERDICT-MISMATCH gcode-to-text ledger=predicate receipt=cases` → `PREDICATE R79-C1 fail`. (This is a property of the *gate*, not a change to the frozen claim: the claims already require the counter to print `PREDICATE R84-C1 pass`, so the receipt must carry both the probe's `PREDICATE R84-PROBE pass` **and** the counter's `PREDICATE R84-C1 pass`, exactly as the round-83 receipt does at `:24` and `:37`.)

Subject vocabulary (`SUBJECTS`, lines 94-100) — first match wins, in this order:
- `tb2-header` — a line matching `^# tb2 gcode-to-text grader probe` (re.M)
- `receipt-header` — `^# R\d+-C\d+ receipt -- TB2 gcode-to-text grader offline`
- `grader-path` — `^GRADER .*corpus/evidence/round52/graders/gcode-to-text/tests/`
- `task-under-test` — `^TASK-UNDER-TEST gcode-to-text\s*$`
- `capture-tree` — `^grader=corpus/evidence/round\d+/tb2-gcode-to-text/`

`subject_shape` returns the **first** pattern that matches, so a receipt whose first line is `# tb2 gcode-to-text grader probe` yields `tb2-header` — but note the header line must literally be `# tb2 gcode-to-text grader probe` (no `(round 84)` suffix tolerated by the *counter* though the *gate* tolerates it, since the gate regex is unanchored at the end: measured, `# tb2 code-from-image grader probe` → `tb2-header`). **Measured counterfactual:** rewriting the receipt's first line to `# gcode-to-text grader probe` gives `DEFECT SUBJECT-ABSENT gcode-to-text corpus/evidence/round84/gcode-to-text-probe.txt` → `PREDICATE R79-C1 fail`.

### C.3 The exact expected ledger row for `gcode-to-text`

```json
{"status":"executed",
 "receipt":"corpus/evidence/round84/gcode-to-text-probe.txt",
 "round":84,
 "subject":"tb2-header",
 "verdict":"predicate",
 "classes":["file-artifact"]}
```

Verdict string `predicate` ✔ (the vocabulary the gate derives for a receipt carrying `PREDICATE R84-C1 pass`); subject string `tb2-header` ✔ (the vocabulary the gate derives for a receipt whose first line is `# tb2 gcode-to-text grader probe`). The two fields the task text did not list, `classes` and `round`, are also required/expected: `classes` is **read and compared** by the gate (§C.1 item 2 — `["file-artifact"]` is the census-derived value) and `round` is asserted by the round-83-style counter (`plans/round83_c1_replay.py:496-503` checks `status`, `receipt`, `subject`, `verdict`, `round` in that order).

**End-to-end verification (measured in a scratch clone, not the lane).** In a `git clone --shared` of the lane, I (i) wrote a minimal `corpus/evidence/round84/gcode-to-text-probe.txt` with the round-83 stamp shape (`# tb2 gcode-to-text grader probe`, `MEMBER`, `SUBJECT_CAPTURE`, `SUBJECT_SHA`, `OBSERVATIONS_BEGIN/END`, `CASE …`, `cases=8 mismatches=0`, `PREDICATE R84-C1 pass`), (ii) flipped the ledger row to the JSON above, (iii) set `L/SKILL.md:74` cell 2 to `executed 20 of 76 …`, and (iv) ran `python3 plans/round79_c1_population_ledger.py --lane .`:

```
LEDGER rows=88 executed=28 unlocated=0 unexecuted=60
CLASS file-artifact k=20 n=76 cell=executed 20 of 76 (round 83 adds `code-from-image`; …
DEFECTS n=0
TARGET classes=16 members=88 pairs=230 replayed=28 located=28 unlocated=0 unexecuted=60 unaccounted=0 unbacked=0 understated=0 covered=15
PREDICATE R79-C1 pass        (exit 0)
```

This confirms the claim's counting outputs ("executed 27 → 28, unexecuted 61 → 60; file-artifact class 19 of 76 → 20 of 76") and the single required SKILL.md count edit. The clone was deleted afterwards; the lane was never written to.

---

## D. Current ledger row for `gcode-to-text` and the captured grader sha

**Current ledger row** (`L/plans/grader-population-ledger.json`, `members["gcode-to-text"]`, measured verbatim):

```json
{"classes": ["file-artifact"],
 "evidence": "no-blocker: tests/test_outputs.py sha256=6b049dc626aa103b",
 "reason": "unattempted",
 "status": "unexecuted"}
```

Note it carries **no** `receipt`, `round`, `subject`, `verdict` keys — those must be added by the flip. The `evidence` field is the round-83-style `no-blocker:` pin (prefix 16 hex) and is what the R84 counter should use as the *base* evidence prefix to check `SUBJECT_SHA` against (round-83's counter does exactly this: `prefix = (row.get("evidence") or "")`, `SHA_RE = re.compile(r"[0-9a-f]{16,64}")`, then `SUBJECT-BASE-EVIDENCE` defect if `SUBJECT_SHA` does not start with it — `plans/round83_c1_replay.py:302-312, 370-372`). The prefix `6b049dc626aa103b` is unique to this row (measured: no other member's `evidence` contains it).

**Captured grader sha (measured, `sha256sum`):**

```
6b049dc626aa103b20d165552e5cb39ba02c6803b04ba06a43d79435b5f701a6  /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round52/graders/gcode-to-text/tests/test_outputs.py
```

**Matches the ledger evidence prefix `6b049dc626aa103b` exactly** (16-hex prefix of the same digest), and matches the claims' stated pin (`plans/round-84-claims.md:14-15`: "sha256 `6b049dc626aa103b20d165552e5cb39ba02c6803b04ba06a43d79435b5f701a6` (ledger pin prefix `6b049dc626aa103b`)"). No drift: the captured grader is byte-identical to what the base ledger pins.

**Grader content** (`corpus/evidence/round52/graders/gcode-to-text/tests/test_outputs.py`, 20 lines, unmodified upstream, canary header present): two functions in definition order — `test_hello_file_exists` (reads `Path("/app/out.txt").exists()`; `assert`, so a missing file ⇒ `AssertionError`, **not** `FileNotFoundError`) and `test_hello_file_content` (`Path("/app/out.txt").read_text().strip() == "flag{gc0d3_iz_ch4LLenGiNg}"`). Also present: `corpus/evidence/round52/graders/gcode-to-text/tests/test.sh` (not part of the frozen subject). Note for the probe: the grader reads **`/app/out.txt`** (not `output.txt` as in the round-83 capture), and `test_hello_file_exists` raises `AssertionError` while `test_hello_file_content` on a missing file raises `FileNotFoundError` — both are F per the frozen kill rule.

---

## E. How the round-83 probe executes the grader (for `ProbeR84` to mirror)

Source: `L/plans/round83_code_image_probe.py`.

**Exact bwrap argument vector** (`sandbox_argv`, lines 69-84, in order):

```
/usr/bin/bwrap
  --unshare-all  --die-with-parent  --new-session
  --ro-bind /usr /usr
  --ro-bind /etc /etc
  [--symlink <target> <link>]  for each of /bin /sbin /lib /lib64 that is a symlink on the host
  --proc /proc
  --dev /dev
  --bind <case_dir>/app  /app
  --dir /tests
  --ro-bind <capture>/test_outputs.py  /tests/test_outputs.py
  --ro-bind <case_dir>/harness.py      /harness.py
  --clearenv
  --setenv PATH /usr/bin
  --setenv LANG C.UTF-8
  --setenv LC_ALL C.UTF-8
  --chdir /app
  /usr/bin/python3 -I -B /harness.py
```

(Bwrap binary present and executable: `/usr/bin/bwrap`.)

**Harness** (the `HARNESS` string constant, lines 31-47, executed inside the sandbox):

```python
import ast, json, runpy
from pathlib import Path
path = "/tests/test_outputs.py"
names = [node.name for node in ast.parse(Path(path).read_bytes()).body
         if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]
module = runpy.run_path(path)
results = []
for name in names:
    try:
        module[name]()
    except (AssertionError, FileNotFoundError) as error:
        results.append([name, "F", type(error).__name__])
    except BaseException as error:
        results.append([name, "D", type(error).__name__])
    else:
        results.append([name, "P", ""])
print(json.dumps(results))
```

**Harness semantics that matter for the frozen kill rule:** the test list is discovered by `ast` from the *captured* bytes in source order (so `test_hello_file_exists`, then `test_hello_file_content`); `AssertionError`/`FileNotFoundError` ⇒ `F`; **any other exception ⇒ `D` (setup defect)**, which the caller turns into a hard failure, never a red witness; a normal return ⇒ `P`.

**Case staging** (`run_case`, lines 86-110): a fresh `tempfile.TemporaryDirectory(prefix="case-", dir=work)` per case; `case_dir/app/` is the `/app` bind; the staged file is written **inside** `case_dir/app/` (round-83 wrote `app/output.txt`; the round-84 analogue must write **`app/out.txt`**); `case_dir/harness.py` gets the harness text; the sandbox runs with `env={"PATH": "/usr/bin"}`, `timeout=60`, `capture_output=True`; a non-zero sandbox exit ⇒ `SetupDefect`; the JSON stdout must be a list of exactly `len(TESTS)` 3-element rows, in `TESTS` order, each verdict in `("P","F","D")` ⇒ else `SetupDefect("sandbox-protocol")`.

**Capture isolation** (`replay`, lines 112-133): the *checked* capture bytes are copied into a per-run temp file (`prefix="capture-"`) and that copy is what gets bound at `/tests/test_outputs.py`, so a concurrent lane edit cannot mutate the bytes under test. The probe then prints, per case, `CASE <id> predicted=<P/F>/<P/F> observed=<P/F>/<P/F>`, then `cases=8 mismatches=0`, then `PREDICATE R84-PROBE pass` (round-83's literal was `PREDICATE R83-PROBE pass`), and returns 1 on any mismatch.

**CLI**: `--lane DIR --work DIR` (both required), `--selftest`. **No receipt is minted by the probe** ("No receipt is minted here: integration must pin the landed tool and clean tip." — round-83 docstring lines 8-9); the receipt is minted by the L1 at integration.

**Constants to re-pin for R84** (round-83's, lines 22-27, as the template): `CAP` → `corpus/evidence/round52/graders/gcode-to-text/tests/test_outputs.py`; `SUBJECT_SHA` → `6b049dc626aa103b20d165552e5cb39ba02c6803b04ba06a43d79435b5f701a6`; `TABLE` → `plans/round84-cases.json`; `CASE_TABLE_SHA` → the L1's frozen digest; `TESTS` → `("test_hello_file_exists", "test_hello_file_content")`; `BWRAP` → `/usr/bin/bwrap`.

**Host pins** (measured on this host, matching the round-83 receipt's stamps at `corpus/evidence/round83/code-from-image-probe.txt:8-9`): `HOST_PYTHON` = `Python 3.14.8`, `HOST_OPENSSL` = `OpenSSL 3.6.5 29 Sep 2026 (Library: OpenSSL 3.6.5 29 Sep 2026)`.

---

## F. Gate registry checks for the knowledge entry — does repairing line 3 affect them?

Entry under repair: `L/corpus/knowledge/tb2-code-from-image-offline.md`. Current first three lines:

```
1  source: S267 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/code-from-image/tests/test_outputs.py :10-31; capture corpus/evidence/round52/graders/code-from-image/tests/test_outputs.py
2  verified-at: 2026-11-04 (round 83; frozen subject b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a)
3  recheck: python3 plans/round83_c1_replay.py --lane . --work DIR
```

Line 3 currently names **neither** an ISO date/cadence **nor** the pin ⇒ Q1 (date/cadence + action) and Q21 (pin or re-pin cadence) are both open, exactly as the claims state (`plans/round-84-claims.md:64-69`). Measured: this entry is one of the **11** entries the Q21 one-liner currently reports as `unpinned` (§F.1).

### F.1 Tests that read `corpus/knowledge/*.md`

| gate / check | file:line | what it reads | effect of repairing entry line 3 |
|---|---|---|---|
| **Q21 one-liner** | `L/corpus/QUALITY.md:237` (criterion) and `:246` (the executable one-liner) | `for f in corpus/knowledge/*.md; do grep -qE '^source:.*[0-9a-f]{40}' "$f" && ! grep -qE '^recheck:.*(commit|pinned|pin|[0-9a-f]{7})' "$f" && echo "unpinned $f"; done` | **Directly affected — and repaired.** The entry currently prints `unpinned corpus/knowledge/tb2-code-from-image-offline.md`; measured over all 77 knowledge entries the one-liner prints **11** unpinned entries, this one included. A repaired line 3 that names the pin (or a re-pin cadence containing `pin`) drops the count to **10** and removes this file from the list. Measured on a candidate line 3 — `recheck: 2026-11-04 (cadence 180d) re-pin at 2fd12b88aafdd04a52c298e3940bcb189f9766d6 -- python3 plans/round83_c1_replay.py --lane . --work DIR` — the Q21 predicate flips to satisfied (`unpinned? False`). **This is the criterion's own check command, not a separate lane gate**; the QUALITY prose figure "5 of 40" at `QUALITY.md:243-244` is a dated historical measurement (2026-10-25), not a live count and not to be edited. |
| **R63 trio gate** | `L/plans/round63_gate_checks.py:106-133` (`trio_missing`), used by `cmd_trio` (`:136-152`) and imported by `L/plans/round64_trio_sweep.py:84-88` | the first ≤12 lines of the entry, for the canonical order `source:` → `verified-at:` → `recheck:` | **Not affected, provided the repair keeps the three keys in that order on lines 1-3.** Measured: `python3 plans/round63_gate_checks.py trio corpus/knowledge/tb2-code-from-image-offline.md` prints `TRIO pass …` today, and with the candidate line 3 `trio_missing` is still `[]` (verified). The repair must not insert a `## ` heading above line 3 or reorder the keys, or `trio_missing` becomes non-empty and the entry flips to `TRIO-RED` in the sweep. |
| **R64 trio sweep** | `L/plans/round64_trio_sweep.py:84-140` (`KNOWLEDGE_DIR`, `RECHECK_RE`, `classify`) | every `corpus/knowledge/*.md` | **Not affected in substance.** The entry classifies `TRIO-OPEN` today (measured via `classify()` → `('TRIO-OPEN', '')`), and stays `TRIO-OPEN` after the repair, so the sweep's red set is unchanged. Note the sweep is already red at this tip for an unrelated reason: `python3 plans/round64_trio_sweep.py --sweep --lane .` prints `SETUP frozen-list-mismatch` (frozen 29-entry list vs 1 observed red) — a pre-existing base condition, not caused by R84. |
| **R75 index parity** | `L/plans/round75_c1_index_parity.py:120-134` (`census`), `:41-44` (`UNIVERSES`), `:53-56` (`README`), `:35-39` (`FIRST_CELL`, `EVIDENCE`) | the **file names** in `corpus/knowledge/`, `corpus/lessons/`, `corpus/evidence/` against `corpus/README.md` index rows | **Not affected by repairing line 3** — parity is over file *names*, not entry content. **But R84's new artefacts will need README rows**, measured in a scratch clone: adding `corpus/lessons/round-84.md` and `corpus/evidence/round84/` without README rows produces `MISSING lessons/round-84.md` and `MISSING-EVIDENCE round84`. The lane is **already** red at base for an unrelated row: `MISSING lessons/round-83-verifier-spotcheck.md` (measured at the real lane tip, `WORKTREE clean`). So the L1 should add the round-84 rows *and* decide on the pre-existing `lessons/round-83-verifier-spotcheck.md` gap. |
| **R52/R74 registry advertisement** | `L/plans/round74_c1_registry.py:60-107` (`self_assessment_files`), `L/plans/round52_c2_registry.py:44-55` | `corpus/knowledge/*.md` as *advertisement* sources (any `python3 <script>` mentioned) | **Not affected**, provided the repaired line 3 does not name a **new** `plans/…py` that is not registered. The current line 3 names `plans/round83_c1_replay.py`, which is registered (`L/SKILL.md:741`). If the repair instead names `plans/round84_c2_admission.py` (the natural successor, per the frozen claims), that script must exist **and** have a SKILL.md registry row, or R74/R52 print `MISSING <script>` (both currently `MISSING 0`). |
| **R28 corpus census** | `L/plans/round28_census.py:42-43` | the `knowledge/` index rows in `corpus/README.md` vs the files on disk | Not affected by a content-only repair; same README-row obligation as R75 for any *new* file. |
| **R30 kappa count** | `L/plans/round30_defects.py:118-121` | counts lines containing `kappa` in `corpus/knowledge/*.md` | Not affected: the entry contains **0** `kappa` lines (measured), so the repair must not introduce the word. |
| **R36/R52 entry-scoped checks** | `L/plans/round36_c2_verify.py:157-168` (`w4`: knowledge-file count vs `knowledge/` index rows), `L/plans/round52_c1_grader_audit.py:234` (globs `corpus/knowledge/tb2-*-grader.md`) | knowledge file counts; a glob over `tb2-*-grader.md` | Not affected: `tb2-code-from-image-offline.md` does **not** match `tb2-*-grader.md` (it ends `-offline.md`), so the R52 auditor does not read this entry. |
| **R78 class/member ledger** | `L/plans/round78_c1_class_member_ledger.py` | `corpus/knowledge/` not read; `SKILL.md` + `plans/grader-selected-members.json` only | Not affected (and retired, §A.1). |

### F.2 The Q13 leg — what `plans/gate_timing_check.py` actually requires (measured)

The claims' Q13 leg points at `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-84.md --commit REV` (exit 0). Requirements, read from `L/plans/gate_timing_check.py`:

- The lesson must have a `## Gate` section whose table has columns `candidate`, `decision`, `reason` (`parse_gate_admissions`, lines 144-197), and at least one row whose decision starts with `admit` (`is_admit`, lines 140-142). **The round-83 lesson's Gate table has different column names** (`id and decision | URL or own-work location | access date | located quote | reason / flip`, `L/corpus/lessons/round-83.md:10-12`) — it is *not* parseable as an admission table, which is exactly the R83-V1 gap. The R84 lesson's Gate table must use the `candidate | decision | reason` shape.
- The `reason` cell must cite the second-seat report **by repo-relative path** in a form `FULL_REPORT_RE` recognises: `.ufo/waves/round-<N>/<wave>/<name>.md` (lines 32-36) — and that wave directory must be a **second wave** for `is_second_wave` to accept it (lines 241-244: the directory must be `falsify` or match `wave[-_ ]?0*2`). **Measured in a scratch git fixture:** a Gate citing `.ufo/waves/round-84/w1/ScoutR84.md` ⇒ `FAIL … no cited, existing, returned second-seat report for this round`; the same Gate rewritten to cite `.ufo/waves/round-84/falsify/ScoutR84.md` (with a `falsify/swarm-registry.json` declaring the seat) ⇒ `PASS line 7 … existing returned second-seat report(s)` and exit 0. **So the R84 wave-1 report cannot satisfy the stock `gate_timing_check.py` Q13 leg by itself**; the L1 must either point the Gate at a second-wave-committed report path (as the sibling seat's draft counter already models — `.ufo/waves/round-84/w1/AdmitR84/round84_c2_admission.py` uses `GREEN_REASON = "second-seat re-read at \`.ufo/waves/round-84/falsify/FixtureReviewer.md\`"`, line 380) or implement Q13 in the R84 counter itself with the same identity rules.
- The cited report must be a non-empty regular file (`mode 100644`) in the **commit tree** (not the worktree), the seat must be in the committed wave registry with role ∈ `ALLOWED_REPORT_ROLES = {reviewer, scout, critic, sentinel, revenger}` (lines 24-26), the **candidate entry must carry a `writer:` line** (lines 55, 252-257, 350-351) that differs from the seat name and from the registry `agentId`, the report must name the candidate path, and it must carry an anchored `VERDICT:` line (`VERDICT_RE`, line 56). **Measured counterfactual:** removing the `writer:` line from the candidate in the fixture flips the verdict to `FAIL … candidate has no committed writer: field; self-review cannot be excluded`. The entry under repair (`tb2-code-from-image-offline.md`) has **no** `writer:` line today (its first three lines are `source:`/`verified-at:`/`recheck:`, then a blank, then the `# code-from-image:` heading) ⇒ the L1's repair must add one (and it must differ from the re-reading seat's id, e.g. `writer: KengakuR84`), otherwise Q13 cannot pass under the stock checker.
- `--commit REV` must be a revision in which the lesson **and** the cited report both exist; `gate_timing_check.py` reads the commit tree via `git ls-tree -rl` / `git show` (`main`, lines ~530-600).

**Bottom line for F:** a repaired line 3 (Q1/Q21) touches the Q21 one-liner's *output* (this file leaves the unpinned list, 11 → 10) and the trio checks stay green; it does **not** affect index parity, the R28 census, the R30 kappa count, the R36/R52 entry-scoped checks, or the R78 ledger. The Q13 leg is a separate requirement with three concrete preconditions the L1 must satisfy: a `candidate | decision | reason` Gate table in `corpus/lessons/round-84.md`, a `writer:` line on the repaired entry that differs from the reviewing seat, and a second-seat report path the checker can resolve in the commit tree.

---

## Frozen-element observations (reported, not edited)

1. **The `gcode-to-text` grader's first leg raises `AssertionError`, not `FileNotFoundError`** (`Path("/app/out.txt").exists()` + `assert`), while the second leg raises `FileNotFoundError` on a missing file. The frozen kill rule ("AssertionError or FileNotFoundError = F") covers both — no conflict. Flagged only so the probe's `D`-classification is not confused by an unexpected exception type.
2. **The frozen claims' counting outputs are confirmed exactly**: executed 27 → 28, unexecuted 61 → 60, file-artifact 19 of 76 → 20 of 76 (measured from the ledger + census, and reproduced end-to-end in a scratch clone where the R79 gate printed `executed=28 unexecuted=60`, `CLASS file-artifact k=20 n=76`, `DEFECTS n=0`, `PREDICATE R79-C1 pass`).
3. **Two pre-existing red gates at this tip are unrelated to R84** and must not be mistaken for R84 regressions: `plans/round63_gate_checks.py depth` (fails on `escape=/app/output.txt` and `unresolved=ledger=plans/grader-population-ledger.json`, i.e. the `L/SKILL.md:74` recipe cell's `/app/output.txt` token and the `ledger=` token at `L/SKILL.md:89`) and `plans/round75_c1_index_parity.py` (`MISSING lessons/round-83-verifier-spotcheck.md`). R84's own edits should not make either worse; the depth gate in particular will keep failing as long as `L/SKILL.md:74`'s recipe cell contains the absolute-path token `/app/output.txt` and `L/SKILL.md:89` contains the `ledger=…` token — **do not add new absolute-path or `ledger=`-shaped tokens to that section**.
4. **`gate_timing_check.py` will not accept a wave-1 report as Q13 evidence** (measured, §F.2). The claims' Q13 wording ("cites, by repo-relative path, a second-seat re-read report that exists in the admitting tree") is satisfiable, but the *stock* checker's second-wave rule means the cited path must live under a second-wave directory (`falsify`/`wave2`) with a committed `swarm-registry.json`. This is the single most likely integration trap for R84-C2 and is flagged for the L1 and the `AdmitR84` seat.

## Commands run (all read-only against the lane; no lane byte was written)

```
mkdir -p /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-84/w1/ScoutR84
mkdir -p /fast/scratch/hyaku/kengaku-r84/ScoutR84        (TMPDIR for every scratch run)
git -C <lane> status --porcelain | head                 -> only "?? .ufo/waves/round-84/"
git -C <lane> log --oneline -3 ; ls-files ; cat-file -t b12a9d4…  (read-only)
grep -n '19 of 76|executed 19|grader-population|round83-' <lane>/SKILL.md
grep -n -o -E '.{0,80}(19 of 76|executed 19|grader-population|round83-|executed 27|unexecuted 61|executed 28|20 of 76).{0,80}' SKILL.md
grep -n -E '^\| [a-z-]+ \| [0-9]+ \| executed [0-9]+ of [0-9]+' SKILL.md      (the 16 class rows)
python3 -c 'json.load(plans/grader-population-ledger.json) …'                (status/classes/verdict/subject census)
python3 -c 're/parse census CLASS lines vs ledger members'                    (88 = 88, class counts)
sha256sum corpus/evidence/round52/graders/gcode-to-text/tests/test_outputs.py
python3 plans/round79_c1_population_ledger.py --lane .            (read-only, in a scratch clone for the flip test)
python3 plans/round63_gate_checks.py depth --skill SKILL.md --receipt corpus/evidence/round62/class-survey.txt --root .
python3 plans/round63_gate_checks.py trio corpus/knowledge/tb2-code-from-image-offline.md
python3 plans/round64_trio_sweep.py --sweep --lane .
python3 plans/round75_c1_index_parity.py --lane .
python3 plans/round78_c1_class_member_ledger.py --lane .
python3 plans/round74_c1_registry.py --lane . ; python3 plans/round52_c2_registry.py --lane .
python3 plans/round82_c1_plans_registry.py --lane .
python3 plans/gate_timing_check.py --lesson corpus/lessons/round-84.md --commit <fixture-rev> --repo <fixture>   (×3 fixture variants)
git clone --shared <lane> <scratch>/clone   (deleted after the measurement)
```

No tool was installed or upgraded (nothing was missing; `bwrap`, `python3`, `openssl` are present).
