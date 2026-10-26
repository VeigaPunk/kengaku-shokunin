# R36ScoutMergePkg — merge/kengaku re-screen (round 36, wave 1)

Seat: scout, read-only. Source `/home/vgpnk/Projects/shokuknow/merge/kengaku/` was only read (no write; the probe ran from a `/tmp` copy). Lane files untouched; scratch in `/tmp/k36-scoutpkg-ELom` (copied evidence in `.ufo/waves/round-36/build/R36ScoutMergePkg/`).

**Theme (one):** executed Toolathlon comparison-function fixture probes ("predicate input types"). It is adjacent to C2: both execute a pinned benchmark grader offline with typed fixtures. C2 is one TB2 task; this is a second benchmark and 16 functions.

Axes (Godspeed): (a) duplication against held ground, (b) id/registry collision, (c) un-opened sources, (d) number reproduction. Cheap axes (a)(b) ran first. The expensive axis (d) was spent on the entry that survived them.

## 1. Verdicts

| Package entry (staged rows) | Verdict | Reason (measured) | Flip condition |
|---|---|---|---|
| `grader-predicate-input-types.md` (S143, S144) | **ADMIT-CANDIDATE, conditional, not for round 36** | Not a duplicate (§2). No registry collision (§3). The round-7 numbers reproduce exactly (§4). It carries three defects that must be repaired in the text before landing (§5). Round 36's claims are frozen to C1 and C2, so landing it needs a claim that names it. | (i) a round-37 claim re-opens S143/S144; (ii) the three §5 defects are corrected; (iii) rows are renumbered past S110 (proposal S111/S112); (iv) the probe script and a lane-side receipt are re-homed into the lane; (v) it lands as a dated amendment, or as a new file with an index row (see §6). |
| `grader-fixture-probe-stage3.md` (S170, S171) | **REFUSE** | It is the interim state of a lineage that its own later entries supersede. It reports no discrimination verdict: 3 of 4 `fixture-rejected` and 1 of 4 `exec-failed`. The staged stage-4 entry (`spreadsheet-grader-fixtures.md`, S180–S182) says "all four spreadsheet graders now discriminate". Admitting stage 3 would put a superseded negative in front of a reader. The lineage also contradicts itself (§7). | Re-admit only as a folded history paragraph inside a reconciled amendment of A1 that resolves the §7 contradiction. Never as a standalone entry. |

## 2. Duplication against held ground — none

`corpus/README.md` index and coverage bullets (`grep -n -i 'toolathlon\|grader' corpus/README.md`):
- `knowledge/benchmark-grader-semantics.md` (README:67, S093/S103/S104) reads one Toolathlon task, `ab-testing`, statically.
- `knowledge/tb2-protein-assembly-grader.md` (README:68, S105–S107) executes one TB2 task.
- `knowledge/benchmark-verifier-execution-model.md` covers Harbor's runner.
- `grep -rln "fixture probe\|comparison function" corpus/knowledge` → no file.

No held entry executes Toolathlon comparison functions or states their input types. `ab-testing validate_task_completion` appears in A1's "not attempted" list as "checks a real cloud storage bucket". That is compatible with the held entry, which read it statically.

## 3. Registry collision — none

Live registry: `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → `100`, ids S001–S107. S108–S110 are reserved by C2. Staged S143/S144 are free ids, but must be renumbered past S110. I propose S111/S112; the L1 decides.

Gate dry-run into `/tmp`, nothing written to the lane:

```
$ python3 plans/sources_adopt.py --registry corpus/SOURCES.md --package <pkg>/SOURCES.append.md \
    --admit-ids S143,S144 --entries corpus/knowledge/grader-predicate-input-types.md \
    --access-date 2026-10-25 --recheck 180d --attest-opened --scope-to-admit --out $T/block.md
