# R30FxC1Counter — can C1's counter be satisfied without the claimed work?

Seat: `L1Kengaku30.R30FxC1Counter-3` (falsify wave, leaf). Lane: `kengaku-shokunin`. Date (UTC): **2026-10-25**.
Scratch: `/tmp/r30fx-c1counter/`. Lane writes: this file only. Installed/upgraded: **nothing**
(`python3` 3.14.8, `gawk`, `grep`, `sha256sum` already on PATH; PACMAN not used).

Item: `plans/adoption_check.py` (sha256 `cb6fc038481b6462e7eb3bace6761033ffda88fc52669960348936b721b93af2`,
tracked, last touched by commit `4b82ff7`; `git diff` empty — the round-29 tool is byte-identical, as C1 claims)
against C1's frozen predicate (`plans/round-30-claims.md:27-40`).

Method: every construction below lives in `/tmp`; the lane was read, never written. Where a run needed
modified bytes I copied `corpus/`, `plans/adoption_check.py` and the **frozen** expect file into a fake
fleet root. The expect file in the passing runs is the lane's own bytes, unmodified:
`sha256=6ac80746e0074680ad6a469b5ae3f61c1473bcafc720f26e7e1558b0ed35103b` (`cmp` clean against
`.ufo/waves/round-30/adoption-expect.json`).

`VERDICT:` line deliberately **not** emitted: my item is neither a source re-read nor the complete-set
review, and a PASS/FAIL verdict on `corpus/knowledge/contamination-transparency-card.md` from a seat that
only ran the counter would be an unrun check asserted as a result. `plans/gate_timing_check.py` would
(correctly) reject this report as a Gate second-seat return for that reason. The verdict below is about
the **counter**, and is labelled so it cannot be read as one.

---

## 0. Baseline: the claim's command on the lane as it stands

```
$ cd kengaku-shokunin && python3 plans/adoption_check.py \
    --expect .ufo/waves/round-30/adoption-expect.json --census
entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok
EXIT=0
```

That matches C1's frozen line character for character. The landed entry is 170 lines / 15 779 B; the six
registry rows are 6 043 B of `corpus/SOURCES.md`. The question is what that line costs to print.

Self-run control (mine, not the committed file): real corpus tree, entry deleted, its README index row
deleted → `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=1 census=fail`, **exit 1**.
`usedby_ok=1` because the registry still names the (now absent) path; census E11 catches the dangling
`used-by` and fails. The committed `claims/control-nothing.txt` (`entries=0 indexed=0 … usedby_ok=0
census=ok`, exit 1) is a different pre-append shape — pre-append registry, so no dangling path. Both exit 1.
The do-nothing round is genuinely killed; nothing below disputes that.

---

## 1. The cheapest junk that meets the counter — run and exit code

Fake fleet root `/tmp/r30fx-c1counter/final/`, lane `junk-shokunin/`. Three fabricated corpus files, a
10-byte conf, and the lane's unmodified expect file:

```
$ cat corpus/knowledge/contamination-transparency-card.md        # 102 B, 7 lines
source: S081
source: S082
source: S083
source: S084
source: S085
source: S086
verified-at: 2026-10-25

$ cat corpus/README.md                                           # 57 B, one line, no table
| `knowledge/contamination-transparency-card.md` | | | |

$ cat corpus/SOURCES.md                                          # 862 B
# SOURCES
## Registry
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S081 |  | docs | B |  |  |  | mined | 2024-01-01 | 90d | corpus/knowledge/contamination-transparency-card.md |
| S082 | x | docs | B | x | x | x | mined | 2024-01-01 | 90d | corpus/knowledge/contamination-transparency-card.md |
   … S083–S086 identical to S082 …

$ cat ../shokunin.conf                                           # 10 B
LANES="
"

$ sha256sum .ufo/waves/round-30/adoption-expect.json             # the lane's file, copied verbatim
6ac80746e0074680ad6a469b5ae3f61c1473bcafc720f26e7e1558b0ed35103b

$ cd /tmp/r30fx-c1counter/final/junk-shokunin && python3 plans/adoption_check.py \
    --expect .ufo/waves/round-30/adoption-expect.json --census
entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok
EXIT=0
```

