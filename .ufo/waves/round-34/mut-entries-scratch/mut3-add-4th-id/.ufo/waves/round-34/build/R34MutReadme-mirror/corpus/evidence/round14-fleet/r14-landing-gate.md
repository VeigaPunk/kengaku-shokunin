# Round 14 landing gate — round 12/13 evidence

**Role:** independent landing review, L2.  
**Measured against:** `HEAD e171cdfbdb350ee90bfc1c66dac54106a3a5e2ca` — `corpus: round-9 aggregator corpus-verdict lesson (rule-10 re-emitted at f09ff1f, canonical-form + rule-8 literal findings, routed rows)`.  
**Axes:** novelty, reproducibility, provenance, durability, and claim scope.

## Gate decision

**Novelty 6 → 7: YES, narrowly, on C1 only.** The four-point ordered emission-density severity response was not observable from r9's n=8 directional three-arm run or r11's powered two-arm middle contrast. It is a new-to-this-lane measurement resolution, not a field-first phenomenon: C1 is priced **INCREMENTAL (low)** against published step-count and instruction-density effects. Its ordered-trend result, inspectable run/recompute machinery, preregistration, and fetched-URL prior-art ledger satisfy the scorecard's three novelty legs. C3's fixed-emission batching dissociation is useful supporting evidence, but its own preregistered power analysis says it was not powered at its near-null point prediction; do not use C3 alone to earn the point. C4 transport is directional only and does not earn novelty credit.

**Landing state: NOT GREEN.** The primary numbers independently re-derive, but several evidence-integrity and document-readiness issues below are MAJOR. This gate does not edit `SKILL.md`, `grader.py`, `SCORECARD.md`, `LOG.md`, `corpus/README.md`, or any round-12/13 artifact. The path table gives an action for every working-tree path in the captured snapshot.

## Numbered claims

### 1. Rubric and baseline — the move is a four-arm measurement, not a new phenomenon claim

**Command:** `git rev-parse HEAD && git show -s --format=%s HEAD`; compare `SCORECARD.md:69-73,136-140,153-160,163-184`.

**Observed:** Current `HEAD` is `e171cdfbdb350ee90bfc1c66dac54106a3a5e2ca`. SCORECARD's novelty proxy requires a construct unavailable to this lane, an inspectable in-repo instrument, and a prior-art verdict with fetched URL (`SCORECARD.md:12-17,155`). Its r9 row records only a directional n=8 granularity result; its r11 row records the powered +0.352 middle contrast; the r12 target explicitly asks for a powered full ladder and a second family (`SCORECARD.md:69,140,165-180`). The r12 report's `f09ff1f` is its **historical pre-r12** HEAD, not the current r14 scorecard measurement base.

**Verdict:** Treat the r12 full ordered response as the one qualifying new-to-lane construct. Do not frame it as a new-to-field phenomenon or count C2/C5/C6 as separate novelty moves.

### 2. C1 — the ordered ladder is independently reproduced from the stored run bytes

**Commands:**

```sh
sha256sum -c corpus/evidence/round12-ladder/prereg-bundle.sha256
python3 corpus/evidence/round12-ladder/recompute_r12.py --selftest
python3 corpus/evidence/round12-ladder/recompute_r12.py --results corpus/evidence/round12-ladder/results-r12.jsonl --out /dev/null
```

Also run the fully specified independent calculation in **Appendix A** from the repository root; it does not import `recompute_r12.py` and does not write files.

**Observed:** The preregistration command reported **9/9 files OK**. The promoted recomputer reported `SELFTEST 165/165 PASS`; the full run reported `4114 records` and `VERDICT R1 ladder: LADDER ESTABLISHED`. Appendix A independently finds 64 complete blocks, Page `L=1773.0`, `E_L=1600.0`, tie-corrected variance `335.000`, `z=+9.452`, and two-sided normal-tail `p=3.324e-21`. It independently reproduces the ordered final means: A-INC `0.2969`, A-CKPT4710 `0.8125`, A-CKPT710 `1.0469`, A-CKPT10 `1.5938`. The raw result file is SHA-256 `ad9c88e79068fa2833c90f071ec6da4035ff37371ff95d84f581dd4e8db842f1`, MD5 `9dd8aa2b6a7aa7890aa802c37d5af0f9`.

**Prior art:** The repository's fetched-source ledger prices C1 **INCREMENTAL (low)**. It records HTTP 200 for the step-length study (`https://arxiv.org/abs/2401.04925`), IFScale (`https://arxiv.org/abs/2507.11538`), and Entity Tracking (`https://arxiv.org/html/2305.02363v2`); it finds no fetched counterpart for the specific forced-full-state-emission-density × wrong-entry-severity measurement (`r12-prior-art-ladder.md:56-67,106-131`).

**Verdict:** C1 clears the novelty proxy narrowly: the lane now has a powered ordered dose-response measurement it could not read from the earlier binary/middle-only evidence, with the actual instrument and bytes in the repository. The evidence does **not** establish a general law or a novel-to-field degradation phenomenon.

### 3. C3 — real dissociation, limited mechanism and power claims

