# R29a2ScopeSentinel — write-scope and credential audit (kengaku round 29, attempt 2)

Seat: leaf sentinel, report-only (deleted nothing, edited nothing outside this file).
State pinned: **2026-10-25 03:49:44 -0300**, lane HEAD `8cf7b60` (entry + gate committed at ~03:49; the
round was still writing while I audited — see §4 finding 2).

Axes named: (a) **coverage** — every path any of the three `git status` calls, a nested-repo sweep and a
committed-blob read can see is classified; (b) **operability** — each verdict carries the command that
produced it, and the two blind spots that would make a naive rerun miss a violation are named.

Verdict vocabulary: **mine** = written by this kengaku round-29 lane; **another lane's** = another
lane's own round/lane activity; **runtime** = hyaku/harness/git machinery, not a lane seat;
**pre-existing** = neither — dated before this round started (round launch `2026-10-25T03:31:56`, `.ufo/watchdog.log:1261`).

## 0. Headline

- **No kengaku round-29 write exists outside `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.** Every
  in-window path found outside the lane is another lane's own round or harness machinery (§1b–§1d).
- **`/home/vgpnk/Projects/shokuknow` is untouched** by this round (§3): its `.git/index` mtime is still
  `2026-10-24 23:33:24`, its newest non-`.git` file older than midnight except one tabi-owned TSV, and
  the C1 source object is tracked and clean.
- **Credential scan: 0 hits, all classes.** 0 provider-token, 0 private-key, 0 URL-userinfo, 0
  `key=value` secret assignment, 0 cookie value, across 4 named targets plus the newly admitted entry
  and all 40 committed attempt-2 blobs. No value is reproduced in this report.

## 1. Path list with per-path verdict

### 1a. Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin` — verdict: **mine**

`git -C .../kengaku-shokunin status --porcelain` was read three times; it moved from 4 to 17 to 7
entries because seats were landing and then committing (§4 finding 2). Union of all three reads:

| Path | Verdict | mtime / evidence |
|---|---|---|
| `corpus/knowledge/benchmark-task-validity-checklist.md` | mine | new, 03:47:04→03:48:03; committed in `8cf7b60` |
| `corpus/SOURCES.md` | mine | M, 03:47:04 (still M at 03:49:44) |
| `corpus/README.md` | mine | M, 03:45:53 |
| `corpus/lessons/round-29.md` | mine | M, 03:47:36 |
| `corpus/evidence/round29-attempt2/adoption-gate-run.txt` | mine | 03:46, 118 B, committed |
| `corpus/evidence/round29-attempt2/census-before.txt` | mine | 03:46, 1416 B, committed |
| `corpus/evidence/round29-attempt2/census-after.txt` | mine | 03:48, 1416 B, committed |
| `corpus/evidence/round29-attempt2/gate-selftest.txt` | mine | 03:48, 337 B, committed |
| `corpus/evidence/round29-attempt2/adoption-measured.txt` | mine | 03:48, 83 B, committed |
| `plans/sources_adopt.py` | mine | 03:47:17, 17823 B (still M at 03:49:44) |
| `plans/adoption_check.py` | mine | 03:47:54, 4549 B, committed |
| `plans/round-29-attempt2-claims.md` | mine | 03:47:04, 6558 B, committed |
| `.ufo/waves/round-29/attempt2/adoption-expect.json` | mine | 03:38, committed |
| `.ufo/waves/round-29/attempt2/control.nothing.txt` | mine | 03:39, committed |
| `.ufo/waves/round-29/attempt2/package-gate.txt` | mine | 03:39, committed |
| `.ufo/waves/round-29/attempt2/build-spec.json` | mine | 03:40, committed |
| `.ufo/waves/round-29/attempt2/build-dispatch.json` | mine | 03:40, committed |
| `.ufo/waves/round-29/attempt2/build-validation.txt` | mine | 03:40, 0 B, committed |
| `.ufo/waves/round-29/attempt2/build-registry-record.txt` | mine | 03:42, committed |
| `.ufo/waves/round-29/attempt2/adopt-block.md` | mine | 03:45, committed |
| `.ufo/waves/round-29/attempt2/adoption-measured.txt` | mine | 03:46, committed |
| `.ufo/waves/round-29/attempt2/gate-preappend.txt` | mine | 03:46, committed |
| `.ufo/waves/round-29/attempt2/gate-postappend-rerun.txt` | mine | 03:46, committed |
| `.ufo/waves/round-29/attempt2/build/` (30 files, `R29a2*.md` seat reports + `swarm-registry.json`) | mine | 03:38–03:49; 40 attempt-2 blobs total in `HEAD` |
| `.ufo/waves/round-29/attempt2/build/R29a2GateAudit.md` | mine | new, untracked at 03:49:44 |
| `plans/__pycache__/*.pyc` (2 files, ignored) | mine | bytecode from seats running the two tools; in-lane, ignored |
| `.jj/`, `.ufo/interactive-sessions/` (ignored) | runtime | pre-existing VCS/harness dirs, not round writes |

