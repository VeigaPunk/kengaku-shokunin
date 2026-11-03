# Round 67 — a torch pipeline-parallel grader replayed offline; the round-65 receipt gate's strict mode; and the round-66 closure's open rows

author: kengaku L1 (round 67, attempt 1), 2026-11-03. Lane-root base for every path below:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Claims (frozen at `dcc39ea3`): `plans/round-67-claims.md`
(R67-C1 coverage, L0-capped at 7, capability `offline-torch-pipeline-parallel-grader-probe`; R67-C2 operability,
held at ceiling 10). Wave `.ufo/waves/round-67/w1`: v1, 13 seats. This draft is seat `LessonDraft`'s output;
the L1 files it as `corpus/lessons/round-67.md`. Receipts cited below are copies in
`.ufo/waves/round-67/w1/LessonDraft/receipts/` (the scratch copies are reaped).

## Mistakes

Class · evidence pointer · captured-by · fix. Row numbers restart at 1 for this lesson; the classes follow the
round-66 lesson's taxonomy (`vacuous`, `survivor`, `stale-premise`, `reference-drift`, `number-drift`, `scope`,
`attribution`, `landing`).

| # | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| 1 | `stale-premise`: the R66-C2 predicate required a `PROBE` line the committed round-65 receipt never carried | `grep -c '^PROBE' corpus/evidence/round65/sqlite-gcov-probe.txt` → `0` (`receipts/probe-line-check.txt`); `plans/round-66-claims.md` R66-C2 kill rule (b); `corpus/lessons/round-66-verifier-spotcheck.md` §2 R66-C2 ("Kill rule (b) holds on committed bytes") | none before the freeze or the run: the round-66 freeze review checked the proposal's receipts, not the shape of the committed receipt (`plans/round-67-claims.md` F2). The round-66 non-author closure caught the failed kill rule only after the run. | R67-C2 (`plans/round-67-claims.md`, frozen at `dcc39ea3`): the successor binds the header `# instrument … version=<V>` to `PROBE_VERSION` in the probe bytes, not a `PROBE` sha, and its claim text carries the pre-freeze read of the committed receipt. Its kill rule (b) is its own test: strict must accept `corpus/evidence/round65/sqlite-gcov-probe.txt`. Status at `dcc39ea3`: the strict mode is **not landed** (`grep -c strict plans/round65_c1_sqlite_probe.py` → `0`); the proposal is `.ufo/waves/round-67/w1/StrictGateBuild/proposed/` (see row 2 and `## Gate`). |
| 2 | `vacuous`: the receipt gate checked that a field is present, not what it says, so a hand-fabricated receipt passed | `.ufo/waves/round-65/w1/SecurityScan.md` M-1; fixture `corpus/evidence/round66/red/fabricated-r65.txt` (sha256 `17436b58…`, identical to `receipts/fixture-identity.txt`); red-before `corpus/evidence/round66/red/red-before-r65-checker.txt` (`CHECK ok cases=5` / `PREDICATE R65-C1 pass`, rc 0) | none before landing: the frozen predicate checked presence. SecurityScan M-1 reported it after landing; the round-65 lesson priced it as a named limitation; no gate refused it. | R67-C2 strict clauses s1–s6, counted only once shown able to fail. Shown: (a) the fabricated fixture with the strict mode exits 1 with `CHECK defect:` findings (`receipts/strict-scratch-cmd1.txt`: `s1 header-missing`, `s4 gcc-line-missing`, `s5 run-driver 'fabricated - nothing ran' != '/usr/bin/python3 /ctl/driver.py'`); (b) the committed round-65 receipt with strict exits 0 and default mode exits 0 (`receipts/strict-scratch-cmd23.txt`); (c) default-mode output is identical between the committed and the proposed probe on both fixtures (`receipts/default-mode-compare.txt`, `default-output-identical=yes`). The strict run is valid only in a lane-shaped tree: `strict_lane()` resolves the lane from the probe's own path, so run from its seat dir the same commands fail with `s1 probe-bytes-missing` and `s2 grader-bytes-missing` (`receipts/three-counting-commands.txt`, which records that failure). Named limitation: a receipt that copies every value from the committed bytes still passes strict. The fix is in the proposal only until it lands in `plans/`. |
| 3 | `landing`: the round-66 landing left a superseded provenance pointer in a knowledge entry | `corpus/knowledge/tb2-sqlite-gcov-offline.md:4` at `dcc39ea3` still reads `source: S233 (corpus/SOURCES.md) …` (`grep -c '^source: S233'` → `1`, `receipts/s233-provenance.txt`); S236, the row that supersedes S233, is present (`grep -c '^| S236 '` → `1`); the kv-store entry received the dated re-point this one did not (`tb2-kv-store-grpc-offline.md:232`) | the round-66 non-author closure, `corpus/lessons/round-66-verifier-spotcheck.md` §6 item 1, after landing; routed, not fixed at the tip. | a dated, append-only re-point of line 4 to S236, as the kv-store entry does at `:232`. |
| 4 | `stale-premise`: the round-66 lesson closed a round-65 pointer correction that the tip does not carry | `corpus/lessons/round-66.md` Carried row 5 reads "closed (this landing)"; `SKILL.md` line 686 at `dcc39ea3` (read with `git show dcc39ea3:SKILL.md`) still names `corpus/evidence/round65/battery-run.txt` as the home of the live BUILD/RUN/FILES lines, and the file carries no dated correction for it (its only `2026-11-03` line is an unrelated row); `SCORECARD.md` line 2885 at `dcc39ea3` names `battery-run.txt` too (`receipts/r65-pointer-status-line686.txt`) | the round-66 non-author closure, `corpus/lessons/round-66-verifier-spotcheck.md` §6 item 2, after landing ("rows 4–7 … not yet landed"). | a dated correction at the four pointers the round-66 lesson's Mistake row 4 names (`SKILL.md:686`, `SCORECARD.md:2885`, `LOG.md:2512`, round-65 report lines 14 and 78); this round read only the first two at the tip. Row 5 of the round-66 Carried table reopened until those bytes exist. |

