# Seat C2RevRowIntent — kengaku round 52, wave 1 (build), hyaku run 11

Role: revenger (read-only). Item: reverse-engineer the INTENT of the 28 unregistered instruments —
for each, what did the round that built it claim it did — and produce one line per instrument: what
it is FOR, whether it is still live or superseded by a later counter, and the truthful `kind`
(gate/probe) and owner for its registry row. Judged on operability.

Base tip `30801b479e3418c11089b8586178b6960216f364`. Frozen claims read in full first
(`plans/round-52-claims.md`); nothing in the lane tree, the fleet repo, or any sibling was written.
No git/jj mutation anywhere. Scratch used and removed (see §6).

## 1. What I did (commands, all read-only)

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r52/C2RevRowIntent/tmp
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round52_c2_registry.py \
    --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin        # → exit 1, MISSING 28 (receipt kept)
for f in <the 28 stems>; do PYTHONDONTWRITEBYTECODE=1 timeout 25 \
    python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/$f.py --help; done   # CLI surfaces
PYTHONDONTWRITEBYTECODE=1 python3 /fast/scratch/hyaku/kengaku-r52/C2RevRowIntent/analyze.py
```

`analyze.py` (in my scratch, removed at yield) re-implements the frozen counter's extraction rules
verbatim against the lane tree and reports, per instrument: which self-assessment file advertises it,
whether a registry row parses for it, its argparse flags, and the raw self-test cell of the row the
counter calls SELFTEST-UNBACKED. It writes nothing inside the lane.

Measured before-state (base tip, my run 2026-10-28, exit 1):

```
ADVERTISED total=72
REGISTERED total=44 rows=46
MISSING 28
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 1     (`order-check`)
PREDICATE R52-C2 fail
```

— byte-identical to the frozen before-block in `plans/round-52-claims.md` §Claim 2.

## 2. Headline finding 1 — `gate_flip_check.py` is NOT actually unregistered; its existing row is invisible to the counter's parser

`SKILL.md` already carries a `gate-flip-check` row, but its verdict-map cell contains one escaped
pipe (`… Flip check (round N): <item> — fired\|not fired — <evidence> …`). The frozen counter's
`parse_rows` splits every table line on the bare `|` character (`line.strip().strip("|").split("|")`)
and keeps only 8-cell rows, so the escaped pipe produces a 9th cell and the row is silently dropped.
Measured: the registry table holds **46 data rows** (48 pipe-lines − header − separator); `parse_rows`
yields 46 rows *counting the header*, i.e. 45 data rows — exactly the `gate-flip-check` row is
dropped (`cells=9`, escaped-pipe count 1; every other data row has 8 cells). That is why the counter
reports `REGISTERED total=44` (45 parsed data rows, 44 distinct entry scripts — no duplicate
instrument exists among them; measured) and lists `plans/gate_flip_check.py` under MISSING.

**Consequence for the C2 build:** the truthful fix is to repair the existing row in place (replace
the escaped pipe, e.g. `fired / not fired`), after which **27 new rows** are needed, not 28. Adding a
29th row for the same instrument would leave a malformed, silently-dropped row in the table — the
registry would then contain an unparseable row the counter cannot see (the same "row the parser
drops" class the round-51 closure's D3 mutation list already names for row deletion). Any new or
repaired row must satisfy the counter's measured row grammar:

- starts with `|`; splits into **exactly 8 cells** on `|` — an escaped `\|` still splits, so no pipe
  of either form may appear inside any cell;
- the **entry** cell (3rd) must contain `python3 plans/<name>.py` matching
  `plans/[A-Za-z0-9_]+\.py` (all 28 names are underscore-style, so all match);
- all 8 cells non-empty (`INCOMPLETE` counts any empty cell);
- the **self-test** cell: if it names exactly one script and ≥1 `--flag`, every named flag must
  occur in that script's bytes, else the row is SELFTEST-UNBACKED. Cells naming 0 or ≥2 scripts are
  not counted (ambiguous cells are accepted by the frozen rule).

## 3. Headline finding 2 — the `order-check` SELFTEST-UNBACKED hit, mechanism measured

The existing `order-check` row's self-test cell reads (raw, SKILL.md:590):

> no `--selftest` in the script; falsifiers are external — `plans/round40_c1_verify.py` mutants
> `O04` (`rc-silence`), `O12` (`rc-error`), `O14` (`error`), each witnessed pre-freeze …, and the
> measured controls `--receipt corpus/evidence/round39/git-leak-probe.txt` → `ORDER FAIL …`;
> `--claims plans/round-99-claims.md` → `ORDER ERROR …`, exit 2

The counter's rule extracts from that cell exactly one script (`plans/round40_c1_verify.py`) and
three flags (`--claims`, `--receipt`, `--selftest`); none of the three occurs in
`plans/round40_c1_verify.py`'s bytes (measured: `--claims=False --receipt=False --selftest=False`),
so the row is flagged. The prose *means* "order_check.py has no --selftest", but the cell pairs the
flag with the wrong script. Truthful repair: name `plans/order_check.py` with a flag it actually
accepts — it takes `--lane`, `--claims`, `--receipt` (`plans/order_check.py:143-145`, measured) —
e.g. "no `--selftest`; red controls: `python3 plans/order_check.py --claims plans/round-99-claims.md
--receipt …` → `ORDER ERROR …`, exit 2", or drop the `.py` token so the cell names zero scripts.

## 4. The intent table — one line per instrument

Columns: instrument · built by (round) · what it is FOR · live or superseded · truthful kind ·
truthful owner · evidence. Evidence keys: D = script docstring (plans/<name>.py), SC = SCORECARD.md
line, LG = LOG.md line, LS = corpus/lessons/<file>. All line numbers read at the base tip.

| # | instrument | built by | what it is FOR | live / superseded | kind | owner | evidence |
|---|---|---|---|---|---|---|---|
| 1 | `plans/adoption_check.py` | r29 (re-used r30/31/33) | One-command re-derivation of an adoption round's landed state from committed bytes: entry exists, README index row, cited S-ids hold registry rows that are `mined` with matching `used-by`, fleet census exits 0; prints 7 frozen fields, exit 0 only when all hold | **Superseded in role** — staging moved to `plans/sources_adopt.py` (registered gate, r29–31), its measured content-blindness closed by the r31/r33 second receipts, and adoptions from r35 on are gated by the `pkg_gate` family; last exercised as a counter in r33 (LG:926); not re-run since | gate | kengaku round 29 | D:2-24; SC:1002,1013,1030,1063,1139; LG:648,653,700,926; LS round-29.md:162,169,172 (M93/M99/M102), round-30.md:124-127 |
| 2 | `plans/attrib_probe.py` | r21 (ext r22 force-trials, r23 stream-trials) | Blind cascade-leg attribution: attributes which cascade leg served a response through the fleet chat shims from a sha256-pinned frozen feature table, journal ground truth read only post-trials; subcommands block-sha / freeze-check / trials / force-trials / stream-trials / score | **Live** — the SCORECARD capability `frozen-table-pin-check` (SC:556, first-working r21, re-demonstrated r24) points at it; the v3 table (`plans/attrib-r23-frozen.md`) is the current pin; the registered `interval-reverdict` gate re-verdicts its receipts | probe | kengaku rounds 21–23 | D:2-31; SC:493-496,556; LG:171,262; LS 2026-10-16-round21-attribution-freeze-surface.md:4,28, round22:13, round23:19,78,102,143 |
| 3 | `plans/catalog_probe.py` | r32 (verify mode r33) | Re-probe the two live public model catalogs (HF `api/models`, OpenRouter `api/v1/models`) and check the catalog entry's freshness; `--verify` re-derives the recorded numbers offline from committed raw bytes and SHA256SUMS | **Live** — SCORECARD capability `offline-catalog-receipt-verification` (SC:561, first-working r33) points at it; r33 C3 ran `--verify` green (SC:1141, LG:936) | probe | kengaku rounds 32–33 | D:2-17; SC:561,1141; LG:936; LS round-32.md:15 |
| 4 | `plans/defect_ledger.py` | r35 | Persistent routed-defect ledger checker: re-runs EVERY row's check in `corpus/defects.jsonl` at the current tip and counts calibration mismatches (a `closed` row whose check fails, an `open` row whose check passes) | **Live** — SCORECARD capability `routed-defect-ledger` (SC:563, first-working r35); the registered `ledger-tip` gate names it as the check authority for `corpus/defects.jsonl`; re-measured green by the r35 spot-check (LS round-35-verifier-spotcheck.md:38) | gate | kengaku round 35 | D:2-15; SC:563,1193; LG:995,1005; LS round-35-verifier-spotcheck.md:38,86-87 |
| 5 | `plans/gate_flip_check.py` | r43 (extended r44) | Require every conditional Gate refusal in a lesson's `## Gate` section (a refusal carrying a flip condition) to be resolved by a later `Flip check (round N): … fired\|not fired …` line; red by construction on the corpus (45 obligations in 18 lessons unresolved at r43) | **Live** (forward gate from r43, never a claim the corpus is clean) — capabilities `gate-flip-check` (SC:1889, r43) and `flip-verdict-check` (SC:1973, r44, reads flip verdicts against entry citations, SELFTEST 27/27). **Its existing registry row is malformed (9 cells, escaped pipe) — see §2** | gate | kengaku rounds 43–44 | D:2-10; SC:1889,1973; LG:1328,1359; LS round-43.md:11, round-43-verifier-spotcheck.md:124, round-44.md:54-57,95-98 |
| 6 | `plans/parser_policy_compare.py` | r27 | Re-score the frozen 1964-response round-26 population under eight alternate answer-extraction policies (E0–E8, pre-registered), publish paired flips/strata/matrix, separate contract mismatch from accuracy; population/pins/dispatch from `grader_perturb.py`, exact CP95 from `attrib_calibration.py` | **Live, no successor; last exercised r27** — nothing later covers the extraction-policy question; it is cited as source row S056 (LS round-27.md:49) and the admitted entry `extraction-policy-comparison.md` advertises it; novelty was held 7→7 (SC:827) | probe | kengaku round 27 | D:2-13; SC:827,870,884; LG:405; LS round-27.md:49,100 |
| 7 | `plans/password_recovery_probe.py` | r45 | Offline execution of the pinned TB2 `password-recovery` grader (digest-checked capture) in a per-case bubblewrap sandbox over 16 frozen cases with pre-written predictions and a same-state regrade; the second F1 constant-compare exemplar (line-membership of one embedded constant) | **Live** — the probe of record for the r45 package; the knowledge entry's `recheck:` clause runs it (`corpus/knowledge/tb2-password-recovery-grader.md:10,181-182`) | probe | kengaku round 45 | D:2-31; SC:2009; entry :10,:181-182; LS round-45.md |
| 8 | `plans/polyglot_c_py_probe.py` | r46 | Offline execution of the pinned TB2 `polyglot-c-py` grader over 18 frozen cases (dual-runtime program verdict: python3 and gcc must both execute `/app/polyglot/main.py.c`); third grader class the lane executes | **Live as the r46 package probe, but its claim was NOT admitted** — the r46 C3 counter landed red (`checks=13 defects=2`, V7 frozen-tags / V8 order; SC:2068); the entry's recheck clause still runs it (`tb2-polyglot-c-py-grader.md:9,211`) | probe | kengaku round 46 | D:2-31; SC:2068; entry :9,:211; LS round-46.md (title: "C3 counter fails V7/V8") |
| 9 | `plans/round28_census.py` | r28 | Read-only round-28 census at a caller-supplied revision (`--revision` mandatory, never inferred HEAD): re-runs `benchmark_spec_audit.py` and `registry_check.py` and reports source/knowledge/index parity | **Superseded as the standing census** — after r30 the lane's census role moved to `state_check.py` / `round_close.py` / the fleet `sources-census.sh`; re-run only as a historical regression check through r30 (LG:660,703,729,832); nothing re-runs it after r30 | probe | kengaku round 28 | D:2; SC:948,1006; LG:660,703,729,832; LS round-29-verifier-spotcheck.md:73,76 |
| 10 | `plans/round30_defects.py` | r30 | Re-derive the five routed defects D1–D5 that round 29's non-author closure left (one command, `defects=N`, exit 0 only when all re-derive repaired) | **Superseded by `plans/defect_ledger.py`** (r35) — that script's docstring states it was mined from the proposal "one persistent routed-defect ledger instead of a new plans/roundNN_defects.py per round" | gate | kengaku round 30 | D:2-14; SC:1031; LG:806; LS round-30.md:152,176-178 |
| 11 | `plans/round31_c1_verify.py` | r31 | Second receipt for r31's adoption C1: the content literals `adoption_check.py` cannot see (frozen entry path, access-date literal, per-row citation identity, pinned revisions, index-title substance, control-receipt digest; V1–V6) against `corpus/knowledge/benchmark-verifier-execution-model.md` | **Superseded as a pattern; still the only checker of its own entry** — r33 re-implemented the same V1–V6 re-pointed at a different entry plus V7/V8, and adoptions from r35 on use the package-gate family; not re-run since r31 | gate | kengaku round 31 | D:2-22; SC:1063,1076; LG:888; LS round-31.md:127 |
| 12 | `plans/round31_defects.py` | r31 | Re-derive the ten routed defects R1–R10 that round 30's non-author closure left | **Superseded by `plans/defect_ledger.py`** (r35, same proposal quote as #10) | gate | kengaku round 31 | D:2-19; SC:1064; LG:865,890; LS round-31.md:128 |
| 13 | `plans/round33_c1_verify.py` | r33 | Second receipt for r33's adoption C1: the r31 checks (V1–V6) re-pointed at `corpus/knowledge/benchmark-grader-semantics.md` plus V7 (the lesson's renumber map S094→S103, S097→S104) and V8 (the r32 refusal rows stand unchanged) | **Superseded as a pattern; still the only checker of its own entry** — same family fate as #11; not re-run since r33 (LG:927) | gate | kengaku round 33 | D:2-21; SC:1143; LG:927; LS round-33.md:31,44 |
| 14 | `plans/round33_defects.py` | r33 | Re-derive the six routed defects N1–N6 that round 32's non-author closure left | **Superseded by `plans/defect_ledger.py`** (r35, same proposal quote as #10) | gate | kengaku round 33 | D:2-18; SC:1140; LG:931; LS round-33.md:31,44 |
| 15 | `plans/round35_c1_verify.py` | r35 | r35 C1 counter: the pinned TB2 `protein-assembly` package admitted (V1 capture digests, V2 registry rows S105–S107, V3 entry quotes verbatim on capture lines, V4 index parity, V5 probe receipt byte-equal to a fresh run, V6 census) | **Superseded by `plans/round36_c1_verify.py`** — the registered `round36-c1-battery` row names it "`--legacy`: the seven junk fixtures against the round-35 counter of record", and the r35 spot-check measured that it "passes a stub probe plus one-word quotes" (LS round-35-verifier-spotcheck.md:86) | gate | kengaku round 35 | D:2-24; SC:1192; LG:1004; LS round-35-verifier-spotcheck.md:37,86 |
| 16 | `plans/round35_hardening.py` | r35 (post-hoc) | Post-hoc hardening checks H1–H6 written after wave-1 seats showed false greens in the r35 frozen counters (frozen instruments byte-equal to the freeze, quote-table parsing, teaches-cell word floor, directional D4/D5 clauses, no untracked files); its own docstring: "NOT the rule of either frozen claim" | **Superseded as a rule candidate by the r36 package gate** — r36 promoted the H1–H6 classes into `plans/pkg_gate.py` + `round36_c1_verify.py` (LS round-36.md:34); the script itself was never a rule and is not re-run | gate (post-hoc, non-rule — the row must say so) | kengaku round 35 | D:2-13; SC:1198; LG:1013; LS round-35.md:28, round-35-verifier-spotcheck.md:86 |
| 17 | `plans/round36_c2_verify.py` | r36 | r36 C2 counter: the pinned TB2 `regex-log` package admitted (W1 capture, W2 rows S108–S110, W3 entry quotes, W4 index, W5 probe digest + receipt byte-equal, W6 census) | **Superseded by `plans/round37_c2_verify.py`** — the registered `round37-c2` row measures the r36 package with the r37 counter, and the r48 lesson records that "the r36–r39 verifier files remain per-round copies … each has its own check count and CLI" (LS round-48.md:38) | gate | kengaku round 36 | D:2-22; SC:1225; LS round-36.md:17,43, round-48.md:38 |
| 18 | `plans/round45_c1_verify.py` | r45 | r45 C1 counter: does the fixture fence do what the lane says — REFUSALS (10 hostile modules), HONEST (104 battery fixtures must be admitted), CALIBRATION (advertised-vs-contradicted count), fence run under `strace -f -y` in bwrap | **Superseded by `plans/round46_c1_verify.py`** — the r46 counter's docstring records that "the round-45 counter is passed by a fence that keys on the counter's own fixture names … 9 of 14 held-out hostile modules … are admitted", and the r50 counter's docstring names r46 "the standing instrument for that property" | gate | kengaku round 45 | D:2-43; SC:2008; LS round-45.md:24-27 |
| 19 | `plans/round45_c2_verify.py` | r45 | r45 C2 counter: the `password-recovery` package admitted (V1–V10 = the r44 counter re-pointed, V11 = the hardened held-out predictor leg: source-linted predictor block, disagreement count only, different seeded state table) | **Superseded by `plans/round46_c2_verify.py`** for the same package — r46's C2 exists because "the false detail round 45 landed is superseded and marked, not left standing" (mislocated anchors, false word counts, lone-CR predictor) | gate | kengaku round 45 | D:2-45; SC:2009; LS round-45.md, round-46.md |
| 20 | `plans/round46_c1_verify.py` | r46 | r46 C1 counter: the fence re-judged under a name-hiding counter (Q39: per-run `secrets` tokens, padded decoy parents, shuffled jobs), strace log outside the sandbox, SEALED modules authored blind, byte-copy check of the r45 refusals | **Live — the standing instrument for the fence's outside-`d` property**: `plans/round50_c1_verify.py`'s docstring explicitly defers to it ("`plans/round46_c1_verify.py` remains the standing instrument for that property") | gate | kengaku round 46 | D:2-43; SC:2066; LG:1459; LS round-46.md |
| 21 | `plans/round46_c2_verify.py` | r46 | r46 C2 depth counter: round 45's false line-level detail superseded and marked (A anchor-line legs live=0 with base rows byte-identical, B predictor vs captured grader disagree=0, C entry source ranges + 5 errata marks, D `anchor_line_check.py --selftest`) | **Live, no successor; role closed at r46** — rounds 47–49 committed no counter scripts (the r50 lesson: rounds 48–49 "froze counters in a 'counting command' cell that no commit ever held"), so nothing later re-points it. **Caution for its row: the script has NO `--selftest` flag** (the string appears only in its docstring/leg D driving `plans/anchor_line_check.py --selftest`; measured `--help` = `--lane/--work` only) — a row claiming `--selftest` on it would be SELFTEST-UNBACKED; name `plans/anchor_line_check.py --selftest` instead | gate | kengaku round 46 | D:2-40; SC:2067; LS round-46.md, round-50.md:14 |
| 22 | `plans/round46_c3_verify.py` | r46 | r46 C3 counter: the `polyglot-c-py` package admitted (V1–V13 incl. the gate with `--rerun`, held-out predictor, re-implemented anchor-line rule); order rule: no graded case before the stage-2 freeze | **Live, no successor; RED at landing** — its claim failed on V7 (frozen tags `both-print`/`toolchain` violated by no case) and V8 (control executed the probe before its receipt): `checks=13 defects=2`, `PREDICATE C3 fail` (SC:2068). The row must record the red state, not a green one | gate | kengaku round 46 | D:2-40; SC:2068; LS round-46.md (mistake rows: unsatisfiable tag set; pre-receipt control) |
| 23 | `plans/round50_c1_verify.py` | r50 | Honest-geometry counter: on the frozen 126-fixture honest population (identity-pinned rebuilds) the fence must admit every fixture while refusing all 20 hostile + sealed modules, under a witnessed mutant floor (≥12); separate process per decision, Q39 opaque parents | **Live** — admitted r50 (novelty 7→8); capability `honest-geometry fence counter` (SC:2134,2179); the knowledge entry `fixture-honest-geometry.md:2-3` recheck clause runs it | gate | kengaku round 50 | D:2-43; SC:2134,2140,2179; LS round-50.md:46-50, round-50-verifier-spotcheck.md:41-44,149-165 |
| 24 | `plans/round50_c2_audit.py` | r50 | Pointer audit: every artifact pointer (lane-relative `plans/`/`corpus/` path or 40-hex hash) in `SCORECARD.md`/`SHONEN.md`/`PROVINCE.md` must resolve at the audit revision, honouring the append-only `SUPERSEDED <p> -> <target>` corrections block | **Live** — admitted r50 (calibration 8→9); it is the gate that caught rounds 48–49's never-committed counters (`unresolved=12` at `71f5f5f`, LS round-50.md:14,51-53); `--selftest` appends a bogus token and requires exit 1 | gate | kengaku round 50 | D:2-26; SC:2135,2140,2180; LS round-50.md:14,51-53 |
| 25 | `plans/round51_routing.py` | r51 | Every routed finding in `corpus/routed-findings.jsonl` names an owner lane (or `unowned:integrator`), a frozen disposition, a resolving source, a non-empty check; `fixed-verified` rows' checks re-derive in the run; `fixed-historical` closes resolve in git; `routed`/`referral` need a non-kengaku owner + `next` | **Live** — admitted r51 (adjacency 8→9, SC:2213); `--run-checks` executes the 41 checks; `--selftest` present. No registry row — the r51 closure's D1 routed exactly this (LS round-51-verifier-spotcheck.md:132-135) | gate | kengaku round 51 | D:2-19; SC:2202,2213; LG:1574; LS round-51.md:8-9,38, round-51-verifier-spotcheck.md:132-135 |
| 26 | `plans/round51_surfaces.py` | r51 | Every surface `PROVINCE.md` declares is machine-checked against `plans/round51-surfaces.json`: anchors/rows coverage, probe-vs-recorded-state (STALE), prose-vs-row (DRIFT), dated ABSENT markers (UNVERVICTED), declared counts vs disk (NUMBER-DRIFT), resolve floor | **Live** — admitted r51 (freshness 8→9); SCORECARD capability `surface-truth-manifest-counter` (SC:568, first-working r51); `--selftest` cases=9. Same missing-row routing as #25 (LS round-51-verifier-spotcheck.md:132-135) | gate | kengaku round 51 | D:2-16; SC:568,2201,2212; LG:1564; LS round-51.md:6-7,35-37 |
| 27 | `plans/routed_open.py` | r41 | Routed-findings burn-down: one append-only JSONL row per routed finding (id once ever, class, source lesson:line, opened_round, status open/closed/refused/blocked, close evidence or blocker, optional check command); prints `routed_open=<n> oldest_round=<r>` and refuses a malformed file (exit 1, summary withheld); `--observe` compares each row's check with its status | **Live** — SCORECARD capability `routed-findings-burndown` (SC:1566, first-working r41); the counts it prints are quoted at every round close r41–r50 (LG:1255,1298,1329,1361-1362,1477); `plans/round51_routing.py` consumes the same ledger for a different question (attribution), not a replacement | gate | kengaku round 41 | D:2-27; SC:1566; LG:1255,1298,1329,1361-1362,1477; LS round-41.md:84-85, round-41-verifier-spotcheck.md:68,91-92 |
| 28 | `plans/tb2_grader_probe.py` | r35 | Offline probe of the pinned TB2 `protein-assembly` grader (digest-checked capture, `uv run --with biopython==1.85`): runs `test_gblock()` on 18 frozen synthetic `/app/gblock.txt` contents, each mapped to an instruction requirement with a prediction written before the first run | **Live** — SCORECARD capability `pinned-grader-probe` (SC:562, first-working r35); its receipt is re-run byte-equal by `round35_c1_verify.py` V5 (LS round-35-verifier-spotcheck.md:37). The whole-benchmark successor for the *population* question is this round's own `plans/round52_c1_grader_audit.py` (R52-C1); the per-task probe role stays with this script | probe | kengaku round 35 | D:2-11; SC:562,1192; LG:1000-1003; LS round-35.md:11, round-35-verifier-spotcheck.md:37 |

