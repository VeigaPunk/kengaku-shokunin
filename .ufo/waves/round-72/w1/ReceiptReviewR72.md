# ReceiptReviewR72 — adversarial review of the R72-C1 receipt against committed bytes

Seat: ReceiptReviewR72 (leaf, no subagents). Reviewed at lane master `b6336136e0e891522b113a94d8e0bd65e0eae8de`
(the round-72 freeze tip). Target of review: `corpus/evidence/round72/hf/receipt.txt` (3494 B, mtime 23:10)
plus its live witness `corpus/evidence/round72/hf/sandbox/K1..K9/`. Instrument: `plans/round72_c1_hf_probe.py`
at the same tip; worktree copy byte-equal to the committed blob (verified below). The battery was **live**
during this review (captures appearing at 23:09–23:11); this seat bound **no** port and ran **no** battery —
all recomputation was offline in scratch. No tools were installed or upgraded (none needed).

All recomputation ran in `/fast/scratch/hyaku/kengaku-r72/ReceiptReviewR72/` (removed at end, see §6).
The nine staged digests were produced by the probe's **own** `stage_case`/`case_dir_sha` via module import,
and cross-checked against an independent hand re-implementation of `tree_digest`; the two agree on every
tree.

## 1. Re-derived bindings (receipt vs committed bytes)

