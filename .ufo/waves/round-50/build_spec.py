#!/usr/bin/env python3
"""Render the frozen round-50 v2 wave specification; no seat dispatch and no lane edits."""
import json
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
WAVE_DIR = LANE / '.ufo/waves/round-50'
OUT = WAVE_DIR / 'w1-spec.json'
FREEZE = '3b02d573d58cc6d2e0d27ef92ac0815354912252'
BASE = '71f5f5f77591d8c3d19297ee9785436da45209e4'
GODSPEED = '''/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.'''

context = f'''# Goal
kengaku round 50 (hyaku run 11), ONE v2 build-and-attack wave, lane repo {LANE}. Base lane tip: {BASE}; the stage-1 freeze (instrument + 126-fixture honest population + controls) is commit {FREEZE}. The frozen claims live at {LANE}/plans/round-50-claims.md — read it in full first; it binds every seat. Two claims: R50-C1 (novelty — an honest-geometry instrument for the fixture fence: `plans/round50_c1_verify.py` over a frozen 126-fixture honest population, 20 frozen refusal modules, 12+blind sealed modules and a mutant floor, plus the fence repaired so it passes) and R50-C2 (calibration — every artifact pointer in SCORECARD.md/SHONEN.md/PROVINCE.md resolves, counted by `plans/round50_c2_audit.py`). The L1 owns the canonical planner seat and is the single integration owner.

# Measured state you must start from (do not re-derive, but do re-run when your item says so)
- Base fence `plans/fixture_fence.py` sha256 05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e.
- Counter on the base fence: `HONEST fixtures=126 admitted=113 refused=13`; REFUSALS 20/20; SEALED 12/12.
- The five honest classes the base fence refuses: `n17-replace-ref` (refs/replace), `n18-shallow-fetch` (FETCH_HEAD), `n20-linked-worktree` and `n21-separate-gitdir` (a `.git` FILE naming a store), `n22-alternates-in-d` (`objects/info/alternates` naming a store inside d).
- `plans/honest50/population.txt` is pinned (`b5197f94…`, 126 rows); `python3 plans/round50_c1_verify.py --lane . --skip-mutants` is the fast leg check (mutant leg is slow and mostly pointless on a control).
- The carried r49 mutant battery `plans/mutants50/c1-mutants.json` (23 inline diffs against the r49 candidate fence) is a CANDIDATE only: on the base fence 4 of 23 change the verdict vector. Your job where named is to re-derive it with WITNESSED kills (QUALITY Q38).

# Routing
Route through the host route table only; the role decides the route. NEVER pass a model, NEVER name or record a model alias in any artifact.

# Tooling authorization (operator, 2026-10-19): you and every seat may install/upgrade tools that help the task; first read /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate; record tool/version/channel/reason). PACMAN GUARD (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via `uv tool`/`npx`/an official binary in ~/.local/bin, or file an L0 question; never run pacman -S/-Sy/-Syu/-U/-R.

# Scratch discipline (operator directive 2026-10-25, binding)
Scratch root for this wave: /fast/scratch/hyaku/kengaku-r50/<seat-name>/ (NVMe). mkdir -p it, export TMPDIR there, `trap 'rm -rf -- "$S"' EXIT` and REMOVE your scratch dir before you yield (copy receipts into your wave report dir first). /tmp is for files under 50 MB only. One live clone per seat (`git clone --shared`); never a full mirror of the lane. No committed tool may hardcode /tmp; pass `--work "$S"`. Anything a report must cite lands in the wave dir or the lane tree — /tmp paths are never citable evidence.

# Environment hygiene (round-50 incident)
NEVER `export GIT_CONFIG_GLOBAL`, `GIT_CONFIG_NOSYSTEM`, `GIT_AUTHOR_*` or `GIT_COMMITTER_*` into a shared shell: the host's git credential helper lives in the global config and a leaked `GIT_CONFIG_GLOBAL=/dev/null` makes every push fail with an opaque error. Set fixture git env per command (`env VAR=… git …`) or inside a subshell only.

# Write scope and bounds
Seats are READ-ONLY against the lane except: (a) your own report file at the absolute path named in your item (under {LANE}/.ufo/waves/round-50/w1/), and (b) scratch-only candidate code inside your scratch dir — transcribe the deliverable into your report or a file in your wave dir when your item says so. NEVER edit production files (plans/*, corpus/*, SCORECARD.md, LOG.md, SKILL.md, PROVINCE.md), never commit, push, stash, checkout or run a mutating git/jj command anywhere, never touch sibling repos, the fleet repo, MANIFEST.json, .ufo/state or .scratch/. Do not share writer paths with other seats; the L1 is the only integrator. Every git fixture call uses `git -C "$D"` with D inside your scratch and verifies `git -C "$D" rev-parse --show-toplevel` equals `$D` before writes. If you test the lane's tools, run them against a `git clone --shared` of the lane at {FREEZE} and never against the live checkout.

# Reports
Your item names an absolute report path; the file MUST exist when you yield — a settled seat with no report file is a routed defect (write your last state into the file if you run out of room). Every `Report:` trailer path printed by tooling is relative to {LANE} — write it at {LANE}/<that path>. Your report must state: axes named, exact commands run, observed outputs (verbatim where they are evidence), the revision measured (a `REV` line for receipts), limits, and a `VERDICT` line. A seat that ends with its scratch tree still on disk reports that as a defect of its own. Never claim R50-C1/R50-C2 admission and never write to SCORECARD/LOG/corpus.'''

