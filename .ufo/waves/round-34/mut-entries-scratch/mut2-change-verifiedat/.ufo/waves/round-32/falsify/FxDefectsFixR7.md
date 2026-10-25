# FxDefectsFixR7 — round-30 lesson peer-review erratum (planned R7 repair)

Round 32, C2. Pre-repair tree = committed `corpus/lessons/round-30.md` (untouched in `git status`); counter = on-disk `plans/round32_defects.py` (its `check_r7` is byte-identical to the frozen copy at `0d32691`; the only uncommitted plan edits are R1/R2 selftest fixture plumbing).

## Ground truth (both reads confirmed)

- `corpus/lessons/round-30.md:66` (line 66): `Q5 pass (S082 labelled a working paper, S084 vendor documentation, S085 a self-report, S081/S082 preprints vs S083/S086 peer-reviewed); Q6 pass` — the grouping **"S083/S086 peer-reviewed"** is present, exactly as R7 targets it.
- `corpus/SOURCES.md:110` (S086 row, scope cell): `...in Japanese; the society publishes these proceedings **without peer review**` — the registry records S086 as published **without** peer review. S083's own cell ("a peer-reviewed benchmark paper's own…") does carry peer review, so the lesson's `S083/S086 peer-reviewed` grouping is wrong for S086. The defect is real and the planned repair is factually correct.

## Simulation (R7 check against appended erratum)

Loaded `plans/round32_defects.py`, copied the committed lesson to `/tmp/r32f-FxDefectsFixR7/`, appended the exact drafted erratum text from `.ufo/waves/round-32/build/R32DraftErrata.md` (line 53), ran `check_r7`:

- Pre-repair (no append) → **RED**: `no appended erratum records S086 as published without peer review`.
- Repaired → **GREEN**: returns `''` (no defect). `check_r7` passes.

**Exact appended line** (one physical line, 246 chars, verbatim bytes from the draft):

```
> **Erratum (round 32):** The `:66` grouping “S083/S086 peer-reviewed” is incorrect for S086. The registry cell records that the society publishes S086 without peer review. S086 is therefore not peer-reviewed; the grouping does not apply to S086.
```

It satisfies all three R7 clauses on the same physical line: `peer-reviewed` still present (append-only), `S086` + `without peer review` within 250 chars, and `S086` + `erratum` within 250 chars (the `.` in `near()` does not cross newlines, so same-line co-occurrence is required and met).

## Residual risks (honesty, not blockers)

- The counter is a token test. A wrapped-but-semantically-identical variant also passes, and so does the denial route (`we cannot claim S086 was published without peer review; erratum pending` → green). A "natural" markdown form with `## Erratum` as a heading line then `- S086 …` on the next line **fails** red (`the S086 peer-review erratum is not labelled`) because the label word is not on S086's line. The drafted single-line blockquote form avoids this; the lane must append it as one physical line.
- Append-only discipline holds: the pre-repair correction's text is left untouched and the erratum is appended.

VERDICT: r7-closable
