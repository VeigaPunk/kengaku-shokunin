# W2SentinelScope — scope and safety review, round 52 wave 2 (read-only)

Seat: W2SentinelScope (sentinel, leaf). Lane: kengaku (`kengaku-shokunin`, HEAD `87301ba`, branch `master`). Fleet root: `/home/vgpnk/Projects/shokunin`.
Snapshot: local time ~20:57–20:58 (-0300). Wave 2 was still running (seats writing), so the untracked-tree findings are a point-in-time snapshot.
Scope of this seat: scope discipline and safety of what the round landed. I did not run the C1 or C2 counters and did not attack their predicates (other seats do that).

## Verdict

**Scope discipline: partially clean.** No round-52 seat wrote a tracked file outside the declared surfaces, and I found no evidence that any seat touched the fleet repo's tracked files, `scripts/`, `templates/`, `MANIFEST.json`, fleet `.ufo/state/`, or a sibling lane. Four items need the L1's attention:

1. **(MEDIUM, latent) The GH013-excluded upstream bytes are on disk, untracked, in the lane tree**, under a wave-1 report directory. Not auto-tracked (`snapshot.auto-track = "none()"` confirmed), but one `jj file track` / `git add` of that directory re-publishes them.
2. **(MEDIUM) The same excluded blob is still reachable from local refs**, via two commits (`de616d7`, `cdc0d68`) that are not ancestors of `master`.
3. **(LOW) Wave-2 seats left non-report artefacts in lane `w2/<seat>/` directories** that the spec does not name (scripts, JSON, text receipts). Benign content, but outside the stated write-scope rule ("report file only" plus spec-named receipts).
4. **(LOW) Host absolute paths** (`/home/vgpnk/…`) appear in 89 committed round-52 files (610 occurrences). No credentials were found. Convention issue; the same pattern runs through the lane's older history.

Nothing in the committed tree or the 183 committed captures is credential-shaped. Details below.

## Findings

### F1 — excluded upstream bytes present untracked in the lane tree (MEDIUM, latent)

- Path: `kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecFetchGraders/artifacts/graders/sanitize-git-repo/tests/test_outputs.py`
- Evidence: `sha256sum` = `57e4904177acac5807b51f7c32444bde1968ba0445855fa4333d9eb73865b59e`, the sha pinned in `corpus/evidence/round52/graders/EXCLUDED.md`. It is the only file in the lane tree with that digest outside `.git`/`.jj`.
- The whole directory `.ufo/waves/round-52/w1/C1ExecFetchGraders/artifacts/graders/` is an untracked, byte-identical duplicate of the committed captures: 184 files (94 `test_outputs.py`, 89 `test.sh`, 1 `verify.sh`), including the excluded file. `diff -rq` against `corpus/evidence/round52/graders` reports only the excluded file as extra.
- The committed wave-1 report `w1/C1ExecFetchGraders/report.md` lines 82–85 describe `artifacts/graders/<population-path>` as "the 184 captured grader files", so a reader would reasonably expect that path to be committed.
- Protection today: `scripts/hyaku/jj-lane.sh` sets `snapshot.auto-track="none()"` (verified with `jj --ignore-working-copy config list --repo`), and its `jj file track` step tracks named paths only. A named-directory track of `.ufo/waves/round-52/w1/C1ExecFetchGraders/` or `git add -A` would stage the excluded bytes, and GH013 would fire again.
- Remediation (L1): delete the untracked `artifacts/graders/` duplicate (the `corpus/evidence/round52/graders` copy is canonical and digest-pinned). Do not add the excluded bytes to any tracked path. Correct the wave-1 report's artifact pointer by an append-only note.

### F2 — excluded blob reachable from local refs (MEDIUM)

