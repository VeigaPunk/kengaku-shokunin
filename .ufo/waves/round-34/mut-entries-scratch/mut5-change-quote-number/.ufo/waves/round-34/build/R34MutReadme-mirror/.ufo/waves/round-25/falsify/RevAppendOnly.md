ATTACKS: append-only discipline, 6180e4f..8ea41f9ed on LOG.md, corpus/lessons, corpus/QUALITY.md, corpus/SOURCES.md, corpus/knowledge (+ per-commit history, live working tree)

Contract used: CORPUS.md:116-118 (SOURCES rule 2: only status/recheck/used-by change in place, logged old→new; a correction is a new row whose teaches opens `supersedes S0NN —`); PROTOCOL.md:123-125, :366, :463 (LOG append-only; a superseded claim gets an appended correction that points at the old text); CORPUS.md:53; QUALITY.md:5-6, :94 (R1), :98 (R5).

## Landed range: every deleted or rewritten line
1. One line rewritten: corpus/SOURCES.md:33 (S011). In `git diff -U0 6180e4f 8ea41f9ed -- <paths> | grep '^@@'`, `@@ -33 +33 @@` is the only hunk with a nonzero old-count. Numstat for the scoped paths is +278 −1. Splitting the row on `|` shows that only cell 12 changed, which is used-by: `corpus/knowledge/llm-judge-calibration.md` → `…, corpus/knowledge/attribution-interval-calibration.md`. **ALLOWED** under rule 2. The old and new values are logged byte-exact at corpus/lessons/round-25.md:36-38.
2. Deleted lines: 0. Per-commit numstat: 3f371d2 +110/−0 and 710409f +41/−0, both on plans/round-25-claims.md; Amendment 1 sits at EOF (`@@ -110,0 +111,41 @@`). 8ea41f9: the only scoped deletion is S011. 4e57f14 touches only considerthese/2026-10-20.md. `merge-base --is-ancestor 6180e4f 8ea41f9ed` exits 0, so no history was rewritten and no rewrite is hidden by an intermediate commit that a later one undoes.
3. Every other hunk is `-N,0`, a pure insertion. Positions:
   - EOF: LOG.md (after :274), both knowledge files, both lessons (after 97/49/180/141 = base lengths), and QUALITY R11–R13.
   - End of section: QUALITY Q11 after :81; SOURCES S027–S037 after :48 (end of registry); SOURCES search log after :65.
4. Independent guard: kama-shokunin/tools/sources-append-only.py, copied to /tmp (sha256 4d786856…). `--selftest` passes 42/42. With `--repo <lane> --from 6180e4f --to 8ea41f9ed` it prints `added S027…S037 (allowed)` and `no append-only violations`, exit 0. Mutation test: editing S011's anchor cell in a /tmp repo gives `[('S011','cell-changed')]`, exit 1, so the guard can fail on this file.
5. S036 teaches opens `supersedes S025 —` (SOURCES.md:58). S025's cells are absent from the diff, so they are unchanged. This matches the rule-2 correction form.

## Breaks and gaps
H1 [HIGH; live tree, uncommitted; breaks append-only if it lands as-is]. File mtimes are 21:49–21:50 −03, after the 8ea41f9 commit at 21:44:48. Committed lines have been rewritten in place:
   - LOG.md:286: `diff -U0 <tip> LOG.md` → `@@ -286 +286 @@`. `mismatch=11 (exit 1)` becomes `mismatch=10 (exit 1; v2 receipt — v1 counted 11 …)`. This violates PROTOCOL.md:463 and :124.
   - corpus/lessons/round-25.md:16-17 (`@@ -16,2 +16,2 @@`): M25 goes `mismatch=11` → `10` and its receipt path → `-v2`; M26 goes `5 PROVINCE rows` → `4 PROVINCE path rows …`. This violates QUALITY.md:94 R1 ("the old line stays byte-identical").
   - R1's own check fails on the live tree: `grep -c 'mismatch=11'` gives LOG.md 0 and round-25.md 0; at the tip LOG.md gives 1.
   - Smallest fix: restore the 8ea41f9 bytes. Then append dated corrections that name LOG.md:286 and round-25.md M25/M26 and give the v2 recompute command.
   - Same edit pass, outside the append-only list:
     - SCORECARD.md :559 and :668 (11→10), plus :660-662 and :672-673, rewritten in place. Only the 11→10 count is in tension with R1.
     - Receipts overwritten in place: round25-calibration/state-check-after.txt:1 and attrib-calibration-selftest.txt:3. By contrast, the `before` receipt got a new `-v2` file.
     - Landed seat report .ufo/waves/round-25/build/StateCheckExec.md rewritten (6 lines removed, 6 added).
   - Live SOURCES.md and round25-sources/gate.md contain additions only (guard tip→live: added S038, exit 0).

