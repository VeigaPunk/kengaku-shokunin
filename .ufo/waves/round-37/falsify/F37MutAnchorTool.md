# F37MutAnchorTool — tool-code mutants of `plans/anchor_digest_check.py` (kengaku round 37, wave 2, falsify)

Seat: F37MutAnchorTool · 2026-10-26 · Lane tip `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5` · before-state `3ea9a1d9005cc07d0a5ce69f4ebf53a81fbcecdd` ("round-36 verifier spot-check").
Target: the **tool code** landed at the tip. Wave 1 (`R37AnchorSweep.md` §5) mutated the *lane fixture* (rows, errata) 5/5 killed with a class-sensitive matrix; this seat mutates the *checker itself* and asks whether the frozen before/after state pair catches it. Complementary probe.

## Axes (godspeed)

1. **calibration** — do the tool's own mutants change the frozen pair's verdict (before `3ea9a1d9` must flag S110; tip must exit 0)?
2. **diagnostic sharpness** — do surviving mutants still name the S110 defect shape (`digest-short`, 63-hex) or only "some" defect?
3. **no harm** — zero writes outside `falsify/` + scratch; lane bytes provably untouched.

## Harness and detector

- `plans/anchor_digest_check.py` has **no selftest**: `main()` accepts only `--lane`, `--evidence-ref`, `--verbose` (source lines 285-288). So the only standing detector is the state pair itself.
- Scratch (fixture rule): `S=/fast/scratch/hyaku/kengaku-r37/F37MutAnchorTool`; `git clone -q --no-local` → `$S/fx/lane` @ tip and `$S/fx/lane36` @ `3ea9a1d9`; `git -C "$D/lane" rev-parse --show-toplevel` = `$D/lane` verified before any run; every git call names `-C`; no commit anywhere; `TMPDIR=$S`.
- Mutants are **copies** under `$S/mut/` (lane file never edited in place). Pristine hash `6d7afcd56a95c59f835be04a16263d43db4840cc8a4b111350be4d7cb8d9a323` = lane file at tip = wave-1 draft hash (R37AnchorSweep.md §table) — byte-identical landing confirmed.
- Note: `plans/anchor_digest_check.py` does **not exist** at `3ea9a1d9` (`sha256sum: ... No such file or directory`), the tool is new at the tip; each mutant is the tip tool copy run against the old lane bytes — exactly the intended calibration exercise.
- Kill rule used: a mutant is **killed** iff the pair's verdict changes — before-state stops reporting `DEFECT S110`, or after-state reports any defect / exit ≠ 0. Message-only deltas are reported but do not count as kills. Baseline validity (pristine): before `exit=1` with `DEFECT S110 … class=digest-short detail=63-hex loc=corpus/SOURCES.md:125`; after `exit=0`, `rows=107 tokens=15 defects=0` with `EXEMPT S110` via `corpus/lessons/round-37.md:32`. Baseline passes, so every mutant run below is conclusive (no inconclusives).

## Matrix — 5 mutants × 2 states (all runs `python3 <mutant> --lane <state> --verbose`; receipts in `F37MutAnchorTool/`)

