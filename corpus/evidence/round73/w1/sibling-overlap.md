# Round 73 sibling overlap — SiblingConnectorR73

Axes: **coverage (R73-C1)** and **calibration (R73-C2)**. Adjacency report only; no sibling code copied, no predicate or registry changed, and no claim adjudicated.

The frozen `plans/round-73-claims.md` was read in full. The comparison is against its declared contracts: C1 widens the advertised-document universe to `plans/*.md`; C2 derives its population from registry rows and prices their eight fields plus the two erratum bindings. Discovery covered sibling directories across the fleet; the entries below are selected source-backed matches, not a claim that every historical script was exhaustively audited. Paths are absolute; quoted lines are source evidence, not runtime results.

## 1. Registry completeness and schema audits

| Owning lane | Absolute instrument path and line read | Difference from kengaku | Borrow verdict |
|---|---|---|---|
| tabi | `/home/vgpnk/Projects/shokunin/tabi-shokunin/scripts/check-gate-registry.mjs:24-40,219-278`. L29: `convention (check-*.mjs, *audit*.mjs) UNION scripts a`; L37: `For every gate, the LATEST registry row for it in document order wins`. Actual implementation reads a revision tree, constructs the union, checks eight fields, and emits `e1-missing-row`, `e2-field-incomplete`, `e3-row-script-absent`. | Tree/naming-convention population rather than C1's advertised-document population or C2's registry-derived population; header-aware historical table parsing rather than exactly eight positional cells; latest-row-wins rather than C2's every-row/duplicate rejection. | **kengaku owns this** — tabi supplies clear prior art, but its latest-row supersession policy contradicts R73-C2's duplicate rule and must not replace it. |
| kama | `/home/vgpnk/Projects/shokunin/kama-shokunin/tools/gate-registry-check.py:1-60,78-80`. L11: `Population: every tracked path matching`; L57: `HEAD commit tree (git ls-tree -r HEAD, round 69), not` [the index]. | Uses tracked `.ufo/waves/round-*/count-*.py` and `tools/round<N>-*.py`; separates occurrence from meaning with thin-row, empty-entry, empty-exit-map and missing-path defects in its lane's historical table shape. C1 instead counts instruments advertised by selected documents. | **kengaku owns this** — occurrence-plus-meaning is adjacent prior art, while kengaku owns its advertised universe and registry home. |
| kotoba | `/home/vgpnk/Projects/shokunin/kotoba-shokunin/verifiers/check_gate_registry.py:16-50`. L16: `Universe (M): every blob directly under verifiers/ at the revision whose`; L46: `PHANTOM row. The counter does not run verifier scripts or prove their actual` [exit statuses]. | Enumerates Python/shell verifier blobs directly under `verifiers/`; requires exactly one conformant row, rejects phantom rows, checks gate verdict classes, active self-test handlers via Python AST/shell arms, pinned-path existence, scope and owner. Kengaku's D2 accepts substring-backed self-test declarations and nonempty pinned/scope cells. | **kengaku owns this** — this is stronger static field-pricing prior art, not permission to strengthen the frozen R73-C2 rule after scoring. |
| mori | `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-gate-registry.py:5-23,31-48,70-71,180-192`. L5: `the registry file whose header row is the eight standard cells`; L40: `population_digest=<sha256 of the newline-joined` [sorted target list]. | Reads eight-standard-cell tables wherever found, attributes a tool through its entry command, rejects duplicate names and escaping/absent entry paths, checks a real self-test argv branch, and emits a digest of its tree-derived audit population. C2 instead prices every accepted registry row and binds errata. | **borrow** — borrow the population-identity receipt technique as supplementary evidence, without adopting mori's different population or self-test requirements. |
| tsukuroi | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-registry-coverage.py:95-120,262-326`. L115: `for mode, kind, _oid, name in self._tree_entries(revision, "tools/"):`; L319: `REGISTRY-ROW-MISSING`. | Uses recursive committed regular `tools/` files, operative rows, one-tool-per-row attribution, duplicate coverage, orphan rows and declared exit-code checks. Its kinds include `library`, unlike frozen C2's `gate|probe`. | **kengaku owns this** — analogous coverage machinery remains lane-local, and its `library` kind is incompatible with C2's enum. |

## 2. Tree-derived universes versus registry-derived universes

The first five instruments above are concrete tree-derived examples: tabi's naming-convention union; kama's tracked counter patterns; kotoba's direct `verifiers/` blobs; mori's `--audit-all` globs; and tsukuroi's recursive regular `tools/` files. None justifies silently replacing R73-C1's document universe or R73-C2's registry-row universe.

Additional comparisons:

| Owning lane | Absolute path and line read | Difference | Borrow verdict |
|---|---|---|---|
| kotodama | `/home/vgpnk/Projects/shokunin/kotodama-shokunin/tools/source-audit-inventory.py:2-19`. L5: `across corpus/knowledge/**/*.md recursively and emits a deterministic JSON or` [text inventory]; subsequent lines specify per-file SHA256 and occurrence locations. | Tree-derived knowledge-marker inventory, not gate-row conformance; explicitly reports `resolved_scholarship: "not-assessed"` rather than mistaking no markers for verified scholarship. | **not relevant** — useful boundary discipline, but it does not price a gate registry. |
| tameshi | `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/registry-check.py:4-6,20-23,35-38`. L5: `contract surface a cold read runs against; this monitor replays every active`; L35: `A row holds when its exit equals expect.exit AND`. | Population comes from active JSON registry rows, not tree discovery; executes argv directly and checks declared exits/output under timeouts. Kengaku C2 parses/prices declarations without running registered tools. | **not relevant** — runtime replay would introduce dependencies and write-scope exposure outside these two frozen claims. |
| kasegi | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/wave-registry.py:2-10`. L9: `names it holds, so seats= and names= are always consistent.` | Emits a seat registry from wave results; it is neither a gate inventory nor a row-conformance counter. | **not relevant** — the shared word registry does not imply the same population or contract. |

