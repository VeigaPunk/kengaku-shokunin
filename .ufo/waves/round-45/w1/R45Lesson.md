# R45Lesson — scribe report (kengaku round 45, wave 1, 2026-10-26)

Seat `R45Lesson` (scribe). Scope: draft `corpus/lessons/round-45.md` plus the SCORECARD round-45 section and the
LOG.md round-45 entry. **No lane file was written** (the lesson, scorecard and log drafts live in my subdir); no
counter, probe or fixture build was run by this seat; no git/jj mutation; no subagent. Times -03.

## Delivered artefacts (all under `.ufo/waves/round-45/w1/`)

| path | sha256 | what |
|---|---|---|
| `R45Lesson/corpus/lessons/round-45.md` | `7ea5ae7a7ca520963e3b0706d3fca97e4eb63f716c3c8a238cc826d09d2402d2` | 125 lines; exactly three `##` sections — `## Gate`, `## Mistakes`, `## Predictions` (plus a `### Routed` subsection under Predictions) |
| `R45Lesson/scorecard-round45-draft.md` | `ef65345221a4b6d269077020243cadebbefc227982e16a034eca3d79e1cf36a4` | SCORECARD round-45 section in the round-44 shape, with `<<FILL>>` slots |
| `R45Lesson/log-round45-draft.md` | `ca4d8c899e88dbe617f69808df645ae13b51905c74e564ad7747ddb45a8504c9` | LOG.md round-45 entry in the round-44 shape, with `<<FILL>>` slots |
| `R45Lesson/qcheck.py` / `qcheck_strict.py` | `69086738…` / `40e844ee…` | quote-location checkers (lenient basename resolution / strict `capture_dir / name`) |
| `R45Lesson/refetch-and-quotecheck.txt` | `ed85a16c…` | envelope-bracketed refetch of the nine upstream files + strict check of the lane entry |
| `R45Lesson/entry-quotecheck-strict.txt` | `def6cd0d…` | envelope-bracketed strict check of both entry revisions + physical line counts |
| `R45Lesson/lesson-gate-quotes.txt` (+ `.py`) | — | 11/11 Gate quotes verified verbatim on their cited capture lines |

