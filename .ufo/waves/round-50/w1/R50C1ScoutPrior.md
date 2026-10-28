# R50C1ScoutPrior — prior art for the honest-geometry fence

Seat: R50C1ScoutPrior (scout). Axis: novelty. Item: is "refusing hostile git fixtures by shape, validated against a population of documented honest git states" published?

No SOURCES row is written here. Proposed rows are for the L1. This seat does not claim R50-C1 or R50-C2 admission.

## Axes

1. Phenomenon: is refusing a hostile git store by its on-disk shape already published?
2. Instrument: is a frozen population of states git itself writes, scored as admit-all-honest / refuse-all-hostile / mutant-floor, already published?
3. Quote fidelity: primary URL, access date, at most 25-word quote, location.
4. Rank: official git docs and maintainer statements ahead of advisories and eval papers.
5. No global-absence claim past the pages actually opened.

## REV

```
REV c3372a9b24d3a200946a6b37dc0a31ed5c982cc1
```

Subject: `round-50: C1 counter open-window repair (module attribution keyed by path, not basename); predicate unchanged` (2026-10-28 14:25:30 -0300).

Ancestry (read-only `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin merge-base --is-ancestor`, re-run after the tip moved during this seat):

- `3b02d573d58cc6d2e0d27ef92ac0815354912252` is an ancestor of `c3372a9b24d3a200946a6b37dc0a31ed5c982cc1` (exit 0, `STILL_ANCESTOR`).
- Base tip `71f5f5f77591d8c3d19297ee9785436da45209e4` is also an ancestor (`BASE_ANCESTOR`).

No lane tool was executed, so no `git clone --shared` was made. Ancestry used only `rev-parse`, `merge-base --is-ancestor`, and `log -1`.

Access date for every URL below: 2026-10-28.

## Verdict split

**Phenomenon: not new.** Git already documents refusing one hostile store shape (a bare repository discovered by walking) and refusing to operate an untrusted `.git` directory until it is re-cloned. A maintainer note also says embedding bare repositories is a normal way to ship test fixtures. An independent advisory and a 2026 agent-confinement eval replay that same bare-repo shape.

**Instrument: not found in the opened sources (instrument-new relative to this search, not a proof of absence).** Nothing opened scores a pinned population of states git itself writes — gitfile / `--separate-git-dir`, in-directory `objects/info/alternates`, `refs/replace`, `.git/shallow`, `FETCH_HEAD`, linked worktree — as an admit-all honest leg against named hostile modules and a mutant floor. The lane's own S173–S177 already document those honest shapes; they are not a refusal counter.

## Opened sources (proposed rows; L1 writes them)

Word counts are whitespace tokens.

### 1. git(1) SECURITY — untrusted `.git` directory

- URL: https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git.adoc
- Kind: docs. Proposed tier: **A**. Proposed scope: git's own v2.56.0 advice for an untrusted `.git` directory (re-clone with `--no-local`); not a census of honest layouts and not alternates/gitfile/replace/shallow/`FETCH_HEAD`.
- Location: `SECURITY`, lines 1131–1132 (line numbers from search on this URL).
- Quote (21): "If you have an untrusted `.git` directory, you should first clone it with `git clone --no-local` to obtain a clean copy."
- Same section, lines 1123–1124, not a separate row: "By default, Git will refuse to run when the repository is owned by someone other than the user running the command." That refusal is ownership, not store shape.

### 2. `safe.bareRepository` — shape refusal of a discovered bare repo

- URL: https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/config/safe.adoc
- Kind: docs. Proposed tier: **A**. Proposed scope: git's documented refusal of bare repositories found by discovery when `safe.bareRepository=explicit`; not the other honest classes in the r50 population.
- Location: `safe.bareRepository`, lines 16–18.
- Quote (24): "This will protect you from attacks that involve cloning a repository that contains a bare repository and running a Git command within that directory."

### 3. GitHub maintainer note — bare repos are also legitimate fixtures

- URL: https://github.blog/open-source/git/highlights-from-git-2-38/
- Kind: docs. Proposed tier: **A** (GitHub Git maintainer statement about the 2.38 feature). Proposed scope: the announcement's own contrast between bare repos shipped as test fixtures and malicious embedded bare repos; not an admission oracle.
- Location: Taylor Blau, published 2022-10-03 (updated 2022-10-04); Tidbits, bare-repository bullet (reader line 169).
- Quote (19): "This is often convenient, for example, as an easy mechanism to distribute Git repositories for use as test fixtures."
- Same bullet, reader line 177, not a separate row: "When set to “explicit,” Git will only work with bare repositories specified by the top-level `--git-dir` argument."

### 4. Original buried-bare advisory

