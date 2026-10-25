ATTACKS: round-25 correction for kaika W3 M19 — corpus/lessons/round-24.md:154-157 (M19 narrowing) + corpus/lessons/2026-10-16-round23-stream-surface.md:182-187 (R5 erratum), base 6180e4f → tip 8ea41f9ed
Seat KengakuR25.CorrM19 (wave 2). Scratch /tmp/k25w2-CorrM19/{a=6180e4f,b=8ea41f9ed} (git archive); mutations only in /tmp/k25w2-CorrM19/m{A,B,C}. No lane write except this report.

## 1. Append-only — SURVIVES
- `git diff --stat 6180e4f 8ea41f9ed -- <both>` → round-24.md 16+/0−, stream-surface 7+/0−; plain `diff a b` → only `>` lines (`141a142,157`, `180a181,187`).
- `cmp -n <base size> base tip` → identical for both (22493 B / 12674 B): base is an exact byte-prefix. Only commit in range touching them: `8ea41f9`. Live tree `cmp` = tip (both files, QUALITY.md, the r23 log). M19 row (round-24.md:29) unchanged.

## 2. Facts vs evidence — SURVIVES (every value reproduces); two LOW precision slips
- "dated … 13:33Z write": note :9, :151. Corroborated: note's instrument pin bb6bd919… = `git show 8a08483:plans/attrib_probe.py | sha256sum` (r22 records, 13:31Z); trial instrument was cce53a16 (log :3).
- "said later receipts supersede it": note :22-23 ("Where the round's landed receipts disagree, they supersede this note"), :153-154.
- "committed (14:23:19Z) after the receipts existed": `3358c4d` 11:23:19-03:00 = 14:23:19Z; receipts `f9337d5` 14:22:45Z; log :194 block stamp 13:49:42Z, :258 13:51:16Z.
- Erratum values: log :233 `GT counts {"alibaba-token-plan": 6, "hyper": 24}`, :234 `ACCURACY: 30/30`, :239 `STREAM TARGET opencode-go: on-target GT n=0`; :341 "Block 2 is authoritative" (= :258-320).
- "Round 25 re-verdicts … UNTESTED": `python3 plans/attrib_calibration.py --root <tip copy> --summary` (exit 0) → `attrib-r23-stream.log 258-320 stream-target:opencode-go 0/0 … stored=FAIL interval=UNTESTED`.
- S1 (LOW): R5 wants "the receipt and line". The named :233-239 lies in block 194-256, which the cited instrument marks superseded: `--json` → `{"lines": "194-256", "role": "superseded", "stamp": "2026-10-16T13:49:42Z"}` vs `{"lines": "258-320", "role": "P1"}` (claims P1 = LAST block). The authoritative line is :303. Values are identical and `:258-320` is disclosed, so no number is wrong.
- S2 (LOW): "the landed receipt" drops its provenance: `f9337d5` subject "r23 WIP receipts: partial stream trials from the aborted dispatch (unverified)"; round-24.md "Round 23 disposition" keeps f9337d5 "as unverified history".

## 3. Closure — PARTIAL
- The named review file states no M19 finding: grep `M19|R5|round23-stream|artifact has landed|time-bounded` on .ufo/waves/kaika-w3/kengaku-review.md → 0 hits (it verified only `C2.lesson_mistake_rows absent→20`). The finding is kengaku-critic.md:11. Its fix, :13: "append a correction clarifying M19's time-bounded source and reevaluate R5 without erasing history". The "kaika W3 critic" attribution at round-24.md:154 is correct.
- Half 1 (time-bounded clarification, append-only): CLOSED by round-24.md:154-157. Dated, attributed, old row kept.
- Half 2 (reevaluate R5): NOT SHOWN. R5 is applied (erratum paid) but never re-evaluated: `git diff 6180e4f 8ea41f9ed -- corpus/QUALITY.md` adds Q11 and R11–R13 only; R5 (QUALITY.md:98) is unchanged and no text re-evaluates it.
  - R5's check is blind to the stale sentence. At base both legs exit 1 (the sentence wraps :9-10; "supersede" ≠ `superseded`), as wave-1 build/ClosureCriteriaScout.md:14 flagged ("needs whitespace normalization"). At tip the stale-sentence leg hits only :184, where the erratum quotes it.
  - Mutations (legs `grep -n 'no round-23 artifact has landed'` / `grep -nE 'erratum|superseded'`; 0 = hit):
    - tip → 0/0.
    - A, original premise rewritten in place, erratum kept → 0/0 (PASSES).
    - B, erratum removed → 1/1 (fails).
    - C, erratum cites a nonexistent `:999-1005` of the 420-line log → 0/0 (PASSES).
    The check sees only that an erratum exists. It misses a rewrite of the old sentence and a bad receipt line, so append-only rests on §1, not on R5.
  - Trigger fit unanswered. R5 covers "later receipts overtake a landed note's premise". Here the receipts landed first (f9337d5 14:22:45Z) and the note landed 34 s later, already overtaken. The narrowing places the fault at commit time, "without the … erratum R5 requires". R5 has no landing-time clause and was born in `94da19e` (2026-10-19), after the 2026-10-16 commit (M19 "captured-by: none" agrees). The facts are true, but whether R5 is the right rule for this case is not addressed.
- R1 gap (LOW): the narrowing corrects M19's verdict. R1 (QUALITY.md:94) requires "the recompute command", but the errata block round-24.md:143-157 carries none: grep `git |grep |python|Recompute` → exit 1. The wave-1 proposal's `Recompute: git log -1 --format=%cI 3358c4d; grep -n '13:33Z' …` (build/RevM19Critic.md:33-34) was dropped on landing.

## Residual risk / gaps
- [INFERENCE] The note's absence proof may be vacuous. `find . -newermt "2026-10-16 12:00"` in the host TZ (−03) uses a threshold of 2026-10-16T15:00:00Z (`date -u -d @…`), which is after the 13:33Z write, so it would return nothing regardless. Neither correction mentions this. Not tested: the r23 seat's actual TZ.
- Out of scope, not checked: the F5/F6 bullets in the same errata block.

VERDICT: PARTIAL — append-only and every cited fact survive (S1/S2 are pointer/qualifier slips), and the M19 time-bounded clarification closes; the critic's "reevaluate R5" half is not shown: R5 is unchanged and its check passes the rewrite and bad-line mutations; the R1 recompute command is missing.
Installs: none (git, coreutils, python3 already present).
