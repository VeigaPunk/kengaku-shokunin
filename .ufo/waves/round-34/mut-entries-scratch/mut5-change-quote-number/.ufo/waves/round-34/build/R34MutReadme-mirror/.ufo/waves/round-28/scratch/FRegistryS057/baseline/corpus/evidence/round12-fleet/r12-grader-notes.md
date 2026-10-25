# r12-grader-notes.md — round-12 gate extension (draft v2) notes for L1

**Agent:** ExecutorGrader (executor). **Role:** draft the round-12 gate extension as a
standalone, importable file and hand L1 the promotion plan.
**Task restated:** draft `corpus/evidence/round12-fleet/grader_r12_draft.py` exposing
`grade_r12(...)` + helpers covering (1) meta regeneration incl. the `+977` chain and the
r11 cross-tree identity, (2) raw re-parse/re-grade for both families incl. the malformed
and bare-array paths, (3) census + `descriptors`/`descriptors_end`, (4) `run.log`,
(5) every `analysis_r12.md` §5 line + R1–R5, (6) the pinned probability files and the
scoring-source discipline, (7) ordering discipline, (8) a `--selftest-r12` mutation
battery; plus this notes file (inventory, copies, promotion plan, offline limits).

**Artifact revision pinned here:** `grader_r12_draft.py`
md5 `7e8910fe713f0e25e7d834f8c9326c99`,
sha256 `011762bea08952a3195422247a97331f50050ee0fc1ccc76fc7fdd414b38821c`,
4 290 lines. Line numbers below are as of that revision.

---

## 1. Acceptance evidence

```
$ python3 corpus/evidence/round12-fleet/grader_r12_draft.py --selftest-r12
[selftest-r12] PASS stats anchors (Page's L / seq semantics / Brier-BSS / reliability / logistic Newton)
[selftest-r12] PASS S0 control (clean synthetic tree): checks=429 mismatches=0
[selftest-r12] PASS S0c control (default paths, structural probs lookup, no explicit probs map): checks=427 mismatches=0
[selftest-r12] PASS S0b control (override mode, n_eff < minima): checks=429 mismatches=0
[selftest-r12] PASS S0d control (degenerate tree: D9 pinned lines, no NaN/inf): checks=429 mismatches=0 bad_tokens=[]
[selftest-r12] PASS S0e control (machinery loader is side-effect free): marker absent: …/IMPORT-SIDE-EFFECT.txt
[selftest-r12] ALL PASS (106 scenarios)
$ echo $?
0
```

* 106 scenarios = 5 controls + 98 battery mutations + 3 degenerate-tree mutations; no
  real run is needed (the tree is synthetic, built into a `tempfile.mkdtemp`).
* Deterministic: byte-identical selftest output under `PYTHONHASHSEED=0/7/999`
  (md5 `e4895b1db4bab5bae5120f7fd5aa1b4b` for all three).
* Verbatim-copy proof (mechanical, `ast.get_source_segment` on grader.py): all 21 copied
  functions plus `KEYS`, `MINUS`, `_SIGN_GLYPHS` and `Report` (minus `erratum`) are
  byte-identical to their grader.py spans; `Report.erratum` is dropped because it needs
  grader.py's module-level `ERRATA`.
* `grader.py` itself is untouched and still green: `python3 grader.py` → `CHECKS n=280
  mismatches=0 errata_pinned=1`, exit 0; `--selftest` → ALL PASS.
* The draft is importable the way grader.py will use it (no import-time side effects, no
  argparse at import, no network): `importlib` load from another CWD works and exposes
  `grade_r12`, `check_r12_ordering`, `check_r12_pins`, `selftest_stats_r12`.

### Real-byte pre-run validation (the run is in flight; `results-r12.jsonl` does not exist yet)