### 1b. Fleet root `/home/vgpnk/Projects/shokunin` — 33 porcelain entries, **none** mine

| Path | Verdict | Evidence |
|---|---|---|
| `.ufo/state/*.report-baseline` (12 M + 3 ?? = 15) | runtime | hyaku baselines; `.ufo/state/kengaku.report-baseline` = `29 e41fd937…` (round launch record), mtime 03:31:54 |
| `.ufo/watchdog.log` | runtime | 44 kengaku hits, all `launch`/`complete` lines, e.g. `:1261 2026-10-25T03:31:56-03:00 launch kengaku round=29` |
| `scripts/hyaku/hyaku.env`, `scripts/hyaku/lane-addendum.md` | runtime | 03:22–03:23, before round launch; `lane-addendum.md:291` is a schema note naming the kengaku package |
| `.scratch/goal-20261025-hyaku-12h.md` | runtime | 03:34:00, 0 kengaku/round-29 refs |
| `.ufo/reports/round-22/souji.md` | **another lane's** | 03:45:55; diff is souji's own round-22 attempt-2 rewrite; 0 kengaku refs |
| `.omp/mcp.json`, `bm.json`, `live.html`, `live_s228.html`, `nama.html`, `s395.txt`, `tf_bavelas.html`, `unblob.log`, `wb2.html`, `write`, `xc.xml`, `mikeseven_pkg.json` | pre-existing | all mtime `2026-10-24 18:07:20`, before launch; 0 kengaku/round-29 refs |
| `scripts/hyaku/append-closure.py.bak-20261023T040735Z`, `scripts/hyaku/fleet-commit.sh.bak-20261023T040735Z` | pre-existing | dated 2026-10-23 |
| `MANIFEST.json` | runtime | mtime 03:33:51 but `git diff` empty and absent from status → rewritten byte-identical, 0 content change |
| `.git/`, `.git/index` | runtime | index mtime 03:49:56 = stat-cache refresh from the status reads this audit and its peers ran; no content write |

### 1c. `/home/vgpnk/Projects/shokuknow` — 1918 porcelain entries, **none** mine

| Path | Verdict | Evidence |
|---|---|---|
| all 1918 status entries (`lanes/…`, `merge/…`, `.ufo/waves/corpus-expansion-1/…`, `MANIFEST.json`) | pre-existing | 0 files under this root have mtime `>= 2026-10-25 00:00` except the one below |
| `lanes/tabi/round8/.work/ratelimit-series.tsv` | **another lane's** | mtime advanced 03:46:10 → 03:48:10 while I watched; content is tabi's `iso_utc/limit/remaining/used/reset_epoch` rate-limit series; 0 kengaku/round-29 refs |
| `merge/kengaku/**` (incl. C1 object `benchmark-task-validity-checklist.md`) | pre-existing | newest mtime in the whole subtree `2026-10-24 23:33`; C1 object tracked and clean at commit `d9583b5a` |
| `.ufo/waves/corpus-expansion-1/{renumber-staged,merge-plan,quote-lint,absent-defect-register,audit-wave,build-wave3}.py` | pre-existing | mtimes 2026-10-23 20:31 … 2026-10-24 23:30 — none touched in the window |
| `.git/index` | — | mtime unchanged `2026-10-24 23:33:24` across my read-only status call |

