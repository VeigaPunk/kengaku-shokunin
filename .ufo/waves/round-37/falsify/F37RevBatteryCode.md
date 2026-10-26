# F37RevBatteryCode — code review of `plans/battery37` (kengaku r37 wave 2, falsify)

Seat: reviewer, leaf (no subagents used). Lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin at tip 357deceb (branch master).
Report path (this file): .ufo/waves/round-37/falsify/F37RevBatteryCode.md

## Scope and method

All 9 modules in `plans/battery37` (p4, p5, p6, p7, p8, p910, p23, d4, d5) were read in full and each
builder was traced against the unmodified gate `plans/pkg_gate.py` (freeze digest confirmed) and the
frozen spec `plans/pkg-spec-r35.json`, plus the round-36 helpers the ctx exposes
(`copy_package`, `rewrite_quotes`, `d4_line`, `d5_line` in `plans/round36_c1_verify.py:55-89,161-174`).
Content claims (capture line contents, quote occurrence counts, manifest format, registry rows, entry
lines) were checked against committed lane bytes.

Evidence commands (all run read-only on the lane):

- `sha256sum plans/pkg_gate.py` → `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41`
  = `GATE_SHA256` at `plans/round37_c1_verify.py:36`. The gate the fixtures target is at its freeze digest.
- Fixture counts: importing each module's `FIXTURES` → p4=4, p5=7, p6=8, p7=6, p8=5, p910=4, p23=6, d4=3,
  d5=7, total 50, all fid unique; receipt `.ufo/waves/round-37/integrate/measure-final.txt` prints
  `BATTERY fixtures=64 wrong=0 renamed_disagree=0` (14 r36 + 50 battery37) and
  `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0`.
- `git ls-files corpus/evidence/round35/tb2-eval/` → exactly SHA256SUMS, antibody.fasta, instruction.md,
  pdb_ids.txt, task.toml, test.sh, test_outputs.py (7 committed files; `__pycache__/` ignored at
  `.gitignore:2`; `.pytest_cache` is untracked working-lane dirt, absent from a clean clone).
- Capture facts: `test_outputs.py` has 73 lines; line 66 `    assert 15 <= gc <= 35, (`, line 71
  `        assert 15 <= gc <= 35, (`, line 23 `    assert len(gblock) <= 3000, ...`; the d5 quote occurs
  exactly once raw and once in the gate's tag/whitespace-stripped flat text; the tb2-eval manifest uses
  bare names (`44a05a24...  test_outputs.py`), six pinned files including unquoted `task.toml`.
- Spec facts: `entry_rules` = min_quotes 8, min_distinct_locations 8, quote_words [3,25],
  min_teaches_words 8, row_tier A, row_status mined; `frozen_instruments` includes
  `plans/tb2_grader_probe.py` (so editing the probe trips P1); `probe_cmd` runs it with cwd=root.

## Axis 1 — fixture isolation: one branch per fixture as declared — PASS

Every single-clause declaration was traced to exactly one firing gate branch; the seven multi-clause
declarations are each forced by gate structure and documented in the module docstring.

| Fixture | Declared | Gate branch that fires (pkg_gate.py) | Verified |
|---|---|---|---|
| p4-no-quote-row | P3,P4 | texts=0 < min_quotes (`:104-133`) + "no parsed quote" (`:135-137`) | yes |
| p4-capture-unreadable | P4,P5 | "unreadable capture" (`:139-140`) + quote-capture-not-pinned (`:160-162`) | yes |
| p4-line-outside | P4 | `q.end > len(lines)`, 9999 > 73 (`:141-142`) | yes |
| p4-one-char-off | P4 | "quote not verbatim there" (`:143-144`) | yes |
| p5-manifest-absent | P5 | manifest-absent early return (`:150-152`) | yes |
| p5-manifest-unparsed-line | P5 | unparsed-manifest-line (`:157-159`) | yes |
| p5-capture-bytes-stale-digest | P5 | digest-vs-bytes on unquoted pinned `task.toml` (`:162-163`) | yes |
| p5-row-capture-unpinned | P5 | row-capture-not-pinned only (`:154-156`) | yes |
| p5-manifest-digest-off-pin | P5 | digest-vs-spec-pin only (`:164-165`) | yes |
| p5-quote-cites-unpinned | P5 | quote-capture-not-pinned only (`:160-162`) | yes |
| p5-extra-capture-file | P5 | not-covered sweep (`:163-166`) | yes |
| p6-m20..m27 (8) | P6 | one `bad.append` each (`:168-190`) | yes |
| p7-m28-entry-deleted | P3,P4,P7,P8 | entry=None fans to 4 clauses (`:87-101,135-137,188-189,241-247`) | yes |
| p7-m29..m33 (5) | P7 | one `bad.append` each (`:190-215`) | yes |
| p8-* (5) | P8 | one branch each (`:217-247`) | yes |
| p910-not-a-git-repo | P9 | ls-files returncode != 0 (`:249-252`) | yes |
| p910-receipt-deleted | P2,P10 | receipt unreadable in both clauses (`:118-121,271-272`) | yes |
| p910-probe-exits-1 | P1,P10 | probe is a frozen_instruments pin + fresh-exit branch (`:107-112,277-279`) | yes |
| p910-receipt-one-byte | P2,P10 | digest pin + byte-equality branch (`:118-121,280-281`) | yes |
| p23-p2-receipt-deleted / -byte | P2 | receipt branches (`:118-121`) | yes |
| p23-p3-heading-renamed | P3,P4 | parse keyed on the heading (`:87-101`) + no parsed quote | yes |
| p23-p3-seven-texts / -locations / -two-word | P3 | min_quotes / min_distinct_locations / word-range (`:104-133`) | yes |
| d4-m44/m45/m46 | D4 | branches (a)/(b-count)/(b-label) (`:318-327`) | yes |
| d5-m48..m53, m55 | D5 | one branch each (`:330-351`) | yes |

