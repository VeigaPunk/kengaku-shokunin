# R50C2ExecVerifyTargets — C2 corrections block, per-row target verification

REV c3372a9b24d3a200946a6b37dc0a31ed5c982cc1 (lane `master`; measured on a `git clone --shared` of the lane at that revision; live `master`/`HEAD` also `c3372a9b…`).
Freeze `3b02d573d58cc6d2e0d27ef92ac0815354912252`: `git merge-base --is-ancestor … HEAD` → exit 0 (`FREEZE_IS_ANCESTOR=yes`). Base `71f5f5f77591d8c3d19297ee9785436da45209e4` also an ancestor (`ancestor=yes`).
Claim served: R50-C2 (calibration). This seat verifies the 12 rows of the `## Round 50 — C2 corrections` block at SCORECARD.md:2136-2166; it claims no admission and writes nothing else.

## Axes named

- **A1 target-exists** — every `SUPERSEDED <pointer> -> <target>` target is present in the tip tree (`git cat-file -e HEAD:<target>`), blob-equal to the worktree file.
- **A2 target-identity** — the target is the artifact the row (and its one-line reason) meant: opened, one line quoted.
- **A3 never-landed-exact** — for every `-> never-landed` row, `git log --all --oneline -- <pointer>` is empty, in the audit's own ref scope (clone) **and** in the superset scope (live repo, all refs incl. `refs/jj/keep/*` and `refs/remotes/origin/cursor/*`), plus `git rev-list --all --objects` shows no such path in reachable history.
- **A4 never-landed-near-miss** — no similarly named file exists at the tip (`git ls-files | grep -F <basename>`), i.e. the `never-landed` verdict is not hiding an available target.
- **A5 block-integrity** — the block is append-only text at the tip, 12 rows, one row per pointer, no duplicate pointer (the audit's `superseded_map` is a dict, so a duplicate would silently shadow).

## Commands run (verbatim; run in the clone unless prefixed `L=`)

```
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
git -C lane rev-parse HEAD                       # c3372a9b24d3a200946a6b37dc0a31ed5c982cc1
git -C lane merge-base --is-ancestor 3b02d573… HEAD ; echo $?    # 0
git -C lane merge-base --is-ancestor 71f5f5f7… HEAD ; echo $?    # 0
git -C lane cat-file -e HEAD:<target>            # per target row
git -C lane rev-parse HEAD:<target> ; git -C lane hash-object -- <target>
git -C lane cat-file -s HEAD:<target> ; sha256sum <target>
git -C lane log -1 --format='last-commit=%h %ad %s' --date=short -- <target>
git -C lane log --all --oneline -- <pointer> | wc -l              # per never-landed row  → 0
git -C $L log --all --oneline -- <pointer> | wc -l                # $L = live lane, all refs → 0
git -C $L rev-list --all --objects | grep -E ' (…|analyze\.py|repo-git-state\.md|round34_….py|round4[89]_….py)$'   # rc=1, no match
git -C lane ls-files | grep -F <basename>        # per never-landed row
git -C lane ls-files | grep -cF <basename>       # counts below
grep -n '^SUPERSEDED' SCORECARD.md ; grep '^SUPERSEDED' SCORECARD.md | awk '{print $2}' | sort | uniq -d   # 12 rows, no dup
```

Block at the tip (SCORECARD.md:2145-2156, all 12 rows, no duplicates, no earlier rewrite — the block header is at :2136 and nothing above :2136 carries a `SUPERSEDED` row):

```
2145:SUPERSEDED corpus/defects.json -> corpus/defects.jsonl
2146:SUPERSEDED corpus/evidence/analyze.py -> never-landed
2147:SUPERSEDED corpus/evidence/round9-replication/predictions-r9.sh -> corpus/evidence/round9-replication/predictions-r9.md
2148:SUPERSEDED corpus/knowledge/repo-git-state.md -> never-landed
2149:SUPERSEDED corpus/routed-findings.json -> corpus/routed-findings.jsonl
2150:SUPERSEDED plans/round34_c1_verify.py -> never-landed
2151:SUPERSEDED plans/round34_defects.py -> never-landed
2152:SUPERSEDED plans/round34_mutate.py -> never-landed
2153:SUPERSEDED plans/round48_c1_verify.py -> never-landed
2154:SUPERSEDED plans/round48_c2_verify.py -> never-landed
2155:SUPERSEDED plans/round49_c1_verify.py -> never-landed
2156:SUPERSEDED plans/round49_c2_verify.py -> never-landed
```

Pointer presence at `HEAD` (the 12 pointers themselves) — all absent at tip:

```
absent  corpus/defects.json          absent  plans/round34_c1_verify.py
absent  corpus/evidence/analyze.py   absent  plans/round34_defects.py
absent  …/predictions-r9.sh          absent  plans/round34_mutate.py
absent  corpus/knowledge/repo-git-state.md   absent  plans/round48_c1_verify.py
absent  corpus/routed-findings.json  absent  plans/round48_c2_verify.py
                                     absent  plans/round49_c1_verify.py
                                     absent  plans/round49_c2_verify.py
```

## Per-row verification

Strict verdict = A1+A2 (target rows) or A3+A4 (never-landed rows), exactly as this seat's item states. `frozen` = the claims' own rule (`§C2` kill rule + the audit's predicate: target exists, or `log --all` empty) — reported separately so the L1 can see that no row is a frozen-rule breach.

| # | row | A1/A3 | evidence | A2/A4 | strict | frozen |
|---|---|---|---|---|---|---|
| 1 | `corpus/defects.json -> corpus/defects.jsonl` | target at tip | `HEAD:` blob `ad3c3f89de7005697d77eaa651666e1708481ba7`, worktree identical, 1163 B, sha256 `4fe3790af27bbd755c207ad467f0a57889efc6ba844764f5b9db67871306154c`, 5 rows | ledger identity: line 1 = `{"id": "R34-D1", "class": "uncommitted-round-work", "opened_round": 34, "source": "corpus/lessons/round-34-verifier-spotcheck.md:75", "check": "r34_d1", "status": "closed", "closed_round": 35, …}`; SCORECARD:563 runs `python3 plans/defect_ledger.py --lane .` **over `corpus/defects.jsonl`** | **PASS** | PASS |
| 2 | `corpus/evidence/analyze.py -> never-landed` | `log --all` = 0 (clone and live) | no such path in `rev-list --all --objects` | **same basename exists at tip**: `corpus/evidence/round9-fleet/analyze.py` (11 tracked `analyze.py` paths). The row's own cited source, SCORECARD:113, says: *"the analyzer on disk is `corpus/evidence/round9-fleet/analyze.py`"*; the row's reason instead names `corpus/evidence/round9-fleet/probeA.py` (also at tip) | **FAIL** | PASS |
| 3 | `…/predictions-r9.sh -> …/predictions-r9.md` | target at tip | 1029 B, sha256 `2a4f62ef20a65e7a7cb3b7414b54d0f995126209c3126ae674b7cc3af2bc1099` — byte-identical to the digest line in `predictions-r9.sha256.repo` (`2a4f62ef…  predictions-r9.md`) | line 1 = `# Round 9 preregistered predictions`; the file holds the preregistered point predictions the `.sh` pointer named. Note: the row's reason names the *guard* `predictions-r9.sha256.repo`, the target is the *guarded* `.md`; both exist and agree | **PASS** | PASS |
| 4 | `corpus/knowledge/repo-git-state.md -> never-landed` | `log --all` = 0 (both scopes) | no such path in any reachable object | basename census = **0** at tip; PROVINCE:415-416 confirms the citation is **Kasegi's** sibling entry (`PROVINCE.md:416: corpus/knowledge/repo-git-state.md is cited as the sibling precedent…`) | **PASS** | PASS |
| 5 | `corpus/routed-findings.json -> corpus/routed-findings.jsonl` | target at tip | `HEAD:` blob `2e819d7aa175137a43129edba932c3f853a51574`, worktree identical, 48957 B, sha256 `39fdef1e3fe06c6b75e63d363bd4420c87a830546e0fb1f4571e56b2a3d1cd7d`, 71 rows | line 1 = `{"id": "R39-R1", "class": "registry-missing-gate-rows", "source": "corpus/lessons/round-39-verifier-spotcheck.md:132", …  "check": "grep -q '^| \`order-check\`' SKILL.md …", "note": null}`; SCORECARD:1572 cites ``corpus/routed-findings.jsonl`` (10 rows…) as the routed ledger | **PASS** | PASS |
| 6 | `plans/round34_c1_verify.py -> never-landed` | `log --all` = 0 (both scopes) | no `plans/…` path in history | **same basename at tip**: `.ufo/waves/round-34/drafts/round34_c1_verify.py`, `.ufo/waves/round-34/final/round34_c1_verify.py` (+7 build/mutant copies; 9 tracked). SCORECARD:1168 itself records "before: entry/counter absent at freeze" | **FAIL** | PASS |
| 7 | `plans/round34_defects.py -> never-landed` | `log --all` = 0 (both scopes) | none | **same basename at tip**: `.ufo/waves/round-34/{drafts,final}/round34_defects.py` (+2 build copies; 4 tracked) | **FAIL** | PASS |
| 8 | `plans/round34_mutate.py -> never-landed` | `log --all` = 0 (both scopes) | none | **same basename at tip**: `.ufo/waves/round-34/{drafts,final}/round34_mutate.py` (+2 build copies; 4 tracked) | **FAIL** | PASS |
| 9 | `plans/round48_c1_verify.py -> never-landed` | `log --all` = 0 (both scopes) | none | basename census = **0**. Nearest stem match is `.ufo/waves/round-48/w1/R48C1ExecControls/fences/round48_c1_verify.v2.py` — a *fence*, not the counter, so not a target the row could re-point at | **PASS** | PASS |
| 10 | `plans/round48_c2_verify.py -> never-landed` | `log --all` = 0 (both scopes) | none | basename census = **0**; no stem match at all | **PASS** | PASS |
| 11 | `plans/round49_c1_verify.py -> never-landed` | `log --all` = 0 (both scopes) | none | basename census = **0**; no stem match | **PASS** | PASS |
| 12 | `plans/round49_c2_verify.py -> never-landed` | `log --all` = 0 (both scopes) | none | **same basename at tip**: `.ufo/waves/round-49/w1/R49C2ExecControls/receipts/instruments/round49_c2_verify.py`, docstring line 2-3 = *"Round-49 C2 counter candidate (coverage): the round-46 TB2 `polyglot-c-py` package under a Q40 re-frozen counter."* (1 tracked) | **FAIL** | PASS |

Strict totals: **7 PASS / 5 FAIL**. Frozen-rule totals: **12/12 PASS** (3 targets exist, 9 pointers have empty `--all` history).

## Findings beyond the row table

1. **Rows 1 and 5 correct a token the audit's own regex invents, not a token a row wrote.** `plans/round50_c2_audit.py` (sha256 at tip `b911d03a08e396e5efdfaa434841300ccb5a452965c9d21c0c5fa56ea5dcaaef`) matches `EXTS` in the order `md|py|json|jsonl|…` with a lazy path group and no trailing boundary, so the text ``corpus/defects.jsonl`` yields the token `corpus/defects.json`. Reproduced against the tip pattern:
   ```
   '`corpus/defects.jsonl`'         -> ['corpus/defects.json']
   '`corpus/routed-findings.jsonl`' -> ['corpus/routed-findings.json']
   '`corpus/evidence/analyze.py`'   -> ['corpus/evidence/analyze.py']
   '`plans/round34_c1_verify.py`'   -> ['plans/round34_c1_verify.py']
   ```
   At the base revision the bare token never appears in the text — every occurrence is the prefix of a `.jsonl` occurrence:
   ```
   git show 71f5f5f…:SCORECARD.md | grep -oF -e 'corpus/defects.json' -e 'corpus/routed-findings.json' | sort | uniq -c
         3 corpus/defects.json
         7 corpus/routed-findings.json
   git show 71f5f5f…:SCORECARD.md | grep -oE 'corpus/(defects|routed-findings)\.json.' | sort | uniq -c
         3 corpus/defects.jsonl
         7 corpus/routed-findings.jsonl
   (SHONEN.md, PROVINCE.md: zero occurrences of either)
   ```
   Consequence: two of the five corpus rows are `.json`-from-`.jsonl` phantoms. Their targets are still the right artifacts (the ledgers the SCORECARD rows cite), so the rows do no harm; but the honest fix is the token regex (`jsonl` before `json`, or a trailing `(?![A-Za-z0-9])`), not an append-only correction per phantom. This is an instrument defect open under the C2 instrument, not a row defect.
2. **Row 2 is the one row whose reason contradicts its own cited source.** SCORECARD:113 says the analyzer on disk is `corpus/evidence/round9-fleet/analyze.py`; the row's reason names `probeA.py`. The exact pointer never landed (true), but a same-named analyzer exists at the tip at the path the cited source names, so `-> never-landed` is the less informative of the two legal corrections.
3. **Rows 6, 7, 8, 12: `never-landed` is true only for the `plans/` location.** Same-named instruments are committed under the wave trees (`.ufo/waves/round-34/{drafts,final}`, `.ufo/waves/round-49/w1/R49C2ExecControls/receipts/instruments/`). Under the frozen rule this is legal; a reader of "never-landed" is nonetheless one directory away from a file of that name. If the L1 wants the strict A4 property to hold, those rows should point at the committed drafts/receipt instrument or the block should say `never-landed (plans/ only)`.
4. **The frozen claims prose enumerates 11 of the 12 rows.** `plans/round-50-claims.md` §C2 says "six pointers … (`plans/round48_c1_verify.py`, … `plans/round34_mutate.py`, and four corpus paths)" — 7 plan names plus "four corpus paths" = 11 names, and "six" matches neither. Measured block: 7 plan rows + 5 corpus rows = 12, which is the measured `unresolved=12`. The block is the complete set; the prose enumeration is short by one corpus path (and the "six" is wrong). Cosmetic for the predicate, but the C2 claim's own before-text is the calibration surface.
5. **No row is a frozen-rule breach**: no target is missing, no `never-landed` row names a path that is in history (checked at exact path against all refs and against all reachable objects).

## Limits

- `git log --all` is ref-scoped. I checked both the audit's scope (clone: 3 branch heads + `origin/HEAD`) and the superset (live repo, 1013 refs: 3 heads, 999 `refs/jj/keep/*`, 11 `refs/remotes/origin/*` incl. `cursor/*` and `devin/wiki-link`). An object reachable only from a reflog entry or a dangling commit is **not observed**; the frozen rule does not ask for it. `git rev-list --all --objects` over the same refs also found no exact path.
- A4 is a basename-substring census over `git ls-files` at the tip, not a semantic rename analysis: a same-content artifact under a wholly different basename would not be detected (e.g. `probeA.py` for row 2 was found only by reading the row's reason).
- A2 is a one-line quote plus the row's reason sentence; it establishes that the target *is* the artifact class the row names, not that every claim in the citing row re-runs. `plans/round50_c2_audit.py` itself was read for its resolution rule but deliberately **not executed** — running the counter is the audit seat's item, and this seat's item is per-row target verification only.
- The tip is a moving target: a later commit that adds `plans/round34_*.py` or `plans/round49_c2_verify.py` would flip rows 6-8/12 to a frozen-rule breach; the REV line above is the revision this receipt is valid for.
- No LSP query was needed (verification is git-tree + file content); no LSP server was consulted, so no LSP result enters this evidence. No tool install or upgrade was performed.

## Evidence retention

Every command, digest and quoted line in this file was produced in this seat's clone at `REV c3372a9b…` (live `master` = same). Raw outputs were not spilled to `/tmp`; the verbatim blocks above are the receipt.

## Scratch

Scratch root `/fast/scratch/hyaku/kengaku-r50/R50C2ExecVerifyTargets` (with `TMPDIR` exported to it) held the one `git clone --shared` and was removed with `rm -rf -- "$S"` after this report was written; a post-removal `ls` of `/fast/scratch/hyaku/kengaku-r50/` shows no `R50C2ExecVerifyTargets` entry. No scratch tree is left on disk.

VERDICT: **C2 corrections block VERIFIED at REV c3372a9b — 12/12 rows PASS the frozen rule (3 targets exist at the tip and are the artifacts the rows meant; 9 never-landed pointers have empty `git log --all` history at the exact path against every ref), so the block cannot manufacture a false resolution by pointing at a missing target or at a path that is in history. Under this seat's stricter A4 criterion 5 of the 12 rows FAIL (rows 2, 6, 7, 8, 12): a same-basename file exists at the tip, and row 2's `never-landed` reason contradicts the SCORECARD line it cites. One instrument defect open (audit `EXTS` regex derives `.json` tokens from `.jsonl` text, which is why rows 1 and 5 exist), and the claims prose enumerates 11 of the 12 rows. No C2 admission is claimed here.**
