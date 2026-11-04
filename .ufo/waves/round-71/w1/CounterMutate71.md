# CounterMutate71 — R71-C1 checker mutation matrix

_Returned in `w1-results.json`; the seat did not write this file itself. Content is the seat's final output, byte-exact._

{
  "seat": "CounterMutate71",
  "role": "mutation-tester",
  "target": "plans/round71_c1_hf_probe.py check_receipt (sha256 d5ce2fa5871bb3d2b7b956f9f92d6e23ee21b7508b5da6dc113f6c3a2c1aa82e, lane master d8a77d3f2b4c8747dbc3a5bcf458b23160a459e0)",
  "report": ".ufo/waves/round-71/w1/CounterMutate71.md",
  "scratch": "/fast/scratch/hyaku/kengaku-r71/CounterMutate71 (kept: matrix.json, matrix.tsv, mutants/, fixtures/, selftest/, logs)",
  "assigned_mutants": {
    "M1_grader_sha": "KILLED",
    "M2_case_set": "KILLED",
    "M3_case_digest": "KILLED",
    "M4_vector_derived": "KILLED",
    "M5_leg_coverage": "KILLED",
    "M6_summary": "KILLED",
    "M7_probe_blob": "KILLED",
    "M8_libraries": "KILLED"
  },
  "assigned_result": "8/8 killed; each mutant accepted a receipt the pristine checker refuses (pristine rc 1, mutant rc 0) while still accepting the genuine receipt (rc 0 with and without --work)",
  "bonus_mutants": {
    "killed": [
      "M10_vector_agree",
      "M11_receipt_rev",
      "M12_probe_blob_rev",
      "M13_probe_working_tree",
      "M14_case_digest_unique",
      "M16_predicate_line",
      "M17_instruction_sha",
      "M18_model_tree",
      "M19_defect_gate",
      "M21_setup_term"
    ],
    "survived": [
      "M9_vector_mismatch",
      "M20_mism_term",
      "M22_seen_p_term",
      "M23_seen_f_term"
    ],
    "note": "survivors are redundancy only: vector-mismatch + predicate mism term + SUMMARY encode the same comparison; deleting M9 and M20 together (D1_M9_plus_M20.py) accepts fx_mism_term (rc 0), proving the pair, not either half, is load-bearing. seen_p/seen_f terms are unreachable without a vector deviation first (fx_coverage_terms refused with 6 vector-mismatch defects under both mutants)."
  },
  "baseline": {
    "genuine_record_check_work_none": "DEFECTS n=0 / PREDICATE R71-C1 pass / rc 0",
    "genuine_record_check_work": "DEFECTS n=0 / PREDICATE R71-C1 pass / rc 0",
    "record_sha256": "136ec423409cbc3031925148b0571ad6edb1cfdf209b42586addb7e2499e6067",
    "reproduction": "receipt.txt == receipt-replicate.txt == my independent --selftest battery receipt, byte-identical",
    "counter_row": "grep -c 'executed 3 of 8' SKILL.md = 0; grep -c 'executed 4 of 8' SKILL.md = 1"
  },
  "restoration_evidence": {
    "lane": "never written; lane-byte fixtures taken on scratch git clone with toplevel verified",
    "grader_sha_before_after": "61a686d6... == 61a686d6...",
    "instruction_sha_before_after": "29151c5b... == 29151c5b...",
    "model_file_sha_before_after": "2a5cd25c... == 2a5cd25c...",
    "restored": true
  },
  "predicate_holds": true,
  "residual_findings": [
    {
      "id": "unbound-receipt-digests",
      "detail": "check_receipt verifies the lane files against constants and binds only PROBE/PROBE_BLOB to the receipt; receipt GRADER/INSTRUCTION/MODEL lines are never read. Corrupting each of the three to 0x64 still exits 0 (DEFECTS n=0). All five lines in the record of record are factually correct (independently re-derived at the tip), so the predicate sentence is true of the artifact but unenforced for 3/5 digests.",
      "probes": "S/extra-probes.json (5/6 forged-field receipts accepted; extra CASE K9 correctly refused)"
    },
    {
      "id": "selftest-nonfunctional",
      "detail": "--selftest exits 1 on every lane: (a) ARM case_digest refused=False because refuse() calls check_receipt(..., None) and the case-digest re-stage is gated on work is not None; (b) stage_case(work/'stage-a') is called without prepare_work -> SystemExit 'grader copy missing at .../stage-a/grader/test_outputs.py', so the staged-digest arms and SELFTEST line never print. The case-digest clause itself is load-bearing under --work (M3). C1's frozen predicate does not cite the selftest.",
      "evidence": "S/selftest.log"
    }
  ],
  "commands": [
    "python3 L/plans/round71_c1_hf_probe.py --lane L --selftest --work S/selftest --port-lock /fast/scratch/hyaku/kengaku-r71/port-5000.lock  (rc 1)",
    "python3 ... --check-receipt L/corpus/evidence/round71/hf/receipt.txt  (rc 0)",
    "python3 ... --check-receipt L/corpus/evidence/round71/hf/receipt.txt --work S/recheck-record  (rc 0)",
    "python3 S/build_mutants.py + S/build_predicate_mutants.py (22 mutants, 1 hunk each, py_compile clean)",
    "python3 S/run_matrix.py (18 mutants x 22 receipts + 3 lane clones)",
    "python3 S/run_predicate_matrix.py (M20-M23)",
    "python3 S/extra_probes.py (unbound receipt fields)"
  ],
  "tooling": "none installed or upgraded; host python3 3.13.16, git, bwrap, /fast/ComfyUI/.venv read-only; port-5000 lock taken for every battery run"
}
