# R34EntryTB2 — scoped findings

- **Behavior:** Drafted the C1 Terminal-Bench `protein-assembly` knowledge entry, describing static evaluator predicates, runner reward mapping, expected-artifact grounding, Harbor context citations, negative space, and located-quote appendix.
- **Gates:** No gates or tests were run. Reported evaluator/runner logic was read from captured bytes; no claims of command execution.
- **Touched surface:** Wrote only `.ufo/waves/round-34/build/R34EntryTB2/entry.md` (7769 bytes; write tool outcome). Source evidence: `.ufo/waves/round-34/assimilation/captures/tb2-eval/{test_outputs.py,test.sh,antibody.fasta,pdb_ids.txt,instruction.md,task.toml,SHA256SUMS}`. Existing S092/S100 context read from `corpus/SOURCES.md` lines 111 and 113.
- **Out of scope:** Did not edit corpus/registry/index, plans, source repo, or product code; did not run any campaign command or runtime judge. This draft is not an admission or verification of the frozen C1 counter.
- **Finding / limit:** The grader embeds protein sequence literals in `test_outputs.py`; its test function does not load `antibody.fasta` or `pdb_ids.txt`. Entry expressly limits what expected-artifact grounding establishes and does not generalize beyond this task.
- **Artifact:** `.ufo/waves/round-34/build/R34EntryTB2/entry.md`

VERDICT: entry-tb2-drafted