| # | Binding | Receipt says | Re-derived by this seat | Verdict |
|---|---|---|---|---|
| 1 | `REV` | `b6336136e0e8…eae8de` | `git rev-parse master` → `b6336136e0e891522b113a94d8e0bd65e0eae8de` (ancestor of itself) | ✅ |
| 2 | `GRADER sha256` | `61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857` | `sha256sum corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py` → same | ✅ |
| 3 | `INSTRUCTION sha256` | `29151c5b2306f522f38fa905de3d34566865829355e5ca0895f4fca04d51dcc1` | `sha256sum corpus/evidence/round71/hf/instruction.md` → same | ✅ |
| 4 | `MODEL tree_sha256 files` | `c5c257677d7143af…b858944 files=5` | probe `tree_digest` **and** independent re-implementation over the 5 files (`config.json`, `model.safetensors`, `tokenizer.json`, `tokenizer_config.json`, `vocab.txt`) → same; `rglob` file count = 5 | ✅ |
| 5 | `PROBE sha256` | `99867c7f080179b4…faa637e` | `sha256sum plans/round72_c1_hf_probe.py` (worktree) → same | ✅ |
| 6 | `PROBE_BLOB sha256 rev` | `99867c7f…faa637e rev=b6336136…` | `git cat-file -p master:plans/round72_c1_hf_probe.py \| sha256sum` → same; worktree bytes == committed bytes (byte-equal compare) | ✅ |
| 7 | `LIBRARIES …` | `python=3.13.16 torch=2.14.1+cu130 transformers=5.21.0 requests=2.34.2` | checker's live `library_versions()` clause passed in my rc=0 run (no `library-drift` defect) | ✅ |
| 8 | `PROVENANCE` arithmetic | `env_cleared=True allowlist=PATH,HOME,LANG,PYTHONPATH,PYTHONNOUSERSITE,PYTHONWARNINGS,TMPDIR,HF_HUB_OFFLINE,TRANSFORMERS_OFFLINE allowlist_seen=9/9 cases=9 distinct=1 canary_seen=0 transformers_file=/venv/lib/python3.13/site-packages/transformers/__init__.py` | allowlist string == `ENV_ALLOW` order (9 names); every capture's `env_keys` ⊇ those 9 → `9/9` correct; unique `transformers_file` across 9 captures = 1 → `distinct=1`; `canary` = `ABSENT` in all 9 → `canary_seen=0`; file is the real `/venv/…/transformers/__init__.py` | ✅ (see F2 for the superset caveat) |
| 9 | `CASE K1…K9 case_sha256` | `4512bfa2…`, `e0c2dc8e…`, `36ce18bf…`, `eaff30cc…`, `d0e8574c…`, `6317bec0…`, `494f5d59…`, `b229944f…`, `3ecda970…` | re-staged all nine cases with the probe's own `stage_case` in scratch → identical digests, all nine; independent digest implementation agrees; 9/9 distinct | ✅ |
| 10 | `LEGS`/`VECTOR` ×9 | frozen table (`PPPP,PPFP,PPFP,PPPF,PFPP,PFFF,FPPP,FPPP,PPPF`), `agree=True` ×9 | matches frozen `VECTORS`; per-case `LEGS`-derived == `VECTOR`-derived; equals the per-case sandbox captures (`derived`, `legs`, `exc`) | ✅ |
| 11 | `LEG-COVERAGE legs=4 seen_p=4 seen_f=4` | as left | recomputed from `LEGS` lines: L1 F@K7,K8; L2 F@K5,K6; L3 F@K2,K3; L4 F@K4,K9; every leg also has ≥1 P → `seen_p=4 seen_f=4` | ✅ |
| 12 | `SUMMARY cases=9 legs=36 mismatches=0 setup=0 exc=2` | as left | mismatches 0 (all `derived` == frozen); setup 0 (all `sandbox_rc=0`); exc = 2 (`K6 test_api_error_handling=E test_sentiment_endpoint=E`) | ✅ |
| 13 | `PREDICATE R72-C1 pass` | pass | all clause conditions hold; counting command #2 re-run by this seat: `python3 plans/round72_c1_hf_probe.py --lane . --check-receipt corpus/evidence/round72/hf/receipt.txt --work <scratch>/check` → `DEFECTS n=0`, `PREDICATE R72-C1 pass`, rc=0 | ✅ |
| 14 | Replicate | `receipt-replicate.txt` | `diff receipt.txt receipt-replicate.txt` → empty (byte-identical; `server_pid=3` is stable because bwrap's PID namespace numbers the server 3 in every case) | ✅ |

Sanity cross-check: the do-nothing control receipt (`.ufo/waves/round-72/c1-control.txt`) carries
`case_sha256=01ba4719c8…546b` for all nine cases; `sha256("\n")` = `01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b`
— exactly the probe's empty-tree digest (`tree_digest` of zero files), confirming the control staged genuinely
empty app trees rather than copying artifacts.

## 2. Refusal attempts (`--check-receipt <file> --work <scratch>/work-<t>`)

| Attempt | Mutation | rc | Defects printed | Verdict |
|---|---|---|---|---|
| **a** — hand-written all-P receipt | Built from scratch: real top-block digests, all nine `LEGS` = P, `VECTOR derived=PPPP agree=True`, forger's `LEG-COVERAGE seen_f=4` / `SUMMARY mismatches=0` / `PREDICATE pass` | **1** | `DEFECTS n=11`: `vector-mismatch` ×8 (K2…K9, `derived=PPPP frozen=…`), `leg-coverage` (`want 'LEG-COVERAGE legs=4 seen_p=4 seen_f=0'`), `summary` (`want '… mismatches=8 setup=0 exc=0'`), `predicate` (`want 'PREDICATE R72-C1 fail'`) | **Refused**, four independent defect families fire |
| **b** — self-consistent `PROVENANCE`, wrong `transformers_file` | (b-base) fully forged frozen-table receipt, never touched a sandbox → `DEFECTS n=0`, rc=0; then `transformers_file=/venv/lib/python3.13/site-packages/not_transformers/__init__.py` → `DEFECTS n=0`, rc=0; and (b3) the **receipt of record** with the one token flipped to `/venv/etc/does-not-exist.so` → `DEFECTS n=0`, rc=0 | **0** | none | **Accepted** — exactly the frozen limitation (v). The checker validates `transformers_file` only by its `/venv/` prefix (probe `:782`), never existence or identity |
| **c** — `LEGS K9` leg-4 = P while `VECTOR K9` stays `PPPF` | One token flip in an otherwise-consistent receipt | **1** | `DEFECTS n=1`: `vector-derived K9 vector=PPPF legs=PPPP` (probe `:822`); `LEG-COVERAGE`/`SUMMARY` recomputes did **not** fire (K4 still prices L4's F; mismatches are computed from `VECTOR` only) | **Refused** by the per-case LEGS↔VECTOR cross-check |
| **d** (extra, beyond the brief) — duplicated `PROVENANCE` | Real receipt + second `PROVENANCE` line with `env_cleared=False` inserted after the good one | **0** | none (`DEFECTS n=0`, rc=0) | **Accepted** — see F3 |

## 3. K9 really prices `tests/test_outputs.py:107`

Grader (`corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py`, 107 lines, leg-4 =
`test_api_error_handling`, grader lines :95–:107):
- `:103` `assert response.status_code == 400, ("API should return 400 for invalid request format")`
- `:107` `assert "error" in error_data, "Error response should contain 'error' field"`

Staged server mode `400-no-error-field` (probe `SERVER_TMPL`): a POST body without `text` answers
`self._json(400, {"detail": "missing text"})`. Chain: `:103` passes (400), `error_data = {"detail": "missing text"}`
lacks `error` → `:107` reds with AssertionError → leg 4 = F, recorded as an assert (not `EXC`). Legs 1–3 stay
green (model `good`, server up, six labels/floats correct) → `PPPF`. The K9 capture confirms:
`detail.test_api_error_handling = "AssertionError: Error response should contain 'error' field"`, `derived=PPPF`.
Contrast K4 (`no-400` mode): missing `text` answers **200** → `:103` reds (`"AssertionError: API should return 400
for invalid request format"` in the K4 capture) — a **different assert site of the same leg**. K9 therefore adds
exactly the coverage the round-71 eight-case table lacked, and claim limitation (vi) ("one assert site, not the
leg as a whole") is accurate.

## 4. Findings

- **F1 (Medium, declared by the claim — limitation (v) confirmed by execution).** The checker accepts a
  from-scratch forgery (rc=0, `DEFECTS n=0`) and any `transformers_file` that merely starts with `/venv/`,
  including a nonexistent path (`/venv/etc/does-not-exist.so` accepted). `--check-receipt` is a consistency
  check over committed bytes and proves nothing about the live run. Mitigation is exactly as frozen: the
  per-case sandbox captures are the live witness — this seat verified all nine manifests carry the same real
  `transformers_file=/venv/lib/python3.13/site-packages/transformers/__init__.py`, `canary=ABSENT`, and the
  allowlist superset.
- **F2 (Low).** `allowlist_seen` is a **superset** check (probe `:612`: `set(env_keys) >= set(allow_names)`), so
  extra variables inside the sandbox cannot lower it. Two extras actually occur in the captures: `PWD` (all
  nine cases) and `TORCHINDUCTOR_CACHE_DIR` (K1–K6, K9; absent in K7/K8 where the model never loads — 11 vs
  10 keys). Both are created **inside** the sandbox, not inherited: a bwrap probe (`--clearenv` + two
  `--setenv`, `env | sort`) shows bubblewrap itself injects `PWD=/tmp` from `--chdir` even under `--clearenv`,
  and a host repro shows `TORCHINDUCTOR_CACHE_DIR=/tmp/torchinductor_vgpnk` first appears in `os.environ`
  during `from_pretrained` weight loading (absent before it). The isolation property (nothing from the caller
  crosses) still holds — the canary never appears in any capture — but "nine-variable allowlist" is a floor,
  not an equality, and no clause of the receipt would notice a benign-looking extra if it ever carried
  influence.
- **F3 (Low — checker under-enforces a frozen kill-rule clause).** The frozen kill rule names "a `PROVENANCE`
  line that is absent/duplicated/outside `/venv/`" as claim-failing, but `check_receipt` reads only
  `prov_lines[0]` (probe `:768`) and never counts `PROVENANCE` lines; a receipt with a good line followed by a
  contradictory duplicate passes with `DEFECTS n=0` (attempt d). The battery can never emit two, and the live
  witness is unaffected, so the claim's evidence base is not touched — but the "duplicated" clause is
  currently unenforced by `--check-receipt`. A successor probe could refuse on `len(prov_lines) != 1`.
  Report-only; no seat edits a frozen rule.
- **F4 (Lane hygiene).** Stray file `corpus/evidence/round72/hf/check.txt` (34 bytes: `DEFECTS n=0` /
  `PREDICATE R72-C1 pass`, mtime 23:10) — a checker stdout capture dropped into the evidence directory
  instead of scratch, presumably a redirect slip by the battery/receipt seat. Untracked; the integrator
  should delete it before commit. Not removed by this seat (outside its write scope).
- **F5 (Informational).** The nine `case-digest` re-staging clauses of `check_receipt` run only when
  `--work` is passed (`if work is not None`, probe `:797` ff.); without it the checker skips digest
  verification entirely. The frozen counting command #2 includes `--work <scratch>/check`, so the predicate
  as frozen is intact — but a bare `--check-receipt` invocation is a weaker check than its output suggests.

## 5. Residual risk and verification gaps

- This seat did **not** run the battery, `--control`, `--stub-control`, or `--selftest` (port 5000 was held by
  the live battery; those arms belong to other seats). The receipt's runtime claims are therefore witnessed
  by the committed captures + byte-identical replicate, not by this seat's own re-run.
- `LIBRARIES` values were accepted via the checker's live-recompute clause at review time, not re-derived
  import-by-import by hand; a host venv change after 23:10 would print `library-drift` on any re-check (it
  did not).
- Attempt coverage was fixed by the item (a, b, c); d was added because the source read showed the gap. The
  `provenance-canary` / `provenance-allowlist-seen` defect codes were verified by source inspection only,
  not by constructed receipts.

## 6. Scratch discipline

Scratch `/fast/scratch/hyaku/kengaku-r72/ReceiptReviewR72/` (recompute trees, five adversarial receipts,
bwrap-probe dir, per-attempt `work-*` trees) was removed after this report was written; nothing was written
to `/tmp` (the only tmpfs use was inside a bwrap sandbox that died with the probe). No tool was installed or
upgraded (channel record: n/a). Writes outside scratch: this report only.
