# ScribeLesson — draft decision-table note for the grader class `serialization-schema`

Seat ScribeLesson (leaf scribe). Draft only; the L1 integrates. Nothing here is committed
by me. The lane was read-only.

## Where the note goes

`SKILL.md:60` opens `## Decision table — grader class → offline replay recipe`; the table
header is at `SKILL.md:68-69`:

```
| class | count | executed | replay recipe | receipt pointer |
```

The `serialization-schema` row is `SKILL.md:84`. Its four cells today:

| cell | text |
|---|---|
| class | `serialization-schema` |
| count | `10` |
| executed | `executed 6 of 10 (round 86 adds \`raman-fitting\`; round 85 adds \`sqlite-db-truncate\` to round 40's \`db-wal-recovery\`)` |
| replay recipe | `the candidate's structured output is parsed by the grader itself from the sandbox filesystem (its JSON parse of the recovered file), so the probe stages the input state and the recovery recipe and lets the grader do the parsing.` |
| receipt pointer | `\`corpus/evidence/round40/db-wal-probe.txt\`, \`plans/db_wal_probe.py\`` |

**The note is a cell-level amendment, not a new table.** The class row already carries the
class's shape; what round 95 adds is a second member of the class whose *report schema*
differs from the round-40 member's, so the row needs to say what that schema is and which
of its edges are decisive. That belongs in the `replay recipe` cell (it is a statement
about how the grader parses) plus the `receipt pointer` cell (the row's own convention:
the class row lists the receipt of each member it counts — see `file-artifact` at
`SKILL.md:74`, whose pointer cell lists eight receipts across five rounds).

**Count check first.** The `executed` cell must match the ledger exactly, or the
lane's own gate reds. Measured at the measured tip T `afe9c229…`:

```
$ python3 plans/round79_c1_population_ledger.py --lane .
LEDGER rows=88 executed=39 unlocated=0 unexecuted=49
CLASS serialization-schema k=6 n=10
PREDICATE R79-C1 pass
```

and the ledger's own member row for this member
(`plans/grader-population-ledger.json`, read at T) is:

```json
"fix-code-vulnerability": {"classes": ["file-artifact", "serialization-schema"],
  "round": 95, "status": "executed", "receipt": "corpus/evidence/round95/vuln-probe.txt",
  "subject": "tb2-header", "verdict": "cases", "reason": "replayed"}
```

So `executed 6 of 10` is already correct at T — the round-95 flip of this member is
already in the class cell, and the class cell needs **no count edit**. The class is
`file-artifact` too: the same ledger row carries both classes, and the `file-artifact`
cell at `SKILL.md:74` likewise reads `executed 30 of 76` with this member counted in it.
**The count is right; the note adds what the class row still does not say.**

## What the class row still does not say (measured)

The `serialization-schema` row names its members only as a count
(`round 86 adds \`raman-fitting\`; round 85 adds \`sqlite-db-truncate\``). It says
nothing about:

1. **this member's report schema** — `fix-code-vulnerability` grades a JSONL *report*
   (`/app/report.jsonl`), not a single JSON *file* like round 40's `db-wal-recovery`
   (`/app/recovered.json`). The class recipe cell says "the candidate's structured output
   is parsed by the grader itself from the sandbox filesystem (its JSON parse of the
   recovered file)" — the round-40 member's shape. Round 95's is JSONL, one object per
   line, and the grader parses **every** line.
2. **which of its edges are decisive** — the class recipe cell names no edge at all.
3. **the round-95 receipt** — the pointer cell lists only round 40's receipt and script.

## Proposed text

### Amendment A — the `replay recipe` cell (replaces the cell at `SKILL.md:84`)

```
the candidate's structured output is parsed by the grader itself from the sandbox filesystem (its JSON parse of the recovered file), so the probe stages the input state and the recovery recipe and lets the grader do the parsing. Round 95 adds `fix-code-vulnerability`, whose graded artefact is a JSONL *report* at `/app/report.jsonl` — one JSON object per line, each with `file_path` and `cwe_id` — and the grader parses every line of it with `json.loads`, so the report's own shape decides the grade: `test_vul_file` collects `file_path` per line and asserts `/app/bottle.py` is among them, and `test_cwe_id` lowercases every `cwe_id` and asserts `cwe-93` is among those filed under `/app/bottle.py`. The edges that decide that shape are C06 (the id is case-folded, so `CWE-93` passes), C07 (a relative `file_path` raises `KeyError` in `test_cwe_id` rather than failing an assertion), C08 (a bare-string `cwe_id` is iterated character by character, so `cwe-93` is never a member), C09 (two lines for one `file_path` are concatenated before the membership test), C10 (a trailing blank line is `json.loads`-ed and raises `JSONDecodeError` in both parsing tests) and C14 (an integer `cwe_id` stringifies to `93`, not `cwe-93`).
```

### Amendment B — the `receipt pointer` cell (replaces the cell at `SKILL.md:84`)

```
`corpus/evidence/round40/db-wal-probe.txt`, `plans/db_wal_probe.py`; `corpus/evidence/round95/vuln-probe.txt`, `plans/round95_vuln_probe.py`
```

