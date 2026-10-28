# C1ExecReadFindings — wave 1, kengaku round 52 (R52-C1, novelty)

**Seat**: `C1ExecReadFindings` (executor) · **wave**: 1 (build) · **lane**: `kengaku-shokunin`
**Base tip named in the claims**: `30801b479e3418c11089b8586178b6960216f364`; lane `master` HEAD at read time
was `07ea2084053f5112ea797a653e6a3a96e8cf4a64` ("round-52: amendment A1 (per-test classification + hardened
CONFIRMED leg) with disclosure receipt"), which **includes Amendment A1** to `plans/round-52-claims.md`. I read
the claims file in full including A1; nothing in it changes this seat's scope.

**Item delivered**: read the lane's 12 hand-read TB2 grader entries and extract, per task, the lane's own recorded
finding in one line — what the grader actually checks, the vacuity/weakness class the lane found, and the exact
`file:line` anchor it cites — into a machine-readable
`read-findings.json` (`task` → `{task, checks, weakness, anchor, source_entry}`).

---

## 1. What I did

1. Read `plans/round-52-claims.md` in full (frozen claims + Amendment A1).
2. Listed `corpus/knowledge/tb2-*-grader.md` — **12 files**, matching the claims file's corroborating count
   (`ls corpus/knowledge/tb2-*-grader.md | wc -l` → 12).
3. Read **all 12 entries in full**, including their `## Findings`, `## Negative space`, `## Prior art` and
   `## Errata` sections (the errata narrow or correct several findings; the reported weakness class below is the
   **post-erratum** statement).
4. For each entry, extracted: the graded surface ("what the grader actually checks"), the lane's own weakness/vacuity
   class wording, and the exact `file:line` anchor the entry cites for that weakness.
5. Verified each extracted anchor string actually occurs in its source entry (grep over all 12 files).
6. Verified all 12 task ids are members of the frozen population `plans/round52-tasks.json` (89 tasks, pin
   `2fd12b88aafdd04a52c298e3940bcb189f9766d6`).
7. Verified every `source_entry` path exists in the lane tree, and that the lane's **capture** of the file each
   anchor points into is digest-green (`sha256sum -c SHA256SUMS` in all 12 capture directories → 96 files `OK`,
   0 failures).
8. Wrote `read-findings.json` (scratch), validated its shape, and copied it into this seat's wave report dir.

I did **not** read, fetch or classify any grader bytes — that is the C1 instrument's job and other seats'. This
seat's product is the lane's *own recorded* findings, quoted/attributed, not a re-derivation.

---

## 2. Exact commands run

```sh
# population / entry inventory
ls /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/tb2-*-grader.md
python3 -c "import json; d=json.load(open('/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round52-tasks.json')); print(d['pin'], d['repo'], d['task_count'], d['capture_file_count'])"

# anchor verification (one grep over all 12 entries, one alternation per anchor)
#   pattern: (test_outputs\.py:(73-102|27|18|30|122|135|64|16|25|70|13|90))
#   path:    <lane>/corpus/knowledge/tb2-<task>-grader.md  (12 paths, ';' separated)

# capture digest check, one per entry (lane-root relative)
cd corpus/evidence && for d in round35/tb2-eval round36/tb2-regex-log round37/tb2-git-webserver \
  round38/tb2-build-pmars round39/tb2-git-leak-recovery round40/tb2-db-wal-recovery \
  round41/tb2-constraints-scheduling round42/tb2-circuit-fibsqrt \
  round43/tb2-feal-differential-cryptanalysis round44/tb2-feal-linear-cryptanalysis \
  round45/tb2-password-recovery round46/tb2-polyglot-c-py; do
  (cd "$d" && sha256sum -c SHA256SUMS | grep -c ': OK$'); done

# sha256 of the captured grader file each anchor points into
sha256sum corpus/evidence/round42/tb2-circuit-fibsqrt/test_outputs.py   # 6117b8ed…
sha256sum corpus/evidence/round35/tb2-eval/test_outputs.py              # 44a05a24…
sha256sum corpus/evidence/round37/tb2-git-webserver/test_outputs.py    # 526aee3d…

# JSON shape + membership validation (scratch, python3 3.14.8)
python3 - <<'PY'
import json
d=json.load(open('/fast/scratch/hyaku/kengaku-r52/C1ExecReadFindings/read-findings.json'))
assert len(d)==12
for k,v in d.items():
    assert set(v)=={'task','checks','weakness','anchor','source_entry'}
    assert v['task']==k
pop=json.load(open('/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round52-tasks.json'))['tasks']
assert all(k in pop for k in d)
PY
```