## 5. The superseded list (explicit, as the item requires)

A superseded instrument still needs a registry row saying so — the registry records history, it does
not prune it. Eight of the 28 are superseded (two more are per-round copies whose *pattern* was
superseded while each remains the only checker of its own entry):

1. `plans/round30_defects.py` → superseded by `plans/defect_ledger.py` (r35). Evidence: the ledger's
   own docstring — "one persistent routed-defect ledger instead of a new plans/roundNN_defects.py per
   round" (plans/defect_ledger.py:3-5).
2. `plans/round31_defects.py` → same, same evidence.
3. `plans/round33_defects.py` → same, same evidence.
4. `plans/round35_c1_verify.py` → superseded by `plans/round36_c1_verify.py` (r36). Evidence: the
   registered `round36-c1-battery` row's entry cell — "`--legacy`: the seven junk fixtures against
   the round-35 counter of record" — and `corpus/lessons/round-35-verifier-spotcheck.md:86`
   ("`plans/round35_c1_verify.py` passes a stub probe plus one-word quotes").
5. `plans/round35_hardening.py` → superseded as a rule candidate by the r36 package gate
   (`plans/pkg_gate.py` + `round36_c1_verify.py`); never itself a rule (its docstring: "NOT the rule
   of either frozen claim"). Evidence: `corpus/lessons/round-36.md:34` (the vacuous-junk class it
   hardened is closed by the r36 gate).