Key single-branch proofs against the gate source:

- p6-m20 (duplicate S105 row): `c_sources` does `len(found) != 1 → append; continue` (`pkg_gate.py:173-176`),
  so the duplicate never reaches the teaches collection (`:183-186`) — the pairwise-distinct branch (M27)
  cannot co-fire. p6-m21 (12 cells) likewise `continue`s before all later checks.
- p5-row-capture-unpinned: the capture's bytes move to a byte-identical `.copy` pinned with the same
  digest (M15 silent), quotes re-cited to the copy at unchanged line numbers (P4 silent), the original
  name leaves manifest and directory (only `pinned[name]` miss fires). Confirmed the manifest line
  rewrite preserves parseability (`MANIFEST_LINE`, bare names).
- p5-quote-cites-unpinned: the extra capture is a dotfile, and the not-covered sweep skips
  `f.name.startswith(".")` (`pkg_gate.py:163-166`) — only the M18 branch fires.
- d5-m55: the gate pins via `parts[-1].endswith(d5["capture_name"])` (`pkg_gate.py:342-344`), so the
  fixture's path-prefixed manifest line satisfies M54's check while the quote (1 raw / 1 flat occurrence,
  verified) is absent — only M55's branch fires.
- d4-m46: the altered line keeps every byte after the label, and all three spec patterns match bytes
  after the label, so only the `startswith(label)` half of branch (b) rejects; M45's two-line file
  rejects on count before patterns run (`pkg_gate.py:322-327`).
- p23 content coupling is guarded at build time: `rows[14]` must contain `test_outputs.py:71`,
  `rows[4]` `:23`, `rows[6]` `:27` (p23.py:88-91,102-104,117-119) — checked against the real capture:
  line 66 and 71 carry the same `assert 15 <= gc <= 35, (` modulo indentation (substring verbatim holds
  for the :66 re-cite), line 23 hosts the 5-word prefix (6 tokens → 5 words ≥ 3, in range), and the
  2-word cut of the :27 row stays verbatim. Resulting counts (8 rows / 7 texts / 8 locs; 8 rows / 8
  texts / 7 locs; 22 rows with one 2-word quote) fire exactly the intended branch under
  min_quotes=8, min_distinct_locations=8, quote_words=[3,25].
- p7-m32 safety: the Negative space section contains no `|`-starting lines (verified), so dropping the
  heading cannot inject `bad_rows` into P3.