- `git log --all --find-object=3269e74e727fda61c936ca34b8f3bfaacf199dda` (the excluded file's git blob) returns `de616d7` and `cdc0d68`. Both have parent `07ea208`, so both are pre-amendment C1 commits.
- `git for-each-ref --contains`: `de616d7` is held by **7** `refs/jj/keep/*` refs; `cdc0d68` by **1** (`refs/jj/keep/cdc0d68b…`). Neither is an ancestor of `master` (`87301ba`), so the lane's own history no longer contains the bytes.
- Risk: a `git push --all` / `--mirror`, or a cherry-pick of `de616d7`, would re-trigger GH013. I did not query the remote for these objects (read-only, no network push probes).
- Remediation (L1): never push `--all`/`--mirror`; keep `refs/jj/keep/*` out of any push. Whether to drop those keep refs is the L1's call (a mutating op; not done here).

### F3 — non-report artefacts in wave-2 seat directories (LOW)

Under `.ufo/waves/round-52/w2/`, the spec names by basename these artefacts (receipts or report-referenced files): `confirmations.json` (A/B/C and RevConfirmations), `labels.json`, `prior-art-audit.json`, `candidate-audit.json`, `quote-check.json`, `capture-verification.json`, `index-rows.md`. Those are spec-authorised.

Not named by basename in `w2-spec.json` (count of spec hits = 0):
- `W2ExecCapturesVerify/verify.py`
- `W2ExecEntryDraft/ast_cmp.py`, `why.py`, `build.py`, `counter.out`
- `W2ScribeIndexRows/receipts/c1-now.txt`, `c2-now.txt`, `c1-selftest-now.txt`, `c2-selftest-now.txt`
- `W2ConnectSiblings2/c1-landed.txt`, `c2-landed.txt`

Not checked against the spec: `W2RevEntryLesson/receipts/analysis.json`.

Rule: "Work ONLY inside your own scratch dir and your own wave report file." These files are in the seat's own report directory, contain no credential shapes, and are not a cross-seat write. I classify them as out-of-rule but benign. The L1 should copy only what it accepts and leave the rest out of commits. Snapshot caveat: these seats were still writing at ~20:57.

### F4 — host absolute paths in committed round-52 files (LOW, convention)

- `git grep --cached -c -e /home/vgpnk` over the round-52 committed surfaces: **89 files, 610 occurrences**.
- Largest: `.ufo/waves/round-52/w2-run.out` (51), `w2-dispatch.json` (51), `w1-run.out` (45), `w1-dispatch.json` (45), `w1-results.json` (35), `w2-spec.json` (26), `w2/swarm-registry.json` (25), `w1-spec.json` (23).
- Captures: **0** files contain a host path. Dispatch, spec and run logs are where the paths sit.
- Context: `git grep --cached -l -e /home/vgpnk -e /fast/scratch` returns 6133 committed files across the lane's history, so this predates round 52. Round 52 extends it.
- Remediation: orchestrator-written logs should be redacted or excluded from the lane commit.

## Credential-shape scan (redacted: location and shape only)

Patterns: `hf_`, `gh[pousr]_`, `github_pat_`, `sk-` (word-bounded), `AKIA`, PEM `BEGIN … PRIVATE KEY`, `xox[abpr]-`, `glpat-`, `AIza`, plus a generic `key|secret|token|password|auth = <12+ chars>` assignment.

| scope | token-shape hits | generic hits | notes |
|---|---|---|---|
| committed round-52 surfaces (`.ufo/waves/round-52`, `corpus/evidence/round52`, `plans/round52*`, `plans/round-52-claims.md`, `SKILL.md`, `LOG.md`) | 0 files | 2 files / 2 hits | both false positives: `.ufo/waves/round-52/w1/C2ScribeRowsB/census-base.json:133` (key named `authority`, prose value); `corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py:18` (upstream `tokenizer = …from_pretrained(…)` line) |
| untracked round-52 (`w2/`, `claims/`) | 0 files | 4 hits / 3 files | code identifiers: `W2ExecEntryDraft/build.py:31`, `:40`, `candidate-audit.json:801`, `W2RevEntryLesson/receipts/analysis.json:104`; shape-checked, no values |
| untracked excluded copy (F1) | 2 `hf_`-shaped tokens in one file | — | total lengths 35 and 37 characters; the GH013 trigger. Value not reproduced here |
| committed captures (183) | 0 files | 0 | `FAKE_*TOKEN` and all token shapes: 0 hits in `.py`/`.sh` |
| committed history, unanchored `sk-[A-Za-z0-9_-]{20,}` | 133 files (pre-round, `.ufo/waves/round-29/…` and `plans/fixtures/…`) | — | **word-bounded `(^|[^A-Za-z0-9_-])sk-…` returns 0 files**, so all 133 are substring false positives (`task-…`-style). |

Other: `/tmp/have.txt` (created 18:22 in-window, 767 B, owner vgpnk): 0 hits, purpose unknown.
Not scanned: fleet tracked files beyond the `sk-` check, and fleet `.scratch/`.

## Capture set (`corpus/evidence/round52/graders`)

- Committed: 183 files = 93 `test_outputs.py` + 89 `test.sh` + 1 `verify.sh`, plus `SHA256SUMS` (184 lines) and `EXCLUDED.md`. All 183 names match the TB2 grader shapes. The `sanitize-git-repo/tests/test_outputs.py` entry is absent, as A5 expects.
- `sha256sum -c SHA256SUMS`: **183 OK, 1 missing** (the excluded file). No other failures.
- Non-benchmark content: none found. Capture sizes run from 295 B (`hf-model-inference/tests/test.sh`) to 18,746 B (`filter-js-from-html/tests/test_outputs.py`). Zero host-path or shokunin strings in any capture.
- Upstream spot-check (read-only GET of raw.githubusercontent at pin `2fd12b88…`, saved in scratch and removed): `adaptive-rejection-sampler/tests/test_outputs.py`, `bn-fit-modify/tests/test.sh`, `regex-log/tests/test_outputs.py`; each matches its pinned sha256 (MATCH). The excluded file was not fetched (A5).

## Lane tree: what the wave wrote

Committed since the freeze parent `30801b4` (`git diff --name-only 30801b4 HEAD`):
- `.ufo/waves/round-52/`: 212 files
- `corpus/evidence/round52/`: 185 files
- `plans/round52_c1_grader_audit.py`, `plans/round52_c2_registry.py`, `plans/round52-tasks.json`, `plans/round-52-claims.md`: 4 files
- `SKILL.md`: +28 lines, 0 deletions (registry rows)
- `LOG.md`: +10 lines (one D2 erratum block)

Commits (author `kengaku-shokunin`): `1315234` freeze, `07ea208` A1, `19bc16c` captures, `28c0018` wave-1 integration, `bfbcb07` exclusion, `87301ba` A5. The lane has no tracked modifications (`git status` shows only `??`).

Untracked (`git status --untracked-files=all`): 200 paths, including the 184-file duplicate (F1), `claims/*` receipts, `w2.ready*`, and wave-2 seat directories (F3).

Lane `.ufo/state/`: does not exist in this lane. Nothing was written under it.

Wave-1 contract note: `.ufo/waves/round-52/w1/C2ScribeRowsE/` has no `report.md` (its prose sits at `w1/C2ScribeRowsE.md`).

## Fleet root, sibling lanes, state, tmp, scratch

- **Fleet tracked files:** `git diff --stat HEAD` is empty for `MANIFEST.json`, `SCORECARD.md`, `LOG.md`, `scripts/`, `templates/`. `MANIFEST.json` (mtime 20:42:58) matches protocol ledger commit `33203a2b` (20:42:58, protocol-shokunin). `SCORECARD.md` (mtime 20:10:15) has no uncommitted diff. The last commits touching either file are protocol-shokunin ledger commits. **[INFERENCE]** these are the orchestrator's writes, not a seat's.
- **Fleet `.scratch/goal-20261028-hyaku-run11.md`:** tracked, uncommitted (+95/−4), mtime 20:40:16. **[INFERENCE]** orchestrator-maintained. No seat path reaches `.scratch/`.
- **Fleet `.ufo/state/`:** in-window appends by the orchestrator's daemons: `disk-guard.log` and `inline-dispatcher.log` (20:57:49), and `.ufo/watchdog.log` (20:54:51). The dispatcher's own lines name `kengaku/w2: live 25/33` and an ORPHAN ready for `kengaku-shokunin/.ufo/waves/round-50/w1.ready`, which are dispatcher observations. `mado.report-baseline` (18:36) and `tsukuroi.report-baseline` (17:40) belong to their lanes. No kengaku seat signature.
- **Fleet root untracked/staged leftovers (none from round 52 by timing):** `D=/` (created 12:07, before wave 1), staged intent-to-add `o.bin`, `oldrep1.out`, `oldrep2.out`, untracked `lane3/` (14:59), `.scratch/closure-r54/*` clones. `tools/` is an empty directory created 20:00:16. **Unattributable** (empty, untracked by git, no content). Recommend the orchestrator confirm whether it came from a tool install (tooling directive).
- **Sibling lanes:** many in-window writes in their own trees (kaidoku 4690, souji 2970, mado 2133, kama 1400, tsukuroi 486, kasegi 373, chousa 243, tameshi 216 files). A narrow probe for round-52 identifiers (`kengaku-r52`, `W2SentinelScope`, `kengaku-shokunin/.ufo/waves/round-52`, `kengaku/w2`) in sibling files modified in the window found 2 hits, both in kaidoku round-49 files (text mentions, not writes into kengaku). No sibling write is attributable to a kengaku seat.
- **`/tmp`:** in-window files are other lanes' or orchestrator's (`/tmp/have.txt`, `/tmp/census-*`, `/tmp/closure-kengaku-r51.json` pre-round, `/tmp/hyaku*`). None is named after a round-52 seat.
- **`~/.local/bin`:** nothing newer than `w1.ready`. No tool installs by this seat.
- **Scratch:** `/fast/scratch/hyaku/kengaku-r52/` is 3.1 GB, with ~25 `w2-*` seat dirs and L1 items (`lane`, `src`, `gh013`, `tb2-*.json`). `/fast` had 535 GB free. `gh013/test_outputs.py.excluded` is an exact copy of the excluded bytes in L1 scratch, outside the lane (it should be removed once the L1 is done with it).

## Commands (all read-only; no git/jj mutation)

- `git -C kengaku-shokunin status --porcelain` and `--untracked-files=all`; `git -C fleet status --porcelain`
- `git log`, `git ls-files`, `git grep --cached` (-c, -l, -o, -n), `git diff --name-only/--numstat/--stat` (base `30801b4`), `git for-each-ref --contains`, `git merge-base --is-ancestor`, `git log --all --find-object=…`, `git check-ignore`, `git show -s`
- `jj --version`; `jj --ignore-working-copy config list --repo` (read-only, no snapshot)
- `find … -newer kengaku-shokunin/.ufo/waves/round-52/w1.ready`; `ls -la --time-style=full-iso`
- `sha256sum -c SHA256SUMS`; `sha256sum` (digest check only, excluded file); `diff -rq` (duplicate vs corpus); `file --mime-type`
- `grep -c`/`-l`/`-o` (redacted via `sed`/`awk`: shape and length only)
- `curl -fsSL` × 3 raw captures at pin into scratch (removed)
- Python: read `plans/round52-tasks.json` key structure; `SHA256SUMS` line count
- No counter was run. No pacman, no install, no network push.

## Files produced

- This report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2SentinelScope/report.md`
- Scoped findings copy: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2SentinelScope.md`
- Scratch `/fast/scratch/hyaku/kengaku-r52/w2-W2SentinelScope/`: created for the curl spot-check, then removed (verified gone).

## Could not do

- Did not query the origin remote for whether `de616d7`/`cdc0d68` objects were ever pushed (`git ls-remote` shows refs only; no object-level check).
- Did not read `jj` operation-log authorship, since `jj op log` can snapshot. The `.jj/` writes in-window are attributed to the L1's lane-helper commits **[INFERENCE]** from timing, not verified.
- Did not verify the `W2RevEntryLesson/receipts/analysis.json` spec authorisation.
- Snapshot only: wave 2 was still writing when I scanned. Re-run F1/F3 after wave 2 settles.

## Request to the L1 (single integration owner)

1. Delete `.ufo/waves/round-52/w1/C1ExecFetchGraders/artifacts/graders/` (untracked duplicate; keep the committed `artifacts/SHA256SUMS`, `fetch_log.tsv`, `paths.txt`). Do not commit the excluded bytes in any form.
2. Do not `--all`/`--mirror` push, and keep `refs/jj/keep/*` (incl. `de616d7`, `cdc0d68`) out of any push.
3. Copy only spec-named receipts into the lane; leave the un-named wave-2 scripts and text receipts out of commits.
4. Consider redacting `/home/vgpnk` from orchestrator-written dispatch/run logs before they are committed.