### Companion — the `file-artifact` row (`SKILL.md:74`), same receipt, same reason

This member is in **two** classes: the ledger row reads
`"classes": ["file-artifact", "serialization-schema"]`, and the `file-artifact` cell at
`SKILL.md:74` counts it too (`executed 30 of 76`). That row's `receipt pointer` cell
lists the round-40 receipt and the rounds 83–88 receipts but **not** round 95's, and its
`replay recipe` cell describes materialising output files rather than this member's
JSONL report. The receipt-pointer cell is the same one-clause addition:

```
`corpus/evidence/round40/db-wal-probe.txt`, `plans/db_wal_probe.py`; `corpus/evidence/round83/code-from-image-probe.txt`; `corpus/evidence/round84/gcode-to-text-probe.txt`; `corpus/evidence/round85/sqlite-db-truncate-probe.txt`; `corpus/evidence/round86/raman-fitting-probe.txt`; `corpus/evidence/round87/mteb-retrieve-probe.txt`; `corpus/evidence/round88/fix-git-probe.txt`; `corpus/evidence/round95/vuln-probe.txt`, `plans/round95_vuln_probe.py`
```

**I do not propose a `replay recipe` edit to the `file-artifact` row.** That row's recipe
cell already describes a class whose members materialise output files in the sandbox and
lets the grader read them — which is true of this member too (`/app/bottle.py` is a file
the grader reads; the report is a second file the grader reads). The JSONL report
schema is the `serialization-schema` row's business, and putting it in both rows would
duplicate it. One class's row carries the schema; both rows carry the receipt.

## The `executed` cell: no edit is required, and the parenthetical's omissions are not a defect

The count is correct and machine-checked, so **no count edit is required**. The
parenthetical does not name round 95:

```
executed 6 of 10 (round 86 adds `raman-fitting`; round 85 adds `sqlite-db-truncate` to round 40's `db-wal-recovery`)
```

I checked whether that is a defect and it is **not**. The parenthetical is a *partial*
provenance list in this table, and the class has executed members from six rounds while
the parenthetical names three:

| round | member | named in the parenthetical? |
|---|---|---|
| 40 | `db-wal-recovery` | yes |
| 85 | `sqlite-db-truncate` | yes |
| 86 | `raman-fitting` | yes |
| 90 | `merge-diff-arc-agi-task` | **no** |
| 92 | `llm-inference-batching-scheduler` | **no** |
| 95 | `fix-code-vulnerability` | **no** |

Rounds 90 and 92 were omitted by the same convention, and `file-artifact` at
`SKILL.md:74` names seven of the twenty-six rounds its members come from. So round 95's
absence is the house convention, not an omission this round introduced.

**The optional edit, if the L1 wants round 95 visible** (a prose edit inside the counted
cell, so it must keep the `executed <k> of <n>` prefix the ledger gate parses —
`plans/round79_c1_population_ledger.py:80`,
`CELL = re.compile(r"^executed\s+(\d+)\s+of\s+(\d+)(?:\b|$)")`):

```
executed 6 of 10 (round 95 adds `fix-code-vulnerability`; round 86 adds `raman-fitting`; round 85 adds `sqlite-db-truncate` to round 40's `db-wal-recovery`)
```

**I recommend the L1 take it** — not because the row is wrong, but because this class
gained a member whose report schema differs from every other member's (JSONL report vs
a single JSON file), and the parenthetical is where a reader learns which member is
which. It is a one-clause prose addition, the count is untouched, and the gate stays
green. **I do not claim the row is wrong; I claim the addition is useful.**

### One thing the L1 should know about this row's history

The `serialization-schema` cell read `executed 3 of 10` at the freeze commit F and reads
`executed 6 of 10` at the measured tip T — a jump of **three**, for a round that
admitted **one** member of the class. The same is true of `file-artifact`
(`24 of 76` → `30 of 76`) and of nine other class cells: the C commit resynced the
whole table against the ledger, because the table had drifted.

Measured, at the tip (`receipts/receipt-class-cells-F-vs-T.txt`):

```
at F d9cd18a7519a… : CLASS serialization-schema k=5 n=10 cell=executed 3 of 10
                      DEFECT CLASS-K-MISMATCH serialization-schema cell=3 of 10 ledger=5 of 10
                      (and 9 further CLASS-K-MISMATCH lines; 14 DEFECTS total, PREDICATE R79-C1 fail)
at T afe9c229e37a… : CLASS serialization-schema k=6 n=10 cell=executed 6 of 10
                      DEFECTS n=0   PREDICATE R79-C1 pass
```

This is **declared** work, not a surprise: `plans/round-95-claims.md:114` — "The legacy
`plans/round79_c1_population_ledger.py` repair (round-94 routed defect 5) lands as
conformance with its before/after counts in the report, not as a claim" — and the lane's
own receipt `.ufo/waves/round-95/L1/legacy-r79-gate.txt` records the before (14 DEFECTS,
rc 1) and after (0 DEFECTS, rc 0) counts. I flag it only because a reader comparing the
two class cells across F and T will see `3 → 6` and wonder whether round 95 admitted
three members of the class. It admitted one; the other two were the drift being fixed.

