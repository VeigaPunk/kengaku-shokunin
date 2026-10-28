# C2ConnProtocol — class → owner map for the C2 routed-finding ledger

seat: `C2ConnProtocol` (connector) · lane `kengaku-shokunin` · round 51 (hyaku run 11) · 2026-10-28
axis named: **adjacency** — `AXES.md:16`: "Cross-domain awareness — evidence belonging to another
domain reported, not absorbed | Lane reports name contested scope; integrator arbitrates".
frozen instrument read: `plans/round51_routing.py` (stage-1 freeze `e07f131`), ledger
`corpus/routed-findings.jsonl`.
ownership sources read: fleet `PROTOCOL.md`, `PROTOCOL-APPENDIX.md` pointers, `MISSION.md`,
`AGENTS.md`, `LEARNING.md`, `CORPUS.md`, `shokunin.conf`, root `SCORECARD.md`, lane `PROVINCE.md`,
`kumitate-shokunin/PROVINCE.md` — all at fleet `9baaeee8e9e13b969f06e6c33597a35af1868c7c`
(`git status --porcelain` over those paths: empty, so the working tree equals the commit).

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7

## 0. Scope of this seat

One item only: for the ledger classes that describe **verifier / closure / report / manifest
process**, name the owning lane and quote the line that proves it. I did not attribute the 71 rows
(that is the attribution seats' work), did not run `--run-checks`, and wrote no production file.
Everything below is a map plus the constraints the frozen counter imposes on it, so an attribution
seat can fill `owner` and `disposition` without inventing an owner.

## 1. The item's two named PROVINCE files do not exist (path defect in the seat brief)

```
$ cd /home/vgpnk/Projects/shokunin
$ for p in protocol-shokunin/PROVINCE.md aggregator-shokunin/PROVINCE.md PROVINCE.md; do \
    if test -e "$p"; then echo "PRESENT $p"; else echo "ABSENT $p"; fi; done
ABSENT protocol-shokunin/PROVINCE.md
ABSENT aggregator-shokunin/PROVINCE.md
ABSENT PROVINCE.md
$ git ls-tree --name-only HEAD | grep -iE 'protocol|aggregat|province'
PROTOCOL-APPENDIX.md
PROTOCOL.md
$ find . -maxdepth 2 -name 'PROVINCE.md' -not -path './.git/*' | grep -E '^\./(PROVINCE|protocol|aggregator)'
none at fleet root or under protocol-/aggregator-
```

There is no `protocol-shokunin/` or `aggregator-shokunin/` directory and no root `PROVINCE.md` —
neither in the tree nor in fleet git history (`git log --oneline --all -- 'protocol-shokunin/PROVINCE.md'
'aggregator-shokunin/PROVINCE.md'` printed nothing). Both are **main-repo lanes whose repo is `.`**:

- `shokunin.conf:20` `protocol|.|fleet-meta: protocol soundness, gate integrity`
- `shokunin.conf:21` `aggregator|.|cross-lane quality, mint and dormancy calls, corpus review`
- `MISSION.md:21-22` `protocol:   { cwd: $SHOKUNIN_ROOT, … }` / `aggregator: { cwd: $SHOKUNIN_ROOT, … }`
- `PROTOCOL.md:146-147` "Every dispatched lane writes its report at `.ufo/reports/round-<N>/<id>.md`
  in the main repo, where `<id>` is the roster id (`protocol` and `aggregator` for the two main-repo
  lanes)."

So the province of `protocol` and `aggregator` is expressed as **file ownership in `PROTOCOL.md`
plus lane-owned sections of the root ledgers**, not as a `PROVINCE.md`. Any seat asked to read a
`PROVINCE.md` for those two lanes should read `PROTOCOL.md` §Invariants, §Gate standard **Registry**,
§Round-robin closure steps 1–4, and `SCORECARD.md:177` / `SCORECARD.md:259` instead. This is a
defect of the seat brief, not of the lane tree.

## 2. Commands run (read-only; clone in scratch)

```
$ export TMPDIR=/fast/scratch/hyaku/kengaku-r51/C2ConnProtocol
$ git clone --shared -q /home/vgpnk/Projects/shokunin/kengaku-shokunin lane   # inside scratch
$ git -C lane rev-parse HEAD                → 4090c3db79d11279ab5e5121ba25e74aa316e6e7
$ git -C lane rev-parse --show-toplevel     → /fast/scratch/hyaku/kengaku-r51/C2ConnProtocol/lane
$ cd lane && python3 plans/round51_routing.py --lane .        # no --run-checks
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=0 incomplete=71
OWNERS attributed=0 unattributed=71
DISPOSITIONS set=0 bad=71
SOURCES resolved=71 missing=0
CHECKS present=61 absent=10
VERIFIED ran=0 passed=0 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 fail
```

(The head matches `.ufo/waves/round-51/claims/c2-before.txt` verbatim; that receipt is the frozen
before-state and I did not re-derive it as a claim.)

Owner vocabulary actually accepted by the counter:

```
$ cd lane && python3 -c "
import importlib.util, pathlib
s = importlib.util.spec_from_file_location('r', 'plans/round51_routing.py')
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
o = m.load_owners(pathlib.Path('/home/vgpnk/Projects/shokunin'))
print(len(o)); print(' '.join(sorted(o)))"
17
aggregator chousa kagi kaidoku kake kama kasegi kengaku kotoba kotodama kumitate mori protocol
souji tabi tameshi unowned:integrator
$ grep -cE '^\s{0,6}[a-z][a-z0-9-]{2,15}:\s*\{' /home/vgpnk/Projects/shokunin/shokunin.conf
0
```

Sweep for sibling ownership anywhere in the ledger (case-insensitive, word boundary):

```
$ for L in kama kotoba kumitate kagi kasegi kake tameshi tsukuroi mado tabi lore revenger \
           kaidoku souji mori chousa kotodama protocol aggregator; do
    printf '%s %s\n' "$L" "$(grep -c -i "\b$L\b" corpus/routed-findings.jsonl)"
  done
kama 0  kotoba 0  kumitate 0  kagi 0  kasegi 0  kake 0  tameshi 0  tsukuroi 0  mado 0  tabi 0
lore 0  revenger 0  kaidoku 0  souji 0  mori 0  chousa 0  kotodama 0  protocol 0  aggregator 0
```

## 3. Fleet-process classes → owning lane, with the proving line

Quotes are verbatim, `file:line` at the revisions above. "Owner" is the lane that owns the artifact
the class is about — the lane whose correction closes the row — not the lane that found it.

| class / family | owning lane | proving quote |
|---|---|---|
| `registry-missing-gate-rows`, `registry-missing-row` — a gate/probe with no registry row | **the lane whose registry home lacks the row**: `kengaku` (its own `SKILL.md`), `protocol` (root `SCORECARD.md` above `## Aggregator lane`), `aggregator` (inside its own section) | `PROTOCOL.md:398-400` "**Registry.** The schema is this section's; a child lane's *registry home* is its own `SKILL.md`. For main-repo lanes (`protocol`, `aggregator`), it is the explicitly lane-owned registry section in root `SCORECARD.md`: protocol above `## Aggregator lane`, aggregator inside its own section" · homes: `SCORECARD.md:177` `## Gate registry — protocol lane registry home`, `SCORECARD.md:259` `## Aggregator lane — …` |
| `registry-row-line-citation`, `registry-row-overstatement`, `round-close-unregistered` — a registry row that is wrong or missing | same lane as the registry home holding the row → **`kengaku`** for the `SKILL.md` rows (R39-R1, R40-R3, R42-R2.2, R42-R3-02, R42-R3-07, R42-R3-28) | same clause `PROTOCOL.md:398`; `PROTOCOL.md:377` "A **gate** is a committed, re-runnable verdict script a lane owns" |
| closeout carry-over: `carried-residuals-bundle`, `c1-counter-soundness-residuals` | **three owners, split by duty**: row content = the lane owning the residual file → `kengaku`; the durable queue row = `aggregator`; the closure-debt answer = `protocol` | `PROTOCOL.md:241-245` "routes cross-domain defects a lane report filed against a sibling's files to the owning lane — the integrator's report carries one routing line per defect **including defects a lane owes its own repo** … The aggregator mirrors each routed defect into the owning repo's `corpus/lessons/` and keeps an **open routed-defects row** in its ledger until the owning lane's correction lands" · `PROTOCOL.md:288` "**`in-flight` is debt, not a resting status.** Every `in-flight` row is answered by the next protocol round" |
| `ledger-status-mismatch`, `ledger-stale-check`, `order-class-ledger-row` | **`kengaku`** — the rows live in its own `corpus/routed-findings.jsonl` / `corpus/defects.jsonl`; the fleet queue is `.ufo/reports/AGGREGATE.md`, owned by `aggregator` | `PROTOCOL.md:502-503` "no lane edits another lane's corpus files, and `round-<N>-aggregator-*.md` are aggregator-owned" · `PROTOCOL.md:326` "The **aggregator** lane is a main-repo lane that reviews every child repo's `corpus/` each round" |
| spot-check **duty** (who must perform it) | **`unowned:integrator`** — a non-author reviewer/operator role, never a rostered lane | `LEARNING.md:42-45` "Each round a non-author — a fresh reviewer or the operator — spot-checks a sample of that round's gate decisions, **at least one admit and one reject**, and records `agree`/`disagree` with a reason in the round's lesson. A subagent the lane dispatched is still the lane." |
| spot-check **record**: `lesson-*` classes, D7's missing row | **`kengaku`** — the lane's own lesson file carries the result | `LEARNING.md:69-70` "`corpus/lessons/round-<N>.md` — carries a `## Gate` section: candidates considered, admitted, rejected (with reasons), and the spot-check result" · `CORPUS.md:19-20` "each `lessons/round-<N>.md` carries a `## Gate` section (candidates, admitted, rejected with reasons, spot-check result)" |
| report process: lands-last, `SHONEN` heading, hash citation, marker-vs-report | filed by the lane → **`kengaku`**; graded at closure → **`protocol`** | `PROTOCOL.md:117-118` "A lane report **lands last** — written only after the lane's child-repo work is committed, and it must cite that commit's hash. Landed means committed" · `PROTOCOL.md:169` "A lane whose mission has terminated or been respawned without filing its round report is recorded `failed` by the integrator" |
| `MANIFEST.json` `rounds` appends, closure ledger, `closure-correction` | **`protocol`** (integrator of record) | `PROTOCOL.md:207-208` "**Integrator of record.** The integrator this protocol assigns work to is the round's `protocol` lane — a role, not a separate rostered lane" · `PROTOCOL.md:252` "Appends one entry to `MANIFEST.json`'s `rounds` array (integrator-of-record scope …)" |
| wave outputs (round-50 D1) inside the lane repo | **`kengaku`** | `PROTOCOL.md:118` "Landed means committed, so changes that exist only in a working tree do not count for the round" · `PROTOCOL.md:468-469` "Lanes write only inside their own child repo and their lane report at `.ufo/reports/round-<N>/<id>.md`" |
| fleet `.ufo/waves/round-<N>/` closure-gate artifacts | **`protocol`** | `PROTOCOL.md:475-476` "`.ufo/reports/`, `.ufo/waves/`, and the round's `.ufo/prompts/*.md` are committed with the round's integration commit — an untracked prompt is non-durable dispatch evidence" |
| `WAVE-DONE` marker and `<wave>-results.json` (round-50 D3) | **`unowned:integrator`** — the orchestrator's dispatcher writes both; no lane may | `.ufo/prompts/kengaku-round-51.md:285-288` "The orchestrator's dispatcher takes it within ~15 s (marker `<wave>.ready.dispatched`), spawns every seat … and when all seats settle writes `<wave>-results.json` beside the dispatch file … and messages you `WAVE-DONE <wave> … results=<path>`" |
| source locations (round-50 D5, `S###` line cites) | **`kengaku`** — `corpus/SOURCES.md` is the lane's own registry | `PROTOCOL.md:435` (file-contract row: `corpus/SOURCES.md` … "append-only per the contract … main-repo lanes (`protocol`, `aggregator`) hold no `corpus/`") · `PROTOCOL.md:352` "A numeric claim carries its counting command, an absence claim its search sweep, and a quote its location (frontmatter/body, file, line)" |
| `host-safety-envelope`, `envelope-drift-record` | **`kengaku`** for the artifact (its own `build-spec.json` / `measure-final.txt`); the fleet-wide seat-containment **policy** ground is **`kumitate`** | `kumitate-shokunin/PROVINCE.md:22` "Isolation substrates for parallel agents (git worktrees, harness isolation backends, jj workspaces) … seat-containment rules derived from their mechanisms" |
| `seat-scratch-leftovers`, `scratch-root-guard*`, `scratch-guard-exit-contract`, `guard-exit-code`, `guard-selftest-gap` | **`kengaku`** — its own scratch tree and its own `plans/scratch_guard.py`; fleet scratch reclamation is operator-side, not a lane | `AGENTS.md` "Disk guard (driver scratch reclamation; every driver gates on it): `scripts/hyaku/disk-guard.sh {check,status,sweep,purge-lane,watch,selftest}`" · `AGENTS.md` "`MISSION.md`, `AXES.md`, `CORPUS.md`, `scripts/` and `shokunin.conf` are operator-side" |
| any class whose fix surface is `MISSION.md` / `AXES.md` / `CORPUS.md` / `scripts/` | **`unowned:integrator`**; `protocol` *names* the correction and may not edit | `PROTOCOL.md:464-466` "Only integrator roles write main-repo files: `MISSION.md`, `AXES.md`, `CORPUS.md`, and `scripts/` are operator-side integrator files, whose corrections the protocol lane names in its round notes and does not edit" |
| contested scope / "whose province is this" | **`protocol`** arbitrates and records the ruling; `aggregator` mirrors it as an open ledger row | `PROTOCOL.md:457-459` "Contested scope — evidence or work is reported in the lane report; the integrator arbitrates by refining `PROVINCE.md` and records the ruling in the round notes" · `PROTOCOL.md:326` |

## 4. Every class actually in the ledger at the tip

64 distinct `class` values over 71 rows. **All 64 resolve to `kengaku`** — each row's `source`
pointer is a lane path (`SOURCES resolved=71 missing=0`) and the sibling sweep in §2 finds no
sibling-lane name in any row, so no row currently has evidence for a non-`kengaku` owner. Grouped
(the fleet-process families of §3 marked ★):

| family | classes | owner at this tip |
|---|---|---|
| ★ registry (5) | `registry-missing-gate-rows`, `registry-missing-row`, `registry-row-line-citation`, `registry-row-overstatement`, `round-close-unregistered` | `kengaku` (`SKILL.md` is its registry home) |
| ★ carry-over (2) | `carried-residuals-bundle`, `c1-counter-soundness-residuals` | `kengaku` (content); queue row `aggregator`, debt answer `protocol` |
| ★ ledger integrity (3) | `ledger-stale-check`, `ledger-status-mismatch`, `order-class-ledger-row` | `kengaku` |
| ★ scratch/guard (6) | `guard-exit-code`, `guard-selftest-gap`, `scratch-guard-exit-contract`, `scratch-root-guard`, `scratch-root-guard-registry`, `seat-scratch-leftovers` | `kengaku` |
| ★ gate registry/behaviour (3) | `gate-p10-unpinned-uv`, `gate-undeclared-dependency`, `gate-without-row-quotes` | `kengaku` |
| ★ counter soundness (3) | `c1-counter-soundness`, `c1-refreeze-keyed-control`, `c2-filler-control` | `kengaku` |
| ★ plan/freeze (5) | `plan-class-from-unfrozen-probe`, `plan-host-dependent-cheat`, `plan-missing-refusals`, `plan-missing-restore-control`, `plan-mutant-numerator` | `kengaku` |
| ★ receipt/doc discipline (16) | `advertised-count`, `claims-edit-unnamed`, `envelope-drift-record`, `frozen-cell-wrong-citation`, `host-safety-envelope`, `intent-brace-prefix`, `log-in-place-rewrite`, `predictor-lone-cr`, `probe-work-dir-traceback`, `readme-provenance-label`, `receipt-without-revision`, `row-anchor-wrong-line`, `scorecard-overstatement`, `sources-correction-rule`, `unattacked-mutation-items`, `v11-lookup-predictors` | `kengaku` (the one whose rule home is fleet `CORPUS.md`, `sources-correction-rule`, closed in-lane at `corpus/QUALITY.md:759`; a *new* row against `CORPUS.md` itself would be `unowned:integrator`) |
| ★ criterion (6) | `criterion-cli-mismatch`, `criterion-false-sentence`, `criterion-nonlanded-tool`, `criterion-self-undermining-scope`, `criterion-unreachable-receipt`, `criterion-wrong-line-pin` | `kengaku` (`corpus/QUALITY.md`) |
| ★ entry (8) | `entry-counterfactual-error`, `entry-false-arithmetic`, `entry-false-sentence`, `entry-internal-inconsistency`, `entry-line-ref-off-by-one`, `entry-overclaim`, `entry-vacuous-clause`, `entry-wrong-citation` | `kengaku` (`corpus/knowledge/`) |
| ★ lesson (7) | `lesson-false-measurement`, `lesson-fix-without-receipt`, `lesson-line-ref-off-by-one`, `lesson-unpersisted-number`, `lesson-unreproducible-command`, `lesson-unsupported-carry-claim`, `lesson-wrong-pointer` | `kengaku` (`corpus/lessons/`); spot-check duty itself `unowned:integrator` |

Consequence for the attribution seats: the C2 move is satisfied by **completing `owner` +
`disposition` on lane-owned rows**, not by manufacturing routed-out rows. Any row marked `routed`
or `referral` needs a non-`kengaku` owner *and* a `next` field; on the evidence above there is no
row for which that is truthful today.

## 5. Hard constraints the frozen counter puts on `owner` / `disposition`

Read off `plans/round51_routing.py` (`check()`), all of them fail the predicate:

1. **Owner vocabulary is a hardcoded 17-name set, not `shokunin.conf`** — in the *committed*
   instrument at `4090c3d` (the bytes the before-receipt was measured with; the working tree
   already carries an uncommitted candidate repair, §7). `load_owners()` there only parses
   YAML-shaped lines `name: {`; `shokunin.conf` has **0** such lines (its `LANES` rows are
   `id|repo|axes` pipes), so the accepted set is exactly `FALLBACK_OWNERS`:
   `aggregator chousa kagi kaidoku kake kama kasegi kengaku kotoba kotodama kumitate mori protocol
   souji tabi tameshi unowned:integrator`. The claim text says "every `owner` names a fleet lane from
   `../shokunin.conf`" (`plans/round-51-claims.md` §C2) — the code does not read that file's roster.
   Seven rostered lanes are **unrouteable** under the frozen counter: `lore`, `revenger`, `mado`,
   `tsukuroi`, `audio`, `game-dev-2d`, `game-dev-3d`. Routing a host-operability row to `tsukuroi`
   fails `OWNER`. This is a prose/code contradiction for the C2 attackers, not something an
   attribution seat may fix by picking a different owner.
2. `routed` / `referral` → owner must not be `kengaku` **and** `next` must be non-empty
   (`NEXT violations`). No row has a `next` field today (`0` of 71).
3. Every row needs a non-empty `check` **regardless of disposition** — the 10 rows with
   `check: ""` (`R40-R5`, `R42-R3-09`, `R42-R3-33`, `R42-R3-34`, `R42-R3-35`, `R42-R3-37`,
   `R45-S5-7b`, `R45-S5-7c`, `R45-S5-7d`, `R45-S5-7e`) cannot pass as anything
   until a command is written.
4. `fixed-verified` → the check is executed (`bash -lc`, cwd = the counter's scratch tmp dir, 60 s
   timeout, committed bytes). The code does **not** sandbox the network; the claims' §Limits
   *declares* that "a check that needs a network or a live model counts as failed", which a human
   must apply — the counter will happily pass a network-dependent check on a networked host. See §7
   for the cwd consequence. `fixed-historical` → `close`'s first token must be
   a 7–40 hex commit that `git cat-file -e` resolves, or an existing lane path.
5. `status` ∈ {`open`,`closed`,`refused`,`blocked`}; `disposition` ∈ {`fixed-verified`,
   `fixed-historical`, `routed`, `referral`, `accepted-risk`, `refused-out-of-scope`}. A `refused`
   **status** is not a disposition.
6. **Vocabulary gap (state, do not smooth):** `R42-R3-14` and `R42-R3-16` carry
   `status: refused` and a `blocker` reading "REFUTED at the tip: …". The frozen disposition set has
   no `refuted` value, so no disposition states the finding's actual fate; the closest honest choices
   are `accepted-risk` (only if a risk is genuinely accepted) or `refused-out-of-scope` (misdescribes
   a refutation). The L1 has to rule, and the ruling belongs in the round notes.

## 6. Round-50 §6 routed defects → owner

`corpus/lessons/round-50-verifier-spotcheck.md:147-186` (the round-50 non-author closure):

| defect | class | owner | why |
|---|---|---|---|
| D1 uncommitted round work (`.ufo/waves/round-50/w1/` 193 files, `w1.ready*`, `plans/round50_c1_verify.py`) | wave outputs / report truth | **`kengaku`** | `PROTOCOL.md:118` landed-means-committed; `:468` lanes write only inside their own child repo |
| D3 wave not settled (no `WAVE-DONE`, no `w1-results.json`) | wave settlement marker | **`unowned:integrator`** for the marker + results file; **`kengaku`** for landing the outputs D1 names | `.ufo/prompts/kengaku-round-51.md:285-288` the orchestrator's dispatcher writes `w1-results.json` and messages `WAVE-DONE` |
| D5 source locations (S175 → `gitrepository-layout.adoc:285-286`; S177 → `git-fetch.adoc:41`) | `row-anchor-wrong-line` family | **`kengaku`** | `PROTOCOL.md:435` `corpus/SOURCES.md` is the lane's; `:352` a quote carries its location; `:502` no lane edits another lane's corpus |
| D7 lesson spot-check row (`corpus/lessons/round-50.md` `## Gate` has no result) | `lesson-*` / spot-check record | **`kengaku`** | `LEARNING.md:69-70`; `CORPUS.md:19-20` |
| (D2, D4, D6 — not in the item's list, same owner) | counter honesty / revision labels / novelty proxy | **`kengaku`** | `PROTOCOL.md:377` a gate is a verdict script the lane owns; `:352` numbers carry their command and revision |

## 7. In-flight edit to the frozen instrument (observed; not this seat's write)

The lane worktree is **not** clean at the tip: `git status --porcelain -- plans/round51_routing.py`
prints ` M plans/round51_routing.py` (13 dirty entries in the lane overall — one is this report file,
the rest are siblings'/L1's work; this seat wrote nothing else). The uncommitted diff changes three
things that matter to C2:

```
-            m = re.match(r"\s{0,6}([a-z][a-z0-9-]{2,15}):\s*\{", line)
+            m = re.match(r"\s*([a-z][a-z0-9-]{1,15})\s*\|", line)
+        for d in fleet.glob("*-shokunin"):
+            if d.is_dir():
+                owners.add(d.name[: -len("-shokunin")])
...
-                out = subprocess.run(["bash", "-lc", cmd], cwd=str(tmp),
-                                     capture_output=True, text=True, timeout=60,
+                out = subprocess.run(["bash", "-lc", cmd], cwd=str(lane),
+                                     capture_output=True, text=True, timeout=90,
...
-    ledger = Path(args.ledger) if args.ledger else lane / "corpus/routed-findings.jsonl"
+    ledger = Path(args.ledger).resolve() if args.ledger else lane / "corpus/routed-findings.jsonl"
```

Second-order effects the L1 must rule on before the after-measurement:

1. **Owner universe widens.** With the worktree bytes the accepted set is `FALLBACK_OWNERS` ∪ the
   `LANES` ids ∪ every `*-shokunin` directory on disk — so `lore`, `revenger`, `mado`, `tsukuroi`,
   `audio`, `game-dev-2d`, `game-dev-3d` become acceptable and §5.1's trap disappears. That makes
   the code match the claim's prose ("a fleet lane from `../shokunin.conf`"), which the committed
   bytes do not. It also accepts a lane that exists on disk but is **unrostered**, which
   `AGENTS.md` forbids as a membership test: "A lane repo that exists on disk is **not** rostered.
   Membership comes only from `MANIFEST.json`." All 21 current `*-shokunin` dirs are in `LANES`, so
   this is latent, not live.
2. **`--run-checks` cwd changes from the scratch tmp dir to the lane root, and the timeout 60 s →
   90 s.** This is a semantic change to a frozen instrument, and it is load-bearing: measured now,

   ```
   $ (cd <scratch-tmp> && bash -lc "grep -q '^| \`order-check\`' SKILL.md && …")   rc=2
   $ (cd kengaku-shokunin && bash -lc "grep -q '^| \`order-check\`' SKILL.md && …") rc=0
   $ (cd <scratch-tmp> && bash -lc "python3 plans/anchor_line_check.py --lane . >/dev/null") rc=2
   $ (cd kengaku-shokunin && bash -lc "python3 plans/anchor_line_check.py --lane . >/dev/null") rc=0
   ```

   Under the **committed** bytes almost every relative-path check (the majority: `grep -q … SKILL.md`,
   `test -f plans/…`, `python3 plans/…`) fails for want of cwd, so the after-target
   `CHECK_FAILED 0` is unreachable unless each `fixed-verified` row's check is written
   cwd-independent (`cd "$LANE" && …`, or absolute paths). Under the **worktree** bytes the same
   checks pass, so the row's disposition flips with an uncommitted edit.
3. `plans/round-51-claims.md` §C2 *Limits* still declares "`--run-checks` executes 71 short shell
   commands from the ledger with a 60 s timeout each in a scratch cwd". A stage-1-frozen claims file
   and the instrument it freezes now disagree. The lane's own rule for this is append-only
   correction: `PROTOCOL.md:123` "Corrections land as new commits, never by amending a cited one",
   and the claims file's own §C2 predicate binds the after-measurement. Either the instrument
   reverts to the frozen bytes, or the claims file takes an **appended amendment** naming the owner
   universe, the cwd and the timeout before any after-measurement is taken — otherwise the before
   (`c2-before.txt`, `ran=0`, cwd=scratch) and the after are produced by different instruments.

This is a connector's observation, not a ruling: the L1 owns the instrument and the claims file.

## 8. Limits

- Read-only against the lane. No `--run-checks` over the ledger: I executed only three individual
  checks (§7) to measure cwd dependence, so I assert nothing about which of the 71 checks pass.
- The owner map is derived from the fleet protocol text at `9baaeee8`; it is a *rule*, and I applied
  it to the tip (`4090c3d`) to conclude "all 64 classes → `kengaku`". A row whose true owner is a
  sibling would need a sibling path in its `source`/`close`; none exists (sweep in §2).
- I tested cwd dependence on three checks only (§7); I did not run the full 71-check set, so I do
  not know how many rows a cwd-sensitive check would sink, nor whether any check needs a clone.
- I did not audit the truth of the 71 rows' `note`/`close` prose — only their owner class; that is
  the attribution and critic seats' ground.
- `unowned:integrator` is a value in the counter's vocabulary, not a lane: rows using it are not
  "routed" in the fleet sense and must not carry a `next` naming a lane.

VERDICT: fleet-process classes are owner-resolvable from quoted protocol text — `protocol` owns
closure/MANIFEST/registry-home-above-aggregator/fleet-wave artifacts, `aggregator` owns the durable
routed-defect queue, corpus review and `round-*-aggregator-*` files, `unowned:integrator` owns the
non-author spot-check duty, the `WAVE-DONE`/results marker and operator-side files, and `kengaku`
owns every artifact in its own repo including all 71 current rows; two named ownership sources in
the seat brief (`protocol-shokunin/PROVINCE.md`, `aggregator-shokunin/PROVINCE.md`) do not exist,
and the frozen counter's owner vocabulary is a hardcoded 17-name set that excludes seven rostered
lanes (prose/code contradiction, flagged for the L1 and the C2 attackers) — while the working tree
already carries an uncommitted edit to that frozen instrument that widens the owner universe to
directory existence, moves `--run-checks` cwd from scratch to the lane root and raises the timeout
to 90 s, none of which the frozen claims file declares (§7).