items = []


def add(name, role, axis, claim, kind, detail):
    scratch = f'/fast/scratch/hyaku/kengaku-r50/{name}'
    report = f'{LANE}/.ufo/waves/round-50/w1/{name}.md'
    item = f'''{GODSPEED}

# Target
kengaku round 50 seat {name} ({role}), serving {claim} ({axis}).
# Item
{detail}
# Evidence and boundaries
Read {LANE}/plans/round-50-claims.md first (frozen predicates, controls, kill rules, open-window rule). Do only this named item. Verify the freeze commit {FREEZE} is an ancestor of the lane tip before any measurement and record the revision you measured. Work read-only against a `git clone --shared` of the lane, except scratch candidate code and your own report/receipt. Unique scratch: {scratch}; mkdir it, export TMPDIR={scratch}, `trap 'rm -rf -- "$S"' EXIT`, remove it before you yield. Report path (MUST exist at yield): {report}.'''
    items.append({'name': name, 'role': role, 'axes': [axis], 'item': item,
                  'milestone': 'kengaku r50 C1 honest-geometry instrument + fence repair; C2 pointer audit'})


# ---------------- R50-C1 (novelty) ----------------
c1_build = [
 ('C1ExecRepair', 'executor',
  'apply the five-class repair to `plans/fixture_fence.py` as a scratch candidate: (1) `.git` FILE whose `gitdir:` target resolves INSIDE d becomes an extra collected store (its seconds line may name `commondir`, also resolved inside d) instead of a blanket refusal; (2) `objects/info/alternates` is admitted only when EVERY line resolves inside d (relative entries resolve against the objects dir); (3) `.git/FETCH_HEAD` is an allowlisted entry (content never read); (4) ref namespace `refs/replace/<40hex>` is admitted (any other `refs/*` name stays refused); (5) every existing refusal path stays closed (out-of-d gitfile, out-of-d alternates, `[include]`, `commondir` outside, symlink, hardlink, mount cross). Transcribe the FULL candidate to `{L}/.ufo/waves/round-50/w1/C1ExecRepair/fence_candidate.py` and report the diff against the base fence. Measure with `python3 plans/round50_c1_verify.py --lane . --skip-mutants --fence <candidate>` on a clone at {F}: report HONEST/REFUSALS/SEALED verbatim.'),
 ('C1ExecRepairB', 'executor',
  'build a SECOND, independent repair candidate that reaches the same honest result by a different mechanism (e.g. a "resolve-then-classify" pass that first normalises every pointer to a real path, then classifies store bytes) — do not read C1ExecRepair\'s report. Transcribe to `{L}/.ufo/waves/round-50/w1/C1ExecRepairB/fence_candidate_b.py`; measure the same four legs. Its purpose is to tell the L1 which repair is smaller and safer; state which and why.'),
 ('C1ExecGitfile', 'executor',
  'prove the gitfile/commondir legs on their own against the candidate at `{L}/.ufo/waves/round-50/w1/C1ExecRepair/fence_candidate.py`: build (a) n21 separate-gitdir honest, (b) n20 linked-worktree honest, (c) gitfile pointing OUTSIDE d (must refuse), (d) gitfile naming a second gitfile (must refuse), (e) commondir relative escaping d (must refuse), (f) gitfile with `\\r`, BOM, trailing junk, absolute path inside d (decide and justify per case). Emit a case table with exit/verdict.'),
 ('C1ExecAlternates', 'executor',
  'prove the alternates leg: (a) relative alternates inside d honoured, (b) absolute alternates inside d honoured, (c) one line outside d refused, (d) chained alternates (A borrows B borrows C, all inside) — state the decision and whether a cycle is refused, (e) alternates entry with `..` climb that lands inside d vs outside, (f) `http-alternates` stays refused. Emit the case table against the candidate fence.'),
 ('C1ExecRefs', 'executor',
  'prove the ref-namespace leg: `refs/replace/<40hex>` admitted (it names an object, never a path), `refs/replace/<non-hex>` refused, `refs/replace/../` refused, `refs/notes/*` and `refs/stash` unchanged, and a `.git/refs/replace` entry as a DIRECTORY vs FILE both handled. Case table against the candidate.'),
 ('C1ExecFetchHead', 'executor',
  'prove the FETCH_HEAD leg: n18 shallow honest admitted; a `.git/FETCH_HEAD` that is a symlink outside d refused; a FETCH_HEAD larger than the text cap refused; and state in one line why admitting the file does not admit a read (the fence never opens it). Case table against the candidate.'),
 ('C1ExecMutRebase', 'executor',
  're-derive the mutant battery against `{L}/.ufo/waves/round-50/w1/C1ExecRepair/fence_candidate.py`: for EACH of the 23 carried rows in `plans/mutants50/c1-mutants.json`, apply the inline diff, record whether it still applies and whether it is CAUGHT by `python3 plans/round50_c1_verify.py --lane . --skip-mutants --fence <mutant>` (verdict-vector change); DROP rows that cannot apply or are not caught and REPORT each drop; then AUTHOR fresh rows (bytes of the candidate fence) until at least 16 rows are witnessed-caught, covering the five repaired classes plus config/argv/symlink/hardlink/mount. Emit a complete replacement `c1-mutants.json` (same schema: id, class, payload, payload_sha256, description, expected_effect, payload_kind, digest) into your wave dir plus a witness table (row → killing fixture → Old-verdict/New-verdict).'),
 ('C1ExecMutAttrib', 'executor',
  'for every row C1ExecMutRebase keeps OR authors, independently witness the kill on a different fixture set ordering: apply the mutant, run the counter twice with different `--work` roots and `PYTHONHASHSEED=0`, and record that the killing fixture and the changed verdict are stable. Rows whose kill depends on ordering are reported and must be dropped; write a per-row `STABLE <id> <fixture> <old->new>` table.'),
 ('C1ExecSealedAudit', 'executor',
  'audit the blind held-out modules the critic seats wrote under `{L}/.ufo/waves/round-50/w1/*Sealed*/` (do not edit them): check each honours the FIXTURES contract (build(ctx,d) returning argv tail, fid/tool/expect/defects), builds twice to the same identity after `.git/index` masking, has no absolute build path, and is not readable from the fence writers\' reports (name cross-check). Emit `contract-ok`, `nondeterministic`, `duplicate-fid`, `name-leaks` rows and the count that may enter `plans/sealed50/`.'),
 ('C1ExecPopRepro', 'executor',
  'reproduce the population pin three times at the freeze tree: run `python3 plans/honest50/build_honest_population.py --lane <clone> --modules plans/honest50/modules --out <scratch>/run{A,B,C} --work <scratch>/w --jobs 8 --repeats 2` and report the three `POPULATION population.txt sha256=…` lines, `CHECKS`, and the byte comparison; confirm 126 fixtures and pin b5197f94…. Any drift is a defect report, not a re-pin.'),
 ('C1ExecCounterSelftest', 'executor',
  'selftest `plans/round50_c1_verify.py` on a clone at {F}: (a) `--fence` a file with no `breach` → all ERROR, predicate fail; (b) delete one population row in a COPY of the lane → `fixtures=125` and fail; (c) corrupt one `tree_sha256` in the copy → `mismatched=1`; (d) empty `plans/sealed46` copy → SEALED total=0 must still fail on `REFUSALS`/`SEALED` compared to literals; (e) a mutant payload that does not apply → `broken=1`; (f) dirty tree without `--allow-dirty` → fail. Emit one line per case with exit code.'),
 ('C1ExecCleanRun', 'executor',
  'run the frozen predicate once on a clean `git clone --shared` of the lane at {F} with the BASE fence and save the complete output to `{L}/.ufo/waves/round-50/w1/C1ExecCleanRun/receipt-base-fence.txt`: it must reproduce `HONEST fixtures=126 admitted=113 refused=13`, `REFUSALS total=20 clean=20`, `SEALED total=12 clean=12`, and exit 1. This is the before-receipt; no claim is scored here.'),
 ('C1ScribeLimit', 'scribe',
  'draft the exact, named limits of the R50-C1 instrument in ≤40 lines: what it does NOT measure (outside-d reads, io_uring, host paths outside scratch, states third-party tools write, host git version drift), each with the reason and the counter/file that would measure it instead. No new factual claims; cite paths only.'),
 ('C1ScribeEntry', 'scribe',
  'draft a `corpus/knowledge/` entry (target path `corpus/knowledge/fixture-honest-geometry.md`) for the honest-geometry instrument: provenance trio first (`source:`, `verified-at:`, `recheck:`), then the construct, the 126-population composition with its pin, the five refused honest classes and their documented git shapes, the controls that must fail, and the measured base numbers. Cite the `S###` rows the frontier seats open this round (read `{L}/corpus/SOURCES.md` after FRScoutGitDocs writes its report; if the ids are not yet assigned, write `S???` with the exact source title and say so).'),
 ('C1ScoutPrior', 'scout',
  'prior-art verdict for the instrument: is "refusing hostile git fixtures by shape, validated against a population of documented honest git states" published? Search the git documentation, sandbox/CI security write-ups and eval-harness docs; fetch at least 3 URLs and quote ≤25 words each with location; verdict split phenomenon-new vs instrument-new. No row is written by you — the L1 writes SOURCES rows; give URL, access date, quote, and proposed tier/scope.'),
 ('C1ConnOverlap', 'connector',
  'sibling-overlap scan: does any sibling lane own "git fixture geometry" or "sandbox admission" ground (read sibling PROVINCE.md files, read-only)? Cite the sibling path and the closest row; propose absorb vs report-out per item. Also check whether `kumitate` owns tool-instrument standards this counter should follow.'),
 ('C1SimplBudget', 'simplifier',
  'attack the instrument\'s size: list every leg, literal and helper the predicate does not need (e.g. legs that a cheaper check subsumes, duplicate literals); propose the smallest counter that keeps the same falsifiable predicate and name what would be lost. No edits — a report with a ranked deletion list.'),
]