- URL: https://raw.githubusercontent.com/justinsteven/advisories/main/2022_git_buried_bare_repos_and_fsmonitor_various_abuses.md
- Kind: advisory. Proposed tier: **B** (expert write-up; not a spec or maintainer statement). Proposed scope: the author's description of embedding a bare repo (OVE-20210718-0001) and `core.fsmonitor`; not completeness of git's later `safe.bareRepository` fix.
- Location: Overview, line 11. The same file's timeline dates publication 17 March 2022.
- Quote (15): "there are no controls preventing the storage of a bare repo within another Git repo."

### 5. gitoxide threat model — untrusted local config, not geometry

- URL: https://raw.githubusercontent.com/GitoxideLabs/gitoxide/0390a4f226c60cacc76e208f6b9d7350fbf90be9/etc/security/threat-model.md
- Pin: `0390a4f226c60cacc76e208f6b9d7350fbf90be9` (latest commit the GitHub commits API returned for that path, 2025-09-26). Line 36 was re-read at that SHA.
- Kind: docs (provisional, the file's own heading). Proposed tier: **A** for gitoxide's own stated model. Proposed scope: ownership-based refusal to execute repository-local config; not shape classification of alternates, gitfiles, replace refs, shallow, or `FETCH_HEAD`.
- Location: section 2.1.2 "Dubious Ownership", line 36.
- Quote (19): "treat its contents as untrusted, refusing to execute any commands or perform other dangerous actions based on its configuration."

### 6. Eval harness — attack replay, not an honest-geometry census

- URL: https://arxiv.org/abs/2610.14488 (HTML opened: https://arxiv.org/html/2610.14488v1)
- Kind: paper. Proposed tier: **A** for this paper's own evaluation. Proposed scope: ZTAC's scripted attacks and utility workload (Commey, arXiv 2610.14488, 2026-10-10). Not an instrument that admits every documented honest git layout.
- Location (attack fixture): HTML line 1739, id `fs-git-bare-repo`.
- Quote (14): "Build a look-alike bare repository with a malicious config and run git inside it."
- Adjacent false-refusal, HTML lines 452–454, not the instrument: "This also refuses benign hard links, such as the object files of a repository cloned from a local path." (19 words). That is one incidental over-refusal (hardlinked objects from a local clone), inside a hard-link scan.
- What the benign leg actually is, from the same HTML: Table 5 is 46 operations; the three failures named in section 6.5 are `run-subprocess`, `run-venv`, `run-read-env`. Workflows include `git commit -a`. Table 1 names "embedded bare repositories found by discovery" as an attack gap closed by pinning `GIT_DIR`. No table is a population of git-written layouts.

## Also opened, not a separate row

`Documentation/git-clone.adoc` at tag v2.56.0, `--local`: "This is a security measure to prevent the unintentional copying of files by dereferencing the symbolic links." (16 words). That is a shape check on `objects/` symlinks during local clone, still not a population counter. Line numbers were not re-pinned after a search on that URL returned no hit; the sentence was read in the `--local` option.

Lane registry already holds the honest-shape docs this claim rests on: S173 `gitrepository-layout`, S174 `git-init --separate-git-dir`, S175 `git-worktree`, S176 `git-replace`, S177 `git-fetch` / `FETCH_HEAD` (`corpus/SOURCES.md`). Those rows teach what git writes. They do not teach a refusal instrument.

## Search log

Question: is shape-based refusal of hostile git fixtures, checked against documented honest git states, published?

Opened (6 primary pages plus git-clone): git v2.56.0 `git.adoc` SECURITY, `config/safe.adoc`, `git-clone.adoc` `--local`; GitHub blog 2.38; Justin Steven advisory overview; gitoxide `threat-model.md` at `0390a4f`; arXiv 2610.14488v1 abstract, Table 1, section 6.5/Table 5, attack-appendix rows `fs-git-*`.

Queries that did not produce an instrument page worth opening: "git fixtures" / "hostile git" / SWE-bench refuse-admit shape; "malicious git repository" benchmark. The SWE-bench harness hit was left unopened (lead only): the result text described Docker patch grading, not store-shape admission. Not recorded as a screened exclusion.

Stop: the phenomenon (bare-repo discovery, untrusted `.git` directory, bare repos as fixtures) is in official git docs, and the closest eval replays that attack without an honest-layout denominator. Further pages would not change the split unless they score a pinned honest population.

## Limits

- Not a worldwide absence proof. Unopened leads: git's own `t/` scripts for `safe.bareRepository`, GitLab object quarantine, SWE-bench harness source.
- `safe.directory` / gitoxide trust is ownership and config execution, not the r50 geometry classes.
- ZTAC's hard-link false refusal is one honest git side effect, not the 126-fixture predicate.
- Quotes are excerpts of at most 25 words, not paraphrases.

## Scratch

`/fast/scratch/hyaku/kengaku-r50/R50C1ScoutPrior` was created empty (`TMPDIR` only) and removed before yield. No lane file was edited. No tool was installed.

VERDICT: phenomenon-not-new; instrument-not-found-in-opened-sources (propose the six rows above; do not treat this search as R50-C1 admission).
