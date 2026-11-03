# SiblingOverlap — round 68 attempt 2, w2 (cross-lane overlap scan)

Seat: SiblingOverlap (leaf; read-only everywhere). Date: 2026-11-03.

Scan base: lane `kengaku-shokunin` tip `7803bdd4` (`== origin/master` at scan time; `0e52fb5d` is its
parent). Every sibling lane was read, none was written; no git/jj write command was run anywhere; the
fleet repo's tracked state (`MANIFEST.json`, `.ufo/`, `.ufo/state/`) was read only.

Writes made by this seat, and no others: this report, plus files under
`/fast/scratch/hyaku/kengaku-r68/SiblingOverlap/` (deleted before yield).

---

## 1. Search commands (reproducible; each search capped)

**A — assigned term scans over the eleven named sibling lanes** (`--include=*.md --include=*.py`,
`.git` excluded, `head -30` cap per term):

```bash
cd /home/vgpnk/Projects/shokunin
for t in 'pypi-server' 'network-service' 'urllib3' 'report-contract' 'sources-census'; do
  echo "=== $t ==="
  grep -rl --exclude-dir=.git --include='*.md' --include='*.py' -F "$t" \
    kake-shokunin kama-shokunin chousa-shokunin mori-shokunin tameshi-shokunin kaidoku-shokunin \
    tsukuroi-shokunin souji-shokunin tabi-shokunin kumitate-shokunin kotoba-shokunin 2>/dev/null | head -30
done
grep -rl --exclude-dir=.git --include='*.md' --include='*.py' -F '## SHONEN' <same eleven lanes> | head -40
# per-lane counts for the table
for d in <same eleven lanes>; do
  grep -r --exclude-dir=.git --include='*.md' --include='*.py' -F -c "<term>" "$d" \
    | awk -F: '{s+=$2} END{print s+0}'
done
```

**B — fleet-wide executable scan** (the decisive one: are any of these terms *implemented* elsewhere?):

```bash
grep -rn --exclude-dir=.git --include='*.py' -F 'SHONEN' .            # all lanes
grep -rn --exclude-dir=.git --include='*.py' -F 'report-contract' .
grep -rn --exclude-dir=.git --include='*.py' -F -- '--shonen' .
find . -name 'sources-census*' -not -path '*/.git/*'
find . \( -name 'sources-census.sh' -o -name 'sources-census.py' \) -not -path '*/.git/*'
```

**C — authoritative-definition reads** (where the shared contract actually lives):

```bash
sed -n '180,225p' scripts/shokunin-watchdog.sh          # report_of(), MIN_REPORT_BYTES
sed -n '99,129p'  templates/round-prompt.md             # §4 Report contract
sed -n '360,400p' scripts/hyaku/lane-addendum.md        # pre-report gate + report extras
head -25 scripts/sources-census.sh                      # contract-v1 census modes/codes
sed -n '1,20p'   kagi-shokunin/corpus/sources-census.sh # the sibling implementation's own header
```

**D — the measurements quoted below** (read-only; results in §3/§4):

```bash
bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
bash <scratch>/sources-census.kagi.sh verify --root /home/vgpnk/Projects/shokunin/kengaku-shokunin
python3 -B souji-shokunin/tools/souji-report-contract.py --report <fixture> --shonen kengaku-shokunin/SHONEN.md
git -C kengaku-shokunin show 7803bdd4:plans/round68_report_contract.py > <scratch>/g.py   # sha 18fbfc21…
python3 <scratch>/g.py --selftest --lane kengaku-shokunin --work <scratch>/a2work

# heading census over filed reports (fleet repo), all six of A2's section names + token scans
for r in 64 65 66 67 68; do
  for f in .ufo/reports/round-$r/*.md; do
    n=0
    for h in '## Work performed' '## Landed changes' '## Before → after measurements' \
             '## Sources & frontier' '## Trend verdicts' '## SHONEN'; do
      grep -qxF "$h" "$f" && n=$((n+1))
    done
    printf '%s %s/6 shonen=%s stale=%s\n' "$f" "$n" \
      "$(grep -cE '^## SHONEN' "$f")" "$(grep -c -F 'Stale-lane' "$f")"
  done
done
```

