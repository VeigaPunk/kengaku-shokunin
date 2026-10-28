# C1RevPredicate — R51-C1 predicate fidelity (clause ↔ code)

Seat: `C1RevPredicate`, reviewer. Round 51 (hyaku run 11), wave 1. Lane `kengaku-shokunin`.
Item: read the frozen predicate sentence in `plans/round-51-claims.md` §C1 beside
`plans/round51_surfaces.py`; list every clause and the exact implementing lines; name clauses the
code does not implement, code legs the sentence does not declare, and clauses whose implementation
is weaker than their wording.

## Axes named

- Axis under review: **freshness 8 → 9** (claim R51-C1: "every surface `PROVINCE.md` declares is
  machine-checked at the tip"). I did not measure the axis; I measured whether the counter can
  decide it.
- My own review axes, in the order they decide the verdict:
  1. **predicate fidelity** — does each clause of the frozen sentence have code that computes
     exactly that clause, against the document?
  2. **kill-rule enforceability** — can the §C1 kill rule fail a landing that the claims forbid?
  3. **receipt integrity** — does a receipt identify the revision and the tree it measured?

## Revision measured

```
REV e07f131cf7037e58a21db6e1f3986cf401ad257c   (stage-1 freeze, detached clone; files byte-identical to tip 4090c3db)
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7   (lane master tip; also the hash the counter itself prints — see F7)
```

`git diff --stat e07f131 -- plans/round51_surfaces.py plans/round51-surfaces.json plans/round-51-claims.md PROVINCE.md corpus/routed-findings.jsonl plans/round51_routing.py` → empty (instrument, manifest, claims and `PROVINCE.md` are unchanged between freeze and tip), so every reading below holds at both.

sha256 of the measured files (from the freeze clone):

```
edf09db7be767a29bac4a645185f2f87452ec1451322d9e723ca65111f53e01e  plans/round51_surfaces.py
60d05a0a3f5b099061a902fac7612cd178c8dda01680ac04b84611a77fcf2dd8  plans/round51-surfaces.json
5e00336ff4ce2edb79346c4021e5bec24e5a6490ef5ccc53bd81fe5b6f7a5298  PROVINCE.md
```

Scratch: `/fast/scratch/hyaku/kengaku-r51/C1RevPredicate` (one `git clone --shared` + 18 fixture
trees). Free space seen at start: `/dev/nvme1n1p2 804G 249G 555G 31% /fast`. Removed before yield.

## Commands run

```sh
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/.../lane
git -C $D rev-parse --show-toplevel     # asserted == $D before every write
git -C $D checkout --detach e07f131cf7037e58a21db6e1f3986cf401ad257c
cd $D && python3 plans/round51_surfaces.py --lane .            # frozen command, freeze tree
cd /home/vgpnk/Projects/shokunin && python3 $D/plans/round51_surfaces.py --lane $D   # --lane from a foreign cwd
cd $D && python3 plans/round51_surfaces.py --selftest
# fixtures: git -C $D archive e07f131 | tar -x -C fxN  (no .git in fixtures, so REV=unknown there)
cd fxN && python3 plans/round51_surfaces.py --lane .
```

Frozen command at the freeze tree, verbatim (this reproduces `claims/c1-before.txt` line for line,
including the `REV` line — which is the first defect, F7):

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
MANIFEST plans/round51-surfaces.json entries=19 sections=2
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
STALE 0
UNVERDICTED 1
NUMBER-DRIFT 1
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
EXIT=1
```

`--selftest` → `[selftest] cases=9 failures=0` / `[selftest] ALL PASS`, exit 0.

---

## §1 Clause map — frozen sentence → implementing lines

Predicate sentence (`plans/round-51-claims.md` §C1, "**Predicate:** exit 0 and final line
`PREDICATE R51-C1 pass`, iff …"), against `plans/round51_surfaces.py` (line numbers at freeze).

| # | Clause (wording) | Implementing lines | Implemented as |
|---|---|---|---|
| 1 | `exit 0` | L225-226 `return 0 if ok else 1`; L363-364 `sys.exit(main())` | yes |
| 2 | `final line PREDICATE R51-C1 pass` | L225 (last `print` before `return`) | yes in `check()` mode — but `--selftest` also prints `PREDICATE R51-C1 pass` (S0, mid-stream, L225 via `run(True)`), see F12 |
| 3 | `ANCHOR-DUP 0` | L165-167 (append), L212-217 (verdict) | yes, but only for one anchor string appearing twice in one section's table — never for two entries claiming one row (F4) |
| 4 | `ANCHOR-MISSING 0` | L162-164 | yes |
| 5 | `UNCOVERED 0` | L172-188: `used` = anchors found, `row_idx` = section rows, `unc = row_idx - used` | yes at **row** granularity; the `stray` leg (L184-186) is unreachable by construction (`anchor_line` is built from that section's rows), and "exactly one entry" (docstring L9) is not computed (F4) |
| 6 | `SECTION-MISSING 0` | L178-179 `if not rows:` | **not implementable in practice**: `section_rows` (L62-88) crosses headings while `started` is false (L73-76), so a section whose table is gone borrows the next section's table and `rows` is never empty (F8) |
| 7 | `STALE 0` (probe agrees with recorded state) | L197-198 `if observed != e["state"]` | yes, against the **manifest's probe spec**, which is a subset of what the row declares (F11) |
| 8 | `DRIFT 0` (recorded state agrees with what the row asserts) | L199-200 `if e["prose"] != e["state"]` | **no** — compares two manifest fields; the row text is never read (F1) |
| 9 | `UNVERDICTED 0` (every absent row carries an `ABSENT <ISO date>` marker) | L201-204 + `ABSENT_RE` L36 | yes, but only for `state=="absent"` entries, only on the anchor line, and any ISO-shaped date passes (F3, F9) |
| 10 | `NUMBER-DRIFT 0` (every `count_claim` equals the probed count) | L205-208 `re.search(r"(\d+)", detail)` | **weaker** — first integer of a free-form detail string of *any* probe kind (F10); rows stating numbers with no `count_claim` are invisible (F11) |
| 11 | `RESOLVE observed_present >= resolve_floor` (floor 13) | L219-223, floor read from `man["resolve_floor"]` | **weaker** — the floor is read from the same file the landing edits; nothing pins it to 13 (F5) |
| 12 | (docstring only) `anchors total == manifest entries` | L8, L170 | tautology: `total = len(entries)` |

Sentence clauses the code does not implement: **8** (DRIFT reads no document text), **6**
(SECTION-MISSING is dead while any later table exists), and the *exactly-one-entry* half of 5.

## §2 §C1 clauses outside the predicate sentence that no code implements

The sentence is not the whole of §C1; these bindings have no code leg and are therefore decided by
prose alone:

| §C1 binding | Code leg | Measured |
|---|---|---|
| Kill rule: "`ROWS` per section must not fall below 9 and 10" | none — `ROWS` is only printed (L187-188) | `fxC`: 3 declared rows + their entries deleted → `ROWS section="## Surfaces" rows=6 entries=6`, `PREDICATE R51-C1 pass`, exit 0 |
| Kill rule: "the landing edit deletes a surface row instead of dating it" | none | same `fxC` run — this is exactly the forbidden edit and it passes |
| After target: "coverage 19/19 **plus one new declared surface**" | none | `fx10b` passes with 19 entries and no new surface |
| Controls 2/3/4 (`drop-one-entry`, `stale-pin`, `undated-absence`) | only mirrored inside `--selftest` S5/S2/S3; the frozen command does not run them | not measured here (out of my item) |
| Control 1 (`declare-all-absent`) "resolve floor is violated" | L219-223, floor from manifest | the control fails on STALE, not on the floor: `fx2` passes at `present=0 floor=0` (F5) |

## §3 Code legs the sentence does not declare

| Leg | Lines | Why it matters |
|---|---|---|
| `REV <hash>` | L148 + `tip_rev` L49-59 | runs `git rev-parse master`, **not** `HEAD`; prints the branch tip regardless of the tree measured (F7) |
| `MANIFEST <path> entries= sections=` | L149 | the only record of which manifest was used; `--manifest` can point at any file |
| `ANCHORS` / `ROWS` / `PROBES` diagnostics | L170, L187-188, L209 | `PROBES … errors=%d` prints a variable that is initialised at L190 and **never incremented** — always `errors=0` (F12) |
| `DETAIL <KEY> …` lines | L214-215 | free-text, truncated to 80 chars of `why` |
| probe kinds `port`, `http` | L110-136 | network probes (1.5 s / 3 s timeouts) inside a counter whose result is claimed deterministic; SF03 probes `/health` while the row declares `/v1/models`, `/health`, `/v1/chat/completions` |
| `--selftest` (9 cases S0-S8) | L235-330 | undeclared in the claims; emits a `PREDICATE R51-C1 pass` line for S0, so `grep PREDICATE` on a selftest log reads a pass (F12) |
| `--manifest` / `--province` overrides | L350-352 | let the counter check a document other than `PROVINCE.md`; nothing in the receipt pins the pair |
| heading match by prefix | L65 `l.strip().startswith(heading)` | manifest `"## Surfaces"` is **not** the heading in `PROVINCE.md` (`## Surfaces (re-verified round 14, …)`; exact-equality False; `### Core` exact-equality True) — an earlier heading sharing the prefix hijacks the section (F13) |
| `lane` argument used by `count` only | L132 (`lane / target`) vs L91, L101 (`expand(t).exists()`) | `paths`/`sha256` targets resolve against **CWD**; `--lane` does not select the tree for 17 of 19 entries (F6) |

## §4 Clauses weaker than their wording — measured

Each fixture is a copy of the freeze tree (`git archive`), run with the frozen command. Only the
named files were edited.

**F1 — DRIFT reads no document text (clause 8).** `fx1`: manifest `prose` for SF01/SF02/SF03 set to
`absent`, `count_claim` SF14 set to `170`; `PROVINCE.md` untouched (sha `5e00336f…` identical
before and after):

```
DRIFT 0
STALE 0
UNVERDICTED 1
NUMBER-DRIFT 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail          (exit 1; only UNVERDICTED remains)
PROVINCE.md sha before/after: 5e00336ff4ce2edb 5e00336ff4ce2edb IDENTICAL
```

So two of the three before-receipt failures are clearable **without touching the declared surface**.
Worse, the recorded readings are contradicted by the rows they describe: the three DRIFT rows each
already carry a dated marker — `PROVINCE.md` lines 12, 13, 14 carry `ABSENT 2026-10-20` at offsets
356, 420, 1039 — and SF01's row states the first local path "does **not** exist here (`test -e` →
absent)". The claims' before-narrative "rows still assert they resolve" is false for all three; the
truthful `prose` is `absent`, which yields `DRIFT 0` at the base tip with `PROVINCE.md` untouched.
`DRIFT 3` is manufactured by the manifest.

