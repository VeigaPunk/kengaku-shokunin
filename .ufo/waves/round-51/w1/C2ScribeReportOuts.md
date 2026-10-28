# C2ScribeReportOuts — round 51 report-out list (what leaves this lane, to whom, on what pointer)

Seat: `C2ScribeReportOuts` (scribe). Round 51, hyaku run 11, wave 1. Lane: `kengaku-shokunin`.
Item: *draft the round's report-out list — for each sibling lane that the attribution names as an
owner, one line stating what is being handed over and what evidence pointer supports it; ground
every line in a ledger row id and a quoted sibling line from the connector seats' maps; never absorb
a sibling's scope into this lane.*

Binding file read in full first: `plans/round-51-claims.md` (§C2, its predicate, kill rule, limits).
Frozen instrument read: `plans/round51_routing.py`. Base ledger read:
`corpus/routed-findings.jsonl` (71 rows, unchanged vs the freeze).

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7      # lane HEAD measured (child of the stage-1 freeze)
REV e07f131cf7037e58a21db6e1f3986cf401ad257c      # stage-1 freeze (ancestor)
REV 9baaeee8e9e13b969f06e6c33597a35af1868c7c      # fleet root, quoted from C2ConnProtocol (not re-measured here)
```

Read-only against the lane. Nothing landed; the only file this seat wrote is this report.

## 1. Axes named

| axis | this seat's relation to it |
|---|---|
| **adjacency** (primary — C2, the judged axis) | the report-out list *is* the axis's output artifact: `AXES.md:16` "Cross-domain awareness — evidence belonging to another domain reported, not absorbed \| Lane reports name contested scope; integrator arbitrates". A handover that names its owner and its pointer is "reported"; one that stays in this lane's ledger as `kengaku` is "absorbed". |
| **freshness** (C1) | named, untouched. No `PROVINCE.md` row, no `round51_surfaces.py` / `round51-surfaces.json` entry is read for a verdict or proposed for change; the only `PROVINCE.md` reads are line pins used as *sources* of ledger rows. |

## 2. The attribution is not one artifact — it changed three times inside this seat's window

Measured with identity pinned, because the answer to "which sibling owners does the attribution
name" changed between reads of the same path:

| read (2026-10-28 -03:00) | `w1/C2ExecLedgerMerge.jsonl` | rows | owners | dispositions |
|---|---|---|---|---|
| 15:34 | 60685 B | **75** (71 base + `R51-R1..R4`) | `kengaku` 71, `kama` 2, `protocol` 1, `unowned:integrator` 1 | fixed-verified 41, accepted-risk 28, refused-out-of-scope 2, **routed 4** |
| 15:38:13 | 62532 B, md5 `3e381ce8…`, sha256 `08a8d2b0…` | **71** | `kengaku` 71 | fixed-verified 42, accepted-risk 24, fixed-historical 3, refused-out-of-scope 2, **routed 0** |
| 15:38:54 (latest read) | 66130 B, md5 `7b990ffd…`, sha256 `cc5acda1…` | **75** | `kengaku` 71, `kama` 2, `protocol` 1, `unowned:integrator` 1 | fixed-verified 41, accepted-risk 28, refused-out-of-scope 2, **routed 4** |

The eight executor fragments, unchanged across all three reads, are the per-seat record:

```
fragments  C2ExecA..H.jsonl (8)
distinct ids in fragments 71   owner counts {'kengaku': 71}
```

Two readings of the same round are therefore live, and the L1's landing decision picks between them:

- **Variant A (71 rows, 15:38:13):** the attribution names **no sibling lane**. Report-out list =
  **empty**; every one of the 71 rows is `kengaku`, and the structural predicate passes on it (§5).
- **Variant B (75 rows, 15:34 and 15:38:54):** four `routed` rows name `kama` ×2, `protocol` ×1,
  `unowned:integrator` ×1. They also exist as candidates in the integration tool
  `.ufo/waves/round-51/integrate_ledger.py` `NEW_ROWS` (`:46-92`), appended unconditionally at
  `:173`. `C2RevRecount.md` rejected an earlier 75-row artifact as landable, verbatim: *"REJECTS the
  current merged artifact as landable: at sha `dfed0019` (75 rows) the frozen predicate prints
  `PREDICATE R51-C2 fail` in a clean clone (`SOURCE missing=2`, `CHECK_FAILED 1` on `R42-R2`) and the
  lane's own `plans/routed_open.py` exits 1 with `invalid=2`. Blocking: F1 … and F2 (`rows=75` vs the
  frozen after target `rows=71`; the counter cannot catch either)."*

Both variants were re-measured with the frozen command in clean clones (§5): the 71-row variant
prints `PREDICATE R51-C2 pass`, the 75-row variant prints `fail` on the two untracked sources. **The
report-out list is state-independent in one respect:** the four lines in §3.2 are the only sibling
owners any variant of this round's attribution names, so they are the complete handover set whenever
those rows land, and the empty list is the complete answer whenever they do not.

**Live hazard:** the tool and the artifact disagree — re-running `integrate_ledger.py` today re-appends
`NEW_ROWS` and reproduces the 75-row variant; the 71-row variant is not that tool's output as it
stands, and the file oscillated between the two inside 40 s.

## 3. The report-out list

### 3.1 Variant A — what a 71-row landing hands over: nothing

Zero rows carry a non-`kengaku` owner, therefore **zero lines**. This is not a gap this seat is
papering over: `C2ConnProtocol.md` §4 reaches the same conclusion from the protocol text — *"the C2
move is satisfied by **completing `owner` + `disposition` on lane-owned rows**, not by manufacturing
routed-out rows. Any row marked `routed` or `referral` needs a non-`kengaku` owner *and* a `next`
field; on the evidence above there is no row for which that is truthful today."* Under this variant
the round's report-out is carried entirely by the connector maps' class rulings (§4), not by ledger
rows — and the L1 must say so in the round notes rather than let a `routed 0` receipt read as
"nothing was reported out".

### 3.2 Variant B — the four candidate handovers, each grounded in a row id and a map quote

If the L1 rules the row-count question in favour of the candidates, these are the lines. Format:
**owner ← row id** · what is handed over · evidence pointer · quoted sibling line from the connector
map (map file + section, and the underlying line re-read first-hand at the revision named).

**1. `kama` ← `R51-R1` (`serving-plane-identity-pin`, `routed`, `status: open`)**
Handed over: serving-plane **health and flag authority** for the live LFM3 pair (`:45669` direct,
`:1234` router `lfm3-server.service`, model `LFM3-1.7B`, `n_ctx 32768`, build `b1-39ebd2`); this lane
keeps only the capture-time identity pin. `next: "kama: serving-plane health/flag authority for the
LFM3 pair (capture 2026-10-28)"`.
Evidence pointer: `source` `PROVINCE.md:15` — **wrong row** (§6 D-c) — and `note` →
`corpus/knowledge/served-endpoint-identity-pin.md`, **untracked at the tip** (§6 D-b).
Sibling line: `C2ConnServing.md` §"Both sides, quoted" → `kama-shokunin/PROVINCE.md:12` (re-read:
"served-model-id reconciliation \| `GET /v1/models` vs `--alias` vs the configured model id") and
`kama-shokunin/PROVINCE.md:44` ("answers *\"is the thing at this baseURL the model this config
believes it is, right now\"* — never *\"is the model good\"*").
Counter-critique carried verbatim: `C2CritSpotAttribution.md` §O1 — *"R51-R1 I agree with **as to
health**, and the owner `kama` is defensible on …"* — and it records that "flag authority stays
kama's" contradicts `kama/PROVINCE.md:10` ("never claims an installed server"); the smallest
correction is to narrow the `next`, not to change the owner.

