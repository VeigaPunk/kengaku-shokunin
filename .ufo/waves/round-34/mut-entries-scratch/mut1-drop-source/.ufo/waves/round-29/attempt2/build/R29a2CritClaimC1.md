# R29a2CritClaimC1 — attack on C1's predicate and counter

Seat: `L1Kengaku29.R29a2CritClaimC1` (adversarial critic, leaf). Scope: claim **C1** and
`plans/adoption_check.py` only. C2 (`plans/sources_adopt.py`) touched only where it is a
second parser of the same registry (A12).
No production file was created, edited or deleted. No tool installed or upgraded.
All probes ran on copies under `/tmp/r29a2-critclaimc1/` (transient); every command and its
literal output is inlined below so the evidence survives detachment.

**Revision note.** `plans/adoption_check.py` was edited by another seat *while this review ran*
(`8c14a5d` blob `51b7b4f` → working tree `ee34914c847879fc…`). The per-attack sections are
measured against the frozen revision; the section **"SUPERSEDING RE-RUN"** re-runs every attack
against the patched file and states which gaps survive. Do not read A5/A8/A12/A13/A14 as open
without reading that section.

Tree state during probing: `git status --porcelain corpus plans` was clean at probe start;
mid-run a sibling wrote `corpus/knowledge/benchmark-task-validity-checklist.md`
(`?? corpus/knowledge/benchmark-task-validity-checklist.md`), so live-tree numbers moved
(`entries=1 indexed=0`). Every attack below is therefore measured on the counter itself with
pinned inputs, not on the sibling's in-flight bytes.

## Axes

1. **Soundness** — can the counter reach exit 0 without the claimed work?
2. **Discriminating power** — does the do-nothing control fail the gamed trees as well as the empty tree?
3. **Predicate fidelity** — does the code enforce the sentence C1 freezes?
4. **Operability** — does the frozen command, as written, run at all?
5. **Single parsing authority** — does the counter parse the registry the way census/C2 claim to?

## Object under test, pinned line numbers (`plans/adoption_check.py` @ `8c14a5d`)

```
33  ROW_RE = re.compile(r"^( {0,3})\|[ \t]*(S[0-9]{3,})[ \t]*\|")
34  SOURCE_LINE_RE = re.compile(r"^source:[ \t]*(S[0-9]{3,})\b", re.MULTILINE)
44      cells = raw.rstrip()[1:-1].split("|")
75          if f"| `knowledge/{name}` |" in readme:
77          if f"verified-at: {access_date}" in text:
79          cited.update(SOURCE_LINE_RE.findall(text))
82  rows_mined = sum(1 for row_id in cited if row_id in registry and registry[row_id][7] == "mined")
88              if cells and rel in cells[10]:
90                  break
93      census_code = 0
96              [str(CENSUS), "validate", "--root", str(lane.parent), lane.name],
101         census_code = proc.returncode
112         and rows_present == len(cited)
113         and rows_mined == len(cited)
116         and census_code == 0
```

Sanity of the column contract: a real mined row parses to 11 cells, `cells[7]='mined'`,
`cells[10]='corpus/lessons/round-29.md, corpus/knowledge/webarena-config…'`
(`S076` in `corpus/SOURCES.md`). Indices 7/10 are correct for flush rows.

---

## A0 — control receipt reproduces (baseline, not an attack)

```
$ cd …/kengaku-shokunin && python3 plans/adoption_check.py \
    --expect .ufo/waves/round-29/attempt2/adoption-expect.json
entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 verified_at=0 census=skipped
exit=1
```
Byte-identical to `.ufo/waves/round-29/attempt2/control.nothing.txt` (line 3). The do-nothing
tree fails. **Verdict: receipt honest, for the property it measures.**

## A1 — fabricated tree via `--lane` (no committed bytes, real work bypassed)

Built `/tmp/r29a2-critclaimc1/fake/corpus/{SOURCES.md,README.md,knowledge/benchmark-task-validity-checklist.md}`
with five hand-written 11-cell rows (`mined`, used-by naming the entry), a README row, and an
entry whose five `source:` lines say *"fabricated line, never opened"*. No quote, no opening.

```
$ python3 counter.py --lane fake --expect expect.json
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=skipped
exit=0
$ python3 counter.py --lane fake --expect expect.json --census
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=ok
exit=0
```

