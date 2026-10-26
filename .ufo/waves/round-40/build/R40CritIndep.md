# R40CritIndep — independent recompute of the pinned `db-wal-recovery` grader (round 40, wave 1)

Seat: critic (leaf). Lane clone read-only at HEAD `3077adbc7145726519f60f01426a5d03381ad444`; the four executed
captures re-verified by digest before use (`test_outputs.py 88dc5c2a…`, `solve.sh ed8530c9…`, `main.db 68cb288e…`,
`main.db-wal.encrypted 68753bdc…`, all four `sha256sum` equal to the probe's `PINS`; `sha256sum -c SHA256SUMS` →
`8 × OK`). Nothing frozen was touched: no `plans/`, `corpus/`, ledger, registry or jj/Git state written; my writes are
this report plus `.ufo/waves/round-40/build/R40CritIndep/` and scratch (deleted at the end).

## Method, and the one independence limit stated up front

I derived each case's seven letters from the grader source alone — `test_recovered_json_exists` (L7-9),`_is_valid`
(L12-18), `_structure` (L21-35), `_sorted` (L44), `_completeness` (L53-80), `_no_duplicate_ids` (L89),
`_wal_was_decrypted` (L98-107) of `corpus/evidence/round40/tb2-db-wal-recovery/test_outputs.py` — plus the case
requirement text and the recipe/variant it names, and SQLite's documented handling of a WAL whose header magic is not
`377f0682/83` (treated as an empty WAL). **Limit:** the receipt was in the same read batch as the grader, so the 28-row
table below is a *recompute*, not a blind prediction; the 28/28 is therefore consistency evidence. The four extra cases
were predicted without any letter to copy and are the blind calibration.

## 1. Ground truth recomputed from the captures (not from the probe's `TRUTH`)

```
$ sqlite3 gt/base.db "select id,name,value from items order by id;"
1|apple|100   2|banana|200  3|cherry|300  4|date|400  5|elderberry|500
$ python3 -c 'xor 0x42' gt/full/main.db-wal ; sqlite3 gt/full/main.db "select id,name,value from items order by id;"
377f0682002de218  (header after XOR 0x42, len=16512)
1|apple|150  2|banana|250  3|cherry|300  4|date|400  5|elderberry|500  6|fig|600  7|grape|700
8|honeydew|800  9|kiwi|900  10|lemon|1000  11|mango|1100
wrong-key 0x43 header = 367e0783  (not a WAL magic → SQLite ignores the WAL)
```
5 base rows alone, 11 rows with the correct key, values `150/250` then `100×id` — the probe's `TRUTH` is right.
(Gotcha recorded for honesty: my first attempt passed key `42` decimal, giving `5f176eea…`; re-run with `0x42`.)

## 2. The 28 frozen cases: my letters, the receipt, and my own run

`driver.py` imports the **byte-identical copy** of the probe in scratch (`crit_probe.py`, sha256 `69af65df…`), grades
each end state twice in the probe's own bwrap sandbox, and compares against my `INDEP` table and against
`corpus/evidence/round40/db-wal-probe.txt`. It never consults the probe's `predicted` field for agreement.