**Commands:** Appendix A's E4 calculation; `python3 corpus/evidence/round12-ladder/recompute_r12.py --results corpus/evidence/round12-ladder/results-r12.jsonl --out /dev/null`; inspect `power_analysis_r12.md:117-123` and `r12-critic-design.md:40`.

**Observed:** `A-MONO − A-CKPT10` final `nwrong` is `+0.656` (sd `1.158`, n=64, t=`+4.535`, sign W/L/T `34/8/22`); the stored analysis reports `DISSOCIATION ESTABLISHED`. Both arms have one forced full-state emission, while MONO lists all ten operations up front and CKPT10 supplies operations incrementally. The preregistered predictor for this contrast was only `+0.0437`; the power analysis explicitly says E4 has no prior paired estimate at n≥44 and is powered for a large effect, not its near-null predicted magnitude.

**Prior art:** The C3 ledger calls the dissociation **NOVEL-instrument**, at medium confidence, after a negative-search log; it explicitly says absence of evidence, not verified absence. Fetched comparators recorded as HTTP 200 include BatchPrompt (`https://arxiv.org/abs/2309.00384`), IFScale (`https://arxiv.org/abs/2507.11538`), Laban et al. (`https://arxiv.org/abs/2505.06120`), and the ACL batch-prompting paper (`https://aclanthology.org/2025.findings-acl.245/`) (`r12-prior-art-ladder.md:81-90,169-196,225-250`).

**Verdict:** The arm pair dissociates operation batching from emission sparsity at fixed emission count. It does **not** prove batching is the only mechanism behind r8's MONO collapse; turn structure and context presentation also differ. C3 is supporting evidence, not the standalone power basis for the novelty move.

### 4. C4/C2/C5/C6 — do not inflate the novelty claim

**Commands:** Appendix A for E2–E5; `python3 corpus/evidence/round12-ladder/recompute_r12.py --results corpus/evidence/round12-ladder/results-r12.jsonl --out /dev/null`; inspect `power_analysis_r12.md:103-115` and `analysis_r12.md:28-43`.

**Observed:**

- **C4 transport:** E5 `T-SPARSE − T-DENSE` is `+0.177`, sd `1.069`, n=48, t=`+1.147`, p=`0.2571`, signs `22/16/10`; each arm passes only `2/48`. Power at the halved effect was filed as `0.327`, with n=169 needed for 80% power. The prior-art ledger prices C4 **INCREMENTAL (low)** and limits it to one additional family (`r12-prior-art-transport.md:428-433`; fetched comparators include `https://arxiv.org/abs/2505.06120`, `https://arxiv.org/abs/2404.06654`, and `https://arxiv.org/abs/2507.11538`).
- **C2 repeatability:** E2 is `+0.297` on the same problems, seeds, and unit as r11's `+0.352`; the correct term is later-run/within-run **repeatability**, not independent replication (`r12-prior-art-ladder.md:133-167`).
- **C5 forecasting:** the stored analysis reports 416 pass events, pooled Brier `0.1288`, pooled BSS `+0.0447`, and family-2 BSS `−3.1474`; forecasts use the same problems/persistence information and family-2 forecasts are constant per arm. The prior-art ledger prices C5 **INCREMENTAL**, not a novel instrument (`r12-prior-art-transport.md:337-423`).
- **C6 adjacent-gap ordering:** derived from the same ladder and priced **INCREMENTAL**; it is not a second independent novelty construct (`r12-prior-art-ladder.md:198-221`).

**Verdict:** C4 is a floor-level directional observation, not established transport; C2 is not independent replication; C5 is not cold forecasting; C6 does not add a separate novelty point. Keep all four claims' caveats attached.

### 5. Round 13 ack audit — hermetic for r9/r11; r12 storage labels need a separate schedule calculation

**Commands:**

```sh
python3 corpus/evidence/round13-ack-state/audit_ack_schedule.py
python3 corpus/evidence/round13-ack-state/analyze_ack_state.py
```

**Observed:** Both commands ran read-only from committed inputs. `audit_ack_schedule.py` reports r9 A-CKPT4710 true ack-only prefix/bare `32/32` and label-wide `32/56`; r9 A-CKPT710 `48/48` and label-wide `48/64`; r11 A-CKPT4710 `220/256` prefix / `216/256` bare versus label-wide `220/448`; r11 A-CKPT710 `330/384` / `324/384` versus label-wide `330/512`. `analyze_ack_state.py` confirms r11 A-CKPT710 has 64 meta records, 512 `-ack`-labelled rows, 384 true ack-only prompts, 330 prefix-`ok`, 324 bare-`ok`, and 18 exact states; its input SHA-256 is `918bf7aa3030baa954c16a20830f078738147ce7cc002768e5ab922ad38f51ad`.

The r13 schedule script declares only r9/r11 inputs (`audit_ack_schedule.py:16-23`); it does not by itself audit r12. Appendix A applies the same prompt-intent rule to the r12 schedule and stored r12 bytes: A-CKPT4710 `212/256` true ack-only prefix (label `212/448`), A-CKPT710 `324/384` (label `324/512`), A-CKPT10 `440/512` (label `440/576`), T-DENSE has **zero** ack-only prompts despite 336 rows labeled `-ack`, and T-SPARSE is `264/288` (label `264/384`). The r12 start-message and checkpoint controls are documented in `probe_plan_r12.md:43-56`; the executable response-label logic is in `run_r12.py:95-119`.

