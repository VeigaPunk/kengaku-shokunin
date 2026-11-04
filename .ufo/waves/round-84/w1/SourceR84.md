# SourceR84 — scoped findings

Round 84 (kengaku), wave w1, seat SourceR84 (scribe). Access date 2026-11-04.
Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Axes: coverage, calibration.
Full audited report with commands and exit codes: `.ufo/waves/round-84/w1/SourceR84/report.txt`.

- Opened the pinned `gcode-to-text` grader this round: HTTP 200, 644 B, sha256 `6b049dc626aa103b20d165552e5cb39ba02c6803b04ba06a43d79435b5f701a6`, equal to the required pin and `cmp`-identical (exit 0) to `corpus/evidence/round52/graders/gcode-to-text/tests/test_outputs.py`. A second independent fetch returned the same bytes, so there is no difference to record and no blocked stop.
- Located quote (exactly one, 5 whitespace-split words) at `:17`: `assert hello_path.read_text().strip() == "flag{gc0d3_iz_ch4LLenGiNg}", (`. Test functions at `:6` (`test_hello_file_exists`) and `:13` (`test_hello_file_content`); body spans `:6-19`.
- Draft row **S271** in the exact 11-column S267 schema, tier A, scope "member replay only — pinned grader acceptance semantics; not a solved-task, model or image claim", no literal pipe in any cell: `.ufo/waves/round-84/w1/SourceR84/S271-row.md`. Draft only — `corpus/SOURCES.md` was not edited.
- Draft round-84 lesson Gate row in the round-83 Gate table shape (5 columns), with URL, access date 2026-11-04, the `:17` quote and word count, reason and flip condition: `.ufo/waves/round-84/w1/SourceR84/gate-row.md`. `corpus/lessons/round-84.md` is ABSENT at this revision; the L1 installs it.
- Fetch transcript (command, HTTP status, byte count, sha256, cmp exit codes, pin check, quote derivation): `.ufo/waves/round-84/w1/SourceR84/fetch.txt`.

## Flag for the L1 (calibration axis, R84-C2 Q13 leg — not edited by this seat)

The frozen Q13 leg names `plans/gate_timing_check.py --lesson corpus/lessons/round-84.md --commit REV`, exit 0. Read-only inspection plus two throwaway scratch fixtures show two conditions the round-84 tree does not currently meet:

1. The checker parses only Gate tables whose header cells contain candidate/decision/reason. The round-83 Gate shape yields zero parsed admissions; on the real lane, `--lesson corpus/lessons/round-83.md --commit 5beac9c4` prints "FAIL: no admit rows in ## Gate" and exits 1. The round-84 lesson needs a candidate/decision/reason table for the knowledge-entry re-admission, alongside the round-83-shaped source table.
2. `is_second_wave()` matches only `falsify` or `wave[-_ ]?0*2`; the round-84 wave directory `w1` is not matched. Fixture: a Gate cell citing `.ufo/waves/round-84/w1/ReviewerR84.md` → FAIL / exit 1 / `second-seat-reports=0`; the same lesson with the report under `.ufo/waves/round-84/falsify/` plus a `falsify/swarm-registry.json` → PASS / exit 0. The registry loader also reads `swarm-registry.json` only from second-wave directories.

Also from the same checker: the candidate entry needs a committed `writer:` line (`corpus/knowledge/tb2-code-from-image-offline.md` has none today), and the cited report must name the candidate path and carry a `VERDICT:` line. This seat's own report cannot serve that role — `scribe` is not an allowed read-only role and the report sits in the `w1` directory. No frozen claim text was changed.

## Limits

Nothing in `corpus/SOURCES.md`, `corpus/lessons/`, `corpus/knowledge/`, `plans/` or the frozen claims file was modified. No build, lint or general test suite was run; no C1 probe, counter or control was executed — the C1 instrument's own verdicts are not this report's evidence. No tool installed or upgraded (curl 8.23.0, Python 3.14.8, OpenSSL 3.6.5, git 2.56.0 observed on the host). No pacman transaction, service restart or config change. Scratch was private, TMPDIR-scoped and removed at exit; no clone or worktree was created; no git mutation in the lane or fleet root (the only commits are in throwaway scratch fixtures).