**F3 — rows may declare ABSENT while every surface resolves (clause 9 + 8).** `fx8`: all 20 table
rows stamped `**ABSENT 2026-10-28**`, entries untouched (`state=present`):

```
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 0   STALE 0   UNVERDICTED 0   NUMBER-DRIFT 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 pass          (exit 0)
```

`UNVERDICTED` is skipped for `state=present`, so a document that declares every surface absent —
the exact inversion of C1 — passes.

**F4 — "exactly one entry per row" is not computed (clause 5).** `fxA` (passing baseline + a second
entry anchored to the already-covered SF13 row):

```
ANCHORS total=20 dup=0 missing=0
ROWS section="### Core" rows=10 entries=11 uncovered=0
ANCHOR-DUP 0   UNCOVERED 0
PREDICATE R51-C1 pass          (exit 0)
```

**F5 — the resolve floor is self-declared (clause 11).** `fx2` (synthetic: 2 absent, dated rows, all
probes absent, `resolve_floor: 0`):

```
RESOLVE observed_present=0 floor=0 verdict=met
PREDICATE R51-C1 pass          (exit 0)
```

Nothing enforces `resolve_floor >= 13`, so §C1's Limits sentence ("adding a resolving surface raises
the count, it never lowers it") is not a property of the instrument.