**Verdict:** Round 13 is a hermetic denominator audit, not a model-behavior probe and not a novelty move. The r12 `analysis_r12.md` ack values are correctly described as storage-label counts; any prompt-intent statement for r12 should cite the separate Appendix A calculation, not attribute it to the r13 scripts.

### 6. Stored-byte reproducibility and gate pin — one path-line drift, not a statistical mismatch

**Commands:**

```sh
python3 corpus/evidence/round12-ladder/recompute_r12.py --results corpus/evidence/round12-ladder/results-r12.jsonl --out /dev/stdout | diff -u corpus/evidence/round12-ladder/analysis_r12.md -
md5sum corpus/evidence/round12-ladder/analysis_r12.md
```

**Observed:** The `diff` exits 1. The sole analysis-content difference is the `Generator source:` provenance line (stored lower-case `/home/vgpnk/projects/...`; regenerated `/home/vgpnk/Projects/...`). The diff also includes the recomputer's two trailing CLI status lines after the markdown output. All statistical values independently checked above match. Current `analysis_r12.md` is MD5 `029c3bcdcf11209d575734742bf239f6`, SHA-256 `1ceebd7568aab4ecba694b983d7f3312c957402c7841b7597d6ed4506b6453e3`.

The final r12 report, log, and doc-delta files instead claim current `analysis_r12.md` MD5 `ddfe60d234cae732143649abe80e1ba8` (and report-final SHA prefix `ef1e69db`); that pin is false for the bytes on disk. The citation-review artifact's `fd3ca422...` is labeled as an earlier mid-review snapshot, not the current file. Also, `grader.py:1529-1536` has only `r12_jsonl` and `r12_runlog` in `R12_PINS`; its comment says `analysis_r12.md` will be pinned, but no `r12_md` key exists. The gate can rederive semantic values without that byte pin, but do not describe the analysis as md5-pinned.

**Verdict:** Falsified: “regeneration from committed bytes must be byte-identical at round close” (r12 report-final §Run results). The numeric result survives; the provenance string does not. Normalize the generated path or explicitly downgrade the byte-identity claim, then use hashes of the actual committed bytes. The round-12 historical L2 documents are not edited by this reviewer.

### 7. Skill citation paths and absent r12 critic artifact

**Command:**

```sh
python3 - <<'PY'
from pathlib import Path
for p in (
    'r12-critic-design.md', 'probe_plan_r12.md', 'power_analysis_r12.md',
    'corpus/evidence/round12-fleet/r12-critic-design.md',
    'corpus/evidence/round12-ladder/probe_plan_r12.md',
    'corpus/evidence/round12-ladder/power_analysis_r12.md',
    'corpus/evidence/round12-fleet/r12-critic-landed.md',
    'corpus/evidence/round14-fleet/r14-critic-landed.md',
):
    print(f'{p}: {Path(p).exists()}')
PY
```

**Observed:** The three bare SKILL citation strings at `SKILL.md:147,155,427-428,444` resolve false from the repo root; their fully qualified `corpus/evidence/...` counterparts resolve true. `corpus/evidence/round12-fleet/r12-critic-landed.md` is absent, although the final r12 report/log contain `{{CRITIC_LANDED_VERDICT}}` placeholders and describe a fresh critic as part of their confidence basis. A round-14 file now exists, but `r14-critic-landed.md:7-12,18` runs `/tmp/r14critic_verify.py` and does not include that verifier's source; its raw-output parse command is abbreviated `python3 - <<'PY' ...` at lines 64-68.

**Verdict:** Fully qualify the new SKILL paths before treating them as root-relative citations. Do not silently treat the absent r12 artifact as delivered. The r14 critic's printed results are useful corroboration, but its independent implementation is not itself durable/re-runnable from the repo; Appendix A supplies a durable independent reproduction of the primary C1/E2-E5 statistics.

### 8. Mock artifacts, final-paperwork state, and header convention

**Command:** Run this repository-root inventory and compare the r11 control paths and cited L2 rows:
```sh
python3 - <<'PY'
from pathlib import Path
for root in ("corpus/evidence/round12-fleet", "corpus/evidence/round11-fleet"):
    d = Path(root)
    print(root, sorted(p.name for p in d.glob("mock*")))
PY
grep -n '448 pass events' corpus/evidence/round12-fleet/r12-prior-art-transport.md
grep -nE '\{\{[A-Z0-9_]+\}\}' corpus/evidence/round12-fleet/r12-report-final.md corpus/evidence/round12-fleet/r12-log-final.md corpus/evidence/round12-fleet/r12-doc-deltas-final.md
grep -n '^## Round 14' SCORECARD.md || true
```
The relevant L2 evidence is `r12-review-citations.md:481-493` and `r12-scope-audit.md:92-117`.

**Observed:** The `mock*` inventory yields only `mock_server_r12.py` under `round12-fleet`; no `mock-*.jsonl` or `mock-run.log` is committed. The review-citations row 407 calls `/tmp/kengaku-r12-mock/results-r12.jsonl` a “committed mock run”; scope-audit F6/F7 also uses `/tmp/kengaku-r12-smoke/` and `/tmp/kengaku-r12-mock/`. By contrast, r11 committed the JSONL, run log, server, and smoke note. `r12-endpoint-freshness.md` is different: although it fetched initially to `/tmp/r12f-models.json`, it reproduces the entire 872-byte response and MD5/SHA-256 inline at lines 114-127, so the capture is not temp-only.