### 1d. Nested lane repos (invisible to fleet `git status` — see §4 finding 1)

`.gitignore:1` is `*-shokunin/`, so the 20 sibling lane checkouts under the fleet root are excluded from
the fleet-root status above. Swept with `find … -newermt "2026-10-25 03:30"`: **904 candidate files**
across 12 sibling repos, every one inside its own repo's own round (kake r51, kotodama r69, mado r35,
revenger r68, souji r22-attempt2, tabi, tameshi r41, kagi, kasegi, …). Verdict: **another lane's**.

Decisive cross-product (`grep -i kengaku` AND `grep -iE 'round-29|round29'`): exactly **1** file —
`revenger-shokunin/.ufo/waves/round-68/R68ConnectorOverlap.md:36` = `kengaku-shokunin         0`, i.e.
revenger's own overlap counter recording *zero* kengaku commits. No kengaku seat wrote into a sibling.

## 2. Credential scan — count and class, no values

Pattern classes searched (`grep -coiE`, count only, values never emitted): `ghp_/gho_/github_pat_`,
`AKIA/ASIA`, `xox[baprs]-`, `sk-…`, JWT `eyJ….…`, `-----BEGIN … PRIVATE KEY-----`, URL userinfo
`scheme://user:pass@host`, and `api_key|access_token|secret_key|password =/ :` assignments.

| Target | mtime / size | hits | keyword mentions |
|---|---|---|---|
| `plans/sources_adopt.py` | 03:47:17, 17823 B | **0** | 0 token, 0 credential |
| `plans/adoption_check.py` | 03:47:54, 4549 B | **0** | 0 token, 0 credential |
| `plans/round-29-attempt2-claims.md` | 03:47:04, 6558 B | **0** | 1 "credential" (prose: "credential-copy disposition") |
| `corpus/knowledge/benchmark-task-validity-checklist.md` (new entry) | 03:48:03, 8630 B | **0** | 0 |
| `.ufo/waves/round-29/attempt2/` (39 files on disk, 40 committed) | — | **0** | 47 "token", 2 "cookie" |
| committed blobs of `corpus/{SOURCES,README}.md`, `corpus/lessons/round-29.md` | `HEAD` | **0** | — |

Class breakdown of the 47 "token" / 2 "cookie" / 7 "credential" keyword mentions (they are **not**
findings, and I checked each context): (i) whitespace-token *word-count* prose in reviewer reports
(`"whitespace-split token counts"`, `"pipe delimiters are separate whitespace tokens"`); (ii) the
dispatch prompt text embedded in `build-spec.json` / `build-dispatch.json`, which contains the audit
*instruction* words ("cookies", "credential-shaped"); (iii) two quoted primary-document lines —
`"no registry credentials"` and a rejected-claim row about "credential remediation"; (iv) the claims
file's historical note about the operator holding attempt 1 on "credential-copy disposition".
None carries a value, a length, a prefix or a fingerprint.

Entropy pass: every ≥40-character `[A-Za-z0-9+/]` run in the target set is either a 40-hex commit id
(`1f3b0f1e…`, `2fd12b88…`, `d7149606…`) or a filesystem path (`/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES`,
`bench/<40-hex>/docs/TASK`). Zero random-looking secret-shaped strings.

Host inventory over the same set (public sources only, no internal hosts, no userinfo):
`aclanthology.org, api.github.com, arxiv.org, betterbench.stanford.edu, codeload.github.com, example.invalid,
github.com, huggingface.co, inspect.aisi.org.uk, jpn.nec.com, neurips.cc, openreview.net, oxrml.com,
proceedings.iclr.cc, raw.githubusercontent.com, uiuc-kang-lab.github.io, ukgovernmentbeis.github.io,
web.archive.org, www.meti.go.jp, www.tbench.ai`. `example.invalid` is the RFC 2606 placeholder, not a
reachable endpoint.