The census dimension is satisfied **by the fabricated tree**:
```
$ scripts/sources-census.sh validate --root /tmp/r29a2-critclaimc1 fake --verbose
ERROR: config not found: /tmp/r29a2-critclaimc1/shokunin.conf
fake	ok	/tmp/r29a2-critclaimc1/fake/corpus/SOURCES.md
census exit=0
```
`grep -c git plans/adoption_check.py` → `0`. The module docstring's "It reads only committed
corpus files" is not implemented and not checkable from the code.
**Verdict: gameable.** Gap: line 62 reads `lane/…` from an arbitrary `--lane`; nothing binds
`--lane` or the expect file to a revision, and census passes a tree with no `shokunin.conf`.

## A2 — zero citations pass vacuously (denominator is self-supplied)

Same fixture, entry reduced to front matter + prose, no `source:` line:

```
entries=1 indexed=1 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=1 verified_at=1 census=skipped
exit=0
```
`cited` is empty at line 67/79, and lines 112–113 compare `rows_present`/`rows_mined` to
`len(cited)` → `0 == 0`. **Verdict: gameable.** Gap: the target is `rows_* == len(cited)`
instead of a set derived from `expect["sources"]` (or a frozen count of 5).

## A3 — README "index" is a substring, not a table row

`fake3` README replaces the inventory row with a Frontier bullet plus an HTML comment:
`<!-- future row: | \`knowledge/benchmark-task-validity-checklist.md\` | x | -->`
```
entries=1 indexed=1 … census=ok
exit=0
```
Line 75 is an unanchored `in readme`. **Verdict: gameable on placement** (comment, prose,
wrong section, "unopened leads" table). The *identity* is not substitutable: the check keys on
`Path(rel).name`, so a row for an unrelated file does not satisfy `indexed` (tested in A9).

## A4 — duplicate row: first/last-wins override

`fake4b` appends a second `S077` row at file end with `status=mined`, after a `queued` original;
`registry_rows` overwrites (`rows[match.group(2)] = …`, line 47) so last-wins:
```
$ … (no --census)  entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=skipped
exit=0
$ … (--census)     … rows_mined=5 … census=fail
exit=1
```
**Verdict: gameable only while `--census` is off.** That is the same mode the control used
(`census=skipped` in `control.nothing.txt`), because line 93 defaults `census_code=0` and line
116 then reads "skipped" as pass. Closed with the flag, open without it.

## A5 — `used-by` on one of five rows is enough

`fake5b`: S077 carries the entry path in `used-by`; S078/S079/S080/S090 carry `—`.
```
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=ok
exit=0
```
Lines 86–90 `break` after the first hit, and census's `W03 mined row with used-by = —` is a
warning that "do[es] not affect clean lanes" (`scripts/sources-census.sh:30`).
**Verdict: gameable even with the frozen command.** Gap: `usedby_ok == len(entries)` is
satisfied by one row; C1's sentence says all five rows carry `used-by` naming the entry.

## A6 — `verified-at` anywhere in the file

`fake6`: no front matter; the string `verified-at: 2026-10-25` sits inside a fenced block
labelled "old draft note", all five ids cited as bare fabricated lines.
```
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=ok
exit=0
```
Line 77 is an unanchored substring. **Verdict: gameable.** The code cannot distinguish
"re-opened today" from "wrote today's date".

## A7 — the expectation file is the whole gate, and it is unpinned

`expect_gamed.json` points the same counter at a **prior** entry and a **prior** access date:
`{"access_date":"2026-10-21","entries":[{"path":"corpus/knowledge/webarena-config-projection.md","sources":["S070","S076"]}]}`
Run against the **committed lane tree** (no edits):
```
$ cd /home/vgpnk/Projects/shokunin && python3 kengaku-shokunin/plans/adoption_check.py \
    --lane kengaku-shokunin --expect /tmp/r29a2-critclaimc1/expect_gamed.json --census
entries=1 indexed=1 cited_rows=1 rows_present=1 rows_mined=1 usedby_ok=1 verified_at=1 census=ok
GAMED-EXPECT exit=0
```
Zero new work, zero new rows, exit 0 with `census=ok`. Nothing pins `adoption-expect.json`
(`grep -n 'adoption-expect\|sha256' .ufo/waves/round-29/attempt2/package-gate.txt` → no match;
`grep -c sha256 package-gate.txt` → `0`; `build-validation.txt` is 0 bytes), `expect["round"]`
and `expect["attempt"]` are read by nobody, and `access_date` is never checked against a fixed
date. **Verdict: gameable.** Gap: the claim's target is only as good as a mutable JSON file the
counter treats as ground truth.