`r12-prior-art-transport.md:19,391` also retains the superseded “448 pass events” C5 denominator; the amended plan and results have 416 pass events. `r12-report-final.md`, `r12-log-final.md`, and `r12-doc-deltas-final.md` still contain unresolved `{{...}}` placeholders and stale 17-file/hash claims. Their text is useful as a dated historical record, not as paste-ready current LOG/README/SCORECARD content. `corpus/README.md`, `LOG.md`, and `SCORECARD.md` were not modified in the captured worktree state.

**Verdict:** Commit the mock server source, but do not claim the r12 mock census is repository-durable until its JSONL/log are added or its report wording is downgraded. Preserve historical false/stale L2 records as archive evidence; correct the actual landing prose from verified bytes, not by copying their unresolved blocks.

For the scorecard header, use the current snapshot rather than r12's historical pre-run HEAD:

```markdown
## Round 14 — pre-move (measured against HEAD e171cdf "corpus: round-9 aggregator corpus-verdict lesson")
```

No r14 SCORECARD section exists in this worktree snapshot. Do not use `f09ff1f` as the r14 pre-move anchor.

## Appendix A — copyable independent raw-byte calculation

Run from the repository root. This stdlib-only program calculates the Page trend, shared-turn paired effects, and prompt-intent ack denominators directly from `results-r12.jsonl`; it imports no lane analysis module and writes no files.

```sh
python3 - <<'PY'
import json, math, statistics
from collections import defaultdict

path = "corpus/evidence/round12-ladder/results-r12.jsonl"
records = [json.loads(line) for line in open(path, encoding="utf-8")]
by = defaultdict(lambda: defaultdict(dict))
for row in records:
    if row.get("cell") in {
        "A-INC", "A-CKPT4710", "A-CKPT710", "A-CKPT10", "A-MONO",
        "T-DENSE", "T-SPARSE",
    }:
        by[row["cell"]][row["pid"]][row["turn"]] = row

arms = {
    "A-INC": 10, "A-CKPT4710": 10, "A-CKPT710": 10,
    "A-CKPT10": 10, "A-MONO": 1, "T-DENSE": 10, "T-SPARSE": 10,
}
print(f"RECORDS={len(records)}")
for arm, turn in arms.items():
    final = [by[arm][pid][turn] for pid in sorted(by[arm])]
    passes = sum(bool(row["ok"]) for row in final)
    mean = statistics.mean(row["nwrong"] for row in final)
    print(f"{arm}: pass={passes}/{len(final)} mean={mean:.4f}")

# Page's ordered alternative over the four preregistered family-1 arms.
ladder = ["A-INC", "A-CKPT4710", "A-CKPT710", "A-CKPT10"]
k = 4
ss_c = sum((j - (k + 1) / 2) ** 2 for j in range(1, k + 1))
L = variance = 0.0
blocks = 0
for pid in sorted(set.intersection(*(set(by[arm]) for arm in ladder))):
    values = [by[arm][pid][10]["nwrong"] for arm in ladder]
    order = sorted(range(k), key=lambda j: values[j])
    ranks = [0.0] * k
    i = 0
    while i < k:
        j = i + 1
        while j < k and values[order[j]] == values[order[i]]:
            j += 1
        midrank = ((i + 1) + j) / 2
        for m in range(i, j):
            ranks[order[m]] = midrank
        i = j
    L += sum((j + 1) * ranks[j] for j in range(k))
    mean_rank = statistics.mean(ranks)
    ss_r = sum((rank - mean_rank) ** 2 for rank in ranks)
    variance += ss_c * ss_r / (k - 1)
    blocks += 1
expected = blocks * k * (k + 1) ** 2 / 4
z = (L - expected) / math.sqrt(variance)
p_page = math.erfc(abs(z) / math.sqrt(2))
print(f"PAGE n={blocks} L={L:.1f} E={expected:.1f} var={variance:.3f} z={z:+.3f} p={p_page:.3e}")

def contrast(name, a, b, turns=None):
    pids = sorted(set(by[a]) & set(by[b]))
    diffs = []
    for pid in pids:
        if turns is None:
            ta, tb = max(by[a][pid]), max(by[b][pid])
            diffs.append(by[a][pid][ta]["nwrong"] - by[b][pid][tb]["nwrong"])
        else:
            diffs.append(statistics.mean(
                by[a][pid][turn]["nwrong"] - by[b][pid][turn]["nwrong"]
                for turn in turns
            ))
    sd = statistics.stdev(diffs)
    t = statistics.mean(diffs) / (sd / math.sqrt(len(diffs)))
    signs = (sum(x > 0 for x in diffs), sum(x < 0 for x in diffs),
             sum(x == 0 for x in diffs))
    print(f"{name}: n={len(diffs)} diff={statistics.mean(diffs):+.3f} "
          f"sd={sd:.3f} signs={signs[0]}/{signs[1]}/{signs[2]} t={t:+.3f}")

contrast("E2", "A-CKPT710", "A-CKPT4710", [7, 10])
contrast("E3a", "A-CKPT4710", "A-INC", [4, 7, 10])
contrast("E3b", "A-CKPT710", "A-CKPT4710", [7, 10])
contrast("E3c", "A-CKPT10", "A-CKPT710", [10])
contrast("E4", "A-MONO", "A-CKPT10")
contrast("E5", "T-SPARSE", "T-DENSE", [7, 10])

# The stored -ack label also includes full-state prompts. Re-derive prompt intent.
ack_specs = {
    "A-CKPT4710-ack": ({4, 7, 10}, False),
    "A-CKPT710-ack": ({7, 10}, False),
    "A-CKPT10-ack": ({10}, False),
    "T-DENSE-ack": ({4, 7, 10}, True),
    "T-SPARSE-ack": ({7, 10}, False),
}
for cell, (checkpoints, dense) in ack_specs.items():
    rows = [row for row in records if row.get("cell") == cell]
    turns = [] if dense else [
        turn for turn in range(2, 11)
        if turn not in checkpoints and turn - 1 not in checkpoints
    ]
    true_ack = [row for row in rows if row.get("turn") in turns]
    prefix = sum(str(row.get("raw", "")).strip().lower().startswith("ok")
                 for row in true_ack)
    bare = sum(str(row.get("raw", "")).strip().lower() == "ok"
               for row in true_ack)
    label_prefix = sum(str(row.get("raw", "")).strip().lower().startswith("ok")
                       for row in rows)
    print(f"{cell}: label={len(rows)} true_ack={len(true_ack)} turns={turns} "
          f"prefix={prefix}/{len(true_ack)} bare={bare}/{len(true_ack)} "
          f"label_prefix={label_prefix}/{len(rows)}")
PY
```

