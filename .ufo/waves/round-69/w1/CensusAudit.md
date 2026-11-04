# CensusAudit — registry state audit, kengaku round-69 w1 (2026-11-03)

Leaf seat, read-only: every command below was run against the lane at
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` (L). No registry file was edited; no git
write command was run anywhere. Scratch `/fast/scratch/hyaku/kengaku-r69/CensusAudit` was
created, used, and deleted before yield (receipt copied to
`.ufo/waves/round-69/w1/CensusAudit/census.txt` first). No tools installed (none needed).

## 0. Lane state the round starts in

- `git -C L rev-parse HEAD` → `b288e8e03bdfed715bbb6de0ea166e2c465c0453` — the round-69
  freeze commit ("round-69 freeze: R69-C1 nginx-request-logging offline replay probe + …,
  census-before", 2026-11-03 21:05:28 -0300); `git -C L log --oneline -2` confirms its
  parent is `a518980e` ("round-68 verifier spot-check (integrator, hyaku): non-author
  admit/reject"), matching the claims doc's stated base.
- Working tree is NOT clean at audit time: `git -C L status --porcelain` →
  ` M SKILL.md`, ` M corpus/QUALITY.md`, ` M corpus/knowledge/tb2-network-service-offline-grader.md`,
  ` M corpus/lessons/round-68.md`, plus untracked `.ufo/waves/round-69/w1.ready`,
  `.ufo/waves/round-69/w1.ready.dispatched`, `.ufo/waves/round-69/w1/`,
  `corpus/evidence/round69/`. `git -C L diff --stat` → 4 files changed, 17 insertions(+).
  The four modified files are exactly the C2 correction targets (E1 SKILL registry rows
  `round68_c1_pypi_finish`/`round68_c2_correction_gate`/`round68_report_contract`/
  `round68_capability_table`; E2 QUALITY; E4 verified-at; E5/E6 lesson) — the corrections
  are landing in the working tree, uncommitted, while this wave runs.
- `corpus/SOURCES.md` and the SKILL `network-service` class row are untouched by the dirty
  set (verified below), so the C1 before-counts still read at frozen-base values.

## 1. Census validate

Ran exactly: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`
(output captured to scratch `census-validate.out`).

- Exit code **0**.
- **W04 count = 24** (24 lines carry `W04`; 25 output lines total).
- Verdict line (raw): `kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md`.
  All 24 W04s are `duplicate url … across scopes` warnings (e.g. `W04 S040 duplicate url arxiv.org/abs/2301.09633 across scopes`, `W04 S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes`) — warnings only, verdict `ok`.
