# F39ReopenRows — S117/S118 live re-open (kengaku r39 wave 2, falsify)

Seat: F39ReopenRows (reviewer, leaf). 2026-10-26.
Attacks: the frozen TB2 admission rows S117/S118 (corpus/SOURCES.md) — freshness of their anchor sha256s, quote fidelity, cell schema, tier/status/used-by.

## Method

Live fetch of both pinned URLs (commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6), sha256 vs row anchor cells and `corpus/evidence/round39/tb2-git-leak-recovery/SHA256SUMS`, verbatim line checks, 11-cell audit against the registry schema, tier/status/used-by audit against the SOURCES legend (SOURCES.md:1-18). Scratch `/fast/scratch/hyaku/kengaku-r39/F39ReopenRows` (deleted after receipt copy).

## Freshness receipts

`curl -fsSL <url> | sha256sum` (receipt `F39ReopenRows/live-refetch-sha256.txt`):

```
dc7b01c1b9dbb0c123def54b146dc1dd399a600edee5970d043a5db5eac4c775  -   (test_outputs.py)
54ac693fd26a4c003f610d62c4b2671f1d1d04ac5b1286f780605e385a9a5861  -   (instruction.md)
```

- Row anchors (SOURCES.md:132, :133): `sha256 dc7b01c1…4c775`, `sha256 54ac693f…5861` — identical to live.
- SHA256SUMS frozen cell values identical; `sha256sum -c SHA256SUMS` in the capture dir: all 7 files `OK` (Dockerfile, challenge-setup.sh, instruction.md, solve.sh, task.toml, test.sh, test_outputs.py).
- Line-range anchors: `test_outputs.py:1-113` — live file is 113 lines (`wc -l`); `instruction.md:1-9` — live file is 9 lines.

## Quote fidelity

- S117, `test_outputs.py:16` (receipt `F39ReopenRows/S117-line16.txt`), live line verbatim:
  `assert text == "secret[lost_and_found_in_git]", f"Flag value is incorrect: {text}"` — 9 words, row claims 9. Exact.
- S118, `instruction.md:4` (receipt `F39ReopenRows/S118-line4.txt`), live line:
  ` 2. clean up the secret in that repo to make sure it cannot be found anywhere in that repo.` — row quote is the verbatim substring sans the ` 2. ` list marker; 18 words, row claims 18. Exact.

## 11-cell audit (schema SOURCES.md:9: id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by)

Both rows carry exactly 11 cells; per-cell results:

- id/source (S117, S118): URLs byte-match the fetched URLs, pinned to the same commit; no duplicate row covers these files (S116 is build-pmars, a different task — SOURCES.md:131).
- kind: `code` (pytest grader — correct), `docs` (instruction — correct).
- tier: both `A`. Legend (SOURCES.md:12-14): A = "primary or authoritative for the row's scope (spec, official docs, source code, … maintainer statement)". S117 is the executed grader's own source; S118 is the task's own instruction. A is right, scoped to each `scope` cell as required.
- scope: matches observed content (S117 "executed scoring predicate… as this capture shows it"; S118 "the request this one task states…").
- anchor: commit, line ranges, quotes, sha256 — all verified above.
- teaches: S117 — five pytest functions ✓ (`test_flag_file_exists_and_correct`, `test_no_secrets_in_commits`, `test_good_commits_preserved`, `test_no_secrets_in_unreachable_objects`, `test_repository_contents_checksum`); stripped literal ✓ (`read_text().strip()` + `assert text == "secret[lost_and_found_in_git]"`, :15-16); two `git log --all` searches ✓ (`log --all --grep "secret\[" --regexp-ignore-case` and `log --all -p -S "secret["`, :28-45 region); init-message substring ✓ (`"chore: init e665d1a2-04a7-4e61-b523-e897e231d9cc" in commit_messages`); `fsck --lost-found` + `cat-file -p` on dangling ✓; pinned non-dot checksum ✓ (`find /app/repo -type f -not -path '*/\.*' … | sort | sha256sum`, expected `2c3d6389…4adb`). S118 — three asks ✓ (recover to `/app/secret.txt`; clean so "it cannot be found anywhere"; irrelevant files and commit messages untouched) and three hints ✓ (`/app/repo`, `secret[...]` format, exactly one such string) — all present at instruction.md:1-9.
- status: both `mined` — legal vocabulary (queued|mined|rejected, SOURCES.md:5-6) and true: both mined into `corpus/knowledge/tb2-git-leak-recovery-grader.md`.
- opened: `2026-10-26` — matches this round's capture date.
- recheck: `180d` — legal relative form (cf. S014 `90d`, SOURCES.md:30); knowledge file line 4 mirrors `recheck: 180d`.
- used-by: `corpus/knowledge/tb2-git-leak-recovery-grader.md` exists; its :1-2 back-reference both rows by URL, commit, line ranges, and `accessed 2026-10-26`. Bidirectional reference holds.

## Findings

No defects found. Both rows are byte-fresh against the pinned commit today, quotes are verbatim at the stated lines within the ≤25-word rule, all 11 cells are populated per schema, and tier/status/used-by are correct.

Non-defect nits (recorded, no action):
- S118's quote omits the ` 2. ` enumeration prefix of line 4; it remains a byte-verbatim substring at the stated line, consistent with the quote convention.
- The knowledge file's recheck also names `plans/git_leak_probe.py --lane .`; the probe re-run belongs to the C2 verifier's ground, outside this seat's re-open assignment — not silently skipped, just out of scope here.

## Residual risk and verification gaps

- Raw.githubusercontent serves immutable commit-pinned content; the check confirms the rows describe the pinned bytes, and separately that upstream's default branch may have diverged (not examined — anchors pin by commit, so divergence cannot invalidate the rows).
- `sha256sum -c` proves the frozen captures match SHA256SUMS; it cannot prove SHA256SUMS itself was frozen before any later edit — that chain rests on the freeze hash 088f7c36 recorded in plans/round-39-claims.md, not re-derived here.

## Receipts (all under .ufo/waves/round-39/falsify/F39ReopenRows/)

- `live-refetch-sha256.txt` — second live fetch, independent of the first, same digests.
- `S117-line16.txt`, `S118-line4.txt` — exact live lines quoted above.
- `S117_test_outputs.py`, `S118_instruction.md` — the live bytes fetched 2026-10-26.

Scratch `/fast/scratch/hyaku/kengaku-r39/F39ReopenRows` removed after receipt copy.

VERDICT: rows-2/2-quotes-2/2