| what | command / call | result |
|---|---|---|
| bundle verification from the repo root | `check_r12_ordering(...)` against the landed 9-file `prereg-bundle.sha256` + `ordering.log` (synthetic stamped records) | 32 checks, **0 mismatches** (`file:corpus/evidence/round12-ladder/prereg-bundle.sha256`, `ordering.log`) |
| `sha256sum -c` agreement | `sha256sum -c corpus/evidence/round12-ladder/prereg-bundle.sha256` | all 9 files `OK` |
| probability-source classification | `_resolve_prob_sources(...)` on the real bundle | pass = `predictions-r12-perproblem.jsonl` (416), sign = `predictions-r12-signevents.jsonl` (304), digests match the pinned `bac550c7…` / `1d99040c…` |
| run-level parse | `_read_runlevel_probs(predictions-r12.md)` | `{RL1:0.55, RL2:0.70, RL3:0.45, RL4:0.50, RL5:0.20, RL6:0.45, RL7:0.50}` = the filed §5 table |
| machinery loader | `_load_machinery(probe_r12.py, ["gen_seq_problem","SYSTEM","gen_problem","sim_apply2"])` | loads with **no side effects** (the synthetic-probe variant writes a marker file on import; the loader never creates it — see S0) |
| family-2 semantics | my drafted `sim_seq_apply` vs `probe_r12.py:sim_apply2` over all 48 pids × 10 ops | 0 mismatches |
| family-1 generator identity | `probe_r12.py:gen_problem` vs grader.py's port over all 64 pids | 0 mismatches |
| census formulas vs committed smoke counts | `census_expected(2,2)["records"]` / `(1,1)` / `(64,48)` | 142 / 72 / 4114 — exactly the counts L1 quotes for the mock and real smokes and plan §4 |
| real descriptor field names | `_check_descriptors` against `run_r12.py:descriptors()` field names | all present: `pids`, `pids_f2`, `n`, `n2`, `seed_scheme`, `seed_scheme_f2`, `temp`, `maxtok`, `system_prompt`, `endpoint`, `server`, `models_json`, `arm_order_counts`, `counterbalance`, `schedule`, `n_jobs`, `machinery_sha256`, `runner_sha256`, `predictor_sha256`, `prereg_bundle_sha256`, `probe_lineage` |

`descriptors_end` is verified against `run_r12.py:descriptors_end()`: `models_json`
(mid-run drift), `server.pid`, `request_ts`, `wall_total_s`, and `n_records` = the file's
line count before that record (= lines − 1).

---

## 2. Check inventory (family → ids → count)

Counts are the invocations on the **synthetic clean tree** (n1=3, n2=3): 429 invocations,
429 distinct ids (no id is emitted twice). At the filed n the two `section4` checks fire as
well
(`r12.census.section4_records_calls`, `r12.runlog.section4_jobs`), so a landed run is
checked by **431** assertions; per-cell sub-ids scale with the cell list, not with n.

