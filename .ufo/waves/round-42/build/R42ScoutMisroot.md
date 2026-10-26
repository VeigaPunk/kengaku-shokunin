# R42ScoutMisroot — host-safety / hygiene watch (kengaku r42 wave 1)

Read-only watch. Window: 17:27:12 -03 (start) to 17:27:43 -03 (end), 2026-10-26. No envelope needed (no fixture/battery run).

## 1. ~/.local/bin
- Start: `stat -c %y /home/vgpnk/.local/bin` -> `2026-10-26 14:05:53.386453172 -0300`; `ls -A ... | sha256sum` -> `436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18`; 103 entries (`ls -la`).
- End: mtime `2026-10-26 14:05:53.386453172 -0300` (identical); sha256 `436b361f...fc18` (identical).
- The dir was last modified 14:05:53, about 3 h before this watch and before sentinel creation (16:56:19). No shim/entry added or removed during the round-42 window. Newest entries: `openbot` symlink 10:50:01, `ruff` 09:46:22 (all earlier than 14:05).
- Full `ls -la --time-style=full-iso` captured at start (output elided by the tool in the middle; head/tail consistent with the above).

## 2. Fleet root git status
- `git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all` -> 0 lines at start and at end (toplevel confirmed `/home/vgpnk/Projects/shokunin`).
- `kengaku-shokunin/` is gitignored at the fleet root (`.gitignore:1:*-shokunin/`), so status cannot see lane writes by design; no kengaku r42 seat file is tracked/untracked in the fleet root.
- Files in the fleet root newer than 16:00: `MANIFEST.json` (17:06:10) and `.ufo/` contents — all committed (HEAD d1e70ce6 17:07:10 "hyaku run9: kaidoku r40 closed ... r41 dispatched", authors protocol-shokunin / lane commits). `.ufo/prompts/kengaku-round-42.md` is the orchestrator's dispatch prompt (commit a6b14ada 16:54:01), not a seat write. No seat write found.

## 3. Scratch /fast/scratch/hyaku/kengaku-r42
- Sentinel: `/fast/scratch/hyaku/kengaku-r42/.ROUND-ROOT-SENTINEL` PRESENT at start and at end, 71 bytes, mtime 16:56:19.866883848, content "kengaku r42 round root; L1 KengakuR42; seats delete only $S/<SeatName>".
- Total at end: 11G, 22 entries (21 seat dirs + my own pass).
- Per-dir sizes (start, `du -sh`):
  R42MutProbe 0, R42QualityDraft 0, R42R5Carried 0, R42CritProbe 368K, R42CritIndep 576K, R42SentinelCounter 1020K,
  R42BatAncRoute 531M, R42MutC2Counter 531M, R42RegistryRows 531M, R42RevC2Counter 531M, R42RoutedRider 531M, R42SentinelProbe 531M,
  R42CritC1Counter 532M, R42PkgEntry 532M, R42CritAttribution 538M, R42CritPytest 542M, L1 724M, R42CritEquiv 1.1G, R42ScoutPriorArt 1.2G, R42CritClaims 1.6G.
  (Each ~531M dir ~= a lane clone.) All inside the round root; none outside.
- Self-note: I briefly created `/fast/scratch/hyaku/kengaku-r42/R42ScoutMisroot.status` (0 bytes, 17:27:20) as a stray file in the round root while triaging; I removed it myself (`rm -f` of that single path) — no other file touched. This was a hygiene slip by this seat; the file is gone (end listing shows only seat dirs + sentinel).

## 4. /tmp
No kengaku-r42 seat wrote to /tmp in the sense that violates the rule, with these observations (files created since 16:56, the sentinel time; content/owner attribution by `head`/`ls`):
- `/tmp/k42-fsp-u1m8gvc_/fsp-dmbc8c00/{app,recipe.sh,harness.py}` — name prefix `k42-fsp` = kengaku-42 fibsqrt probe harness. Dir mtime 17:27:35; at the next stat the `fsp-dmbc8c00` subdir and then the whole `k42-fsp-*` were gone (ephemeral mktemp, cleaned by its owner). Small; ATTRIBUTED to a kengaku r42 probe run (inference from the name). Not under scratch -> technically a /tmp use, <50 MB, self-cleaned.
- `/tmp/tmpxh5mdqcv/{correct,WRONG,absent}/*.bin` (17:21) and `/tmp/tmpdxjf9cu9/{cache,lane_evidence_oracle.tsv}` (17:22): Python tempfile dirs; content (`lane_evidence_oracle.tsv`, 'selftest ... /fast/scratch/hyaku/kasegi-r39/...' in /tmp/bp.txt) points at the kasegi round-39 lane, not kengaku r42.
- `/tmp/kd-*` (17:01-17:06), `/tmp/del.*`, `/tmp/tip.*`, `/tmp/x.sc.cpp`, `/tmp/unarmed.out`, `/tmp/probe.err`, `/tmp/T49Read03-*`, `/tmp/t49r5`, `/tmp/r1`, `/tmp/r2`, `/tmp/sa|sb|sbase`: `grep -l -E 'kengaku-r42|kengaku r42|round-42|round 42|R42'` over the kd-*/r1/r2/bp/readme-noappend/base-skill/T49Read03-* files -> no hits. `kd-*` content = kaidoku r40/unblob/FRITZ research; T49 = tameshi r49; `bp.txt` = kasegi. Not kengaku r42.
- Total content of /tmp files naming kengaku/round 42: none found beyond the k42-fsp harness above.
- /tmp contains 427 entries host-wide (other lanes); not enumerated further.

## Findings
- misroot: 0 (sentinel intact, no seat deleted/wrote the round root; only my own removed stray file).
- host writes (~/.local/bin or fleet-root tracked files by a r42 seat): 0.
- Minor hygiene: (a) one self-cleaned /tmp/k42-fsp-* harness (name-attributed to kengaku r42, small); (b) round root at 11G across 21 dirs — about 14 of them hold ~531M lane clones that seats should delete at exit (their `trap rm -rf "$S"`).

Commands used: `ls -la --time-style=full-iso /home/vgpnk/.local/bin`, `stat -c %y`, `ls -A ... | sha256sum`, `git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all`, `git check-ignore -v`, `du -sh /fast/scratch/hyaku/kengaku-r42/*`, `find /tmp -maxdepth 1 -newermt '2026-10-26 16:56'`.

VERDICT: misroot-0-host-writes-0-sentinel-present