**Consequence for this note:** the `executed` cell's *count* is now right, so my note
below touches only the two prose cells. The count edit is the optional parenthetical
clause, and nothing else.

## Every fact in the proposed text, with its source

| claim | source |
|---|---|
| graded artefact is `/app/report.jsonl`, one JSON object per line | `corpus/evidence/round95/graders/fix-code-vulnerability/tests/test_outputs.py:16,26-31,40-43` — `report_path = Path("/app/report.jsonl")`, `for line in f: item = json.loads(line)` in both parsing tests |
| each object has `file_path` and `cwe_id` | same file `:44` `item.get("cwe_id", [])`, `:43` `item.get("file_path", "")` |
| `test_vul_file` collects `file_path` per line and asserts `/app/bottle.py` among them | same file `:26-32` |
| `test_cwe_id` lowercases every `cwe_id` and asserts `cwe-93` among those filed under `/app/bottle.py` | same file `:45` `cwe_ids = [str(cwe_id).lower() for cwe_id in cwe_ids]`, `:47-50` merges by `file_path`, `:52` `assert "cwe-93" in report["/app/bottle.py"]` |
| C06 `CWE-93` passes (id case-folded) | `plans/round95-cases.json` case C06 (`report=upper-cwe`, predicted `P,P,P,P,P,P`); observed `P,P,P,P,P,P` in `corpus/evidence/round95/vuln-probe.txt` |
| C07 relative `file_path` raises `KeyError` in `test_cwe_id` | case C07 (`report=relative-path`, predicted `P,F,E:KeyError,P,P,P`); observed identically. The `KeyError` comes from `report["/app/bottle.py"]` at `:52` when no line carried that key (the report's key was `bottle.py`) |
| C08 bare-string `cwe_id` iterated character by character | case C08 (`report=string-cwe`, predicted `P,P,F,P,P,P`); observed identically. `str(cwe_id).lower() for cwe_id in cwe_ids` at `:45` iterates the *string* `cwe-93` into its characters |
| C09 two lines for one `file_path` concatenated before the membership test | case C09 (`report=split-lines`, predicted `P,P,P,P,P,P`); observed identically. `:47-50` `report[file_path] = report[file_path] + cwe_ids` |
| C10 trailing blank line raises `JSONDecodeError` in both parsing tests | case C10 (`report=trailing-blank-line`, predicted `P,E:JSONDecodeError,E:JSONDecodeError,P,P,P`); observed identically. `json.loads(line)` at `:28` and `:42` on the empty final line |
| C14 integer `cwe_id` stringifies to `93` | case C14 (`report=int-cwe`, predicted `P,P,F,P,P,P`); observed identically. `:45` `str(cwe_id).lower()` on the int `93` |
| the member is `serialization-schema` and `file-artifact` | `plans/grader-population-ledger.json` at T |
| its receipt is `corpus/evidence/round95/vuln-probe.txt` | same ledger row; the file exists and its `MEMBER fix-code-vulnerability` line is at `:2` |
| its probe is `plans/round95_vuln_probe.py` | `corpus/evidence/round95/vuln-probe.txt:7` `TOOL_SHA 932e66b1e476…` = the frozen-table sha256 of `plans/round95_vuln_probe.py` (`plans/round-95-claims.md` row 1) |

## Why these six edges and not the others

The class is about *report schema*, so the note names the edges that move the report's
**shape or typing**, and leaves the edges about the *code fix* alone. The nine code-side
edges of this member are C01 (solve), C02 (do-nothing), C03 (report only), C04 (patch
only), C05 (oracle), C11 (only `_hkey` patched), C12 (a fix that strips instead of
raising), C13 (an over-strict fix) and C15 (a package `/app/bottle/` shadowing
`/app/bottle.py`) — none of them is a report-schema edge, and none belongs in a
`serialization-schema` note. C15 is worth one sentence of its own to the L1: it is the
edge where the grader's *import* of `bottle` resolves to a different file than the file
the report names, so it is an edge about which artefact is graded rather than about the
report's shape; it belongs in a `file-artifact` note, not here.

## Honest limits

- The edge descriptions above are read from the **captured grader bytes** and the
  **committed probe receipt**, both frozen at T. They are not re-measured by this seat:
  this seat ran the census (receipt `census-t3.txt`) but not the C1 probe, whose fifteen
  cases each take a bwrap sandbox. The observed vectors quoted here are the committed
  ones at `corpus/evidence/round95/vuln-probe.txt`.
- The note describes the *class row*, not a new per-grader decision table. The lane has
  per-grader sections for rounds 37–44 (`## Database-recovery TB2 grader — round 40` and
  its `### Decision table — what the grader reads, and what passes it`,
  `SKILL.md:1201-1203`), but no round-95 section exists and creating one is a bigger
  change than the task asks for. If the L1 wants the full house-style per-grader table
  for this member, the case table gives the material and I have laid out which columns
  it would need.
