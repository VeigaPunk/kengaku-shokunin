# SiblingOverlap — round-68 w1: sibling-overlap scan for the two declared surfaces

Seat: SiblingOverlap (connector, leaf, read-only). Date: 2026-11-03.
Assignment: scan the sibling lanes at their current tips for (a) offline replay of benchmark graders over a
localhost service, (b) correction-gate instruments for routed defects, (c) the pip/urllib3 rendering chain;
re-check the round-37 own-gate-mutation ruling at current tips; classify each hit surface-level vs term-level.

Bounds observed: wrote only this file; scratch root `/fast/scratch/hyaku/kengaku-r68/SiblingOverlap`
created and removed, no artifact kept; no probe or gate executed (executor/mutation seats own that, and
`--selftest` would duplicate them); nothing bound or contacted on `127.0.0.1:8080`; no git/jj mutation; no
package install. Inputs read: `plans/round-68-claims.md` in full (306 lines); the receipt of record
`corpus/evidence/round68/pypi/receipt.txt` in full; the round-63 probe's docstring and bwrap runner (the
machinery R68-C1 imports); the two frozen instruments and the per-case evidence verified present (sizes
only, not executed); and the in-wave reports `RenderingTrace.md`, `SourceOpen.md`, `gate/red-before.txt`.

## 0. Verdict

No sibling lane owns, claims or contests any of the three scanned surfaces. Every hit is a term-level
adjacency (the fleet shares the *mechanics*: sandboxed children, mutation batteries, correction/obligation
gates, loopback fixtures, receipt re-derivation), and each lane's instance is over its own ground. The
round-37 ruling — mutation-testing of a lane's own gate is a fleet-wide pattern, not kengaku ground — still
holds at the current tips of both named instruments.

## 1. Tips pinned (read-only: `git -C <lane> rev-parse --short=10 HEAD`, 2026-11-03)

| lane | tip | lane | tip |
|---|---|---|---|
| tameshi | `f20ba482c7` | kasegi | `c81eef717e` |
| kumitate | `3c36933621` | kake | `ced2878a1e` |
| kotoba | `1c8f37edf2` | tabi | `7032914cb5` |
| chousa | `f748abbb6b` | souji | `8c27791a16` |
| kagi | `6191805a47` | kaidoku | `c99e907cb5` |
| kama | `6035e952c2` | tsukuroi | `ffd139e4e0` |
| mori | `84c6cbc3b4` | protocol + aggregator | fleet root `82cab2382f` |
| kengaku (self) | `d5b3c3090d` detached; `master` `d2ed4ca3` | | |

The freeze commits `a8883187` (instruments, claims, wave spec) and `d5b3c309` (check-receipt flag) sit on
the detached wave tip; the claims' base remains `master` `d2ed4ca3`. Read-only seats write to the wave dir
regardless of tip.

## 2. Method and classification rule

- **surface-level** — a sibling `PROVINCE.md`/`SKILL.md`/`corpus/knowledge` entry claims the same object
  (executing a benchmark grader's own tests; a correction gate over *kengaku's* routed defects; the
  pip/urllib3 renderer), or a sibling instrument's subject is a round-68 artifact. These would be routed
  (named owner + what is routed).
- **term-level** — the lane holds a named, committed instrument or corpus claim that implements a *term* of
  the surface (replay of frozen rows, sandboxed child, mutation battery, correction/obligation gate,
  loopback service fixture, routed-defect re-derivation), with the lane's own ground as subject. Noted,
  not routed.
- **none** — no instrument, claim or surface statement touches the term.

Recorder commands (from `/home/vgpnk/Projects/shokunin`; exact outputs):

```
grep -rIl -i 'urllib3' */corpus/knowledge */SKILL.md | grep -v '^kengaku-shokunin/' | wc -l            -> 0
grep -rIn -iE '\bgrader\b' */PROVINCE.md */SKILL.md | grep -v '^kengaku-shokunin/' | wc -l            -> 0
grep -rIn -i 'pep 503\|simple index\|offline replay' */PROVINCE.md */SKILL.md \
  | grep -v '^kengaku-shokunin/' | wc -l                                                              -> 0
grep -rIil 'terminal-bench\|terminal_bench' */corpus | grep -v '^kengaku-shokunin/'                  -> 2 files,
   kumitate corpus/knowledge/multi-agent-coordinator-topologies.md and corpus/lessons/round-63.md only
grep -c '^| D-' .ufo/reports/AGGREGATE.md                                                             -> 165
wc -l < kengaku-shokunin/corpus/defects.jsonl                                                         -> 5
grep -c 'R67\|round-67\|round_67' kengaku-shokunin/corpus/defects.jsonl                               -> 0
```