## Sweep

**Sections read** of `corpus/lessons/round-66-verifier-spotcheck.md` (all seven): §1 Step-1 conformance, §2 per-claim
re-check (R66-C1, R66-C2, axes, axis-harm), §3 admission, §4 discernment spot-check (its table), §5 trend verdicts,
§6 routed defects (items 1–6), §7 SHONEN, and the trailing "Commands run" block.

**Command:** `python3 .ufo/waves/round-67/w1/LessonDraft/receipts/sweep.py` (copied from the scratch sweep; output
`receipts/sweep-output.txt`; exit 1).

**Output (excerpt; `…` marks trimmed text; the full output is `receipts/sweep-output.txt`):**

```
--- section 2 candidate statements ---
  [MINED row-1 (R66-C2 predicate froze on a PROBE line the committed receipt never carries)] - Frozen kill rule (b): …
--- section 6 candidate statements ---
  [ROUTED item 2] 2. **Open mistake rows 3–7 (from the lane's own report).** Row 3 (strict receipt gate, fabricated receipt admitted, M-1) …
SWEEP section2-mined=1 section6-routed=1 new-rows=1
SWEEP VERDICT new-row-found
```

**Reading of that output.** The second §2 candidate (`Verdict: **C2 not verified** …`) restates the kill-rule (b)
failure of row 1; it is not a new row. The pattern scan missed §6 item 1 because its text carries none of the
marker words, so §6 was also read by hand. Hand-reading found items 1 and 2 of §6 as further rows, verified at
the tip (rows 3 and 4 above; `receipts/s233-provenance.txt`, `receipts/r65-pointer-status.txt`,
`receipts/r65-pointer-status-line686.txt`). The sweep therefore did **not** find "no further row": it found two,
and they are carried above. §2's R66-C1 bullets, §3, §4, §5 and §7 carry verdicts and no defect statement beyond
row 1 and row 2's references.

## Gate

**Sources admitted this round** (both opened live on 2026-11-03; both `mined`, tier A, `corpus/SOURCES.md:253-254`):

- **S238** — Terminal-Bench 2.0 `torch-pipeline-parallelism` grader, `tests/test_outputs.py` at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`,
  https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/torch-pipeline-parallelism/tests/test_outputs.py .
  Accessed 2026-11-03 (live `curl`, HTTP 200; sha256 `23574246a407163a8e6581c84287cc2f1eb745efbaad2a317a5a28c39958c64f`,
  equal to the capture; `receipts/live-refetch.txt`).
  Located quote, grader line 157 of the capture:

  QUOTE S238 | corpus/evidence/round67/sources/torch-pipeline-parallelism-test_outputs.py | AFAB violation: found forward after backward at {key}

  (`grep -c -F 'AFAB violation: found forward after backward at {key}'` on the capture → `1`; `receipts/source-quotes.txt`.)

- **S239** — Terminal-Bench 2.0 `torch-pipeline-parallelism` `instruction.md` at the same pin,
  https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/torch-pipeline-parallelism/instruction.md .
  Accessed 2026-11-03 (live `curl`, HTTP 200; sha256 `989bfcf0c54baf6c8cdc391743dbb2f9e858c5779dd85112536875d4d1b2dcd2`,
  equal to the capture; `receipts/live-refetch.txt`).
  Located quote, instruction line 18 of the capture:

  QUOTE S239 | corpus/evidence/round67/sources/torch-pipeline-parallelism-instruction.md | Run forward passes for all microbatches first, then run backward passes.

  (`grep -c -F` on the capture → `1`.)

**Assimilation: none.** Reason (`plans/round-67-claims.md` F3): no `merge/kengaku/` theme is admitted this round;
the round-54 mass id drift stays open in L0 `kengaku | round-54`; adopting nothing is the honest state.

## Carried

The L0 questions carried, unchanged; nothing assumed answered:

- `kengaku | round-25/33/51` — coverage L0 cap (R67-C1 does not lift it: a grader execution does not lift the cap).
- `kengaku | round-56` — carried, unchanged.
- `kengaku | round-63` — carried, unchanged (amended K2 detector).
- `kengaku | round-54` — merge/kengaku id drift; assimilation none this round.