## 3. Outside-observed provenance: actual kama round-50 reader

**Owner:** kama. **Absolute path:** `/home/vgpnk/Projects/shokunin/kama-shokunin/tools/round50-replay-bind-audit.py`.

Read lines 1-83 and 260-290. The actual reader is L271 `def environ_keys(pid):`, with L273 `with open(f"/proc/{pid}/environ", "rb") as fh:`. It returns environment **names**, not values, from NUL-separated process environment bytes. Its declared env leg at L48-51 checks the server and parent for the planted `KAMA_R50_CANARY` and checks that a planted `sitecustomize` marker remains empty. The surrounding counter also joins the observed server PID to the replay receipt, observes executable/listener/model mappings, and checks teardown.

**Difference:** this is a live Linux process provenance witness; kengaku's two claims concern registry/document/script bytes and do not assert that registered commands actually executed. **Verdict: not relevant** — retain it as provenance adjacency, not a reason to add `/proc`, networking, live process execution or canaries to R73's frozen counters. No live process environment was read by this seat.

## 4. Declared-field pricing and protocol closure gates

Kotoba and mori above are the closest row-field-pricing siblings. Protocol owns the outer eight-field standard, not kengaku's lane-local inventory:

- `/home/vgpnk/Projects/shokunin/PROTOCOL.md:398-405` assigns child registries to their own `SKILL.md` and lists name, kind, entry, verdict map, self-test command/spelling, pinned-value path, write scope and owner. This is a schema authority, not evidence that any given lane's rows conform.
- **Protocol**, `/home/vgpnk/Projects/shokunin/.ufo/gates/root-ledgers.py:3-27`: L22 describes `closure_check_row_lost`; the gate checks fleet-root ledger identity and the registered closure-check row within the correctly ordered registry window. It does **not** price every row's eight fields. **Verdict: kengaku owns this** — C2's per-field pricing is not subsumed by protocol's registry-presence guard.
- **Protocol**, `/home/vgpnk/Projects/shokunin/.ufo/waves/round-15/closure-check.py:2-12`: L4-5 says it reads durable closure evidence and reports unresolved, contradicted or missing `rounds[]` ledger rows. Its actual registered command is in `/home/vgpnk/Projects/shokunin/SCORECARD.md:195`, under the registry heading at L177; root-ledgers is registered at L196. This is closure evidence/status corroboration, not an eight-field gate-row audit. **Verdict: not relevant** — closure-ledger rows must not be conflated with C2 registry rows.
- **souji**, `/home/vgpnk/Projects/shokunin/souji-shokunin/tools/souji-registry-agreement.py:8-22,166`: L16 requires stale statements to be `append-only by bytes`; L17 requires a later `R29-CORRECTION` line, with the following lines requiring the exact file:line tag and derivation evidence. It also compares SOURCES `used-by` declarations with committed knowledge entries. Unlike C2's two label→revision errata checks, this prices source links and byte-anchored stale-statement corrections. **Verdict: kengaku owns this** — correction-binding is adjacent prior art, not the same erratum population or a substitute for D4.