| # | family | distinct ids (clean tree) | what it pins | killed by |
|---|---|---:|---|---:|
| F1 | `r12.pin.*` | 2 | landed-byte md5/sha256 of `results-r12.jsonl` / `analysis_r12.md` (mechanism; L1 fills `R12_PINS`) | 1 |
| F2 | `r12.meta.*` | 17 | family-1 meta regeneration (`gen_problem(3000+pid*41)`), stored `seed` on the `+977` chain, `truth`/`tail_touched`, r11 cross-tree identity (init/ops/truth/tail_touched), retry chain exercised | 6 |
| F3 | `r12.meta2.*` | 15 | family-2 meta regeneration through the hash-pinned `probe_r12.py:gen_seq_problem`, `+977` depth by reproduction, plan §2.2 invariants, `features` keys, uniqueness, disjointness from family 1 | 5 |
| F4 | `r12.replay.*` | 60 | per graded cell (`A-INC`, `A-CKPT4710`, `A-CKPT710`, `A-CKPT10`, `A-MONO`, `T-DENSE`, `T-SPARSE`) × {`turn_set`, `got`, `want`, `ok`, `nwrong`, `parse_fail_path`, `bare_bracket_path`}, per ack cell × {`turn_set`, `raw_truncated`}, `filler.fields` | 9 |
| F5 | `r12.census.*` | 28 | §4 per-cell counts, pinned totals (4 114 / 4 002 / 416), stamped vs unstamped records, `A-INC-ack`=0, `graded_missing_ok`, `ack_has_ok`, `descriptors`/`descriptors_end` presence | 6 |
| F6 | `r12.descriptors.*` | 34 | the §3 run-time unit: pids/n, seed schemes, temp/maxtok, system prompt (== `probe_r12.py:SYSTEM`), endpoint/server, all four script/bundle sha256 fields, `arm_order_counts` (+ per-arm sums), `n_jobs`, family-2 counterbalance, lineage, `descriptors_end` (last record, model id, server pid, `n_records`) | 9 |
| F7 | `r12.runlog.*` | 15 | the 7 SUMMARY cells re-derived from the JSONL, `wall_total_s` present and > 0, job count/denominators, §2.1 rotation and §2.2 parity order realized per pid, known pids/cells | 4 |
| F8 | `r12.pred.*` | 15 | probability-source uniqueness (pass/sign), bundle-pinned sha256 for both files, sha256 **as stated inside `predictions-r12.md`**, event sets/ranges, family-2 constancy, scoring-source provenance, unmapped = none, RL1–RL7 present | 6 |
| F9 | `r12.ordering.*` | 26 | every bundle line verifies from the repo root, repo-relative paths, required members, `pre ≤ post ≤ min(run-script-hash) ≤ max ≤ first request_ts` (plain `<=`, r11 anti-pattern 15), `run-script-hash` digests == the committed script bytes, first stamped record is `descriptors` | 5 |
| F10 | `r12.analysis.*` | 217 | census sentence, arm table (7 rows × 4 fields), E1 (L/E_L/var_L/z/p/direction + n_blocks/pids_missing), E2 (diff/sd/n, t/df/p, CI, sign W/L/T + `direction`, McNemar), E3 (3 gaps), E4/E5 (+ `n_panel`), E6 (counts, pass/sign/runlevel/all Brier incl. per-arm/per-contrast/per-event, BSS pooled + 3 splits + sign/runlevel/all, calibration pass + all, 5 reliability bins with `n/a`), finish audit, ack compliance (5 cells), excluded pids, realized arm positions, `NOTE degenerate` consistency, 5 verdict lines + R2 clause, descriptor + ordering sentences, scoring table (per-row predicted/observed/abs-error/identifiability) | 47 |

**Total: 10 families, 429 distinct ids (429 invocations on the synthetic tree; 431 at the
filed n).**

The full id list is reproducible:

```
python3 - <<'EOF'
import importlib.util, tempfile, shutil, collections
spec = importlib.util.spec_from_file_location("g12", "corpus/evidence/round12-fleet/grader_r12_draft.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ids = []
oeq, ook = m.Report.eq, m.Report.ok
m.Report.eq = lambda s, c, a, b: (ids.append(c), oeq(s, c, a, b))[1]
m.Report.ok = lambda s, c, a, b: (ids.append(c), ook(s, c, a, b))[1]
tmp = tempfile.mkdtemp()
st = m._build_r12_fixture(tmp); rep = m._run(st)
print(rep.checks, len(set(ids)), len(rep.mismatches))
print("\n".join(sorted(set(ids))))
shutil.rmtree(tmp, ignore_errors=True)
EOF
```

---

## 3. Verbatim copies vs newly written code