c1_attack = [
 ('C1CritPredicate', 'critic',
  'attack the predicate itself: construct (in scratch) fences that PASS `plans/round50_c1_verify.py` without doing the claimed work — a fence that refuses on the fixture directory NAME patterns, one that keys on file counts, one that admits everything except paths containing "outside" — and report which (if any) reach `PREDICATE R50-C1 pass`. If one does, the counter is broken and the round must be re-designed: say so explicitly.'),
 ('C1CritDoNothing', 'critic',
  'run the cheapest do-nothing control fresh on a clone at {F}: `python3 plans/round50_c1_verify.py --lane . --skip-mutants` (base fence). Confirm `HONEST admitted=113` and `PREDICATE fail`; then state whether any *other* control reaches the predicate by skipping the claimed work.'),
 ('C1CritAdmitAll', 'critic',
  'test four degenerate fences (`admit_all`, `refuse_all`, `only_dot_git_exists`, `refuse_if_alternates_or_gitfile_or_symlink`) through the counter; for each, report the exact failing leg and whether the honest leg with the two in-d indirection classes is what separates boundary reasoning from shape matching.'),
 ('C1CritPopScope', 'critic',
  'attack population completeness: enumerate documented git states the 126-fixture population does not hold (grafts, `info/grafts`, `objects/info/packs` variants, `shallow` + replace together, `core.worktree`,`worktreeConfig`, submodules, LFS pointers, `gc` cruft packs, `commit-graph` chains, `packed-refs` peeled annotated tags, `reftable` backend) and mark each: must-admit / may-refuse / out-of-scope, with a git-doc pointer. Quantify the over-refusal surface this population cannot see.'),
 ('C1CritIdent', 'critic',
  'attack the identity pins: can a fixture be swapped for a hostile one without changing `tree_sha256`? Try (a) an extra empty directory, (b) a mode bit, (c) a file mtime, (d) a masked `.git/index`, (e) an unmasked file with identical content hash but different inode. Report what the identity cannot see and whether that matters for admission decisions.'),
 ('C1CritBlind1', 'critic', 'author TWO blind hostile modules against the repaired fence (read only `plans/fixture_fence.py` at the freeze tree and the claims doc — never another seat\'s repair), each an out-of-d escape a naive pointer-resolution repair would admit: (i) a gitfile whose target is a SYMLINK chain ending outside d, (ii) an alternates line using an absolute path that resolves through `..` to outside d. Write them under `{L}/.ufo/waves/round-50/w1/C1CritBlind1/sealed/`; state each expected refusal'),
 ('C1CritBlind2', 'critic', 'author TWO blind hostile modules: (i) a `commondir` file whose target escapes d, (ii) a store reached by a gitfile that is itself inside d but whose `objects/info/alternates` line escapes d (two-hop). Under `C1CritBlind2/sealed/`; state expected refusals.'),
 ('C1CritBlind3', 'critic', 'author TWO blind hostile modules: (i) `refs/replace/<40hex>` whose target object lives in an OUTSIDE store borrowed through alternates (the repair must not turn one allowed pointer into a read outside d), (ii) `.git/FETCH_HEAD` as a hardlink to a file outside d. Under `C1CritBlind3/sealed/`.'),
 ('C1CritBlind4', 'critic', 'author TWO blind hostile modules: (i) a `.git` FILE with a `gitdir:` line containing a NUL or a newline delimiter trick, (ii) a store whose `config` gains an `[include]` only AFTER the gitfile is followed (the repair must still parse the resolved store config). Under `C1CritBlind4/sealed/`.'),
 ('C1CritBlind5', 'critic', 'author TWO blind hostile modules: (i) an honest-looking repo with an extra `.git/objects/info/alternates` CHAIN A→B where B is outside d, (ii) a linked worktree whose `commondir` points to a store OUTSIDE d while its own gitdir is inside. Under `C1CritBlind5/sealed/`.'),
 ('C1CritBlind6', 'critic', 'author TWO blind hostile modules: (i) a fixture with two repositories where the SECOND one\'s store crosses a mount boundary (bind-mount not available — emulate the device check with a hardlink into a different device if possible, else state why it cannot be built), (ii) a `.git` file naming `../` a repo whose objects are a symlink to outside d. Under `C1CritBlind6/sealed/`.'),
 ('C1RevRerun', 'reviewer',
  'independent rerun of the frozen predicate against `{L}/.ufo/waves/round-50/w1/C1ExecRepair/fence_candidate.py` on a clean clone at {F}: report every line verbatim, exit code, and whether HONEST/REFUSALS/SEALED match the seat\'s claim. Do not accept a summary.'),
 ('C1RevClaim', 'reviewer',
  'adversarially assess falsifiability and causal separability of R50-C1 under its frozen kill rule: is the claim reachable without the fence repair? Does C1 depend on any C2 artifact? Is the mutant floor satisfiable by a fence that does not resolve pointers (shape keys)? Write the strongest non-author rejection case and whether the committed evidence answers it.'),
 ('C1RevNoHarm', 'reviewer',
  'identify plausible harm from admitting this novelty claim: (a) does the repaired fence WEAKEN any refusal (compare the 20 refusals + 12 sealed verdicts before/after)? (b) does landing a 126-fixture population bloat the repo or encode host-specific bytes? (c) does the novelty claim double-count round 48\'s honest leg? State an exact testable check per risk.'),
 ('C1MutBypass', 'mutation-tester',
  'attack the counter\'s own accounting: mutate the counter in scratch (predicate line printed unconditionally; HONEST denominator read from the population file; `mismatched` list ignored; SEALED leg skipped) — one mutation at a time — and show whether the frozen predicate still fails on a fence known to be bad (base fence). Any mutation that lets the base fence pass is a counter defect: report it with the diff.'),
 ('C1MutSealed', 'mutation-tester',
  'take the 12 `plans/sealed46/` modules and mutate each fixture one byte-level change at a time in the direction of "an honest repository" (remove the outside pointer, keep shape) — record which mutated fixtures the BASE fence still refuses and which the r49 candidate admits; this bounds what the sealed leg can see. Report survivors as limits of the leg.'),
 ('C1MutHostile', 'mutation-tester',
  'take the 20 `plans/refusals46/` modules and build 6 fresh hostile variants that a pointer-resolving repair might admit (gitfile to outside, alternates to outside via relative climb, commondir outside, include through a resolved store, replace ref pointing into an outside store, hardlinked FETCH_HEAD). Measure base fence and the r49 candidate; hand them to the L1 as candidate sealed50 rows with expected refusal.'),
 ('C1LabratProbe', 'executor',
  'one falsifiable probe: does `git` itself, with `GIT_CEILING_DIRECTORIES` set at d and a gitfile naming a store outside d, resolve and READ that store (i.e. is the escape real, not theoretical)? Build it in scratch under strace and report the syscalls that leave d. This grounds why the repair must resolve pointers rather than trust them.'),
 ('C1RevengerIntent', 'revenger',
  'reverse-engineer the base fence\'s intent for the five refused classes from its docstring, the r45/r46 counter contracts and the r49 critic reports: for each, was the refusal a deliberate security boundary or a shape heuristic? Quote the lines. State which of the five can be reopened without weakening a named refusal.'),
]