The `\bgrader\b` zero and the corpus-only Terminal-Bench pair are the load-bearing facts for (a): the only
sibling corpus text that names TB2 cites its published results as orchestration data
(`multi-agent-coordinator-topologies.md:29,53,83` — "Terminal-Bench (2 tools): Independent +1.7% (0.350) vs
SAS 0.344"), never grader execution. This reproduces the round-37 scan's finding at the current tip.

## 3. The round-37 precedent, re-checked at current tips

The ruling text is kengaku's own committed record — `PROVINCE.md` (round-37 "Reported out", lines 283-286):
"mutation testing of a lane's own gate is a fleet-wide pattern, not kengaku ground — tameshi's
`tools/mutate-and-run.sh` and kumitate's `gate-mutants.mjs` are the precedents
(`.ufo/waves/round-37/build/R37ConnSibling.md` §S4); the round-37 harness is scoped to `plans/pkg_gate.py`."

| instrument | state at tip | evidence |
|---|---|---|
| tameshi `tools/mutate-and-run.sh` | present, last touched `6d8c11e3` (round-51); ten recorded legs replayed at pinned revisions (`js-kimi-census` … `bash-drift-pins`) | `tools/mutate-and-run.sh:1-30,80-100` |
| kumitate `scripts/gate-mutants.mjs` | present, last touched `84cb1d5d` (round-43); contract `kumitate-gate-mutants-v2`, kill predicate K43, `TARGETS = ['cite-check','wave-census']` (its own gates) | `scripts/gate-mutants.mjs:1-40` |
| tameshi ownership clause | "every lane's gate remains its own; tameshi owns only the reusable craft … Never edits a sibling's gate code" | `PROVINCE.md:14-17` |
| tameshi service offer | any lane may request a sweep; "absorption stays with the gate's owner" | `corpus/knowledge/service-optin-protocol.md:1-25` |

**Status: the ruling holds.** R68's `--selftest` red fixtures (the fabricated all-P receipt for C1; the five
E1–E5 red fixtures for C2) are applications to kengaku's own *new* instruments, inside the pattern's scope.
No round-68 artifact advertises the mutation battery as the round's new ground — C1's capability is
`offline-network-service-grader-probe`, C2's is correction landing. If integration text ever states the
red-fixture battery itself as the capability, that would re-open the r37 ruling; nothing in the frozen
claims or wave drafts does.

Also re-checked, because R68-C1 is a per-case bwrap sandbox: the round-38 split is still committed —
kumitate owns the *runner* (bounded, env-cleared, PID-namespaced child and its verdict line); "kengaku's
per-case sandbox is a consumer pattern of the same class and cites it; kengaku does not re-specify caps,
scopes or bind policy" (`PROVINCE.md:336-340,367-368`). R68-C1 imports the committed round-63 probe
("one implementation … not a copy", claims §Instrument), so it re-specifies nothing; the split is preserved.

## 4. Scan table — hits only

Class: `surface-level` / `term-level`. Strength: `direct` = committed instrument/claim implements a
distinctive term; `weak` = shares a generic term only. `Routed?` answers the assignment's rule.

