# SiblingOverlap — kengaku round 64, wave w1 (connector seat)

Scope: read-only scan of every sibling lane repo under
`/home/vgpnk/Projects/shokunin/*-shokunin/` (21 lane repos; `kumitate-shokinin`
is a stray directory, not a lane repo — it holds no `PROVINCE.md`). Every
sibling `PROVINCE.md` was read in full before the greps. Nothing outside
`.ufo/waves/round-64/w1/SiblingOverlap/` and the seat scratch was written; no
git mutation, no network, no sibling file edited. Frozen claims read first:
`plans/round-64-claims.md` (freeze `859ac24f`, base `5f517fe`).

Counting rule: an item counts as **OWNS** only if a sibling's own `PROVINCE.md`
(or a sibling-owned instrument it names) claims the *same object* — benchmark
grader replay, a gRPC/kv-store service, the grader-class census, or a
corpus-wide provenance-trio sweep. A sibling that merely *uses* the same word
("trio", "census", "freshness", "offline replay"), **cites** kengaku's bytes, or
**lists a filename** does not own the object; those are listed **DOES NOT OWN**
with the quoted line and are not counted.

> **Correction to a first-draft grep.** The first pass filtered sibling hits
> with `grep -v "^kengaku/"`, which matches no sibling path (the directory is
> `kengaku-shokunin/`) and therefore let kengaku's own bytes through as if
> they were sibling hits. The receipt of record is `greps.py`/`greps.txt`,
> which excludes the lane by its exact directory name and re-scans all 20
> sibling lanes. Every number below comes from that receipt.

---

## Verdict — Question 1

**Does any sibling own or claim offline replay/execution of benchmark graders,
gRPC/kv-store service building, or provenance/freshness sweeps over corpora?**

Receipt: `python3 greps.py` → `greps.txt` (patterns A–G, one line each with the
lanes that hit).

| Sub-question | Verdict | Decisive evidence (corrected receipt) |
|---|---|---|
| Benchmark-grader offline replay / execution | **NO sibling owns it** | Pattern A (`graders/executed\|executed17\|graders/SHA256SUMS\|test_outputs\.py`): **12 files in 4 lanes** (kama, souji, tabi, tsukuroi) — every one is a *citation or a filename listing*, not ownership: `tabi-shokunin/.ufo/waves/round-32/w1/ConnSiblings.md` (quotes kengaku's grader path), `souji-shokunin/.ufo/waves/round-52/w1/S52connector01/evidence/01-sibling-term-sweep.txt` (a sibling-term sweep listing kengaku's TB2 grader digests), `kama-shokunin/.ufo/waves/round-58/w1/out/X04ScratchHygiene/tmp-c1-before.txt:993` and `tsukuroi-shokunin/.ufo/waves/round-48/w2/TExecCounterB/tmp-listing-pre-run.txt:1474` (both are `/tmp` **listing receipts** naming `tb2_test_outputs.py`; no grader content). Pattern E (154 files, 11 lanes) — every corpus-level hit is a different subject: `kagi-shokunin/corpus/lessons/round-27.md:114` (release-anchor ordering on offline replay), `kaidoku-shokunin/corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:46` (firmware transform replay), `kama-shokunin/corpus/knowledge/ollama-evidence-replay.md` (Ollama capture replay), `kotoba-shokunin/corpus/knowledge/sibling-overlap-census-round74.md` (lane-scope census). No sibling **executes** a benchmark grader. |
| gRPC / kv-store service building | **NO sibling owns it** | Pattern C (`grpcio\|kv[._-]store\|kv-store-grpc`): **3 files in 1 lane** — `tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecMirrorTimestamps/{host,official,stable}-extra-pkglist.txt`, a **pacman package-list mirror** whose lines are `python-grpcio 1.84.0-1` / `python-grpcio-tools 1.84.0-1` (package names in a DB mirror, no service). Pattern D (`127.0.0.1:5328\|localhost:5328`): **0 files, 0 lanes** — no sibling names or binds the port. (Live check: `pacman -Q python-grpcio` → "package 'python-grpcio' was not found"; `pacman -Si python-grpcio` → available in `extra` at 1.84.0-1, i.e. the tsukuroi mirror is a package-name list, and the C1 venv route stays PyPI per the frozen claim.) |
| Provenance/freshness sweeps over corpora | **PARTIAL — contested, routed below** | Four siblings own *a* corpus-header/freshness gate over **their own** corpus; none owns a sweep over kengaku's. See contested scope C-1. |

### The kama overlap the task asked me to flag