# ---------------- R50-C2 (calibration) ----------------
c2 = [
 ('C2ExecAudit', 'executor',
  'run `python3 plans/round50_c2_audit.py --lane .` at {F} and produce a per-pointer table of the 12 unresolved pointers: pointer, where cited (file:line), what it was meant to be, and a proposed resolution (`-> existing target` or `-> never-landed` with the `git log --all --oneline -- <path>` output that proves it). Save the table to your report; no lane edits.'),
 ('C2ExecCorrections', 'executor',
  'draft the append-only `## Round 50 — C2 corrections` block for SCORECARD.md: one `SUPERSEDED <pointer> -> <target|never-landed>` row per unresolved pointer, ordered as the audit prints them, each with a one-line reason and the evidence command. Emit the exact block to `{L}/.ufo/waves/round-50/w1/C2ExecCorrections/block.md` — the L1 pastes it verbatim.'),
 ('C2ExecVerifyTargets', 'executor',
  'verify every target in the C2 corrections block: the target exists at the tip and is the artifact the row meant (open it, quote one line); for each `never-landed`, show `git log --all --oneline -- <pointer>` is empty AND that no similarly named file exists (`git ls-files | grep`). Emit PASS/FAIL per row.'),
 ('C2RevRerun', 'reviewer',
  'independently rerun the audit and its `--selftest` on a clean clone at {F}, then on a scratch copy with the corrections block appended to SCORECARD.md: report `POINTERS … unresolved=` before and after, exit codes, and whether the selftest still proves the check can fail.'),
 ('C2CritScope', 'critic',
  'attack the audit\'s surface definition: find pointer shapes it misses (extensions absent from EXTS, paths under `..`, `~/` paths, `.ufo/` paths, JSON-embedded paths, pointers inside PROVINCE tables) and pointers it counts that are not artifacts (e.g. example paths in prose). Quantify each with a grep over the three files.'),
 ('C2CritNonVacuity', 'critic',
  'try to make the audit green without fixing anything: append `SUPERSEDED <pointer> -> never-landed` for a pointer that IS in history; point a row at an unrelated existing file; add a correction twice. Report which variants the audit accepts (each is a defect) and which it refuses.'),
 ('C2CritHash', 'critic',
  'attack the hash half: a 40-hex token that is a commit but not an ancestor; a token that is a 40-hex substring of a longer hash; a gitlink/other object type. Show whether `cat-file -e` + `merge-base --is-ancestor` misclassifies any of them, with receipts.'),
 ('C2ScribeCorrections', 'scribe',
  'write the prose half of the C2 corrections block (≤25 lines) explaining what the four never-committed counters were, why the rows cited them anyway, and what the correction discipline now requires; cite the round-49 lesson and the audit command. No lane edits.'),
 ('C2RevNoHarm', 'reviewer',
  'check that the corrections are append-only and do not rewrite earlier SCORECARD text: diff the block against the file, confirm the twelve cited lines are untouched, and state whether any correction changes a historical claim instead of re-pointing it.'),
]

