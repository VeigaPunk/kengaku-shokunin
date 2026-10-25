# Round 33 — renumbered assimilation, routed-defect closure, byte-retained catalogs (2026-10-25, hyaku run 7)

Baseline `112091c2d9`; frozen prereg `plans/round-33-claims.md` (freeze commits `f0b20aea` +
`c227e486`). Round shape: one v1 build wave of 36 seats + one v1 falsify wave of 36 seats
(dispatched inline via the orchestrator's `.ready` bridge; results recorded below).

## Gate

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| `benchmark-grader-semantics.md` (admission patch of the round-32 draft) | **Admitted** | Staged S094 → **S103** (Toolathlon `main.py` @ `9be8d8fe`), staged S097 → **S104** (arXiv 2412.05579v2), both opened this round. S093 was already `mined` and already named this entry in `used-by` at the round-33 freeze; no S093 cell changed in round 33. New rows S103/A and S104/B cite this entry; the entry's source lines were re-pointed by document. Four refusal rows S094/S097/S101/S102 stand unchanged. Gates: collision/schema `collisions=0 defects=0` exit 0; final landed-row quote gate 8/8 located, 0 overlong, 0 mismatch/unmapped (`.ufo/waves/round-33/assimilation/gate-receipts.txt`). |
| Staged catalog rows S101/S102 (SWE-bench locked replay + release map) | **Rejected** | Not cited by the admitted entry; CORPUS.md rule 4 forbids appending rows no admitted entry cites. Their round-32 refusal rows stand. Flip: a later entry that cites them re-grounds them under unused ids. |
| Staged `judge-calibration-thresholds.md` (un-admitted kappa table) | **Rejected (carry-over)** | Still refused: its kappa figures (0.84/0.46/0.21) appear in no anchor cell (Q3); unchanged from rounds 29–30. |

## Assimilation record (operator directive, §10)

- Theme: *benchmark grader semantics* (package `merge/kengaku/`, 1 entry, 3 cited rows).
- **Renumber map (by document, never arithmetic):** staged S094 → lane **S103** (Toolathlon
  evaluation/main.py @ `9be8d8fe`, tier A); staged S097 → lane **S104** (arXiv 2412.05579v2,
  tier B preprint). S093 was already `mined` and its `used-by` already named this entry at the freeze (the pointer was added in round 32); this round changed no S093 cell. New ids S103/S104 carry the actual row delta. Guard proof: `.ufo/waves/round-33/assimilation/idguard-*`.
  S001–S102, staged ids through S104+, collisions S094/S097/S101/S102 (staged package) → the two
  adopted rows take S103/S104; id-guard proof: `.ufo/waves/round-33/assimilation/idguard-*`.
- Re-grounded quotes (located this round): S103 `main.py:58` signature (0.1 default) vs `:280`
  executed call (0.05); S104 title, abstract and comments were re-located at arXiv 2412.05579v2. The abstract contains both `LLMs-as-judges` and `LLMs-as-Judges`; see the corrected S104 entry and row.
- `## Gate` records ≥1 admit (above) and ≥1 reject (S101/S102 catalog rows, threshold entry).

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| landing | `.ufo/waves/round-32/` — 89 files sat untracked at a pushed tip (round-32 closure §5) | round-32 verifier spotcheck `## 5`; Q19 | committed under round 33 (`c227e486`); counter `plans/round33_defects.py` N1 now guards it at every tip |
| number-drift | `corpus/README.md` and the existing draft cited refused ids S094/S097 | no prior check joined source IDs to registry row health | re-pointed to S103/S104; V8 now reads the refusal row's actual `teaches` cell and the selftest tests its erasure |
| scope | staged S094 row misstated the executed tolerance (0.1 default vs 0.05 invoked) and overbroadened a fail-open claim (absent credentials fail *closed* via implicit `None`) | round-32 falsify seats `FxFailOpen`, `FxTolerance`; entry lines 47-53 | corrected using S103's pinned capture |
| reference-drift | staged S097 anchor dropped one L in "LLMs-as-judges" (round-32 refusal record) | refusal row S097; S104 quote gate | corrected capitalization claim against arXiv v2 bytes; both spellings occur in abstract |
| stale-premise | r32 C3's frozen predicate required zero missing fields while HF's default projection legitimately dropped four | `catalogs/after.txt` hf_schema_delta=4 | preserve r32 failure; round33 uses byte-retention predicate instead |
| baseline-delta | frozen C1 prose says S093 `used-by` gains the entry, control `entries=0`, and 40 knowledge/index rows | `R33FS093Delta.md`, `R33FControl.md`, `R33FIndexTruth.md`; freeze `f0b20aea` | preserve frozen claims; report observed state: S093 already linked (pointer added in r32 `bcd2a6c`), control `entries=1`, baseline knowledge/index 41/41; no S093 mutation in r33; append r32 lesson correction |
| counter-strength | N1–N6/C3 counters admit false greens or false negatives; `--verify` is internal consistency, not origin authentication | `R33CounterAttack.md`, `R33FC3Provenance.md`, `R33FOpenRouter.md`, `R33FDefectSelftest.md` | retain frozen predicates; disclose instrument limits and hold axis scores |
| verifier-cell-index | `check_v8` read registry `anchor` at `row[5]` instead of `teaches` at `row[6]` | `R33C1Counter.md`; 11-cell `SOURCES.md` header | corrected V8 to `row[6]` and added green-row / erased-teaches selftest; frozen `checks=8 defects=0` output unchanged |
| staged-landed-drift | first admission package's anchor/teaches prose differed from landed rows; initial quote receipt ran on staged rows | `R33FLandedBytes.md`; `assimilation/append-rows.md` and `SOURCES.md` | synced append rows to final registry rows, made S103 blob-only/S104 version-pinned, regenerated append block, and re-ran landed-row gate 8/8 |
| entry-overreach | S093 capture statement, diagnostic-log carve-out, survey capitalization exclusivity, PROVINCE locator, and task-level scope were overstated | `R33FEntryTruth.md`; pinned captures | corrected the entry against pinned bytes; each benchmark claim now names one task |
| misroot | `R33FCensus.md` was written to fleet `.ufo/waves/` rather than lane reportDir | fleet-root status sweep; byte-identical copy hashes | copied byte-exact to lane and removed only the fleet-root copy; corrected baseline count to 41/41 |
| vcs-bypass | an L1 `git commit` created detached local revision `2b4cef2e` outside `master` | `jj-lane.sh state` showed `head=detached`, remote still `7895588` | abandoned only the self-created orphan, restored working-tree bytes, and re-landed through `jj-lane.sh`; remote tip verified at close |
| receipt-pointer | `defects-after.txt` named `c227e486` although the six repairs landed at `7895588`; C1 had no committed after receipt | `R33FQ22.md`, `R33FMeasurement.md` | corrected revision; added `adoption-after.txt` and re-ran both C1 commands |
| landing (own round) | `git cat-file -t a44b5a8` fails in both repos — round-31 report's "lane tip" is a phantom hash | round-31 verifier spotcheck §5 D1; `plans/round33_defects.py` N3 | appended erratum naming `ae95fe0` (`3d3ca566`); token remains verbatim per append-only |

## Seat ledger

Wave-1 build: 36 seats; wave-2 falsify: 53 seats; total **89**. Both are v1 waves under the run-7 32–64 band; no residual call.

| wave | role mix | flash-majority / attack share | reports / dead |
|---|---|---|---|
| build | executor 9, scribe 10, scout 4, reviewer 4, critic 4, mutation-tester 2, connector 1, sentinel 1, revenger 1 | 19/36 m_flash roles (52.8%); 10/36 attack roles (27.8%); 1 connector | 36 reports / 0 dead |
| falsify | executor 24, scribe 3, reviewer 11, critic 4, mutation-tester 8, sentinel 2, connector 1 | 27/53 m_flash roles (50.9%); 25/53 attack roles (47.2%); 1 connector | 53 reports / 0 dead |

Results and registries: `.ufo/waves/round-33/{build-results.json,falsify/swarm-registry.json}`. One falsify report (`R33FCensus.md`) was misrooted to fleet `.ufo/waves/round-33/falsify/`, copied byte-exact into lane reportDir, and the fleet copy removed; see `## Mistakes`.

## Round-33 disclosures

- The round-32 closure (`corpus/lessons/round-32-verifier-spotcheck.md`) routed 6 items;
  N1–N6 all re-derive green (`corpus/evidence/round33/defects-after.txt`, `checks=6
  defects=0`, exit 0, at the landing tip).
- The refusal rows S094/S097/S101/S102 stand unchanged in round 33. S093's `used-by` already named both entries at freeze; its pointer was added in round 32 (`bcd2a6c`), although only the new row admission was refused. No S093 cell changed in round 33.
- `corpus/QUALITY.md` gains **Q22** (a receipt is only evidence if something re-runs it at the
  tip) — considerthese/2026-10-25 proposal 2's cheap half; the persistent `defects.jsonl`
  ledger it sketches stays unimplemented debt, named in the criterion.
- considerthese/2026-10-25 proposal 3 landed as an L0 decision-packet append (fleet
  `l0-questions.md`, commit `22d28422`); proposal 1 (model-diverse verification) is
  operator-side and not lane-actionable.
- The SOURCES census is clean at both ends: freeze `.ufo/waves/round-33/claims/census-before.txt`
  → `corpus/evidence/round33/census-after.txt`, exit 0 at each, the same 15 `W04` ids.
- The freeze's knowledge/index baseline (`plans/round-33-claims.md:4`) is understated: the
  `112091c2` Git tree has 41 knowledge files and 41 README index rows, both unchanged at round 33.
  The frozen control also prints `entries=1`, not the copied `entries=0` prose; see the before
  receipt and the falsification reports.
- Final C1 commands are retained at `corpus/evidence/round33/adoption-after.txt`. The final C2
  receipt names repair commit `7895588` (not `c227e486`) and is re-derived at the landing tip.
- C3 stores the full bounded OpenRouter `?limit=10` response and reads its `total_count=467`;
  the probe's `--verify` confirms internal consistency, not endpoint authenticity, and the claim's
  absolute no-fabricated-bytes kill-rule is not enforceable by this offline verifier.
- No tools were installed or updated this round.