No tool was installed or upgraded for this seat (nothing needed one beyond `python3` 3.14.8 already on the host);
no pacman transaction was attempted. No git/jj mutation of any kind was run (`git rev-parse`/`git log`/
`sha256sum` reads only).

---

## 3. Measured numbers

| quantity | measured |
|---|---|
| hand-read TB2 grader entries found | **12** (`corpus/knowledge/tb2-*-grader.md`) |
| entries extracted into `read-findings.json` | **12 / 12** |
| task ids present in the frozen population `plans/round52-tasks.json` | **12 / 12** |
| extracted anchors verified verbatim in their source entry | **12 / 12** |
| `source_entry` paths existing in the lane tree | **12 / 12** |
| capture digest check (`sha256sum -c SHA256SUMS`, 12 dirs) | **96 files `OK`, 0 failed, 0 warnings** |
| entries whose weakness class **cannot** be stated from the entry text | **0** (negative result — see §5) |

Capture sets checked and their sizes: `round35/tb2-eval` 6, `round36/tb2-regex-log` 5, `round37/tb2-git-webserver` 6,
`round38/tb2-build-pmars` 5, `round39/tb2-git-leak-recovery` 7, `round40/tb2-db-wal-recovery` 8,
`round41/tb2-constraints-scheduling` 10, `round42/tb2-circuit-fibsqrt` 9,
`round43/tb2-feal-differential-cryptanalysis` 12, `round44/tb2-feal-linear-cryptanalysis` 11,
`round45/tb2-password-recovery` 9, `round46/tb2-polyglot-c-py` 8.

---

## 4. The 12 task ids with their recorded weakness class

Full text in `read-findings.json`; the anchor column is the exact `file:line` the entry cites for that weakness.

