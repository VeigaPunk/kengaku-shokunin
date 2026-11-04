# ConnectorR81 — sibling-overlap scan, kengaku round 81 w1 (read-only)

Scope: the three mechanism families named in the seat item, grepped lane-locally across all 20
sibling repos under `/home/vgpnk/Projects/shokunin/*-shokunin/`, plus gate registries and the
S255–S261 id/URL collision check. Everything below was read from the sibling repos' working trees
(no sibling clone was made; none needed) and from kengaku at the tip of scan time,
`805a65c836f745703e5c1652d10ce8e55043265b` (`git rev-parse master`; freeze `4d896e0d…`, base
`4e833e9f…` untouched). Method: one regex grep per pattern with `path` = the 20 sibling lane roots
(excluding kengaku and the fleet root), then file-level `read` of every cited pin to confirm it
still holds at today's bytes. Load-bearing zero results, stated as run:

- `MINTED_BY` → **0 hits** in all 20 sibling repos.
- `WORKTREE clean` → **0 hits** in all 20 sibling repos.
- `HOST_PYTHON|HOST_OPENSSL` → **0 hits** in all 20 sibling repos.
- `routed-findings` → hits only in tameshi wave reports *about* kengaku
  (`tameshi-shokunin/.ufo/waves/round-50/w1/T50ConnSiblingDefects.md:64-68,169-173`,
  `round-57/w1/T57W1ConnectorSiblings.md:7,21-22`); no sibling operates a kengaku-shaped registry.
- `merge-base --is-ancestor` → widespread as commodity git audit furniture (examples:
  `audio-shokunin/reports/round-63/r63-reviewer.md:20,111`, `round-64/r64-verifier.md:83-84`,
  `round-94/r94-scribe.md:29-30`; `chousa-shokunin/.ufo/waves/round-26/falsify/FRegistryExactPath.md:12`,
  `round-29/falsify/RerunCounterA.md:12-15`); as **committed gate logic** only in the kama/tabi/mori
  instruments below. Fleet-root `MANIFEST.json` and `.ufo/prompts/closure/*` hits are fleet records
  and prompt templates, not lane mechanisms; excluded from the per-lane rulings.

## 1. Mechanism matrix (path:line re-verified 2026-11-04 unless marked)

### (a) Offline replay of a captured grader with a subject-locating receipt — no sibling owns it

Nearest sibling relatives, each ruled adjacent-but-different:

- **kumitate** `scripts/receipt-evidence.mjs:180-203` (registry row `receipt-evidence`,
  `SKILL.md:~622`): re-spawns each receipt's recorded argv inside a `git archive` extraction of the
  judged rev and compares exit + stdout/stderr sha256, plus a nonce sweep against rounds 48–57.
  Replays *its own lane's* commands; the subject is never a captured third-party grader and there
  is no subject-capture sha pin. Adjacent-but-different.
- **kumitate** `replay71-probe` row (`SKILL.md:~633`): replay of its own frozen round-69 controls.
  Same ruling.
- **kama** `tools/round72-receipt-tip-binding.py:50-83`: classifies a receipt as
  stale/unbound/shifted/bound from its `tip=`/`rev=` header (`git cat-file -e`,
  `merge-base --is-ancestor`, intervening-drift classes). Locates a receipt in history; replays
  nothing. Adjacent-but-different.
- **tabi** `scripts/check-measurement-binding.mjs:569-623`: binds a counter + counted inputs +
  measuredRevision (ancestor check, counter digest at two revisions, argv-shape support). Evidence
  binding, not subject replay. Adjacent-but-different.
- **mori** `tools/mori-retention-reconcile.py:159-188`: receipt wrapper schema
  `mori-r21-command-receipt-v1`, `measured_revision` ancestor check, policy/allowlist byte equality
  between measured and judged revisions. Adjacent-but-different.

