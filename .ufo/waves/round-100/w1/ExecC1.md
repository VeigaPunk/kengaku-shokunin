# ExecC1 — R100-C1 independent re-measurement (round 100, wave 1)

Seat: ExecC1 (leaf). Independent re-measure of R100-C1 at T and BASE with own grader venv;
probe double-run from a `git archive` of T; C03/C04/C07/C08 rebuilt with own code and graded by
the captured test_outputs.py under real pytest 8.4.1 in bubblewrap.

## Method / tooling
- Scratch: /fast/scratch/hyaku/kengaku-r100/ExecC1 (TMPDIR set; removed before yield).
- Clones: `git clone --shared` of the lane, detached at T=dbe0cefa607cf57f7f58346fce64bcc127144ca0
  and BASE=7846037679de77d050141c785996471801e5a19a; `git rev-parse --show-toplevel` verified.
- Grader venv: `uv venv -p 3.13 G` (CPython 3.13.16) + `uv pip install pytest==8.4.1 pandas==2.3.2
  pytest-json-ctrf==0.3.5` (uv 0.13.0, channel uv tool/pip, reason: frozen test.sh uvx pins).
  Resolved numpy 2.5.4 (unpinned, stamped). No pacman used (host-wide PAUSED guard honoured).
- Frozen instrument SHA256s at T match round-100-claims.md: probe b255a428…, cases 286d1772…,
  counter 96fdf22f….
- Probe: `python3 plans/round100_fdp_probe.py --lane . --work … --grader-venv G` run twice from a
  `git archive` of T (archive-T, not a git repo, so LANE_TIP prints the fatal line — expected).
  OBSERVATIONS blocks (15 CASE + 15 DETAIL lines) diffed: run1 == run2 == committed receipt
  `corpus/evidence/round100/fdp-probe.txt` (obs_equal True, detail_equal True for both runs);
  only header LANE_TIP differs (receipt F=54df15ca… vs archive's fatal line).
- Independent cases: mybuilder/build.py reads ONLY committed documents/, solution placement.tsv,
  summary.csv, invoices-json/; never imports the probe BUILDER. Runs the byte-identical captured
  test_outputs.py (md5 5eca4355… both, sha256 978f506a… = frozen pin) via
  `bwrap --clearenv --unshare-all --ro-bind /usr /lib /lib64 /etc --dev-bind /dev … --bind app /app
  --ro-bind tests /tests … $G/bin/python -m pytest /tests/test_outputs.py -v`. No test-file edit.

## Counter results
- At T: `REV dbe0cefa…`, LEGS L1–L13 all pass,
  `TARGET executed_rows=44 … cells=crypto-credential:5,file-artifact:35 set_equals_base_plus_member=1
  located=1 executed=1 cases=15 legs=120 mismatches=0 new_rows=8 new_rows_flagged=0
  new_rows_line_live=0 changed_outside_table=0 defects=0`, `PREDICATE R100-C1 pass` (receipt c1-at-T.log).
- At BASE: LEGS L1–L12 fail, L13 pass; `TARGET executed_rows=43 … cells=crypto-credential:4,
  file-artifact:34 … located=0 executed=0 cases=0 … defects=12`, `PREDICATE R100-C1 fail`
  (receipt c1-at-BASE.log). BASE=78460376 has no round100 instruments — fail is structural.

## Gap reproduction (my own build → real pytest 8.4.1, 7/7 pass, exit 0, reward 1)
- C03 (all-total-rows): summary = header + 11 copies of the single total row (sha256 a64eacd0…,
  prefix matches receipt DETAIL), 21 invoices + 7 other. All 7 tests pass → gap REPRODUCES.
- C04 (one-invoice-repeated): summary = header + 10 copies of 41ibljh7.pdf row (440.0) + total
  (sha256 ba31a9a6… matches receipt), 21 + 7. All 7 pass → gap REPRODUCES.
- C07 (documents-subdir): all 17 documents copied to /app/documents/keep/, originals moved,
  correct summary. All 7 pass (incl. test_original_documents_dir_empty) → gap REPRODUCES.
- C08 (duplicate-copy): extra copy-41ibljh7.pdf inside /app/invoices/ (22 files), correct summary.
  All 7 pass → gap REPRODUCES (set collapse).
- Cross-check: my summary SHA256 prefixes a64eacd07a70e320 (C03) and ba31a9a6c6c19914 (C04) match
  the committed receipt DETAIL lines exactly.

## Verdicts
R100-C1 pass — frozen TARGET line and PREDICATE pass reproduced at T; BASE fails as frozen.
R100-C1 probe determinism pass — two archive runs byte-identical, OBSERVATIONS == committed receipt.
R100-C1 gap C03 reproduces pass — 7/7 pass, reward 1, summary sha matches receipt.
R100-C1 gap C04 reproduces pass — 7/7 pass, reward 1, summary sha matches receipt.
R100-C1 gap C07 reproduces pass — 7/7 pass despite documents/keep/ non-empty.
R100-C1 gap C08 reproduces pass — 7/7 pass despite duplicate invoice copy.

## Risks / blockers
None. Sandbox binds need /dev and the uv-python root bound at its symlink target name; resolved.
Evidence bundle: .ufo/waves/round-100/w1/ExecC1/ (c1-at-T.log, c1-at-BASE.log, probe-run1/2.txt,
build.py, builder-C*.log, pytest-all.log).
