# W2ExecConfirmC report (kengaku r52 wave 2, executor)

Attacked: R52-C1 candidate rows 6-10 (1-based rank in the counter's CANDIDATES list, total=29): crack-7z-hash, db-wal-recovery, extract-elf, financial-document-processor, hf-model-inference. (Rows 6-10 of the raw output file would instead be bn-fit-modify..code-from-image; I read the item as candidate rank, and say so.)

Commands: `python3 plans/round52_c1_grader_audit.py --lane <lane>` (cwd scratch, TMPDIR=scratch) -> `TASKS 89/89/88`, `CAPTURES expected=184 present=183 mismatched=0`, `CANDIDATES total=29`, `CONFIRMED new=0`, `PREDICATE R52-C1 fail`, `R52-C1-A5 fail` (prior-art absent, expected). Then read each grader's tests/test_outputs.py, built receipts with `mk.py` (asserts every quote is a verbatim substring of the captured bytes), and re-ran the counter on a scratch copy of the lane (graders, tb2 entries, plans, my confirmations.json): `CONFIRMED new=3 ['crack-7z-hash','extract-elf','financial-document-processor']`.

## Receipts (4 rows, 3 new tasks; reader W2ExecConfirmC)
- crack-7z-hash `test_solution_file` L8-13: only `os.path.exists("/app/solution.txt")`. Content in separate `test_solution_content` (== "honeybear").
- extract-elf `test_extract_js_exists` L309-313: only `.exists()` + `.is_file()`.
- financial-document-processor `test_directories_created` L18-28: only exists()+is_dir() on /app/invoices, /app/other.
- financial-document-processor `test_summary_csv_exists` L100-103: only `.exists()` on summary.csv. Counter did NOT list this second presence-only test (a counter under-detection: only test_directories_created is listed) — task still a candidate.

## Refusals
- db-wal-recovery: `test_recovered_json_exists` (L7-9) is genuinely presence-only, but the lane hand-read this task before (corpus/knowledge/tb2-db-wal-recovery-grader.md) -> counter rejects as `not-a-new-task`; no receipt written.
- hf-model-inference: `test_model_downloaded` is a FALSE POSITIVE of the P1 rule: it has os.path.exists but also loads model and tokenizer via from_pretrained and asserts both non-None (L8-22). Not presence-only; refused. This shows the per-test P1 rule's content-marker vocabulary misses library-load calls (no read_text/open/json.load) — a misclassification case for the A1 attack.

Caveat: the presence-only tests are one test among a multi-test grader; whole graders are not vacuous (other tests check content/behaviour). The claim is per-test only, as A1 states.

Attack verdict: did not land against the instrument's candidates for 4 of 5 rows (true findings), landed on 1 (hf-model-inference false positive) and 1 under-detection (financial summary_csv_exists). Excluded capture (sanitize-git-repo) untouched.

Files: /fast/scratch/hyaku/kengaku-r52/w2-W2ExecConfirmC/confirmations.json (copied to .ufo/waves/round-52/w2/W2ExecConfirmC/confirmations.json). Tools installed: none.