**Copied byte-exact from `grader.py`** (block marked at draft:340–628, "verbatim copies
from grader.py"; L1 deletes the whole block at promotion). Spans were taken mechanically
with `ast.get_source_segment`:

| helper | grader.py span | helper | grader.py span |
|---|---|---|---|
| `KEYS` | 110 | `file_sha256` | 852–857 |
| `Report` (minus `erratum`) | 267–291 | `parse_runlog_summary` | 564–575 |
| `extract_json_block` | 116–129 | `_mean` | 862–863 |
| `sim_apply` | 132–148 | `_sd_sample` | 866–871 |
| `tail_touched` | 151–154 | `_betacf` | 874–907 |
| `gen_problem` | 157–205 | `betai` | 910–920 |
| `states_along` | 208–213 | `t_two_sided_p` | 923–925 |
| `grade_state` | 216–220 | `t_crit` | 928–937 |
| `die` | 294–296 | `_binom_cdf_le` | 940–941 |
| `read_text` | 299–306 | `exact_sign_p` | 944–950 |
| `load_jsonl` | 309–318 | `exact_mcnemar_p` | 953–957 |
| `_num` / `_SIGN_GLYPHS` / `MINUS` | 960–964 / 842 / 841 | | |

**Newly written in round 12** (draft:626–4277, everything after the copy block):

* statistics: `_midranks`, `page_l_trend` (Page's L, per-block midranks, tie-corrected
  `coef·S²_block` — identical to the plan's `5·S²_block` at k=4; direction `increasing` /
  `decreasing` / `neutral`), `paired_stats`, `mcnemar_pairs`, `_logit/_sigmoid/_loglik`,
  `calibration_gradient`, `logistic_fit` (damped Newton, ≤50 iters, tol 1e-10),
  `logistic_calibration`, `brier_scores`, `reliability_bins`, `_bss`, `_score_set`,
  `_close_dp` (half-ulp at the stored precision), `_safe_num`, `_close_na` (accepts `n/a` iff the
  recomputation is undefined);
* family-2 semantics transcribed from plan §2.2: `sim_seq_apply`, `seq_states_along`,
  `grade_seq`, `f2_invariants`, `_tail_positions`;
* machinery coupling: `_load_machinery` (ast-scoped exec — module-level imports, defs and
  literal-only assignments; a probe script's import-time `open(...)`/`sys.exit()` is never
  run), `_literal_ast`, `_unpack_gen`, `_retry_depth`;
* record introspection: `_walk`, `_hex_set`, `_model_ids`, `_int_values`, `_list_values`,
  `_string_values`, `_get_key`, `_meta_index`, `_want_for`, `_feat_eq`, `_norm_counts`,
  `_hash_file`, `_parse_realized_positions`;
* checks: `_check_meta_f1/f2`, `_check_replay`, `_check_census`, `_check_descriptors`,
  `_check_descriptors_end`, `_check_summary`, `_check_analysis`, `_check_prob_sources`,
  `_load_probs`, `_resolve_prob_sources`, `_read_runlevel_probs`, `_grab12`,
  `_verdict_line`, `_pred_lookup`, `_identify_score_row`, `_paired_pair_value`;
* entry points: `grade_r12`, `check_r12_ordering`, `check_r12_pins`, `_analysis_inputs`,
  `_recompute_r12`, `r12_verdicts`, `r11_e2_point`, `census_expected`, `arm_order`,
  `arm_order_counts`, `f2_order`;
* selftest: `selftest_stats_r12`, `_profile_grid_fit` (independent profile-likelihood
  cross-check of the Newton fit), the fixture builder/writer, the mutation battery.

---

## 4. Promotion plan (exact; do not edit the draft)

1. **Delete** the block from `# ---------- verbatim copies from grader.py` (draft:340) to
   `# ---------- round-12 meta / meta2 ----------`; grader.py already defines every name.
2. **Paste** draft:629 (`# ======================= R12-CODE`) through the end of
   `r12_verdicts` — i.e. everything before `# ======================= fixture selftest`
   — into `grader.py` **immediately after `check_r11_ordering`** (grader.py:1425 region,
   before `selftest_stats` at grader.py:1485). Function names to land, in order:
   `_midranks, page_l_trend, paired_stats, mcnemar_pairs, _logit, _sigmoid, _loglik,
   calibration_gradient, logistic_fit, logistic_calibration, brier_scores,
   reliability_bins, SIGN_CONTRASTS, RL_IDS, BSS_SPLITS, _bss, _score_set,
   _paired_pairs_turns, sign_event_pairs, _close_dp, _close_na, _safe_num, _retry_depth,
   _parse_realized_positions, sim_seq_apply, seq_states_along, grade_seq, _literal_ast,
   _load_machinery, _unpack_gen, _tail_positions, f2_invariants, _walk, _hex_set,
   _model_ids, _int_values, _list_values, _string_values, _get_key, _hash_file,
   _meta_index, _want_for, _check_meta_f1, _feat_eq, _check_meta_f2, _FENCE_RE, _BARE_RE,
   _check_replay, _check_census, _norm_counts, _check_descriptors, _check_descriptors_end,
   _check_summary, _PROB_KEYS, _SIGN_KEYS, _load_probs, _resolve_prob_sources,
   _read_runlevel_probs, _check_prob_sources, _nw_maps, _error_pids,
   _paired_pair_value` — note the draft no longer defines `_paired_diffs` /
   `_paired_diffs_turns` (they were superseded by `_paired_pairs_turns`, which returns
   `(pid, a, b)` triples so the E3/E4/E5 contrasts and their sign events come from one
   implementation) — `r11_e2_point,
   r12_verdicts, _recompute_r12, _grab12, _verdict_line, _pred_lookup,
   _identify_score_row, _check_analysis, _TS_RE, check_r12_ordering, check_r12_pins,
   _analysis_inputs, grade_r12`.
3. **Imports:** grader.py needs one new import, `ast` (next to `argparse`/`hashlib`).
4. **REPO_ROOT:** reuse the r11 section's `REPO_ROOT`/`_find_repo_root` (grader.py:806
   region); drop the draft's `_find_repo_root` copy (draft:117).