kama owns the serving plane (`kama-shokunin/PROVINCE.md:3` "**Domain:** local
model serving & endpoint health — local LLM endpoints, baseURL"; `:6` "**Owns
(surfaces):**"; `:10` "producer discovery & read-only service inspection of
local serving ports"). The C1 probe builds a **lane-authored gRPC kv-store
server** on `127.0.0.1:5328` — **not** a model endpoint and **not** in kama's
registry (kama's three registry rows are `127.0.0.1:8080`, `:34113`, and a
`127.0.0.1:[0-9]+` pin: `kama-shokunin/registry/endpoint-consumers.tsv:35-37`).
kama's own boundary rule is explicit: "kama answers *'is the thing at this
baseURL the model this config believes it is, right now'* — never *'is the
model good'* or *'is the request safe'*"
(`kama-shokunin/PROVINCE.md:47-48`), and kama "refuses: model quality/eval
(kengaku)" (`:44`).

**Overlap verdict: none on the object, one on the port plane.** The C1 server is
a benchmark fixture, not a served model; kama's `listeners` census classifies a
foreign service as `FOREIGN_SERVICE` (`kama-shokunin/tools/kama-probe.sh:29`,
`:64`, `:712-737`), so a C1 run would show up in kama's census as an unowned
listener. That is **read-only observation by kama of kengaku's fixture**, which
kama's province permits ("read-only service inspection"), not a claim conflict.
Contested scope **C-2** below.

kengaku's own province already refuses the serving plane: "**Not owned:** the
model-serving plane (llama-server flags, slot/batch config) — no lane owns it;
escalate to the integrator instead of remediating"
(`kengaku-shokunin/PROVINCE.md:25-26`).

---

## Verdict — Question 2

**Does any sibling's corpus already hold the grader-class census ground or the
trio-sweep pattern (kumitate gate tooling, tameshi mutate-and-run)?**

| Ground | Verdict | Decisive evidence |
|---|---|
| Grader-class census | **NO sibling holds it** | Pattern B (`network-service\|grader-class\|class_survey\|class-survey`): **3 files in 1 lane** (tabi) — and all three are tabi *quoting kengaku's own round-63 git log* (`tabi-shokunin/.ufo/waves/round-57/scout/receipts/07-meter-red-kengaku.txt:20,26`: "R63-C1 pypi-server offline replay (miss …), R63-C2 grader-class SKILL table (pass)"), i.e. a citation of kengaku's record, not a sibling census. The census itself is kengaku-only: `corpus/evidence/round62/class-survey.txt` (`CLASS network-service count=8`), `corpus/evidence/round52/graders/executed17.lst`, `kengaku-shokunin/PROVINCE.md:893-912` ("Round 62: the population's first grader-class census"). The prior round's scan agrees: `kengaku-shokunin/.ufo/waves/round-63/w1/SiblingOverlap.md:6-9` — "no sibling lane owns (a) offline replay of TB2 graders … (c) a grader-class census". |
| Trio-sweep pattern | **YES — held by 4 siblings, each with a DIFFERENT rule** | kumitate `scripts/sources-check.mjs:381-383` (first **5** lines, presence-only, no order); tsukuroi `tools/check-knowledge-header.py:9-27` (column-0, outside fences, **last** occurrence operative, value-validated); chousa `tools/research-gate.sh:3606-3622` (**before the first `## ` heading**, presence-only); kengaku (12-line window, before first `## `, **in order**). None is kengaku's rule. (Pattern F, `\btrio\b`, hits 2558 files in all 20 lanes — the bare word is fleet-common noise, so the counting rule uses the **instrument** lines above, not the word.) |

### Measured divergence — the same 65 kengaku entries under four trio rules

Command: `python3 /fast/scratch/hyaku/kengaku-r64/SiblingOverlap/measure_final.py`
(receipt `measure_final.txt`, `current.txt` in the seat dir). kengaku's own rule
is read from the gate itself — `from round63_gate_checks import trio_missing`
(`plans/round63_gate_checks.py:97-118`, window 12 lines, before first `## `,
keys in order).

```
corpus/knowledge/*.md files = 65
GREEN kengaku round-63 trio gate : 36   RED 29
GREEN tsukuroi-style rule        : 37   RED 28
GREEN chousa-style rule          : 37   RED 28
GREEN kumitate-style rule        : 25   RED 40
frozen list == recomputed red set: True  (computed 29, frozen 29)
```

The recomputed red set equals `corpus/evidence/round64/trio-red-at-base.txt`
entry-for-entry (`SET equal: True`) — the frozen list is confirmed against the
gate as committed.

**The one entry the kengaku rule alone condemns.** `tb2-grader-vacuity-triage.md`
is red for kengaku (`missing= verified-at,recheck`) but **green** under the
tsukuroi and chousa rules: it carries `verified-at: 2026-10-28` at line 13 and
`recheck:` at line 14 — inside the file, but **one line past kengaku's 12-line
window** (`plans/round63_gate_checks.py:79` `TRIO_WINDOW = 12`; the file's first
`## ` heading is at line 16). Its `source:` block is 12 lines of `S179`–`S190`
rows, so the trio cannot start earlier without editing the opening bytes —
which C3's kill rule forbids ("An entry 'repaired' by editing its opening bytes
instead of appending → the claim is dead"). The claims doc's own note (`plans/round-64-claims.md:181-182`: "two entries
carry `verified-at` but fail the gate's first-12-lines/before-first-heading/order
rule") is close but not exact, measured **at the base tip**
(`git show 5f517fe…:<file>`, receipt `base_tip.txt`): **two** entries carry the
*string* `verified-at`; exactly **one** carries a column-0 `verified-at:` **key**
outside the window (`tb2-grader-vacuity-triage.md:13`); the other
(`tb2-cancel-async-tasks-grader.md:74`) carries it as prose inside a
`Round-61 verified-at: …` line, which is not a key. **Reported, not edited** —
the claims file is frozen.

---

## Per-sibling table (owns / does-not-own, quoted line + path:line)

| Sibling | Owns (quoted) | Does-not-own for this round (quoted) |
|---|---|---|
| **kama** | `:3` "**Domain:** local model serving & endpoint health — local LLM endpoints, baseURL"; `:10` "producer discovery & read-only service inspection of local serving ports"; `:17` "lane instruments … `tools/kama-ollama-evidence.py` (offline Ollama capture replay)" | Does not own a gRPC/kv-store service: its ground is *model* endpoints and its registry holds `:8080`/`:34113` only (`registry/endpoint-consumers.tsv:35-37`); `:63-65` scopes its own live fixture to "the process this tool started … any other unregistered endpoint still needs L0" |
| **tameshi** | `:3` "**Domain:** verification-fixture craft — the reusable method of honest checks: hermetic suites, mutation testing, fail-closed arms, verdict-line discipline, no-permissiveness audits, before/after proof"; `:7` "**Owns:** the method, documented from the fleet's existing gates as primary surfaces" | Does not own any product domain: `:14-15` "**Refuses:** product domains — every lane's gate remains its own; tameshi owns only the reusable craft"; `:16-17` "Never edits a sibling's gate code (read-only probes; recommendations travel in round reports)". Its ten mutation legs (`tools/mutate-and-run.sh:8-20`) are kumitate/kagi gates — no benchmark grader, no gRPC |
| **chousa** | `:3` "**Domain:** deep-research method (調査) — the reusable craft of source research"; `:5-9` "**Owns:** question framing; source hierarchy …; claim-vs-source verification" | Does not own the trio *rule*: its metadata mode (`:684` "Metadata mode checks source, verified-at and recheck in the Markdown header") breaks at the first `## ` heading (`tools/research-gate.sh:3606`) and checks presence, not order. `:10-16` "**Refuses:** … model-quality or evaluation claims (→ kengaku)" |
| **kumitate** | `:3` "**Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime"; `:15` "The lane's own instruments `scripts/*.mjs` … and its learning registry `corpus/SOURCES.md` (checked by `scripts/sources-check.mjs`)" | Does not own kengaku's gate: `scripts/sources-check.mjs:381-383` checks the trio in the **first 5** lines, presence-only, no order, no window-before-heading. `:31` "Local model serving and endpoints → kama. Prompt and skill craft → kotoba. Research method → chousa." — no mention of grader replay or a corpus-wide trio sweep |
| **tsukuroi** | `:3` "**Domain:** host operability & system repair (繕, mending)"; `:8` "**Owns (surfaces, all read-only probes):** pacman state …" | Does not own the trio rule: `tools/check-knowledge-header.py:9-27` — column-0 keys outside fences, **last occurrence operative**, `verified-at` must be an ISO date. `:25-26` "**Refuses:** endpoint/model serving health (→ kama), secrets (→ kagi), binary RE of drivers" — no grader or gRPC surface |
| **chousa/kumitate/tsukuroi** (path containment) | chousa `tools/build-spans.py:107` `os.path.commonpath([real, self.root]) != self.root`; kotodama `tools/source-audit-inventory.py:119` `resolved.is_relative_to(root.resolve())`; kaidoku `tools/round-40/ledger-status.py:105`; mado `tools/mado-assessment.py:65` | Containment guards exist as **prior art** for C2's `_resolves` repair, but no sibling owns kengaku's `plans/round63_gate_checks.py` gate (kengaku-only file) or its `ESCAPE` finding id (`grep -rIn -E "DETAIL escape|finding id .ESCAPE"` → 0 hits in siblings) |
| **kotoba** | `:3` "**Domain:** prompt & skill craft"; `:33` "Sibling census re-pin (round 74, freshness): all 20 § Adjacent lanes re-read at frozen fleet heads" | Its census is a **lane-scope** census, not a grader-class census (`corpus/knowledge/sibling-overlap-census-round74.md`); confirmed as prior finding in `kengaku-shokunin/.ufo/waves/round-63/w1/SiblingOverlap.md:14` |
| **kake** | `:3` "**Domain:** web properties & publishing"; `:17` "The lane's own gates: `scripts/freshness-sweep.mjs`, `scripts/probe-delta.mjs`" | Its freshness sweep re-verifies **cited paths / pins** over its own corpus (`scripts/freshness-sweep.mjs:5-12`, `:247`); it does not classify provenance-trio state and does not sweep kengaku's corpus |
| **kaidoku** | `:3` "**Domain:** reverse engineering of shipped artifacts with REA on this Linux" | Its `tools/round-35/c1-coverage-counter.py:105-140` does trio-presence + README-index checks — but over **kaidoku's own two named entries** (`ENTRIES` dict, `:16-19`), not a lane-wide sweep; and it uses regex presence (`:105-111`), not order-in-window |
| **kagi / kasegi / mori / souji / tabi / mado / audio / game-dev-2d / game-dev-3d / lore / revenger / kotodama** | `:3`/`:5`/`:6`/`:9` domain lines: secrets & vault ops; bounty & security research; fleet & host observability; fleet repository & workspace hygiene; browser & web-interaction craft; desktop & compositor craft; game audio production; 2D/3D game production; fictional-world records; reverse engineering of shipped artifacts; linguistic-cultural worldbuilding | None owns a grader, a gRPC service, a grader-class census, or a trio sweep. `mori-shokunin/PROVINCE.md:67` names the boundary: "\| kama \| Owns local model-serving and endpoint health; mori does not infer serving health from host/resource signals." `tsukuroi-shokunin/PROVINCE.md:25` likewise routes endpoint health to kama |

---

## Contested scope — named for the L1 to route, NOT absorbed

**C-1 — the trio *rule* is fleet-ambiguous; the C3 repair form is not portable.**
Four lanes each enforce a provenance trio over their own corpus with four
different rules (kumitate: first-5-lines presence; tsukuroi: last-occurrence
operative, column-0; chousa: before-first-heading presence; kengaku: 12-line
window, before-first-heading, **in order**). Measured on the same 65 kengaku
entries: red counts **29 / 28 / 28 / 40** respectively (`measure_final.txt`).
The frozen C3 repair form is **append-only** and **kengaku-rule-specific**:

```
AFTER the frozen C3 append-only addendum block on all 29 red entries:
  still RED under kengaku round-63 trio gate : 29/29
  still RED under tsukuroi-style rule          : 26/29
  still RED under chousa-style rule            : 28/29
  still RED under kumitate-style rule          : 29/29
```

A dated addendum carrying `verified-at: 2026-11-03` at EOF repairs **0/29**
under kengaku's own rule (the gate stops at line 12 / the first heading) — it
only helps under a last-occurrence rule (3/29 flip). The frozen claim is
correct about this (`plans/round-64-claims.md`: TRIO-ADDENDUM is "opening
predates the rule" and the sweep is a *new* instrument, `plans/round64_trio_sweep.py`,
which imports the gate's `trio_missing` so the OPEN class cannot drift). **The
routing ask for the L1:** if any sibling later adopts "trio-green" as a
fleet-wide notion, it must be told that *green* is rule-relative — a kengaku
entry that is TRIO-OPEN can be red under tsukuroi's rule and vice-versa. Do not
let this round's `red=0` be read as a fleet-wide green. *(Measured on the
current working tree, which now carries 29 `## Freshness addendum (round 64)`
blocks: kengaku rule still 36 green / 29 red; tsukuroi-style 39/26; chousa-style
37/28; kumitate-style 25/40 — `current.txt`.)*

**C-2 — the port plane (5328) sits on kama's registry vocabulary.** kama owns
"producer discovery & read-only service inspection of local serving ports"
(`:10`) and classifies unknown listeners as `FOREIGN_SERVICE`
(`tools/kama-probe.sh:29`). The C1 probe starts a lane-authored gRPC server on
`127.0.0.1:5328` (host-visible: the frozen house shape keeps the network
SHARED). kama's own L0 line reads "L0 must approve any endpoint outside the
declared local model registry … any other unregistered endpoint still needs L0"
(`kama-shokunin/PROVINCE.md:63-65`; L0 row `kama | round-16` in
`/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:58`). **Not a claim
conflict** (a benchmark fixture is not a model endpoint, and 5328 is not a
kama registry row), but the L1 should decide once whether a *lane-authored
benchmark fixture* on an unregistered loopback port needs the same L0 note
kama's live fixture is pending. Also: **port 5328 is free now** — `ss -ltn |
grep -E "5328|8080"` → no match, rc 1 (observed at scan time).

**C-3 — a stale cross-lane pointer in kama's province (report-only).**
`kama-shokunin/PROVINCE.md:143-144` cites
`kengaku-shokunin/.ufo/waves/round-31/w1/out/ConnSibling/overlap.md` as the
evidence that "kengaku excludes the model-serving plane". That path does not
exist: `find .ufo/waves/round-31 -name "*overlap*"` → 0 hits; the round-31
connector artifact is `.ufo/waves/round-31/build/R31ConnSibling.md`. The
substance still holds (kengaku `PROVINCE.md:25-26` refuses the model-serving
plane) but the cited path is dead. **Route to kama; do not edit kama's file
from here.**

**C-4 — the depth-gate `_resolves` repair (C2) has fleet prior art, but no
sibling owns the finding id.** Sibling root-containment guards exist
(chousa `tools/build-spans.py:107`, kotodama `tools/source-audit-inventory.py:119`,
kaidoku `tools/round-40/ledger-status.py:105`, mado `tools/mado-assessment.py:65`),
and kotoba already skips absolute pointer tokens by rule
(`kotoba-shokunin/verifiers/check_report_pointers.py:60-61` "Absolute (`/...`)
and home (`~/...`) tokens are skipped"). kengaku's C2 goes further — it *names*
the escape (`DETAIL escape=`, finding id `ESCAPE`) and fails on it. Pattern G
(`DETAIL escape|finding id .ESCAPE`) → **0 files, 0 lanes**: the id is
kengaku-local. The L1 should note in the round report that the `ESCAPE` id and
the fail-on-escape verdict are kengaku-local, so a sibling gate citing "the
escape rule" does not silently inherit them.

**C-5 — a kengaku entry contests kama's province, and kama's round-64 wave-b
scan has already routed it (concurrent, this round).** kama's own
sibling-overlap seat for round 64
(`kama-shokunin/.ufo/waves/round-64/b/CN02SiblingOverlap.md:56` §3c row C1, and `:70` §4)
records: "kengaku `corpus/knowledge/served-endpoint-identity-pin.md` (rows
'owning process', decision rule 3, measured pin table) | Kengaku builds its own
served-endpoint pin from tokenised `/proc/<pid>/cmdline`, the same identity fact
kama's C1 binds. Kengaku's rule 3 defers flag a…" and routes it: "kengaku (C1):
cite kama's binding for the served-endpoint identity; kengaku keeps its battery
and pin fields." The entry is real and pre-dates this round
(`kengaku-shokunin/corpus/knowledge/served-endpoint-identity-pin.md:1-3`, header
`source: S178 … verified-at: 2026-10-28`; its "owning process" row is
`/proc/<pid>/cmdline`, tokenised). **This seat does not absorb it and does not
edit kengaku's entry** — but the L1 must know the same-round kama scan already
filed it, so the two waves' routing lines meet. It does **not** touch C1/C2/C3:
the C1 probe's server is a gRPC kv-store fixture, and the contested entry is
about a **served model endpoint** identity pin.

---

## Sibling-scope boundaries this seat did **not** cross

- No sibling file was edited; all sibling reads were `read`/`grep`/`bash` on
  absolute paths.
- No sibling's gate was executed against a sibling's corpus (tsukuroi's
  `check-knowledge-header.py` requires `tools/_revision.py` in the target lane —
  kengaku has none, `ls kengaku-shokunin/tools/_revision.py` → absent — so it
  cannot be pointed at kengaku anyway; kumitate's `sources-check.mjs` is
  `--self`-scoped; chousa's `research-gate.sh` was **read**, not run).
- The 29-entry red set was re-derived by **importing kengaku's own gate
  function** (`trio_missing`), never by re-implementing the rule.
- No port was bound; `ss -ltn` was used read-only. No git mutation.
