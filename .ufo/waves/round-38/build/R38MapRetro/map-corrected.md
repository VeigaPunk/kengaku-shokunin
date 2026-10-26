# R38MapRetro — corrected `## Requirement map` for `knowledge/tb2-git-webserver-grader.md` (draft, not integrated)

The entry is append-only lane text and this seat writes no lane file, so this fragment is the corrected
4-row table for the L1 to append as an erratum. Only the table is checked by `map_label_retro.py`; the
per-row prose the round-37 closure (D2) and `F37CritC2Map` ask for is drafted in the seat report, not
here. Labels are re-derived under round-38 C2 V7 over **every** receipt case whose violates-set carries
the line (`violates-r37.tsv`), and each cited case is one of those violating cases.

## Requirement map

| Instruction line | Label | Receipt cases |
|---|---|---|
| `instruction.md:1-6` | unenforced | `static-file-no-git` |
| `instruction.md:7` | partly | `wrong-port-8081`, `static-file-no-git` |
| `instruction.md:8` | partly | `not-found`, `status-then-content-split` |
| `instruction.md:9` | partly | `capitalised`, `leading-space`, `token-in-body` |

Changes from the entry (`corpus/knowledge/tb2-git-webserver-grader.md:103-108`):

- row 8: `catch-all-200` -> `status-then-content-split` (the catch-all satisfies line 8 as written; the
  split case is a state whose first answer to the line's own request is not `hello world`, observed pass);
- row 9: label `enforced` -> `partly`, witness `token-in-body` added (body `TEST PASSED` is not
  `hello world` and the case is observed pass);
- rows 1-6 and 7 keep their labels and cases; row 7's prose needs the by-construction qualifier
  (`verify.sh:57,60` hardcode `localhost:8080`), which the table cannot express.