**F6 — `--lane` does not select the probed tree.** From the fleet root:
`python3 $D/plans/round51_surfaces.py --lane $D` → `PROBES run=19 present=3 absent=16 errors=0`,
`STALE 10` (SF07-SF13, SF17-SF19), `RESOLVE observed_present=3 floor=13 verdict=violated`, exit 1.
The frozen command is correct only because its CWD is the lane root; a receipt produced with
`--lane <clone>` from anywhere else measures the caller's CWD for 17 entries.

**F8 — SECTION-MISSING cannot fire while a later table exists (clause 6).** `fx4` (`### Core` table
deleted, heading kept):

```
ROWS section="### Core" rows=8 entries=10 uncovered=8
ANCHOR-MISSING 10
UNCOVERED 8
  DETAIL UNCOVERED ### Core row line 124 has no manifest entry
  …
SECTION-MISSING 0
PREDICATE R51-C1 fail
```

`### Core` borrowed eight rows from `### Frontier` (lines 124-131); the run fails, but it blames the
wrong section and the declared clause never fires.

**F9 — the ISO date is a token, not a verdict (clause 9).** `fxB2` (row and anchor dated
`ABSENT 1999-01-01`) → `UNVERDICTED 0`, `PREDICATE R51-C1 pass`, exit 0. `fxB3` (`ABSENT
2099-12-31`, a future date) → `UNVERDICTED 0`, pass, exit 0.