5. **DEFAULTS / sidecars:** add
   `"r12_jsonl"`, `"r12_md"`, `"r12_runlog"` → `corpus/evidence/round12-ladder/{results-r12.jsonl,
   analysis_r12.md, run.log}`; the sidecar constants `R12_SHA`, `R12_ORDERING`, `R12_PRED`,
   `R12_MACHINERY`, `R11_JSONL`, `R11_MD` are already defined in the pasted block.
6. **PINS:** fill `R12_PINS` (draft:160, currently `{}`) at landing from the LOG.md md5
   entries — `{"r12_jsonl": ("md5", …), "r12_md": ("md5", …), "r12_runlog": ("md5", …)}` —
   and add the three keys to `main`'s `paths` dict so `check_r12_pins` enforces them.
7. **main():** add `--r12-jsonl/--r12-md/--r12-runlog`; after
   `check_r11_ordering(rep, jsonl_path=paths["r11_jsonl"])` add
   `_r12_recs = load_jsonl(paths["r12_jsonl"]); grade_r12(_r12_recs, read_text(paths["r12_md"]),
   read_text(paths["r12_runlog"]), rep); check_r12_ordering(rep, jsonl_path=paths["r12_jsonl"]);
   check_r12_pins(paths, rep)` (sidecar existence checks for `R12_SHA`, `R12_ORDERING`,
   `R12_PRED`, `R12_MACHINERY` mirroring the r11 block).
8. **Selftest:** add `--selftest-r12` to the argparse and
   `if args.selftest_r12: sys.exit(max(1 if selftest_stats_r12() else 0, _run_r12_fixture()))`;
   also call `selftest_stats_r12()` from `run_selftest` (it only adds assertions).
9. **Keep out of the promotion:** the whole `# ======================= fixture selftest` section (draft:2861+) (`FIX1/FIX2/FIX_*`, `_fix_*`, `SYNTH_*`, `_build_r12_fixture`,
   `_fixture_analysis_md`, `_run`, `_battery`, `_md_*`, `_apply_file_mutations`,
   `_restore_fixture`, `_run_r12_fixture`, `main`) — grader.py's own `main`/`run_selftest`
   absorb steps 7–8.

---

## 5. Checks I could NOT implement offline (with reasons)

1. **Liveness/identity of the served unit.** No network and no `/proc` in this container,
   so the gate cannot confirm that `descriptors.models_json` matches a live `/v1/models`
   response, nor that `server.argv` matches `/proc/<pid>/cmdline`. It pins: both
   `models_json` reads agree (drift check), the same `server.pid`, and the four
   `*_sha256` fields. The *truth* of the model id is out of reach offline.