M1 [MEDIUM; landed]. The round re-verdicts r22 `TARGET hyper 10/10 -> PASS` as INDETERMINATE (LOG.md:283, lesson M24), but the places that state that verdict carry no appended correction:
   - corpus/knowledge/attrib-r21.md:463 ("correct 10/10 = 1.000 (bar 0.80) — PASS") and :479 ("hyper is now validated on forced serves"). The file is not in the range, and `grep -nEi 'errat|correct|supersed'` on its headers finds nothing. QUALITY.md:98 R5 says the old sentence "is not left as current".
   - LOG.md:188-189 ("run-2 10/10 = 1.000 PASS") and :215-216 ("-> FAIL … it failed"). The r25 entry names the receipt tokens, not this superseded LOG text (PROTOCOL.md:124).
   - SCORECARD.md:541 ("hyper validated"): cited by M24, but no R25-E erratum covers it (R25-E1..E5 are at :646-650). Still none in the live tree.
   - Caveat: this is a re-verdict under the new rule Q11, not refuted arithmetic, and r23 hyper 24/24 does PASS. The r23 STREAM verdict did get its erratum (round23-stream-surface.md:182-187).

L1 [LOW]. SOURCES Leads: the Clopper–Pearson lead was inserted after base :67 (the heading and blank line), so at the tip it sits at :82, ahead of the three existing leads (:83-85). That is a prepend, not an append. No line changed, and the contract does not address order.

L2 [LOW]. QUALITY.md:92 still says "Each row cites the mistake it closes in `corpus/lessons/round-24.md`". The appended R11–R13 (:104-106) cite round-25.md, so the untouched preamble is now false and has no note.

L3 [LOW; already flagged at ClosureCriteriaScout.md:23]. R1's check breaks when a correction quotes the old value:
   - `grep -c 'extremes n=2 and n=9'` on llm-judge-calibration.md → 2 (:72 plus the r25 correction at :104).
   - `grep -c 'Q1–Q8 pass'` on round-24.md → 6.
   - R1 was not superseded this round.

L4 [LOW]. Line shifts: Q11 moves the R rows down by 8 (R1 :86 → :94). Lane-committed files contain one line-number cite into the shifted files, plans/attrib_calibration.py:37 → SOURCES.md:33, and that line did not move (`git grep -nE '(QUALITY|SOURCES)\.md:[0-9]+'`, excluding wave reports). Wave-1 receipts cite base numbers (ConnChousa.md: QUALITY.md:86,90); those are dated, and they are now stale.

Residual risk / gaps:
- H1 describes the live tree around 21:50 −03, while the integrator was still editing; the state may change before the next commit.
- S011's anchor still reads "Abstract", but its new user cites §4.1–§5.2. Leaving the anchor alone is correct under rule 2 (anchor is immutable); the append-only way to cover those sections would be a new row.
- Not checked: the fleet-repo deletions of the misrooted seat copies (M29).

VERDICT: PARTIAL — the landed 6180e4f..8ea41f9ed SURVIVES: one rewritten line (S011 used-by, allowed and logged), 0 deletions, guard exit 0, mutation caught. It BREAKS in the live uncommitted tree (LOG.md:286 and round-25.md:16-17 rewritten in place), and the hyper re-verdict has no appended correction at attrib-r21.md:463/479, LOG.md:188-189 or SCORECARD.md:541.
Installs: none. Used kama-shokunin/tools/sources-append-only.py read-only via a /tmp copy, plus python3, git, diff and awk.