---

## 2. Hit table

Counts are file-hit counts over `*.md` + `*.py` (wave specs included — that is where most of the bulk
lives). Class: **term-level** = same word, different surface; **surface-level** = the same artifact or
the same gate.

| term | lanes with hits (count) | class | routed? |
|---|---|---|---|
| `pypi-server` | tabi (2) | **term-level** — both hits are one line, `tabi-shokunin/.ufo/waves/round-57/scout/scout.md:388` and `…/w1/R57Scout.md:388`, quoting kengaku's own round-63 commit subject (`6b0908a5 round-63: R63-C1 pypi-server offline replay …`) inside a lane-history scan. No artifact, no checker, no grader copy. | no (cited, not contested) |
| `vectorops` (grader stub package) | none outside kengaku (0 hits fleet-wide) | — | no |
| `network-service` (TB2 class name) | none in the eleven; fleet-wide only kengaku's own reports (`round-62/63/64/68/kengaku.md`) | — | no |
| `urllib3` | kama (3), tsukuroi (1) | **term-level, with a version near-miss** — kama `round-20/build/advice/GgufOracle.md:15` records `uv` resolving `urllib3 2.8.0`; tsukuroi `round-24/w1/ExecPacmanLogCensus/table.md:234` records the host package upgrade `python-urllib3 (2.7.0-1 -> 2.8.0-1)` (2026-10-20). Neither is pip's vendored copy that S240 names. | routed (O4) |
| `report-contract` | souji (629), tabi (290), kaidoku (16), tameshi (13), kotoba (6), mori (5), kake (2), tsukuroi (2), kumitate (3), kama (1), chousa (1) | **surface-level** at souji (`tools/souji-report-contract.py`, a committed executable gate); **term-level** everywhere else (wave specs, seat reports, one scratch-only checker in mado). | routed (O1) |
| `## SHONEN` heading gates | kake (189), kumitate (543), souji (372), kotoba (337), tabi (194), kaidoku (141), chousa (120), mori (112), tameshi (105), kama (158), tsukuroi (69) | **surface-level**: the heading is a fleet-wide report contract defined in `templates/round-prompt.md` §4 and enforced by `scripts/shokunin-watchdog.sh:report_of`; kengaku's A2 gate restates it. souji's committed gate also checks it. | routed (O1, O5) |
| `sources-census` | kake (1114), kama (1209), chousa (779), mori (821), tameshi (1280), kaidoku (841), tsukuroi (720), souji (1654), tabi (901), kumitate (1248), kotoba (780) | **surface-level** at kagi (`corpus/sources-census.sh`, a second validator of the same contract — not in the named eleven but reachable from the same term); **term-level** elsewhere (invocations of the one fleet script, plus wave receipts). | routed (O2) |

No `agent://` message, no swarm, no subagent was used. No file outside this report and my scratch was
created, modified or deleted.

---

## 3. O1 — `report-contract` is implemented twice, and the fleet contract has four authorities that do not agree

### The authorities (all read this session)