| # | sibling (tip) | surface | class | strength | routed? | basis at tip |
|---|---|---|---|---|---|---|
| 1 | tameshi `f20ba/*` | (a) offline replay / sandboxed-child execution | term-level | direct | no | `mutate-and-run.sh` replays 10 frozen legs at pinned revisions (exit-graded); `defect-probes` runs guard-removal mutants' children under bwrap, and `env-diff.py` runs commands under bwrap (per kengaku's committed r38 prior-art block, `kengaku PROVINCE.md:318-322`); `tools/registry-replay.py` replays frozen registry requirements |
| 2 | tameshi `f20ba/*` | (b) gate-mutation/fixture method; routed-item disposition | term-level | direct | no | owns the reusable craft only, never a sibling's gate (`PROVINCE.md:14-17`); `tools/evidence-disposition.py` gates "every frozen expected check accounted for exactly once"; `corpus/routed-defects.json` (`tameshi-routed-defects-v1`, round 58) is a lane-local routed-defect ledger with status + evidence per item |
| 3 | kumitate `3c369/*` | (a) bounded runner / per-case sandbox mechanics | term-level | direct | no | `scripts/cap-run.mjs` is the fleet's bwrap runner (`kengaku PROVINCE.md:336-340`); r38 split names kengaku's sandbox a consumer pattern |
| 4 | kumitate `3c369/*` | (b) own-gate mutant battery | term-level | direct | no | `scripts/gate-mutants.mjs`, contract `kumitate-gate-mutants-v2` (K43), targets its own `cite-check`/`wave-census` only |
| 5 | kotoba `1c8f3/*` | (b) own-record correction verifier | term-level | direct | no | PROVINCE Core: "appended correction of this lane's own committed record" counted by `verifiers/check_scoped_rules_v32.py --self-test` (`PROVINCE.md:27`); no routed-defect gate |
| 6 | chousa `f748a/*` | (b) defect/claim audit gates | term-level | weak | no | `tools/quarantine-check.py` re-derives its own absent-defect-register slice + frozen decision rule; `freeze-check.py`, `claims-audit*.py`, `receipt-pin.py` are claim/receipt gates, not correction gates for verifier-routed defects |
| 7 | chousa `f748a/*` | (c) CPython `http.client` | term-level | weak | no | `corpus/SOURCES.md:64` S054 = `http.client.HTTPConnection` **documentation**, timeout semantics, tier A, `mined`; not the renderer (see F1) |
| 8 | kagi `61918/*` | (a) pinned-receipt replay | term-level | weak | no | `corpus/release-clock.py` "replays the **pinned round-26 rearmed receipt**, not live vendor truth" (`SKILL.md:48`) |
| 9 | kagi `61918/*` | (b) closure-obligation gate | term-level | direct | no | `corpus/closure-dispositions.py`: "Turn a non-author closure's decisions into a machine-checked obligation set" — one typed disposition per routed defect D1–D9, pointer resolution, closure sha256 pinned; over its own closure record |
| 10 | kama `6035e/*` | (a) offline capture replay + `:8080` listener census | term-level | direct | no | `tools/kama-ollama-evidence.py` (offline Ollama capture replay; `PROVINCE.md:17`); `PROVINCE.md:11` pins omp's `http://127.0.0.1:8080` fallback consumer row; r65 endpoint census observes `127.0.0.1:8080` (connection refused, no listener). Refuses model quality/eval -> kengaku (`PROVINCE.md:42`) |
| 11 | kasegi `c81ee/*` | (b) routed-defect counter | term-level | direct | no | `corpus/instruments/r45-routed-defects.py`: counts exactly the five status-bearing routed defects of its own round-44 spot-check §6 and excludes the self-reported item 6 — the same counted-set shape as R68-C2's items 1–5 |
| 12 | kake `ced28/*` | (a) receipt replay / saved-response offline audit | term-level | weak | no | `scripts/receipt_replay.py` replays frozen round-23 receipt sets at one revision with named rejections; `scripts/header_audit.py`/`base_path_audit.py` audit saved GET bytes offline (`PROVINCE.md:33-35`) |
| 13 | tabi `70329/*` | (a) self-launched loopback service fixtures | term-level | direct | no | Chromium/WebView2 on "ephemeral loopback" CDP endpoints (`PROVINCE.md:37-59`); loopback HTTP fixture, not a grader |
| 14 | tabi `70329/*` | (b) own-gate mutant + cited-receipt checks | term-level | weak | no | `scripts/check-gate-mutants.mjs`, `check-cited-receipts*.mjs`, `check-source-reopen-receipt.mjs`; its open L0 (fleet `.ufo/l0-questions.md:199`) is the frozen-gate vs routed-fix conflict family (F4) |
| 15 | kaidoku `c99e9/*` | (b) routed-defect -> instrument | term-level | direct | no | `SKILL.md:1848` (`tools/round-59/annotation-audit.py`) reconstitutes "the r58 closure's routed defect D58-1 as an instrument" over its own receipt annotations |
| 16 | kaidoku `c99e9/*` | (c) PyPI wheels as RE carriers | term-level | direct | no | reads PyPI wheel members as carriers (uv 0.13.0 rust-auditable wheels, `PROVINCE.md:343`; pyproj SQLite, `:356`); refuses installing Python packages (`PROVINCE.md:110`); no pip install/render claim |
| 17 | tsukuroi `ffd13/*` | (b) correction-conformance gate | term-level | direct | no | `tools/check-root-dac-correction.py`: "Narrow, read-only round-13 correction-conformance gate (not a semantic proof)", exit 0/1/2, `--selftest` with in-memory doc fixtures + mktemp git sandbox; plus source-scope/journalctl correction checks — all its own knowledge-base corrections |
| 18 | mori `84c6c/*` | (a) bwrap-sandboxed counter | term-level | weak | no | `count-c2-a1.py` runs its tool under `bwrap --ro-bind / / --tmpfs /home --tmpfs /fast` (`kengaku PROVINCE.md:331`); sandbox mechanic, no service/grader |
| 19 | mori `84c6c/*` | (b) routed-item re-derivation | term-level | direct | no | `tools/mori-routed-check.py`: re-derives round-23 routed items R1–R4 at a committed revision, "every predicate reads git objects only … the working tree is never consulted" — the re-deriving-receipt discipline R68-C2 uses |
| 20 | protocol `82cab/*` | (b) correction/queue rule owner | term-level | direct | no | `PROTOCOL.md:123-137,366-367` (append-only corrections, named correction entries); `:245-249` (routing lines, durable routed-defect row, "the ledger row … is the durable queue"); `.ufo/gates/root-ledgers.py` is a protocol-lane **ledger-identity** gate, not a correction gate |
| 21 | aggregator `82cab/*` | (b) durable routed-defect ledger owner | term-level | direct | no | `PROTOCOL.md:245-249` mirrors each routed defect into the owning repo and keeps an open ledger row until the correction lands; ledger `.ufo/reports/AGGREGATE.md` carries 165 `D-` rows, last commit `f47ad6ba` (2026-10-25, tree restore; content 2026-10-19) — no instrument over correction content |