**1 031 bytes of fabrication prints C1's frozen pass line and exits 0**, with
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /tmp/r30fx-c1counter/final junk`
returning `junk unlisted …` then `junk ok …`, exit 0. The entry has no URL, no locator, no quote, no
claim, no card gate, no field mapping, no `## Extends`, no attribution — and no occurrence of the string
"contamination".

### 1a. Sharper: the real registry, the real fleet-shaped tree, a 159-byte corpus delta

Copy of the lane's full `corpus/` into `/tmp/r30fx-c1counter/realreg/stub-shokunin/`, then only two files
touched: the entry replaced by the 7-line stub (15 779 B → 102 B) and `corpus/README.md` replaced by one
57-byte line (56 063 B → 57 B — no TOC, no coverage map, no Frontier list):

```
$ cmp corpus/SOURCES.md kengaku-shokunin/corpus/SOURCES.md   && echo identical
identical
$ python3 plans/adoption_check.py --expect .ufo/waves/round-30/adoption-expect.json --census
entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok
EXIT=0
```

The six real rows (quotes, locators, `opened=2026-10-25`, `used-by`) do the entire job. Cost of admission as
the counter measures it: **159 bytes of corpus bytes, whatever they say**.

### 1b. Cited ids need not be the claim's ids

Same real-registry tree, entry rewritten to cite six *other* fabricated rows (`S011`–`S016`, blank cells),
the claim's six rows left uncited and untouched:

```
entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok
EXIT=0
$ grep -c "S08[1-6]" corpus/knowledge/contamination-transparency-card.md
0
```

`rows_present`/`rows_mined` are computed over the *cited* set; `usedby_ok` over `entry["sources"]`. Two
disjoint six-row sets can satisfy the two halves. **The entry never names S081–S086 and the counter
cannot tell.**

### 1c. Remaining unenforced clauses, each executed

| # | construction | printed line | exit |
|---|---|---|---|
| a | all six rows `opened=1900-01-01` | `… rows_mined=6 usedby_ok=1 census=ok` | 0 |
| b | all six rows `opened=2024-01-01` (junk fleet) | same | 0 |
| c | expect `sources` = `[S081,S081,S082,S083,S084,S085]` (5 distinct) | `cited_rows=6 … usedby_ok=1 census=ok` | 0 |
| d | two identical index rows in README | `indexed=1` | 0 |
| e | `source: S081 # "a fabricated quote that no fetch contains"` | `cited_rows=6` | 0 |
| f | all six `source:` lines *and* the index row inside a ``` fenced block | `entries=1 indexed=1 …` | 0 |
| g | lane not in `shokunin.conf` at all (empty `LANES=`), conf 10 B | `census=ok` (census says `unlisted` + `ok`) | 0 |
| h | §1 junk with the conf deleted | `census=fail` | 1 |

(h) is the only environment requirement the census leg imposes: `/tmp/.../shokunin.conf` must exist beside
the lane. (g) shows it need not register the lane, and `census=ok` is a statement about the tree sitting
next to the copy, never about the real fleet.

---

## 2. Calibration — what the counter *does* catch (so the verdict is not over-read)

Single-cell mutants on the §1 tree, one at a time:

| mutant | printed line | exit | caught by |
|---|---|---|---|
| one cited row `status=queued` | `rows_mined=5` | 1 | cell 7 |
| one row `opened=2027-01-01` | `census=fail` | 1 | census E08 (future only) |
| one row `used-by=—` | `usedby_ok=0` | 1 | per-row used-by |
| `verified-at` line removed | … `usedby_ok=1 census=ok` | 1 | `verified_at_ok` |
| seventh `source:` id added | `cited_rows=7` | 1 | exact count |
| entry file deleted | `entries=0` | 1 | presence |
| `--census` omitted | `census=skipped` | 1 | `args.census` |
| empty `entries` | `empty expectation is not a pass` | 1 | guard |

So the seven printed fields are real, monotone, and do kill the do-nothing and partially-done round. The
defect is not that the counter is weak on plumbing; it is that C1's predicate sentence asserts more than
that plumbing.

---

## 3. What the counter cannot see (each with the run above that proves it)

1. **Any content of the entry.** §1: 102-byte stub with zero body passes. No claim, gate, mapping,
   attribution, falsifier, `## Rejected`, `## Corrections`, `## Extends` is read.
