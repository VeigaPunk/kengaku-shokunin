# R100-C1 review — ReviewC1 (round 100, 2026-11-06)

Scope: review of the frozen R100-C1 instruments and receipt at T = dbe0cefa607cf57f7f58346fce64bcc127144ca0,
per the seat item: observe-only hook neutrality, BUILDER-vs-`why` realization, reward leg, captured-name
staging equivalence, L1–L13 vs the frozen predicate text, and what L3/L10/L12/L13 add. Method: isolated
`git clone --shared` checkout detached at T under /fast/scratch/hyaku/kengaku-r100/ReviewC1 (removed after
receipt copy); all frozen files hash-verified against the claims tables before review.

## Instrument identity (all match `frozen-instruments` / `candidate-bytes`)

- plans/round100_fdp_probe.py b255a428…, plans/round100-cases.json 286d1772…, plans/round100_c1_replay.py
  96fdf22f…, capture test_outputs.py 978f506a…, SKILL.md 726dcdc8…, ledger d0df8332…, SOURCES.md 1f4c2354… —
  equal to the claims tables at T. Both SHA256SUMS files list exactly their directory (25 + 15 files) and
  every line hashes (independent re-verification, not via the counter).

## Checks

1. **Observe-only hook cannot change verdicts** — PASS. plans/round100_fdp_probe.py:185-196: the plugin is
   `@pytest.hookimpl(hookwrapper=True)` on `pytest_runtest_makereport`; it `yield`s first, then only reads
   `outcome.get_result()` and records `verdict[item.name]`; it mutates nothing pytest consumes. The reward
   leg is `rc = int(pytest.main(["-q","-p","no:cacheprovider","/tests/test_outputs.py"]))` (:197) —
   pytest's own exit — matching test.sh, which writes reward 1 iff the uvx pytest exit is 0 (test.sh:31-37,
   uvx pins `-p 3.13 -w pytest==8.4.1 -w pandas==2.3.2 -w pytest-json-ctrf==0.3.5` = GRADER_WANT). The only
   differences from the real grader invocation (`-q`/`no:cacheprovider`/no `--ctrf`) change output format,
   not outcomes or exit code.
2. **BUILDER realizes each case kind as its `why` says** — PASS for all 15, checked against the actual
   grader semantics (identification by sha512 content only, literals "summary.csv"/"total", `.json` suffix
   exclusion, DictReader header/11-row check, pandas name-based content check with strict `< 0.01`):
   - C03 all-total-rows: `total*11` after `assert len(total)==1` — why "11 rows all total,81315.2,5402.48",
     matches fixture summary.csv total row exactly; grader needs only 11 rows in table.
   - C04 one-invoice-repeated: `inv*10 + total` — "no uniqueness" (grader checks file set and row count,
     not row uniqueness).
   - C07 documents-subdir: copies of all 17 docs into `/app/documents/keep/` — grader's
     `test_original_documents_dir_empty` iterates top-level only (`iterdir()` + `is_file()`), so `keep/`
     passes; why "only top-level files counted" is exact.
   - C08 duplicate-copy: `copy-first_invoice` — same content → same sha512 → set collapses; why exact.
   - C09 misclassified-one: invoice file moved to `other/`, its `.json` sidecar withheld, summary 9+total
     =10 rows → predicted `P,F,F,P,F,F,P,0` follows from set non-equality on both moved tests + 10≠11.
   - C10 vat-zero: empty VAT written as "0"; grader maps both empty and 0 to 0 before `< 0.01` compare.
   - C11/C12 arithmetic: independent float check — |6204.199−6204.19| = 0.009000000000014552 < 0.01 (pass),
     |6204.2−6204.19| = 0.010000000000218279 ≥ 0.01 (fail); predicted `P,…,P,1` / `P,P,P,P,P,F,P,0` exact.
   - C14 headers-reordered: header and body columns swapped to filename,vat_amount,total_amount — DictReader
     `fieldnames` order assert fails, pandas reads by name → predicted `…,F,P,…` split exact.
   - C15 bom-header: `\ufeff` prefix before `filename` — DictReader first fieldname mangled (fail), pandas
     C parser strips a leading UTF-8 BOM (pass) → `…,F,P,…` split exact; observed receipt agrees.
   - C02/C05/C06/C13 negatives likewise follow from the grader text (absent dirs raise FileNotFoundError in
     iterdir/open/read_csv; notes.json excluded by suffix; notes.txt enters the hash set; missing summary
     fails the invoices set + both summary readers).