## 5. Coverage appendix — every named lane

| lane | surfaces checked | result | what was read |
|---|---|---|---|
| tameshi | (a) (b) (c) | (a) term-direct, (b) term-direct, (c) none | `PROVINCE.md:3-20,38-45,75-83,101-112`; `tools/mutate-and-run.sh:1-30,80-100`; `tools/registry-replay.py:1-25`; `tools/evidence-disposition.py:1-12`; `corpus/knowledge/service-optin-protocol.md:1-25`; `corpus/routed-defects.json` |
| kumitate | (a) (b) (c) + wave arrangement | (a) term-direct, (b) term-direct, (c) none; arrangement is its knowledge surface, round-68 wave is kengaku's L1 under fleet `scripts/hyaku/ufo-wave-policy.json` (not a kumitate lane gate) | `PROVINCE.md:1-38`; `scripts/gate-mutants.mjs:1-40`; `git log -1` over `gate-mutants.mjs`/`cap-run.mjs`; `corpus/knowledge/multi-agent-coordinator-topologies.md:29,53,83`; `corpus/lessons/round-63.md:11-19` |
| kotoba | (a) (b) (c) + sibling census | (a) none, (b) term-direct, (c) none; its `sibling-overlap-census-round74.md` is its own-boundary census (20 lanes at frozen heads, "reports sibling scope … edits no sibling"), not a fleet arbitration service — noted, not counted | `PROVINCE.md:13-35,44-77`; `corpus/knowledge/sibling-overlap-census-round74.md:1-40` |
| chousa | (a) (b) (c) | (a) none, (b) term-weak, (c) term-weak | `PROVINCE.md` (full, 17 lines); `corpus/SOURCES.md:64`; `tools/quarantine-check.py:1-20`; tools listing |
| kagi | (a) (b) (c) | (a) term-weak, (b) term-direct, (c) none | `PROVINCE.md:13-38,53-81`; `corpus/closure-dispositions.py:1-18`; `SKILL.md:48` |
| kama | (a) (b) (c) | (a) term-direct, (b) none, (c) none | `PROVINCE.md:9-42,59-75,100-103`; `corpus/lessons/round-65.md:7,21` |
| kasegi | (a) (b) (c) | (a) none, (b) term-direct, (c) none (its r57 `http.client` TLS note is one wave observation, not a surface) | `PROVINCE.md:1-52`; `corpus/instruments/r45-routed-defects.py:1-20` |
| kake | (a) (b) (c) | (a) term-weak, (b) none, (c) none | `PROVINCE.md:26-36,94-110,141`; `scripts/receipt_replay.py:1-22` |
| tabi | (a) (b) (c) | (a) term-direct, (b) term-weak, (c) none | `PROVINCE.md:37-136`; `scripts/` listing (`check-gate-mutants.mjs`, `check-cited-receipts*.mjs`, `check-source-reopen-receipt.mjs`); `.ufo/l0-questions.md:199` |
| souji | (a) (b) (c) | none — hygiene surfaces only (fleet/lane removal receipts, Obsidian ledger; refuses secrets -> kagi) | `PROVINCE.md:1-55`; `tools/` listing |
| kaidoku | (a) (b) (c) | (a) none, (b) term-direct, (c) term-direct | `PROVINCE.md:102-110,135,343,345,356,465`; `SKILL.md:1845-1848` |
| tsukuroi | (a) (b) (c) | (a) none, (b) term-direct, (c) none | `PROVINCE.md:1-30`; `tools/check-root-dac-correction.py:1-20`; tools listing |
| mori | (a) (b) (c) | (a) term-weak, (b) term-direct, (c) none | `PROVINCE.md:125-126,150,200`; `tools/mori-routed-check.py:1-25`; tools listing |
| protocol | (a) (b) (c) | (a) none, (b) term-direct (rule owner) | `PROTOCOL.md:123-137,236-262,289-322,365-367,407-411,429-433,462-469`; `.ufo/gates/root-ledgers.py:1-25` |
| aggregator | (a) (b) (c) | (a) none, (b) term-direct (ledger owner) | `PROTOCOL.md:245-249`; `.ufo/reports/AGGREGATE.md` (`D-` row count; `git log -1`) |