| # | case | my letters | receipt | my run | why (grader cell) |
|---|------|-----------|---------|--------|-------------------|
|1|empty-app|FFFFFFF|same|same|no file → `FileNotFoundError` ×6|
|2|untouched|FFFFFFF|same|same|same|
|3|oracle-solve-sh|PPPPPPP|same|same|oracle XOR 0x42 + rw extract → 11 rows|
|4|base-only-ro|PPPPFPF|same|same|5 rows: L53 len≠11, L98 `>5`|
|5|plain-read-then-solve|PPPPFPF|same|same|rw open drops the bad WAL; oracle still writes 5 rows|
|6|xor-wrong-key|PPPPFPF|same|same|header `367e0783` ≠ magic → 5 rows|
|7|decrypt-then-extract|PPPPPPP|same|same|11 rows|
|8|decrypt-checkpoint-truncate|PPPPPPP|same|same|11 rows|
|9|decrypt-in-place-no-json|FFFFFFF|same|same|no file|
|10|literals-never-open-db|PPPPPPP|same|same|only ids, values 1-2, names 3-11 are pinned; db never read|
|11|literals-names-1-2-wrong|PPPPPPP|same|same|names of ids 1-2 unpinned (L64-65 pin only values)|
|12|literals-id3-name-wrong|PPPPFPP|same|same|L70 pins name of id 3|
|13|truth-value-float-id1|PPFPPPP|same|same|L35 `isinstance(150.0,int)` F; `150.0==150` elsewhere|
|14|truth-reversed-order|PPPFFPP|same|same|L44, then L58|
|15|truth-plus-duplicate-id11|PPPPFFP|same|same|L53 len 12, L89|
|16|truth-dup-id10-no-id11|PPPPFFP|same|same|L58 (`ids≠1..11`), L89|
|17|truth-extra-field|PPPPPPP|same|same|L30 is `issubset`, not equality|
|18|truth-wrapped-object|PFFFFFF|same|same|L17; dict iteration yields str keys → L33/`TypeError`, L53, L89, L98|
|19|truth-ids-as-strings|PPFFFPP|same|same|L33; lexicographic L44; L58; wal test skips (keys are str)|
|20|truth-ids-as-floats|PPFPPPP|same|same|L33 only; `1.0==1` in L44/L58/L89/L105|
|21|truth-trailing-garbage|PFFFFFF|same|same|`json.load` JSONDecodeError|
|22|truth-wrong-path|FFFFFFF|same|same|no file at the path|
|23|empty-list|PFPPFPF|same|same|L18; vacuous loop; L53; L98|
|24|truth-drop-id11|PPPPFPP|same|same|L53 len 10|
|25|truth-value-id3-wrong|PPPPPPP|same|same|value of id 3 unpinned|
|26|truth-bool-value-id5|PPPPPPP|same|same|`isinstance(True,int)`; value 5 unpinned|
|27|truth-name-null-id1|PPFPPPP|same|same|L34; name of id 1 unpinned, wal pins only value 1|
|28|truth-value-string-id4|PPFPPPP|same|same|L35; value 4 unpinned|

```
$ python3 driver.py      # 28 graded cases + 4 extras, each graded twice
indep_vs_observed 28/28 indep_vs_receipt 28/28 observed_vs_receipt 28/28
recompute of the grader's pinned cells: ids 11 + values 2 + names 9 = 22 of 33
```
Receipt reproduced independently, twice:
```
$ python3 crit_probe.py --lane $S/lane --work $S/w > p1.txt   (again > p2.txt)
cmp p1.txt p2.txt                                  → two probe runs byte-equal
cmp p1.txt corpus/evidence/round40/db-wal-probe.txt → my probe output byte-equal to frozen receipt
```
So `cases=28 observed_pass=8 observed_fail=20 mismatches=0` and `regrade cases=28 differ=0` stand, and the receipt is
deterministic across runs, hosts-invariant in the ways it claims (no path/timing lines).

## 3. My own extra cases (predicted blind, then run)

Built against truth recomputed in §1, with my own generators (no `mk.py` variants reused).

| extra | end state | my prediction | observed | consequence |
|-------|-----------|---------------|----------|-------------|
| x1 `bool-id1` | id of row 1 written as JSON `true` | PPPPPP**P** | PPPPPPP | **passes 7/7**: `isinstance(True,int)` is True (L33), `True==1` in L44/L58, and `1 in id_to_item` matches the `True` key (hash equality) in L105 — a non-integer id is graded correct |
| x2 `nan-value-id1` | id 1 value `NaN` | PPFPFPF | PPFPFPF | L33 F; L105 `nan==150` F; L64 F — **and L12-18 passes**, i.e. the "valid JSON" test accepts the non-RFC `NaN` literal |
| x3 `symlink-recovered` | truth at `/app/out/recovered.json`, `/app/recovered.json` a symlink to it | PPPPPPP | PPPPPPP | L9 `os.path.exists` follows symlinks: existence is "a readable thing at that path", not "a created regular file" |
| x4 `bom-truth` (supplementary) | truth prefixed with UTF-8 BOM `EF BB BF` | PFFFFFF | PFFFFFF | `json.load` raises `JSONDecodeError: Unexpected UTF-8 BOM` — an agent that writes `utf-8-sig` is graded 1/7 |

Extra calibration: **3/3 required extras and 4/4 including the supplementary one matched**, including the two
non-obvious calls (bool id passes though float id fails; NaN passes the validity test but fails completeness and the
WAL test).

## 4. What my recompute adds to the frozen headline observations (no contradiction)

Confirmed exactly as the freeze states: 22 of 33 cells pinned (11 ids + 2 values + 9 names; the 11 unpinned cells are
values of ids 3-11 and names of ids 1-2), hand-typed JSON that never opens the database passes 7/7 (case 10), "Fix the
WAL file" is never checked (cases 10-11, 25-26 pass while `fix-wal` is violated), the rw-open trap costs the oracle two
tests (case 5 `PPPPFPF`), wrong-key XOR leaves 5 rows (case 6), `True` passes as an int value (case 26), floats fail only
the structure test (case 20), an extra field passes (case 17).

