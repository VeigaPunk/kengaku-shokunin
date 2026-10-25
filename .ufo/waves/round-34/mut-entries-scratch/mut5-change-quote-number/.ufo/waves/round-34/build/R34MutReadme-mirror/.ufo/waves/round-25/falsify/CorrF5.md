ATTACKS: round-25 §Errata F5 bullet, `corpus/lessons/round-24.md:150-153` ("Gate pass lines superseded"), tested for append-only, for its facts against the evidence, and for whether it closes kaika W3 F5 (`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w3/kengaku-review.md:134`).

## Survives
- S1 append-only. `git diff --numstat 6180e4f 8ea41f9ed -- corpus/lessons/round-24.md` → `16 0`. The -U0 hunk is `@@ -141,0 +142,16 @@`. In bytes, the tip blob starts with the full 22,493-byte base blob, and the base ends in `\n`. Only `8ea41f9` touches the file in that range. The `e21f9ea` blob equals the `6180e4f` blob, and the live file equals the tip blob. "The lines above stay as written" holds.
- S2 the target exists. There are exactly five "Q1–Q8 pass" lines (`round-24.md:65-69`), and the bullet does supersede them explicitly.
- S3 "across four sources (M22)" holds. M22 (`:32`) lists S002×2, S012, S005 and S009. §Post-review corrections (`:120-129`) records them as fixed. The entry corrections exist: `contamination-detection-and-transparency.md:85-100`, `llm-judge-calibration.md:84-97`, `agent-time-horizon-and-task-validity.md:48-62`.
- S4 "corrected" holds for the S009 numbers. I re-fetched https://arxiv.org/html/2506.22316 → 243,278 B, sha256 `3aa84ebb…77ab55f3`, which equals the receipt (`round-24.md:95`). Table `S4.T3`, Ref-5 FR cells: BiGGen 45.54/38.99/37.59/36.48/35.40; FLASK 45.58/45.13/44.58/40.53/48.58. So the ranges at `llm-judge-calibration.md:89-93` are exact. This means `round-25.md:50` ("48.58% column unverified"), in the same commit, is stale and the lane's record contradicts itself. Sibling ReopenS009F3 found the same.
- S5 F5's Gate half is met as written: the pass lines are superseded, and F2–F3 are named (by content, via M22) as fixed.

## Breaks (by severity)
- M1 (medium) The one verdict the bullet restates misrecords the outside verdict.
  - `:152` says "the judge-calibration entry's gate result is 'disagree (partial), corrected'".
  - The outside records for this admit sample say agree:
    - `kengaku-review.md:95`: "**agree (admit)** | Admission holds … they do not reverse the admit".
    - `kengaku-review.md:115`: "One admit agreed".
    - The integrator's `corpus/lessons/round-24-verifier-spotcheck.md:12`: "admit | llm-judge-calibration.md … | W3ReviewKengaku | agree"; `:17` "ADMITTED".
  - `grep -rn 'disagree (partial)' /home/vgpnk/Projects/shokunin/.ufo` → no matches. The label comes only from the lane's own line `round-24.md:120` (`e21f9ea`).
  - It is also a category error. Per `corpus/QUALITY.md:12-13`, the Gate records "pass/fail per entry". Agree/disagree is the outside spot-check vocabulary, and discernment is scored on it (`LEARNING.md:35,45`). Writing "disagree" as the gate result flips r24's admit sample from agree to disagree.
  - Right reading: admitted; outside re-check failed one S012 location and one approximate S009 figure; both corrected; spot-check agree.
- L1 (low) "one unreproduced range" is false against the pinned source.
  - `llm-judge-calibration.md:27` "up to ~45–48%" matches the per-dataset Ref-5 FR maxima: 45.54 (BiGGen, GPT-4o) and 48.58 (FLASK, Mistral), per S4.
  - So it was an approximation (a Q10 defect, `QUALITY.md:75-78`), not an unreproduced figure.
  - The bullet repeats W3 F3's misread ("unlabelled 4th column", `kengaku-review.md:132`). FLASK spans two columns (colspan=2, FR|MAD), so its FR column is labelled.
  - It is also harsher than the lane's own `e21f9ea` wording: "not what Table 3 reports as a single range" (`llm-judge-calibration.md:89-90`); M22 says "one number drifted".
- L2 (low) "the outside spot-check found five quote-location slips" is wrong: it found four.
  - The review lists four, F2(a)–(d) at `kengaku-review.md:128-131`, and `:114` says "four location slips and one unreproduced figure".
  - The fifth slip, S005 opening-summary item 2 "Contamination" (`agent-time-horizon-and-task-validity.md:59-62`), is not in the review. `grep S005` on the review → only `:68`, `:131`, `:141`. The lane found it when it re-opened S005 (`:51`).
  - `:95`'s "Two location slips (F2b)" does not rescue the count. F2b (`:129`) names one slip, and the lane corrected one judge location. The count was copied from `RevF5.md:19`.
- L3 (low) "Closes kaika W3 F5's residual" claims too much.
  - RevF5 named two residual surfaces (`.ufo/waves/round-25/build/RevF5.md:17-19`).
  - The second is the fleet report trend bullet `.ufo/reports/round-24/kengaku.md:177-178`: "No admitted entry fails its re-check … 7 agree, 1 location disagree, fixed". It is unchanged; its only commit is `dec4b51`.
  - It is not recorded as residual in `round-25.md:52`, and `LOG.md:290` reads "corrections appended for … F5".
  - The report's own §Post-review fixes (`:244-273`) eases this, so the report half is mitigated, not closed by this bullet.
- L4 (low) The supersession is too broad. All five pass lines (`:65-69`) are superseded "by §Post-review corrections". That section says nothing about the saturation entry (`:67`) or the paired-eval entry (`:69`), and only the judge entry gets a replacement result.
  - RevF5's proposed fix covered only the three corrected entries (`RevF5.md:23`).
  - Two outside-found defects corrected in the same commit cannot be reached from the pointer: F11 (`llm-judge-calibration.md:99-107`) and F12 (`paired-eval-uncertainty-reporting.md:51-57`). F5 itself names only F2–F3, so this is a completeness gap, not an F5 failure.

## Smallest append-only fix (recommendation only; no lane file edited)
Append one line to `round-24.md` §Errata:
- The spot-check verdict on judge-calibration was agree (admit) (`kengaku-review.md:95`). Its gate result is: admitted; S012 location and the approximate S009 figure corrected.
- The outside check found four location slips plus one approximate figure, reproducible from S009 v4 Table 3. The fifth S005 slip was found by the lane.
- The fleet trend bullet `kengaku.md:177` stays residual (integrator-owned).

## Residual risk / verification gaps
- I did not re-open S002, S005 or S012; sibling seats own those. Whether S005's second slip is real is unverified (dynamic OpenAI page). L2 holds either way.
- No LSP server applies to markdown, so checks were done with git, grep and one source fetch.
- Scratch only: `/tmp/k25w2-CorrF5/s009.html`.

VERDICT: PARTIAL — the bullet is append-only and does supersede the five Gate pass lines, but the verdict it restates is wrong ("disagree (partial)" where both outside records say agree; "unreproduced" range disproved by S009 v4 Table 3; outside found 4 slips, not 5), and "closes F5's residual" leaves out RevF5's fleet-report surface.
Installs: none (Python urllib, git, coreutils only; no pacman, uv, npm or binaries).