2. **The amendment relation — C1's stated reason for the flip.** Nothing checks that the entry names
   `corpus/knowledge/contamination-detection-and-transparency.md` or the round-6 union table. §1 removes
   the word "amendment" entirely and still passes. The claim's surface ("admitted as an amendment that
   names the lane entry it extends, not as a rival design") has no counted form.
3. **The Frontier bullet move and the coverage-map row — the axis surface.** §1a deletes all 56 KB of
   `corpus/README.md` down to 57 bytes (zero Frontier lines, zero coverage rows) and `indexed=1`. The
   counter's only README read is one anchored index-row regex.
4. **Identity of the six ids.** §1b: entry cites `S011`–`S016`; `cited_rows=6 rows_present=6 rows_mined=6`
   and `grep -c S08[1-6]` = 0. The code compares a *count*, never a set, against `entry["sources"]`.
5. **Distinctness of the six.** §1c: `expect.sources` with `S081` twice passes; the frozen "six distinct"
   clause is not implemented even in the file the counter trusts.
6. **`opened=2026-10-25`.** Never read (`grep -n opened plans/adoption_check.py` → no match). §1a–§1c use
   `2024-01-01`; `1900-01-01` also passes. Census E08 only rejects *future* dates, so the round's
   "opened this round" claim — the freshness half of a coverage delta — is unverified in the counted path.
7. **Quote presence, locators, word caps, and the kill rule.** `anchor`, `source`, `scope`, `teaches` cells
   are never read (§1 blank cells pass). The six `source:` lines carry no URL, no locator and no quotation
   (§1e puts a *fabricated* quote in a trailing comment, §1f hides the lines in a fenced block). C1's kill
   rule ("a cited source whose located quote cannot be found in this round's own fetch is refused"; "fewer
   than four of the six survive → honest stop") has **no code path** in the counting command, and the
   round's fetch artifacts are not committed (`corpus/evidence/round30/` holds counter outputs only).
8. **Row identity.** Fabricated rows may carry an empty `source` cell and no URL at all (§1). Census E04
   compares URLs only when a URL exists, so a registry made of unidentifiable rows passes the census leg.
9. **That the index row is a table line, or that there is exactly one.** §1d (two rows), §1f (fenced code
   block) both pass, contradicting the code's own comment "anchored: an index row is a table line, not a
   mention inside a comment".
10. **That the lane is the lane.** §1g: an unregistered `junk-shokunin` in a fabricated `/tmp` root with a
    10-byte conf prints `census=ok`. `census=ok` binds the copy to its own sibling conf, not to
    `shokunin.conf`'s `kengaku` row or to the fleet.
11. **Novelty.** "the entry is new corpus bytes on ground the lane did not hold" (C1's axis verdict) — no
    check reads any other knowledge file, no overlap measure exists.
12. **That the bytes are committed.** The script's own docstring claims it "re-derive[s] … landed state
    from committed bytes" and "reads only committed corpus files". It never invokes git; it reads the
    worktree. The landed entry is `?? corpus/knowledge/contamination-transparency-card.md` in
    `git status` right now, and the baseline run above passes on it. Worktree bytes suffice, so "landed"
    in the counter's sense means "present in a directory".

---

## 4. Prior art in this wave (calibration, not credit)

`build/R30CritC1.md` already argued, with probes, the core of items 1, 4, 6, 7, 11 and the freeze gap
(its B1–B6, Attack 3). My additions on top of it, each independently run above: the *fully fabricated*
registry with blank cells and no URLs (§1, item 8); a fabricated fleet root with an empty `LANES=` and an
**unregistered** lane still scoring `census=ok` (item 10); total destruction of `corpus/README.md`
(56 063 → 57 B, item 3); `opened=1900-01-01` (item 6, unbounded past rather than a re-dated copy);
duplicate ids *inside the expect file* (item 5); duplicate index rows and fenced-block anchoring (item 9);
and the worktree-vs-committed gap in the counter's own docstring (item 12). The headline result is
therefore **reproduced, not discovered** — which matters, because a falsify wave that books the same
defect twice reads as extra yield it does not have.

---

## 5. Verdict on the claim

**The counting command reproduces exactly; the predicate does not mean what the claim says.** Two clauses
of the frozen sentence have no implementation at all — "citing exactly the six ids S081 … S086 (six
distinct)" (a count is implemented; identity and distinctness are not) and "`opened=2026-10-25`" (nothing
reads cell 8). Three more are implemented at a strictly weaker strength: "exists" means "non-empty file",
"one index row" means "one matching line anywhere, cells free, fenced blocks count", "`used-by` naming the
entry" binds `expect["sources"]`, which need not be the ids the entry cites.

