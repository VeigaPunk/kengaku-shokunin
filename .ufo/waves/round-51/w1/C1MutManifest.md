# C1MutManifest — round 51, wave 1 (mutation tester, C1 surface manifest)

Seat: `C1MutManifest`. Item: mutate `plans/round51-surfaces.json` in scratch — (1) flip SF01 `state`
to `present`, (2) set SF14 `count_claim` to 170, (3) move SF11's `section` to `## Surfaces`,
(4) duplicate an anchor string, (5) point SF16's port at 8793 — run the frozen counter for each,
record the exact legs that fire, and report which mutations the current predicate does **not** catch.

## Axes named

- **A1 — manifest-truth detection**: does the frozen predicate kill a manifest that lies about a
  probed surface? (exit code, not just a counter delta.)
- **A2 — leg attribution**: which leg fires, and does the firing leg name the *right* artifact — the
  manifest field, the document row, or a proxy that happens to be adjacent?
- **A3 — survival on a passing baseline**: the C1 after-target is `PREDICATE R51-C1 pass`, exit 0. A
  mutation masked only by the before-tip's pre-existing failures is not "caught" by the predicate; it
  is caught by the baseline. Every mutation that produced no new leg at the red baseline was therefore
  replayed on a *clean* baseline that prints `pass` (probes C0–C4), so "survived" means "exit 0".

## Revision measured

`REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7` (lane `master`).

Manifest/claims identity vs the stage-1 freeze commit
`e07f131cf7037e58a21db6e1f3986cf401ad257c`:

```sh
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff --stat \
  e07f131cf7037e58a21db6e1f3986cf401ad257c..HEAD -- plans/ PROVINCE.md corpus/routed-findings.jsonl
# (empty output)
```

So the mutated bytes are the frozen bytes. Pristine hashes measured in the scratch clone:

```
60d05a0a3f5b099061a902fac7612cd178c8dda01680ac04b84611a77fcf2dd8  plans/round51-surfaces.json
5e00336ff4ce2edb79346c4021e5bec24e5a6490ef5ccc53bd81fe5b6f7a5298  PROVINCE.md
edf09db7be767a29bac4a645185f2f87452ec1451322d9e723ca65111f53e01e  plans/round51_surfaces.py
```

The lane's own copies hash to the same three values after the probe, and
`git status --porcelain plans/ PROVINCE.md corpus/routed-findings.jsonl` in the lane is empty.

## Commands

```sh
S=/fast/scratch/hyaku/kengaku-r51/C1MutManifest
mkdir -p "$S"; export TMPDIR="$S"
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" rev-parse --show-toplevel    # /fast/scratch/hyaku/kengaku-r51/C1MutManifest/lane
cd "$S/lane"
python3 plans/round51_surfaces.py --lane .            # baseline
python3 "$S/mutate.py"                                # M1-M5 on the real baseline
python3 "$S/mutate2.py"                               # M4b + clean-baseline replays C0,C2,C3,C4
python3 "$S/mutate3.py"                               # M5 on the real baseline (part 1 aborted at M4b)
ss -ltn | grep -E ':(8791|8793)\b'
```

Every mutation ran with cwd = the scratch clone root, so the detector is the frozen command with only
manifest/PROVINCE bytes swapped. Pristine bytes were held in memory and rewritten after every run; the
driver asserts `sha256(restored) == sha256(pristine)` before starting the next mutation.

Socket state at measurement (relevant to M5):

```
LISTEN 0      512        127.0.0.1:8793       0.0.0.0:*
LISTEN 0      512        127.0.0.1:8791       0.0.0.0:*
```

## Baseline (pristine, no mutation)

