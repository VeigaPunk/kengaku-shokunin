# round 98 probe dry runs (L1 KengakuR98, before freeze)

- dry run 1 (`probe-dryrun-1.txt`, rc 1): every leg `MISSING` — the summary regex required the literal
  path `/tests/test_outputs.py`; pytest prints `test_outputs.py::name` relative to rootdir. Reward legs
  already matched the predictions (1 for C01/C04/C07/C09, 0 elsewhere).
- dry run 2 (`probe-dryrun-2.txt`, rc 1): path fixed; 9/12 matched. C11/C12 read `E:assert` because pytest's
  short summary prints the rewritten bare-assert text, not an exception type; C02 naroditsky read `E:`.
  Lesson: the summary line is not a type channel.
- dry run 3 (`probe-dryrun-3.txt`, rc 0): verdicts read through an observe-only report hook
  (`call.excinfo.typename`) with `pytest.main`; 12/12 cases equal their P0 predictions, unchanged since
  P0 commit 5584a6f7 (case table sha 02f30e6a… in all three runs).
