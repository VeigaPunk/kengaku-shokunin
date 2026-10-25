# ReadmeIndexScout — P2e: corpus/README.md index ↔ tree parity

Base `6180e4fb92e9`. README from that commit: sha256 `3f9f2bd0…021e70`, byte-identical to worktree `corpus/README.md`;
`git diff --stat 6180e4fb92e9..HEAD -- corpus/{README.md,knowledge,lessons,evidence}` empty (HEAD `3f371d2` differs only under `plans/`).

## Commands (offline; no endpoint traffic)
1. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 6180e4fb92e9:corpus/README.md > /tmp/kengaku-r25-readme/README.base.md`
2. `grep -oP '(?:corpus/)?(?:knowledge|lessons|evidence)/[A-Za-z0-9._*?/\[\]{},\-]+' README.base.md | sed 's/[.,;:)]$//' | sort -u | wc -l` → **92**
3. `python3 /tmp/kengaku-r25-readme/index_census2.py` — row/token map, globs+braces expanded over `git ls-tree -r 6180e4fb92e9 corpus/`
4. `os.path.exists`/`glob.glob` per token under `…/kengaku-shokunin/corpus` → `tokens=92 unresolved=0`
5. `find corpus/{knowledge,lessons,evidence} -maxdepth 1 …` → knowledge 32 files, lessons 26 files, evidence 28 files + 14 dirs = 42

## Counts
- 118 table rows = **71 naming a `knowledge/|lessons/|evidence/` path** (92 token instances, 87 distinct) + 28 bare-basename-only + 19 neither.
- 92 distinct tokens (87 in rows, 5 prose-only); 12 lane-root `corpus/…`, 80 corpus-relative. Unresolved: **0/92**, no dangling row.
- Reverse: knowledge 32/32 rowed; lessons 25/26 rowed; evidence 42/42 rowed.

## The 71 index rows naming a prefixed path
- 29–46 knowledge: one `knowledge/<file>` each (18 rows).
- 47–52 knowledge + `corpus/evidence/…`: round8-horizon/, round9-replication/, round9-fleet/prior-art.md, round11-power/, round12-ladder/, round18-kimi-routing/README.md.
- 53 `knowledge/probe-battery-r19.md` + `evidence/probe-r19-*.log`; 54 `knowledge/attrib-prior-art-r21.md` + `knowledge/probe-battery-r19.md`;
  55 `knowledge/attrib-r21.md` + `evidence/attrib-r21-*.log`; 56–60 one `knowledge/<file>` each (5).
- 61–68 lessons one each (8); 69–71 lessons + `corpus/evidence/round8-horizon/`, `round9-{replication,fleet}/`, `round11-{power,fleet}/`.
- 72–73 one each (2); 74 + `corpus/evidence/round12-{ladder,fleet}/`; 75–76 + `round13-ack-state/`, `round14-fleet/`; 77–78 one each (2);
  79 `lessons/round-13-coverage.md` + `evidence/round13-coverage/`.
- 85–89 one `lessons/2026-10-16-*` + an `evidence/attrib-r2{1,2,3}-*`/`probe-r19-*` glob each; 90 `lessons/round-24.md`.
- 106–117 twelve `evidence/<round-dir>/` rows; 157–158 `evidence/round24-sources/`, `evidence/round24-census/`.

## Resolution detail (all OK)
`probe-r19-*.log`→19, `attrib-r21-*.log`→4, `attrib-r22-*.log`→3, `attrib-r23-stream*.log`→2; braces `round9/11/12` → 6 dirs exist;
`probe-r19-{P2-servicetier,P3,P8-kimi-code-auth,P9-absent-port}.log` → 4/4. Nested tokens verified: `round9-fleet/prior-art.md`,
`round18-kimi-routing/README.md`, `round13-coverage/{coverage_census.py,surface-receipt.json}`, `round14-fleet/r14-review-priorart.md` — all present.

## Bare-basename rows (28, lines 124–151)
19 `probe-r19-*.log` + 4 `attrib-r21-*.log` + 3 `attrib-r22-*.log` + 2 `attrib-r23-stream*.log`. No `evidence/` prefix;
they resolve only via the `### evidence/` "Root-level receipt logs" header. Each is also matched by a prefixed glob row
(53/55/85/87/88/89), so no artifact depends on the bare form — convention weakness, not a broken link.

## Mismatches
1. **`corpus/lessons/round-24-verifier-spotcheck.md` has no index row** — present at base and in worktree, added by `a42bb40`
   ("round-24 verifier spot-check (integrator, kaika)"). `grep -n 'verifier-spotcheck' corpus/README.md` → rc=1;
   `git grep -n 'round-24-verifier-spotcheck' 6180e4fb92e9` → no hits (no inbound mention anywhere in the base tree).
   Integrator-authored (its header says "the lane owns `round-24.md`"), which explains but does not cure the missing row.
No other mismatch. Orphan count invariant across all three readings of "index row" (prefixed-only, prefixed+bare, any mention): 0/0/1.

## Calibration notes (rejected findings)
- First shell cross-check used `grep -oE` with a bracket class missing `-`, truncating every token at its first hyphen
  (37 tokens, all "unresolved"). Rejected: a truncating tokenizer yields 100% false-positive mismatch, and the tell was
  that *every* token failed. Corrected `grep -oP` reproduced the Python census exactly (92 tokens, 0 unresolved).
- Top-level-only set comparison flagged `round9-fleet/prior-art.md` and `round18-kimi-routing/README.md` as "dangling".
  Rejected: both are nested files that exist (`test -e` OK); the flag was an artifact of a maxdepth-1 comparison set.
- No external source opened (`Frontier`: no SOURCES rows earned). No installs.

VERDICT: 71 index rows / 92 tokens all resolve (0 dangling); exactly one unindexed artifact —
`corpus/lessons/round-24-verifier-spotcheck.md` — index parity 85/86 top-level artifacts, sole mismatch class = one missing `lessons/` row.