2. **Whether the landed bytes are the ones LOG.md records.** LOG.md is L1-owned and
   forbidden to this gate; the landing md5s are therefore *inputs* (`R12_PINS`), not
   derived facts.
3. **The `features` payload of `meta2` beyond the plan-documented invariants.** The plan
   fixes the invariants (kinds ⊇ {DEL,MOV,REV}; last 3 ops touch ≥2 positions) but not the
   field's key set. The gate requires at least one recognized key
   (`kinds|op_kinds|kinds_present|tail_positions|positions|n_ops|len_init|n_tokens|n_truth`)
   whose value matches the recomputation; an exotic key set must be reconciled by L1.
4. **`predict_r12.py`'s predictor correctness.** Re-running it would *re-derive*
   probabilities, which the brief forbids as a scoring source. The gate instead pins the
   filed bytes (bundle sha + the sha256 stated inside `predictions-r12.md`) and recomputes
   the scores *from those bytes*.
5. **The exact family-2 draw distribution.** The plan delegates it to
   `probe_r12.py:gen_seq_problem`, so the gate does not re-implement it: it loads the
   pinned function (side-effect-free) and verifies reproduction. The fixture uses a
   stand-in generator, which is why the fixture's own distribution proves nothing about
   the real one.
6. **A true single-serving check of the served endpoint** (that no second slot was opened):
   not observable from the committed bytes.
7. **`--parallel 2` / `--kv-unified` flag semantics**: the argv is only checked for
   presence; its effect on the served unit is not measurable offline.

---

## 6. Forward contracts the gate imposes on the yet-unwritten artifacts

These are the places where the gate has to name a schema; L1 should treat each as a
requirement on the producer (or amend the gate at promotion):

1. `descriptors`/`descriptors_end` field names: `models_json`, `server.pid`,
   `machinery_sha256`, `runner_sha256`, `predictor_sha256`, `prereg_bundle_sha256`,
   `arm_order_counts`, `n_jobs`, `counterbalance`, `probe_lineage`, `seed_scheme`,
   `seed_scheme_f2`, `pids`, `pids_f2`, `n`, `n2`, `temp`=0.2, `maxtok`=8192,
   `system_prompt` == `probe_r12.py:SYSTEM`. All are produced by the landed
   `run_r12.py:descriptors()` (verified field-by-field).
2. Probability files: exactly **one** pre-hashed pass-event file (`arm`+`pid`+`p_pass`)
   and exactly **one** pre-hashed sign-event file (`contrast`+`pid`+`p_diffpos`), plus
   RL1–RL7 inside `predictions-r12.md` §5 (the probability = the first bare-float cell of
   the row).
3. `analysis_r12.md` must carry the amended §5 lines; where the amended plan's label and
   the in-flight `recompute_r12_draft.py` label differ, the gate accepts both (documented
   per check below) — except the E2 sign `direction=<+1|-1|NEUTRAL>` field, which the gate
   **requires** (D4).
4. Reliability bins: edges pinned `[0, 0.2, 0.4, 0.6, 0.8, 1.0]`, 5 lines, top bin closed,
   empty bins `pred=n/a obs=n/a n=0`.
5. `wall_total_s: <float>` on its own line; `[i/N] ('CELL', pid)` progress lines with
   `i+1`-style numbering (the denominator must equal the job count).
6. `run-script-hash <ts> <sha256> <file>` lines; a trailing parenthetical is tolerated
   (`probe_r12.py (post-critic-D1 rewrite)`); `probe_r12.py` and `run_r12.py` are required,
   `predict_r12.py` is optional (it is pinned inside the bundle).

---

## 7. Findings for L1 (divergences found while reconciling the draft with the landed bytes)

