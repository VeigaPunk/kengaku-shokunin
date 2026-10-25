# R29a2 — sibling-overlap scan (connector seat)

Role: leaf connector, round 29 attempt 2 (hyaku run 6, 2026-10-25). Read-only everywhere; no
production edits, no lane gates run under `shokuknow`, no subagents. All citations re-verified in
this session on the live trees at 2026-10-25.

## Scope correction (coverage)

The brief says `/home/vgpnk/Projects/*-shokunin`. That glob matches exactly **one** repo:
`kimi-shokunin` (`ls -d /home/vgpnk/Projects/*-shokunin` → `kimi-shokunin`, exit 0). The 21 real
lanes live one level down, at `/home/vgpnk/Projects/shokunin/*-shokunin`
(`ls -d */ | wc -l` → 26 entries; 21 `*-shokunin` lane repos plus fleet docs). I scanned both
locations; a scan honouring only the literal glob would have reported "no owner" while never
looking at a lane.

Lanes scanned (21): audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kasegi,
kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi —
plus `kimi-shokunin`.

Method note (operability): the harness `grep` tool returned `No matches found` for
`/home/vgpnk/Projects/shokunin/*-shokunin/corpus` and for a brace path
`…/*-shokunin/{SKILL.md,PROVINCE.md,README.md}` even for terms that provably occur inside those
files — wildcard directory segments in `path` are not expanded. Every hit below comes from shell
`grep -rn` with an explicit directory, not from the tool. Anyone re-running this with the glob
form will get a false clean.

## Topic rows

| # | Topic | Owning lane | file:line | Decision | One-line reason |
|---|-------|-------------|-----------|----------|-----------------|
| A | Published per-task validity checklist | **kengaku** (sole) | `corpus/knowledge/benchmark-task-validity-checklist.md:1` (entry, untracked this round: `git status` → `?? corpus/knowledge/benchmark-task-validity-checklist.md`); index `corpus/README.md:64`; frontier `corpus/README.md:240`, `:261-262`; scope claim `PROVINCE.md:215-219` ("the published task-validity instruments a benchmark maintainer runs on its own …"); boundary rows `PROVINCE.md:123-125`, `:201`, `:210`; `SKILL.md:570,572,680,699` restate "NOT task validity" for the two existing gates | **keep** | All 15 `*bench*` knowledge files in the fleet are kengaku's (`find */corpus/knowledge -iname "*bench*"` → 15/15 under `kengaku-shokunin/`); no sibling holds benchmark-evaluation province, and the campaign already assigns this topic here (`.tower/comms/inbox/20261024-r100-assimilation-census-tower-survey-summary.md:38`: "kengaku benchmark task-validity checklist"). |
| B | Contamination transparency card | **kengaku** (sole vocabulary holder; no card instrument anywhere) | `corpus/knowledge/contamination-detection-and-transparency.md:1` (S001/S002/S004, `verified-at: 2026-10-19`); gap stated `corpus/README.md:263`; `PROVINCE.md:125` | **keep** | Tier/access vocabulary exists only here; every non-kengaku `contaminat|transparency` hit in lane corpora is a different object — kotodama myth purity (`corpus/knowledge/myth-symbol/purity-pollution-boundary-systems.md`), kotoba harness self-contamination (`corpus/knowledge/harness-verifier-round10.md:141`), chousa editorial transparency of sources (`corpus/knowledge/contextual-source-admission-r24.md:2`) — so a card format has no sibling to route to. |
| C | Source-adoption gate | **split: contract + validator = fleet (`/home/vgpnk/Projects/shokunin/scripts/`); staged→append construction = kengaku** | fleet validator `scripts/sources-census.sh:24-29` (E01–E11), `:40` (0–3 leading spaces), `:16` (exit 0/1/2), `:126-145` (selftest incl. `E01-malformed-row`, `E03-duplicate-id`, `E11-dangling-usedby`, `validate-findings-exit-1`, `validate-clean-exit-0`); contract `scripts/hyaku/lane-addendum.md:250-311` — anchor clause `:268-270`, no-staged-row-as-is + normalization `:288-296`, pre-append `sources-census.sh validate --file` `:304`, round-end `validate --root` `:309`; census clause `CORPUS.md:152`; lane side `plans/sources_adopt.py:1` (424 lines), `plans/adoption_check.py:1` (127) | **keep the builder, route the validator** | Checks 1/2/4 of C2 restate the fleet's E01/E03/E07/E09/E11 (already binding: `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → 14×W04 + `kengaku ok …/corpus/SOURCES.md`, **EXIT=0**); only check 3 (prose-`recheck` normalization, `used-by` rewrite to the admitted set, escaped-pipe refusal) has no fleet implementation — `lane-addendum.md:288-296` demands it but ships no tool, so that half must stay lane-side. |

No sibling lane owns any of the three. Verified by shell grep, not the harness tool:

```
cd /home/vgpnk/Projects/shokunin && grep -nEi "task[- ]validity|validity checklist|transparency card|source[- ]adoption|adoption gate" */SKILL.md */PROVINCE.md */README.md
```
→ hits only in `kengaku-shokunin/{SKILL.md:570,572,680,699; PROVINCE.md:125,201,210,215,217,219}`,
exit 0. Same pattern over every `*/corpus` tree (`grep -rn … */corpus --include="*.md"`) → no
non-kengaku hit; over `/home/vgpnk/Projects/kimi-shokunin` (whole tree, all file types) → no output,
exit 0. The only non-kengaku mention of an "adoption gate" in the fleet is
`game-dev-2d-shokunin/reports/round-104/r104-crit4.md:37` ("the adoption gate that binds first"),
a companion-HEAD gate, not a registry gate.

