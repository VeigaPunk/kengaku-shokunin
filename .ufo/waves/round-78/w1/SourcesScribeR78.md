# SourcesScribeR78 — source-row and Gate drafts

Axes: coverage and calibration. Prose-only seat; no product changes, counter execution, commits, installs, publishing, or delegation.

## Draft registry rows (verbatim)

Each row uses the fleet `CORPUS.md:86-108` contract's 11 cells; no cell contains a pipe. These are integration drafts, not instructions to append duplicate ids: working-tree `corpus/SOURCES.md:270-271` already contained S254/S255 when inspected.

```text
| S254 | Git git-status documentation — https://git-scm.com/docs/git-status | docs | A | Git's documented untracked-file reporting options; not proof that a particular worktree is clean | --untracked-files[=<mode>], HTML capture lines 2320/2322/2326; fetched 2026-11-04; sha256 22ff28ff73f83696c4a503e9c92e7a15f4ded2f91d96cc5668ee79db0a1b0180 | Explicitly request untracked-file reporting when assessing cleanliness; tracked changes alone do not establish absence of untracked paths | mined | 2026-11-04 | on-release | corpus/lessons/round-78.md |
| S255 | Round-62 grader-class census receipt — corpus/evidence/round62/class-survey.txt | own-work | A | class membership counts of the committed grader population | f20a2f6fcceb6769b48109d57904f52376190e44:corpus/evidence/round62/class-survey.txt; CLASS lines 11,14,16 and EXECUTED-COVERAGE line 21; sha256 ee30c6984c13985fe3efaa2d81c908b915da0f178ce5ca267bc0f0a37cd45613 | Use named CLASS member lists to define the ledger universe; historical EXECUTED-COVERAGE totals do not establish current per-member replay evidence | mined | 2026-11-04 | 90d | corpus/lessons/round-78.md |
```

`own-work` is explicitly a listed kind in fleet `CORPUS.md:91-92`; repo paths are allowed sources at :90. Tier A is scoped, and includes the lane's own re-runnable gate output (:93-97). S255 is admitted only for the census's committed-population membership counts, not independent proof that its classifier is correct or that members were replayed. `mined` means cited by an existing used-by lesson (:103-108): the working-tree `corpus/lessons/round-78.md:13-25` explicitly cites both S254 and S255.

## Gate

