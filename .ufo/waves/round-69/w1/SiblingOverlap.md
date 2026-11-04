# SiblingOverlap — cross-lane overlap scan, kengaku round 69 w1

**Seat:** SiblingOverlap (connector, leaf). **Scope:** the round's declared ground — `nginx-request-logging`,
`7788`/`8080`, `PEP 503`, `network-service`, `/etc/hosts` staging, `routed defect` gates — against every sibling
lane tree and the fleet report surface. **Mode:** read-only. No sibling file was edited; no gate, battery,
test or formatter was run anywhere; no git or jj write was issued.

**Measured lane state:** `git -C . rev-parse --short HEAD` → `b288e8e0` at scan start. `git -C . status
--porcelain` was read twice. At 21:0x it showed only `?? .ufo/waves/round-69/w1.ready`,
`?? .ufo/waves/round-69/w1.ready.dispatched`, `?? .ufo/waves/round-69/w1/` (the wave's own untracked
outputs; no tracked path dirty). By 21:12, after this seat's reads, it also showed ` M SKILL.md`,
` M corpus/QUALITY.md`, ` M corpus/knowledge/tb2-network-service-offline-grader.md`,
` M corpus/lessons/round-68.md`, `?? corpus/evidence/round69/`. Those four modified paths are exactly R69-C1's
class row / S241 row and R69-C2's E2/E4/E5/E6 surfaces — **sibling seats' in-flight landings, not this seat's**.
This seat wrote only this report and issued no git write.

**Counts: `TERM-LEVEL 18`, `SURFACE-LEVEL 2`.** Unit of count is a distinct *(lane, surface-element)*
classification, not a file. Two surface-level hits, both **routed**, neither contested.

---

## 1. Classification rule used (borrowed, cited, and flagged provisional)

The fleet has exactly one committed, adjudicated rule for this job: kotoba's sibling-overlap census.

- `kotoba-shokunin/corpus/knowledge/sibling-overlap-census-round49.md:45-53` — `contested` = the sibling's
  committed scope surfaces claim part of the lane's core; `adjacent` = either side's scope surfaces state a
  split of one artifact/function/trigger area; `none` = neither.
- Same file `:54-55` — **"Wave reports and run logs (`.ufo/`, `reports/`) are not scope surfaces: a split
  stated only there does not make a row `adjacent`."**
- Same file `:253-265` — precedence: a claim makes the row `contested` unless the sibling's own scope surfaces
  state a split; **a split stated only by the claimant never overrides a sibling's claim**.
- Same file `:416-421` — the rule is **provisional**: the operator question (fleet `.ufo/l0-questions.md:105`)
  carries no answer. I use it as the least-arbitrary available standard and label it as such.

I apply it in the assigned two-level vocabulary:

- **term-level** — same token, different surface element (a response header, a package name, a file path, a
  quoted source). No ownership question arises.
