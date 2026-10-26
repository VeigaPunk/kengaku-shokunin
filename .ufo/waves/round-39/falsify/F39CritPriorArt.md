# F39CritPriorArt — prior-art re-open for `tb2-git-leak-recovery-grader.md` (kengaku r39, wave 2)

Seat: critic, leaf. Lane tip read: `acf4375` (falsify spec commit); the entry is unchanged since the measured tip `a6832f5`
(`git diff --stat a6832f5..HEAD` → only `falsify-dispatch.json` / `falsify-spec.json`). Entry read at
`corpus/knowledge/tb2-git-leak-recovery-grader.md:294-316`. Every source below was re-fetched as bytes on 2026-10-26
(raw.githubusercontent.com / `gh api` / HF raw), not from search snippets. Scratch `S=/fast/scratch/hyaku/kengaku-r39/F39CritPriorArt`
(removed before yield; receipts copied to `.ufo/waves/round-39/falsify/F39CritPriorArt/`). No lane file edited.

Axes: **novelty** (does any prior source void "first probed instance"), **coverage** (quote/location/date/state per source),
**provenance** (can the reader re-fetch what the entry cites).

## Answer

- **Quotes/locations: 6 of 7 source items check out.** Every quoted string in the `## Prior art` block is present at its
  stated location or commit (the `TASK_REVIEW_AUTOMATION.md:244` quote appears there with the source's
  markdown bold markers, `**Nop Validation**`, stripped by the entry; the two R38 `§2.5` snippets at `:309` are in
  `R38PlanNext.md:126-135`, still unopened as the entry says). One item is mislabelled: **TB2 #86 is a pull
  request, not an issue**.
- **Dates/states: no contradiction.** JonathanGabor `35f11039` = 2026-01-24T01:06:41Z; Evan-Kim2028 `7fd6346` = 2026-09-15;
  TB2 `2fd12b88` = 2026-04-30; TB2.1 `main` = `7131e437`; TB2.1 #239 open 2026-09-25; TB2 #84 open
  2026-09-28; TB2 #86 open PR 2026-09-28; laion dataset created 2026-09-25. The entry states none of these dates, so
  nothing in it is contradicted.
- **Voids: 0.** No cited source reports `echo-only` or an observed reflog-retention pass. The one source on the reflog
  dimension names the gap and asserts it is covered by `fsck` (`audit.txt:1485`); it executed no test, and the entry
  already discloses exactly that.
- **But six precision defects** (D1-D6), two of them material to the novelty paragraph: an overbroad upstream-search
  claim (D1) and an unscoped "first probed instance" that omits a prior **executed** third-party probe (D4).

## Source-by-source

| # | Entry citation | Re-opened result | Reports `echo-only`? | Reports reflog retention? |
|---|---|---|---|---|
| 1 | `harbor-framework/terminal-bench docs/TASK_REVIEW_AUTOMATION.md:244` (entry `:295-296`) | Quote present at line 244 (`\*\*Nop Validation\*\* confirms doing nothing fails tests (task is non-trivial).`). File last touched 2026-10-15 (`2e29ca91d5f1`); live `main`, unpinned. | no | no |
| 2 | JonathanGabor/terminal-bench-2-audit @ `35f11039`, `audit_results/20260120_125158/audit.txt:1485` (`:301-303`) | Verbatim: ``- Doesn't explicitly check `git reflog` entries (though fsck should catch objects if they become dangling after cleanup)``. Commit exists, both author and committer 2026-01-24T01:06:41Z. Method is an LLM rating from task text + container file listing + test code + `solve.sh` (`README.md`; `test_audit.py` has zero `def test_`; `util.py:73-79` pulls the image, `:94-120` lists `/`); **no test case is run**. Task rating 4. | no | names the gap at 1485, no retention observation |
| 3 | Evan-Kim2028/task_validation `data/gold/tb21_census_verdicts.jsonl:33` (`:297-298`) | Exact: `{"unit_id": "git-leak-recovery", "invalid": false, … "grade": "A", "evidence": "reference pass, nop reject", "adjudicator": "machine"}`; commit `7fd6346` 2026-09-15. | no | no |
| 4 | laion/terminal-bench-2-1-apptainer-v1 `README.md:107`, "empty attempt reward 0" (`:298-299`) | Row `\| git-leak-recovery \| validated \| 2/2 \| 0 \|`; header at `:80` defines column 4 as `empty-attempt reward`; `:22` defines `validated` as 2/2 oracle + empty attempt 0. Dataset created 2026-09-25; task not in the modified list (`:45-56`); its pinned upstream revision `7131e437` **is** current TB2.1 `main`. | no | no |
| 5 | TB2.1 issue #239 (`:306-307`) | Open issue, 2026-09-25T22:54:11Z; body: after rewrite + `gc`/`prune`, `repo.commit("d6987af…")` raises `ValueError`, "the trial gets reward 0 even when the working tree is exactly what the task wants". Matches the entry's "opposite defect". | no | no |
| 6 | TB2 #84 (`:307`) | Open issue, 2026-09-28T07:56:53Z, GitPython ValueError on history rewrite. Matches. | no | no |
| 7 | TB2 #86 (`:307`) | **Open pull request** (`pull_request != null`), 2026-09-28T08:18:15Z, `fix(sanitize-git-repo): verifier crashes…`. Entry calls it an "issue". | no | no |