Outside the named list, spot-checked and excluded: **revenger** (`PROVINCE.md` refuses "harness/evidence
auditing"; "does not take ownership of generic harness gates") — no hit; **mado**, **kotodama** appear only as
sandboxed-counter precedents in kengaku's own round-38 block, no r68 surface; **kengaku** itself owns (a) via
`service-grader-probe` (SCORECARD:567) and the pip chain via rounds 63/64 (the only lanes whose recent
lessons mention pip/urllib).

## 6. Tally

OVERLAP surface-level=0 term-level=21 routed=0

Breakdown: term-level direct = 15 (rows 1, 2, 3, 4, 5, 9, 10, 11, 13, 15, 16, 17, 19, 20, 21), term-level weak =
6 (rows 6, 7, 8, 12, 14, 18). Per surface: (a) 7, (b) 12, (c) 2. Nothing met the surface-level test, so
nothing is routed; no named owner is asked to cede anything.

## 7. Second-order findings for the L1 (claims not edited)

**F1 — attribution split, reported in-wave, not my verdict.** `RenderingTrace.md` §5 measured that the
renderer of `HTTPConnection(host='localhost', port=8080)` is urllib3 2.7.0
(`pip/_vendor/urllib3/connection.py:163-164`, vendored sha `668b37ab…a1532`), not CPython's
`http.client.HTTPConnection` (which has no `__repr__`/`__str__`; S240 supports only base-class/field
separation). The capture that seat measured carries sha `dedbc20d70cc29…375d`, equal to the receipt's K2
`stderr_sha256` line — so the attribution finding is over the exact bytes the receipt binds. Scan
consequence: surface (c) is urllib3, and the only sibling term in the family — chousa's S054 — is CPython
*documentation* at the docs tier (timeout semantics), not the code path that rendered the bytes. No sibling
holds the urllib3 renderer; a re-source creates no overlap (see §8).

**F2 — the durable routed-defect ledger has no round-67 rows.** kengaku's `corpus/defects.jsonl` holds 5
rows, all R34-D1..D5 closed in round 35 (`grep -c 'R67\|round-67\|round_67'` -> 0), so the lane's own
`routed-defect-ledger` capability (SCORECARD:563, `plans/defect_ledger.py` over that file) cannot re-run the
five round-67 items. Fleet-side, the aggregator ledger's last commit is a 2026-10-25 tree restore with
2026-10-19 content. Precedent for the alternative: tameshi keeps `corpus/routed-defects.json`
(`tameshi-routed-defects-v1`) with one status+evidence row per closure-routed item. R68-C2's artifacts
(errata, tally, registry, gate) are a different instrument; whether the five rows also belong in a durable
lane ledger is an L1 decision, not a defect in the frozen predicate (E1–E5 do not read that file).

**F3 — `:8080` is kama's observation ground, not its fixture ground.** kama owns read-only listener
discovery (`ss -ltn` classification) and records `127.0.0.1:8080` as omp's inherited fallback consumer row;
its r65 census observes 8080 connection-refused. R68-C1's index is a lane fixture the probe starts and stops
(with `require_port_free` per case), not a serving-plane claim, and this wave's host guard already assigns
8080 to the L1 battery. No conflict and no route; the round report's ownership statement is what keeps a
later reader from reading the fixture as kama's surface.

**F4 — a live fleet precedent for the correction-vs-frozen-gate boundary.** tabi's open L0
(`.ufo/l0-questions.md:199`) asks whether a routed fix supersedes a refused round's frozen counting gate.
R68-C2 avoids that family: it appends dated errata and a new gate rather than rewriting the round-67
predicates, and the gate re-hashes committed bytes. Worth one line in the calibration note; nothing to
route.

**F5 — protocol/aggregator division is rule + ledger, not instrument.** The protocol lane owns the
append-only correction rule and the routing line; the aggregator owns the durable row. Neither owns a gate
over correction content, so R68-C2's lane-local gate neither duplicates nor trespasses. Presenting the C2
gate as a fleet instrument would misstate that division; the scan found no such claim.

## 8. One bounded proposed move (for the L1; not applied)

Re-source surface (c) to the object that actually rendered the bytes: carry the renderer as urllib3 2.7.0
(S241b, `pip/_vendor/urllib3/connection.py:163-164`, sha `668b37ab12835bdf8643a695a9f050551339b280742231f163fc575a925a1532`)
in the knowledge-entry addendum and the S240/S241 rows, narrowing S240 to base-class/field separation. The
frozen K2 clause, predicate, receipt and probe bytes stay untouched (the conclusion is unchanged; only the
attribution moves). Do **not** re-source to CPython `http.client` documentation: chousa's S054 already holds
that term (F1), and it is not the renderer.

- Affected axes: coverage (C1's sourced duty becomes true) improved; calibration (C2) unchanged and
  unharmed; no sibling surface harmed — the scan shows no lane holds urllib3.
- Risks: the frozen claims text cannot be edited, so the correction must ride an appended erratum/entry
  section; the receipt and `--check-receipt` bytes must not change; if the round report re-words F1 without
  the erratum, it reads as a post-data rule change.
- Verification: `grep -c 'urllib3'` on the new entry >= 1 and the located quote/sha above present; S240 row
  scope reads base class + `_get_hostport` field separation only; `python3 plans/round68_c1_pypi_finish.py
  --check-receipt corpus/evidence/round68/pypi/receipt.txt` still exits 0 (no receipt bytes touched).

## 9. Observed at yield (not this seat's artifact; not adjudicated)

Working-tree state at 2026-11-03 after this scan: `plans/round68_c2_correction_gate.py` carries an
uncommitted change (`git diff --numstat` -> `8 2`; the freeze commit is `d5b3c309`/`a8883187`). It is not
mine — this seat wrote only this file — and it means the instrument bytes in the tree are not the freeze
bytes while the wave runs. No content was read or judged here; the sentinel/reviewer seats and the L1 own
that question.

## 10. Five-line summary

1. Verdict: `surface-level=0 term-level=21 routed=0`; no sibling owns, claims or contests (a), (b) or (c).
2. The round-37 own-gate-mutation ruling holds at tips (tameshi `f20ba482c7`, kumitate `3c36933621`); R68's
   red fixtures are in-pattern applications scoped to kengaku's own new instruments.
3. L1 integration: cite the lane-local precedents — kagi `closure-dispositions.py`, mori
   `mori-routed-check.py`, kasegi `r45-routed-defects.py`, tsukuroi `check-root-dac-correction.py` — and keep
   kumitate's runner as the consumer pattern (r38 split).
4. Reported contradiction (not this seat's verdict): the renderer is urllib3, not CPython S240; §8 proposes
   the append-only re-source that touches no frozen byte.
5. Finding: kengaku `corpus/defects.jsonl` has 0 round-67 rows and the aggregator ledger predates round 67
   (last commit a 2026-10-25 tree restore); whether the five defects get durable ledger rows is the L1's call (§F2).