| # | task id | weakness class the lane recorded (post-erratum wording) | anchor |
|---|---|---|---|
| 1 | `circuit-fibsqrt` | **Fixed graded-input table / lookup substitute.** The graded set is 28 points, not the function: a 1195-line lookup circuit for exactly those 28 inputs scores 3/3 while failing both instruction examples (208, 20000); line order, comment lines and the "last 32 lines" sentence are unenforced. Lane's class wording: the graded artefact is not read by the grader at all — it is *executed* by a C program the grader compiles from its own read-only copy. | `tests/test_outputs.py:73-102` |
| 2 | `polyglot-c-py` | **Dual-runtime execution over a three-point fixed table.** Three fixed points are not a Fibonacci definition — a polyglot printing the three literals from a table passes; the grader also mutates the directory it just asserted on (writes `cmain` into it), so it is not idempotent (7 of 18 passing states fail a re-grade). | `tests/test_outputs.py:27` |
| 3 | `password-recovery` | **F1 constant-compare family** (the lane's 2nd exemplar). The answer is a literal in the grader, so reading the public test file passes with no forensic recovery of the disk image; 1000 decoy lines are free (membership, not exactness or count). | `tests/test_outputs.py:18` |
| 4 | `feal-differential-cryptanalysis` | **In-process module import.** The agent's module runs inside the grader's process with the answer's public accessor in the same namespace, so five cheats that never recover the key pass (import `get_keys`, `sys.modules` shadow, rebind `get_keys`, always-equal object, `os._exit(0)`); the 30-second budget is unenforced. | `tests/test_outputs.py:30` |
| 5 | `feal-linear-cryptanalysis` | **F1 constant-compare on a text file** (the lane's 1st exemplar of F1). The 100 expected values are published in the test file and regenerable from the public generator's literal keys and hash chain, so three attack-free states pass; shape (order, separators, padding, extra content) is free. | `tests/test_outputs.py:122` |
| 6 | `constraints-scheduling` | **Order-sensitive constraint model.** The score depends on VEVENT order, not on the requested meeting (decoy VEVENT first → PPP; meeting first → PFF); the earliest test cannot reject an invalid submitted slot (only earlier slots are tested); input integrity compares decoded text, so a full CRLF rewrite of all three inputs passes. | `tests/test_outputs.py:135` |
| 7 | `db-wal-recovery` | **Graded artefact is a JSON export whose source of truth is never opened.** All seven tests read only `/app/recovered.json`; "Fix the WAL file" is graded only through the export, only 22 of the 33 `id`/`name`/`value` cells are pinned, and hand-typed JSON passes 7/7 without opening the database. | `tests/test_outputs.py:64` |
| 8 | `git-leak-recovery` | **Graded state is a repository history read through only four views.** "The secret cannot be found anywhere in that repo" is not the union of those views: eight passing violators (echo-only, reflog expiry, gc-only, blob ref, tag message, stash, dot-file work tree, `.git/config`); recovery and provenance are never checked because the expected secret is a literal in the grader. | `tests/test_outputs.py:16` |
| 9 | `protein-assembly` | **Literals replace source lookups.** The grader never opens the task's reference inputs (`pdb_ids.txt`, `antibody.fasta`, the plasmid, FPbase/PDB API results), so every requirement naming a source is enforced only through the literals; a G-only linker passes and failure messages misattribute (a one-residue error in a subprotein fails with the *order* message, because `find` returns −1). | `tests/test_outputs.py:25` |
| 10 | `build-pmars` | **Build provenance read as shape, not history.** Nothing reads a package, checksum, build log, Makefile or mtime, so a canned 21-line program + empty `debian/` dir + zero-byte `src/dummy.c` pass 4/4; the Debian check is existence-only (a zero-byte regular file named `debian` passes), the `ldd` scan is a `DT_NEEDED` scan blind to a run-time `dlopen`, and no exit status is ever read. | `tests/test_outputs.py:70` |
| 11 | `configure-git-webserver` | **Verdict channel and diagnostic channel are the same channel.** A body containing only the token `TEST PASSED` passes while the helper prints `TEST FAILED` (the helper echoes the body into the graded stdout); no assertion observes the clone/commit/push, so a static file with no repository, hook or push passes — only the first response's status and the second response's body are read. | `tests/test_outputs.py:13` |
| 12 | `regex-log` | **Fixed in-test fixture.** The log and the nine expected dates are literals inside the test file, so a plain alternation of the nine strings is a passing "regex"; several stated requirements are unobserved by that fixture (no-leading-zero octets, digit-adjacent dates, year width, month-length validity, the Feb-29 permitting side). | `tests/test_outputs.py:90` |

Two entries name the class in the lane's own vocabulary and the other ten state it as the entry's headline finding;
both forms are reproduced verbatim in the `weakness` field (the JSON quotes the lane's wording, not mine).

---

## 5. Entries whose weakness class cannot be stated from the entry text

**Negative result: none. 0 of 12.** Every entry states its weakness explicitly — either as a named class paragraph
(entries 1, 2, 3, 4, 5, 6, 7, 8, 10, 11) or as an explicit numbered findings list with "Three findings follow from the
executed table" / "The six findings, each bounded to this capture" (entries 9 `protein-assembly`, 12 `regex-log`). No
entry says "the weakness could not be determined", and no entry's errata retracts its headline weakness; the errata
that touch weakness (e.g. `circuit-fibsqrt` E1–E7, `db-wal-recovery` round-40 erratum, `polyglot-c-py` round-46
erratum item 1) **narrow** it, and I report the narrowed form.

Two caveats the L1 should carry, both stated from the entry text itself:

- **`protein-assembly` and `regex-log` carry no named class label.** Their weakness is a findings list, and their
  entries have no `## Summary` section (the other 10 do). The weakness class is still fully stateable from the entry
  text (I state it above), but if the C1 instrument wants a *label* for these two, it must be derived, not quoted.
- **`constraints-scheduling` finding 3 is published prior art** (TB2.1 PR #245, S124) and the entry explicitly
  claims **no novelty** for it; the same is true of the `configure-git-webserver` static-file weakness (TB2.1 issue
  #133, S114) and of `circuit-fibsqrt`'s "examples not graded" (an LLM audit, tier C). Four of the 12 entries say in
  their own Prior-art section that the class is already published. This bears directly on the C1 score rule
  (phenomenon-new vs phenomenon-known) for any of these 12 that end up as *confirmed findings*.

---

## 6. Cross-check offered to the C1 instrument (Amendment A1)

Amendment A1 moves the classification unit to the **test function** and defines `P1` = presence-only test; a task is
a vacuity candidate when ≥1 of its tests is `P1`. From the **entry text alone** (I did not read grader bytes), four of
the 12 hand-read tasks record a presence-only test function:

| task | presence-only test recorded in the entry | entry anchor |
|---|---|---|
| `circuit-fibsqrt` | `test_gates_file_exists` asserts only `Path("/app/gates.txt").exists()` | `test_outputs.py:11` |
| `password-recovery` | `test_recovery_file_exists` asserts only existence | `test_outputs.py:10` |
| `db-wal-recovery` | `test_recovered_json_exists` asserts only `os.path.exists` | `test_outputs.py:9` |
| `build-pmars` | the file's only presence check, `binary.exists()` (the entry names no test function for it) | `test_outputs.py:24` |

The other 8 record no presence-only test (their tests compare content, values, or subprocess output). This is
**[INFERENCE] from the lane's entry text**, not a measurement of the grader bytes; the instrument's own per-test split
is the authority. It is offered as a spot-check, not as a result.

---

## 7. Files produced (absolute paths)

| path | content |
|---|---|
| `/fast/scratch/hyaku/kengaku-r52/C1ExecReadFindings/read-findings.json` | the deliverable: 12 tasks → `{task, checks, weakness, anchor, source_entry}` (scratch copy; removed with the scratch dir before yield, per the operator directive) |
| `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecReadFindings/read-findings.json` | byte-identical kept copy of the deliverable, for the L1 to integrate |
| `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecReadFindings.md` | this report (the wave's `reportDir` is `.ufo/waves/round-52/w1`, per `w1-dispatch.json`) |
| `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecReadFindings/report.md` | identical copy at the write-scope path named in my seat brief |

No other file was created, modified or deleted. The lane tree, the fleet repo, `.ufo/state/`, `templates/`,
`scripts/`, `MANIFEST.json` and `/home/vgpnk/Projects/shokunin/.scratch/` were **not** touched. No
`git commit/add/push/stash/checkout/reset/pull` and no mutating `jj` command was run anywhere.

---

## 8. Risks and blockers

- **Anchor-variant note for the classifier.** The population lists, for `circuit-fibsqrt`, **both**
  `circuit-fibsqrt/tests/test_outputs.py` and `circuit-fibsqrt/environment/tests/test_outputs.py` (plus
  `sim.c` in both places). The lane's entry anchor is the `tests/` variant, which is also the frozen claims file's
  primary grader ("`tests/test_outputs.py`; `environment/tests/test_outputs.py` when the task has no `tests/` grader"),
  so my anchors are consistent with the frozen rule — but the lane has **not captured** the `environment/tests/`
  copy (only `round42/tb2-circuit-fibsqrt/` with `tests/` bytes exists, 9 files `OK`). If the two copies differ, the
  instrument's file-level class for that task is computed over the `tests/` bytes while the population also requires
  the `environment/tests/` capture to be fetched and digest-pinned. The lane's capture gives
  `tests/test_outputs.py` = `6117b8edb7d567b30e32b16a9244bec4c131ec01e9065d52f6f53f87e36f0438`.
- **Scope note.** These 12 tasks are the lane's *previously read* tasks, so they cannot serve as the "never read by
  this lane before this round" population that R52-C1 leg 3 requires; they are the lane's own baseline for what a
  weakness looks like, useful for calibrating the second-reader confirmations, not as confirmed findings.
- **No blockers.** All 12 entries were read in full; no entry was unreadable, truncated unread, or ambiguous about
  its weakness class.