- **S254 — admit, mined.** Opened https://git-scm.com/docs/git-status live on 2026-11-04. Fetch returned **HTTP 200**, **100062 bytes**, SHA-256 **22ff28ff73f83696c4a503e9c92e7a15f4ded2f91d96cc5668ee79db0a1b0180**. The option is at raw HTML line **2320**; the governing sentence is at **2322**: **“Show untracked files.”** (3 words). Additional located quote at :2326: “The mode parameter is used to specify the handling of untracked files.” The fetched capture and its `.sha256` file were saved under the seat scratch directory before cleanup. Existing lane capture `corpus/evidence/round78/sources/git-status.html` independently hashed to the same digest and had the same byte count; this seat did not write that lane capture. Docs also explain at :3162-3167 that the no flag/config suppresses untracked reporting. This is documentation evidence, not a worktree-clean execution test. Recheck on-release; used by `corpus/lessons/round-78.md`.
- **S255 — admit, mined.** Opened `corpus/evidence/round62/class-survey.txt` on 2026-11-04: **5528 bytes**, **24 lines**, SHA-256 **ee30c6984c13985fe3efaa2d81c908b915da0f178ce5ca267bc0f0a37cd45613**. Observed `CLASS network-service count=8` at :11, `CLASS process-environment count=3` at :14, `CLASS db-state count=2` at :16, and `EXECUTED-COVERAGE` at :21. Located quote (:21, 5 whitespace-separated words): **“EXECUTED-COVERAGE executed=17 classified=17 classes-covered=12 classes-uncovered=network-service,process-environment,db-state,container-image”**. Exact committed-byte command: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show f20a2f6fcceb6769b48109d57904f52376190e44:corpus/evidence/round62/class-survey.txt | sha256sum` → the full digest above, exit 0. Working-file `sha256sum` returned the same digest. Recheck 90d; used by `corpus/lessons/round-78.md`. No census counter rerun was performed.
- **Reject candidate — “a class count in a prose table is evidence of class membership.”** The frozen claims distinguish SKILL's prose counts from the census's actual `members=` lists. Counts do not identify members or demonstrate replay. **Flip:** enumerate membership from pinned committed grader bytes and reconcile every named member against the stored census/ledger, with detector-backed reasons or passing receipts as appropriate. Merely matching the aggregate number does not flip this rejection. This is a reject-with-flip Gate candidate, not a third registry row.

SOURCES: S254 mined, S255 mined

## Commands, provenance, and findings

Claims were read in full before the first shell command. Relevant skill read: `godspeed`.

Actual live-fetch command (including the separately fetched header observation):

```sh
S=/fast/scratch/hyaku/kengaku-r78/SourcesScribeR78; mkdir -p "$S" && code=$(curl -sSL -o "$S/git-status-doc.html" -w '%{http_code}' https://git-scm.com/docs/git-status) && echo "HTTP=$code" && echo "BYTES=$(wc -c < "$S/git-status-doc.html")" && sha256sum "$S/git-status-doc.html" && curl -sS -D - -o /dev/null https://git-scm.com/docs/git-status | sed -n '1,12p'
```

Outcome: HTTP=200; BYTES=100062; digest above; command completed successfully. The second request returned HTTP/2 200 and `last-modified: Mon, 02 Nov 2026 06:50:40 GMT`; those headers belong to the second request, not an atomically saved header/body pair.

Checksum artifact creation:

```sh
sha256sum /fast/scratch/hyaku/kengaku-r78/SourcesScribeR78/git-status-doc.html > /fast/scratch/hyaku/kengaku-r78/SourcesScribeR78/git-status-doc.html.sha256
```

Outcome: success, no stdout. Scratch was removed before yield under the mandatory scratch-cleanup rule; the report retains its observed digest, byte count, exact HTML line numbers and quote, not a claim that the scratch capture remains available.

Working census inspection command:

```sh
F=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round62/class-survey.txt; sha256sum "$F" && echo "BYTES=$(wc -c < "$F")" && echo "LINES=$(wc -l < "$F")"
```

Outcome: digest above, BYTES=5528, LINES=24. Specialized grep/read tools located the quoted lines. No counter was imported.

Read-only provenance commands used `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin`: `rev-parse master`, `rev-parse HEAD`, `status --porcelain`, `log -3 --format='%h %ad %s' --date=iso -- corpus/SOURCES.md`, `show master:corpus/SOURCES.md`, and `merge-base --is-ancestor 2f9eeafb master` / `merge-base --is-ancestor 3ae0ab54 master`. Both revisions were ancestors (exit 0); observed master/HEAD was `f20a2f6fcceb6769b48109d57904f52376190e44`. The saved master registry contained S250–S253; working-tree rows S254/S255 were additional. Status included modified `corpus/SOURCES.md`, modified `plans/round78_c2_stamp_location.py`, and untracked round-78 surfaces. This is an observation, not attribution of those edits to an actor.

**Finding: S255's observed working-tree anchor is wrong.** It says verbatim `corpus/evidence/round62/class-survey.txt lines 1-9 (\`CLASS … members=\`, \`EXECUTED-COVERAGE …\`)`. The partial-class records are at 11/14/16 and EXECUTED-COVERAGE is at 21. Reproduction: specialized grep over the census using `^(CLASS (network-service|process-environment|db-state)|EXECUTED-COVERAGE)` produced those four line numbers. The draft above supplies the correct anchor. Since registry corrections are append-only under fleet `CORPUS.md:116-118`, L1 must decide integration based on whether these in-flight draft rows have been admitted; this seat did not alter them or allocate a replacement id.

Corrections to interim narration: CORPUS.md was absent only from the lane, not unavailable; the canonical file is `/home/vgpnk/Projects/shokunin/CORPUS.md` and its contract was read. The claim that a recheck cell changed concurrently is not established by stable snapshots; latest raw observed S255 had `90d`. Claims about who appended the rows were inference, not execution evidence. Earlier speculation about master's S25x population was superseded by the saved master-file grep showing S250–S253.

Touched durable surface: only `.ufo/waves/round-78/w1/SourcesScribeR78.md`. Scratch surfaces: fetched HTML, checksum file, and read-only master registry export (all removed). Existing sources, lesson, claims, and census files remained read-only.

Out of scope: C1/C2 verdicts, source-census validation, registry landing/correction, judge execution, product changes, and commits. No tools installed. Method deviation: early shell commands used sed for output slicing and grep for a count; these were observational only, but did not follow the specialized search/paging preference. No peer messages or dispatches occurred.

Self-evaluation: accuracy 4/5 (mutable working-tree provenance remains a limit); completeness 4/5 (raw scratch capture deliberately removed by rule); clarity 4/5 (command audit adds length); actionability 4/5 (anchor correction requires L1 integration); conciseness 3/5 (audit trail is longer than the requested rows). Overall 3.8/5. Highest-impact improvements applied: located canonical fleet contract, corrected S255 line anchors, and separated observed facts from actor/concurrency inference. User-agreement check: deliverable covers all requested draft/Gate fields without claiming counter execution.