## A8 — five ids on one `source:` line count as one cited row

`fake8`: entry line `source: S077 S078 S079 S080 S090`, registry holds **only S077**.
```
entries=1 indexed=1 cited_rows=1 rows_present=1 rows_mined=1 usedby_ok=1 verified_at=1 census=ok
exit=0
```
`SOURCE_LINE_RE` (line 34) captures one id per line, and the corpus already writes citations
this way: for `corpus/knowledge/webarena-config-projection.md` the counter reports
`cited_rows=1` while the single `source:` line names S070,S071,S072,S073,S074,S075,S076.
**Verdict: gameable even with `--census`.** All five ids can be visibly cited in the entry while
four registry rows are simply absent.

## A9 — path escape + README row for a file that does not exist

`fake9`: entry moved to `plans/benchmark-task-validity-checklist.md`, the knowledge copy deleted,
README still carrying `| \`knowledge/benchmark-task-validity-checklist.md\` | fabricated |`.
```
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=0 verified_at=1 census=fail
exit=1
```
`indexed` was fooled (phantom row for a nonexistent path) but the exact-rel used-by join
(line 88, `rel in cells[10]`) refused. **Verdict: path escape closed by the used-by string join;
the phantom README row is real but not sufficient.** The entry must exist and be named verbatim.

## A10 — `verified-at` prefix laxity

`fake10`: `verified-at: 2026-10-25T00:00:00Z-stale-clone` → `verified_at=1`, exit 0 with census ok.
No boundary at line 77. **Verdict: gameable, low value** (needs a sloppier date, not a forgery).

## A11 — one appended row suffices; the cited id can be an old row

Real-corpus mirror (`cp -r corpus`), then: append **one** row `S077` (`mined`, used-by = entry),
add the README row, and write an entry that cites `source: S001` (an already-mined contamination
paper) and says in prose *"the other four claimed ids do not exist"*.
```
entries=1 indexed=1 cited_rows=1 rows_present=1 rows_mined=1 usedby_ok=1 verified_at=1 census=skipped
ONE-ROW+UNRELATED-CITE exit=0
```
**Verdict: gameable.** The five-row measurement collapses to one real row plus one recycled
citation; `rows_mined == len(cited)` never asks for S078/S079/S080/S090.

## A12 — the counter's row parser contradicts the census and C2 (false red, duplicate authority)

Rows indented by 1 space match `ROW_RE` (`( {0,3})`, line 33) but `raw.rstrip()[1:-1]` (line 44)
slices off the indent *and* the leading pipe, giving 12 cells, so line 45 drops the row:
```
flush  : ROW_RE_match=True cells=11 first=' S077 ' idx7=' mined '
1-space: ROW_RE_match=True cells=12 first=''       idx7=' — '
$ python3 counter.py --lane fake5 --expect expect.json
entries=1 indexed=1 cited_rows=5 rows_present=0 rows_mined=0 usedby_ok=0 verified_at=1 census=skipped
exit=1
```
Census, on the *same* tree, counts and mines them:
```
$ scripts/sources-census.sh validate --root /tmp/r29a2-critclaimc1 fake5
fake5	ok	/tmp/r29a2-critclaimc1/fake5/corpus/SOURCES.md        (rc=0)
$ scripts/sources-census.sh census --root /tmp/r29a2-critclaimc1 fake5
fake5	rows	5
fake5	status.mined	5
```
Census accepts 0–3-space rows by contract (`sources-census.sh:39-40`), and C2's frozen
requirement 1 exists precisely because "a column-zero-only pattern false-greens an indented
collision" — yet C1's own parser silently discards indented rows. **Verdict: false red /
divergent third parser.** A row set that census calls clean makes the counter report zero rows.

## A13 — the frozen target command cannot produce `census=ok` (BLOCKER, operability)

The claim's target command is run from the lane root. The counter then spawns
`[CENSUS, "validate", "--root", <lane.parent>, lane.name]` (line 96) with cwd inherited from the
lane; census resolves a bare lane name against **cwd**:
```
$ cd …/kengaku-shokunin && scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku-shokunin
ERROR: unknown lane (not a dir, not in conf or root): kengaku-shokunin
rc from lane cwd=2          ← also "unknown lane", not 0
$ cd /home/vgpnk/Projects/shokunin && scripts/sources-census.sh validate --root . kengaku-shokunin
kengaku-shokunin ok … census exit=0
```
So the frozen line `python3 plans/adoption_check.py --expect … --census` run as written yields
`census=fail`, exit 1, **whatever the corpus contains**. Reproduced on the live tree while the
entry already existed: `entries=1 indexed=0 … census=fail`. With `--lane kengaku-shokunin` from
the parent directory the same tree gives `census=ok`.
**Verdict: the target is unreachable exactly as frozen.** Two effects: (i) the round cannot report
the frozen line honestly; (ii) a seat that "fixes" it by dropping `--census` lands A4/A2 green.