**2. `kama` ← `R51-R4` (`served-model-service-unit-absent`, `routed`, `status: open`)**
Handed over: the retirement question for `qwen-coder.service` / `:34113` (unit gone, `curl` → `000`),
i.e. whether it is retired in favour of the LFM3 pair. `next: "kama: whether the qwen-coder unit is
retired in favour of the LFM3 pair"`.
Evidence pointer: `source` `PROVINCE.md:14` — re-read: "| Served local model | `http://127.0.0.1:34113`
— `/v1/models`, `/health`, `/v1/chat/completions` …" — **the pin is correct for this row**.
Sibling line: `C2ConnServing.md` → `kama-shokunin/PROVINCE.md:13` (re-read: "liveness/readiness probe
conventions \| `/health`, `/props`, `/slots`") and `kama-shokunin/PROVINCE.md:10` ("kama governs
discovering whatever serves these ports and never claims an installed server").
`C2CritSpotAttribution.md` §O1 agrees with this row outright.

**3. `protocol` ← `R51-R2` (`fleet-ledger-attribution-gap`, `routed`, `status: open`)**
Handed over: the fleet **routed-finding ledger schema** question — no sibling ledger carries both
`owner` and `disposition` (`C2ConnLedgerSchema.md` §1–§3: 20 of 21 lanes hold zero `corpus/*.jsonl`;
the private partial schemas are kagi `owner`+`status`, tsukuroi `owner`+`action` / `recipient`+`state`,
tabi 4-value `disposition`). `next: "protocol: fleet routed-finding ledger schema (owner + disposition
+ next)"`.
Evidence pointer: `source` now `corpus/lessons/round-51.md:1` in `integrate_ledger.py`; the file
**exists in the working tree (5655 B, 15:37) but is UNTRACKED**, so it resolves at write time and not
at the committed tip (`PROTOCOL.md:356`).
Sibling line: `C2ConnProtocol.md` §3 → `PROTOCOL.md:207-208` (re-read: "**Integrator of record.** The
integrator this protocol assigns work to is the round's `protocol` lane — a role, not a separate
rostered lane") and `PROTOCOL.md:457-459` ("Contested scope — evidence or work is reported in the lane
report; the integrator arbitrates by refining `PROVINCE.md` and records the ruling in the round
notes").
**Disagreement, stated not smoothed:** `C2ConnLedgerSchema.md` §3 routes the same question as "an
integrator call … worth one routed row with a non-kengaku owner"; `C2ConnTooling.md` §3 assigns the
fleet-rule classes to `unowned:integrator`; the candidate chose `protocol`. All three pass the
predicate; the L1 owns the choice.

**4. `unowned:integrator` ← `R51-R3` (`domain-source-trees-absent`, `routed`, `status: open`)**
Handed over: restore-or-retire decision for three surfaces `PROVINCE.md` describes as resolving —
`~/Projects/webzites/repos/llm-wiki`, `~/archive/bench-arena`, `~/Projects/bounties/ledger/telemetry.jsonl`
— absent on this host at 2026-10-28. `next: "operator/integrator: restore or retire the three declared
source trees"`.
Evidence pointer: `source` `corpus/evidence/round51/surfaces/paths.txt:1` — **untracked** at the tip
(§6 D-b).
Sibling line: `C2ConnProtocol.md` §3 → `PROTOCOL.md:464-465` (re-read: "Only integrator roles write
main-repo files: `MISSION.md`, `AXES.md`, `CORPUS.md`, and `scripts/` are operator-side integrator
files").
**Limit on this line:** no connector map names an owner for *host paths outside the repo*; the quote
covers operator-side *files*. The handover is by authority, not by a sibling's named surface, and
this seat does not upgrade it into one. `unowned:integrator` is a value in the counter's vocabulary
(`plans/round51_routing.py:44-45`), not a rostered lane; the claim text admits it
(`round-51-claims.md` §C2: "or `unowned:integrator`").

## 4. Sibling lanes the connector maps name as owners, with **zero** rows to hand over

Under either state these carry no ledger row. Every entry is 0 rows at this tip (no sibling lane name
occurs in any field of any of the 71 base rows — `C2ConnProtocol.md` §2 sweep, re-confirmed by the
all-`kengaku` fragment census in §2).

| lane | class the map assigns it | rows | quoted sibling line (from the map, re-read) |
|---|---|---|---|
| `aggregator` | fleet corpus review; durable routed-defect queue | **disputed 0–2** | `shokunin.conf:21` "aggregator\|.\|cross-lane quality, mint and dormancy calls, corpus review"; `PROTOCOL.md:245` "The aggregator mirrors each routed defect into the owning repo's `corpus/lessons/` and keeps an **open routed-defects row** in its ledger until"; `PROTOCOL.md:326` "The **aggregator** lane is a main-repo lane that reviews every child repo's `corpus/` each round" |
| `kumitate` | wave dispatch / coordinator topology | 0 | `kumitate-shokunin/PROVINCE.md:24` "Multi-agent coordinator topology — orchestration topology **decisions** (how a wave's seats are arranged: which topology, what a coordinator may delegate, what the arrangement costs)" |
| `kotoba` | dispatch-prompt craft (the rule; the instance text stays in-lane) | 0 | `kotoba-shokunin/PROVINCE.md:13` "Agent-definition, always-on (AGENTS.md-class) and dispatch-prompt craft"; `kumitate-shokunin/PROVINCE.md:29` "Local model serving and endpoints → kama. Prompt and skill craft → kotoba. Research method → chousa." |
| `chousa` | external claim-vs-source verification | 0 | `chousa-shokunin/PROVINCE.md:5-6` "**Owns:** question framing; source hierarchy (primary / secondary / aggregator / unsourced); citation chaining and hop resolution; claim-vs-source verification" |
| `kagi` | credentials of the `:8791`/`:8793` cascade shims | 0 | `kama-shokunin/PROVINCE.md:42` "**Refuses:** model quality/eval (kengaku), credential material & auth flows (kagi)" |
| `tameshi` | verification-fixture method (rows stay `kengaku`: `R42-R3-27`, `R42-R3-34`, `R45-S5-7e` are this lane's own artifacts) | 0 | `tameshi-shokunin/PROVINCE.md:3-5` "**Domain:** verification-fixture craft — the reusable method of honest checks: hermetic suites, mutation testing, fail-closed arms, verdict-line discipline, no-permissiveness audits, before/after proof." |
| `souji` | residue listing, not the guard (`R39-R5` is `closed` in-lane) | 0 | `souji-shokunin/SKILL.md:381` "Audit private scratch \| Only an explicit own scratch root, including its actual wave-slot spelling; never broad `/var/tmp` fallback or another seat/slot." (a scratch-audit row, not a routed-findings ownership line — quoted as the map does, with that limit) |
| `mori` | wave-settlement *reading* (acceptance stays kumitate's) | 0 | `mori-shokunin/PROVINCE.md:46` "mori reports filesystem shape; kumitate owns orchestration/result semantics"; `:136-137` "Planning, slot acquisition, retrying and adjudicating dispatch remain **kumitate/operator**-owned" |
| `tsukuroi`, `revenger`, `lore`, `mado`, `audio`, `game-dev-2d`, `game-dev-3d` | none today | 0 | **unrouteable under the frozen counter** — the accepted set is 17 names and these seven conf lanes are not in it (§6 D-a). A handover to any of them prints `owner … not a fleet lane` and fails C2. |

## 5. Counter measurements (scratch clones, read-only, no `--run-checks`)

Both variants were measured with the frozen command in a scratch clone at `4090c3d`, the artifact
copied over `corpus/routed-findings.jsonl`:

```sh
export TMPDIR=/fast/scratch/hyaku/kengaku-r51/C2ScribeReportOuts
git clone --shared -q /home/vgpnk/Projects/shokunin/kengaku-shokunin "$TMPDIR/lane"
git -C "$TMPDIR/lane" rev-parse --show-toplevel   # …/C2ScribeReportOuts/lane
git -C "$TMPDIR/lane" rev-parse HEAD              # 4090c3db79d11279ab5e5121ba25e74aa316e6e7
cp .ufo/waves/round-51/w1/C2ExecLedgerMerge.jsonl "$TMPDIR/lane/corpus/routed-findings.jsonl"
cd "$TMPDIR/lane" && python3 plans/round51_routing.py --lane .
```

**Variant B artifact (75 rows, latest read 15:38:54, sha256 `cc5acda1…`)** — verbatim (the 15:34
artifact printed the same counters; only the two `DETAIL` lines differed, showing the then
`:line`-less sources):

```
LEDGER corpus/routed-findings.jsonl rows=75
FIELDS complete=75 incomplete=0
OWNERS attributed=75 unattributed=0
DISPOSITIONS set=75 bad=0
SOURCES resolved=73 missing=2
CHECKS present=75 absent=0
VERIFIED ran=0 passed=0 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
  DETAIL SOURCE R51-R2 source 'corpus/lessons/round-51.md:1' does not resolve
  DETAIL SOURCE R51-R3 source 'corpus/evidence/round51/surfaces/paths.txt:1' does not resolve
PREDICATE R51-C2 fail
```

**Variant A artifact (71 rows, 15:38:13, md5 `3e381ce8…`)** — verbatim:

```
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=71 incomplete=0
OWNERS attributed=71 unattributed=0
DISPOSITIONS set=71 bad=0
SOURCES resolved=71 missing=0
CHECKS present=71 absent=0
VERIFIED ran=0 passed=0 failed=0
CLOSE_REFS resolved=3 missing=0
NEXT violations=0
PREDICATE R51-C2 pass
EXIT=0
```

Reading: the 71-row variant is structurally landable; the 75-row variant is not, on two unresolved
sources that are both fixable by committing `corpus/lessons/round-51.md` and the evidence tree — the
`integrate_ledger.py` sources are now `:line`-qualified, which answers the `<path>:<line>` contract the
reviewer's F1 named. Neither run executes the 41 `fixed-verified` checks; that hazard is cited from
`C2ExecClosedChecks.md:125-136`: `VERIFIED ran=41 passed=2 failed=39` under the frozen invocation and
`passed=41 failed=0` with `cwd=lane`.

## 6. Defects and conflicts observed while drafting (reported, not fixed)

**D-a — the frozen counter cannot accept seven real lanes as owners.** `load_owners` matches
`^\s{0,6}([a-z][a-z0-9-]{2,15}):\s*\{`; `shokunin.conf` lists lanes as `id|repo|axes` inside
`LANES="…"`, so zero lines match and the vocabulary is the hardcoded 17-name literal. Measured by
importing the counter's own function:

```
instrument owners: 17
conf lanes: 23
conf lanes NOT accepted by instrument: ['audio','game-dev-2d','game-dev-3d','lore','mado','revenger','tsukuroi']
accepted but not a conf lane: ['unowned:integrator']
```

Five independent seats measured the same (`C2ConnTooling.md` F3, `C2ConnLedgerSchema.md` §4,
`C2ConnProtocol.md` §5.1, `C2ConnServing.md` C-2, `C2ExecD.md`; `C2CritSpotAttribution.md` reports
four). The claim text says "every `owner` names a fleet lane from `../shokunin.conf`"; the code does
not read that roster.

**D-b — pointers that do not resolve at the committed tip.** `corpus/lessons/round-51.md`
(present, UNTRACKED), `corpus/evidence/round51/surfaces/paths.txt` (UNTRACKED),
`corpus/knowledge/served-endpoint-identity-pin.md` (UNTRACKED). `PROTOCOL.md:356` — "An evidence
pointer must resolve at *closure* time, not only at write time" — is the rule this breaks; the
clean-clone run in §5 is what makes it visible, because the working tree hides it.

**D-c — `R51-R1`'s `source` pin points at the wrong row.** `source: "PROVINCE.md:15"`; re-read at
REV 4090c3d, `PROVINCE.md:15` is "| Route telemetry | `~/Projects/bounties/ledger/telemetry.jsonl` —
**ABSENT**, reconfirmed round 14 …", while the claim is about the LFM3 pair.
`grep -n 'LFM3\|45669\|lfm3' PROVINCE.md` → **0 hits**: the surface table does not mention the pair at
all. The counter cannot see this (its `SOURCE` test is file-granular — `src = r["source"].split(":")[0]`),
so the row passes while citing nothing that carries it. Same class as ledger row `R45-S5-1`
(`row-anchor-wrong-line`).

**D-d — a connector map's own line pin is off by one.** `C2ConnTooling.md` §2 cites
`kumitate-shokunin/PROVINCE.md:28` twice for "Prompt and skill craft → kotoba". Re-read:
`:28` = "- MCP/OAuth security practice (token passthrough, confused deputy) → kasegi / kagi." and the
cited sentence is `:29`. The map flags exactly this defect class in this lane (its F1/F2) and then
commits it against a sibling; the sentence it quotes is real, the line number is not.

**D-e — tool and artifact disagree, and the artifact oscillates.** `integrate_ledger.py:173` appends
`NEW_ROWS` unconditionally, so a re-run reproduces the 75-row variant; the 71-row variant at 15:38:13
is not that tool's output. Measured: the same path held 75 rows (15:34), 71 rows (15:38:13) and 75
rows again (15:38:54). Whoever lands must pin which variant the claim is measured on, or the next
re-run silently changes the ledger the predicate was scored against — and `rows=71` vs `rows=75` is
the after-target's own number.

**D-f — `next` carries two meanings in one file.** In the 75-row variant, 32 rows carry `next`: the 4
`routed` rows (where it is a routing target) and 28 `accepted-risk` rows (where it means "re-open
when …", e.g. `R40-R5` "kengaku round 52 backlog"). No predicate violation — the counter requires
`next` only for `routed`/`referral` and ignores extra keys — but a reader of the ledger cannot tell a
routing target from a backlog note without the disposition.

**D-g — the connector brief named two files that do not exist.** `C2ConnProtocol`'s item names
`protocol-shokunin/PROVINCE.md` and `aggregator-shokunin/PROVINCE.md`; measured here
(`ls: cannot access … No such file or directory`) and in that map's §1. Both lanes are fleet-root lanes
(`shokunin.conf:20-21`), so their province is `PROTOCOL.md` + lane-owned root ledger sections, not a
`PROVINCE.md`.

**D-h — `aggregator` assignment is a live three-way disagreement.** `C2ConnServing.md`'s ledger table
assigns `R40-R3` (`round-close-unregistered`) and `R42-R4` (`sources-correction-rule`) to `aggregator`
("fleet rule / process … row's own note: the rule 'exists only outside the lane: …/CORPUS.md:116-118 …
read-only'"); the attribution assigns both `kengaku` `fixed-verified` (`C2ExecA.jsonl`,
`C2ExecB.jsonl`), and `C2ConnProtocol.md` §4 assigns them `kengaku` too ("`SKILL.md` is its registry
home"; `sources-correction-rule` "closed in-lane at `corpus/QUALITY.md:759`"). Reported verbatim; not
ruled here.

## 7. Commands run (verbatim, in order)

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r51/C2ScribeReportOuts && export TMPDIR=$_
df -h /fast                                     # /dev/nvme1n1p2 804G 249G used 555G avail 31%
wc -l corpus/routed-findings.jsonl              # 71
git -C kengaku-shokunin rev-parse HEAD          # 4090c3db79d11279ab5e5121ba25e74aa316e6e7
python3 -c "…json.loads C2Exec*.jsonl…"         # fragments 8, distinct ids 71, owners {kengaku:71}
python3 -c "…C2ExecLedgerMerge.jsonl…"          # 15:34: 75 rows/4 routed; 15:38:13: 71 rows/0 routed;
                                                # 15:38:54: 75 rows/4 routed again (oscillation, D-e)
stat -c '%s %y' C2ExecLedgerMerge.jsonl; md5sum; sha256sum
                                                # 66130 B 15:38:54, md5 7b990ffd…, sha256 cc5acda1…
python3 -c "…load_owners(Path('/home/vgpnk/Projects/shokunin'))…"   # 17 accepted, 7 conf lanes rejected
for spec in kumitate:3,24,28,29 kotoba:3,13,68 chousa:5-6 tameshi:3-5 mori:46,136-137 \
            kama:10,12,13,42,44 souji/SKILL:381 AXES:16 PROTOCOL:117,118,207,208,241-245,326,352,356,377,398-400,435,457-459,464-466,468-469,475-476,502-503
                                                # every quoted sibling line re-read first-hand
grep -n 'LFM3\|45669\|lfm3' PROVINCE.md          # 0 hits (D-c)
git ls-files --error-unmatch corpus/lessons/round-51.md corpus/evidence/round51/surfaces/paths.txt \
                             corpus/knowledge/served-endpoint-identity-pin.md   # all UNTRACKED (D-b)
grep -n 'NEW_ROWS' .ufo/waves/round-51/integrate_ledger.py    # :46 definition, :173 unconditional append
git clone --shared -q … lane; git -C lane rev-parse --show-toplevel
cp C2ExecLedgerMerge.jsonl lane/corpus/routed-findings.jsonl
cd lane && python3 plans/round51_routing.py --lane .   # §5, both states
```

No `--run-checks` was run by this seat. The frozen-command check result is cited, not re-derived,
from `C2ExecClosedChecks.md:125-136`.

## 8. Limits

- The attribution moved three times inside this seat's window (§2, D-e) and was still the 75-row
  variant at the last read. Everything here is pinned by hash and mtime, but a further rewrite would
  change which variant §3.1/§3.2 applies to; the fragment census (71/71 `kengaku`) is the most stable
  leg, because the eight fragments did not change at all.
- `REV 9baaeee8…` (fleet root) is quoted from `C2ConnProtocol.md`, not re-measured; the sibling lines
  themselves were re-read in the working trees of `kumitate`, `kotoba`, `chousa`, `tameshi`, `mori`,
  `kama`, `souji` and of the fleet root — readable and clean enough to quote, but not pinned by this
  seat.
- §4's zero-row entries assert "no ledger row carries this class", a fact about the 71 base rows, not
  about the fleet's whole surface. A class nobody opened is invisible to C2 (claims §Limits).
- I did not decide any owner or any disposition. §3.2 reports what the candidate assigned and what the
  maps quote; where the maps disagree (D-h, §3.2 line 3) both readings are printed.
- No check was executed; nothing here says which `fixed-verified` checks pass.
- Tooling: nothing installed or upgraded this seat — no pacman/uv/npx transaction was attempted
  (pacman is paused host-wide; nothing was needed).

## 9. Scratch

`/fast/scratch/hyaku/kengaku-r51/C2ScribeReportOuts` was created, held one `--shared` clone
(`…/C2ScribeReportOuts/lane`, toplevel verified before any write) and three counter runs, and was
removed before yield. Free space seen: `/dev/nvme1n1p2 804G 249G used 555G avail 31%`; nothing
citable lives outside this wave directory and the lane tree.

VERDICT: report-out list drafted for both variants the attribution admits, because the artifact
oscillated 75 → 71 → 75 rows inside this seat's window. **Variant B (75 rows, the last state read,
sha256 `cc5acda1…`):** four handovers, one line each, each grounded in a ledger row id and a quoted
connector-map line — `kama` ← `R51-R1` (LFM3 identity pin; health/flag authority handed over, pointer
cites the wrong PROVINCE row), `kama` ← `R51-R4` (qwen-coder unit retirement, pointer correct),
`protocol` ← `R51-R2` (fleet routed-finding ledger schema), `unowned:integrator` ← `R51-R3`
(restore-or-retire three absent source trees). **Variant A (71 rows):** no sibling owner is named, so
the list is **empty** and the round's adjacency move rides on 71 in-lane attributions plus the
connector maps' class rulings — the L1 must say that in the round notes, because `routed 0` otherwise
reads as "nothing reported out". Eight further sibling lanes are named by the maps with zero rows
(aggregator is a live three-way disagreement), and seven rostered lanes are unrouteable under the
frozen counter. Three candidate pointers do not resolve at the committed tip, one connector map's own
line pin is off by one, and the integration tool no longer reproduces the artifact it wrote — all
reported, none fixed, no sibling scope absorbed.
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