## 3. Source repo untouched — explicit statement

**`/home/vgpnk/Projects/shokuknow` was not written, committed, fetched or pushed by this round, and not
by me.** Evidence: (a) `git -C .../shokuknow status --porcelain` shows the same 1918-entry backlog as
before the round, none of it naming kengaku round 29 (§1c); (b) `.git/index` mtime is still
`2026-10-24 23:33:24` — unchanged before and after my read-only status call; (c) the newest file
outside `.git` other than tabi's live TSV is dated `2026-10-24`; (d) `HEAD` is `8b94c5c1 "Stage wave 13…"`,
reflog top entry has no round-29/kengaku commit; (e) none of the four campaign tools that write there
(`renumber-staged.py`, `merge-plan.py`, `quote-lint.py`, `absent-defect-register.py`) changed mtime in
the window. No campaign tool was executed by any seat — two seats state this in their own reports
(`build/R29a2RevQuoteS090.md:221`, `build/R29a2RevQuoteS078.md:140`).

## 4. Blind spots / operability findings (each rerunnable)

1. **The audited command set cannot see sibling lanes.** Fleet `.gitignore:1` = `*-shokunin/`, so
   `git -C /home/vgpnk/Projects/shokunin status --porcelain` omits all 20 nested lane repos
   (`git check-ignore -v kengaku-shokunin` → `.gitignore:1:*-shokunin/`). A round-29 seat writing into
   e.g. `mado-shokunin/` would have been invisible to the two fleet-level status calls the ticket
   specifies. The §1d `find -newermt` sweep (904 files) is what closes this; recommend it as the
   standing form of this check, or per-repo `git status` over `*-shokunin`.
2. **A single status snapshot under-reports a live round.** My three reads saw 4 → 17 → 7 entries in
   ~11 minutes because seats landed C1/SOURCES/lessons/evidence at 03:45–03:48 and committed `8cf7b60`
   at ~03:49. Any scope verdict taken mid-flight is stale; this one is pinned at 03:49:44 and its path
   list is the union of all three reads.
3. **mtime is not write-evidence on its own.** Fleet `MANIFEST.json` has mtime 03:33:51 today yet is
   byte-identical to `HEAD` (`git diff --stat` empty, absent from porcelain) — a rewrite with identical
   content. Conversely a content write can be mtime-preserved (`cp -p`), which is why §1c also greps
   content and reads `git log`, not just mtimes.
4. **Advisory, not a violation:** one seat fetched a page to `/tmp/keng_s091.html`, outside the
   `/tmp/r29a2-<name>/` scratch convention (`build/R29a2QuarS091.md:91`). The file no longer exists
   (the same report records its absence at `:123`), `/tmp` is not a protected tree, and no credential
   shape was found while it existed. The convention held for the other 35 `/tmp/r29a2-*` dirs.
5. **In-lane stray artifacts:** `plans/__pycache__/{sources_adopt,adoption_check}.cpython-314.pyc` and
   the `.jj/` ignored dir are untracked/ignored and never reached `HEAD`; no action needed beyond
   noting they are the only non-corpus side effects of tool runs.

## 5. Limits — what I did not verify

- I did not judge, integrate or score the round, and did not re-run any campaign tool or any of the
  lane's gates; claim-level correctness (C1 target line, C2 ten PASS cases) is other seats' surface.
- The credential scan is pattern- and entropy-based plus context reading; it does **not** prove the
  absence of a secret that matches no known shape (e.g. an unlabelled high-entropy value shorter than
  40 chars, or a secret inside a fetched page that never reached the lane).
- The sweep window is `mtime >= 2026-10-25 03:30`; a write with a deliberately preserved older mtime is
  outside what mtime can catch. Content greps cover the two protected roots only, not all 20 siblings.
- Scratch dirs under `/tmp/r29a2-*` were not audited for credential content beyond the S091 file.

Tooling: no installs or upgrades performed (no pacman/uv/npx/cargo action was needed), so the PACMAN
GUARD was not engaged.