- **surface-level** — another lane already owns or has executed *this exact surface*. Sub-classified
  **routed** (the sibling's own committed text assigns it elsewhere or keeps its own gate) vs **contested**
  (both lanes' scope surfaces claim the same element).

Consequence of `:54-55` that I hold to throughout: sibling `.ufo/waves/` and fleet `.ufo/reports/` hits are
**evidence of what a lane did**, never a scope claim. They are counted as term-level unless the same element
also appears in that lane's `corpus/`, `SKILL.md` or `PROVINCE.md`.

---

## 2. Headline negatives (the coverage that decides the round)

These are the results that make the round's ground uncontested, and each carries its raw line.

| Question | Raw output | Reading |
|---|---|---|
| Does any sibling carry the TB2 grader corpus? | per-lane matrix below: `graders52=Y` for `kengaku-shokunin` only, `-` for all 20 others | the grader bytes are kengaku-only |
| `nginx-request-logging` in a sibling? | per-lane `grep -rl -F` over every lane → **`kengaku-shokunin` 127 files, `tabi-shokunin` 7 files, every other lane 0**. tabi's 7 are 4 committed `corpus/` files (3 censuses + the r57 lesson) quoting kengaku's own line, plus 3 wave-dir copies of the same row (§3 S1) | one sibling *cites* the term and assigns it to kengaku; none claims it |
| `network-service` in a sibling scope surface? | `grep -rln -F 'network-service' */corpus */SKILL.md */PROVINCE.md` → 17 files, **all under `kengaku-shokunin/`** (`corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, 4 `corpus/knowledge/*`, 6 `corpus/lessons/*`, `SKILL.md`, `PROVINCE.md`) | zero sibling scope claims on the class |
| nginx **configuration** vocabulary in a sibling? | `grep -rlnE 'nginx\.conf\|server_name\|error_log\|limit_req'` fleet-wide minus kengaku → **0** real hits; the single file is `audio-shokunin/corpus/fixtures/measure_audio.py:1236,2462,3157,3179,42530`, where `server_name` is the PipeWire/ALSA `Server Name:` field | K3 (`access_log` creation/format) and K4 (`limit_req_zone`) rest on grader bytes alone |
| `access_log` anywhere outside kengaku? | `grep` fleet-wide minus kengaku → **no matches** | same |
| `limit_req_zone` anywhere outside kengaku? | `grep` fleet-wide minus kengaku → **no matches** | same |
| `PEP 503` outside kengaku? | 2 files, both vendored: `kagi-shokunin/.ufo/waves/round-28/retained-probes/SrcNodeSemver/node_modules/node-gyp/gyp/pylib/packaging/{markers,utils}.py` | term-level; no lane-built index surface |
| `7788` as a port? | `grep -rE '(:|port[ =]\|port=)7788\b'` fleet-wide → 0 port tokens; every hit is a hash/nonce substring (kaidoku `after.json` evidence ids, mado nonce `778899`, a kotodama URL id) | no `7788` surface exists |
| Who holds `127.0.0.1:8080` now? | `ss -ltnp '( sport = :8080 )'` → header row only, **no listener** | port free at scan time |
| Is the 8080 lock in place? | `ls -la /home/vgpnk/.local/share/kengaku-r69/` → `-rw-r--r-- 1 vgpnk vgpnk 0 Nov  3 21:06 port-8080.lock` | kengaku-local lock file present, 0 B |
| Does any sibling *bind* 8080? | kama `corpus/lessons/round-1-critic.md:110` ("No nginx, caddy, or SSH forwarding process was found"), kagi `claim-ledger.sh` and fleet `AGGREGATE.md:318-321,934-937` use it GET-only; the host's 8080 is the Jitsi videobridge | no sibling binds it → no contested bind |
| Does any sibling stage a lane-written `/etc/hosts`? | kake's 12 hits are fetched RFC/source text (`.ufo/waves/*/sources/rfc3986.txt`, `S089.txt`, `S008-1.txt`); kaidoku's are **fixture content** inside firmware carriers (`kaidoku-shokunin/tools/round-40/mk-l-carriers.py:53`, `tools/round-41/mk-l-carriers.py:88` → `'etc/hosts': b'127.0.0.1 localhost\n'`); no lane writes a sandbox `/etc/hosts` | the R69-C1 staging technique has no sibling precedent and no sibling owner |

**Per-lane surface matrix** (raw, the command's own output):

```
audio-shokunin         graders52=-  ev69=-  plans=0    evdirs=0
chousa-shokunin        graders52=-  ev69=Y  plans=0    evdirs=194
game-dev-2d-shokunin   graders52=-  ev69=-  plans=0    evdirs=0
game-dev-3d-shokunin   graders52=-  ev69=-  plans=0    evdirs=0
kagi-shokunin          graders52=-  ev69=-  plans=14   evdirs=0
kaidoku-shokunin       graders52=-  ev69=-  plans=32   evdirs=22
kake-shokunin          graders52=-  ev69=-  plans=2    evdirs=0
kama-shokunin          graders52=-  ev69=-  plans=2    evdirs=0
kasegi-shokunin        graders52=-  ev69=-  plans=2    evdirs=0
kengaku-shokunin       graders52=Y  ev69=Y  plans=206  evdirs=88
kotoba-shokunin        graders52=-  ev69=-  plans=52   evdirs=0
kotodama-shokunin      graders52=-  ev69=-  plans=0    evdirs=0
kumitate-shokunin      graders52=-  ev69=-  plans=0    evdirs=0
lore-shokunin          graders52=-  ev69=-  plans=0    evdirs=0
mado-shokunin          graders52=-  ev69=-  plans=19   evdirs=0
mori-shokunin          graders52=-  ev69=-  plans=0    evdirs=113
revenger-shokunin      graders52=-  ev69=-  plans=0    evdirs=0
souji-shokunin         graders52=-  ev69=-  plans=0    evdirs=0
tabi-shokunin          graders52=-  ev69=-  plans=18   evdirs=107
tameshi-shokunin       graders52=-  ev69=-  plans=21   evdirs=0
tsukuroi-shokunin      graders52=-  ev69=-  plans=18   evdirs=0
```

Round 69 is fleet-wide and concurrent: fleet `.ufo/reports/round-69/` holds `audio, chousa, game-dev-2d,
kake, kama, kotoba, kotodama, kumitate, mori, revenger, tameshi, tsukuroi` (no kengaku yet), and nine sibling
lanes carry a `.ufo/waves/round-69/` dir. A per-lane count over those nine dirs:

```
chousa       round69: nginx=0  8080=0  pep503=0  etchosts=0
kake         round69: nginx=2  8080=0  pep503=0  etchosts=0
kama         round69: nginx=0  8080=0  pep503=0  etchosts=0
kotoba       round69: nginx=2  8080=1  pep503=0  etchosts=0
kotodama     round69: nginx=0  8080=2  pep503=0  etchosts=0
kumitate     round69: nginx=0  8080=0  pep503=0  etchosts=0
mori         round69: nginx=0  8080=0  pep503=0  etchosts=0
revenger     round69: nginx=0  8080=0  pep503=0  etchosts=0
tsukuroi     round69: nginx=0  8080=0  pep503=0  etchosts=0
```

Every non-zero cell was opened and is incidental: kake's two are the S009 registry mirror (§4 T2); kotoba's
two are scout receipts quoting `server: nginx` (§4 T13) and its one `8080` hit is a byte offset
(`ScoutAmp.md:35`, "offset 80803 of 102489"); kotodama's two are 14-digit Wayback capture timestamps
(`20200808073903id_`, `20250808020412id_`) inside SOURCES rows. **No sibling round-69 work touches this
round's C1 ground** — but the negative is "inspected and incidental", not "absent".

---

## 3. SURFACE-LEVEL 2

### S1 — tabi: the exact term, quoted from kengaku, adjudicated *to* kengaku → **ROUTED**

The only sibling that names `nginx-request-logging` at all. It names it as **kengaku's**, four times.

| File:line | What it is |
|---|---|
| `tabi-shokunin/corpus/adjacency-host-delta-r57.tsv:29` | `line  kengaku-shokunin  PROVINCE.md:969  -  -  -  **Reported out:** \`headless-terminal\` and \`nginx-request-logging\` (the other network-service members) are blocked on this host by absent …  no-tabi-ground  -` |
| `tabi-shokunin/corpus/adjacency-host-delta-r58.tsv:29` | same row, same disposition |
| `tabi-shokunin/corpus/adjacency-host-delta-r59.tsv:146` | same row, same disposition |
| `tabi-shokunin/corpus/lessons/round-57.md:66-67` | `… the line reports OUT terminal/nginx tooling (\`headless-terminal\`, \`nginx-request-logging\`) as blocked on absent binaries and keeps it kengaku ground; no browser, CDP, or web-interaction surface is named.` |
| `tabi-shokunin/.ufo/waves/round-57/measure/c1-adjudications.json` | machine record: `"lane": "kengaku-shokunin"`, reason `… nginx tooling (headless-terminal, nginx-request-logging) as blocked on absent binaries and keeps it kengaku ground … no tabi ground to declare overlap on` |

**Status: routed.** This is the sibling-split exit of the rule (`:256-258`): tabi's own committed scope
surfaces state the split and assign the element to kengaku. Not contested. tabi's files were left untouched.
Note the census rows are tabi `corpus/` files (a scope surface under `:54-55`), not merely a wave report — so
this is a real assignment, not an incidental mention.

**Second-order coupling (see §5.1).** All three censuses pin kengaku's province bytes:
`lane kengaku-shokunin PROVINCE.md f0b82513f781a803502f2c6c85e80eb8a8f6541c148afd19170ff7c094bba736 971 1 - - <head>`.
`sha256sum kengaku-shokunin/PROVINCE.md` today → the same `f0b82513…`, 971 lines. **The pin is currently
exact**, so any kengaku edit to that file is visible to tabi's next rebind.

### S2 — kotoba: the same gate shape, the same round → **ROUTED**

kotoba's round-69 C2 is a re-deriving counter over *its own* round-68 routed defects:

- `kotoba-shokunin/verifiers/check_r68_routed_repairs.py` (24,944 B, `Oct 25 07:28`), docstring line 2:
  `"""check_r68_routed_repairs.py — C2 counter for kotoba round 69.`; prints
  `r68 routed defects closed N of 8`; base pin `a5f7459f99bb27bf697e9438362e75ac5833eca8` must print
  `0 of 8` / exit 1; eight per-defect checks D1–D8, each naming the exact committed artifact it reads and
  running executing checks in a `git clone --shared` sandbox.
- Fleet `.ufo/reports/round-69/kotoba.md:25` — `C2 consistency — the eight routed round-68 defects closed |
  consistency | verifiers/check_r68_routed_repairs.py | r68 routed defects closed 8 of 8 (exit 0) | 0 of 8 (exit 1)`.
- Family precedent: `verifiers/check_r63_routed_repairs.py`, `…r64…`, `…r66…`, `…r67…` (kotoba
  `.ufo/waves/round-69/assimilation/validate/SKILL.md:493-496`), each a per-round routed-repair counter.

**Status: routed.** Same *method class* as `plans/round69_c2_routed_defects.py` (a base-red, re-deriving
closure counter over a prior round's routed defects); **different surface**: kotoba's predicate reads kotoba's
eight defects, kengaku's reads kengaku's seven (E1–E7). No E-check duplicates a D-check; no file is shared.
Boundary basis: `tameshi-shokunin/PROVINCE.md:14-17` ("every lane's gate remains its own … Never edits a
sibling's gate code"), and kotoba's `PROVINCE.md` claims the instruction-surface gates, not this one.

---

## 4. TERM-LEVEL 18

| # | Lane | Element actually hit | Evidence (file:line) |
|---|---|---|---|
| T1 | kake | nginx **source code** as ETag-format evidence (`ngx_http_set_etag`) — a committed scope surface, but a different element from config/logging/grader legs | `corpus/SOURCES.md:17` (S009), `corpus/knowledge/ghp-etag-anatomy.md:1,8,30,43,53,62,64`, `corpus/README.md:41`, `corpus/lessons/round-20.md:211`, `corpus/lessons/round-61.md:56`, `corpus/knowledge/drift-detection.md:104` ("Byte-nginx" backend label) |
| T2 | kake | round-69 mirror of T1 (concurrent round-69 artifact; not a scope surface) | `.ufo/waves/round-69/sources-append/registry-base.md:17` |
| T3 | kagi | `server: nginx` in 35 fetched HTTP captures | `.ufo/waves/round-26..31/**/*.headers` (e.g. `round-26/build/ClockS030.headers.txt:2`), plus `round-27/sandboxes/**` copies |
| T4 | kasegi | quoted source text: a paper citing Reese's nginx book; a Debian security changelog | `corpus/source-snapshots/round-24/S011.txt:532`, `round-40/S025.txt:427,952`, `round-50/S080.txt:1238,1243` |
| T5 | kama | negative absent-process finding while diagnosing the 8080→34113 forward | `corpus/lessons/round-1-critic.md:110` |
| T6 | kotodama | a fetched page that *was* an nginx error body; a dead-link note | `corpus/lessons/round-54.md:129`, `corpus/knowledge/civilizations/mesoamerica-primary-sources.md:33` (`HTTP 404, nginx; TLS certificate CN=…`) |
| T7 | kaidoku | `nginx.vim` file paths inside an AppImage inventory | `corpus/evidence/round-36/c1/{K3,K4}/oracle.tsv:651,946` (+ their `after.json`) |
| T8 | mori | captured `server: nginx` headers, a nav link to nginx.org, `app: nginx` page prop | `corpus/evidence/recheck-r32/S043.src:440`, `sources-r48/aliyun-nas-quota.html:190`, `sources-r67/S578.html:4626`, `sources-r59/w1-results-r54.json:154` |
| T9 | chousa | wave fetch headers + `network.json` fixtures (all `.ufo/`) | `.ufo/waves/round-29/falsify/DiffToolB/*.network.json`, `round-30/falsify/AttackRowS055/fetch-headers.txt:2`, `round-31,33/**/*.headers` |
| T10 | tsukuroi | mirror headers, `certbot-nginx` / `nginx 1.30.6-1` package rows, one `openat(… "nginx" …)` strace line | `.ufo/waves/round-24/w1/ExecMirrorTimestamps/*`, `round-32/w2/RevSourcesRows/S175-retry.headers:2`, `round-48/w2/TExecLiveKill/tr.base:12109` |
| T11 | souji | `server: nginx` in wave + census headers | `.ufo/waves/round-23/w1/ScoutCommunity.md:18`, `round-44/w1/S44scout58/os.headers.txt:2`, `census/round-44/waves/w1/…` |
| T12 | tameshi | `server: nginx` in evidence/wave headers, incl. a **round-69** capture | `.ufo/evidence/round-69/win-host/sources/s300-headers.txt:4`, `round-68/…/s299-headers.txt:4`, `round-60/**`, `.ufo/waves/round-41,54/**` |
| T13 | kotoba | round-69 scout receipts quoting the header; an omp binary string | `.ufo/waves/round-69/w1/ScoutDeepCode.md:21` (`server: nginx/1.18.0 (Ubuntu)`), `ScoutJunie.md:138` (`nginx/1.31.7`), `.ufo/round-44/evidence/omp-live-18.12.2-strings.txt:2408306` |
| T14 | audio | `server_name` is the PipeWire/ALSA **`Server Name:`** field, a different domain entirely | `corpus/fixtures/measure_audio.py:1236,2462,3157,3179,42530` |
| T15 | fleet | `7788` has no port surface; all hits are hash/nonce substrings | kaidoku `corpus/evidence/*/after.json`, mado `c2-at-data-nonce778899.txt`, kotodama `S571 …4587788/hsj-…` |
| T16 | kagi | `PEP 503` only in vendored `packaging` inside `node-gyp` | `.ufo/waves/round-28/retained-probes/SrcNodeSemver/node_modules/node-gyp/gyp/pylib/packaging/{markers,utils}.py` |
| T17 | kake + kaidoku | `/etc/hosts` as fetched source text and as **firmware fixture content** — never as a sandbox staging file | kake `.ufo/waves/*/sources/rfc3986.txt`; kaidoku `tools/round-40/mk-l-carriers.py:53`, `tools/round-41/mk-l-carriers.py:88` |
| T18 | kumitate + kagi + tameshi | routed-defect **mechanism variants**, not closure counters: kumitate a ledger-completeness gate (`UNLEDGERED`/`QUOTE_ABSENT`/`ANSWER_DEAD`, contract `kumitate-routed-ledger-v2`, round 68); kagi a one-closure disposition parser; tameshi a method registry | `kumitate-shokunin/scripts/routed-ledger.mjs:1-25`, `kagi-shokunin/corpus/closure-dispositions.py:1-20`, `tameshi-shokunin/corpus/routed-defects.json` |

Distinctiveness check for T18: `grep -rn 'DEFECTS n='` fleet-wide outside kengaku → **only** kengaku's own
`.ufo/reports/round-68/kengaku.md` lines (24, 40, 42, 51, 52, 96). The print shape is not reused anywhere.

---

## 5. Second-order effects and contradictions (stated, not smoothed into a score)

### 5.1 kengaku's own scope surface contradicts the round's after-state — and a sibling has it pinned

`kengaku-shokunin/PROVINCE.md:969` reads:

> **Reported out:** `headless-terminal` and `nginx-request-logging` (the other network-service members) are
> blocked on this host by absent `vim` and `nginx`; tmux-based terminal harness work stays kengaku ground if
> the binaries land.

`kengaku-shokunin/SKILL.md:78` today reads `executed 2 of 8 (round 64 \`kv-store-grpc\`; round 68
\`pypi-server\` replayed offline …)`. R69-C1's declared target is `executed 3 of 8` plus a `S241` row.

After a passing C1 the lane holds two scope surfaces that disagree about the same member: SKILL.md says the
class has three executed members including `nginx-request-logging`; PROVINCE.md says that member is blocked
because `nginx` is absent. **Both are literally defensible** — the replay prices the grader through a
lane-written shim, and `PROVINCE.md`'s own narrow reading survives (named limitation (ii): the shim answers
`-t`, so nginx's real syntax checker is still not exercised). What is false after C1 is only the *implication*
that the member is untouched. So this is a **precision gap, not a falsification** — an attacker who calls
`PROVINCE.md:969` false would be overstating.

The contradiction is in the remedy, and I will not resolve it:

- **Arm A — leave `PROVINCE.md:969` as written.** Cheap, keeps tabi's pin exact, and the sentence stays
  literally true. Cost: the lane's province text silently understates its own coverage, and tabi's three
  censuses keep a quote that reads as "not entered" while the round's C1 says "entered".
- **Arm B — amend `PROVINCE.md:969` to name the offline replay and keep "real-nginx execution blocked".**
  Makes the lane's two scope surfaces agree. Cost: kengaku's `PROVINCE.md` sha256 changes from
  `f0b82513…` (971 lines) to something else, and **all three of tabi's committed censuses
  (`adjacency-host-delta-r57/r58/r59.tsv`) pin that sha and the 971-line count**. tabi's round-57 lesson
  records `correction cycle 0 of 2 consumed`; a moved line spends one. That is a real, measurable cost paid
  by another lane for a kengaku bookkeeping edit.

Neither arm is in R69-C1's frozen before→after targets, which name only `SKILL.md`, `corpus/SOURCES.md` and
the receipt. **This is the finding: the target set is incomplete on the lane's own scope surfaces, and the
omission is coupled to a sibling's pin.** It is not mine to fix — `PROVINCE.md` is outside my write scope and
outside the frozen targets.

### 5.2 The 8080 lock is lane-local

`~/.local/share/kengaku-r69/port-8080.lock` serialises kengaku seats only. Sibling lanes have no reason to
honour it, and the fleet's 8080 has a documented history of being a *foreign* listener (Jitsi; fleet
`AGGREGATE.md:318-321,934-937`, kama `corpus/lessons/round-1-critic.md:110`, kagi `round-3/kagi.md:23-26`).
At scan time `ss` showed no listener, and no sibling lane binds 8080 (all sibling uses are `curl` GETs), so
the hazard is **standing but not triggered**. The probe's own refusal design (`SETUP port-8080-occupied`) is
the correct guard and already covers it; nothing to change.

### 5.3 Two lanes score "round-68 routed defects closed" in the same round 69

kotoba (C2, eight defects, `N of 8`) and kengaku (C2, seven defects, `DEFECTS n=0`). A fleet reader scanning
`.ufo/reports/round-69/` sees the same phrase twice. They are not the same claim and neither can be cited as
corroboration for the other. Recording it so the round's own report does not imply cross-lane agreement that
does not exist.

---

## 6. Findings a claim's attacker should use

1. **R69-C1 — the before→after set is incomplete (§5.1).** `PROVINCE.md:969` is the sentence a sibling has
   already pinned and adjudicated, and it is the one sentence the round's own staging makes imprecise. Ask the
   claim for its disposition: A or B, named, with the tabi cost stated. "Not touched" is an answer, but it
   must be an explicit one.
2. **R69-C1 — do not let the attack overstate.** The "blocked … by absent `nginx`" clause is *narrowed*, not
   falsified, by a shim-priced replay. An attacker who writes "PROVINCE.md is false" has mis-calibrated; the
   defensible statement is "PROVINCE.md no longer states the member's actual status".
3. **R69-C1 — no sibling corroboration exists for the config semantics.** `limit_req_zone`, `access_log`,
   `nginx.conf`, `server_name` have **zero** sibling occurrences. The K4 red witness and the K3 log legs rest
   on the grader's bytes and the lane's shim alone; there is no sibling knowledge entry to lean on and none to
   route to. Anyone claiming "the fleet already knows nginx request logging" is wrong.
4. **R69-C1 — the `/etc/hosts` staging has no precedent to inherit.** No sibling stages a lane-written
   `/etc/hosts`; the only `/etc/hosts` in sibling trees is firmware fixture content (kaidoku) and fetched RFC
   text (kake). The staging fix disclosed in the freeze is genuinely new lane method, not a copied pattern —
   so it carries no sibling review.
5. **R69-C2 — a same-round sibling precedent exists with a stricter per-defect shape (S2).** kotoba's D1–D8
   each name the exact committed artifact read, pin a base-red revision, and sandbox anything that executes.
   Ask whether each of kengaku's E1–E7 names an artifact that *can be absent* and a base-red value it must
   print at `a518980e` — that is the shape the fleet's most mature instance uses, and it is a fair bar to hold
   E1–E7 to. It is not a defect if E1–E7 differ; it is a question worth asking before the after-receipt is
   scored.
6. **R69-C2 — the `DEFECTS n=` print shape is kengaku's alone** (zero non-kengaku hits fleet-wide), so no
   reader can confuse it with a sibling gate's output. Negative, and useful: it means the gate's verdict line
   cannot be satisfied by a sibling instrument's transcript.

---

## 7. Commands run (exact argv) — and what each returned

Read-only throughout. `grep`/`read`/`glob` tool calls are described by pattern and path; shell argv is exact.

```
ls /home/vgpnk/Projects/shokunin/                                   → 21 *-shokunin lanes + fleet files
git -C . rev-parse --short HEAD                                    → b288e8e0
git -C . status --porcelain                                         → 3 untracked round-69 wave paths only
ls .ufo/waves/round-69/w1/                                          → CensusAudit, GateReceipts.md, LegPricing.md,
                                                                      NginxBattery, NginxBattery.md, ReceiptReverify,
                                                                      drafts, gates, nginx, provenance-erratum.txt,
                                                                      swarm-registry.json
for d in */; do … [ -d "$l/corpus/evidence/round52/graders" ] …     → matrix in §2 (kengaku only Y)
for d in */; do grep -rl -i nginx … ; grep -rl -F 'PEP 503' … ; done → per-lane term counts (nginx kake=174,
                                                                      kasegi=53, kama=40, kotodama=30, kengaku=156,
                                                                      kaidoku=18, chousa=14, tsukuroi=15, kagi=10,
                                                                      mori=6, tameshi=6, souji=5, kotoba=4, tabi=2,
                                                                      revenger=1, kumitate=2; pep503 kengaku=41,
                                                                      kagi=2; etchosts kengaku=15, kake=12,
                                                                      kaidoku=8)
grep -rln -F 'PEP 503' .                                             → 2 vendored node-gyp files (§4 T16)
for l in …; do [ -d "$l/corpus/evidence/round69" ] … ; done          → chousa + kengaku only
ss -ltnp '( sport = :8080 )'                                         → header row only; no listener
ls -la /home/vgpnk/.local/share/kengaku-r69/                         → port-8080.lock, 0 B, Nov 3 21:06
ls /home/vgpnk/Projects/shokunin/.ufo/reports/round-69/              → 12 sibling reports, no kengaku
for l in chousa kake kama kotoba kotodama kumitate mori revenger tsukuroi; do … grep -rl -i nginx …
  grep -rl -F '8080' … grep -rl -F 'PEP 503' … grep -rl -F '/etc/hosts' …; done
                                                                     → per-lane table in §2; every non-zero
                                                                       cell opened and incidental
for l in */; do grep -rl -F 'nginx-request-logging' "$l"; done      → kengaku 127, tabi 7, all others 0
for l in …; do find "$l" -maxdepth 3 \( -name '*defect*' -o -name '*routed*' \); done
                                                                     → tameshi corpus/routed-defects.json;
                                                                       kumitate corpus/routed-ledger.md +
                                                                       scripts/routed-ledger.mjs; kotoba
                                                                       verifiers/check_r{63,64,66,67,68}_routed_repairs.py
grep -rln -F 'network-service' */corpus */SKILL.md */PROVINCE.md     → 17 files, all kengaku (§2)
grep -rlnE 'nginx\.conf|server_name|error_log|limit_req' …           → audio measure_audio.py only (T14)
grep -rn 'DEFECTS n=' … | grep -v kengaku-shokunin                  → no output (§4 T18)
grep -rn -E '(:|port[ =]|port=)7788\b' .                             → no port token (T15)
sha256sum kengaku-shokunin/PROVINCE.md                               → f0b82513f781a803502f2c6c85e80eb8a8f6541c148afd19170ff7c094bba736
git -C kengaku-shokunin rev-parse HEAD                               → b288e8e03bdfed715bbb6de0ea166e2c465c0453
for f in r57 r58 r59; do grep -P '^lane\tkengaku-shokunin\t' tabi-shokunin/corpus/adjacency-host-delta-$f.tsv; done
                                                                     → 3 rows, sha f0b82513…, 971 lines, heads
                                                                       21b13dc7 / b5032ff8 / 2c1ef88a
sed -n '960,975p' kengaku-shokunin/PROVINCE.md                       → the "Reported out" sentence (§5.1)
sed -n '58,72p' tabi-shokunin/corpus/lessons/round-57.md             → the no-tabi-ground adjudication (S1)
sed -n '1,40p' kotoba-shokunin/verifiers/check_r68_routed_repairs.py → D1–D8 contract (S2)
ls -l kotoba-shokunin/verifiers/check_r68_routed_repairs.py          → 24944 bytes, Oct 25 07:28
head -25 kumitate-shokunin/scripts/routed-ledger.mjs                 → ledger-completeness contract (T18)
head -20 kagi-shokunin/corpus/closure-dispositions.py                → disposition parser (T18)
find tabi-shokunin -name 'c1-adjudications.json'                     → .ufo/waves/round-57/measure/… (S1)
grep -n 'executed [0-9] of 8' kengaku-shokunin/SKILL.md              → 78:| network-service | 8 | executed 2 of 8 …
df -h /fast                                                          → 804G, 53% used
```

**Two queries were re-run, and the first form is recorded so nobody reproduces it.** A `grep` whose `path` was
the glob `/home/vgpnk/Projects/shokunin/*-shokunin` returned `No matches found` for `nginx-request-logging`
and for a control term known to exist (`TB2`) — i.e. that path form silently matches nothing in this tool, and
a "no matches" from it is not evidence. Every cross-lane count in §2 was therefore taken with a shell
`for l in */` loop that names each lane directory explicitly. Likewise a first pass over the nine sibling
round-69 wave dirs used one combined alternation and a per-file match cap; it was re-taken as four separate
per-lane counts (§2 table), which is what surfaced kotoba's and kotodama's incidental `8080` hits.

## 8. Commands NOT run (stated so no check is read as passed)

- **The C1 battery was not run by me.** No invocation of `plans/round69_c1_nginx_probe.py` in any form:
  not the measuring command, not `--check-receipt`, not `--render-table`, not `--selftest`. I did not read the
  NginxBattery seat's receipt to form a verdict, and I assert nothing about C1's pass or fail.
- **The C2 gate was not run by me.** No invocation of `plans/round69_c2_routed_defects.py`, with or without
  `--selftest`.
- **No sibling gate, battery, test, linter or formatter was run** in any lane (kagi's `claim-ledger.sh`,
  kumitate's `routed-ledger.mjs`, kotoba's `check_r*_routed_repairs.py`, tabi's census scripts — all read only).
- **No git/jj write** anywhere: no commit, push, stage, stash, checkout, switch, add, rm, restore. Only
  `rev-parse`, `status`, and `sha256sum`/`grep` reads.
- **No file edited** other than writing this report. Sibling files, `PROVINCE.md`, `SKILL.md`,
  `corpus/SOURCES.md`, `corpus/QUALITY.md`, the fleet root's `MANIFEST.json` and `.ufo/` were read, never
  written.
- **No tool installed or upgraded** (no pacman, no `uv tool install`, no `npx`, no binary fetch). Nothing to
  record under the tooling authorization.

## 9. Scratch

`/fast/scratch/hyaku/kengaku-r69/SiblingOverlap` was created with `mkdir -p` and held no files (the scan is
grep-and-read only, no clone, mirror, fixture or `--work` dir was needed). It is deleted before this seat
yields.