3. **Captured-name staging is grader-equivalent** — PASS. `randomize_filenames.py` renames at build; the
   grader never consumes names (only sha512 content, the literals "summary.csv"/"total", and the ".json"
   suffix). Independently recomputed sha512 of all 17 captured documents: they equal the grader's expected
   sets exactly (10 invoice hashes, 7 other hashes); placement.tsv sha256 matches all 17 files; fixture
   summary.csv row names are the staged names, so the content test's `/app/invoices/<filename>` opens.
4. **L1–L13 match the frozen predicate text** — PASS. Ran the official command at T
   (`python3 plans/round100_c1_replay.py --lane . --rev T --work … --grader-venv …`, scratch venv
   pytest 8.4.1/pandas 2.3.2/pytest-json-ctrf 0.3.5 on 3.13): rc 0, `LEGS L1=pass … L13=pass`, TARGET
   `executed_rows=44 member=financial-document-processor cells=crypto-credential:5,file-artifact:35
   set_equals_base_plus_member=1 located=1 executed=1 cases=15 legs=120 mismatches=0 new_rows=8
   new_rows_flagged=0 new_rows_line_live=0 changed_outside_table=0 defects=0`, `PREDICATE R100-C1 pass` —
   byte-identical field order/values to the frozen predicate line (evidence receipt c1-run.txt). The L6
   rerun (probe from `git archive` of T) reproduced the receipt's CASE/DETAIL block and the
   TOOL_SHA/CASE_TABLE_SHA/GRADER_SIDE stamps.
5. **L3/L10/L12/L13 do what the claims say** — PASS.
   - L3 (round100_c1_replay.py:262-265): `freeze_commit` requires the claims file be added by exactly one
     commit (= 54df15ca…, independently derived) and compares receipt LANE_TIP by equality, not ancestry —
     kills round-99 M04b's BASE-as-identity forgery.
   - L10 (:222-249, :314-315): row census BASE→T by row-id regex gives exactly the 8 added rows
     (git diff: SOURCES.md 8 insertions, S342–S349, zero removals; ledger census independently confirmed
     BASE 43/crypto 4/file-artifact 34 → T 44/5/35), AND re-runs the BASE gate bytes on a checkout of T:
     no DEFECT for any added row. Count + flag, not flag-only.
   - L12 (:316-322): `git diff --name-only F..T` restricted to the candidate-bytes table ∪ the receipt,
     and each OWNED file must have changed F..T AND hash to its candidate sha (ledger byte-pinned, so the
     L7 cell counts cannot drift silently).
   - L13 (:324-325): BASE line-gate bytes on the T tree must print no `ROW … state=live` for an added row.
   - P2 control scoping confirms discriminating power (controls/ run1): receipt-identity → only L3 fails;
     extra-row → L10 (and L12 on bytes); extra-file → only L12; skill-cell → only L12; typed-words → L13
     (and L12); extra-member → L7; counter-edit → L11; forged-receipt → L3+L6; do-nothing/c1-only → fail
     rc 1; positive/c1-both → pass with legs=120. Matches the claims' "what is new" bullets exactly.

## Findings

- RC1-1 INFO — C11/C12 `why` strings end in a dangling colon with no explanation text ("one total 6204.19
  -> 6204.199:") — plans/round100-cases.json:76,82. Cosmetic; the mechanism ("strict 0.01 band") is carried
  by the claims text and the predicted vectors. Frozen file — route to round 101 if worth polishing.
- RC1-2 LOW — a hung sandboxed case (`CASE_TIMEOUT=1800`) raises `subprocess.TimeoutExpired`, which is not
  among the caught types in `one()`/`main()` (only SystemExit is), so the probe would exit rc 1 via
  traceback without printing a PREDICATE line — plans/round100_fdp_probe.py:326-333,419-423. Fail-closed
  (the frozen predicate cannot print pass), diagnostics-only degradation; replay would record it as an L6
  failure, not could-not-evaluate.

No finding changes any verdict or the frozen predicate; nothing falsifies the claim. Both nits are routed
(round 101 material), not repaired in round.

## Evidence

- .ufo/waves/round-100/w1/ReviewC1/c1-run.txt — my end-to-end counter run at T (rc 0, predicate pass).
- .ufo/waves/round-100/w1/ReviewC1/controls-c1-legs.txt — LEGS/PREDICATE/TARGET lines of the twelve C1 P2
  controls (run1) used for the L3/L10/L12/L13 scoping check.