# ---------------- frontier, sources, report support ----------------
frontier = [
 ('FRScoutGitDocs', 'scout',
  'open and quote the git documentation rows this round needs (fetch each URL, record HTTP status, access date, and a ≤25-word located quote with the exact section): `gitrepository-layout(5)` for `objects/info/alternates`, `refs/replace/`, `.git/shallow`, `FETCH_HEAD`, `commondir`; `git-init(1)` for `--separate-git-dir`; `git-worktree(1)` for the gitfile + `commondir` pair. Propose id ranges, tier, scope, anchor per row. Do NOT edit SOURCES.md.'),
 ('FRScoutAlternates', 'scout',
  'second source check for the alternates leg: the git documentation paragraph on relative alternates entries and the security note about borrowed stores; also check whether git documents that `refs/replace/<object>` names an object, not a path. Report URL, status, date, quote, and whether the claims doc\'s classification matches the documentation.'),
 ('FRScribeSources', 'scribe',
  'draft the SOURCES.md rows (contract v1 shape, 11 columns, no `|` inside cells) from FRScoutGitDocs/FRScoutAlternates reports: id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by (`corpus/knowledge/fixture-honest-geometry.md`). Emit the rows to your wave dir for the L1 to append; do not edit corpus/.'),
 ('FRScribeGate', 'scribe',
  'draft the round-50 lesson Gate block: at least one ADMIT and one REJECT from this round\'s sources (reject one candidate source with a reason and a flip condition), the access dates and ≤25-word quotes, and the census command/output placeholders the L1 fills.'),
 ('FRScribeMistake', 'scribe',
  'draft the `## Mistakes` rows for `corpus/lessons/round-50.md` from this round\'s evidence: (1) the leaked fixture git env that broke the lane push (`GIT_CONFIG_GLOBAL=/dev/null` from a test shell), class `landing`; (2) the r49 honest stop (counter/population never landed) and what this round changed, class `landing`; (3) any seat-reported mistake you find in the wave dirs, class as appropriate. One row per mistake: class · evidence pointer · captured-by · fix.'),
 ('FRExecCensus', 'executor',
  'run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` at {F} and save the full output + exit code; then run the four frozen census snippets from CORPUS.md (rows, malformed rows, tier histogram, status histogram, duplicate ids) and save them. This is the before census; the L1 takes the after at close.'),
 ('FRDistillFindings', 'reviewer',
  'read every seat report that exists under `{L}/.ufo/waves/round-50/w1/` when you run and fold them into one findings table: claim served, finding, evidence pointer, severity for admission, and duplicates merged. Flag any finding that contradicts another. This is the wave-close distill for the L1.'),
 ('SentWaveHygiene', 'critic',
  'audit the whole wave for boundary violations: writes outside the allowed paths, secrets/credential material, /tmp citations, fleet-repo or sibling-lane touches, shared writer paths, leaked git env, seats that edited production files. One report with a per-seat disposition table and the exact commands you used.'),
 ('RevReportShape', 'reviewer',
  'pre-check the round report structure against the report contract (sections in order, one evidence pointer per bullet, before→after with counting command and commit, Sources & frontier, trend verdicts, `## SHONEN` with one line per box, stale-lane line, tool installs). Produce a checklist the L1 can tick, plus the SHONEN box list from SHONEN.md.'),
]