Sections delivered (acceptance): `## Gate` (8 admits S149–S156, each with a located quote + sha256 + flip; 2 rejects
— `gitignore` with reason+flip, `SHA256SUMS` — plus a flip-check shell block), `## Mistakes` (6 rows: the round's
mined do-nothing-control row, the docstring-repair row, the gitignore-as-row row, the frozen-edit row, the entry-
citation row, the capture-layout/anchor row), `## Predictions` (frozen predictions vs before-controls vs observed,
plus `### Routed` mapping the five round-44 spot-check §4 items onto this round's instruments).

## Measurements made by this seat (each with its command)

1. **Nine upstream files byte-identical to the captures** — envelope-bracketed, `refetch-and-quotecheck.txt`:
   `ENVELOPE start 23:34:31 … ENVELOPE end 23:34:35 exit=0 local_bin_content_before=c263b11afb1cccf6
   after=c263b11afb1cccf6 unchanged`; nine `http=200`; nine `identical` under `cmp`.
2. **Physical line counts** (last line counted even without final newline): `test_outputs.py 18, instruction.md 9,
   setup.sh 43, Dockerfile 20, test.sh 29, README.md 33, solve.sh 68, task.toml 41, gitignore 23` — so the entry's
   five past-EOF `source:` ranges (`setup.sh 1-45`, `Dockerfile 1-16`, `test.sh 1-31`, `README.md 1-46`,
   `solve.sh 1-70`) were real at 23:29:43.
3. **Entry quote lines** — lane copy at 23:29:43 (`657a16ca…`): 19 quote rows, 10 with flat capture names (unreadable
   under `plans/pkg_gate.py`'s `capture_dir / name`), 6 line errors after remapping, one row's quote containing two
   `|`. `R45PkgEntry`'s independent check agrees (`quote rows 19 … unreadable rows: 10 … line mismatches: 6 of 19`,
   `lane-entry-check.txt` sha256 `5c7068b2…`). The file was then rewritten: `2f26e325…` (23:38:12, `rows=17 bad=0`)
   and `9472e6b1…` (23:39:34, `rows=17 bad=0`, flat names after the captures were flattened).
4. **Anchor leg red at the nested layout** — read from `R45PkgRows/validate.txt`: `ANCHOR_exit=1`,
   `rows=149 tokens=55 defects=5`, five `class=anchor-unbound` (S149 twice, S151, S152, S153, S155), cause “directory
   plus the URL's basename” (`plans/anchor_digest_check.py:53-64`). Round 44's capture dir is flat (12 entries).
5. **Gate quotes** — 11/11 verbatim on the cited line (`lesson-gate-quotes.txt`), verified again after the captures
   were flattened.

## Conflicts recorded verbatim (no judgement — the canonical Rust judge decides)

- **Frozen instruments edited after the freeze commit.** Freeze per the seat assignment: `b4fcd351`. Child
  `52d7486` (23:20:26) changes `plans/round-45-claims.md` (`rows S149–S157` → `rows S149–S156`) and
  `plans/round45_c2_verify.py` (`SPEC_SHA256` re-pinned); `claims/frozen-digests.txt` keeps two digests for each.
  Uncommitted at 23:38:11: `plans/round45_c2_verify.py` hashes `156a4242fe1b3ec27d1f5b2c09acad3f61095525476da9248f1f1c96e5c5a757`
  against the frozen `8c302709…`, diff = `MECH_ROW` capture group `[A-Za-z0-9_.-]+` → `[A-Za-z0-9_./-]+` and
  `"under-varsea": {"tests/test_outputs.py": (9,)}` → `(9, 10)`.
- **Frozen capture directory rewritten in place at 23:38.** `git status --porcelain -- corpus/evidence/round45` →
  five `D` (`environment/Dockerfile`, `environment/setup.sh`, `solution/solve.sh`, `tests/test.sh`,
  `tests/test_outputs.py`) + five `??` (flat names); all nine file sha256 unchanged; `SHA256SUMS` now
  `fb2cf5e8d0e717f5ba0fa17642a73133bcaa79e37a702223c0acc971cf8dbfb6`.
- **`plans/fixture_fence.py` absent** at 23:30:47 (`ls` → `No such file or directory`), so C1's fence leg had no
  subject; the round-45 C2 counter had no run receipt at draft time.
- **PATH-dir content drifted between my two envelope runs** (not by this seat; neither run saw an internal change,
  so both receipts are valid under Q32): `~/.local/bin` digest `c263b11afb1cccf6` at 23:34:31 →
  `e396f23e40a69201` at 23:38:11; `find ~/.local/bin -newermt '2026-10-26 23:30'` names
  `OpenBot-0.51.1-x86_64.AppImage` (296,219,269 B, 23:36:46) and `bin` (1,810 B, 23:36:47). Recorded, not assessed.

## Not done / out of scope

- Did not run `plans/round45_c1_verify.py`, `plans/round45_c2_verify.py`, `plans/password_recovery_probe.py`,
  `plans/anchor_digest_check.py` or any fixture build. Every `<<UNOBSERVED: …>>` slot in the draft is a fact I did
  not measure; the lesson says so at each slot.
- Did not edit `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md` or the ledger; did not write into
  `~/.local/bin`, the fleet root or any fixture; no `git add/commit/…`, no jj.
- The probe receipt was **read, not produced**: `cases=16 observed_pass=5 observed_fail=11 mismatches=0`,
  `regrade cases=16 differ=0`, `ENVELOPE … exit=0 … unchanged` (L1 run 23:27:11–23:27:15).

## Scratch

`S=/fast/scratch/hyaku/kengaku-r45/R45Lesson` — deleted below with `plans/scratch_guard.py safe-rm` after the
receipts were copied into `R45Lesson/`. No receipt file in my subdir exceeds 1 MiB (largest: 3.4 KB draft; total
~60 KB).

VERDICT: lesson-draft-sections-3
