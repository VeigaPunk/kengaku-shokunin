# F39MapControl — V7 controls on the landed C2 entry (kengaku r39, wave 2 FALSIFY)

2026-10-26. Target: `corpus/knowledge/tb2-git-leak-recovery-grader.md` `## Requirement map` (entry:130-144) and the
frozen counter `plans/round39_c2_verify.py` V7, measured at lane tip `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c`.

## Fixture

- `S=/fast/scratch/hyaku/kengaku-r39/F39MapControl`; `git clone -q --no-local <lane> "$S/lane" && git -C "$S/lane" checkout -q a6832f5…`;
  `git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r39/F39MapControl/lane` (checked before any write).
  `TMPDIR=$S`; counter run as `python3 plans/round39_c2_verify.py --lane . --work "$S/work"`. Scratch deleted before finish (`scratch_exists=no`).
- Mutated bytes are the landed bytes: `sha256sum` lane vs clone entry → both `7659595b05ff4847c161a853acf60ebdc5d77ed60323c3c098fe0dcf82bd4fb4`;
  receipt `git-leak-probe.txt` both `d7f3a465ccc411572c96fc039235854093d1eb52ccd685b618a28a10de609b5f`.
- No lane file touched: `git -C <lane> status --porcelain -- corpus plans` → `0`. No process left running (`pgrep -af 'round39|git_leak|pkg_gate'` → none).

## Baseline (pristine clone)

`python3 plans/round39_c2_verify.py --lane . --work "$S/work"` (2.56 s wall, exit 0; full output: `baseline-counter.txt`):

```
V7 ok rows=4 tags=4 bad=0
checks=7 defects=0
PREDICATE C2 pass
```

Line-identical to the landing measurement `.ufo/waves/round-39/integrate/measure-final.txt` (C2 block: `V7 ok rows=4 tags=4 bad=0` / `checks=7 defects=0` / `PREDICATE C2 pass`).

## Mutants — 25, one per table-row point (entry:141-144)

Method: smallest behavior-bearing point = one map row; harness `v7_battery.py` writes the mutated entry into the
clone, runs the frozen counter, restores, and asserts `sha256 == 7659595b…` after every mutant. Full log: `v7-battery.log`.

| Control | Mutants | V7 verdicts (all: rc=1, `checks=7 defects=1`, `PREDICATE C2 fail`, only V7 DEFECT) |
|---|---|---|
| relabel each row to each other label | 8 (4 rows × 2 other labels) | 8/8 killed — `<tag>: labelled X, receipt derives Y` for every row/label pair |
| cite a non-violating case | 5 (append `echo-only`/`readme-edited`/`message-rewritten`/`readme-edited` to the wrong rows + replace `readme-edited`→`echo-only` in files-untouched) | 5/5 killed — `cites no case or a case that does not violate it` |
| duplicate a tag | 4 (each tag's row duplicated verbatim) | 4/4 killed — `duplicated=['<tag>']`, rows=5 |
| drop a tag | 4 (each row deleted) | 4/4 killed — `missing=['<tag>']`, rows=3 |
| wrong line number | 4 (3→4, 4→3, 5→4, 5→3) | 4/4 killed — `line N is not the frozen instruction.md:M` |

Every mutant tripped exactly one check — V7; V1-V6 stayed `ok` in all 25 runs. Killed 25, survived 0, inconclusive 0.

### Restoration evidence

Per-mutant restore asserted inside the harness (abort on sha mismatch; never fired). After the last mutant, a full
re-run on restored bytes: `V7 ok rows=4 tags=4 bad=0` / `checks=7 defects=0` / `PREDICATE C2 pass`,
`restored_entry_sha256=7659595b…` = pristine digest.

## Observation (adjacent, coverage note — no contract change)

V2's `--require-clean-tree` never fired in any mutant run although the entry was a modified *tracked* file:
`plans/pkg_gate.py:262` `c_clean_tree` runs `git ls-files --others --exclude-standard` — untracked only (`pkg_gate.py:259-266`, P9 gated at `:308`).
Reproduced once with a relabelled row: gate printed `P9 ok untracked=0` … `defects=0`, `V2 ok` (`p9-dirty-entry.log`).
Harmless for the predicate because V7 is the check that sees the map and it fires; the flag name is simply broader than its behavior.

## Re-derivation — the 'reviewer should prefer' paragraph

Claim (entry:193-196): dropping empty-app's tags "moves `messages-untouched` from `partly` to **`unenforced`**"
(entry:194) and this is "also what the grader does: test 3 only asks that the init subject appear once" (entry:194-195).

Re-derived with the frozen counter's own `receipt_cases`/`dry`/`derive` over the frozen receipt (`rederive.py`; log `rederive.log`):

- Frozen labels recomputed = the entry map exactly: `recover-secret` enforced (5 violators, all fail), `secret-gone`
  partly (8 fail / 8 pass), `files-untouched` enforced (`empty-app`, `readme-edited` both fail), `messages-untouched`
  partly (`empty-app` fail; `history-rebuilt`, `message-rewritten` pass).
- Excluding `empty-app`: `files-untouched` → **enforced** (only `readme-edited` fails);
  `messages-untouched` → **unenforced** ({`history-rebuilt`: pass, `message-rewritten`: pass}).
- Grader side: capture `test_outputs.py:61` — `assert "chore: init e665d1a2-04a7-4e61-b523-e897e231d9cc" in commit_messages, (` —
  test 3 (lines 52-63) runs only `git log --oneline --all` and asserts substring presence; no other test reads messages.

The paragraph re-derives exactly as written; no defect found.

## Verdict

V7 is sound against this mutant family: every demanded control, on every row, turns V7 red alone; pristine and
restored bytes run green; the `unenforced`-without-empty-app claim is receipt-derivable.

VERDICT: v7-controls-25/25
