# Round 9 aggregator corpus verdict — kengaku-shokunin

> **Path convention.** Bare `CORPUS.md`, `PROTOCOL.md`, `MANIFEST.json`, `SCORECARD.md`, `LOG.md`, `.ufo/…` and `<lane>-shokunin/…` pointers in this file are **main-repo (`shokunin`) relative** — they do not resolve inside this checkout. Paths inside this checkout are written `corpus/…`, `SKILL.md`, `SHONEN.md`, `PROVINCE.md`.

**Measured revision:** landed `kengaku-shokunin` `f09ff1f`; worktree had only untracked in-flight evidence directories, so verdict is for committed bytes. This lesson is an aggregator mirror draft; the aggregator-dispatched reviewer is still lane-authored, not non-author evidence.

## Verdict

**NOT CONFORMANT — literal CORPUS rule 8 and the round-9 rule-10 obligation fail.** Rule 8 has one literal `op://` hit at `corpus/lessons/round-5-aggregator-audit.md:56`, but it is only the quoted sweep pattern `grep -rn 'op://' ...`, classified schematic-placeholder rather than a real vault path: **FAIL-literal / PASS-intent**. The prior six-repo verdict was stale under round-8 §13.7; this lesson re-emits the kengaku rule-10 verdict.

## Rules 1–10 evidence

1. **PASS.** `git show f09ff1f:corpus/README.md | grep -c '^| \`knowledge/'` → 22; `git ls-tree -r --name-only f09ff1f -- corpus/knowledge | wc -l` → 22.
2. **PASS.** README lesson rows → 13; `git ls-tree -r --name-only f09ff1f -- corpus/lessons | wc -l` → 13; Python sweep found round and evidence markers in all 13 lesson blobs.
3. **PASS (observed practice).** Python sweep over 35 knowledge/lesson blobs found explicit opinion markers where needed; other entries carry source/evidence material and are re-derivable through the committed gate.
4. **PASS-after-correction.** `git show f09ff1f:corpus/knowledge/bench-arena-round7-noise-n25.md | sed -n '13p;23,24p'` shows the appended correction `0/12 → 0/17`; the falsified survivor is gone from the landed blob.
5. **PASS.** Negative-claim sweep `git grep -n -E '0 hits|none found|absent|no source|NO' f09ff1f -- corpus/knowledge corpus/lessons` found surrounding search/sweep commands; no unswept negative was identified.
6. **PASS.** Location sweep `git grep -n -E 'frontmatter|body|header|script|installed skill|:line|lines?' f09ff1f -- corpus/knowledge corpus/lessons` found location-qualified quote conventions; the prior sampled citation check passed.
7. **PASS.** Knowledge index/files 22/22 and lesson index/files 13/13, measured with the commands above.
8. **FAIL-literal / PASS-intent.** `git grep -n 'op://' f09ff1f -- corpus/` → one hit, the quoted sweep command at lesson line 56; no real vault path or secret value. `git grep -nE 'sk-|xox|bearer|password=|token=' f09ff1f -- corpus/` found no credential value. Literal rule text nevertheless bans `op://` references.
9. **PASS for landed corpus.** The round-6 lesson has an appended “Post-audit re-measurement” section (`git show f09ff1f:corpus/lessons/round-6-aggregator-audit.md | grep -n 'Post-audit re-measurement'` → present), and the previously missing README rows are present.
10. **FAIL at cutoff; re-emitted here.** Round-8 §13.7 explicitly recorded that per-repo rule-10 verdicts were not re-emitted and the §11.1 claims were stale. This lesson is the required re-emission at `f09ff1f`.

## Box 3 and gate

Round-8 box 3 was firm `[x]` at `0c51208`: committed cold-run evidence recorded `python3 grader.py --selftest` exit 0 with expected finding IDs and `python3 grader.py` exit 0, `CHECKS n=149 mismatches=0`, `VERDICT: PASS`. Re-executed at landed `f09ff1f`: `python3 grader.py --selftest` → exit 0, S0–S6 all pass with expected IDs; `python3 grader.py` → exit 0, `CHECKS n=280 mismatches=0 errata_pinned=1`, `VERDICT: PASS`; frozen archive run at `f09ff1f` reproduced the same. **Firm, not broken.**

Against PROTOCOL §Gate standard: verdict **satisfied** (0 clean, 1 mismatch/fail, 2 missing input; 2 should be explicitly labeled `could-not-evaluate`); self-test **satisfied** (isolated temp copies, exit and finding-id assertions); two evidences **satisfied** (committed pinned evidence plus frozen archive run); registry **partial** (`SKILL.md:405-449` has prose fields but lacks a schema row and explicit class mapping/write-scope/owner fields); scope **satisfied** (stdlib-only, no network/endpoint, temp copies only); revision naming **partial** (caller records `f09ff1f`, stdout does not).

## Movement and durability

Round-6 (`f147a27`) was **not conformant — 7,9,4; 5 majors / 12 defects**. Rule 7 is now 22/22 + 13/13; the rule-4 `0/12` survivor was corrected to `0/17`; rule 9's corpus lesson/index work is append-only; box 3 advanced to a firm expanded-gate pass. Residuals are literal rule 8, registry schema gaps, and rule-10 freshness.

The prior `shokunin:.ufo/reports/round-11/kengaku-DRAFT.md` (main repo `shokunin`, not a path in this checkout) was measured as untracked/non-contract, 15,922 bytes with 40 unfilled `{{…}}` tokens, while `round-11/kengaku.md` was absent (D-90, owner kengaku, severity 6). The current contract report exists, but the draft's former non-durability remains a contract defect to mirror, not evidence.
