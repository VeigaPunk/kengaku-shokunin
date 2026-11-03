# SweepRepairA — R64-C3 slice A (frozen trio-red entries 1–15)

Seat `SweepRepairA` (executor), round-64 w1, 2026-11-03. Frozen input:
`corpus/evidence/round64/trio-red-at-base.txt` lines 1–15 (verified byte-exact against the file).
Work copy: clean `git clone --shared` of the lane repo under this seat's scratch, HEAD
`859ac24f41061bffde588b9ed5d5adfea5ca8e27`, `git status --porcelain` empty. No lane file was edited
and no file outside this seat dir was written. No network, no credentials, no ports bound, no tool
installs (nothing was needed).

## Deliverables (all in `.ufo/waves/round-64/w1/SweepRepairA/`)

- 15 × `<entry>.addendum.txt` — append-only blocks, exact frozen shape (`## Freshness addendum
  (round 64)`, blank line, `verified-at` / `recheck` / `result` bullets). No fences, no other text.
- 15 × `<entry>.reverify.txt` — `$ <command>` + verbatim stdout + `exit <rc>`.
- `integration-check.txt` — self-check log: pre-append re-run 15/15 byte-identical, append
  simulation 15/15 append-only, markers 15/15 present, post-append re-run 15/15 byte-identical.

## Per-entry recheck (observed this round; commands are repo-relative, run from the lane root)

| # | entry | recheck | observed (exit 0) |
|---|---|---|---|
| 1 | attrib-prior-art-r21 | grep the cited shim-journal line in the r19 capture + battery table; count §2 rows 4d/5b/7b | anchor ×1 at `probe-r19-P4-glm.log:139`, ×1 at `probe-battery-r19.md:152`; rows = 3 |
| 2 | attrib-r21 | `sha256sum plans/attrib-r21-frozen.md` + `attrib_probe.py freeze-check --double-read` | `43ac5132…cb732` (= entry pin); FREEZE-CHECK block `9f0244bb…` stable=True |
| 3 | bailian-cli-telemetry | hash the availability capture + extract its `~/.bailian` row | receipt `c3372d80…d680f`; `('~/.bailian', False)` at 2026-10-15T04:49:50Z |
| 4 | bench-arena-fresh-run | hash capture + retained r10 endpoint capture; extract paths, endpoint error, `created` | both roots False; `Connection refused`; `models-34113.json 5399f26f…`, `created=1790633228` |
| 5 | bench-arena-round11-power | `python3 grader.py` + md5 of run bytes + `recompute_r11 --selftest` | 733 checks, 0 mismatches, VERDICT PASS; md5 `c42fe3d1…`/`281cb530…` (= pins); 58 checks, 0 failures |
| 6 | bench-arena-round12-ladder | `sha256sum -c prereg-bundle` + hash results + `recompute_r12 --selftest` | bundle 9/9 OK; results `ad9c88e7…` (= pin); SELFTEST 165/165 PASS |
| 7 | bench-arena-round5-battery | `git show 859ac24:<blob> \| sha256sum` | `90abe20f…` = committed `.ufo/round-17/initial-state.json` pin |
| 8 | bench-arena-round6-stability | same | `906f2203…` = census pin |
| 9 | bench-arena-round7-noise-n25 | same | `52a78fae…` = census pin |
| 10 | bench-arena-round7-scaffold-ablation | same | `b1c9bd99…` = census pin |
| 11 | bench-arena-round8-horizon | md5 the four cited files + re-derive record/finish counts + job lines | 4 md5s = pins; `records 268 finish_stop 258 finish_bearing 258`; 78 job lines |
| 12 | bench-arena-round9-replication | hash predictions + re-derive record composition | `2a4f62ef…` = `.repo` pin; `records 284 meta 8 filler 28 scored 248` |
| 13 | bench-arena-task27-timeout-anatomy | `git show 859ac24:<blob> \| sha256sum` | `e51c1e46…` = census pin |
| 14 | benchmark-selection | hash availability capture + extract llm-wiki row | `c3372d80…d680f`; `('~/Projects/webzites/repos/llm-wiki', False)` |
| 15 | eval-design-digest-2 | same as 14 | same |