Terminal-Bench 2.0 grader replay (round-52 captures, subject-capture sha, offline test-function
import) is kengaku-exclusive by province: `PROVINCE.md` round-35/36/37 partial frontier admissions
own exactly this activity for pinned TB2 graders. No sibling repo contains any TB2 grader-replay
instrument (see §3 for the only TB2 URL occurrences in sibling bytes — borrowed fixture copies).

### (b) Host-state pin (`python3 -V` / `openssl version`) in a receipt — zero siblings; new this round

`HOST_PYTHON|HOST_OPENSSL` has no hit in any sibling repo. It exists only in kengaku, landed this
round: receipts `corpus/evidence/round81/log-summary-date-ranges-probe.txt:7-8` and
`corpus/evidence/round81/vulnerable-secret-probe.txt:7-8`; counter
`plans/round81_c1_new_members.py:78-80` (REQUIRED tuple), `:139-140` (`host_values`),
`:329-334` (`HOST-PYTHON-MISMATCH` / `HOST-OPENSSL-MISMATCH`), `:553` (host-python mutant);
driver `plans/round81_c1_remint.py:90-91,130-138`; criterion `corpus/QUALITY.md:1293-1297`;
LOG `LOG.md:3134-3136`. Round-80 receipts (`corpus/evidence/round80/*-probe.txt:1-13`) carry
`MINTED_BY_SHA` but no host pin — confirming the claims' framing that this is R81's successor
addition, not a fleet-standard field. No owner collision; nothing to route.

### (c) Routed-finding registry whose checks must fail at a base revision — kengaku owns the mechanism; siblings are adjacent-but-different

Owner of the shape this round uses: kengaku (`corpus/routed-findings.jsonl`;
`plans/routed_open.py` / `plans/round51_routing.py` / the R79/R80/R81 C2 debt counters with the
mechanical sensitivity leg that reverts each row's evidence to base and requires that row's check
to fail there). Per-lane nearest mechanisms:

- **kotoba** `verifiers/check_r63_routed_repairs.py:77-81`: `BASE_REV` pinned in code — "the
  do-nothing control, pinned in code: the r62 tip, **before any of the five routed corrections**;
  BASE_REV is also the append-only baseline". This is the closest sibling analogue to a check that
  must fail at base — but it is one counter, one code-pinned base, five corrections of one round;
  no per-row `check` field, no mechanical per-row revert. Adjacent-but-different.
- **kama** `tools/gate-registry-check.py:2-37` with its base-failure demonstration
  `.ufo/waves/round-28/w1/out/ExecGateRegistryCheck/commands.sh:12-14` and
  `base-4179301.out` (exit 1 at base `4179301f`, unregistered counters): a committed check shown
  able to fail at a base revision — but attached to *registry completeness*, not to a routed
  findings ledger. Adjacent-but-different.
- **kagi** `corpus/closure-dispositions.py:1-43`: typed dispositions over one round's routed
  defects, `source_sha256` pin, `fixed` rows must carry a resolving pointer that names the id.
  Resolves at the tip; no base-failure leg, no executable check string. Adjacent-but-different.
- **kaidoku** `SKILL.md:986` (`routed-defects | gate / kaidoku` — the round-18
  `routed-defects.py --strict` over six R17 defects) and `SKILL.md:1750-1763`
  (`tools/round-45/registry-scope.json` scored by `tools/round-45/c2-counter.py`); the
  `jj-red-before` row at `SKILL.md:989` pins baseline `9011581d`. Named+substance checks for a
  fixed six-defect set, not a rolling per-row registry. Adjacent-but-different.
- **tameshi** `corpus/routed-defects.json:1-17` (schema `tameshi-routed-defects-v1`, statuses
  judged against the tree, evidence rules in `.ufo/evidence/round-50/c1/measure.py`): no
  executable per-row check — matching tameshi's own round-57 scan
  (`T57W1ConnectorSiblings.md:46`: "no executable per-row verification"). Adjacent-but-different.
- **kotodama** `reports/round-14/routed-resolution.json:1-15`: resolutions with evidence + control
  strings; data lineage, no executable check. Adjacent-but-different.