**Observed output:** `RECORDS=4114`; family-1 means match the stored arm table; Page `L=1773.0 E=1600.0 var=335.000 z=+9.452 p=3.324e-21`; E2 `+0.297`, E3a `+0.438`, E3b `+0.297`, E3c `+0.547`, E4 `+0.656`, E5 `+0.177` with the n/sd/sign/t values stated above. R12 prompt-intent outputs are exactly: A-CKPT4710 `label=448 true_ack=256 prefix=212/256 bare=212/256`; A-CKPT710 `512 / 384 / 324/384 / 318/384`; A-CKPT10 `576 / 512 / 440/512 / 440/512`; T-DENSE `336 / 0`; T-SPARSE `384 / 288 / 264/288 / 216/288`.

## Hash register

Full hashes identify the evidence bytes reviewed; run-byte MD5s are included because the r12 gate/report convention uses MD5. Commands: `sha256sum <path>` and `md5sum <path>` from the repository root.

| Path | SHA-256 | MD5 (where recorded) |
|---|---|---|
| `SCORECARD.md` | `db72bd3a849997e5674a9accc23484ff6cd3be66c7d29b3eae9d55f254ca750e` | — |
| `SKILL.md` | `afa189f6e2379f95897fa5cea492cfa51a04225f62b4fd2323291634d0951f18` | — |
| `grader.py` | `bf69666f9b0c5d33b66329bf2f8f3b9907871eda9c8e6cb7ad9a12f40a914ca7` | — |
| `corpus/evidence/round11-fleet/r11-critic-landed.md` | `2d44d6346ea917d5d043f741013165a65dace1ea7b31fff76a2974f9f1ee922d` | — |
| `corpus/evidence/round11-fleet/r11-review-baseline.md` | `a9392753c3dbb1ed7827770de9ed04b71a480ffd7ea10b82f9387ac58f5ddf15` | — |
| `corpus/evidence/round11-fleet/r11-prior-art-granularity.md` | `6ba92153aa10054d82d582a84c189e27fd87c989f5b4189a0e8c9c0cb9f63f6a` | — |
| `corpus/evidence/round12-ladder/probe_plan_r12.md` | `0efa130a1dfff4ebc145cf6abe4b818c2f5644e4b03c638dfd9d6b54c7389b52` | — |
| `corpus/evidence/round12-ladder/power_analysis_r12.md` | `15cd40e8c3a9b33d9f04d33e4b1887439385bf5dffc6a12b20b79f66645b5c88` | — |
| `corpus/evidence/round12-ladder/probe_r12.py` | `1871697f5c3410adf3c17297138e76416cdeb63194038324eec067abe6b90662` | — |
| `corpus/evidence/round12-ladder/run_r12.py` | `3beb91ea705a85636bd232074a5c71b9c64f8aa5b9995f3e3376aa849fdecddf` | — |
| `corpus/evidence/round12-ladder/recompute_r12.py` | `5c57e4d70dbe239c698e6d97842e5345dd37933e0587dd9d87f9bf1cda6f7342` | — |
| `corpus/evidence/round12-ladder/results-r12.jsonl` | `ad9c88e79068fa2833c90f071ec6da4035ff37371ff95d84f581dd4e8db842f1` | `9dd8aa2b6a7aa7890aa802c37d5af0f9` |
| `corpus/evidence/round12-ladder/run.log` | `361141901ae823afd003c6b4cc95d25b5c8681121c783a7fa9745ffc2b53d60e` | `700d1ddd2ece50d7bdedd55859c59f3a` |
| `corpus/evidence/round12-ladder/analysis_r12.md` | `1ceebd7568aab4ecba694b983d7f3312c957402c7841b7597d6ed4506b6453e3` | `029c3bcdcf11209d575734742bf239f6` |
| `corpus/evidence/round12-fleet/r12-prior-art-ladder.md` | `907a0d23c9311573e436fd9b17e5bc132047bbe102d93fdc3a4cd5752beba2fa` | — |
| `corpus/evidence/round12-fleet/r12-prior-art-transport.md` | `457508defddcd3a15d37b6eb9d8f8b96f75c1860670d68644e3681ab5438c1a6` | — |
| `corpus/evidence/round12-fleet/r12-critic-design.md` | `bd48683e12f4b871371fad877500b217f3bf6d89ffb9cf717c6a117d0c94004a` | — |
| `corpus/evidence/round12-fleet/r12-report-final.md` | `1b5bcd5691a9995a5c6ee6d2398ba6fbe04414edbadc7704e2cedb792d4b532a` | — |
| `corpus/evidence/round12-fleet/r12-log-final.md` | `7be6e4f7136766632746e56c5f245aced612c5ba2e8d1a3247acbd3222fe80c3` | — |
| `corpus/evidence/round12-fleet/r12-doc-deltas-final.md` | `e4135a8e6472cf5e41cf82a3782504e79cd5a53d041d5f9981272ad311ca3dba` | — |
| `corpus/evidence/round12-fleet/r12-review-citations.md` | `a77e722f27ec3b265b8b50c7ffba9e1c0c694bbfc7a2c18814a81734e0311924` | — |
| `corpus/evidence/round12-fleet/r12-scope-audit.md` | `d328e72100eccf1caae82a6851d70f680c696e051624a741fff290a80ed0cda1` | — |
| `corpus/evidence/round12-fleet/r12-mock-smoke.md` | `c05ce4e9f28478b4a92d043a90d681c98f452ee0fec224bbc13ef7c0f468368f` | — |
| `corpus/evidence/round12-fleet/INTEGRATOR-NOTES.md` | `bab2b3261ca9a2e0d84adff20ae3f302597d5e2f9cd98a25239784c76313b83e` | — |
| `corpus/evidence/round13-ack-state/audit_ack_schedule.py` | `f250abd518f4d7802c5c1008bedcf52603c393957b57cbb9c54e28710bba066d` | — |
| `corpus/evidence/round13-ack-state/analyze_ack_state.py` | `87d01584e3ab3022139b044b26dcdb16936b67b12ed413dee67f7e4c253404e4` | — |
| `corpus/evidence/round14-fleet/r14-critic-landed.md` | `f032fd9d229f860e179eed87b9becfa19b8f45285099468739a53055d64fa1af` | — |
| `corpus/evidence/round14-fleet/r14-scribe-drafts.md` | `5d21abaabc5a95282f659065317a9303b65804e5a81b7b299e137932daaba6a0` | — |
| `corpus/knowledge/bench-arena-round12-ladder.md` | `8ce2a99f1bf129ce03e41b83f1fdedc065d6faa77349d77a57ddeda1343c33d8` | — |

