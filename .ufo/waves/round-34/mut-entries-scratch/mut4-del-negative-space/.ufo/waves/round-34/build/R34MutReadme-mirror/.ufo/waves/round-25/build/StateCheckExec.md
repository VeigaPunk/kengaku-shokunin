# StateCheckExec — Kengaku round 25 C2

Axes: calibration (owned move); novelty/coverage not changed.

Files: implemented `plans/state_check.py` only in private clone `/tmp/kengaku-r25-StateCheckExec` (branch `r25-StateCheckExec`, observed HEAD `3f371d2a2ce5ccf1b40b2161210f6591a8320a0a`). This report is the only write in the lane tree. Base archive resolved to `6180e4fb92e90c0b172e9788e2c765d097f2e142`.

Behavior: offline stdlib CLI supports `--root`, `--summary`, `--json`, `--selftest`, exit 0/1/2. P2a/P2b re-run only the two frozen allowlisted Python commands; expected evidence tokens/exit are compared. `sources-registry` has no command in its evidence cell and is explicitly `OFFLINE_UNVERIFIABLE`. P2b checks the seven base axis rows, backticked paths/line and section anchors, plus named offline commands. P2c diffs the four canonical seed boxes against fleet `PROTOCOL.md`, requires one indented evidence line per box, and resolves local pointers. P2d tests the first local path without reading file contents; URL/endpoint observations are offline-unverifiable and never contacted. P2e checks frozen README row→path and base file→row membership. Later rows/files are reported `OUT_OF_POPULATION` and excluded from assertion counts.

BEFORE measurement (frozen population per `plans/round-25-claims.md:75-91`):

Command: `python3 /tmp/kengaku-r25-StateCheckExec/plans/state_check.py --root /tmp/kengaku-r25-base-6180e4f --summary` (cwd `/home/vgpnk/Projects/shokunin`)

Output:
```
assertions=238 match=228 mismatch=6 offline_unverifiable=4
MISMATCH: P2d.surface.Research notes (SSOT for eval craft).path:12 — {"ABSENT_marked": false, "exists": false, "path": "~/Projects/webzites/repos/llm-wiki", "resolved_path": "/home/vgpnk/Projects/webzites/repos/llm-wiki"}
MISMATCH: P2d.surface.Local benchmark battery.path:13 — {"ABSENT_marked": false, "exists": false, "path": "~/archive/bench-arena/", "resolved_path": "/home/vgpnk/archive/bench-arena"}
MISMATCH: P2d.surface.Served local model.path:14 — {"ABSENT_marked": false, "exists": false, "path": "/proc/1299/cmdline", "resolved_path": "/proc/1299/cmdline"}
MISMATCH: P2d.surface.Client CLI telemetry.path:16 — {"ABSENT_marked": false, "exists": false, "path": "~/.bailian/telemetry.jsonl", "resolved_path": "/home/vgpnk/.bailian/telemetry.jsonl"}
MISMATCH: P2d.surface.Model catalogs.path:17 — {"ABSENT_marked": false, "exists": false, "path": "~/.bailian/skills/bailian-docs-llm-wiki/models", "resolved_path": "/home/vgpnk/.bailian/skills/bailian-docs-llm-wiki/models"}
MISMATCH: P2e.file-to-row.lessons/round-24-verifier-spotcheck.md:81 — {"indexed": false, "path": "lessons/round-24-verifier-spotcheck.md", "row_lines": []}
VERDICT: FAIL — at least one frozen assertion mismatches
```

Evidence notes: `PROVINCE.md:12-17` contains the tested surface claims; absent local paths above lack an `ABSENT` row marker. Base `corpus/lessons/round-24-verifier-spotcheck.md` exists but is not indexed in `corpus/README.md:81-90`.

Checks: only the explicitly requested base `--summary` measurement was run; it returned 1 for the six frozen mismatches. No build, lint, formatter, selftest, or post-integration gate was run; main owns those checks. No LSP refactor was needed for this new standalone file; no LSP tool was exposed. Risks: `sources-registry` cannot be re-derived from a row command until its evidence cell names one; the recorded base mismatches remain to be handled by the integrator.

Installs: none.

VERDICT: C2 state checker implemented in the scoped private clone; base BEFORE measurement retained above (6 mismatches, 4 offline-unverifiable).