New, from the extras:
1. **A boolean id passes all seven** (x1). `record-format` is enforced only to "`isinstance(int)`", and bool is an int
   subclass; `sorted` and the id-list equality both accept it. Not covered by any frozen case (case 26 covers only
   `value`).
2. **The "valid JSON" test is not a JSON-validity test** (x2): `json.load` accepts `NaN`/`Infinity` literals. An entry
   that says "the grader requires valid JSON" would overstate; it requires "what `json.load` accepts".
3. **`json-at-path` is existence-tested, not file-tested** (x3): a symlink (or any readable object at the path) passes.
4. **Encoding fragility** (x4): a BOM turns a correct answer into 1/7 — a grader-side false negative, not an escape.

Two **tagging traps** for whoever admits extras into the probe (they would corrupt V7 if copied verbatim):
- x3's end state *satisfies* the instruction (`json-at-path`), so it must carry **no** `violates=` tag. I tagged it
  `json-at-path` in my driver only as a probe of the test; admitting it with that tag would wrongly turn a label
  `enforced → partly`.
- x2's `NaN` violates `record-format` (a value must be an integer), which it does carry — so it adds a fail, not a pass,
  and cannot flip the label. x1 legitimately carries `record-format` and adds a pass; `record-format` stays `partly`
  either way (already 2 passers, case 17 and case 26). x4 may carry `json-at-path` (unreadable at that path) and keeps
  that label `enforced`.

## 5. Expected V7 requirement map (precomputed, so the entry can be checked against it)

Derived by the counter's stated rule (label from **all** receipt cases carrying the tag) over the frozen dry table:

```
fix-wal        cases=23 pass=5 label=partly     (literals-never-open-db, literals-names-1-2-wrong, truth-extra-field,
                                                 truth-value-id3-wrong, truth-bool-value-id5)
extract-all    cases=15 pass=4 label=partly     (literals-never-open-db, literals-names-1-2-wrong,
                                                 truth-value-id3-wrong, truth-bool-value-id5)
json-at-path   cases= 5 pass=0 label=enforced
record-format  cases= 8 pass=2 label=partly     (truth-extra-field, truth-bool-value-id5)
sorted-by-id   cases= 1 pass=0 label=enforced   (single carrying case — thin, but the rule says enforced)
eleven-records cases=10 pass=0 label=enforced
```
If `corpus/knowledge/tb2-db-wal-recovery-grader.md` labels any row differently, that is a V7 defect, not a judgement
call. (At my clone HEAD the entry, S119 and S120 are absent — `SOURCES.md` ends the S-series at S118 — which is the
expected wave-1 floor, not a defect.)

## 6. Impacted axes and correction

- **coverage / calibration (C2):** the grader class is characterised more sharply (22/33 cells; three type-escape
  hatches; one encoding false negative; the "valid JSON" and "path" tests are weaker than their names). These are
  *additions* to the frozen headline list; nothing in the receipt, dry table, probe or counter needs to change, and no
  frozen byte was touched.
- **Impact on C1:** none (different surface; I did not read the counters).
- **Smallest safe correction:** none to frozen files. If the L1 wants the extras admitted later, add them as new probe
  cases with the tagging fixed per §4 and a fresh freeze — not as an edit to the frozen table. The entry's prose should
  say "`json.load`-parseable", "a readable object at the path", and "a boolean is accepted where an int is required"
  rather than "valid JSON", "file created", "integer id".

## 7. Evidence index

- `.ufo/waves/round-40/build/R40CritIndep/driver.py` (sha256 `511fd4a0…`), `driver.out` (`c8f098c6…`), `p1.txt`
  (`c74c6b91…`), `crit_probe.py` (`69af65df…` = byte-identical to `plans/db_wal_probe.py`).
- Commands: `sha256sum` on the four captures; `sha256sum -c SHA256SUMS` (8 OK); the two xor/sqlite ground-truth reads in
  §1; `python3 crit_probe.py --lane $S/lane --work $S/w` twice + `cmp` against the frozen receipt; `python3 driver.py`
  (28 + 4 cases, each graded twice); the V7 label computation in §5.
- Scratch `/fast/scratch/hyaku/kengaku-r40/R40CritIndep` removed before finishing; no lane file written, no git/jj
  mutation, no package installed.

VERDICT: indep-agree-28/28-extra-3/3