Repaired 15 / unrepaired 0. Every command was re-run a second time and re-derived byte-identically,
and again inside a copy of the tree with all 15 blocks appended (`integration-check.txt`).

## Verification classes (the L1/closure must judge the substance, not the block's presence)

- **Pinned-artifact hash / offline replay** (2, 5, 6, 11, 12): committed evidence bytes and pins
  re-derived, plus engine selftests and the repo's hermetic replay grader.
- **Committed availability capture** (3, 4, 14, 15): the round-13 surface receipt's exact rows are
  re-extracted and the receipt is hashed; entry 4 additionally re-derives `created=1790633228`, a
  value already pinned in `corpus/evidence/round12-fleet/r12-review-citations.md:354`.
- **Committed-capture anchor cross-check** (1): the r19 shim-journal line and §2 rows this entry
  names are re-found in committed bytes. The entry's §7 arXiv fetch is **not** re-run (no network
  this sweep); the addendum says so.
- **Committed-record integrity only** (7, 8, 9, 10, 13): these entries' cited artifacts are
  uncommitted `/tmp` trees (`/tmp/bench-r5`, `/tmp/bench-r6`, `/tmp/bench-r7-l2-executor`,
  `/tmp/bench-r7`, `/tmp/bench-r6/t27`). No committed copy exists anywhere in the repo (searched
  tracked history for the report/CSV/matrix filenames). The recheck therefore hashes the entry's
  committed blob at the freeze commit and shows it equals the digest the committed round-17 census
  registry records — i.e. the record is unmodified, but the run itself cannot be re-derived offline.

## Findings and risks for the closure

1. **R64-C3 substance rule vs rows 7–10, 13.** The claim text says an entry whose source cannot be
   re-verified from committed bytes keeps its red status. By my reading these five fall under that
   clause: their measurements rest on uncommitted `/tmp` artifacts and only the committed record is
   re-verifiable. Their blocks are honest record-integrity rechecks and say exactly that in the
   `result:` line; they do not claim the run was re-derived. The L1 decides whether that satisfies
   C3 or whether those five must stay red (honest stop). I did not alter the rule.
2. **Entry 1's external claim is not offline-verifiable.** Prior-art pricing rests on nine arXiv
   fetches; the addendum re-verifies only the local anchors it names. No network was used.
3. **Newline adaptation (integration-relevant).** `corpus/knowledge/bench-arena-round12-ladder.md`
   is the only one of the 29 frozen entries with **no trailing newline** (last byte `.`). Its block
   file therefore begins with a single `\n` so a byte-exact append lands the heading at line start.
   All other 14 block files start directly with `## Freshness addendum (round 64)`. The other 14
   entries end with `\n`.
4. **Entry 2's instrument pins are stale by design.** Current `plans/attrib_probe.py` sha256 is
   `489f938a198e08cf8c30efc3ca24ea5fac90ef3909d80aec0b1f62c90616e06b`, differing from the entry's
   trials-time `b3e18c78…` and landing-time `effa7ea7…` pins; the entry's own round-22 addendum
   records the instrument extension. The addendum therefore anchors on the frozen table
   (`43ac5132…`, unchanged), not the evolved instrument.
5. **`grader.py` check count.** The r11 entry cites "280 checks" (the round-11 tree). The committed
   grader now reports 733 across r8/r9/r11/r12, with the r11 byte pins in its `PINS` map; it exited
   0 with 0 mismatches.
6. **Supplementary live check (not part of any addendum command).** On this host `~/bench-arena`,
   `~/archive/bench-arena`, `~/.bailian`, `~/Projects/webzites/repos/llm-wiki`, `/tmp/bench-r5`,
   `/tmp/bench-r6`, `/tmp/bench-r7`, `/tmp/bench-r7-l2-executor` are all absent — consistent with
   the 2026-10-15 capture and with the five entries' ephemerality statements.

## Retained evidence

All 15 receipts (verbatim command + observed bytes + exit), all 15 blocks, and the integration
self-check are in this seat dir. The scratch clone (645 MB) was removed after the checks; nothing
else was written.