## Contradictions and limits

1. **Duplicate policy:** tabi latest-row-wins and protocol closure-ledger last-row-wins are deliberate append-only supersession policies; C2 deliberately rejects duplicate names and prices every row. Importing either sibling policy would undo D3.
2. **Universe policy:** tree-discovered scripts, document-advertised scripts and registry-declared scripts are three different sets. A tree-derived gate is not proof of the frozen `ADVERTISED total=112`, and C2's `106` target does not make it a tree-completeness claim.
3. **Substrate:** the inspected kengaku source uses `Path.read_text`/`exists`, despite C2's docstring saying committed bytes only. Several siblings use revision-addressed git blobs. A landing measurement must establish snapshot identity externally; this scan does not certify that identity.
4. **Field strength:** syntactic parse success is not active-handler proof or observed runtime behavior. Kotoba's AST handler check, mori's argv-branch check and tameshi's runtime replay are distinct verification surfaces, not interchangeable green results.

## One bounded proposed move

**Add a supplementary population-identity receipt to the L1's landing evidence, borrowing mori's digest technique without changing either counter.** At the one landing snapshot, record the sorted C1 advertised script paths and their source-document provenance, plus C2's ordered row-name/entry-script pairs, with separate digests. Keep these as evidence, not a new predicate, script or registry.

Affected axes: **calibration improves** because equal counts with substituted members become visible; **coverage is unchanged** because no population member, counting rule, target or kill rule changes. Runtime: no registered command executes. Contract: the frozen output lines remain authoritative. Substrate: both population receipts must derive from exactly the same landing snapshot. Verification: an independent reader can reproduce both manifests and compare identities; duplicate row identities remain visible in C2's ordered list rather than being deduplicated away.

Risks: a manifest generated from a later worktree is misleading; sorting/deduplicating C2 rows could erase the very second-row defect D3 prices; a digest without the manifest does not permit inspection. Do not import mori's self-test policy, tabi's supersession rule or a tree-derived population as part of this move. This proposal is not implemented or admitted by this seat.

## Commands and verification boundary

This was a read-only source scan using file discovery, source reads and line-location searches. Discovery/source-inspection shell batches returned exit 0; sibling instruments, selftests and mutants were **not executed**, so no sibling runtime verdict is claimed. The actual files and lines above were opened, including tabi's evaluator/field checks, tsukuroi's tree enumeration/coverage checks, and kama's environ reader.

One incidental local control was invoked during comparison:

`cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 plans/round52_c2_registry.py --lane . --universe legacy 2>&1 | head -20; echo "rc=$?"`

Observed excerpt: `ADVERTISED total=113`, `MISSING 0`, `PREDICATE R52-C2 pass`, `PREDICATE R73-C1 fail`, followed by `rc=0`. **The printed rc is the pipeline/head status, not a captured counter exit code; the counter exit code is not established by this receipt.** No separate stderr was captured. The live source had changed during the scan; these numbers are neither a frozen control result nor a landing-tip score. No claim conclusion is drawn from this invocation.

No tools installed or updated. Scratch was created solely at `/fast/scratch/hyaku/kengaku-r73/SiblingConnectorR73`; no fixture or clone was needed. The report records cleanup separately.