6. `plans/round36_c2_verify.py` → superseded by `plans/round37_c2_verify.py` (r37). Evidence: the
   registered `round37-c2` row measures the r36 package; `corpus/lessons/round-48.md:38` records the
   per-round-copy pattern for the r36–r39 C2 verifiers.
7. `plans/round45_c1_verify.py` → superseded by `plans/round46_c1_verify.py` (r46). Evidence: r46
   counter docstring ("the round-45 counter is passed by a fence that keys on the counter's own
   fixture names"); r50 counter docstring ("`plans/round46_c1_verify.py` remains the standing
   instrument for that property").
8. `plans/round45_c2_verify.py` → superseded by `plans/round46_c2_verify.py` for the same package.
   Evidence: r46 C2 docstring ("the false detail round 45 landed is superseded and marked, not left
   standing") and `corpus/lessons/round-46.md` §Mistakes (mislocated anchors, false word counts,
   lone-CR predictor).
9. `plans/round28_census.py` → superseded as the standing census (by `state_check.py` /
   `round_close.py` / the fleet `sources-census.sh`); re-run only as a historical regression check
   through r30 (LOG:660,703,729,832); nothing re-runs it after r30.
10. `plans/adoption_check.py` → superseded in role: staging by the registered `sources_adopt.py`
    gate, content literals by the r31/r33 second receipts, later adoptions by the package-gate
    family; last exercised r33 (LOG:926).
11. `plans/round31_c1_verify.py` and `plans/round33_c1_verify.py` → per-round copies of the
    "adoption second receipt" pattern (r33 = r31's V1–V6 re-pointed at a different entry, plus
    V7/V8); the pattern itself was superseded by the package-gate family from r35 on, but each copy
    remains the only checker of its own entry (`benchmark-verifier-execution-model.md` vs
    `benchmark-grader-semantics.md` — measured ENTRY constants).

Live (no successor, still the instrument of record): `attrib_probe.py`, `catalog_probe.py`,
`defect_ledger.py`, `gate_flip_check.py`, `parser_policy_compare.py` (unexercised since r27 but
unreplaced), `password_recovery_probe.py`, `polyglot_c_py_probe.py` (claim red), `round46_c1_verify.py`,
`round46_c2_verify.py` (role closed r46, no successor — rounds 47–49 committed no counters,
`corpus/lessons/round-50.md:14`), `round46_c3_verify.py` (red), `round50_c1_verify.py`,
`round50_c2_audit.py`, `round51_routing.py`, `round51_surfaces.py`, `routed_open.py`,
`tb2_grader_probe.py`.

## 6. Files produced, receipts, scratch

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2RevRowIntent/report.md` — this report.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2RevRowIntent.md` — the same
  content at the path the item trailer named (duplicate copy, kept so either path resolves).
- Receipts copied into the wave report dir before scratch removal:
  `c2-before.txt` (the counter run at the base tip, exit 1), `helps.txt` (the 28 `--help` surfaces),
  `analyze.py` + `analyze-out.txt` (the read-only extraction analysis).
- Scratch dir `/fast/scratch/hyaku/kengaku-r52/C2RevRowIntent/` removed before yielding.

## 7. Limits and negative results

- I did not execute any instrument beyond `--help` (argparse surfaces only; `PYTHONDONTWRITEBYTECODE=1`
  so no `__pycache__` was written into the lane). Liveness/supersession verdicts rest on document
  evidence (docstrings, SCORECARD/LOG lines, lessons), not on re-runs; each row's evidence pointers
  let the L1 re-check any verdict.
- "Live" means "still the instrument of record at the tip" (a registered row, a SCORECARD capability
  row, a knowledge-entry recheck clause, or a later counter's docstring names it). It does not mean
  "recently re-run": several live instruments (e.g. `attrib_probe.py`, `parser_policy_compare.py`)
  have not been executed since their own rounds.
- I searched for a second malformed registry row (escaped pipes, wrong cell counts) and found none:
  exactly one data row (`gate-flip-check`) fails the 8-cell parse; the separator and header parse as
  expected. I also checked for duplicate instruments among the parsed rows: none (44 distinct scripts
  from 45 parsed data rows).
- The `SELFTEST-UNBACKED` finding is the counter's own; I measured its mechanism (§3) but did not
  repair anything — the row edits are the C2 build seats' work.
- Tool installs: none needed; no pacman transaction touched (host-wide pause respected).