## A14 — the frozen target string is not what the counter prints

Claim line 27 freezes
`entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok`
but line 104–107 always prints an extra field before `census`:
`… usedby_ok=1 verified_at=1 census=ok`. The frozen string is not a contiguous substring of any
output (A1b, A5, A8, A13 all show `verified_at=1` intervening), and the only consumer of the
string is the claim's own prose (`grep -rn cited_rows` outside the counter → `plans/round-29-attempt2-claims.md:27` only).
**Verdict: documentation defect; "prints exactly" is false as frozen.**

---

# SUPERSEDING RE-RUN — working tree `ee34914c847879fc…` (counter patched by another seat mid-review)

`git status` flipped `M plans/adoption_check.py` while this review ran. All verdicts above are
against the frozen revision `8c14a5d` (blob `51b7b4f`). The working tree now carries:
`required = sum(len(entry["sources"]))` with `len(cited) == required` and `rows_* == required`;
`usedby_ok` as an `all(...)` over the entry's sources (no `break`); `body = raw.strip()` before
the cell split (indent fix); a `-shokunin` suffix strip for the census lane name; and a print
without `verified_at`. Every fixture was re-run against a pinned copy of that revision.

The frozen command, as written from the lane root, now returns the frozen target **exactly**:

```
$ python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok
exit=0
```

| attack | frozen `8c14a5d` | tree `ee34914c` | state |
|---|---|---|---|
| A1 fabricated `--lane` tree | exit 0 | exit 0 | **OPEN** |
| A2 zero-cited entry (frozen expect) | exit 0 | exit 1 | closed |
| A2'' nothing cited **and** `sources: []` | (would pass) | **exit 0** | **OPEN** (residual) |
| A3 README row inside an HTML comment | exit 0 | exit 0 | **OPEN** |
| A4 duplicate `mined` row last, no `--census` | exit 0 | exit 0 (exit 1 with `--census`) | **OPEN without the flag** |
| A5 one-of-five `used-by` | exit 0 | exit 1 | closed |
| A6 `verified-at` in a fenced block | exit 0 | exit 0 | **OPEN** |
| A7 tuned gamed expect (prior entry) | exit 0 | **exit 0** | **OPEN** |
| A8 five ids on one `source:` line | exit 0 | exit 1 | closed |
| A10 `verified-at` prefix (`…25T00:00:00Z-stale-clone`) | exit 0 | exit 0 | **OPEN** |
| A11 one row + unrelated cite | exit 0 | exit 1 | closed |
| A12 1-space-indented rows | `rows_present=0`, exit 1 | `rows_present=5`, exit 0 | closed |
| A13 frozen command from lane cwd | `census=fail`, exit 1 | `census=ok` | closed — with a new fragility |
| A14 extra `verified_at` field | mismatch | exact 7-field line | closed |

Re-run evidence for the OPEN rows (pinned copy of `ee34914c`, `--census` unless noted):

```
fake     entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok   exit=0   # A1
fake3    … cited_rows=5 … census=ok                                                          exit=0   # A3
fake4b   … census=fail exit=1  |  --census omitted: census=skipped                            exit=0   # A4
fake6    … verified-at inside ``` old draft note ```                                          exit=0   # A6
fake10   verified-at: 2026-10-25T00:00:00Z-stale-clone                                        exit=0   # A10
fake11 + expect_empty.json  entries=1 indexed=1 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=1 census=ok  exit=0   # A2''
$ cd /home/vgpnk/Projects/shokunin && python3 kengaku-shokunin/plans/adoption_check.py \
    --lane kengaku-shokunin --expect …/expect_gamed2.json --census     # {"access_date":"2026-10-21","path":"…/webarena-config-projection.md","sources":["S070"]}
entries=1 indexed=1 cited_rows=1 rows_present=1 rows_mined=1 usedby_ok=1 census=ok   exit=0   # A7
```

What the repair did **not** change, and why each still matters:

- **A1/A7 share one root gap: the denominator is still caller-supplied.** `required` is computed
  from `expect["sources"]`, and `--lane`/`--expect` are arbitrary paths. A tuned expectation plus a
  prior entry passes on the committed tree with zero new work (A7 evidence above). `required` is a
  better denominator than `len(cited)`, but it is pinned to nothing.
- **A2'' is the floor case of the same gap**: `sources: []` → `required=0`, `cited=∅` passes
  `len(cited)==required`, and `all(())` is `True`, so `usedby_ok=1`. Nothing encodes the frozen 5.
  Smallest fix: `required = sum(...)` must equal a frozen `expect["cited_floor"]` (5), or reject an
  empty `sources` list outright.
- **A3/A6/A10 are unchanged substring checks** (README `in readme`; `verified-at: {date} in text`).
  They remain the cheapest places to put a phrase without the artefact.
- **A4** is closed by the census flag only; `census_code` still defaults to `0`, so a run without
  `--census` still treats "skipped" as pass — the mode the frozen control receipt used.
- **A13's new fix is a directory-name heuristic**: it strips `-shokunin` and hopes the remainder is
  a conf/root lane. Verified failure mode — a lane dir `foo-shokunin` (not in any conf) now gets
  `census=fail`, exit 1, while the same bytes at `foo` give `census=ok`, exit 0. The node is not
  wrong today (`kengaku` is a conf lane) but it turns a path into a name. Smallest correction:
  pass the absolute path — `[str(CENSUS), "validate", "--root", str(lane.parent), str(lane)]` was
  verified rc 0 from the lane cwd.

Effect on the round's own data: the landed bytes do satisfy the strict reading as well — all five
rows `S077,S078,S079,S080,S090` are `mined` with `used-by =
corpus/knowledge/benchmark-task-validity-checklist.md`, the entry has five `source:` lines and
`verified-at: 2026-10-25` (8563 B), and `corpus/README.md:64` carries the inventory row. The laxity
was not exercised this round; the point is that the gate could not have told if it had been.

---

## Predicate vs code (frozen `8c14a5d`; post-repair state in the right-hand note)

| C1 sentence | Enforced at | Same condition? | at `ee34914c` |
|---|---|---|---|
| frozen command prints *exactly* the 7-field line | 104–107 | **No** — 8 fields (A14) | now exact |
| … and exits 0 | 109–118 | yes, but cheaply (A1/A7) | still cheap (A1/A7) |
| object under test is `corpus/knowledge/benchmark-task-validity-checklist.md` | 69–72 via expect | mechanically, but expect is unpinned (A7) | unchanged |
| "citing exactly S077 S078 S079 S080 S090" | 34, 79, 112–113 | **No** — any/zero set, supersets, one id per line (A2, A8, A11) | count pinned to `expect["sources"]`, so still only as exact as the expect file (A2'', A7) |
| the five rows appended with `status=mined` | 82 | only for ids the entry actually cites (A8/A11) | count now compared to `required` |
| `used-by` naming the entry | 86–90 | **No** — one of five, `break` (A5) | now `all(...)` — fixed |
| entry carries access date `2026-10-25` | 77 | substring anywhere, prefix lax (A6, A10) | unchanged |
| ≤25-word located quote per source, re-opened | — | **not enforced at all** | not enforced |
| kill rule: no substitute row to reach target | — | **not enforced**; counter cannot see intent | not enforced |
| control: do-nothing ⇒ exit 1 | A0 | true, but see below | true |

## Is the control discriminating?

Partly, and not for the reason claimed.

1. It separates *nothing written* from *bytes written* (A0). It does **not** separate
   *re-grounded* from *fabricated*: A1/A3/A6 pass with rows and prose that were never opened,
   because the counter has no notion of a quote, a location, or an opening.
2. It was run **without** `--census` (`control.nothing.txt:3` ends `census=skipped`) while the
   target command includes `--census`. The control therefore never exercises the dimension the
   target freezes — at the frozen revision it would have recorded `census=fail` had the flags
   matched (A13), and today it leaves a duplicate-row tree (A4) passing.
3. It cannot detect the strongest attack (A7): it used the frozen expect, and the receipt records
   no `sha256` of `adoption-expect.json`, so a swapped expect is indistinguishable afterwards.