```sh
python3 plans/round51_surfaces.py --lane .
```

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
MANIFEST plans/round51-surfaces.json entries=19 sections=2
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
  DETAIL DRIFT SF01 prose=present state=absent (the row's first path cell asserts the wiki tree resolves; round-15/25 rows alrea)
  DETAIL DRIFT SF02 prose=present state=absent (the row asserts the relocated battery resolves at the archive path)
  DETAIL DRIFT SF03 prose=present state=absent (the row declares a live served model endpoint)
STALE 0
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
EXIT=1
```

This reproduces `.ufo/waves/round-51/claims/c1-before.txt` line for line. The baseline is red, which
is exactly why A3 exists: at a red baseline, "the run still exits 1" proves nothing about a mutation.

## Mutant table

| # | mutation | mutant sha256 | new legs on real baseline | exit | clean-baseline replay | verdict |
|---|---|---|---|---|---|---|
| M1 | SF01 `state` → `present` | man `2066e5bbdd6c3692d069ccc95b147eced8ccfaf139949d798df3cf16d2569dad` | `STALE 0→1` (SF01), **`DRIFT 3→2`** | 1 | C4: `DRIFT 1` + `STALE 1`, exit 1 | **killed** (STALE) |
| M2 | SF14 `count_claim` → 170 | man `32a379ea541114b6c168054adf7a3a75c6288aad652823d9240a6efc48cc7688` | `NUMBER-DRIFT 1→0`, nothing added | 1 (baseline only) | C0: `PREDICATE pass`, exit **0** | **SURVIVED** |
| M3 | SF11 `section` → `## Surfaces` | man `3a5280536a6ee54847574b1e861dfeccfd237faf7ddb77a1089d970d780ac34b` | `ANCHOR-MISSING 0→1` (SF11), `UNCOVERED 0→1` (Core line 109) | 1 | — | **killed** (2 legs) |
| M4a | duplicate an **entry** (SF07 → SF07-DUP, same section, same anchor) | man `34e68a7574f74ae0dc9d190dec5e1ec5248229d5def29d614f8dd51cc34bb3c1` | **none**; `PROBES 19→20`, `present 13→14` | 1 (baseline only) | C2: `PREDICATE pass`, exit **0**, `present=14` | **SURVIVED** |
| M4b | duplicate an **anchor string** in the document (SF16 row twice) | prov `797772af4a73e1b1665934bfceee554a2b031566c840295469b41b75c3f42cf5` | `ANCHOR-DUP 0→1` (SF16 ×2), `UNCOVERED 0→2` (lines 114, 115) | 1 | — | **killed** (2 legs) |
| M5 | SF16 probe `port` → 8793 | man `33f8115fb5c1c5a53878b342381c821a226208f07a794179b0b74a18b7bb384e` | **none — stdout identical to baseline** | 1 (baseline only) | C3: `PREDICATE pass`, exit **0** | **SURVIVED** |

"duplicate an anchor string" has two readings; both are measured (M4a entry-level, M4b document-level)
because they land on opposite sides of the predicate.

## Per-mutant evidence (verbatim leg output)

### M1 — SF01 `state` `absent` → `present`

```
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 2
  DETAIL DRIFT SF02 prose=present state=absent (the row asserts the relocated battery resolves at the archive path)
  DETAIL DRIFT SF03 prose=present state=absent (the row declares a live served model endpoint)
STALE 1
  DETAIL STALE SF01 probe=absent state=present (missing: ~/Projects/webzites/repos/llm-wiki)
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
```

The leg that fires is `STALE` and it names the right artifact (`probe=absent state=present`). Note the
side effect: `DRIFT` falls 3 → 2, because `DRIFT` is `prose != state` and the lie makes the two agree.
The mutation is killed, but a progress reading of "DRIFT 3 → 2" after such an edit is a lie, not
progress.

### M2 — SF14 `count_claim` 25 → 170

```
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
  DETAIL DRIFT SF01 prose=present state=absent (the row's first path cell asserts the wiki tree resolves; round-15/25 rows alrea)
  DETAIL DRIFT SF02 prose=present state=absent (the row asserts the relocated battery resolves at the archive path)
  DETAIL DRIFT SF03 prose=present state=absent (the row declares a live served model endpoint)
STALE 0
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 0
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
```

`NUMBER-DRIFT` goes 1 → 0 and **nothing else changes**. The exit stays 1 only because DRIFT/UNVERDICTED
were already red. On a clean baseline (C0, below) the same edit prints `pass`, exit 0, while
`PROVINCE.md` line 112 still reads `present; 25 rows, …` and line 119 still reads `holds 37 after round
25`. Neither number is 170.

### M3 — SF11 `section` `### Core` → `## Surfaces`

```
ANCHORS total=19 dup=0 missing=1
ROWS section="## Surfaces" rows=9 entries=10 uncovered=0
ROWS section="### Core" rows=10 entries=9 uncovered=1
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
  DETAIL DRIFT SF01 prose=present state=absent (the row's first path cell asserts the wiki tree resolves; round-15/25 rows alrea)
  DETAIL DRIFT SF02 prose=present state=absent (the row asserts the relocated battery resolves at the archive path)
  DETAIL DRIFT SF03 prose=present state=absent (the row declares a live served model endpoint)
STALE 0
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
ANCHOR-DUP 0
ANCHOR-MISSING 1
  DETAIL ANCHOR-MISSING SF11 anchor not found: | Own probe artifacts | `for d in round8-horizon 
UNCOVERED 1
  DETAIL UNCOVERED ### Core row line 109 has no manifest entry
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
```

Killed by two legs that name both sides of the misplacement: the entry has no row in its new section,
and the row has no entry in its old section. Exact line attribution: `### Core` line 109.

### M4a — duplicate an entry (SF07 copied to `SF07-DUP`, same `section`, same `anchor`)

```
ANCHORS total=20 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=10 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=20 present=14 absent=6 errors=0
DRIFT 3
  DETAIL DRIFT SF01 prose=present state=absent (the row's first path cell asserts the wiki tree resolves; round-15/25 rows alrea)
  DETAIL DRIFT SF02 prose=present state=absent (the row asserts the relocated battery resolves at the archive path)
  DETAIL DRIFT SF03 prose=present state=absent (the row declares a live served model endpoint)
STALE 0
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=14 floor=13 verdict=met
PREDICATE R51-C1 fail
```

Every leg is unchanged. `ANCHOR-DUP` stays 0 (it counts an anchor matching more than one **row**, not
two entries sharing an anchor), `UNCOVERED` stays 0 (coverage is `row_idx - used` on **sets**, and the
duplicate collapses into the row it already covered), and `RESOLVE` rises 13 → 14 because `present`
counts entries, not rows. Exit is 1 only from the pre-existing failures.

### M4b — duplicate an anchor string in `PROVINCE.md` (SF16 row twice)

```
ANCHORS total=19 dup=1 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=11 entries=10 uncovered=2
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
  DETAIL DRIFT SF01 prose=present state=absent (the row's first path cell asserts the wiki tree resolves; round-15/25 rows alrea)
  DETAIL DRIFT SF02 prose=present state=absent (the row asserts the relocated battery resolves at the archive path)
  DETAIL DRIFT SF03 prose=present state=absent (the row declares a live served model endpoint)
STALE 0
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
ANCHOR-DUP 1
  DETAIL ANCHOR-DUP SF16 anchor appears 2 times
ANCHOR-MISSING 0
UNCOVERED 2
  DETAIL UNCOVERED ### Core row line 114 has no manifest entry
  DETAIL UNCOVERED ### Core row line 115 has no manifest entry
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
```

Killed. Mechanism worth recording: an entry with >1 anchor hit is dropped from `anchor_line`
altogether (only the `else` branch records it), so one duplicated row costs three legs at once
(`ANCHOR-DUP 1` + both rows uncovered). Noisy, but safe.

### M5 — SF16 probe `port` 8791 → 8793 (real baseline)

```
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
  DETAIL DRIFT SF01 prose=present state=absent (the row's first path cell asserts the wiki tree resolves; round-15/25 rows alrea)
  DETAIL DRIFT SF02 prose=present state=absent (the row asserts the relocated battery resolves at the archive path)
  DETAIL DRIFT SF03 prose=present state=absent (the row declares a live served model endpoint)
STALE 0
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
```

Byte-identical to the baseline. The probe returned `present` on 8793 (STALE 0, `present=13` unchanged),
so the row's claim — anchor `` `ss -ltn 'sport = :8791'` ``, result cell `LISTEN on 127.0.0.1:8791
(ds-flash-shim, read-only shim; :8793 not probed this round)` — is now "verified" against a socket the
row explicitly disclaims.

## Clean-baseline replays (A3)

`C0` is a synthetic passing state built in scratch from manifest fields plus one dated marker — SF01/02/03
`prose` → `absent`, SF14 `count_claim` → 170, `ABSENT 2026-10-28` appended to the SF04 row. **The
document's own numbers were left untouched** (line 112 still says 25, line 119 still says 37). It exists
only to give the mutations a green floor.

### C0 — clean baseline, no mutation (man `0948af3fa68f9cbd28e26baba6b85e3f0dff2d132807637a3c33c83ea3954890`)

```
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 0
STALE 0
UNVERDICTED 0
NUMBER-DRIFT 0
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 pass
EXIT=0
```

**The pass state is reachable with `PROVINCE.md`'s asserted counts uncorrected.** That is the direct
evidence for finding F1.

### C2 — clean baseline + duplicated entry (man `4f6f2ac008bde612cc0a01ee0de7ee57bcebfa7ab9c8092e6a9b81b4c0f0fb18`)

```
ANCHORS total=20 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=10 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=20 present=14 absent=6 errors=0
DRIFT 0
STALE 0
UNVERDICTED 0
NUMBER-DRIFT 0
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=14 floor=13 verdict=met
PREDICATE R51-C1 pass
EXIT=0
```

20 entries against 19 document rows, and the predicate passes with an inflated resolve count.

### C3 — clean baseline + SF16 port 8793 (man `716eab9e5d7b8c381279a63eb4b92324a2c5ad21dad1b4ce6ba4ccc3cb63c78b`)

```
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 0
STALE 0
UNVERDICTED 0
NUMBER-DRIFT 0
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 pass
EXIT=0
```

### C4 — clean baseline + SF01 `state` → `present` (man `c3af0b32043010a307d985aca60a7c193af7f00b4243b370273880d9c6bd1b12`)

```
DRIFT 1
  DETAIL DRIFT SF01 prose=absent state=present (the row's first path cell asserts the wiki tree resolves; round-15/25 rows alrea)
STALE 1
  DETAIL STALE SF01 probe=absent state=present (missing: ~/Projects/webzites/repos/llm-wiki)
UNVERDICTED 0
NUMBER-DRIFT 0
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
EXIT=0 → 1
```

On a green floor the lie is killed twice over (`DRIFT` and `STALE`), because `prose` is `absent` there.
That is the correct behaviour and it confirms M1 is not a hole.

## Findings

**F1 — M2 survives: `NUMBER-DRIFT` compares the manifest to the probe, never the document to the probe.**
The counter has three artifacts for a count — the row's prose number, the entry's `count_claim`, and the
probe — and exactly **one** comparison (`count_claim` vs probe). For `state` the same three artifacts get
**two** comparisons (`prose` vs `state`, `state` vs probe), which is why M1 is sound and M2 is not. C0
proves the consequence: `PREDICATE R51-C1 pass` with `PROVINCE.md` still asserting 25 (and 37 in the
round-25 correction) against a probed 170. So the C1 after-target's `NUMBER-DRIFT 0` is achievable by
editing one manifest integer and leaving the document wrong — it is not evidence that the surface
description became true. Two ways out for the L1, both cheap: (a) require the row's own number to equal
the probe (`re.search(r"(\d+)\s+rows", row_line)` against `count_claim`), which conflicts with the
append-only "date it, do not edit it" landing rule and therefore needs a claims-file amendment; or
(b) keep the manifest-only comparison but stop presenting `NUMBER-DRIFT` as document truth — the claims
file's `Predicate` clause already says "every `count_claim` equals the probed count", while its `Before`
narrative reads as if the counter had caught the document. The predicate text and the axis sentence
("every surface `PROVINCE.md` declares is machine-checked") do not currently say the same thing.

**F2 — M4a survives: entry duplication is invisible and inflates `RESOLVE`.** `ANCHOR-DUP` is a
document-level leg (one anchor matching several rows); it never sees two entries sharing an anchor.
Coverage is a set difference, so a duplicate entry collapses onto a row that is already covered, and
`UNCOVERED` stays 0. `present` counts **entries**, so the duplicate raises `RESOLVE observed_present`
13 → 14 (C2). The claims file's kill rule protects the document side (`ROWS` per section must not fall
below 9/10) but nothing protects the entry side: `ANCHORS total` is printed and never compared to the
row total. A lander could satisfy "coverage 19/19 plus one new declared surface" by duplicating an entry
and never declaring a new surface. One-line leg: fail when `len(entries) != sum(rows per section)`, or
fail when two entries share `(section, anchor)`.

**F3 — M5 survives: the probe target is a free parameter.** `probe()` reads `port` from the entry and
nothing ties it to the row. The row names `:8791` twice (in the anchor's `sport = :8791` and in the
result cell) and explicitly disclaims `:8793`; the mutant probes `:8793`, gets `LISTEN`, and the row
counts as verified. This is not a theoretical mutant: any live socket on the host (a sibling service, a
dev server) makes the row "present" while `:8791` may be gone. Survival here is conditional on the
substituted port listening — which is exactly the condition under which the row's claim is unchecked.
Same shape applies to `paths` entries (the probe's `targets` need not be the path the row's first cell
names) and to `sha256` pins. One-line leg: compare the first `:(\d+)` in `anchor` to `probe.port`, and
the first backticked path in the row to `probe.targets[0]`.

**F4 — M1 is caught, but its `DRIFT` count moves the wrong way.** Flipping `state` to the prose value
silences `DRIFT` for that entry and moves the signal to `STALE` (3 → 2 drift, 0 → 1 stale). The
predicate is still sound — a pass implies `state == probe` and `prose == state`, hence `prose == probe`,
and C4 confirms it on a green floor — but `DRIFT` alone is not a progress metric: it decreases when the
manifest is falsified. Anyone reporting "DRIFT 3 → 0" as evidence of repair should be required to report
`STALE` alongside it.

**F5 — M3 and M4b are correctly killed with precise attribution.** M3 costs two legs that name both
sides of the move (`ANCHOR-MISSING SF11`, `UNCOVERED ### Core row line 109`); M4b costs `ANCHOR-DUP
SF16 anchor appears 2 times` plus both duplicated rows uncovered. Both fail closed. No change needed.

## Restoration

Pristine bytes were restored after every run and asserted byte-identical before the next mutation
began; the driver printed `restored OK` with the pristine hashes each time, and the final hashes equal
the initial ones:

```
FINAL manifest sha256 60d05a0a3f5b099061a902fac7612cd178c8dda01680ac04b84611a77fcf2dd8
FINAL province sha256 5e00336ff4ce2edb79346c4021e5bec24e5a6490ef5ccc53bd81fe5b6f7a5298
```

`git -C <clone> status --porcelain` is empty after the series. The lane tree was never written to: its
three files hash to the values above, and `git status --porcelain plans/ PROVINCE.md
corpus/routed-findings.jsonl` in the lane is empty. All mutants lived under
`/fast/scratch/hyaku/kengaku-r51/C1MutManifest/`, which was removed after this evidence was transcribed.

## Limits

- **M5's survival is conditional on the substituted port listening.** Both 8791 and 8793 were `LISTEN`
  at measurement (`ss` output above). Had 8793 been closed, the real-baseline run would have shown
  `STALE 1` — but that would be the *baseline's* port state being probed, not the mutation being
  detected, since no leg compares the probe's port to the row's. C3 (clean floor, exit 0) is the
  decisive arm: the port is never compared.
- **C0/C2/C3/C4 are synthetic.** They are a scratch-built passing state (`prose` fixed for SF01–03,
  SF04 row dated, `count_claim` 170), not the L1's landing edit, and I am not proposing them as one.
  Their only job is to give A3 a green floor. C0's significance is that it passes while
  `PROVINCE.md`'s asserted numbers are untouched.
- `--selftest` was not exercised by this seat (C1MutCounter owns the counter-side mutation arm); I
  mutated the *data*, not the instrument. The five controls named in the claims file
  (declare-all-absent, drop-one-entry, stale-pin, undated-absence, do-nothing) were not re-run here.
- `prose` truth is out of scope: this seat assumes the recorded readings and asks only whether the
  predicate can tell a true manifest from a false one.
- Probes are point-in-time (`port` 1.5 s, `http` 3 s); `present=13 absent=6` matched the frozen receipt
  on every run, so nothing flapped.
- No model endpoint was used and no route/model alias is recorded; the work is pure stdlib + sockets.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7

VERDICT: 3 of the 5 named mutations are killed by the frozen predicate (M1 by `STALE` — though `DRIFT`
falls as it fires; M3 by `ANCHOR-MISSING` + `UNCOVERED`; M4b by `ANCHOR-DUP` + `UNCOVERED`), and 3 of the
6 probes survive on a clean floor at exit 0: **M2** (`count_claim` → 170 passes while `PROVINCE.md` still
asserts 25 and 37 — `NUMBER-DRIFT` never reads the row), **M4a** (duplicating an entry fires no leg and
inflates `RESOLVE` 13 → 14 — no `entries == rows` leg), and **M5** (pointing the probe at :8793 passes
while the row names :8791 — the probe target is never cross-checked against the row). The predicate is
sound for `state` (three artifacts, two comparisons) and unsound for counts, entries and probe targets
(three artifacts, one or zero comparisons); the C1 after-target's `NUMBER-DRIFT 0` is therefore not, by
itself, evidence that the document became true.