- Frozen-receipt check: `head -n 25 .ufo/waves/round-69/census-before.txt` vs my output →
  `diff` clean; **byte-identical** (the frozen file's 26th line is its own `rc=0` trailer).
  The census axis starts exactly at the frozen state; close can honestly record
  "census exit 0".

## 2. SOURCES.md registry

- Row count — `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → **232**.
- Highest id — `grep -oE '^\|[[:space:]]*S[0-9]{3,}' … | grep -oE '[0-9]+' | sort -n | tail -3`
  → `238, 239, 240`; **highest = S240** (last data row, line 255; file has 288 lines, no
  S-rows after 255).
- S241 free? — `grep -cE '^\|[[:space:]]*S241[[:space:]]*\|' corpus/SOURCES.md` → **0** → free.
  This confirms the R69-C1 before→after target's before side (`0 → 1` once the live-reopened
  grader row lands).
- Last three rows' cell shapes — `grep -E … | tail -3 | awk -F'|' '{print NF}'` → **NF=13 for
  S238, S239, S240** (leading+trailing empty fields + 11 content columns, matching the header
  `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` at line 21). No malformed/ragged row.
- `used-by` resolution (extracted `$12`, tested on disk, back-referenced):
  - S238 → `corpus/knowledge/tb2-torch-pipeline-parallel-offline.md` — file **exists**, 12 `S238` back-references inside it.
  - S239 → `corpus/knowledge/tb2-torch-pipeline-parallel-offline.md` — file **exists**, 10 `S239` back-references.
  - S240 → `corpus/knowledge/tb2-network-service-offline-grader.md` — file **exists**, 2 `S240` back-references.
  All three resolve to real, back-citing knowledge entries; no dangling used-by.

## 3. Claims the round-69 report must not contradict

- `grep -c 'executed 2 of 8' SKILL.md` → **1**. The class row (SKILL.md:78) reads
  `| network-service | 8 | executed 2 of 8 (round 64 kv-store-grpc; round 68 pypi-server replayed offline, R68-C1 pass …)`. This is the claims' frozen before state (→ `executed 3 of 8` after C1 lands); at audit time the flip has NOT landed.
- `grep -n 'strict attack share' corpus/lessons/round-68.md` → exactly one line, **:100**:
  `**Strict attack share.** … the strict attack share 3/12 = 25 % (floor met exactly) — the wider set is named here, never counted as attack share again.` — present with the strict role set {reviewer, critic, mutation-tester, labrat}; consistent with C2's E5 (exactly one line).
- SCORECARD (no contradiction): :569 capability `offline-network-service-grader-probe` entered round 64, re-demonstrated 68 (`R68-C1 pass`); :2822 `network-service (8 graders)` named uncovered-with-members; :2836 R63-C1 MISS row with coverage held 7 under the L0 cap — all agree with the claims' "L0-capped at 7" and the 2-of-8 → 3-of-8 member framing (nginx adds a member, not a new capability row).

## 4. Findings a claim's attacker should use

1. **Every count in this report is working-tree bytes at HEAD `b288e8e0` plus the in-flight
   dirty set listed in §0.** The four modified files do not touch `corpus/SOURCES.md` or the
   class row, so §1–§3 counts are simultaneously true of the freeze commit — but an attacker
   quoting "before" numbers later in the wave must re-check, because the C2 corrections
   (uncommitted at audit time) change SKILL/QUALITY/lesson/knowledge bytes around them.
2. **The census script reads the working tree, not HEAD.** The frozen-match holds only
   because SOURCES.md is unmodified. If a landed correction adds a duplicate URL, W04 moves
   off 24 without any registry-row edit — an "exit 0, W04=24" close claim should re-run the
   census at the landing tip rather than cite this receipt.
3. **"Census clean" would overstate.** The honest close phrasing is "census exit 0, verdict
   ok, 24 known W04 duplicate-url warnings, byte-identical to census-before" — rc 0 is a
   pass-with-warnings, not a warning-free run.
4. **S241 is the next free id** (max live id S240; 232 live rows for ids S001–S240 leaves 8
   ids in that range not present as live rows — retired/gapped; I did not enumerate which,
   not required by the seat). If two seats race to claim S241 the C1 target
   `0 → 1` can silently become 2; the claims freeze a count target, so the row must land
   exactly once.
5. Last three rows are well-formed (NF=13) with resolving used-by — no registry-structure
   defect for a C2-style row check to trip on.

## 5. Commands I did NOT run

No C1 battery, no `round69_c1_nginx_probe.py` in any mode (`--run`/`--check-receipt`/
`--render-table`/`--selftest`); no C2 gate (`round69_c2_routed_defects.py`, any mode); no
port-8080 battery and no `ss`/flock probing; no `git` write command anywhere (only
`rev-parse`, `status --porcelain`, `log`, `diff --stat`, `diff -- SKILL.md`); no edit to
SOURCES.md, SKILL.md, SCORECARD.md, QUALITY.md, lessons or knowledge; no pacman/uv/npm
install (none needed); no subagent or labrat spawned (leaf seat); no scratch beyond
`/fast/scratch/hyaku/kengaku-r69/CensusAudit` (deleted at close).
