# Round 35 — one TB2 grader read and executed; routed defects move into a ledger (2026-10-25, hyaku run 7)

Baseline `58a19f37312e1b22fd2a7957bdfc6bb7832aadd0`; frozen claims `plans/round-35-claims.md`
(freeze `11d64530179b78e33ba6074fc77d63d36ee7ac31`). Controls scored red before any repair or
grader run: `.ufo/waves/round-35/claims/control-*.txt` (`control-c1-nothing.txt`,
`control-c1-skip.txt`, `control-c2-nothing.txt`, `control-c2-flip.txt`).

## Gate

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| `knowledge/tb2-protein-assembly-grader.md` (C1) | **Admitted** (candidate) | The frozen predicate binds admission: `python3 plans/round35_c1_verify.py --lane .` must print `checks=6 defects=0` and `PREDICATE C1 pass`, exit 0 (V1–V6, `plans/round-35-claims.md:26-31`). Q1 triad lines 1–5 (`knowledge/tb2-protein-assembly-grader.md:1-5`); Q2 S105–S107 tier A for their own scope; Q3 22 located quotes, each re-checked by V3 against the capture line; Q4 Negative space with a falsifier (`:80,90`); Q5 maintainer task code labelled self-report beyond its own behaviour; Q6 extends `knowledge/benchmark-verifier-execution-model.md` / `knowledge/benchmark-grader-semantics.md` and the `corpus/README.md` §Frontier round-33 clause; Q7 entry, index row and coverage row land together (`corpus/README.md:68,257,282`). Round-34 critic findings fixed: bare pinned URLs without `/tasks/`, no unquoted S092/S100 assertions, evaluator files in the manifest. Kill rule: any V red at the landing tip → not admitted; a probe case whose observation differs from its frozen prediction is reported as a mismatch, never re-predicted. |
| S105 `tests/test_outputs.py` @ `2fd12b88` | **Admitted (mined)** | Opened 2026-10-25 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/tests/test_outputs.py`; quote, line 42: “assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx, (”; sha256 `44a05a24…96582`. Row `corpus/SOURCES.md:120`. |
| S106 `tests/test.sh` @ `2fd12b88` | **Admitted (mined)** | Opened 2026-10-25 at `…/protein-assembly/tests/test.sh`; quotes, lines 27 and 21: “echo 1 > /logs/verifier/reward.txt” and “-w biopython==1.85”; sha256 `9ede4664…267b5`. Row `corpus/SOURCES.md:121`. |
| S107 `instruction.md` @ `2fd12b88` | **Admitted (mined)** | Opened 2026-10-25 at `…/protein-assembly/instruction.md`; quote, line 29: “The GS linkers between different subproteins should be between 5 and 20 amino acids long.”; sha256 `1bb2af1d…003f7c5`. Row `corpus/SOURCES.md:122`. |
| Assimilation package candidates (merge/kengaku re-screen) | **0 admitted; 6 refused as staged** | Round-34 read-only package screen (`.ufo/waves/round-34/build/R34ReconPackage.md`) refused all six staged entries: `terminal-bench-release-identity.md` (Q6: duplicates/corrects existing coverage, no named extension), `toolathlon-grader-contract-2026-10-23.md` (Q1/Q2: no live row S114), `judge-meta-evaluation-2026-10-23.md` (Q3: cited S103 does not support survey claims), `benchmark-grader-integrity-models-2026-10-23b.md` (Q1/Q2: no live row S108), `cjk-benchmark-governance-2026-10-23c.md` (Q1/Q2: S115–S117 not lane-held), `cjk-dataset-documentation-standard-2026-10-23.md` (Q2/Q3: no live rows; dataset-documentation evidence cannot substantiate a contamination-card claim). Re-screen for a theme fitting C1: `terminal-bench-release-identity.md` is the closest (same repository as S100/S105–S107) but stays refused — it corrects a task-count, not a grader read, and no admitted entry cites it. Flip: a staged row gains a live registry row and is cited by an admitted entry. `merge/kengaku/MERGE-REPORT.md` is absent at its referenced fleet path at draft time; the section quotes its `:3` and `:26–35` via `R34ReconPackage.md:16-19`. |
| Quarantine S091 (NEC 技報, RAKUDA caveat) | **Re-grounded, not appended** | The staged quote 「ただし、RAKUDAベンチマークは1ターンの対話かつ少数データでの評価のため、対話性能の一側面しか測れていないことには注意が必要となります。」 is present in `.ufo/waves/round-34/assimilation/captures/nec-s091-reopen.html` (60,335 B, sha `b60af775…` in `captures/quarantine-SHA256SUMS`; tag-stripped, raw HTML line 276). Round 34's “quote absent” reason was false (spot-check D5; erratum appended to `corpus/lessons/round-34.md`). Not appended: no admitted entry cites it (CORPUS rule 4). Flip: an admitted entry cites it. |
| Quarantine S105 (METI GENIAC archive) | **Not appended** | The located quote 「以下の2つのベンチマークを用いて、日本語の性能評価を行いました。」 is present in `.ufo/waves/round-34/assimilation/captures/geniac-s105-reopen.html` (13,030 B, sha `2f46a13e…`), but no admitted entry cites the row (CORPUS rule 4). Flip: an admitted entry cites it. (Distinct from S105 `tests/test_outputs.py`, which is adopted this round as the TB2 row; the staged GENIAC row was never in the live registry.) |

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| false-refusal-reason | `corpus/lessons/round-34-verifier-spotcheck.md:64,79` (D5); the false reason in `corpus/lessons/round-34.md:11,21,37` (“Access Denied 418 bytes”, “opened NEC response was unavailable”) vs the round's own reopen capture `assimilation/captures/nec-s091-reopen.html:276` | round-34 non-author verifier spot-check → ledger row `R34-D5` (`corpus/defects.jsonl:5`) | Re-ground a refusal on the best available capture, not the first fetch: judge S091 from `nec-s091-reopen.html` (quote present) before deciding; append an erratum to `corpus/lessons/round-34.md` that names `nec-s091-reopen.html` and “present” (r34_d5 requires exactly one such line), and add this S091 row to the round-35 Mistakes table; verify `python3 plans/defect_ledger.py --lane .` prints `PREDICATE C2 pass`. Shown able to fail: at freeze `claims/control-c2-nothing.txt:5` — `R34-D5 status=open observed=fail agree=yes erratum_lines=0 r35_mistake_row=False`. |
| committed-scratch-bloat | `corpus/lessons/round-34-verifier-spotcheck.md:31,76` (D2): `.ufo/waves/round-34/mut-entries-scratch/` held 106,323 blobs, 1650.6 MiB logical of recursive self-mirrors (mut1–mut5 copies of the repo incl. older wave scratch, PDFs, PNGs) | round-34 non-author verifier spot-check → ledger row `R34-D2` (`corpus/defects.jsonl:2`) | Mutants must run in a `mktemp` clone outside the repo and commit only receipts — never the scratch tree. The guard is r34_d2: zero committed paths under the three mirror roots (`mut-entries-scratch`, `build/R34MutRegistry/mirror`, `build/R34MutRegistry/mut`) at the branch tip; any newly committed mirror re-opens the row. Shown able to fail: at freeze `claims/control-c2-nothing.txt:2` — `committed_mirror_paths=109413`. |
| receipt-claims-unbacked-manifest | `corpus/lessons/round-34-verifier-spotcheck.md:42,77` (D3): `R34CaptureTB2Eval.md` says “same hashes are in SHA256SUMS” while the committed `tb2-eval/SHA256SUMS` listed only `antibody.fasta pdb_ids.txt task.toml instruction.md`; the evaluator files' real hashes (`44a05a24…`, `9ede4664…`) were verified against upstream | round-34 non-author verifier spot-check → ledger row `R34-D3` (`corpus/defects.jsonl:3`) | A receipt claim must be backed by the manifest it names: append `test_outputs.py` and `test.sh` to the round-34 capture manifest (`.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS`) and to the round-35 evidence manifest `corpus/evidence/round35/tb2-eval/SHA256SUMS`, each at its pinned digest; r34_d3 requires both evaluator files listed and every listed digest equal to the file bytes. Shown able to fail: at freeze `claims/control-c2-nothing.txt:3` — `listed=4 evaluator_listed=False bad=0`. |
| uncommitted-round-work | `corpus/lessons/round-34-verifier-spotcheck.md:30,75` (D1): 1423 untracked at closure (1425 at freeze control), incl. `plans/round34_c1_verify.py`, `plans/round34_defects.py`, `plans/round34_mutate.py` and round-34 wave leftovers | round-34 non-author verifier spot-check → ledger row `R34-D1` (`corpus/defects.jsonl:1`) | Commit round work (as drafts under the wave tree) or remove it, and leave `git status --porcelain` empty under the round-34 wave tree and the three plan-tool paths; r34_d1 counts untracked there. Shown able to fail: at freeze `claims/control-c2-nothing.txt:1` — `untracked=1425`. |
| scorecard-misattribution | `corpus/lessons/round-34-verifier-spotcheck.md:50-52,78` (D4): the round-34 SCORECARD C2 row says the counter draft's selftest was not green, while `build/R34C2CounterDraft.md:8` shows `cases=10 failed=0`; the red selftest is the mutation harness (`build/R34MutC2Harness.md:12-13`) | round-34 non-author verifier spot-check → ledger row `R34-D4` (`corpus/defects.jsonl:4`) | Append a SCORECARD correction line starting `- **D4 correction (round 34 C2):**` that names both lines and both outcomes; r34_d4 requires exactly one such line carrying `R34C2CounterDraft.md:8`, `cases=10 failed=0`, `R34MutC2Harness.md:12`, `SELFTEST green failed`. Shown able to fail: at freeze `claims/control-c2-nothing.txt:4` — `correction_lines=0`. |

## Assimilation record

- **Considerthese proposal 2** (2026-10-25) mined into a persistent routed-defect ledger (C2):
  `corpus/defects.jsonl` holds the five round-34 spot-check defects D1–D5 (each with id, class,
  opened_round, source `:75-79`, check function, status, closed_round, recurrence_of), and
  `plans/defect_ledger.py` re-runs every row's check at the current tip and counts mismatches
  against the ledger's own status. The frozen predicate is `rows=5 closed=5 observed_pass=5
  mismatches=0` + `PREDICATE C2 pass`, exit 0 (`plans/round-35-claims.md:47-51`); at freeze every
  row was `open` and red (`claims/control-c2-nothing.txt`), demonstrating each check can fail.
- **merge/kengaku re-screen**: the six staged package entries screened in round 34
  (`.ufo/waves/round-34/build/R34ReconPackage.md`; staged without writing into the lane,
  `MERGE-REPORT.md:3`) were re-screened for one theme fitting C1; the closest candidate
  (`terminal-bench-release-identity.md`, same terminal-bench-2 repository as S100/S105–S107)
  remains refused on Q6 — it corrects the 89-vs-92 task count, not a grader read — and no package
  row is appended because no admitted entry cites one (CORPUS rule 4). `merge/kengaku/MERGE-REPORT.md`
  is absent at its referenced fleet path at draft time; its `:26–35` candidate list is carried by
  `R34ReconPackage.md:16`.
- **Quarantine slice**: S091 re-grounded from `nec-s091-reopen.html` (quote present; refusal reason
  false — D5) and S105 (METI GENIAC) quote located; neither row appended because no admitted entry
  cites it. Round-34 lesson carries the appended erratum (D5); the round-35 lesson records the
  Mistakes row here.
- No new source-copy containment or other assimilation entry beyond the above; C1's S105–S107 are
  the round's opened sources and are admitted above.

## Census

Before: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` — 15
W04, `kengaku ok`, exit 0; output byte-identical to committed
`corpus/evidence/round35/census-before.txt` (`claims/census-before.txt`).

After: same command at the landing tip — `<L1>` (`corpus/evidence/round35/census-after.txt`, exit code). SOURCES rows: `<L1>` (97 before; +3 rows S105–S107 expected). Additions by tier A/B/C: `<L1>` (`<L1>`/0/0). Rows touched: `<L1>`. Frontier rows advanced: `<L1>`.