## Working-tree file disposition

Snapshot command: `git status --short --untracked-files=all` → 0 staged, 2 modified, 53 untracked before this gate file. **COMMIT** below means land the listed bytes as evidence/archive, not endorse every historical sentence; the falsifications above govern. The three official index/ledger files were unchanged in this snapshot.

| Path | Action | Reason |
|---|---|---|
| `SKILL.md` | **FIX-FIRST** | Root-relative bare citations at the lines named in claim 7 do not resolve; use the existing fully qualified paths. |
| `grader.py` | **COMMIT** | Main reports 732 checks/exit 0; not rerun here (no project-wide validation). Do not claim an `analysis_r12.md` byte pin: `R12_PINS` has only JSONL/run-log keys. |
| `corpus/evidence/round12-ladder/analysis_r12.md` | **FIX-FIRST** | Its one generated provenance line differs from current regeneration; normalize or explicitly record the path-sensitive byte limit before using as a byte-identical artifact. |
| `corpus/evidence/round12-ladder/ordering.log` | **COMMIT** | Hash timestamps and launch/request evidence are useful; launch and earliest request serialize to the same second, so strict sub-second ordering is `[INFERENCE]`, while the prereg hash clearly predates both. |
| `corpus/evidence/round12-ladder/power_analysis_r12.md` | **COMMIT** | Filed family-1/family-2 floors and the E4/E5 power caveats are load-bearing. |
| `corpus/evidence/round12-ladder/power_r12.py` | **COMMIT** | Re-runnable seeded power calculation. |
| `corpus/evidence/round12-ladder/precheck_r12.py` | **COMMIT** | Re-runnable generation/schema precheck. |
| `corpus/evidence/round12-ladder/predict_r12.py` | **COMMIT** | Filed predictor machinery. |
| `corpus/evidence/round12-ladder/predictions-r12-perproblem.jsonl` | **COMMIT** | Hashed preregistered prediction events. |
| `corpus/evidence/round12-ladder/predictions-r12-signevents.jsonl` | **COMMIT** | Hashed preregistered sign-event predictions. |
| `corpus/evidence/round12-ladder/predictions-r12.md` | **COMMIT** | Hashed preregistration and run-level forecast record. |
| `corpus/evidence/round12-ladder/prereg-bundle.sha256` | **COMMIT** | 9/9 entries verify against the current bundle. |
| `corpus/evidence/round12-ladder/prereg-precheck.log` | **COMMIT** | Records the pre-request generation/schema gate. |
| `corpus/evidence/round12-ladder/probe_plan_r12.md` | **COMMIT** | Hashed design of record; 416 pass-event amendment and schedule are explicit. |
| `corpus/evidence/round12-ladder/probe_r12.py` | **COMMIT** | Hashed probe/generator source. |
| `corpus/evidence/round12-ladder/recompute-run.log` | **COMMIT** | Preserve as historical output; it records a path spelling that is not portable, noted in F-R12-1. |
| `corpus/evidence/round12-ladder/recompute_r12.py` | **FIX-FIRST** | Output embeds an absolute source path and therefore changes with path casing; normalize before promising portable byte identity. |
| `corpus/evidence/round12-ladder/results-r12.jsonl` | **COMMIT** | Primary run bytes; SHA-256 and MD5 recorded above and independently re-read. |
| `corpus/evidence/round12-ladder/run.log` | **COMMIT** | Primary run log; SHA-256 and MD5 recorded above. |
| `corpus/evidence/round12-ladder/run_r12.py` | **COMMIT** | Hashed runner; do not change the run bytes as part of this audit. |
| `corpus/evidence/round12-fleet/INTEGRATOR-NOTES.md` | **COMMIT** | Contains the controlling 416 denominator correction and recorded L1 adjudications. |
| `corpus/evidence/round12-fleet/grader_r12_draft.py` | **COMMIT** | Historical development artifact; r11 has the same `grader_r11_draft.py` precedent. |
| `corpus/evidence/round12-fleet/mock_server_r12.py` | **COMMIT** | Reusable mock source. The expected r11-equivalent JSONL/log are absent; see Gaps. |
| `corpus/evidence/round12-fleet/r12-connector.md` | **COMMIT** | Preserve the L2 report; do not reuse its superseded 448 pass-event count. |
| `corpus/evidence/round12-fleet/r12-critic-design.md` | **COMMIT** | Pre-hash critic record; the listed pre-run defects and dispositions are evidence. |
| `corpus/evidence/round12-fleet/r12-doc-deltas-final.md` | **COMMIT — archive only** | Preserve its unresolved/stale state; not paste-ready (17 vs 18 ladder files, stale analysis hash, placeholders). |
| `corpus/evidence/round12-fleet/r12-doc-deltas.md` | **COMMIT — draft archive** | Round-11 precedent includes draft doc files; keep placeholders visibly draft, do not apply them. |
| `corpus/evidence/round12-fleet/r12-endpoint-freshness.md` | **COMMIT** | The `/tmp` capture is reproduced in full with hashes in this artifact, so it is not sole temporary evidence. |
| `corpus/evidence/round12-fleet/r12-grader-notes.md` | **COMMIT — archive** | Historical implementation notes; current gate status is not inferred from its old run. |
| `corpus/evidence/round12-fleet/r12-log-draft.md` | **COMMIT — draft archive** | Preserve as a draft; do not append its unresolved text. |
| `corpus/evidence/round12-fleet/r12-log-final.md` | **COMMIT — archive only** | It still has placeholders and the false `ddfe...` analysis hash; not paste-ready for `LOG.md`. |
| `corpus/evidence/round12-fleet/r12-mock-smoke.md` | **COMMIT — archive** | Preserve commands/failing-before note; its result captures remain temporary and are not the missing durable mock JSONL. |
| `corpus/evidence/round12-fleet/r12-mutation.md` | **COMMIT — historical report** | Preserve the battery results; its statement that the promoted recomputer currently fails is superseded by the observed 165/165 selftest. |
| `corpus/evidence/round12-fleet/r12-prior-art-ladder.md` | **COMMIT** | Fetched-source ledger and C1/C3 verdicts underpin the novelty adjudication. |
| `corpus/evidence/round12-fleet/r12-prior-art-transport.md` | **COMMIT — preserve with erratum** | Keep the L2 prior-art record; its 448 C5 event denominator is superseded by the hashed plan's 416. |
| `corpus/evidence/round12-fleet/r12-recompute-notes.md` | **COMMIT — archive** | Preserve historical design decisions; its `/tmp/r12-verify/gen.py` synthetic fixture is not load-bearing evidence for the real run. |
| `corpus/evidence/round12-fleet/r12-report-draft.md` | **COMMIT — draft archive** | Round-11 precedent includes report drafts; do not use placeholders as current facts. |
| `corpus/evidence/round12-fleet/r12-report-final.md` | **COMMIT — archive only** | Preserve the historical falsifiable-target record; unresolved placeholders, false analysis hash, and absent r12 critic prevent using it as the current final report. |
| `corpus/evidence/round12-fleet/r12-review-baseline.md` | **COMMIT** | Re-runnable pointer review; temporary output captures are not sole support for its commands. |
| `corpus/evidence/round12-fleet/r12-review-citations.md` | **COMMIT — archive with errata** | Preserve review; row 407's “committed mock run” points to `/tmp`, not an in-repo JSONL. |
| `corpus/evidence/round12-fleet/r12-scope-audit.md` | **COMMIT — archive with caveat** | Preserve the scope ruling; F6/F7 mock/smoke counts are sourced from temporary captures, not repo files. |
| `corpus/evidence/round12-fleet/recompute_r12_draft.py` | **COMMIT — historical draft** | r11 has the same `recompute_r11_draft.py` precedent; promoted engine is the run-time instrument. |
| `corpus/evidence/round13-ack-state/analyze_ack_state.py` | **COMMIT** | Hermetic, read-only r11 state audit; input hash and observed counts are recorded above. |
| `corpus/evidence/round13-ack-state/audit_ack_schedule.py` | **COMMIT** | Hermetic, read-only r9/r11 intent-denominator audit; its declared scope is not r12. |
| `corpus/evidence/round14-fleet/drafts/lessons-round-12.md` | **COMMIT — draft archive** | Editorial draft, not the canonical `corpus/lessons` entry. |
| `corpus/evidence/round14-fleet/drafts/lessons-round-13.md` | **COMMIT — draft archive** | Editorial draft, not the canonical `corpus/lessons` entry. |
| `corpus/evidence/round14-fleet/drafts/lessons-round-14.md` | **COMMIT — draft archive** | Editorial draft, not the canonical `corpus/lessons` entry. |
| `corpus/evidence/round14-fleet/r14-connector.md` | **COMMIT** | Peer-owned L2 artifact; its content gate is the connector owner's scope. |
| `corpus/evidence/round14-fleet/r14-critic-landed.md` | **FIX-FIRST** | Its “fresh implementation” execution harness is `/tmp/r14critic_verify.py` and is not included; retain only after making the independent method durable or explicitly limit its claim. |
| `corpus/evidence/round14-fleet/r14-mutation.md` | **COMMIT** | Peer-owned L2 artifact; its content gate is the mutation owner's scope. |
| `corpus/evidence/round14-fleet/r14-revenger-r13.md` | **COMMIT** | Peer-owned r13 review artifact; its content gate is the owner's scope. |
| `corpus/evidence/round14-fleet/r14-review-priorart.md` | **COMMIT** | Peer-owned prior-art artifact; its content gate is the reviewer's scope. |
| `corpus/evidence/round14-fleet/r14-scout-surfaces.md` | **COMMIT** | Peer-owned surface audit; its content gate is the scout's scope. |
| `corpus/evidence/round14-fleet/r14-scribe-drafts.md` | **FIX-FIRST before applying** | Its novelty block treats the second-family direction as a new qualifying construct and attributes r12 ack conclusions to the r13 scripts, whose declared inputs are r9/r11. Narrow the pasted novelty rationale to C1 (C3 caveated) and cite the separate r12 schedule calculation. |
| `corpus/knowledge/bench-arena-round12-ladder.md` | **FIX-FIRST before indexing** | Its “python3 -” independent tally has no code body; the independent verifier it describes is throwaway. Link/inline durable verification (Appendix A here) before indexing it as independently re-derived. |
| `corpus/evidence/round14-fleet/r14-landing-gate.md` | **COMMIT** | This gate artifact; contains the reproducer, hashes, novelty decision, and full path dispositions. |

