# C1 entry truth-claim review

## Finding 1 — scope phrase overstates what the submitted entry directly sources

**Entry line 13:** “Harbor context is bounded by S092 ... and S100 ...” and “neither turns this task-level reading into evidence of a particular run.”

**Evidence:** The entry's own appendix table contains only captured task files (`test_outputs.py`, `test.sh`, FASTA, PDB list, and instruction) at lines 40–56. It has no quote or capture for S092/S100 in the listed captured bytes. The frozen claims do identify S092/S100 roles at `plans/round-34-claims.md:136-138` (S100/S092 as candidate package knowledge provenance) and line 109 (C1's sourced rows are S105–S107), but that does not itself establish the factual content summarized in line 13. The entry presents these as corroborating framework-internal context without a located evidence anchor. Label as lane/package context and cite its actual captured source, or remove it from this evidence-grounded task entry.

**Impacted axes:** provenance/traceability; scope discipline.

## Finding 2 — reference-input grounding is not a demonstrated basis for the hard-coded sequences

**Entry lines 13, 28:** says artifact grounding establishes the expected artifacts' role and evaluator embedded-sequence approach; line 28 quotes the grader comment that each subprotein has only one matching PDB-listed protein, then properly says this is not a demonstrated runtime lookup or sequence-by-sequence derivation.

**Evidence:** `assimilation/captures/tb2-eval/test_outputs.py:25-36` shows the grader comment and literal component strings, but does not identify PDB IDs corresponding to donor/acceptor/molecule binder or compare those literals to FASTA/API records. `pdb_ids.txt:1-20` only lists IDs. `instruction.md:14-15,24-26` requires PDB/API and FPbase criteria. `antibody.fasta:1-4` only provides heavy/light-chain sequences. Thus the careful qualification at line 28 is supported, but the heading “Expected-artifact grounding” and the phrase “grounded against” in line 13 can be read as stronger derivation than evidence provides; clarify that only file roles and captured contents were inspected, not the grader literals' provenance/correctness against them.

**Impacted axes:** truthfulness; task-scope/coverage quality.

## Finding 3 — “all the requirements” is an unsupported broader reading in the code docstring, avoid implying it

**Entry line 9:** describes the output test as grading one gblock against encoded-protein sequences and sequence-structure constraints; it does not explicitly claim full task compliance. The nearby sections otherwise bound the scope correctly.

**Evidence:** `test_outputs.py:11-12` docstring says it meets “all the requirements described in task.yaml,” while actual asserts at lines 13-73 check file representation, alphabet/length, translated literals/order, linkers, and GC only. The captured task instruction has additional requirements at `instruction.md:12-26` (protein/API identity, antibody sequence, DHFR reuse, spectral match, start/stop and methionine handling). This entry does not repeat the docstring's overclaim, but line 19 boundary (“source checks this file representation and alphabet/length”) and line 32 negative-space correctly constrain it; retain that distinction and explicitly say the grader does not independently establish all task instructions if this entry is used as a completeness statement.

**Impacted axes:** precision; non-overclaim.

## Re-derivable numeric claims

Numbers in entry lines 19–23, 28 and 32 are directly re-derivable from captures: one file/line (`test_outputs.py:13-23`), 3000 nt (`:23`), five components (`:28-36`), four intervening GS linkers of 5–20 aa (`:47-58`), 50-nt windows with 15–35 GC (`:64-73`), runner 1/0 reward mapping (`test.sh:18-29`), two FASTA records (`antibody.fasta:1-4`), and 20 PDB IDs (`pdb_ids.txt:1-20`). The sequence count is five, but expected-artifact files are two; they are not interchangeable. The shell runner also installs/fetches dependencies and runs pytest (`test.sh:3-23`), so its reward mapping does not establish any live Harbor reward consumption/aggregation; entry line 24 explicitly scopes that out.

Remote URL re-open attempt: `read` on the pinned raw GitHub URL returned HTTP 404. Therefore the source comparison here relies on the round capture bytes and their SHA256 entries, not a successful independent remote fetch. Capture checksums for the two main evaluator files were not present in `SHA256SUMS` (that file lists only artifact/task metadata files); do not imply those two byte captures are hash-verified by that manifest. Local command evidence: `sha256sum ...` output gave test_outputs.py `44a05a...96582`, test.sh `9ede46...267b5`, antibody.fasta `e0e136...c333`, pdb_ids.txt `ea338c...358c2`; `wc -l ...` output was 73, 30, 20, 123 total. Those two hashes are locally observed, but no committed expected digest for them is displayed in the capture manifest.

VERDICT: critic-entry-tb2 (3 findings)
