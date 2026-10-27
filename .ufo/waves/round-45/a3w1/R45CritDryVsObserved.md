# R45CritDryVsObserved — round 45 a3w1 (dry-vs-observed case audit)

Scope: every frozen prediction in `corpus/evidence/round45/password-recovery-dry-cases-freeze.txt` vs the landed
receipt `corpus/evidence/round45/password-recovery-probe.txt`, case by case — `predicted=` vs observed letter,
`tests=` vs `tests=`, and whether the frozen `violates=` sets stand under the observed outcome.
Measured lane tip: `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (`git -C lane rev-parse HEAD`, also the dispatch hash).

## 0. Tamper / provenance checks (is the receipt a true transcript of the frozen table?)

- Freeze predates the first recorded probe run (`git log`, lane):
  `b4fcd35 21:24:14` freeze → `05b02e2 23:27:18` "first recorded probe run" → `7d062c0 23:40:57` receipt reframe.
  The freeze file's only commit is `b4fcd35`.
- Freeze digest matches the C2 counter pin: `sha256sum` = `46036abe…aabb` = `DRY_SHA256`
  (`plans/round45_c2_verify.py:93`). Receipt `cf74f451…4e2` (not pinned by the counter; it is gate-regenerated).
- Captures intact: `sha256sum -c SHA256SUMS` in `corpus/evidence/round45/tb2-password-recovery/` → 9× `OK`.
- Fresh `--dry` on a clean `--shared` clone inside the envelope is BYTE-IDENTICAL to the freeze
  (`diff` → `DRY-BYTE-IDENTICAL`; receipt `dry-rerun.txt`).
- Fresh FULL probe run inside the envelope is BYTE-IDENTICAL to the committed receipt
  (`diff` → `RECEIPT-BYTE-IDENTICAL`, sha256 `cf74f451…4e2`; receipt `probe-rerun.txt`, `-clean.txt`):
  ```
  ENVELOPE start 00:29:53 cwd=/home/vgpnk/Projects/shokunin
  ENVELOPE end 00:29:57 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
  ```
  Dry envelope: `ENVELOPE start 00:29:37 … exit=0 … ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged`.
- Structural caveat (matters for what "matching" proves): the receipt's `violates=` and `predicted_tests=`
  are printed from the SAME `CASES` table that generates `--dry` (`plans/password_recovery_probe.py:352-355`),
  and `match=` compares only the test letters (`l1 == c.predicted`). So freeze↔receipt tag equality is **by
  construction** — the receipt cannot detect a wrong tag set. The audit below re-derives tags independently.

## 1. Case-by-case comparison (all 16, freeze order = receipt order)

| Case | freeze pred/tests | observed/tests | verdict match | violates= identical | regrade |
|---|---|---|---|---|---|
| nop | fail / F- | fail / F- | yes | yes | same |
| oracle-solve-sh | pass / PP | pass / PP | yes | yes | same |
| constant | pass / PP | pass / PP | yes | yes | same |
| constant-crlf | pass / PP | pass / PP | yes | yes | same |
| constant-joined | fail / PF | fail / PF | yes | yes | same |
| dir-state | fail / PF | fail / PF | yes (`error=IsADirectoryError` added) | yes | same |
| empty-file | fail / PF | fail / PF | yes | yes | same |
| wrong-23 | fail / PF | fail / PF | yes | yes | same |
| prefix-decoy | fail / PF | fail / PF | yes | yes | same |
| sub-first | fail / PF | fail / PF | yes | yes | same |
| sub-last | fail / PF | fail / PF | yes | yes | same |
| lower23 | fail / PF | fail / PF | yes | yes | same |
| decoys-1000 | pass / PP | pass / PP | yes | yes | same |
| password-eq | fail / PF | fail / PF | yes | yes | same |
| crlf-line | pass / PP | pass / PP | yes | yes | same |
| under-varsea | fail / F- | fail / F- | yes | yes | same |

Summary: `cases=16 predicted_pass=5 fail=11` = `observed_pass=5 observed_fail=11 mismatches=0`,
`regrade cases=16 differ=0` — reproduced on my own run (receipt `crosscheck.txt`: `FIELD-MISMATCHES: 0`).

Test-letter semantics confirmed against the captured grader: `F-` = first assert dies, second test never run
by the harness (disclosed in the probe docstring: pytest would run it and still exit 1 — the only thing
`test.sh` rewards). `dir-state`'s `PF` is the IsADirectoryError path, verified: `exists()` true on a directory,
`read_text()` raises, harness maps non-assert exception → `F` (`probe:202-204`).

## 2. Requirement-map labels — do the frozen violates= sets still stand?

Re-derived labels from MY fresh receipt (V7 rule `derive()`, `round45_c2_verify.py:241-246`):
all nine tags reproduce the entry's labels exactly (`crosscheck.txt`: forensic→partly, the other eight→enforced).
**No observed outcome changed any label: zero cases passed with a tag set that did not foresee it.**

But the frozen tag semantics are never written down, and re-deriving them case by case exposes defects:

### D1 — `constant-joined` vs `dir-state`: `recover` tagged inconsistently (the real defect)

The probe's own gloss (`probe:88`): `recover` = "the recovered password is among the guesses".
- `dir-state`: password written (inside the dir), graded artifact yields NO guess list → gloss violated → **tagged**.
- `constant-joined`: password written (joined with two decoys), guess list = `[66-char blob]`,
  `"8XDP5…W54" in guesses` → False → gloss violated → **untagged**.

Symmetric fact patterns, asymmetric tags. Rescue readings fail: "password recoverable as substring" would make
`constant-joined` satisfied but then `dir-state`'s tag (password inside `…/x`, equally grep-able) is wrong and
the gloss is falsified anyway. Under the gloss as written, `constant-joined` should carry `recover`.
Label-stable both ways (either fix keeps `recover` enforced, all-cited cases observed fail), so no label flips —
but the requirement-map row `instruction.md:2 | recover` cites `dir-state` and not `constant-joined`
(entry `:63`): the cited-case list is incomplete under the gloss, or the tag/gloss is wrong. The case's own
prose even describes the recover violation ("the line itself is not the answer") while the tag set omits it.

### D2 — `wrong-23` prose contradicts its own tag set

Freeze line 17 / probe:139-141: tags `prefix,suffix` violated, prose says "format-conforming".
Recipe writes `'Z'×23` — 23 chars ✓, `[A-Z0-9]` ✓, `8XD` ✗, `W54` ✗: only length+charset conform.
Observed `PF` matches prediction, so this is a frozen-table prose defect, not a dry-vs-observed mismatch;
it does weaken "a format-conforming wrong guess is punished" as stated (prefix-decoy is the case that
actually carries that meaning).

### D3 — tag convention is a coin flip the labels silently depend on (fragility, not a landed defect)

The case table leaves a genuine semantic ambiguity: do format tags judge the intended password or every emitted
guess line? Under a strict per-line reading, `password-eq`'s line `PASSWORD=<pw>` (32 chars, no `8XD`, contains
`=`) violates len23/prefix/charset although those tags are absent; `decoys-1000` includes short `WRONGGUESSn`
lines on an observed pass, which would make len23/prefix/suffix partly enforced rather than enforced. This
alternative reading is not forced by the instruction, whose shape clauses describe the password, not every
candidate guess. The oracle case does NOT demonstrate a counterexample: `solve.sh` builds candidates by
trimming the right edge of the `8XD`-starting first fragment and left edge of the `W54`-ending last fragment,
so emitted 23-char combinations retain the prefix and suffix. The freeze's intended-password interpretation
is plausible, but is nowhere stated; the observed cases cannot distinguish these readings. This is a limitation
of the requirement-map's explanatory semantics, not evidence that any derived label changed.


### D4 — structural: `mismatches=0` can never certify the tag sets

The receipt echoes `violates=` from the frozen `Case.violates` field itself (`probe:355`) and `match=`
compares only letters. A freeze that mis-tagged every case would still print `mismatches=0`, `match=yes`,
`regrade=same`. The C2 kill rule ("a probe case whose observed verdict contradicts its frozen prediction")
therefore binds verdicts only; tag-set correctness rests entirely on the freeze author's annotation —
the only independent check of it in this wave is this audit (which finds D1/D2 above).

## 3. Disagreements found

1. `recover` on `constant-joined` (freeze omits; its own gloss + symmetry with `dir-state` require it) —
   label-stable annotation defect (D1).
2. `wrong-23` prose "format-conforming" vs its tag set — prose defect (D2).
3. Undocumented tag convention; per-line reading would flip len23/prefix/suffix/charset labels via passing
   cases — fragility, no landed label change (D3).
4. `match`/`mismatches`/`regrade` columns verify letters only; `violates=` equality is by construction (D4).

No disagreements on: any `predicted=` letter (16/16), any `tests=` pair (16/16, incl. the two `F-` short-circuits),
pass/fail counts, case order, `regrade` (16× `same`), or any derived requirement-map label (9/9 reproduced).
Not independently verifiable: the order claim "no case executed before the freeze" (git timestamps corroborate
the commit order but not host execution history); V11 state disagreements (outside this item).

Report receipts: `R45CritDryVsObserved/{dry-rerun.txt,probe-rerun.txt,probe-rerun-clean.txt,crosscheck.txt}`.

VERDICT: dry-vs-observed-mismatches-0