**F10 — NUMBER-DRIFT reads the first integer of any detail string (clause 10).** `fx6`, with
`count_claim: 5` on SF07 (a `paths` entry, nothing counted):

```
NUMBER-DRIFT 0
PREDICATE R51-C1 fail          (fails on the unrelated baseline counters)
```

with `count_claim: 3`:

```
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF07 row claims 3, probe says all 5 targets resolve
```

The compared "probed count" is the target count inside an English sentence.

**F11 — the probe is a subset of what each row declares (clauses 7 and 10).** Row-by-row, from
`PROVINCE.md` lines 12-19 and 107-116 vs the manifest:

| Entry | Row declares | Probed |
|---|---|---|
| SF01 | parent + 5 subpaths (`wiki/ai/agents-and-engineering/`, `wiki/karpathy/`, `wiki/ai/{4 dirs}/`, `Home.md`, `raw/`) | parent dir only |
| SF02 | `~/archive/bench-arena/` + 6 targets (`tasks/`, `grade.sh`, `loop.sh`, `report-grok45.csv`, `report-qwenlocal*.csv`, `telemetry-qwenlocal-v2.csv`) | parent dir only |
| SF03 | 3 endpoints (`/v1/models`, `/health`, `/v1/chat/completions`) | `/health` |
| SF05 | 2 paths | 1 |
| SF06 | local pair + 2 HTTPS catalogs (huggingface, openrouter) | `index.md` |
| SF07 | 10 evidence dirs | 5, one of which (`round13-coverage`) is **not** in this row |
| SF08 | `python3 grader.py` exit 0/1/2, `--selftest` S0-S7 | `grader.py` exists |
| SF09 | arXiv / ACL / ICLR / vLLM / GitHub issues | one local citation file |
| SF10 | digest `90c87c88…ae941f` | 8-hex prefix `90c87c88` |
| SF11 | 12 dirs in the row's own loop + "28 root receipt logs" | 7 dirs; no count |
| SF12 | `attrib_probe.py` + `-r21-`/`-r22-`/`-r23-frozen.md` | `attrib_probe.py` digest |
| SF14 | `test -e` + "25 rows" + 2 evidence paths | count only |
| SF15 | digest `42d86d99…15a386` | 8-hex prefix |
| SF16 | `ss -ltn 'sport = :8791'` | TCP connect to loopback |
| SF17 | 3 named sources incl. "the ART dossier" | 2 files |
| SF18 | `--summary` + `--selftest` exit 0; "4 unique samples, 92/92 correct, transitions 2, 1" | `attrib_calibration.py` exists |
| SF19 | `--summary` + `--selftest` exit 0; "10 mismatches" | `state_check.py` exists |

