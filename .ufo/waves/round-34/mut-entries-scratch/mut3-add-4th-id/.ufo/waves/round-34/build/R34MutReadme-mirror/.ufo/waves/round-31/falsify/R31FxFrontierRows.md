# R31FxFrontierRows — falsify report: corpus/README.md lined changes

Lane: `kengaku-shokunin` (baseline `0883e72`, landed round-31 commit `dbb07364`).
Attack target: the three README changes at `dbb07364` — index row, coverage-map row, frontier sub-bullet —
plus the bidirectional index count. All commands below ran from the lane root unless noted.
No files under the lane were created/edited except this report.

---

## 1. Index row: title cell, one row, no duplicate

**Survived.**

- Exactly one index-table row: `corpus/README.md:66` — `| \`knowledge/benchmark-verifier-execution-model.md\` | Where a benchmark's verifier actually runs (Harbor's per-task \`environment_mode\` resolution: shared by default) … | S092 (Harbor @ 6099b8cf), S093 (SWE-bench Pro V2 @ 66f92766), S100 (terminal-bench-2 @ 2fd12b88) |`.
- One-row check (script `plans/round31_c1_verify.py` V4: "the index carries exactly one row for the entry; title cell non-trivial"): `checks=6 defects=0`, exit 0.
- Manual check: `grep -n 'benchmark-verifier-execution-model' corpus/README.md` → exactly 3 lines: table row (`:66`), coverage-map row (`:253`), frontier bullet (`:276`). No duplicate table row.
- Title cell re-derives against the entry body (`corpus/knowledge/benchmark-verifier-execution-model.md`): "per-task `environment_mode` resolution: shared by default" = `verifier_mode.py:31` `return _resolve_mode(task_cfg.verifier) or VerifierEnvironmentMode.SHARED` (byte-verbatim in capture); "stale rewards deleted" = `verifier.py:207` `await self._remove_reward_files()`; "`/tests` re-uploaded unless the verifier image owns it" = `verifier.py:209` guard + `:220-223` upload_dir + `:128` comment (`:128`: "# The verifier image already owns /tests/test.{sh,bat}."); "SWE-bench Pro V2's own git-based test-space reset" = `test.sh:71` `T) git checkout HEAD -- "$path"`; "log-scan grader that reads its PASSED set" = `parser.py:68,71,88-90,121`.
- Pin ids in the row match the registry and the frozen claim pins: S092 → `6099b8cf…`, S093 → `66f92766…`, S100 → `2fd12b88…` (committed `corpus/SOURCES.md` lines 111-113; `plans/round-31-claims.md` pinned revisions).

## 2. Index 40/40, both directions

**Survived.**

- `grep -c '^| \`knowledge/' corpus/README.md` → **40**.
- `ls corpus/knowledge/*.md | wc -l` → **40**.
- Set-equality (no orphans either way): index cell ids vs file basenames, backtick-stripped, `comm -23` / `comm -13` → both empty.

## 3. Coverage-map row (`corpus/README.md:253`)

**Survived** (with one anchor-integrity caveat — see Finding 1).

Re-derived:

- Counts/ids: committed registry at `dbb07364` has **91 distinct** S-rows, no duplicate ids, S092/S093/S100 present (committed `corpus/SOURCES.md:111-113`); each row tail reads `| mined | 2026-10-25 | 180d | corpus/knowledge/benchmark-verifier-execution-model.md |` (status=mined, opened=2026-10-25, used-by names the entry).
- Counter (live tree): `python3 plans/adoption_check.py --expect .ufo/waves/round-31/adoption-expect.json --census` → `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok`, exit 0. Counter on a clean `git archive dbb07364` copy: same line except `census=fail` (exit 1) — an artifact of running the detached copy (fleet census `--root <lane.parent>` sees no sibling lanes), not a committed-state failure.
- Second receipt: `python3 plans/round31_c1_verify.py --lane .` → `checks=6 defects=0`, exit 0.
- "covered at source-code depth": every code quote the row names locates in the pinned captures (see §1; `verifier_mode.py`, `verifier.py`, `test.sh`, `parser.py`), except one — the S092 anchor (Finding 1).
- "Not runtime task validity (PROVINCE refuses it), not contamination measurement, not deployment config": matches the entry's §What this does not establish; PROVINCE refusal verified at `PROVINCE.md:201` ("runtime task validity, hosted judges and contamination remain open"), `:210`, `:219`.

## 4. Frontier sub-bullet (`corpus/README.md:276`)

**Survived** (one wording tension — see Finding 2).

Re-derived:

- "reads the harness's own verifier-mode resolver and `Verifier.verify` at Harbor commit `6099b8cf`": entry cites `verifier_mode.py` and `verifier.py`; S092 pins `6099b8cf2bfbbb3e7ff1eb2163bfc4524dbd9ba5`; captures verified (HTTP 200 signatures in `R31SrcS092a/b/c.md`; hashes match `captures/SHA256SUMS.txt`).
- "Terminal-Bench 2.0 axis-E cell is filled by this entry": checklist `corpus/knowledge/benchmark-task-validity-checklist.md:94` lists TB2 coverage as "A, B, C, D, F, G" with **no E**; entry fills E (shared mode + harness upload restore).
- "SWE-bench Pro axis-E cell was already credited to S078 in `knowledge/benchmark-task-validity-checklist.md:96`": line 96 reads "**SWE-bench Pro V2** — S078 covers A, B, C, E, F (partly), J" — exact.
- "clause stays open for … runtime task validity (which `PROVINCE.md` refuses to this lane)": verified (above).
- "stays open for Toolathlon": the entry reads no Toolathlon bytes (S080 untouched this round) — confirmed.

---

## Findings

**Finding 1 — Moderate. Landed S092 anchor quote is not byte-locatable at the pin; the caveat was dropped at landing; the repair sits uncommitted.**

- Captured `config.py` @ `6099b8cf` lines 590-593 are four adjacent Python string literals:
  590 `"Whether the verifier runs in the agent's environment ('shared') "`, 591 `"or in a dedicated container ('separate'). When omitted: defaults "`, 592 `"to 'separate' if a verifier 'environment' is set, otherwise "`, 593 `"'shared'."`.
- The committed row's anchor `config.py:590-593: "When omitted: defaults to 'separate' if a verifier 'environment' is set, otherwise 'shared'." (13 words)` — `git show dbb07364:corpus/SOURCES.md | sed -n '111p'` — is **not** a byte substring of the file even newline-normalized (verified programmatically: `q in text` → False). The lane's own gate locates by byte substring (`plans/sources_adopt.py:404-412` `locates`: "never a fuzzy or whitespace-insensitive match"), so this anchor fails the gate's location test as committed.
- Wave-1 knew: `R31DraftEntry.md:24,38,42` flag "four adjacent string literals, not byte-contiguous" and "that one span stays human-verified". The landed registry row dropped that marker.
- The working tree carries an **uncommitted** repair: `git diff HEAD -- corpus/SOURCES.md` shows S092's anchor changed to two spans at `590-592` with "two spans because the description is four implicit string literals" (both spans locate: True), and S100 gained a count command. So `HEAD` ≠ working tree for the registry; today's counters exercise the repaired bytes, not the landed bytes.
- Impact: the entry's substantive content survives (all other quotes I checked locate byte-exactly), so the README's "covered at source-code depth" row is not falsified; but one of the three cited rows' committed anchor does not meet the lane's own located-quote standard, and the fix is not yet landed.

**Finding 2 — Low. Frontier bullet's "clause stays open for task-level scoring code" is overstated by one task's grading code.**

- S093's own registry scope says "the executed grading code for one SWE-bench Pro V2 task" and the entry analyzes that task's `test.sh` + `parser.py` in depth (including the `DATA_DIRS` skip hole and the log-scan last-write-wins rule). Calling "task-level scoring code" fully open after reading and analyzing one task's grading code is imprecise; it should say the remaining suite-wide scoring code stays open. Not a structural failure of the claim (the discharge is explicitly "for verifier execution only"), but the open-clause wording is broader than the evidence warrants.

---

## V E R D I C T

SURVIVED: index row (title cell non-trivial, exactly one row, no duplicate); index **40/40** in both directions; coverage-map row's counts, S-ids, mined/opened/used-by state, counter outputs (`entries=1 … census=ok` exit 0; `checks=6 defects=0`) and all entry-content claims (mode resolution shared-by-default, two restore guarantees, SWE Pro test-space reset, log-scan grader, PROVINCE refusal, TB2 axis-E fill, S078 credit at `checklist:96`).

FELL: nothing fully — but the **committed S092 anchor quote fails byte-location** at the pin (four adjacent literals; caveat present in wave-1 draft, dropped in the landed row), and the repair is only in the uncommitted working tree (`git diff HEAD -- corpus/SOURCES.md`), so the landed row does not meet the lane's own located-quote standard; frontier bullet's "task-level scoring code stays open" wording is broader than S093's read grading code supports.

Residual risk / verification gaps: the pinned-commit authenticity of the captures rests on the wave-1 fetch receipts (`R31SrcS092a/b/c.md`, `R31SrcS093a/b.md`, `R31SrcS100a/b.md`; hashes match `captures/SHA256SUMS.txt`); I did not re-fetch the three repositories (leaf, offline reads only). The TB2 89-manifest / 92-root-entry counts were not re-run live (they rest on `R31DraftEntry.md` §Counts receipts and S100's row); the admission bar's quote-location runs only on captures the gate is handed, so no live re-derivation was possible from this seat.
