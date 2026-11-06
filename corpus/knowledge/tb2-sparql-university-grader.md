source: S317–S322, https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sparql-university/tests/test_outputs.py:79; companion files and quotes in corpus/lessons/round-97.md §Gate
verified-at: 2026-11-06 (round 97; measured T f1083da60e7ff6b88f7420aae7424f7762d14700)
recheck: on-release

# SPARQL output equality is not query-criterion coverage

The captured grader executes `/app/solution.sparql` against a hidden Turtle graph, not the agent's graph. Three functions check file existence, query execution, and equality with four reference tuples. Country tokens are split on commas, stripped and sorted. Result rows become a set of `(row.professorName, normalized(row.countries))`; other projected variables are ignored.

The replay runs the captured functions unchanged and real pytest 8.4.1 for the reward leg, under Python 3.13 and rdflib 7.1.4. Eighteen cases × four legs reproduce their mechanism predictions (`plans/round97-cases.json`, `corpus/evidence/round97/sparql-probe.txt`).

| intervention | observed | interpretation |
|---|---|---|
| captured solve.sh, unchanged | P,P,P,1 | positive control |
| no query file | F,FileNotFoundError,FileNotFoundError,0 | no-work is rejected |
| remove EU VALUES restriction | P,P,P,1 | the hidden graph has no >10-student professor without an EU department; the criterion is redundant on this fixture |
| replace both reference dates with the date of NOW() | P,P,P,1 on the measured host date | date-policy error not distinguished; not an assertion about arbitrary future graph data |
| ignore graduation dates | P,P,F,0 | adds Marie Dubois; this criterion does have a witness |
| include roles containing Professor rather than starting with it | P,P,F,0 | adds assistant professor Voulodimos |
| count students per department rather than across a professor's departments | P,P,P,1 | the instruction's per-department requirement and solution's aggregate requirement coincide on this graph |
| literal VALUES answer without a graph pattern | P,P,P,1 | answer agreement does not establish query logic |
| UNION query with itself | P,P,P,1; 8 rows, 4 distinct | duplicates disappear under set comparison |
| extra projected count variable | P,P,P,1 | output-schema constraint is not checked |
| renamed professorName variable | P,P,AttributeError,0 | the grader reads field names, not column position |
| literal answer from the agent graph | P,P,F,0 | two names differ and Alex Dimakis exists only in the hidden graph |

## Reuse rule

For a query benchmark, pair each logical criterion with a data witness that changes membership when only that criterion is dropped. Separate output equivalence from implementation semantics: a literal answer can satisfy exact result equality. Price set/multiset and projection semantics independently. Here, graduation and role have witnesses; EU membership and department-level versus aggregate enrollment do not.

## Limits

This is a located offline replay of the pinned member, not a survey of SPARQL benchmark quality. The task image was not pulled. The verifier library pins are modelled with a pre-staged venv; CPython micro and pyparsing are unpinned and printed separately. The wrapper's network installation and CTRF reporting are not replayed; pytest's test-file success is observed directly. The finding set is finite, not exhaustive.
