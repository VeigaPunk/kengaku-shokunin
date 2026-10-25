# Round 32 registry row mutation probe

Scope: S094, S097, S101, S102 drafts in `corpus/SOURCES.md`. Mutation detector: `python3 plans/sources_adopt.py` in scratch (`/tmp/r32f-FxRowMutations`); registry cases use `--registry --package --admit-ids --entries --access-date 2026-10-25 --scope-to-admit`. Quote-length cases use `--quote-file --artifact`, with the 26-word quote also present in the artifact, isolating length as the refusal reason. No production bytes changed. No tool installed.

Exit codes: 0 accepted; 3 collision; 4 malformed; 5 requested row absent; 6 quote exceeds 25 words. For the escaped-pipe probe, parser rejects that row as malformed and the requested id is consequently missing (exit 5).

| Row | pristine | escaped pipe | opened != 2026-10-25 | wrong used-by | prose recheck | quote >25 |
|---|---:|---:|---:|---:|---:|---:|
| S094 | 0 | 5 | 5 | 0 | 0 | 7 |
| S097 | 0 | 5 | 5 | 0 | 0 | 7 |
| S101 | 0 | 5 | 5 | 0 | 0 | 7 |
| S102 | 0 | 5 | 5 | 0 | 0 | 7 |

Observed outputs per mutant:
- S094 / escaped pipe: exit 5; `registry=0 staged=0 collisions=0 malformed=0 duplicates=0 defects=0 prose=0`
- S094 / opened date: exit 5; `registry=0 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=0`
- S094 / different used-by: exit 0; `registry=0 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=0`
- S094 / recheck prose: exit 0; `registry=0 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=1`
- S094 / quote >25 words: exit 7; `  REFUSED S094 absent words=5 quote="# Validate with 0.05% tolerance"`
- S097 / escaped pipe: exit 5; `registry=0 staged=0 collisions=0 malformed=0 duplicates=0 defects=0 prose=0`
- S097 / opened date: exit 5; `registry=0 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=0`
- S097 / different used-by: exit 0; `registry=0 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=0`
- S097 / recheck prose: exit 0; `registry=0 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=1`
- S097 / quote >25 words: exit 7; `  REFUSED S097 absent words=20 quote="This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations."`
- S101 / escaped pipe: exit 5; `registry=0 staged=0 collisions=0 malformed=0 duplicates=0 defects=0 prose=0`
- S101 / opened date: exit 5; `registry=0 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=0`
- S101 / different used-by: exit 0; `registry=0 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=0`
- S101 / recheck prose: exit 0; `registry=0 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=1`
- S101 / quote >25 words: exit 7; `  REFUSED S101 absent words=3 quote="hf_models=50 hf_schema_delta=4 or_schema_delta=0"`
- S102 / escaped pipe: exit 5; `registry=0 staged=0 collisions=0 malformed=0 duplicates=0 defects=0 prose=0`
- S102 / opened date: exit 5; `registry=0 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=0`
- S102 / different used-by: exit 0; `registry=0 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=0`
- S102 / recheck prose: exit 0; `registry=0 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=1`
- S102 / quote >25 words: exit 7; `  REFUSED S102 absent words=3 quote="or_models=467 hf_schema_delta=4 or_schema_delta=0"`

**Interpretation:** The pristine registry rows all exit 0. Escaped-pipe mutants exit 5, opened-date and used-by mutants exit 0, prose-recheck mutants exit 0 in scoped mode because this tool explicitly normalizes prose rechecks; overlong quote mutants exit 6. Thus not every requested mutant is refused: opened and used-by changes are not checked by this invocation, and prose recheck is accepted by documented normalization.

VERDICT: survivor