Only SF04 and SF13 are 1:1. Rows stating numbers with no `count_claim` (SF11 "28", SF18 four
numbers, SF19 "10", SF14's two evidence paths) are invisible to NUMBER-DRIFT.

**F13 — section identity is a prefix, not the heading.** `fx9` (an earlier `## Surfaces (archived,
round 9)` table inserted above the real one): `ROWS section="## Surfaces" rows=1 entries=9
uncovered=1`, `ANCHOR-MISSING 9`, `SECTION-MISSING 0` — the manifest's section string never equals a
heading in the document, and the first prefix match wins.

**F14 — the SF04 anchor embeds the marker the repair must change.** SF04's anchor is
`` `~/Projects/bounties/ledger/telemetry.jsonl` — **ABSENT** ``. Dating the row (the intended
repair) makes the anchor stop matching: `fx10` → `UNVERDICTED 1` + `ANCHOR-MISSING 1`. Only after
re-pinning the anchor in the manifest (`fx10b`) does the counter pass:

```
REV unknown
MANIFEST plans/round51-surfaces.json entries=19 sections=2
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 0   STALE 0   UNVERDICTED 0   NUMBER-DRIFT 0
ANCHOR-DUP 0   ANCHOR-MISSING 0   UNCOVERED 0   SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 pass          (exit 0)
```

**F7 — the REV line does not identify the measured tree.** In the freeze clone `git rev-parse HEAD`
= `e07f131…`, and the counter printed `REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7` (master's tip),
because `tip_rev` runs `rev-parse master` (L52-54). The tree is also unverified for dirtiness, so a
receipt can name a commit whose bytes were not measured. `c1-before.txt` is correct only by
coincidence (measured with CWD = lane on `master` at `297e179`).

**F12 — `errors` is a fabricated constant.** `present = absent = errors = 0` (L190); only
`present`/`absent` are incremented; `PROBES … errors=%d` (L209) therefore prints `errors=0` in every
run, including runs where probes fail (F6 printed `absent=16 … errors=0`). Separately, `--selftest`
prints `PREDICATE R51-C1 pass` for S0 mid-stream, so a `grep PREDICATE` on a selftest log reads a
pass.

## §5 Findings by severity

**Blocker (the counter cannot decide the claim as written)**

1. **F1** — `DRIFT` (L199-200) compares `prose` to `state`; the document is never read. `DRIFT 3` is
   clearable by editing only the manifest (`fx1`), and the recorded readings for SF01/SF02/SF03 are
   contradicted by rows that already carry `ABSENT 2026-10-20`. The claim's "surface changed:
   `PROVINCE.md`" is not enforced by the predicate.
2. **F3** — a `PROVINCE.md` whose every row says ABSENT passes (`fx8`, exit 0). This is the exact
   inversion of C1 and it is indistinguishable from the after target.
3. **F2/§2** — the kill rule's row-count floor is not computed: deleting three declared surface rows
   (the forbidden "delete instead of date") passes at `rows=6` (`fxC`, exit 0).
4. **F5** — the resolve floor is read from the file under edit; `present=0 floor=0` passes (`fx2`).
   Control 1 therefore does not test the floor, only STALE.
5. **F6** — `--lane` does not select the probed tree for 17 of 19 entries (`paths`/`sha256` are
   CWD-relative). Any receipt produced with `--lane <dir>` from a foreign CWD is void (measured:
   `present=3`, `STALE 10`).

**High (clause fires but not on the clause's wording)**

6. **F7** — `REV` prints `master`'s tip, not `HEAD`; no dirty-tree detection. Receipt integrity for
   every C1 receipt, including the before receipt's provenance claim.
7. **F11** — one entry per row, probe per entry: the row's declared targets are only partly probed
   (SF01, SF02, SF03, SF05, SF06, SF07, SF08, SF09, SF11, SF12, SF17, SF18, SF19), and rows stating
   numbers without `count_claim` are invisible. "Every surface is machine-checked" is true only at
   row granularity, for whatever subset the manifest chose.
8. **F8** — `SECTION-MISSING` is unreachable for both declared sections while later tables exist;
   the failure is reported against the wrong section (borrowed `### Frontier` rows).
9. **F14** — the SF04 anchor contains the marker the repair must change, so the intended edit breaks
   `ANCHOR-MISSING` unless the manifest is edited in lockstep.
10. **F10** — `NUMBER-DRIFT` compares the first integer of a free-form detail string of any probe
    kind; a fabricated `count_claim` on a `paths` entry is accepted.

**Medium (soundness/diagnostics)**

11. **F4** — "covered by exactly one entry" (docstring L9) is not computed: 20 entries over 19 rows
    passes.
12. **F9** — any ISO-shaped date satisfies `UNVERDICTED` (1999 and 2099 both pass); the marker is a
    token, not a re-verification.
13. **F13** — section identity is a `startswith` prefix; the manifest's `"## Surfaces"` is not the
    heading in the document, and an earlier prefix match hijacks the section.
14. **F12** — `errors=0` is printed but never computed; `--selftest` emits a mid-stream
    `PREDICATE R51-C1 pass`.

## §6 Residual risk and verification gaps

- I did not measure the five §C1 controls as frozen artefacts (`claims/*.txt` for controls 1-4 do not
  exist in the wave dir at the time of writing; only `c1-before.txt` and `c2-before.txt` are there).
  My `fx1`/`fx2`/`fx8`/`fxC` runs show that a *stronger* control family than the one frozen passes,
  which is sufficient to reject the predicate but does not substitute for the frozen receipts.
- `prose` readings are judgements; I falsified the three that the receipt depends on by quoting the
  rows, and I left the other sixteen as recorded. A wrong `prose` on a present row (row says ABSENT,
  target resolves) is undetectable by construction (F3).
- Fixtures ran without `.git` (`git archive` extraction), so their `REV` is `unknown`; the freeze
  clone run carries the revision.
- I did not review C2 or the round-50 D1/D3/D5/D7 routed defects — out of this item.
- The instrument is unchanged between `e07f131` and `4090c3db`, so nothing here is a stale reading of
  a moved file.

VERDICT: FAIL — the frozen predicate is not faithful to its own sentence. `DRIFT` never reads
`PROVINCE.md` (F1), and the predicate passes a document in which every row declares ABSENT while
every surface resolves (F3), a landing that deletes three declared surface rows instead of dating
them (F2, `rows=6`), a duplicate entry double-covering one row (F4), and a zero floor (F5); `REV`
misreports the measured revision (F7) and `--lane` does not select the probed tree (F6). C1 must not
be scored on this counter until `DRIFT` is computed from the row text, the row-count floor and the
floor constant are enforced inside the instrument, and `REV`/probe resolution are bound to the
measured tree.

REV e07f131cf7037e58a21db6e1f3986cf401ad257c