registry=100 staged=173 collisions=0 malformed=0 duplicates=0 defects=0 prose=1
wrote .../block.md rows=2        (exit 0)
```

Without `--attest-opened` the gate reports `missing: S143:not-opened-this-round`. I opened the pinned sources myself (§4) and the staged rows carry `opened 2026-10-24`, so the L1 must re-date them to 2026-10-25.

The gate-normalised S144 `recheck` cell still reads `on-commit — python3 lanes/kengaku/round7/toolathlon-grader-fixture-probe.py --fetch --src-dir /tmp/keng-toolathlon-src (ran 2026-10-24)`. That path is relative to the source repo and does not resolve in the lane. The lane has 0 rows pointing into shokuknow (round-35 scout measured it). Re-homing is the open condition (iv).

## 4. Sources the lane has not opened, and my own reproduction

The lane holds no Toolathlon row other than S103 (`ab-testing`). Every function A1 cites sits in a source file the lane has not opened. I opened the sources below myself on 2026-10-25 (curl, pinned commit `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`):

| Staged row | Source URL (opened) | Located quote (<=25 words) | Location |
|---|---|---|---|
| S143 | https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/yahoo-analysis/evaluation/main.py (sha256 `02ec4bda…078058`, 388 lines) | `def compare_rating(rating, stock_result):` | line 9 |
| S143 | same | `start = stock_result['start']` | line 42 |
| S143 | same | `results[horizon] = price > start` | line 50 |
| S143 (added; A1 cites it but S143 does not) | https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/sync-todo-to-readme/evaluation/main.py | `submission_todos: List[Tuple[str, int, str]],` | line 127 (`def compare_todos(` at 126) |
| S143 (added) | https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/oil-price/evaluation/main.py | `def _compare_summary(expected: List[Dict], actual: List[Dict]) -> List[str]:` | line 618 |
| S143 (added) | https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/add-bibtex/evaluation/main.py | `"""Check whether an agent entry contains the normalized ground-truth data."""` | line 81 (`def entries_match(entry1, entry2):` at 80) |
| S171 (refused row, opened only to check stage 3) | https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/academic-pdf-report/evaluation/main.py | `from .task_utils import compare_names, compare_titles, check_affiliation_requirements` | line 11 (`def check_filled_excel(excel_path, expected_data):` at 28) |

S144 is own-work. The probe is `lanes/kengaku/round7/toolathlon-grader-fixture-probe.py`. I copied it to `/tmp` and re-ran it:

```
$ python3 toolathlon-grader-fixture-probe.py --fetch --src-dir /tmp/k36-scoutpkg-ELom/src
exit=0   ## Counts - discriminates: 16 of 16   (Wall time: 70.51 seconds)
## Not attempted (no hermetic fixture): 10 lines
```

The 16 rows match the round-35 scout's re-run. The "Not attempted" list has 10 entries, which equals the A1 text ("Ten candidates"). The breakdown in A1 (3 game-statistics, 3 `.xlsx`, 2 buckets, 1 csv, 1 workbook) matches the list. Output saved at `.ufo/waves/round-36/build/R36ScoutMergePkg/out7.txt` (sha256 prefix `c251b4b3`).

## 5. Defects in A1 that must be repaired before landing

1. **Overclaim, contradicted by its own S144 table.** A1 says the functions take "grade strings plus price dicts, … none of which a bare string satisfies", and the S143 `teaches` cell says "never bare strings". The round-7 table (`out7.txt`, "real input type" column) lists 6 of 16 functions that take plain strings. They are `compare_tables` (two markdown texts), `model_label_matches`, `compare_websites`, `similar`, `is_station_name_match` and `stock_codes_match`. All six `discriminate`. The round-6 negatives for those six cannot be explained by "needs a non-string type". The finding should narrow to: several functions need structured types, and the round-6 shapes did not match the domain.
2. **Denominator 38 versus 37.** A1 repeats "23 of 38 as uncallable" and "9 of 13". The round-6 summary table says `of 38 candidates` (`round6/toolathlon-grader-behaviour-probe.md:35-39`), but its per-candidate record (`:86` on) has 37 rows. I counted them in Python: `37 Counter({'no-callable-shape': 23, 'ok': 13, 'exec-failed': 1})`, and 13+23+1=37. This confirms the round-35 scout's R2 finding. The entry must state 37 or name the 38th candidate.  The summary's own 4 discriminating + 9 non-discriminating = 13 `ok` rows is consistent.
3. **`compare_rating` narrative is unsupported.** A1 says round 6 "read the resulting `None` as 'no discrimination'". The round-6 per-candidate row reads `| yahoo-analysis | compare_rating | ok | str | False | False | False |` (`:126`), not None. The round-6 probe script is not in `lanes/kengaku/round6/` (only the .md), so the claim cannot be re-derived. State it as unreproduced, or drop it.

Smaller notes:
- S143 cites only `yahoo-analysis`, but A1 names types from at least 8 other graders (compare_todos, `_compare_summary`, entries_match and others). Add S143-style located quotes for the functions the prose names, as in §4, or cite only the table.
- The grader-semantics entry's tolerance caveat does not interact: A1 never claims tolerances.
- A1's phrase "every function that could be made hermetic discriminates" is true only of the 16 functions listed. It does not extend to the unattempted 10.

## 6. Landing constraints against the round-36 counters

- C1 (`round36_c1_verify.py`) builds its battery from round-35 bytes and reads the lane tree only for untracked files and the nested-path count. C2's W4 is `knowledge files == index rows >= 43`, not a literal. Either landing shape, a dated amendment or a new file plus an index row, therefore passes both counters, provided S111/S112 are inserted inside `## Registry` (the round-35 E12 constraint) and the `recheck` cell is a cadence.
- The claims file freezes round 36 to C1 and C2. A1 is a third deliverable, so it is out of scope for round 36 unless the L1 opens a claim for it. The round-35 lesson row at `corpus/lessons/round-35.md:19` set exactly this flip ("a round-36 claim that re-opens S143/S144"), and no round-36 claim does.
- Do not bulk-append: the package still has 24 id collisions with S001–S107 (round-35 scout §1). Only the two rows above pass the gate, via `--scope-to-admit`.

## 7. Stage-3 refusal detail

- Stage-3 artefact (`round9/toolathlon-grader-fixture-probe3.md`): `exec-failed 1 of 4`, `fixture-rejected 3 of 4`. Its own text says "The four functions still have **no discrimination verdict**". That is a measurement of the fixture and the environment, not of the graders.
- The staged stage-3 entry's claim that `check_filled_excel` "fails to import … relative import" is true of the source (line 11 `from .task_utils import …`, §4). That is a harness fact, not a grader fact, and the stage-4 entry already supersedes it ("must be imported as a member of a synthetic package").
- Lineage inconsistency to resolve before any admission of the cluster. `spreadsheet-grader-fixtures.md` says all four graders discriminate, "26 of the lane's 26 … all 26 discriminate", and in its scope paragraph "Ten grader functions … remain unattempted". `grader-sheet-checks-real-pandas-r16.md` says the three `nvidia-market` sheet checks could not be exercised because the import chain ends in the `openai-agents` SDK, and that "the coverage figure should still read as every comparison function carrying a measured verdict except these three". The stage-4 4-of-4 claim and the r16 negative cannot both stand. I did not install pandas or re-run stages 8–16; they stay unverified, not refuted.
- The wider lineage (`grader-fixture-coverage.md`, `grader-candidate-*`) is not screened beyond the two requested; the round-35 scout's cluster verdict (fold into A1 as amendments) remains untested here. I recommend holding it until A1 lands.

## 8. Other themes checked

Nothing else in the 65-entry package fits C2/PROVINCE better than A1 and stage 3. The CJK, contamination, card, OSF and post-5G entries stay out of theme and are not re-screened. The round-35 refusals (`toolathlon-grader-contract` denominators, `terminal-bench-release-identity`, grader-semantics/verifier/task-validity filename collisions) were not re-examined and are neither confirmed nor reversed.

## 9. Evidence ledger

| Claim | Command | Output |
|---|---|---|
| Round-7 probe reproduces | `python3 toolathlon-grader-fixture-probe.py --fetch --src-dir …/src` (from a `/tmp` copy) | `exit=0`, `discriminates: 16 of 16`, 10 "Not attempted" |
| Pinned yahoo source | `curl -fsSL …/yahoo-analysis/evaluation/main.py; wc -l; sha256sum` | 388 lines, `02ec4bda…078058`; lines 9, 42, 50 as quoted |
| Round-6 per-candidate rows | python count over `round6/toolathlon-grader-behaviour-probe.md` after the last `| task` header | `37 Counter({'no-callable-shape': 23, 'ok': 13, 'exec-failed': 1})`; summary denominators `of 38` |
| Strings-only functions | `awk` over round-7 table, "real input type" column | 6 of 16 take two plain strings (listed in §5.1) |
| Gate dry-run | `sources_adopt.py … --admit-ids S143,S144 … --scope-to-admit` | `registry=100 staged=173 collisions=0 malformed=0 duplicates=0 defects=0 prose=1`; `rows=2`; without `--attest-opened`: `missing: S143:not-opened-this-round` |
| Live registry size | `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` | 100 (S001–S107) |
| No held duplicate | `grep -rln "fixture probe\|comparison function" corpus/knowledge` | no matches |
| Source repo untouched by me | I wrote only under `/tmp` and the lane build dir | no write into shokuknow (its tree already shows unrelated modified `.ufo` files from other work) |

Not verified: stage 3 run (needs pandas via `uv`), stages 8–16 probes, and the round-6 probe script (absent from the source repo).

VERDICT: package-1-admit-1-refuse-0-hold