1. **Census sentence "1 vs 2 descriptors" (producer defect).** Amended §5 pins
   `2 descriptors, 64 meta, 48 meta2, G graded, A ack, F fillers, E error records`, and
   only that reading accounts for the pinned total:
   `2+64+48+1328+2256+416 = 4114` (`1+… = 4113`). `recompute_r12_draft.py:1251`
   (`descriptors = by_cell.get("descriptors", 0)`) prints the start record only, so its
   document will emit `1 descriptors`. **The gate requires 2** (`r12.analysis.counts.descriptors`).
2. **E2 sign `direction=` is missing from the in-flight recompute writer** (its line is
   `E2 exact sign: wins=%d losses=%d ties=%d two-sided p=%s`, `recompute_r12_draft.py:1807`). The
   amended §5 (D4) requires the field; the gate fails without it
   (`r12.analysis.e2.sign_direction`).
3. **Run-level per-event Brier is `n/a` in the in-flight recompute** because it scores the
   whole RL set as one group (`lambda k: "RL"`), so `per_group.get(rid)` is `None` and the
   line prints `RL1=n/a …`. The plan's §5 only pins the pooled value, so the gate tolerates
   `n/a`; my fixture prints real per-event squared errors and checks them
   (`r12.analysis.e6.brier_runlevel.RL*`, only when numeric values are present).
4. **`underpowered` trigger.** The in-flight engine adds the paired-contrast n
   (`e2.n < 44 || e5.n < 44`) to the plan's family-n rule; the gate accepts either trigger
   (both floors 44) and reports the reason in the detail.
5. **Family-2 `+977` depth.** `probe_r12.py:gen_seq_problem` **recurses** and returns a
   2-tuple, so no retry count is observable. The gate re-derives the depth by reproduction
   (`_retry_depth`); all 48 design seeds have depth 0 (verified on the committed bytes), so
   an "exercised > 0" requirement would have been a false alarm and is not imposed (family 1
   still requires ≥1 retried seed: 31/64 design seeds are rejected at least once).
6. **Plan §2.3 prose vs §5 template for the E2 line** ("710 - 4710"): the writer's
   U+2212 MINUS and the template's ASCII hyphen are both accepted (`[-\u2212\u2013]`).
7. **`bss()` degenerate value.** Both the in-flight engine and the gate return "undefined"
   when the group climatology has zero mean squared error; the gate accepts the stored
   `n/a` in exactly that case (`_close_na`) and requires a number otherwise.
8. **Number formatting is compared at the printed precision** (`_close_dp`): `L`/`E_L` at
   1 dp, `var_L` at 3 dp, `p` at 4 dp, `t`/`z` at 3 dp, Brier/BSS at 4 dp, counts exactly.
   This is why the gate does **not** demand an integer `L` (D2: `L` is half-integral under
   ties) — a mutation that writes `999.0` for `L=85.5` is killed, and one that writes the
   true value with a different decimal count is accepted only if it matches at its own
   precision.

---

## 8. Mutation battery (S7) — shape and coverage

* 98 battery entries + 3 degenerate-tree entries + 5 controls = **106 scenarios**, all
  reported `PASS` (each entry asserts that its named check id appears among the
  mismatches of the mutated tree).
* The six mutations named in the brief are present and killed: flip an `nwrong` (M01/M04),
  corrupt a meta seed (M13), delete `descriptors_end` (M30/M24), perturb a stored analysis
  number (M40/M49–M64/M79–M82), swap a prediction probability (M84/M85/M88), reorder
  `ordering.log` (M91/M92).
* Coverage map (family → number of killing mutations): meta 6, meta2 5, replay 9, census 6,
  descriptors 9, runlog 4, pred 6, analysis 47, ordering 5, pin 1 — **every family has ≥1
  killer**.
* Extra scenario families worth noting: the degenerate tree (all four ladder arms tied for
  every pid) asserts the D9 pinned outputs (`t=+0.000`, `p=1.0000`, `z=+0.000`, CI
  `[+0.000, +0.000]`) and that no `nan`/`inf` token appears in the document; the
  "default paths" control (S0c) runs the exact call shape grader.py will use (module
  constants + structural probability lookup, no fixture-supplied probability map).