# P2d — PROVINCE.md `## Surfaces`: first-path existence (read-only)

Base: lane HEAD `3f371d2a2ce5ccf1b40b2161210f6591a8320a0a`; `git diff 3f371d2 -- PROVINCE.md`
empty, so the bytes checked are the base bytes.

Method: for each row of `## Surfaces` (`PROVINCE.md:12-20`) took the **first backticked local
path**, expanded `~`→`/home/vgpnk`, resolved repo-relative paths against the lane repo, and ran
`test -e` only. No HTTP client was run. `ss -ltn 'sport = :34113'` was read as local kernel
state, not as endpoint verification.

| Row | First path (expanded) | test -e | Row carries `ABSENT` | Verdict |
|---|---|---|---|---|
| L12 Research notes | `/home/vgpnk/Projects/webzites/repos/llm-wiki` | MISSING | no — row only says `test -e` → absent for the *sibling* `~/wikillm/llm-wiki` | STALE — unmarked |
| L13 Local benchmark battery | `/home/vgpnk/archive/bench-arena/` | MISSING | no | STALE — unmarked |
| L14 Served local model | `http://127.0.0.1:34113` (endpoint, not a path); first local path `/proc/1299/cmdline` | n/a; `/proc/1299/cmdline` MISSING | no | OFFLINE-UNVERIFIABLE — live-state claim |
| L15 Route telemetry | `/home/vgpnk/Projects/bounties/ledger/telemetry.jsonl` | MISSING | yes, literal `**ABSENT**` | CONSISTENT-ABSENT |
| L16 Client CLI telemetry | `/home/vgpnk/.bailian/telemetry.jsonl` | MISSING | no | STALE — unmarked |
| L17 Model catalogs | `/home/vgpnk/.bailian/skills/bailian-docs-llm-wiki/models/{index.md,models.jsonl}` | MISSING (both members after brace expansion) | no | STALE — unmarked; HF/OpenRouter URL facets also unverifiable |
| L18 Own probe artifacts | `corpus/evidence/round8-horizon/` | EXISTS (all 10 listed dirs exist) | n/a | CONSISTENT |
| L19 In-repo gate | `grader.py` | EXISTS | n/a | CONSISTENT |
| L20 Public literature | `corpus/knowledge/eval-prior-art-calibration.md` | EXISTS | n/a | OFFLINE-UNVERIFIABLE (surface itself is URLs) |

## Findings (each grounded in observed output)

1. **Four rows are stale and unmarked.** `test -e` returns MISSING for L12, L13, L16, L17, yet
   the `ABSENT` token census over lines 11-20 is `ABSENT=1` at line 15 only
   (`awk 'NR>=11&&NR<=20{gsub(/ABSENT/,"ABSENT"); print NR, ...}'`). Parent-level checks agree the
   absences are whole-tree, not leaf-only: `ls -d` on `~/Projects/webzites/repos/llm-wiki`,
   `~/archive`, `~/Projects/bounties`, `~/.bailian` → all four `No such file or directory`.
2. **Only route telemetry is honestly marked.** L15 carries `**ABSENT**` and its path is missing:
   the one row whose marker survives a mechanical check.
3. **L14 asserts current live state that cannot be verified offline**: served id
   `Qwen3-Coder-30B-A3B-Instruct UD-IQ2_XXS`, `owned_by=llamacpp`, `n_ctx=16384`, and the
   round-10 process pin `llama-server` pid 1299 with a 41-token `EXACT_MATCH` argv. The identity
   claim is untested (no endpoint traffic), but the row's currency is contradicted by local
   evidence: `ss -ltn 'sport = :34113'` printed no listener, and `/proc/1299/cmdline`,
   `~/.config/systemd/user/qwen-coder.service`, `~/.config/llama/qwen-coder-godspeed.jinja` are
   all MISSING. State precisely: not falsified, but not reproducible today.
4. **L20's local anchor exists** (`corpus/knowledge/eval-prior-art-calibration.md`), but the row's
   surface is public URLs, so its live reachability is outside this check by assignment.
5. **Header currency claim is unsupported.** `PROVINCE.md`'s table caption says "re-verified round
   14, 2026-09-29"; with 4 of 9 first paths and all of L14's local pin paths missing, at most 3/9
   rows survive a today-`test -e`. The round-24 map below already records these as absent, so the
   defect is confined to the frozen table's marker discipline, not to lane state.
6. **Unresolved:** whether L12/L13/L16/L17 relocated elsewhere on the host was not searched; this
   item assigned existence only, and the round-24 section's own `test -e` results match mine.

Counts: 9 rows → 3 CONSISTENT (L18, L19, L20-local-anchor), 1 CONSISTENT-ABSENT (L15),
4 STALE-unmarked (L12, L13, L16, L17), 1 live-state row flagged (L14).

VERDICT: P2d fails as written — 4/9 first paths missing without an `ABSENT` marker; L14 is
offline-unverifiable and contradicted as current by local-only evidence; 0 installs, no
network traffic, no writes outside this report.