So C1's `same condition in the counter's code` is **false**, and the pass line is reachable for 159 bytes
of corpus delta in the two files the claim says it gates. Two readings are available and only one is
honest:

- as **registry plumbing** (the do-nothing round scores zero; the six rows must exist, be `mined`, and
  name the entry): the counter stands, and C1's landed bytes clear it honestly;
- as **the admission C1's Surface and axis verdict describe** (amendment status, quotes located, Frontier
  bullet moved, freshness this round): the counter is necessary only, and the claim books an `improved`
  coverage trend on a surface the supervisor's counting command cannot see.

Because the claim froze the sentence, not the reading, C1's predicate should **not** be recorded as
meaning what the claim says. Whether C1 itself misses is a separate question that turns on the entry's
content — checked by other seats' prose review, not by this command; this report says nothing about the
entry's quality, and the 4/6 kill-rule survival count belongs to `build/R30CritC1.md` §B5.

**Impacted axes**

- **calibration** — the claim asserts a three-way identity (one sentence / same condition in code / same
  label in the receipt) that the code does not satisfy. A frozen predicate that overstates its counter is
  a calibration defect even when the landing is honest.
- **coverage** — C1's ledger delta rests on this command; the delta is real in the registry but the
  coverage *surface* (README index/coverage/Frontier) is invisible to it, so a regression that dropped the
  frontier edit would score identically.

**Smallest safe correction** (claim-side is cheaper than code-side, and C1 is already frozen):

1. Claim-side, no code: split the predicate sentence into `(a)` the registry predicate the counter
   actually computes, and `(b)` the admission properties established by prose seats (amendment naming,
   quote fidelity, frontier move), and stop asserting `(a) = (b)`. Record the frontier/coverage edits as
   prose evidence, not as a counted field.
2. If the code is to carry the sentence instead, the minimum set that makes §1–§1c fail, all cheap string
   work in `adoption_check.py`: per-entry `set(cited) == set(entry["sources"])` and no duplicate ids;
   `registry[id][8] == access_date` for every expect source; `len(re.findall(index_re, readme)) == 1` with
   the matching line outside a fenced block and its first cell non-empty; and `registry[id][5]` (anchor)
   non-empty and ≠ `—` with at least one quoted span, via the same `sources_adopt.quoted_spans` C3 lands so
   the two gates cannot disagree. (This overlaps `R30CritC1.md` §"Smallest safe correction" 1 — do not
   apply both lists as if they were two fixes.)
3. Environment: have the census leg run `sources-census.sh census --root <fleet> kengaku` (the fleet
   summary) rather than `validate` on `lane.parent`, so `census=ok` cannot be produced by a 10-byte conf in
   `/tmp` (item 10).

---

## 6. What I did not verify

- I did not re-fetch S081–S086; quote fidelity is not my item, and no fetch receipt is consumed by the
  counter either way. `build/R30FxSrcS082.md` and `build/R30CritC1.md` cover source identity.
- I did not exercise `plans/sources_adopt.py`'s `--quote-file/--artifact` CLI (C3's item, and its `main()`
  was being edited while I ran).
- Runs were executed against a copy; if the lane's `corpus/SOURCES.md` or the entry changes after
  `2026-10-25`, the byte counts in §0/§1a shift. The counter's code hash (`cb6fc038…`) and the expect hash
  (`6ac80746…`) pin the half that matters.
