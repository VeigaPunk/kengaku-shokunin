# GateBuild — round 63 w1: R63-C2 depth checker + provenance-trio gate

Seat scope: build the frozen R63-C2 instrument and the provenance-trio gate; produce the
red-before and before-state receipts. No claim rule was edited; ambiguities are resolved below
and reported, not re-frozen.

## Deliverable

- `L/.ufo/waves/round-63/w1/gate/gate_checks.py` — 514 lines, python3 stdlib only,
  sha256 `65dcdd34587762fdbb5f223f1e5396e975623a7f57a299e388c3a2dbaf1793c0`
  (`ast.parse` ok). L1 copies it to `plans/round63_gate_checks.py`.
- CLI: `trio <file>` | `depth --skill <SKILL.md> --receipt <class-survey.txt> [--root <lane root>]`
  (default `--root .`) | `--selftest --work <dir>` (alias `selftest --work <dir>`).
- Exit codes: 0 pass | 1 fail | 2 usage/setup (unreadable argv/skill/receipt, missing `--work`).

## Acceptance evidence (all commands run against the final bytes above)

1. Selftest — `python3 .ufo/waves/round-63/w1/gate/gate_checks.py --selftest --work
   /fast/scratch/hyaku/kengaku-r63/GateBuild/selftest` → **rc=0**
   (`gate/selftest.txt`, sha256 `06fd8772…ba1da8`):

   ```
   SELFTEST GOOD rc=0 expect=0 n=16 class_match=True count_mismatch=0 ok
   SELFTEST BAD-COUNT rc=1 expect=1 n=16 class_match=True count_mismatch=1 ok
   SELFTEST NO-SECTION rc=1 expect=1 n=0 class_match=False count_mismatch=0 ok
   SELFTEST pass
   rc=0
   ```

   Fixtures live in `mkdtemp(dir=<--work>)` and are removed (work dir empty after the run).

2. Trio red-before — `cd L && { python3 .ufo/waves/round-63/w1/gate/gate_checks.py trio
   corpus/knowledge/tb2-grader-class-census.md; echo "rc=$?"; } > gate/trio-red.txt 2>&1`
   → **rc=1**, `gate/trio-red.txt` (sha256 `151a66fd…ef0577`):

   ```
   TRIO fail missing=verified-at,recheck file=corpus/knowledge/tb2-grader-class-census.md
   rc=1
   ```

   Matches the frozen expectation character for character.

3. Before-state — `git -C L show c78749a5:SKILL.md > <scratch>/SKILL.base.md`
   (base sha256 `f6d71a00ecdfba0cbc6708761f13eb12560c963afa609c172cdef0bf55a2b646`, 1384 lines),
   then `python3 gate_checks.py depth --skill <scratch>/SKILL.base.md --receipt
   L/corpus/evidence/round62/class-survey.txt --root L` → **rc=1**
   (`gate/depth-before.txt`, sha256 `bbe03d1f…234923`):

   ```
   ROWS n=0 class_match=False count_mismatch=0 paths total=0 resolved=0 share=0.00
   DETAIL section-absent heading='## Decision table — grader class → offline replay recipe'
   PREDICATE R63-C2 fail
   rc=1
   ```

