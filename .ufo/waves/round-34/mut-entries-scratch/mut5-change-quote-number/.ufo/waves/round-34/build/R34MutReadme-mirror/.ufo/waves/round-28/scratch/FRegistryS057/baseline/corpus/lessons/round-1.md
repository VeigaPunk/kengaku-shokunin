# Lessons — round 1

Evidence: LOG.md round-1 entry; commit `90a5ce8` (SKILL.md + LOG.md);
report `~/projects/shokunin/.ufo/reports/round-1/kengaku-shokunin.md`.

## 1. Verify prompt paths before walking them

`~/wikillm/llm-wiki` did not exist (`find -maxdepth 3`, 0 hits). Actual
copy at `~/Projects/webzites/repos/llm-wiki`. Lesson: ground-truth every
path in a task prompt with one `ls`/`find` before planning reads; record
the corrected path in SKILL.md so the next agent skips the search.

## 2. Seed SKILL.md is filler; replace, don't append

The seed was 408 bytes of generic instructions ("develop decision
tables…"). Round-1 rewrite grounded every table row in a cited wiki
section. Lesson: shonen SKILL.md has zero information value — treat as
placeholder, write the domain artifact wholesale.

## 3. Write tool can emit non-ASCII invisibly

A zero-width non-joiner appeared inside "godspeed" on SKILL.md line 116
after `write`; caught only by `grep -nP '[\x{200B}-\x{200D}]'`. Lesson:
after any large `write`, run the invisible-char check before commit —
zero-width chars survive `read` silently.