4. Its `base 1f3b0f1…` label is a corpus revision, not a tool revision:
   `git cat-file -e 1f3b0f1ec41ec297130e8944ff97968d32324632:plans/adoption_check.py` → exit 128;
   the counter first exists at `8c14a5d`. The receipt cannot be re-derived "at base" with the
   committed tool; it is a working-tree run against base corpus bytes.
5. Net: the control is a valid *empty-tree* control and not a control for the two properties the
   claim actually needs (grounding, and committed-vs-supplied bytes). A discriminating control
   would be a second receipt run against a fabricated lane (A1) with the same flags, expected to
   exit 1 — today it exits 0.

## Smallest safe corrections — status after the mid-review repair

Landed in the working tree (`ee34914c`) by another seat: 1 (as a suffix heuristic, not the path
form), 3 (count pinned to `expect["sources"]`), 4, 8, 9. Still open: 2, 5, 6, 7, plus the residual
floor from 3 and the fragility in 1.

1. **(operability, A13) — LANDED, but as a name heuristic.** The tree strips `-shokunin` and
   passes the remainder. Correct today (`kengaku` is a conf lane) and wrong off-fleet: a lane dir
   `foo-shokunin` not in any conf yields `census=fail`, exit 1, while the same bytes at `foo` yield
   `census=ok`, exit 0 (verified). Prefer the absolute path —
   `[str(CENSUS), "validate", "--root", str(lane.parent), str(lane)]`, verified rc 0 from the lane
   cwd — which needs no name convention.
2. **(soundness, A4/A2) — OPEN.** `census_code` still defaults to `0`, so `census=skipped`
   satisfies the `census_code == 0` conjunct; A4's duplicate-row tree passes with the flag omitted.
   Default it to `1`, or require `--census`, and record the receipt with the same flags as the
   target.
3. **(soundness, A2/A8/A11) — PARTLY LANDED.** `required = sum(len(entry["sources"]))` and
   `len(cited) == required` are in. The residual is the floor: `sources: []` ⇒ `required=0` and
   `all(())` is `True`, so an entry citing nothing passes (A2'', exit 0, `census=ok`). Require
   `required == 5` from a frozen `expect["cited_floor"]`, or refuse an empty `sources` list. Line
   34 still captures one id per `source:` line; with the count pinned to five that now costs a
   false red on the corpus's own multi-id style (`webarena-config-projection.md` reports
   `cited_rows=1` for a line naming seven), so `findall` is the matching half of this item.
4. **(soundness, A5) — LANDED.** `all(...)` over `entry["sources"]`; `fake5b` now `usedby_ok=0`, exit 1.
5. **(soundness, A3) — OPEN.** `f"| \`knowledge/{name}\` |" in readme` is unanchored; a README
   HTML comment satisfies it (`fake3`, exit 0, `census=ok`). Anchor to a line and to the inventory
   section.
6. **(soundness, A6/A10) — OPEN.** `verified-at: {access_date}` is still a substring; a fenced
   "old draft note" (`fake6`) and a prefixed value `…25T00:00:00Z-stale-clone` (`fake10`) both
   pass. Anchor to `^verified-at: …$`.
7. **(soundness, A7) — OPEN, and this is the one that matters.** The expect file is still the
   whole gate and still unpinned: a tuned expectation naming the prior entry and the id it really
   cites exits 0 on the committed tree (`expect_gamed2`, `census=ok`). Emit `expect_sha=<sha256>`
   in the line and record the same hash beside the control receipt, so a swap shows up in a diff.
8. **(duplicate authority, A12) — LANDED.** `body = raw.strip()`; `fake5` now reports
   `rows_present=5`, matching census's `rows 5 / status.mined 5`.
9. **(fidelity, A14) — LANDED.** The print is the frozen seven fields and the frozen line is now
   reproduced byte-for-byte.

With 1,3,4,8,9 landed the frozen target is reachable and the round's own bytes satisfy the strict
reading. What the counter still cannot do is tell a caller-supplied tree from the lane's committed
one (A1/A7), and that is the difference between a gate and a calculator. Items 2 and 7 are the
cheap closers: one default and one hash.

## What is not gameable (stated for symmetry)

- Entry identity: the used-by string join (line 88) requires the literal `rel`, and a phantom
  README row plus an entry outside `corpus/knowledge/` fails (A9).
- A cited row that is `queued`/`rejected` fails `rows_mined` (line 82) — verified by A4's first
  variant (`rows_mined=4`, exit 1).
- Absent entry / absent README row fail `present`/`indexed` (A0, and the live mid-flight tree
  printed `indexed=0` with the entry already written).