Search receipts for "reports echo-only": `grep -ric 'echo-only'` = 0 in `tra.md`, `audit.txt`, `census.jsonl`,
`laion.md`, and the executed third-party audit (`kim.jsonl`). `grep -ric 'reflog'`: `audit.txt` 2 (line 1241 is a
different task's walkthrough, 1485 is this task), `laion.md` 0, `census.jsonl` 0.

## Findings

### D1 — "No upstream issue or PR … names this grader" is false as written (entry `:305-306`)
Literal counterexamples exist in a repo the entry says it searched (`harbor`), both predating the entry:
- `harbor` issue #1644 (closed, 2026-05-13), body line 14: `result_path: jobs/2026-05-12__15-48-52/git-leak-recovery__amFfVcJ/result.json`;
- `harbor` PR #60 (closed, 2025-10-16), 2 comment occurrences (`git-leak-recovery__HEeFa7o`, `git-leak-recovery__3NHaYWx`).

Both are incidental job-path mentions, not reports about the grader — which is exactly why the sentence should say what it
means. **Impacted axis: provenance (false-negative search claim).** Smallest safe correction: "No upstream issue or PR in
… **reports** this grader" or "files a defect against this grader". Keep the sentence; drop the universal wording.

### D2 — TB2 #86 is a PR, not an issue (entry `:307`)
`gh api repos/harbor-framework/terminal-bench-2/issues/86` → `pr=true`. **Impacted axis: citation fidelity.**
Correction: "TB2 issue #84 and PR #86". One word.

### D3 — The cited audit names three gaps, not one; the `stash-secret` novelty sentence needs the word "probe" (entry `:301-304`, `:312-313`)
The audit's `## Potential Gaps:` list is three bullets, all dismissed:
- `:1485` reflog (quoted by the entry);
- `:1486` "Doesn't explicitly check stashes (though fsck would find stash-related dangling objects)";
- `:1487` "Doesn't check packed objects directly (though fsck handles these)".

The entry's next paragraph says "No opened source reports … `stash-secret`". That stays true only in the sense of
*probed case*; the same cited audit names the stash gap outright. Read strictly, the two sentences collide. The audit also
mis-assesses the grader in the two places nearest this entry's claims: `:1464` "The agent must actually find and extract the
secret to pass this (hardcoding unlikely due to specific format)" — the literal is in the grader at `test_outputs.py:16`,
which is `echo-only`'s whole mechanism — and `:1477` "Explicitly checks dangling commits, blobs, AND trees for `secret[`" —
`cat-file -p` of a dangling commit prints no file content. Those mis-assessments **strengthen** the novelty claim and should
be said, because they are the nearest miss. **Impacted axes: novelty, coverage.** Correction: "One LLM audit names the
reflog, stash and packed-object gaps and dismisses all three" and "No opened source **probes** `echo-only` … `stash-secret`".

### D4 — "first probed instance" is unscoped; a prior executed probe of this grader is uncited (entry `:312-315`)
`kimjune01/terminal-bench-audit` @ `bbe0f8c` (2026-07-20; opened in wave 1, `R39ScoutPriorArt.md` §3.E, dropped from the
entry) re-graded this task in the pinned image `sha256:62160e52…`. `results/verdicts-2.1.jsonl:161-165`:
`baseline gold_pass`; `nuke-git` and `nuke-preexisting` `caught` (reward 0); `reset-hard` reward 1 `FRAME_BLIND`;
`wipe-sentinel` reward 1 `FRAME_BLIND`. So a third party **executed** the grader before round 39 and published a passing
verdict on a mutated state. It does **not** report `echo-only` or reflog retention (its class is collateral-damage
blindness; `nuke-git` is caught, a sensitivity control), so this is not a void — but the bare phrase "first probed instance
for TB2 `git-leak-recovery`" reads as first-ever probing of the grader, which is false. **Impacted axes: novelty,
provenance.** Correction: "first probed instance of the **incomplete-cleanup** class for TB2 `git-leak-recovery`", cite
rows 161-165, and note `reset-hard`'s applicability check only greps for `.git` (`harness/mutations.sh:25-26`) while
`DESIGN.md:85` requires "≥3 commits", so its `applied=yes` may be vacuous — do not lean on it.

### D5 — "one public fork" is unnamed, and the fork wave 1 used is gone (entry `:308`)
`gh api repos/harithoppil/terminal-bench-2-verified` → 404 (2026-10-26). The claim itself is true on other public forks:
`dn522/terminal-bench-2-verified` and `Aochong-Li/terminal-bench-2-verified` both serve `git-leak-recovery/tests/test_outputs.py`
with sha256 `dc7b01c1…`. But the entry gives no locator, so a reader cannot re-check it. **Impacted axis: provenance.**
Correction: name one fork and its commit (e.g. `dn522/terminal-bench-2-verified@<sha>`).

### D6 — the contract line is cited to a moving branch (entry `:296`)
`docs/TASK_REVIEW_AUTOMATION.md` is live `main` (last touch 2026-10-15, `2e29ca91d5f1`); line 244 is correct today but
line-number citations to an unpinned branch drift. **Impacted axis: calibration/operability.** Correction: pin the commit
or record the access date; the quote itself is present and is the project's contract wording for `tasks/`-repo validation.

### Byte-identity claim — verified (`:308`)
`sha256sum` over six files — TB2 pinned fetch, the lane capture, TB2.1 `main` (`7131e437`), the laion revision `7131e437`,
and the two live forks — returns one hash, `dc7b01c1b9dbb0c123def54b146dc1dd399a600edee5970d043a5db5eac4c775`, for all six.
The entry's `dc7b01c1…` is correct; only the fork locator is missing (D5).

## Novelty verdict

No cited source voids "first probed instance" **for the finding as scoped** (an incomplete-cleanup state that scores 5/5):
- the only reflog mention is a gap statement in an unexecuted LLM audit (already disclosed in the entry);
- the only prior executed probe (`kimjune01`) reports a different class and catches the destructive-mutation control;
- the three validation sources report the whole-task verdict only.

The phrase still needs the scope and the kimjune01 citation (D4), and the "No opened source reports …" sentence needs
"probes" to keep it separable from the audit's named stash gap (D3).

## Limits
- No probe, grader, or oracle was executed by this seat; the validation and issue sources were read, not re-run.
- GitHub search is tokenized; I used the quoted phrase `"git-leak-recovery"` (`terminal-bench` 0, TB2 0, TB2.1 0,
  `harbor` 2). Unquoted search returns 83/0/1/16 — all incidental token matches; I did not open those 83.
- `harithoppil/terminal-bench-2-verified` was 404 at 2026-10-26; the two substitute forks were hashed, not cloned.
- `kimjune01` rows were read from `verdicts-2.1.jsonl`, not re-executed; its FRAME_BLIND semantics come from `DESIGN.md:17,70`.
- The JonathanGabor `audit.txt` is copied whole into this seat's receipt dir for line-level re-check; it is a public source,
  not a lane tree.

## Receipts (command → output, abridged)
See `.ufo/waves/round-39/falsify/F39CritPriorArt/receipts{1,2,3,4}.txt`; key lines:

```
$ sed -n 244p tra.md
**Docker Build** … **Nop Validation** confirms doing nothing fails tests (task is non-trivial).
$ sed -n 1485,1487p audit.txt
- Doesn't explicitly check `git reflog` entries (though fsck should catch objects if they become dangling after cleanup)
- Doesn't explicitly check stashes (though fsck would find stash-related dangling objects)
- Doesn't check packed objects directly (though fsck handles these)
$ sed -n 33p census.jsonl
{"unit_id": "git-leak-recovery", "invalid": false, … "grade": "A", "evidence": "reference pass, nop reject", "adjudicator": "machine"}
$ sed -n "80p;107p" laion.md
| task | status | oracle passes | empty-attempt reward | modified |
| `git-leak-recovery` | validated | 2/2 | 0 |  |
$ sha256sum tb2_to.py lane_to.py tb21_to.py laion_to.py f_dn522.py f_Aochong-Li.py
dc7b01c1…c775  (all six)
$ quoted issue search totals: terminal-bench 0, terminal-bench-2 0, terminal-bench-2-1 0, harbor 2
$ gh api issues 239/84/86
#239 pr=false state=open created=2026-09-25T22:54:11Z
#84  pr=false state=open created=2026-09-28T07:56:53Z
#86  pr=true  state=open created=2026-09-28T08:18:15Z
```

Count: 7 source items, 6 fully right (quote+location+state), 1 type mislabel (#86), 0 novelty voids, 6 precision defects.

VERDICT: prior-art-6/7-voids-no