- **kotodama** `tools/check-evidence-coupling.py:1559-1568` (re-read today): compares
  `(expected_exit, sorted(finding_ids))` against a frozen expectation — the attribution primitive
  kengaku's round-75 report-out already inventoried. Duplicate at the primitive level only;
  different subject (evidence coupling, not routed debt).

Gate registries (the item's "and their gate registries"): every lane keeps its own —
chousa `SKILL.md:83-86` (`research-gate` rows with exit maps); kama's SKILL registry policed by
`tools/gate-registry-check.py`; kaidoku `SKILL.md:986-989` + `:1750-1763`; kumitate
`SKILL.md:611-633` (the largest: `readme-map`, `receipt-evidence`, `receipt-attest`,
`source-capture`, `source-dupes`, `replay71-probe`, …); kengaku's own §Gate/probe registry
(128 rows per the round-79 report). souji's exit-column registry and tameshi's expected-exit
JSON rows are cited from committed scan bytes (`tameshi-shokunin/.ufo/waves/round-57/w1/T57W1ConnectorSiblings.md:42,60`)
and were not re-verified at today's tip. `audio-shokunin/SKILL.md` and
`game-dev-2d-shokunin/SKILL.md` do not exist at repo root (grep reported both paths missing).
No fleet-wide registry standard exists; a would-be standard's owner is protocol/integrator
(per the round-10/11 referrals recorded in `PROVINCE.md` and the round-75 `SiblingR75` report-out).

## 2. Rulings — duplicate / adjacent-but-different / absorbable, and owners

| Overlap | Ruling | Owner / disposition |
|---|---|---|
| Routed-findings registry with per-row executable checks | **adjacent-but-different** in kagi/kotoba/kaidoku/tameshi/kotodama; the kengaku shape (per-row `check` + sensitivity leg) is unowned elsewhere | kengaku keeps its gate (product-lane bookkeeping; `PROVINCE.md` "every lane's gate remains its own"). A fleet-wide routed-registry **standard** belongs to protocol/integrator — referred again here, not imposed |
| Receipt-to-revision binding (kama/tabi/mori) | **adjacent-but-different** (locates/binds; never replays a captured subject) | Already routed/inventoried in the round-75 `SiblingR75` PROVINCE report-out (`PROVINCE.md`, round-75 section). No new line needed |
| Env pin `HOST_PYTHON`/`HOST_OPENSSL` | **novel** — zero siblings; no owner collision | kengaku's successor predicate this round. If the fleet ever standardizes receipt schemas (kagi `source_sha256`, kumitate `receipt-attest` v3 field-whitelist, kengaku env pin all converge), protocol/integrator owns it — referral only, nothing absorbable now |
| Offline replay of a captured grader | **kengaku-exclusive**; kumitate's `receipt-evidence.mjs` is the nearest foreign relative | In-province (TB2 grader readings, `PROVINCE.md` round-35/36/37). Nothing absorbed |
| `merge-base --is-ancestor` | **duplicate only as a commodity primitive** (git's own); no mechanism-level duplicate | No action; citing a primitive is not absorbing a mechanism |
| Gate registries | **adjacent-but-different** per lane; kumitate's is the largest and pins its own duplicate-URL groups (`source-dupes` row) | Every lane keeps its own; fleet standard (if ever) → protocol/integrator |

One non-obvious observation for the L1, cited not adopted: kumitate's `source-dupes` gate already
mechanizes the "same normalized URL claimed under differing scopes" problem *within* a lane
(`kumitate-shokunin/SKILL.md:~632`, contract `kumitate-source-dupes-v1`). If the fleet ever wants a
cross-lane URL-dedupe check over the per-lane registries, extending that primitive — not writing a
new instrument — is the cheapest route. Nothing this round absorbs it.

## 3. SOURCES ids S255–S261 and URL collisions — count 0

Id numbers are lane-local namespaces; sibling lanes occupy S254–S261 with entirely different
documents (all re-read today): kaidoku `corpus/SOURCES.md:170-181` (git-show/git-cat-file/
git-ls-tree/GFM/grep manual/subprocess/git-diff/gitrevisions/hashlib/jsc2js), kotodama
`corpus/SOURCES.md:282-293` (masks/museums), revenger `corpus/SOURCES.md:268-279` (decompilers),
souji `corpus/SOURCES.md:213-224` (Python docs/gvfs/worktree.c/symlink), tameshi
`corpus/SOURCES.md:130-139` (GoogleTest/flaky-test papers), tsukuroi `corpus/SOURCES.md:262-274`
(POSIX/bash/grep/Windows commands), mado `corpus/SOURCES.md:221-225` (own-work + Hyprland).
Numeric overlap is by design not a collision; the per-lane census is the registry's authority and
cross-lane dedupe happens only in shokuknow merges, by document.

The external URLs kengaku round 81 opens are S261's four pinned files
`raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88…/{log-summary-date-ranges,vulnerable-secret}/{instruction.md,task.toml}`
(kengaku `corpus/SOURCES.md:277`; S259 `:275` and S260 `:276` are own-work rows, S258/S255–S257
predate this round). Grep of all 20 sibling repos for
`harbor-framework/terminal-bench-2|log-summary-date-ranges|vulnerable-secret`: **no registry row in
any sibling**; `log-summary-date-ranges` and `vulnerable-secret` have zero sibling hits
anywhere. The only sibling occurrences of kengaku's TB2 pins are borrowed byte copies inside wave
artifacts, neither of which claims the URL: `kaidoku-shokunin/.ufo/waves/round-41/w2/artifacts/R41W2Reservation/tx-scan.json:19601`
(an embedded copy of a KengakuR41 seat script, round-41 constraints-scheduling pin) and
`kumitate-shokunin/.ufo/waves/round-63/build/K63RevengerDispatcher/forgery-borrowed/build-dispatch.json:375-431`
(a revenger forgery fixture copied from kengaku round-35 dispatch bytes, protein-assembly pins).
**Collisions: 0.**

## 4. PROVINCE.md adjacency (9, held) — record NOTHING this round

Precedent: adjacency moved 8→9 at round 51 via R51-C2 (`SCORECARD.md:2207,2218`) and every round
since records "adjacency 9 (held; …)" with the connector's sibling scan as the wave's evidence
(`SCORECARD.md:2843,2892,2932,3791,3855`). `PROVINCE.md` gains a "Reported out" line only when
evidence actually leaves the lane (round-9/10/11/12-14/25/75 precedents in the file itself). This
scan routes nothing out, absorbs nothing, and arbitrates no new overlap: the one cross-lane
mechanism family (kama/tabi/mori receipt binding) was already sent out in round 75, and the env
pin has no sibling owner to notify. **Recommendation: no routing line in `PROVINCE.md`; the
SCORECARD axis cell should read "adjacency 9 (held; the connector's sibling matrix is the wave's
evidence)"** in the established wording. A routing line becomes warranted only if a later seat in
this wave sends evidence out; none of the findings above creates that obligation.

## Limits

- Sibling greps ran against the 20 sibling working trees at scan time; no sibling clone or mirror
  was made. Pins marked "re-read today" were opened file-level; souji's SKILL exit-column and
  tameshi's registry-check reference rest on committed tameshi round-57 scan bytes and were not
  re-verified at today's tip.
- `audio-shokunin` and `game-dev-2d-shokunin` have no root `SKILL.md`; their corpus/ surface was
  covered by the repo-wide pattern greps (all zero-hit for the three mechanisms).
- Fleet-root `MANIFEST.json` / `.ufo/reports/` / `.ufo/prompts/` hits are fleet records and prompt
  templates, not lane mechanisms; excluded from rulings but noted where load-bearing.
- Tools installed or upgraded: none (pacman paused host-wide per the orchestrator ruling; nothing
  needed). Scratch `/fast/scratch/hyaku/kengaku-r81/ConnectorR81` was created empty and deleted
  before yield; the only file written in the lane is this report.