4. Dry run of the after-state shape (advisory, not the builder's landing): a 16-row section
   generated from the real census receipt, real `--root` → **rc=0**, `ROWS n=16
   class_match=True count_mismatch=0 paths total=1 resolved=1 share=1.00`, `PREDICATE R63-C2
   pass` (`gate/depth-after-dryrun.txt`, sha256 `8afb85cd…7a359e3`). The claims' counting command
   shape also works with the default `--root .` from the lane cwd (same output, rc=1 on today's
   section-less `SKILL.md`).
5. Edge matrix — `gate/edges.txt` (sha256 `26d0f053…81da581`): trio green/out-of-order/
   past-line-12/after-heading/no-dash; usage exits (2,2,2,2); share floor 9/10=0.90 **passes**
   (inclusive), 8/10=0.80 fails; 4-cell and 6-cell rows fail; header worded `Grader class`
   passes; backticked URL excluded from path accounting; `###` heading does not match.

## Ambiguity resolutions (frozen rule unchanged)

1. **Base-tip typo in the seat brief.** The 40-char literal
   `c78749a5565dfd186f10a1d8ac98e19dac2429666` is not an object in the lane repo (extra digit;
   `git cat-file -t` fails). The claims file's short tip resolves: `git rev-parse c78749a5` →
   `c78749a565dfd186f10a1d8ac98e19dac2429666` (commit). Base extraction used the resolved tip.
2. **Duplicate backticked paths** are priced once (set semantics), so a repeated broken pointer
   is not double-counted in the share.
3. **Row pointer cell**: passes iff it holds >=1 path token and at least one of its tokens
   resolves; the section-wide share prices the rest.
4. **Trio key out of canonical order** (e.g. source, recheck, verified-at) counts as not
   established, so it is listed in `missing=`; the first occurrence of each key is the one
   ordered.
5. **Trio window**: `missing=` lists canonical keys absent or out of order, in canonical order —
   hence exactly `verified-at,recheck` for the round-62 entry.
6. **Heading match**: compared after `rstrip()` only (trailing whitespace tolerated); leading
   whitespace, case, the em dash U+2014 and arrow U+2192 are exact. The claims file wraps the
   quoted heading across two lines; the single-line form (as in the seat spec) is the byte string
   checked, verified equal after whitespace normalisation.
7. **Header row**: the row immediately above a separator row is ignored whatever its wording
   (first cell literally `class` also ignored) — the frozen rule says to ignore the header without
   fixing its text. A second table in the section is *not* excused: all `|` rows are class rows.
8. **URLs**: a backticked token carrying `scheme://` is not a repo-relative path and is excluded
   from path accounting (a PEP 503 citation cannot depress the share).
9. **`path.txt:11` tokens** do not end in a counted suffix and are therefore not path tokens; the
   frozen definition is syntactic and is applied as written (a pointer cell with only a
   `path:line` token fails `row-pointer=<class>:no-path-token`).
10. Unreadable `--skill`/`--receipt`/argv file → setup exit 2; a nonexistent `--root` is not a
    special case (all paths unresolved → fail 1).

## Consumer contract for the C2 section (strict points that can bite)

- Heading line: `## Decision table — grader class → offline replay recipe` exactly (U+2014,
  U+2192), at column 0; section ends at the next line starting with `## `.
- Exactly 16 data rows, one per `CLASS` name in `corpus/evidence/round62/class-survey.txt`
  (`signal-delivery 1, subprocess-exec 45, shell-exec 6, candidate-import 6, file-artifact 76,
  stdout-inspection 29, numeric-band 10, crypto-credential 12, network-service 8, timing-wall 9,
  filesystem-metadata 10, process-environment 3, git-plumbing 3, db-state 2,
  serialization-schema 10, container-image 0`).
- 5 cells: class | count | executed | replay recipe | receipt pointer. Count cell must be a plain
  integer equal to the receipt (no `45 (52%)`).
- Pointer cell must contain a backticked repo-relative token ending `.py .md .json .txt .sh .lst
  .yml` or `/`, resolving from the lane root. `path.txt:11` does not qualify.
- Run the gate from the lane root (or pass `--root`), else resolution collapses.

## State / hygiene

- Green trio leg is **not yet observable**: `corpus/knowledge/tb2-network-service-offline-grader.md`
  did not exist at 15:08 (checked once, no polling). Synthetic green fixture prints
  `TRIO pass …` (edges receipt). The frozen green leg needs the C2/knowledge builder's entry.
- No tool installs or upgrades; no network calls; no git mutation; port 8080 never bound.
- Scratch `/fast/scratch/hyaku/kengaku-r63/GateBuild/` removed after copying all receipts into
  `gate/`. Writes were confined to the seat dir and that scratch dir.

## Risks

- The gate is only as good as the section's literal shape; items 8/9 above are strict by the
  frozen wording and are the most likely cause of an honest fail if the builder's pointer cells
  carry line suffixes.
- `class_match` requires exactly 16 receipt classes and 16 unique rows; a legend table inside the
  section will fail the row count.
