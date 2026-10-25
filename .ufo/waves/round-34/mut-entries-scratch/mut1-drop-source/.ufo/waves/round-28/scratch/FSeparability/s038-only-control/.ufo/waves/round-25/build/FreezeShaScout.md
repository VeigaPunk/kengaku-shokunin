# FreezeShaScout — r25 C1 freeze/instrument provenance

Read-only. Base archive `git archive 6180e4fb92e90c0b172e9788e2c765d097f2e142` -> `/tmp/kengaku-r25-freeze-sha`.

## Method (offline; observed)
- `freeze-check --double-read` on `plans/attrib-r{21,22,23}-frozen.md` from the archive: 3/3 exit 0 — `9f0244bb…ba33c`, `77b8d4a0…0238`, `1b2d6a01…4f87`, each `stable=True`.
- Whole-file `sha256sum` is the wrong check (files hash `43ac5132…`/`dda50485…`/`6a0254dd…`); the pin covers the fenced block only (`plans/attrib_probe.py:142-160`).
- Git instrument versions (`git log --format=%h -- plans/attrib_probe.py`: 0d23c61, 8a08483, a2ff634): `effa7ea7…` (0d23c61), `bb6bd919…` (8a08483), `489f938a…` (a2ff634 = base blob; HEAD 3f371d2 unchanged).

## Findings
F1. **Scored pin `3d7861f8…` has no committed bytes.** `corpus/evidence/attrib-r22-opencode-trials.log:207` re-verifies it; `r22-legs.log:5,8` and `r22-legs-hyper.log:5,8` start under it. But `plans/attrib-r22-frozen.md` has one commit (8a08483) whose block-sha is `77b8d4a0…`; §6 carries only `124ade67…`/`77b8d4a0…` (`:235,:245`). The `3d7861f8` line was replaced in freeze-3 (`r22-opencode-trials.log:64-67`); no git version preserves its bytes.
F2. **r22 run-1 executed under a different table than its score block attests.** `r22-legs.log:8` meta `3d7861f8` (trials 11:50:06-11:51:50Z); block `:260` (11:57:30Z) re-verifies `77b8d4a0` (`:263`); addendum `:367` confirms. Only block `:312` (run-2) has execution pin = scoring pin = `77b8d4a0`.
F3. **Only 3 of 7 observed instrument versions are committed.** Committed: `effa7ea7` (0d23c61), `bb6bd919` (8a08483), `489f938a` (a2ff634/base). Uncommitted: `b3e18c78` (r21 trials, all r21 metas), `34c4fa67` (r22 freeze-time, `attrib-r22-frozen.md:197`), `05da8927` (r22 run+scoring, `:204`, `r22-legs.log:264,316`), `cce53a16` (r23 run+block 1, `attrib-r23-frozen.md:207-208`, `r23-stream.log:198`).
F4. **r21 score blocks record no instrument sha** (`r21-impl-ds` 130/176/222/268; `r21-impl-glm` 142). `effa7ea7` as scoring bytes is [INFERENCE] from `plans/attrib-r21-frozen.md:260-276` and block clocks 10:27:01/10:27:03Z > edit 10:26:44Z; the lane admits the gap (`corpus/knowledge/attrib-r21.md:280-292`).
F5. **r23 rescore pair: same table, different instrument.** `r23-stream.log:197,261` both pin `1b2d6a01…`; 30-row tables hash identically (`c4436beb…`) but instruments differ `cce53a16` (block 1) vs `489f938a` (block 2). Block 2 authoritative (`:339-345`). The frozen table's instrument pin is `cce53a16` (`attrib-r23-frozen.md:207-208`) — not the scoring bytes.
F6. **Dedup collision across freezes.** `r22-legs.log:312` and `r22-opencode-trials.log:204` have byte-identical 20-row tables (sha `54c7888c…`) yet pin `77b8d4a0` vs `3d7861f8`; rows came from distinct runs (11:53:41-11:55:08Z vs 11:50:45-11:52:12Z).
F7. **Index/header drift would mis-pool.** `corpus/README.md:149` says r22-opencode instrument `34c4fa67`; receipt header `:5` agrees but machine meta `:81` and scoring `:208` say `05da8927`. `README:151` says r23 instrument `cce53a16`; authoritative block `r23-stream.log:262` is `489f938a`. `README:166` calls `3d7861f8` the r22 anchor; committed live pin is `77b8d4a0`.

## Scored-block matrix (P1: last block per file authoritative)
| receipt | blocks | authoritative | table pin | verifies? | instrument at scoring | committed? |
|---|---|---|---|---|---|---|
| r21-impl-ds-trials.log | :130,:176,:222,:268 | :268 (`:316` rule) | `9f0244bb` (all 4) | yes | not recorded; `effa7ea7` [INFERENCE] | yes (0d23c61) |
| r21-impl-glm-trials.log | :142 | :142 | `9f0244bb` | yes | not recorded; `effa7ea7` [INFERENCE] | yes (0d23c61) |
| r22-legs.log | :260,:312 | :312 | `77b8d4a0` | yes | `05da8927` | **no** |
| r22-opencode-trials.log | :204 | :204 | `3d7861f8` | **NO (bytes absent)** | `05da8927` | **no** |
| r23-stream.log | :194,:258 | :258 | `1b2d6a01` | yes | `489f938a` | yes (a2ff634) |

Non-authoritative: `r22-legs:260` table `77b8d4a0`/inst `05da8927` but executed under `3d7861f8`; `r23-stream:194` table `1b2d6a01`/inst `cce53a16`.
Trial-only (0 scored trials in P1): r21-ds, r21-glm, r22-legs-hyper, r23-stream-trials — the last has two sections, `:5` (v2 pin `77b8d4a0`, inst `bb6bd919`, 13:38Z) and `:234` (v3 pin `1b2d6a01`, inst `cce53a16`, 13:46Z).

## C1 pooling rule implied by these bytes
- Groups are `(table pin, scoring instrument)`: A = r21-impl-ds + r21-impl-glm (`9f0244bb`, `effa7ea7` inferred); B = r22-legs:312 (`77b8d4a0`, `05da8927`; that instrument hardcoded max_tokens 16 against the table's 64 row — `attrib-r22-frozen.md:279-282`); C = r22-opencode:204 (`3d7861f8`, unrecoverable); D = r23-stream:258 (`1b2d6a01`, `489f938a`).
- A/B/C/D MUST NOT be pooled as one accuracy sample; per-leg recall also must not cross shims (r21 ds roster vs glm roster). B and C collapse to one row-sample under P1 dedup (F6), so C1 must name the duplicate, not count n=40.
- C1 may re-verdict from stored rows (prediction/GT/chain are in the receipts) but MUST NOT claim freeze-check re-verification for `3d7861f8` or byte-reproducibility for uncommitted instruments.

VERDICT: 3/3 committed table blocks freeze-check OK; scored pin `3d7861f8` and instruments `b3e18c78`, `34c4fa67`, `05da8927`, `cce53a16` have no committed bytes; C1 must pool only within the four (table,instrument) groups above and cannot byte-verify the r22-opencode block.

Installs: none (stdlib python3 only; no package transactions).