## Adjacent capabilities (not owners, but they change what C1/C2 may claim)

| Capability | Where | Relation |
|---|---|---|
| Quote-still-there audit over recorded fetch manifests | `kake-shokunin/scripts/source_recheck.py:1-12` (773 lines), selftests `source_recheck_selftest.py:1-12` (952), `source_recheck_hardening_selftest.py:1-14` (531) | Offline re-check of a *manifest's* quoted text; no `SOURCES.md` schema, no id collision, no append. Different object — not a duplicate of C2. |
| Re-open located quotes against the registry's live source | `chousa-shokunin/tools/quote-reopen.py:1-8`; plus `quarantine-check.py:1-8`, `absent-split.py:1-8` | Operative sibling for C1's *re-grounding duty*. kengaku's `adoption_check.py` verifies registry↔entry↔used-by consistency only; it never re-opens a URL. If C1's re-grounding is to be gated later, chousa's tool is the prior art to borrow from, not re-derive. |
| Round-evidence census | `kumitate-shokunin/scripts/wave-census.mjs:1-12` | Wave-dispatch census, unrelated to source rows. |
| Assimilated-worker gate | `kotodama-shokunin/tools/harness/receipt_guard_adoption.py` | Name collision only ("adoption"); receipt guard for harness runs. |

## Second-order effects and one contradiction

1. **Asymmetric delegation inside the claim.** `plans/adoption_check.py:35` pins the fleet path
   (`CENSUS = Path("/home/vgpnk/Projects/shokunin/scripts/sources-census.sh")`) and
   `:98-106` shells `validate --root <lane parent> <lane>`; `plans/sources_adopt.py` imports no
   `subprocess` (`grep -n "import" …` → argparse/re/sys/tempfile/pathlib only). So the counter
   *reuses* the fleet validator while the gate *re-implements* its row parser. The two share a
   byte-identical anchor copy — `REGEX` at `plans/sources_adopt.py:33` and
   `plans/adoption_check.py:33` are the same `ROW_RE` source text. Consequence: the gate can accept
   a block the counter's census later rejects (E09/E11 are stricter than the gate's own schema
   check) and there is no same-checker proof tying them — exactly the drift the critic seat records
   independently (`R29a2CritClaimC2.md:140`). Cheap fix inside the claim's own surface: have
   `sources_adopt.py` call the census on the constructed block instead of (or in addition to) its
   own parser, so the positive path and the counter share one checker.
2. **The gate's "before" is a fleet-relative statement.** C2 says the adoption contract "lives as
   ad-hoc shell run by hand each round". That is true of *construction* (`lane-addendum.md:288-296`
   gives the shell, not a tool) but false of *validation*, which the fleet already ships and already
   binds kengaku with exit 0 today. Any report sentence claiming the fleet lacks an adoption gate
   would overclaim; the accurate sentence is "the fleet validates rows but ships no builder".
3. **Contradiction, stated not smoothed:** C2's case (b) — "a 4-space-indented row must *not* count
   (outside the census clause)" — is asserted against a census clause whose *only* shipped
   implementation is `sources-census.sh:40` ("accepts 0–3 leading ASCII spaces"). Nothing in
   kengaku verifies the census itself would ignore a 4-space row; the selftest verifies only
   kengaku's copy. The claim is true of the lane's parser and, so far as this seat observed, unproven
   of the fleet parser.
4. **Scope creep to avoid.** `sources-census.sh` already prints 14 W04 findings on kengaku's
   registry (duplicate URL across scopes). None is E-class, so the registry is clean by the fleet
   bar; a new lane gate must not start refusing on W04, or it will block every future append on
   pre-existing state.

## Verification (re-runnable, read-only)

```
ls -d /home/vgpnk/Projects/*-shokunin                    # → kimi-shokunin only
ls -d /home/vgpnk/Projects/shokunin/*-shokunin | wc -l   # → 21
cd /home/vgpnk/Projects/shokunin
find */corpus/knowledge -maxdepth 2 -iname "*bench*" | grep -vc kengaku      # → 0
grep -rnE "^#+.*|" scripts/sources-census.sh | sed -n '24,29p;40p'           # E01–E11, 0–3 spaces
grep -nE "adoption|0–3 leading|sources-census.sh validate" \
  scripts/hyaku/lane-addendum.md                                             # → 241,268,304,309
TMPDIR=/tmp/r29a2-conn bash scripts/sources-census.sh validate \
  --root /home/vgpnk/Projects/shokunin kengaku; echo "EXIT=$?"               # → 14×W04 + ok, EXIT=0
cd kengaku-shokunin && sed -n '33p' plans/sources_adopt.py plans/adoption_check.py  # same ROW_RE
grep -nE "CENSUS|subprocess" plans/adoption_check.py                         # → 35, 98
grep -c subprocess plans/sources_adopt.py                                    # → 0
```
Observed 2026-10-25 in this session: all of the above as annotated, except the `sed -n '33p'` pair
printed a single line — both files carry the identical `ROW_RE` source text at line 33, verified by
`grep -nE "ROW_RE" plans/adoption_check.py` → `33:`.

## Tooling

No installs, no upgrades, no pacman transactions. Nothing written outside this report; scratch
`/tmp/r29a2-conn` held only the census TMPDIR. No campaign tool under `/home/vgpnk/Projects/shokuknow`
was executed; `shokuknow/merge` was read only (`ls`, `grep` over `MERGE-REPORT.md` filenames).
