# round 97 P1 dry runs (L1 KengakuR97)

- dry run 0 (not kept, re-described here): probe rc 2, `ModuleNotFoundError: No module named 'isodate'` in the
  version stamp — rdflib 7.1.4 no longer depends on isodate; the stamp was narrowed to python/rdflib/pytest/pyparsing.
- dry run 1 (output overwritten by run 2, re-described here): 12 of 18 cases `observed=P,F,E:ParseException,0`.
  Probe defect, not a grader finding: `stage()` tested `isinstance(source, str)`, and the sentinel `"solve"` is a
  str, so every solve-based case wrote the literal text `solve` as the query. Fixed by `source != "solve"`.
  Recorded as lesson M2 (round 97).
- dry run 2 (`probe-dryrun-2.txt`): rc 0, 18/18 cases observed == the P0 mechanism predictions, with a DETAIL line
  per case (result form, variables, rows, distinct rows, names) proving each transform changed what it claims.