Mutant-kill completeness of the battery37 half (each target mutant's observable flips): traced for
M02,M03,M04,M06-M12 (p23/p4), M13-M19 (p5), M20-M27 (p6), M28-M33 (p7), M34-M38 (p8), M39,M41-M43
(p910), M44-M46 (d4), M48-M53,M55 (d5). M05/M40/M47/M54 are the r36 battery's kills per the module
docstrings (d5.py:16-17 names r36-L6 for M54) — correct division of labor, no battery37 fixture claims
them.

## Axis 2 — no reliance on lane working-tree state beyond ctx helpers — PASS (1 note)

- All fixture content derives from ctx: `ctx.genuine_package` / `ctx.r36.copy_package`, `ctx.spec`,
  `ctx.r36.QUOTE_ROW` / `rewrite_quotes`, `ctx.d4_line`, `ctx.d5_line`, `ctx.d5_capture_dir`, `ctx.git_add`.
- The only direct `ctx.lane` read is p910 `_ignore_rule` (p910.py:37-38), copying the lane `.gitignore`
  into the fixture. It is read-only, goes through a ctx-provided attribute, and is documented with its
  reason (p910.py:25-30): P10's probe import byte-compiles the captured grader into
  `corpus/evidence/round35/tb2-eval/__pycache__` inside d from the second gate run onward, and fixtures
  are separate repos where the lane's own .gitignore does not apply. Necessary and correct.
- Note N1 (residual, not a defect): `copy_package` copies the lane working tree's capture dir
  (round36_c1_verify.py:61-63). Untracked `.pytest_cache` dirt in a working lane would be copied into
  fixtures and trip P9 on every package fixture — but loudly (`wrong>0`), and the frozen predicate
  mandates a clean clone of the tip, where only the 7 committed files exist (verified via
  `git ls-files`). Fail-visible, not silent.

## Axis 3 — scratch hygiene: nothing outside d — PASS

Every write in all 9 modules targets a path under the handed-in `d`: entry (p4.py:44-46, p7.py:52-62,
p23.py:63-65), SOURCES.md (p6.py:17-33), README.md and one knowledge file (p8.py:36-46,86-92), captures
and manifest (p5.py:31-37,118-121,151-152), receipt/probe/.gitignore/.git pointer (p910.py:37-38,64-66,
82-89,102-108), d4/d5 erratum files and d/caps (d4.py:29-33, d5.py:24-31). No module uses tempfile, the
cwd, or writes to `ctx.lane`. d4/d5 fixture paths are built from `d` itself so the counter's renamed run
relocates them (d4.py:40-42, d5.py:41-43). p910 `_not_a_git_repo` writes its `.git` pointer inside d and
fail-fasts if d is still inside a readable worktree (p910.py:44-56) — the pointer file forces the
gate's `ls-files` returncode branch, which is exactly M39's target.

## Axis 4 — determinism: no time/random — PASS

Imports across all 9 modules: hashlib, re, pathlib, shutil, subprocess only. Grep for
`time|random|datetime|uuid|socket|urllib|requests|environ|now(|today(` over `plans/battery37/*.py`
returns a single hit: the URL data string at p6.py:68 (a literal in the M22 fixture, not an I/O call).
All fixture bytes derive from committed lane bytes plus constants; iterations walk fixed manifest order
(p5.py:56-62) or sorted ids (p5.py:74, p8.py:64). Every positional/anchor assumption carries a
build-time assert that fails the build instead of misdeclaring (p23.py:88-91,102-104,117-119;
p4.py:31-34,77-79; p7.py:70-73,76-79,88-91; p910.py:70-71,104-106; d5.py:36-40,55-58,71-73,84-86,97-99;
d4.py:49-51,60-62; p6.py:44-46,74-77).

## Axis 5 — no `--spec` — PASS

Every returned argv is `["package", "--root", str(d), "--require-clean-tree"]` (p910 adds `--rerun`
only) or `["d4-line"|"d5-line", "--file"/"--capture-dir", ...]`; no module appends `--spec` (the spec
path is the counter's own addition, round37_c1_verify.py `run_gate`). The harness independently rejects
a forbidden argv (SETUP check in `main`).

## Axis 6 — no network — PASS

No HTTP/socket/urllib/requests client anywhere in the modules; p910's subprocess calls are local git
probes only (p910.py:45-56). Note N2 (residual, gate property not battery code): clause P10's uv
fallback (`uv run --no-project --with biopython==1.85`, pkg_gate.py:275-280) can reach PyPI when `Bio`
is not importable and the wheel is not cached; the p910 P10 fixtures transitively exercise that clause.
The measurement host satisfied it (receipt shows byte-equal reruns), and this is the round-36 landing's
behavior, outside battery37's code.

## Findings

No defects on any reviewed axis. Non-blocking notes:

- N1: p910's direct `ctx.lane/.gitignore` read (p910.py:37-38) — within the ctx contract, read-only,
  documented, and required for P9 stability across the counter's 57 gate runs per fixture dir.
- N2: P10 fixtures transitively depend on the host being able to re-run the probe (importable Bio or
  cached biopython wheel) — environmental, deterministic, gate-side.
- N3 (cosmetic): docstring seat labels are inconsistent — p8.py:1 says "Battery37 module R37BatP8",
  d4.py:3 "seat R37BatD4", others carry none. Zero behavioral impact.

Reviewer-side actions recorded: read-only inspection of the lane; no lane file written; no scratch
clone or counter run was needed for this seat (counters belong to the calibration seats), so no scratch
dir was created under /fast/scratch/hyaku/kengaku-r37/ and nothing remains to delete. The FIXTURES-count
check exec'd the modules via importlib at the lane path; bytecode caching could only refresh the
gitignored `plans/battery37/__pycache__/*.pyc`, which pre-existed this session (present in the first
directory listing) — no tracked byte touched. No tools were installed.

VERDICT: battery-code-0-defects
