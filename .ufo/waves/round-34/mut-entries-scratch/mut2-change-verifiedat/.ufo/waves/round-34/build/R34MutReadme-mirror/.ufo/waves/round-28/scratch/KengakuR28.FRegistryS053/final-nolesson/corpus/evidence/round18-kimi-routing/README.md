# round18-kimi-routing — evidence index (digest; bytes in the parent repo)

Index of the parent-fleet round 18 (kimi secondary-model routing, 2026-10-15).
The artifacts live in the parent repo at
`/home/vgpnk/Projects/shokunin/research/round-18-kimi-model-routing/` (branch
`master`); the fleet report is `../.ufo/reports/round-18/kengaku.md`. Merge
commits verified 2026-10-15 with
`git -C /home/vgpnk/Projects/shokunin log --oneline`: M1 `4738fee` (census),
M2 `7e2c473` (definitions), M3 `c2174a5` (battery), M5 `db82042` (fastmode),
M6 `bd0c690` (battery-opencode), M4 `fbae972` (routing + report). The report is
byte-identical to `routing/kengaku-round18-report.md` (`diff -q` exit 0;
committed at `389ede4`).

**Bytes are not copied here** — this is a digest repo, and the parent trees are
the SSOT. The digest of the findings is
`corpus/knowledge/kimi-model-routing-round18.md`; this file indexes what each
tree contains, its file count, and its hygiene gate.

| Tree | Files | Contains | Hygiene gate |
|---|---:|---|---|
| `census/` (M1) | 68 | `ANALYSIS.md` (13-provider / 143-entry inventory, defects D1–D9, usage/quota evidence, TTFT/TPS smoke), `manifest.json` (redacted inventory, key digests only), `raw/` live captures, `scripts/` probes + `verify_numbers.py` (every ANALYSIS figure traces to a capture) | `bash scripts/hygiene_check.sh` → `RESULT: CLEAN (0 hits)`, exit 0 (first run exited 1 on the shim capture; `probe_shims.py` redacts at capture time) |
| `definitions/` (M2) | 25 | `ANALYSIS.md` (client-semantics audit: declared vs transmitted; 121 defects / 94 notes / 46 verify-later over 143 entries), `audit-table.md` + `audit-table.json`, `config-corrections.toml` (56 splice-ready blocks + quarantine + verify-later), `raw/` (mock client captures + live probes) | `bash scripts/hygiene_check.sh` → 25 files scanned, `TOTAL HITS: 0`, exit 0 |
| `battery/` (M3) | 402 | `ANALYSIS.md` (n=2 TTFT/TPS + 9 correctness probes × 17 models, prediction scoring), `SELECTION.md` (26→17 pool diff), `SMOKE.md`, `predictions/`, `raw/` (188 live captures + telemetry), `smoke/` (188 mock captures), `raw-run.log` | `python3 scripts/hygiene_check.py .` → 402 scans, `hits: 0`, exit 0 (a round-1 self-reference doc defect was fixed; recorded in `HYGIENE.md`) |
| `battery-opencode/` (M6) | 44 | `ANALYSIS.md` (`opencode-go/deepseek-v4.1-flash`: M3-spliceable row, 11/11 requests, 0 regrade mismatches), `predictions/`, `raw/`, `smoke/`, `raw-run.log` | `python3 scripts/hygiene_check.py .` → 44 scans, `hits: 0`, exit 0 |
| `fastmode/` (M5) | 14 | `ANALYSIS.md` (service_tier acceptance sweep, phase-B TTFT/TPS, echo + quota evidence, no-go verdict + conditional protocol), `raw/` (run 1/run 2 captures, discovery + echo evidence), `scripts/` | `python3 scripts/hygiene_check.py` → 14 files, `TOTAL HITS: 0`, exit 0 |
| `routing/` (M4) | 6 | `kimi-secondary-models-round18.toml` (13-entry payload + evidence ledger + ladders + limits), `APPLY.md` (operator runbook; live config not written), `splice_secondary.py` (pinned-hash guard; dry-run verified), `kengaku-round18-report.md` (fleet report) | `python3 hygiene_check.py` → 7 files scanned (tree + fleet report), `TOTAL HITS: 0`, exit 0 |

Gate summary (all six, 2026-10-15): every tree's hygiene gate returned 0 hits /
exit 0; no credential value or credential-shaped string is in any artifact, and
the live `~/.kimi-code/config.toml` was opened read-only and never modified by
any mission.

Re-verify the merge point without the parent repo's working tree:

```bash
git -C /home/vgpnk/Projects/shokunin log --oneline -1 4738fee
git -C /home/vgpnk/Projects/shokunin log --oneline -1 fbae972
diff -q /home/vgpnk/Projects/shokunin/.ufo/reports/round-18/kengaku.md \
        /home/vgpnk/Projects/shokunin/research/round-18-kimi-model-routing/routing/kengaku-round18-report.md
```

Both commands were run 2026-10-15 when this index was written; the parent repo
merged the trees and the diff exited 0 (identical).