for n, r, detail in c1_build:
    add('R50' + n, r, 'novelty', 'R50-C1', 'build', detail.replace('{L}', str(LANE)).replace('{F}', FREEZE))
for n, r, detail in c1_attack:
    add('R50' + n, r, 'novelty', 'R50-C1', 'attack', detail.replace('{L}', str(LANE)).replace('{F}', FREEZE))
for n, r, detail in c2:
    add('R50' + n, r, 'calibration', 'R50-C2', 'attack' if r in ('reviewer', 'critic', 'mutation-tester') else 'build',
        detail.replace('{L}', str(LANE)).replace('{F}', FREEZE))
for n, r, detail in frontier:
    add('R50' + n, r, 'novelty+calibration', 'R50-C1+R50-C2', 'attack' if r in ('reviewer', 'critic', 'mutation-tester') else 'build',
        detail.replace('{L}', str(LANE)).replace('{F}', FREEZE))


extra_c1 = [
 ('C1ExecSealedAssemble', 'executor',
  'assemble the `plans/sealed50/` candidate from the blind critic modules and the hostile variants: de-duplicate by fixture identity, verify the FIXTURES contract and two-build determinism, reject modules whose fixture is not refused by the BASE fence (a sealed row must be a real hostile case), and emit `{L}/.ufo/waves/round-50/w1/C1ExecSealedAssemble/sealed50/` plus a manifest row per module (file, sha256, fixture, expected).'),
 ('C1ExecRepairDiff', 'executor',
  'compare `C1ExecRepair/fence_candidate.py` and `C1ExecRepairB/fence_candidate_b.py` against the base fence: a line-level risk table of what each OPENS (newly admitted shape) and what it keeps CLOSED; flag any difference where one repair admits a case the other refuses, and say which is correct with a git-doc or fixture reason.'),
 ('C1ExecParity', 'executor',
  'build the before/after refusal parity table: for each fixture of the 20 refusals46 modules and the assembled sealed50 set, record base-fence verdict, r49-candidate verdict and the final repair verdict; every row must stay BREACH. Emit `parity.tsv` in your wave dir and state any row that changed.'),
 ('C1ExecCounterHygiene', 'executor',
  'audit `plans/round50_c1_verify.py` for scratch hygiene (operator directive 2026-10-25): no `/tmp` literal, `--work` honoured, `tempfile.mkdtemp` under it, no writes outside the work dir (run under strace -f -e trace=openat,mkdir,unlink and list paths outside), no lane writes, runtime per leg. Emit the trace summary and a defect list.'),
 ('C1CritBlind7', 'critic', 'author TWO more blind hostile modules against the repaired fence: (i) a store directory that is a SYMLINK to the real store inside d (must refuse: symlink anywhere stays refused), (ii) a gitfile naming a store that is itself reached through a symlinked parent inside d. Under `C1CritBlind7/sealed/`.'),
 ('C1CritBlind8', 'critic', 'author TWO more blind hostile modules: (i) `packed-refs` with a peeled line naming an object only present in an outside store, (ii) `.git/objects/info/commit-graph` whose `commit-graph-chain` names a file outside d. Under `C1CritBlind8/sealed/`.'),
 ('C1CritRepairWeaker', 'critic',
  'decide which repair candidate is weaker for the security property, from the candidates and their measured verdicts only: construct the minimal hostile fixture that one admits and the other refuses (in scratch), and report it. If neither admits anything hostile, say what the fixture set cannot distinguish.'),
 ('C1CritMount', 'critic',
  'attempt the mount-boundary hostile/honest pair the r49 critic named (`w2/R46W2C1Intent.md`): can a mount point be created inside a fixture without root (bind mount in a user namespace, `unshare -rm`)? Report the observed capability and, if impossible, the exact refusal text; state what the repair must do when the device check fires.'),
 ('C1CritHygiene', 'critic',
  'attack the determinism of the counter: run the predicate twice with different `--work` roots, `PYTHONHASHSEED` values and shuffled `--jobs`; report any line that differs (fid order, verdicts, mutant catch count) and whether the difference can flip the predicate.'),
 ('C1RevBlindIndependence', 'reviewer',
  'verify the blind-set independence claim: check the blind critic reports and module paths for any evidence they read the repair candidates or each other (timestamps, quoted lines, shared paths); state per blind seat `independent` / `contaminated` with the pointer.'),
 ('C1RevParity', 'reviewer',
  'independently recompute the refusal parity table for a sample of 10 hostile fixtures (5 refusals, 5 sealed) on the base fence and the repair, and report any parity row that C1ExecParity got wrong.'),
 ('C1MutRepairB', 'mutation-tester',
  'run the re-derived mutant battery against `C1ExecRepairB/fence_candidate_b.py`: report caught/survived per row and compare with repair A. Mutants that apply to A but not B are `not-applicable`, never `caught`.'),
 ('C1MutSealedBlind', 'mutation-tester',
  'take the assembled blind modules in `C1ExecSealedAssemble/sealed50/` and mutate each fixture one byte-level step towards honest (remove the outside target) in scratch; report whether the repaired fence then ADMITS the mutated fixture (it should, if the mutation removes the escape) and whether the base fence still refuses it (bound of what the leg sees).'),
 ('C1ScoutGitVersion', 'scout',
  'host-sensitivity survey: which of the 126 fixtures depend on git output that changes with version or config (hooks samples, info/exclude, `worktree --relative-paths`, commit-graph layout, reflog format)? Cite the git release notes you can fetch and name the fixtures by fid.'),
 ('C1ScoutPrev', 'scout',
  'trace the honest-population lineage (r46 novel, r48, r49, r50) from the committed wave dirs: what each round added, what each refused, and what the r49 seat left unlanded. Cite paths and digests; this becomes the honest-history paragraph of the report.'),
 ('C1ScribeSealedDoc', 'scribe',
  'write the `plans/sealed50/README.md` draft: authoring provenance (blind rule, who wrote what shape), the contract each module follows, the refusal each is expected to produce, and the measured base-fence verdict. No lane edits.'),
 ('FRScoutContractV1', 'scout',
  're-read the SOURCES contract v1 in `/home/vgpnk/Projects/shokunin/CORPUS.md` and the maintained parser note; produce the exact 11-column row template and the census commands (rows, malformed, tier, status, duplicate id, mined used-by) so the append by the L1 cannot fail the gate. Quote the contract lines you rely on.'),
 ('FRScribeLesson', 'scribe',
  'draft the `corpus/lessons/round-50.md` skeleton: header, `## Mistakes` table stub, `## Gate` stub (admit + reject with quote fields), `## Claim evidence and honest verdicts` stub with the two claims and the receipt paths the L1 will fill. No verdicts of your own; placeholders must be explicit (`<L1 fills>`).'),
]
for n, r, detail in extra_c1:
    add('R50' + n, r, 'novelty' if 'C1' in n else 'novelty+calibration', 'R50-C1' if 'C1' in n else 'R50-C1+R50-C2',
        'attack' if r in ('reviewer', 'critic', 'mutation-tester') else 'build',
        detail.replace('{L}', str(LANE)).replace('{F}', FREEZE))

attack_roles = {'reviewer', 'critic', 'mutation-tester'}
attack = sum(i['role'] in attack_roles for i in items)
assert len(items) == 72, len(items)
assert attack >= 18, attack
spec = {
    'wave': 'kengaku-r50-w1',
    'milestone': 'kengaku round 50: one v2 wave builds and attacks the R50-C1 honest-geometry instrument (126-fixture honest population, repair of five over-refused documented git states, witnessed mutant floor, blind sealed set) and the R50-C2 self-assessment pointer audit',
    'reportDir': '.ufo/waves/round-50/w1',
    'maxLanes': 72,
    'axes': ['novelty', 'calibration'],
    'context': context,
    'items': items,
}
WAVE_DIR.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + '\n')
print(f'wrote {OUT} items={len(items)} attack={attack} roles={sorted({i["role"] for i in items})}')
