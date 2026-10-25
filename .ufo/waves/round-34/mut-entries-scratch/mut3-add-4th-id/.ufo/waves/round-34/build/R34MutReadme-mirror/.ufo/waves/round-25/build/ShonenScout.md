# ShonenScout — P2c: SHONEN.md vs canonical seed

Read-only seat. Base `6180e4fb92e9`, HEAD `3f371d2`; `git show 6180e4f:SHONEN.md | cmp - SHONEN.md` and the
same at `3f371d2` → identical (SHONEN unchanged through the round-25 pre-registration).

## Exact byte diff
Seed = PROTOCOL.md:441-448, 4-space block de-indented, `<name>`→`kengaku-shokunin`: 8 lines/364 B.
`diff -u /tmp/seed_only.txt SHONEN.md` → SHONEN.md 12 lines/1521 B; LF only, final `\n`, no CR/tab/trailing space.

- delta `+1157 B` = 4 inserted evidence lines (321+245+317+270 = 1153 B) + 4 `\n`.
- each box line differs only at offset 3 (`0x20`→`0x7E`, `[ ]`→`[~]`); lengths 87/71/62/56 unchanged.
- heading, blank lines, prompt and all four box texts byte-identical; U+2014 at offset 19 in both.
- reconstruction (glyphs flipped + the exact 4 lines) == file: `reconstruction_identical True` (1521 B).
  No other byte, box, or prose difference exists.

## Evidence lines per box

Canonical (`PROTOCOL.md:432`): one indented line per box, `[x] <verifier-id>` or `[~]` with a resolvable
pointer, "no other prose"; `PROTOCOL-APPENDIX.md:30` records per-box prose as a variant defect.

- Box1 `:5` → `:6` (321 B); Box2 `:7` → `:8` (245 B); Box3 `:9` → `:10` (317 B); Box4 `:11` → `:12` (270 B).
- Exactly one per box; 4 boxes in canonical order/text; 0 `[x]`, 4 `[~]`; every line is multi-claim
  prose, not a pointer → form non-canonical. `corpus/lessons/round-24.md:28` (M18) already names it, but
  its "multi-line prose" misdescribes the bytes (each block is one physical line); the pointer-only
  defect is what persists.

## Pointer resolution (11/11 named pointers resolve)

- Box1 `corpus/README.md` §Source availability → `corpus/README.md:7` (digest-vs-original at `:9-14`);
  receipt resolves: valid JSON, 80 lines, 8 paths, 12 candidates, `limits`. No pointer to SKILL.md
  though the claim is about it (`SKILL.md:23`, `:53` tables; `:60` anti-patterns; `:556` checklist;
  `:599` sources).
- Box2 `LOG.md rounds 4–14` → `LOG.md:7-21` bullets; no `##` heading exists for rounds 4–15 (first is
  `LOG.md:24` = 16). `analysis_r12.md` (116 lines) and `round-13-coverage.md` (59 lines) both support
  the prose.
- Box3 lesson 118 lines, non-author verifier at `:3`; `0c51208` is parent of `d8f2898`, which parents
  `06cdc98`; all ancestors of HEAD; commit times 22:42:50Z / 23:34:48Z / 23:38:29Z bracket the lesson
  start 23:31:22Z. The "not current" caveat is supported by `round-13-coverage.md:9-15` + receipt.
- Box4 bare `PROVINCE.md` resolves; the claim's support is `PROVINCE.md:141-162` (historical-absent
  table), routing is `:125-139`; `:97-100` supersedes the header's "round 14".

## Proposed canonical one-line pointers

1 `  SKILL.md:23-58`
2 `  LOG.md:7-21`
3 `  corpus/lessons/round-8-aggregator-box3-coldrun.md:3`
4 `  PROVINCE.md:125-139`

Box1 cannot be fully evidenced by one pointer (tables 23-58, anti-patterns 60-178, checklist 556-598,
sources 599+) — operator-side gate-text question, not a lane fix.

## Remaining unknown

Whether a historical non-author verifier may ever convert box3 to `[x]`: `PROTOCOL.md:63-68` requires a
reviewer who did not author the round's changes; this pass is not current, so `[~]` is defensible. The
promotion decision is outside this seat.

SOURCES: no external source opened this round — zero rows. Installs: none.

VERDICT: byte-identical to the canonical seed except four `[ ]`→`[~]` glyphs and four inserted per-box evidence lines (exactly 1 per box, all 11 pointers resolve); the sole canonical defect is prose instead of one resolvable `path:line` pointer per box.