| # | artifact | what it enforces |
|---|---|---|
| A | `scripts/shokunin-watchdog.sh:187-211` (`report_of`, the driver's content check) | report exists; round-baseline digest differs; a heading matching `^#+[[:space:]]*SHONEN…` **or** a bold list marker `- **SHONEN**` (case-insensitive, either macron byte); `wc -c ≥ MIN_REPORT_BYTES` (**400**, `:54`; not overridden in `shokunin.conf`). Nothing else. |
| B | `templates/round-prompt.md:99-125` (§4 "Report contract") | six sections **in order**, `SHONEN` last. Marker rule at `:121-125`: a contentless report counts as failed — and it explicitly **exempts** "missing required sections other than **Sources & frontier** and **Trend verdicts**". |
| C | `scripts/hyaku/lane-addendum.md:376-379, 387-388` | pre-report `grep -c '^## SHONEN'` must print 1 **and** be followed by one `[~]`/`[ ]` line per `SHONEN.md` box; report extras are "the canonical **Trend verdicts** section; a `Stale-lane` line". Records the recurrence: kake r52 left every round commit off-branch; kotoba r69 and r71 both filed without the SHONEN heading. |
| D | `souji-shokunin/tools/souji-report-contract.py` (sha256 `a19c405a4454670415822f623c0dbac3d641991633b5495f4a62481f1f250ad5`, landed `1e771ed5` 2026-10-28, registry row `SKILL.md:257`, scorecard `SCORECARD.md:563,575`) | 7 predicates: `sections` (six canonical headings, #6 = **stale-lane**), `shonen-boxes` (count of `- [x~ ]` lines equals the box count), `trends`, `stale-lane` (non-empty line/heading), `measurements` (≥1 row with a 7–64-hex commit **and** a counting command), `claims` (1–3 `C1..C3` ids in Work performed), `evidence` (repo-relative pointer or 40+ hex). `check-<name>=PASS\|FAIL` lines, exit 1 on any FAIL. |
| E | `kengaku-shokunin/plans/round68_report_contract.py` (committed blob at `7803bdd4` = sha256 `18fbfc2111d747ae9f40220333f0bbd56062c89e93bcd7c2477358228a0723f4`; `git show 7803bdd4:plans/round68_report_contract.py` reproduces this sha and the table below) | 6 predicates S1–S6: S1 six headings, `## SHONEN` last, exact `## ` text, each exactly once, ordered; S2 box lines matched by the box's first five normalized words, count equal; S3 `expansion:/quality:/discernment:` + verdict token inside `## Trend verdicts`; S4 ≥2 table rows in Before → after, each with a backticked token or 7+ hex; S5 the gate's `PLACEHOLDERS` token scan (three fixed acronyms, a lorem-ipsum phrase, an angle-bracket placeholder, matched case-insensitively); S6 ≥400 B and ≥3 `##` headings. |

B and E agree on the six-section list and on `SHONEN` last — E is a faithful executable copy of B's
section list. The disagreements are elsewhere.

**Provenance note (mid-scan working-tree change, recorded not absorbed).** When this scan opened, the
lane tree was clean at `7803bdd4`. While it ran, another seat left uncommitted edits in
`plans/round68_report_contract.py` and `plans/round68_capability_table.py`; the gate's working copy is
now sha256 `dbd3f373…` against the committed blob's `18fbfc21…`. The diff touches only `selftest()`
and adds one `_mutate()` helper above it — lines 1–161 (`check()`, all S1–S6 logic, `box_keys`,
`section`, `skeleton`) are byte-identical to `git show 7803bdd4:…` — and the new selftest raises the
fixture set to 10 with per-counter `expected` defect sets. So the matrix below describes both the
committed and the working bytes, but every A2 number quoted in this report was measured from the
**committed blob** (extracted with `git show 7803bdd4:plans/round68_report_contract.py`, sha
`18fbfc21…`), not from the moving working copy. This is precisely the class the round's own sha
binding exists to catch.

### Divergence matrix (read from the committed code, not from prose)

| property | A (driver) | B (template) | C (addendum) | D (souji) | E (kengaku A2) |
|---|---|---|---|---|---|
| SHONEN heading | any level `#+`, case-insensitive, or bold marker | required section | `grep -c '^## SHONEN' = 1` | `## SHONEN` body counted | exact `## SHONEN`, once, last |
| one line per box | — | yes (`:118-120`) | yes | yes (count only) | yes (count **and** 5-word prefix match) |
| Trend verdicts | — | required, but **not** a marker predicate | required ("canonical") | 3 trends, verdict token | 3 trends, regex `trend: verdict` |
| Stale-lane | — | — | required line | required (6th heading, non-empty body) | **absent** |
| placeholders | — | marker rule ("placeholder text") | — | — | S5 |
| byte floor | 400 | — | — | — | 400 (S6) |
| digest delta | required | — | — | — | — |
| source-census | applied separately | — | — | — | — |

**Measured non-equivalence on one input.** The A2 `--selftest` green fixture built by the **committed**
gate blob (sha256 `e212c9f35d88adf35c3f50a55e469eeeb3ff486f9200a82ae4010ee9f89fc7c0`;
`SELFTEST n=5 red-refused=4 green-ok=1`, rc 0) was fed to D unchanged:

```
check-sections=FAIL   detail-sections: stale-lane headings=0 expected 1
check-shonen-boxes=PASS   check-trends=PASS
check-stale-lane=FAIL detail-stale-lane: no stale-lane line
check-measurements=PASS   check-claims=PASS   check-evidence=PASS
SUMMARY checks=7 pass=5 fail=2      exit=1
```

So a report that E certifies green is refused by D. The same attempt-1 report fixture is refused by
both (D `pass=2 fail=5`, E `S1,S2,S3`), i.e. the two gates agree only on the grossly deficient input.
Neither subsumes the other: D has `stale-lane`, `claims`, `evidence`, fence/comment masking
(`mask()`) that E lacks; E has S5 placeholders, the two-row/two-pointer rule and strict box-prefix
matching that D lacks. Joint compliance is possible only for a report that carries all six of E's
headings plus a `Stale-lane` heading after them, ≥2 pointed rows and no placeholders.

### Where the fleet's own reports actually stand (measured on the fleet repo, `.ufo/reports/`)

Round 68, all 13 filed reports (`grep -qxF` per heading, token scan for `Stale-lane`):

- **all six headings:** 7 of 13 — chousa, kake, kotoba, kumitate, mori, revenger, tsukuroi.
- **partial:** kotodama 5/6, tameshi 5/6, audio 4/6, game-dev-2d 4/6, kengaku 4/6, kama 3/6.
- **`## SHONEN` present:** 11 of 13 — the two that lack it are **kengaku's and tameshi's**, i.e. exactly
  the defect class that relaunched kengaku as attempt 2 (`.ufo/watchdog.log:2132`). The miss is not a
  kengaku-only anomaly this round.
- **`Stale-lane` token present:** 6 of 13 — chousa, kotoba, kotodama, kumitate, revenger, tsukuroi.

Recent rounds, same measurement:

| round | reports | all six | `Stale-lane` token |
|---|---|---|---|
| 64 | 15 | 12 | 10 |
| 65 | 14 | 11 | 9 |
| 66 | 13 | 8 | 6 |
| 67 | 13 | 10 | 5 |
| 68 | 13 | 7 | 6 |

So kengaku's A2 S1 would reject **6 of 13** round-68 fleet reports, and souji's D would reject at
least the **7** that carry no `Stale-lane` token (and more, since D also requires the heading form,
1–3 claim ids in Work performed and a commit-plus-command row). Also measured:
`## Before → after measurements` is the arrow form in **876** fleet reports and `->` in **1** — D
normalizes both (`normalize_heading`), E requires the arrow byte-for-byte — and every lane's
`SHONEN.md` carries exactly **4** box lines (21 lanes), kengaku's being 459 B.

A cross-run of D and E over all 13 round-68 reports is **not** reported here as a divergence measure:
E's S2 matches the report's box lines against the *lane's own* `SHONEN.md` box text, so running E with
kengaku's box list scores every other lane's report on the wrong checklist (all 13 fail E, and the
defect that dominates is S2). The valid single-input comparison is the one above: E's own green
fixture, scored by D.

### Classification and routing

**Surface-level** — same artifact (the fleet round report and the SHONEN box set), two committed
executables (D, E) plus two prose/predicate authorities (A, B/C) that disagree with each other on
which sections are marker-level. Contested because: E's S1 treats `## Sources & frontier` and
`## Trend verdicts` as hard defects, while B's marker rule says a report missing exactly those two is
`ok` plus a conformance note; A does not look at either. And E is silent on the `Stale-lane` extra
that C requires and D enforces, so an E-green report can still be non-conformant under C.

**Route to the L1 for the round-68 report; do not absorb, do not edit.** The report should name D as
prior art (souji r36 built the same gate one round after its own r35 spot-check routed report
defects — the same defect class that produced kengaku's A2), state E's own scope as *lane-local
pre-flight for this lane's report*, and carry the two deltas (S1 vs the marker rule; no Stale-lane
predicate) as named limits. This is exactly the routing form the seat spec requires: the L1 decides,
and neither lane's bytes change.

---

## 4. O2 — `sources-census`: two validators for `SOURCES-CONTRACT-v1`, measured on the same file

| artifact | path | sha256 | size | role |
|---|---|---|---|---|
| fleet census (canonical) | `scripts/sources-census.sh` | `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30` | 806 lines | modes `census/validate/overdue/shared/selftest`; TSV `E01–E12` + `W01–W04`; includes `E11 used-by path missing on disk` |
| sibling implementation | `kagi-shokunin/corpus/sources-census.sh` | `8d30d627021cd70947bfec6a3984418ff1e7f1a8a16d8b5ab580a56898a0968a` | 675 lines | kagi r21 C3; embeds the contract's seven §Census one-liners verbatim and adds cross-file checks; `FINDING SC_*` vocabulary (15 ids); no reference to the fleet script, and the fleet script does not reference it |
| wave fixture copy | `kaidoku-shokunin/.ufo/waves/round-50/w1/ConnCrossClaim/census-fixtures/sources-census.sh` | `3fb72615…` (byte-identical to fleet) | — | proof the fleet copy is the instrument lanes copy for fixtures |

Independent corroboration that the fleet script is the reference: kake's `round-27/w1/SourceCensus.md:9`
pins the same sha256 before running it (`:12`, `:19`, `:32`).

**Measured on kengaku's own registry** (`corpus/SOURCES.md`, 232 rows, S240 appended):

```
bash scripts/sources-census.sh validate --root …/shokunin kengaku
  → exit 0 · 24 × W04 · final line "kengaku ok …/kengaku-shokunin/corpus/SOURCES.md"

bash <kagi copy> verify --root …/kengaku-shokunin
  → exit 1 · 443 findings · "SOURCES_CENSUS: FAILED (findings=443 rows=232)"
    SC_FETCH 232 · SC_USEDBY_NOCITE 163 · SC_ENTRY_HEADER 25 · SC_USEDBY_MISSING 19
    SC_REJECT_SHAPE 2 · SC_ENTRY_CITE 2
    SC_DUP 0 · SC_ENUM 0 · SC_SECTIONS 0 · SC_MALFORMED 0 · SC_INFLATION 0
```

Reading of the contradiction, stated rather than smoothed: **the two instruments agree on every
contract-level predicate** (0 duplicates, 0 enum violations, 0 missing/foreign sections, 0 malformed
rows under the sibling's own codes) and **disagree only on kagi-local extensions** — a
`corpus/source-fetches.tsv` provenance ledger (232 rows lack it), used-by citation reciprocity
(163), an entry-file `source:` header shape (25), a `corpus/`-prefix rule for used-by paths (19 — I
checked all 8 distinct paths named: every one **exists** on disk as `corpus/evidence/…` or
`plans/…`; the sibling flags them for not being `corpus/`-prefixed, not for dangling), and
rejected-row shape (2). So kengaku has **no contract-level census defect**; what it has is a registry
that would fail if the fleet ever adopted kagi's provenance ledger.

**Classification:** surface-level at the instrument (two validators, one contract, disjoint code
vocabularies, no cross-reference), term-level for the other ten lanes (they invoke the one fleet
script).

**Route to the L1:** kengaku's F3 duty ("same command → exit 0 required") is scored by the fleet
instrument only, which is contract-level. The report should say so explicitly (it already cites the
command, not the sibling), and should note the forward risk: a fleet-wide provenance ledger would
require backfilling 232 rows in this lane — a future round's work, not this one's. Do not port kagi's
checks into the lane now; do not edit either script.

---

## 5. O3 — `R68-C1`/`R68-C2` collide across lanes inside round 68

Two fleet reports for round 68, filed in the same window, use the same unqualified claim ids for
different claims:

| file | line | id | axis | claim |
|---|---|---|---|---|
| `.ufo/reports/round-68/kengaku.md` | 8 | R68-C1 | **coverage** | TB2 `pypi-server` offline replay (the round-62/63 grader capability) |
| `.ufo/reports/round-68/kengaku.md` | 9 | R68-C2 | **calibration** | round-67 routed defects as dated corrections |
| `.ufo/reports/round-68/tameshi.md` | 40 | R68-C1 | **calibration** | figure-attribution instrument (capability acquisition) |
| `.ufo/reports/round-68/tameshi.md` | 59 | R68-C2 | **operability** | arm-liveness per-row scratch slot + 6th standing row |

The axis of C1 is *inverted* between the two lanes: kengaku's C2 and tameshi's C1 are both
"calibration". The collision is already in the fleet's own state: `MANIFEST.json`
`.rounds[1051].notes` (tameshi, round 68 closure) carries an unqualified `R68-C1` that means
**tameshi's** claim — "the R68-C1 capability-row command printed as grep -c 'figure-attribution
check' reads 4 at tip, not the reported 1". A fleet-wide `grep R68-C1` returns two lanes' distinct
claims plus the manifest note; a reader cannot tell which is meant without the path.

**Classification:** term-level (same token, different surface) but with a **routing consequence**:
the token is a cross-lane identifier, and the fleet has no lane qualifier in its filed reports.

**Route to the L1:** the round-68 fleet report should cite this lane's claims lane-qualified
(`kengaku R68-C1`) and name the collision as a fleet-level naming hazard (tameshi's own filed
lesson `tameshi-shokunin/corpus/lessons/round-68-verifier-spotcheck.md:26,52` uses the same ids for
its claims). No edit to either report, to tameshi's lesson, or to `MANIFEST.json`; a fleet-wide
`<lane>:R<n>-C<m>` convention is the L1's call, not this seat's.

---

## 6. O4 — `urllib3`: S240's pin is a *vendored* copy; the sibling evidence is the host package at 2.8.0

S240 (`corpus/SOURCES.md:255`) names urllib3 `src/urllib3/connection.py` at tag `2.7.0` and scopes it
to "the endpoint rendering **pip 26.2.1** embeds in connection-refused stderr". The sibling records
that mention urllib3 name a *different copy* of the package — both at 2.8.0 — and neither is the copy
S240 binds:

- `tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecPacmanLogCensus/table.md:234` — the host package was
  upgraded `python-urllib3 (2.7.0-1 -> 2.8.0-1)` on 2026-10-20 (so the installed distribution is
  2.8.0-1).
- `kama-shokunin/.ufo/waves/round-20/build/advice/GgufOracle.md:15` — a `uv`-provisioned venv
  resolved `urllib3 2.8.0`.
- The host `python3` has no `pip` at all (`python3 -m pip --version` → `No module named pip`), so the
  only pip in play is the probe's own venv (round-63 machinery `ensure_venv`), and its vendored
  `urllib3/connection.py` is what S240's sha256 binds.

**Classification:** term-level (same package name, different copies: pip-vendored vs host
distribution vs an unrelated venv). **Routed as an observation**, because the row's scope column
already says "pip 26.2.1": the risk is a reader substituting the host/venv 2.8.0 for the vendored
2.7.0 (the amendment A1 text's "byte-identical to upstream urllib3 2.7.0" is the right sentence, and
it is easy to misread as a statement about the host). The round-68 fleet report's Sources & frontier
bullet should keep the `pip 26.2.1`/vendored qualifier adjacent to the tag. No edit.

---

## 7. O5 — the `## SHONEN` heading gate: what kengaku's A2 does and does not cover

The heading is a fleet-wide contract, not a kengaku invention: all 21 lane `SHONEN.md` files carry
exactly 4 boxes; `templates/round-prompt.md:118-120` defines the per-box line rule; the driver's
`report_of` is the completion predicate; `scripts/hyaku/lane-addendum.md:378-379` is the pre-report
gate; `souji-shokunin/tools/souji-report-contract.py` is the only sibling *committed* checker of the
report's SHONEN section. Other SHONEN readers are different surfaces and stay term-level:

- `chousa-shokunin/tools/lane-preflight.py` (committed, `b2043bf9` 2026-11-01) — G04
  `shonen-pointers`: every path-shaped word in a `SHONEN.md` backtick span must exist under ROOT.
  Validates the **checklist file**, not the report section.
- `audio-shokunin/reports/round-1-calibration/count_checklist.py` — box counters over a historical
  revision of `SHONEN.md`; a round artifact.
- `kagi-shokunin/corpus/claim-ledger.sh:649,657,766` — treats `SHONEN.md` as a root doc in a
  lockstep membership set.
- `mado-shokunin/.ufo/waves/round-35/scratch-evidence/RevReportShape/check-report-shape.py` — a
  wave-scratch checker (uncommitted, one round only) that cites `report_of` + prompt §4 +
  addendum:196; it is the closest prior art to E but never landed as tooling.
- `mori-shokunin/tools/mori-round13-regressions.py --shonen` — a promotion-seed comparison input,
  different surface.

**Routing consequence for the L1:** E's S6 byte floor (400) is exactly A's `MIN_REPORT_BYTES`
default, but A also requires the digest-delta and accepts the bold-marker form; C requires one box
line per box *and* the two extras; D requires the box count and the stale-lane heading. The report
should list this four-way split as the reason the gate exists, not claim E subsumes the driver. No
edit; the frozen A2 predicate is unchanged.

---

## 8. O6 — the surfaces with no contest (recorded, so the absence is evidence)

- `pypi-server`, `vectorops`, `network-service` — no sibling copies the grader, the stub package, the
  PEP 503 index builder, or the TB2 class table. The only sibling mention is tabi's one-line quote of
  kengaku's commit subject (§2). R68-C1's artifacts are uncontested.
- No sibling lane references `round68_report_contract` or `R68-C1/R68-C2` in an executable or a
  lesson outside the collision in O3 (fleet-wide `grep -E 'R68-C1|R68-C2|round68_report_contract'`
  outside `kengaku-shokunin` → `MANIFEST.json`, `tameshi-shokunin/SCORECARD.md`,
  `tameshi-shokunin/corpus/lessons/round-68-verifier-spotcheck.md`, and one `.jj` object).

---

## 9. Proposed move (one, bounded — for the L1, not executed here)

In the round-68 fleet report's Sources & frontier and Trend verdicts sections, cite this lane's
claims **lane-qualified** (`kengaku R68-C1`, `kengaku R68-C2`) and add one cross-lane-overlap bullet
naming the three findings that change how a reader prices this round:

1. the A2 gate is a **second** implementation of a contract souji already gates
   (`tools/souji-report-contract.py`, `a19c405a…`, r36) and it does not subsume that gate (measured:
   an A2-green report fails souji 2/7);
2. the A2 gate is **stricter than the driver's marker rule** on `## Sources & frontier` and
   `## Trend verdicts`, and **silent** on the addendum's `Stale-lane` extra — so "A2 pass" must not be
   written as "report contract satisfied";
3. `R68-C1`/`R68-C2` are **not unique** in round 68 (tameshi's filed report and `MANIFEST.json`
   `rounds[1051].notes` use the same ids for different claims).

Affected axes: **coverage** (unchanged — no claim artifact moves, the probe/receipt are untouched) and
**calibration** (improved at the margin: the round's own mistake class is now named at fleet scope
instead of being absorbed as a lane-local checker). No counter, predicate, vector, case, kill rule or
target is touched, and nothing is written outside this seat's allowed paths.

## 10. Risks

- **Over-reading the census measurement.** The 443 sibling findings are *extensions*, not contract
  violations; calling them defects in kengaku would be false. The report must carry the split
  (0 contract-level / 443 extension-level) or omit the number.
- **Gate scope creep.** Naming D as prior art is not a proposal to replace E, and E's frozen
  predicate is not amendable by this seat. Any adoption decision (share one gate, or keep per-lane
  pre-flights) is the L1's.
- **Namespace "fix" temptation.** Renaming or requalifying claim ids after the fact would edit frozen
  documents on two lanes; the finding is a naming hazard only, and the claims themselves are
  unaffected.
- **urllib3 version substitution.** Treating the host distribution (2.8.0-1) or a venv resolution
  (2.8.0) as the S240 pin would silently change the clause's mechanism; the qualifier must stay
  attached to the tag.
- **Wave-directory drift.** `kagi-shokunin/corpus/sources-census.sh` is a *committed* lane artifact
  (r23/r24), not a wave leftover — a reader who assumes `corpus/tools`-style local gates are
  ephemeral would misclassify it.

## 11. Verification

Every number above is re-derivable with the commands in §1:

- `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → exit 0,
  24 × W04, `kengaku ok …` (baseline also committed at
  `kengaku-shokunin/.ufo/waves/round-68/census-before.txt`).
- `bash <kagi copy> verify --root …/kengaku-shokunin` → exit 1, 443 findings, the breakdown in §4;
  the copy taken was byte-identical to the kagi source (copied, not edited).
- `git -C kengaku-shokunin show 7803bdd4:plans/round68_report_contract.py > <scratch>/g.py &&
  python3 <scratch>/g.py --selftest --lane <lane> --work <scratch>` → rc 0,
  `SELFTEST n=5 red-refused=4 green-ok=1`, exactly as Amendment A2 item 3 declares; per-fixture
  defects `r1 S1,S2,S3 · r2 S2 · r3 S3 · r4 S5 · r5 pass`. Run from the committed blob (sha
  `18fbfc21…`), not from the working copy that another seat edited mid-scan.
- `python3 -B tools/souji-report-contract.py --report <A2 green fixture> --shonen <kengaku SHONEN.md>`
  → exit 1, `SUMMARY checks=7 pass=5 fail=2`.
- sha256s quoted: `a19c405a…` (souji gate), `18fbfc21…` (kengaku gate), `3fb72615…` (fleet census),
  `8d30d627…` (kagi census) — re-runnable with `sha256sum` on the committed paths.

## 12. Limits / what this seat did not do

- No predicate, counter, case table, kill rule, target, registry row, claim doc or sibling file was
  edited; no git/jj write, commit, push, stage, stash, checkout or switch was run anywhere.
- No live network fetch: all authorities are local committed bytes or the fleet's own runtime scripts.
- The sibling census run is a read-only diagnostic of *kengaku's* file; it is not kengaku's census
  verdict and not a claim that kagi's rule set is correct.
- The heading census is taken on the **fleet repo's** `.ufo/reports/` for round 68 (all 13 reports)
  and the rounds 64–68 aggregate, under the section names this lane's A2 gate uses; it is a census of
  those reports, not of every historical report, and it does not judge whether another lane's older
  axis wording ("Per-axis and learning outcomes") is non-conformant.
- The lane working tree changed under this seat mid-scan (another seat's uncommitted edits to
  `plans/round68_report_contract.py` and `plans/round68_capability_table.py`, both named in §3). I
  read and measured the **committed** bytes (`7803bdd4`) and did not touch, revert or judge the
  uncommitted work; this report attributes nothing to the working copy.
- No `agent://all` message, no swarm, no subagent.

## 13. Tooling record

No tool was installed, upgraded or removed this seat (nothing was needed: `grep`, `find`, `awk`,
`sha256sum`, `python3` 3.14.8, `bash`). No pacman transaction was attempted.

## 14. Scratch

Scratch root `/fast/scratch/hyaku/kengaku-r68/SiblingOverlap/` (census outputs, the kagi-census copy,
the A2 selftest fixtures) was deleted before yield; the receipts quoted above are in this report.