## Gaps

- **MAJOR — portable analysis bytes:** normalize the `Generator source:` field, regenerate, update the actual hashes, and either pin `analysis_r12.md` in `R12_PINS` or state explicitly that the gate checks semantic outputs rather than a byte hash. Do not copy `ddfe60d2...` into canonical docs.
- **MAJOR — durable mock evidence:** add the r11-equivalent r12 mock JSONL and run log, or remove claims that those captures are committed/reproducible from a stored run. `mock_server_r12.py` exists; `mock-*.jsonl` and `mock-run.log` do not.
- **MAJOR — documentation links:** qualify the SKILL citations from repository root before landing the modified `SKILL.md`.
- **MAJOR — independent-verifier provenance:** the r14 critic's temporary harness and the knowledge draft's incomplete `python3 -` command are not durable. Appendix A is a copyable independent reproduction for C1 and E2-E5; do not imply it verifies uncomputed forecast/calibration details.
- **MAJOR — canonical landing artifacts:** no `LOG.md`, `SCORECARD.md`, or `corpus/README.md` change existed in this snapshot. L1 still owns the current-round table, correct HEAD anchor, and both-direction index/LOG updates; this review does not create those changes.
- **MINOR — wording/power:** keep C3 as a fixed-emission dissociation, not a single-mechanism proof; keep C4 as floor-level directional data; call C2 repeatability; call C5 same-problem persistence skill. The r12 launch and first request share second-resolution timestamp `01:19:59Z`; strict within-second ordering is `[INFERENCE]`, while the prereg hash at `01:16:08Z` clearly precedes the first request timestamp.
- **FATAL:** none to the raw C1 data or its independently recomputed ordered statistic. The landing is nevertheless not ready until the MAJOR evidence/document issues are resolved or explicitly carried as limitations.