| # | mutant (smallest behavior-bearing point) | before @`3ea9a1d9` | after @tip | verdict |
|---|---|---|---|---|
| M1 | drop the 64-length check: `if not HEX64.fullmatch(tok):` → `if not re.fullmatch(r"[0-9a-f]+", tok):` (check(), line 261) | exit 1; still `DEFECT S110` but diff shows `class=digest-short detail=63-hex` replaced by `class=digest-unknown detail=not-committed-evidence-and-not-in-a-SHA256SUMS` (`m1_drop64_before.diff`, 1 line) | exit 0; output **byte-identical** to pristine (`m1_drop64_after.diff` empty) | **SURVIVED** — before still flags S110, after still clean; only the class label eroded |
| M2 | accept uppercase: format gate `HEX64` → `HEX64_ANY` and membership `tok` → `tok.lower()` (lines 261-268) | exit 1; byte-identical (`m2_upper_before.diff` empty) | exit 0; byte-identical (`m2_upper_after.diff` empty) | **SURVIVED** — neither state contains an uppercase anchor token |
| M3 | skip indented rows: `ROW = r"^ {0,3}\|\s*(S\d{3,})\s*\|"` → `r"^\|\s*(S\d{3,})\s*\|"` (line 78) | exit 1; byte-identical (`m3_indent_before.diff` empty) | exit 0; byte-identical (`m3_indent_after.diff` empty) | **SURVIVED** — every census row in both states starts at column 0 (grep `^ {1,3}\|\s*S\d{3,}\s*\|` on tip SOURCES.md → no matches) |
| M4 | erratum accepted without committed-evidence check: `supported = [t for t, _ in toks if HEX64.fullmatch(t) and t in allowed]` → drop `and t in allowed` (line 213) | exit 1; byte-identical (`m4_errnom_before.diff` empty) | exit 0; byte-identical (`m4_errnom_after.diff` empty) | **SURVIVED** — see note below |
| M5 | search only the round36 dir: `EVIDENCE = "corpus/evidence"` → `"corpus/evidence/round36"` (line 86) | exit 1 (exit code unchanged); defects 5 → **9**: new `DEFECT S036 … abbrev-unresolved`, S105, S106, S107 `digest-unknown` (`m5_r36only_before.diff`, 13 lines); S110 still flagged `digest-short` | **exit 1, `rows=107 tokens=15 defects=12`** — S036, S070, S072-S074, S105-S107, S111, S112, S113, S114 all flagged false-positive on the clean tip (`m5_r36only_after.diff`) | **KILLED** by the after-half: the clean-lane predicate (`exit 0`) fails |

Why M4 cannot bind on these states: at `3ea9a1d9` the erratum does not exist (`git -C fx/lane36 ls-tree --name-only HEAD corpus/lessons/` lists no `round-37.md`), and at the tip the real correction is genuinely committed evidence — `git -C fx/lane cat-file blob HEAD:corpus/evidence/round36/tb2-regex-log/instruction.md | sha256sum` → `4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c`, exactly the erratum's correction — so the dropped membership check never changes `supported`. The mutation is semantically live (a fabricated erratum citing any 64-hex string would exempt a row and silence `erratum-incomplete`), but the frozen pair has no state where an erratum cites an unverifiable correction. Wave 1's fixture matrix did test that axis (its M1: "erratum's correction → fabricated 64-hex" → killed), so the gap is in the **standing state pair**, not in the tool's total test history.

## Coverage findings (survivors are findings, not contract changes)

1. **The frozen pair is verdict-shaped, not class-shaped.** M1 survives while silently degrading the exact diagnostic the tool was built for: S110 is still flagged, but the tool no longer says `digest-short detail=63-hex` — it says `digest-unknown`. A class-sensitive assertion on the before-state (`class=digest-short` for S110), like wave 1's matrix used, would kill M1. Until then, the landing's calibration cannot detect loss of the S110 defect *shape*, only loss of "some S110 defect".
2. **Three whole axes are unexercised by the pair**: uppercase tokens (M2), indented census rows (M3), and unverifiable erratum corrections (M4). Each mutant is byte-identical on both frozen states; nothing in the two commits can distinguish them from pristine. Any future recalibration of this tool should add one fixture per axis (wave-1's `fixture_matrix.py` already covers the erratum-fabrication and uppercase axes when it is re-run; it is not part of the frozen predicate).
3. **M5 is the one mutant the pair genuinely owns**: narrowing the evidence root breaks the clean tip loudly (12 false defects incl. all of C2's S111-S113) while leaving the before-half's S110 flag intact — the pair catches it in the after direction only.

## No harm / restoration evidence

- Mutants lived only in `$S/mut/`; the lane file was never opened for writing. After all runs: `sha256sum` of clone `plans/anchor_digest_check.py` and of the real lane file both `6d7afcd56a95c59f835be04a16263d43db4840cc8a4b111350be4d7cb8d9a323` (unchanged from baseline); `git -C "$D/lane" status --porcelain` → empty (exit 0). Mutant hashes recorded in `F37MutAnchorTool/mutant-hashes.txt`.
- No lane file edited; writes confined to `.ufo/waves/round-37/falsify/F37MutAnchorTool/` (receipts: pristine + 5×2 verbose outputs, 5×2 diffs, hashes) and scratch. No tools installed. Scratch `/fast/scratch/hyaku/kengaku-r37/F37MutAnchorTool/` deleted at the end (trap + explicit `rm -rf`).

VERDICT: anchor-tool-mutants-1/5
