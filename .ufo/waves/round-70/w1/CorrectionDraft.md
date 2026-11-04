# CorrectionDraft — round 70 w1 (scribe; R70-C2 D1–D8)

Seat: `CorrectionDraft-2` (scribe, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
(`L`). Lane tip at seat start `384e9c76`; the L1's C2 corrections were in the working tree while I
read. Snapshot of every quote below: **working tree at 2026-11-04T00:55Z** (local 2026-11-03
21:55), with the per-file sha256s in §0. I wrote no lane file except this report and
`W/CorrectionDraft/`; I did not edit a predicate, case table, vector, digest, kill rule, target,
registry row, lesson, receipt or the gate.

Verdict line: **D1–D4, D6 and D8 are closed and re-derived; D5 lands with a wrong count in its
index row (five vs the lesson's six Mistakes rows); D7 lands with a reason contradicted by the
wave's own S155 capture; the lesson still repeats `line 59` for S243 after A4 corrected the row to
`:61`.** At the snapshot the gate prints `DEFECTS n=0` / `PREDICATE R70-C2 pass` / rc 0; the three
content defects above pass that gate because E5/E7 are presence checks.

## 0. Snapshot and bounds disclosure

| file | sha256 (snapshot) |
|---|---|
| `corpus/SOURCES.md` | `b1acdb73e3d2cfb10fc9cab59ed4ec8b6697a6ae556b1a95d95cc2571015e8f9` |
| `corpus/README.md` | `b4342d69…7f1c47` (00:55Z) → `560ee7df5cab6a2c01d95de8963d16bfa563ffd25afc4ec28f23fe6bcbf52631` (00:58Z) |
| `corpus/knowledge/tb2-nginx-request-logging-offline.md` | `d02a5b3785d72263df88639bffb1e704a53a68ab307114ff0dde4b26f11269c7` |
| `corpus/lessons/round-70.md` | `147dc5e8…f0d8c024` (21:54) → `800663837f3728e5400719c7e4ca20f054bbf195d6b18d6cbd09f7d4a6f86f47` (21:55:47) |
| `plans/round-70-claims.md` | `fce41ef991ace96aebe9fb91c96adb3e2bbeaafc202d7c692df0bc2de4f281b6` (A1–A4) |
| `plans/round70_c2_routed_defects.py` | `367ce58e41799a75b9fd3a9df5ad032c1fe30acc89b7fb4bba32ffb7c35a36fb` |
| `corpus/evidence/round70/c2/depth-gate-provenance.txt` | `b98a951164b00e49714f76610ef17efb002f1a2e70f010ad576802d1ce699d37` |
| `corpus/evidence/round70/gates/trio-nginx.txt` | `01eb853fe42fab456843785368b47de96289fd1dcc8927965312446f9bbe09b2` |
| `corpus/evidence/round70/gates/r69-c2-landing.txt` | `caaf41f1fe1923e9f4895d0ff98d889a8f36bca2a608169fd3c46c3d4b64c989` |

**Post-snapshot drift (the L1 is integrating while the wave runs).** Between 00:55Z and 00:58Z the
L1 added the round-70 row/block to `corpus/README.md`; the round-69 Lesson bullet moved `:789` →
`:790`, and the lesson file was rewritten at 21:55:47 (`80066383…`). Re-checked at 00:58Z: the three
content defects below **persist** — `corpus/README.md:564` and `:790` still say “five Mistakes
rows”; `corpus/lessons/round-70.md:26` still says `Located quote, line 59:`; the S244 note still
says “bytes are not in this lane”. The new round-70 row itself (`README:565`) says “six Mistakes
rows”, so the correct form is already in the file.

Bounds disclosure: for D6 I made a throwaway `git clone --shared` of `L` under
`S=/fast/scratch/hyaku/kengaku-r70/CorrectionDraft`, checked out `4038bb11` there, ran the
round-69 gate, then deleted `S`. No lane/fleet ref, index or worktree was touched; no commit,
push or identity was used anywhere. The clone/checkout is the same provenance the D6 receipt
records (`git clone --shared <lane> <scratch>; git -C <scratch> checkout 4038bb11`). Tooling: none
installed; no subagent (leaf).

## 1. What I ran (commands + rc)

| # | command | rc | observation |
|---|---|---|---|
| 1 | `bash scripts/hyaku/jj-lane.sh state kengaku-shokunin`; `git -C L rev-parse master` | 0 | `local=384e9c76…`, `head=detached`, 5 modified + 4 untracked at seat start |
| 2 | `sha256sum .ufo/waves/round-69/w1/gates/depth-gate.txt corpus/evidence/round69/gates/depth-gate.txt` | 0 | `f683297c…c9d9` / `d65bbda…96e22` — equal to provenance:3–4 |
| 3 | `diff` the two depth-gate files | 1 (one line) | `1c1`: `…paths total=33 resolved=33…` vs `…total=34 resolved=34…` |
| 4 | `python3 plans/round63_gate_checks.py trio corpus/knowledge/tb2-nginx-request-logging-offline.md` | 0 | `TRIO pass corpus/knowledge/tb2-nginx-request-logging-offline.md` (64 B) |
| 5 | `cmp` that output with `corpus/evidence/round70/gates/trio-nginx.txt` | 0 | byte-equal |
| 6 | `git clone --shared L S/lane-4038`; `git -C S/lane-4038 rev-parse --show-toplevel`; `git -C S/lane-4038 checkout 4038bb11`; `cd S/lane-4038 && python3 plans/round69_c2_routed_defects.py` | 0 | toplevel = `S/lane-4038`; HEAD `4038bb11`; `E1..E7 ok`, `DEFECTS n=0`, `PREDICATE R69-C2 pass` |
| 7 | compare that stdout with `r69-c2-landing.txt` lines 8–16 | 0 | **byte-equal** (`OUTPUT-BEGIN` block) |
| 8 | `git show 4038bb11:plans/round69_c2_routed_defects.py \| sha256sum` | 0 | `ea28b006d528a99befdc193c5463ef552b0a15d0b71b03a091ec011fae115485` (same as the working file) |
| 9 | `git show 502893ad:<path>` for S242/S243/S244, README, entry, receipts, lesson | 0 | all six absent/targeted as §2 records (base `grep -c round-69` in README = 0; entry anchor = `instruction.md lines 1-20`) |
| 10 | `python3 plans/round70_c2_routed_defects.py` (L, working tree) | 0 | at **00:51:42Z**: `E1..E8 ok`, `DEFECTS n=0`, `PREDICATE R70-C2 pass` |
| 11 | same after A4's used-by repair (`plans/...py` sha `367ce58e…`) | 0 | at **00:55:34Z**: identical `E1..E8 ok` / `n=0` / pass |
| 12 | registry cell arithmetic (`cells()` logic) on S241–S244 | 0 | 11 cells each; used-by = `c[10]` = entry path (S241/2/3), `—` (S244) |
| 13 | `sed -n '59p;61p' corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py` | 0 | `:59` = `def test_nginx_config_syntax():`; `:61` = the `subprocess.run(["nginx", "-t"], …)` line |
| 14 | `awk '/^## Mistakes/{…}' corpus/lessons/round-69.md \| grep -c '^| \*\*'` | 0 | **6** rows (also 6 at `4038bb11`) |
| 15 | wave receipt checks: `sha256sum`, `cmp .out .dispatch`, `od -c .rc`, `wc -c .stderr`, JSON parse | 0 | see §5 |
| 16 | read `/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/grader-fixture-coverage.md` | 0 | 2869 B, 39 lines, sha `25d6a864…85ed`; **line 1 empty**, `source:` at line 2 |
| 17 | read `W/SourceOpen70/S155-toolathlon-transcript-copy.md` + `SourceOpen70/SHA256SUMS-sourceopen70.txt` | 0 | 7033 B, sha `3b9a4902…42ee`; `instruction.md` 1882 B `26a7ac98…`; `test_outputs.py` 5947 B `045cc716…` |

Receipts copied to `W/CorrectionDraft/`: `trio-fresh.txt`, `r69-gate-4038.out`,
`depth-sha-diff.txt`, `s244-candidate.txt`, `w1-receipts.txt`.

## 2. D1–D5: closing bytes, old → new ledger lines

### D1 — false cross-root byte-identity → **closed** (E1 re-derives it)

Routed at `corpus/lessons/round-69-verifier-spotcheck.md:170` (D1). Old claim, still present in the
round-69 wave notes: `.ufo/waves/round-69/w1/GateReceipts.md:85-89` ("seat before my run and are
byte-identical to my captures:" followed by both paths at `f683297c35998f…`) and
`.ufo/waves/round-69/w1/EvidenceIndex.md:81,83,174-175` ("E7's receipts are already byte-identical
across the two roots… `f683297c…`, 104 B").

Closing bytes — `corpus/evidence/round70/c2/depth-gate-provenance.txt:1-7`:

```
1  TREE-CAPTURE .ufo/waves/round-69/w1/gates/depth-gate.txt PRE-CLASS-ROW
2  LANDING-COPY corpus/evidence/round69/gates/depth-gate.txt
3  SHA .ufo/waves/round-69/w1/gates/depth-gate.txt f683297c35998f66187475daf2f68333f62294fab9356d436cba459c02efc9d9
4  SHA corpus/evidence/round69/gates/depth-gate.txt d65bbbdad6bf722961e27d8800a4ea92a75e5fafd06113a96781ca2d84a96e22
5  LINE-DIFF ROWS n=16 class_match=True count_mismatch=0 paths total=33 resolved=33 share=1.00 -> ROWS n=16 class_match=True count_mismatch=0 paths total=34 resolved=34 share=1.00
6  ADDED-TOKEN corpus/knowledge/tb2-nginx-request-logging-offline.md
7  NOTE … the earlier "byte-identical at f683297c" claim is superseded.
```

**Ledger line a reader needs:** *Depth-gate copies: the wave copy is `PRE-CLASS-ROW` at
`f683297c…` (`paths total=33`); the corpus copy is the landing run at `d65bbda…` (`paths total=34`);
they differ in exactly one line (`33 → 34`), and the added token is
`corpus/knowledge/tb2-nginx-request-logging-offline.md`.* Re-derived by command 2/3 (sha256 + diff
`1c1`). Residual: the old false lines in the round-69 wave notes are superseded only by this new
file; a reader of `GateReceipts.md`/`EvidenceIndex.md` alone still sees them. The frozen E1 asks
for supersession in this file, so this is a named residual, not an open check.

### D2 — “trio gate green” with no receipt → **closed** (E2 re-derives it)

Routed at spot-check `:177` (D2). At `502893ad` the receipt path was absent; the only committed
trio receipts named `tb2-network-service-offline-grader.md`.

Closing bytes — `corpus/evidence/round70/gates/trio-nginx.txt:1` (64 B, sha `01eb853f…09b2`):

```
TRIO pass corpus/knowledge/tb2-nginx-request-logging-offline.md
```

A fresh `plans/round63_gate_checks.py trio …` (command 4) prints exactly these bytes (command 5:
`cmp` → byte-equal). **Ledger line:** *Provenance trio for the nginx entry: `TRIO pass
corpus/knowledge/tb2-nginx-request-logging-offline.md`, committed at
`corpus/evidence/round70/gates/trio-nginx.txt`; re-running the trio command reproduces it byte for
byte.*

### D3 — instruction citation too narrow / unregistered surface → **closed** (E3 re-derives it; used-by arm live after A4)

Routed at spot-check `:181` (D3). At `502893ad`: entry line 1 read `anchor: … instruction.md lines
1-20`; no S242 row existed.

Closing bytes:

- `corpus/knowledge/tb2-nginx-request-logging-offline.md:1` — `… anchor: tests/test_outputs.py
  lines 11-178 (eight legs in file order), instruction.md:6-11,15-18 (S242) — sha256
  045cc716…4acda0`.
- `corpus/SOURCES.md:257` — S242 row: `… instruction.md | docs | A | … | instruction.md:6-11,15-18
  fetched 2026-11-03 HTTP 200, 24 lines, 1882 bytes, sha256
  26a7ac98aced6107f147206790ada77bbf8ed3c25fb360cf323d5fc6889edf99; :16 verbatim: "Welcome to the
  benchmark webserver" | … | mined | 2026-11-03 | 180d | corpus/knowledge/tb2-nginx-request-logging-offline.md |`
  (11 cells; `c[10]` is the entry).
- Entry errata `:55-58` records the anchor change (E-D3).

**Ledger line:** *Entry anchor is `instruction.md:6-11,15-18 (S242)`; S242 registers the
instruction at pin `2fd12b88` with sha256 `26a7ac98…9edf99` and the entry in `used-by`.*

### D4 — S241 summary cell misstates leg 5 → **closed after A4** (E4 re-derives `:61`)

Routed at spot-check `:187` (D4). Old bytes: `corpus/SOURCES.md` S241's **note** cell (cell index 6,
not `teaches`) at base — `legs 2-4 are HTTP-observable and need no nginx; legs 5-6 are file reads;
leg 8 greps the whole log content, so one stale line satisfies it`. (The spot-check attributes the
phrase to `teaches`; it is the note cell — an attribution slip in the route, not in the fix.)

Closing bytes:

- `corpus/SOURCES.md:258` — S243 note: `supersedes S241 — leg 5 is the nginx -t subprocess,
  satisfied by a shim; legs 6-8 read config bytes and a log the server writes, so S241's legs 5-6
  file-read summary is wrong`; evidence cell now `tests/test_outputs.py:61 fetched 2026-11-03,
  sha256 045cc716…; verbatim: result = subprocess.run(["nginx", "-t"], capture_output=True,
  text=True)`; `used-by` = the entry.
- Entry errata `:60-62` (E-D4) now cites `tests/test_outputs.py:61`.

**Ledger line:** *S243 supersedes S241's note cell: leg 5 is `subprocess.run(["nginx","-t"], …)`
at `tests/test_outputs.py:61` (a subprocess a shim satisfies, not a file read); S241's row stays as
written (append-only).* The repair is recorded in `plans/round-70-claims.md` A4 item 2
(`:209-213`). **Open inconsistency:** `corpus/lessons/round-70.md:26` still says `Located quote,
line 59:` — stale against A4 and against the row. Fix the lesson to `:61` before the lesson is the
durable record.

### D5 — corpus index omission → **lands, but its row is wrong** (E5 is presence-only)

Routed at spot-check `:190` (D5). At `502893ad`, `git show 502893ad:corpus/README.md | grep -c
round-69` → `0`; at snapshot `grep -c round-69` → `7`.

Closing bytes:

- `corpus/README.md:564` — the `lessons/round-69.md` index row.
- `corpus/README.md:786` — `## Round-69 supporting artifacts (2026-11-03)` (block `:786-793`).

**Ledger line (as landed is false):** the row and the block's Lesson bullet (`:789` at 00:55Z,
`:790` at 00:58Z after the round-70 block landed) both say **“five Mistakes rows”**, but the
landed lesson has **six** (`awk` over `corpus/lessons/round-69.md` → 6: asserted-coverage;
self-unreadable receipt; spurious-selftest; port-gate refusal; path-dependent digest; misattributed
dirt). Worse, the row's parenthetical names *receipt-from-prose for the new entry's trio* — which is
routed defect D2, not a Mistakes row — and omits *spurious-selftest* and *path-dependent case
digest*. The correct line must read **“six Mistakes rows”** and list the six (or say “five named +
one”). E5 checks only the two substrings (`lessons/round-69.md`, the heading), so it passes the
wrong count. This is a counter-drift recurrence of the class the round-68/69 lessons track.

## 3. (a) D6 — the landing receipt's header lines as they should read

Landed file `corpus/evidence/round70/gates/r69-c2-landing.txt` (684 B, sha `caaf41f1…c989`),
lines 1–6 and 18:

```
1  # R70-C2 E6: the round-69 correction gate's green run at its measured revision
2  # lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin
3  REV 4038bb11
4  FULL 4038bb1150345e11f4c52c8a39ca16cecb9e975a
5  PROVENANCE git clone --shared <lane> <scratch>; git -C <scratch> checkout 4038bb11; HEAD short = 4038bb11
6  COMMAND python3 plans/round69_c2_routed_defects.py
…
18 RC 0
19 DATE 2026-11-03
```

This is the form E6 requires: `REV 4038bb11` + `DEFECTS n=0` + `PREDICATE R69-C2 pass` + `RC 0`
(gate `check_r69_landing`, `plans/round70_c2_routed_defects.py:262-276`). I re-derived it rather
than trusting it: commands 6–8 reproduce the `OUTPUT-BEGIN` block **byte for byte** at a clean
checkout of `4038bb11` (stdout sha256 `724a1e1ac23cba9d9b0b778aef4c9cda37ee2870af39fe03aeec3f88c12dc449`),
`4038bb11` is an ancestor of `master`, and the gate file at that rev is `ea28b006…` (same as the
working copy). The receipt is therefore a reproducible record, not prose.

**Header as it should read (exact; the added two lines are recommended bindings, optional under
E6):**

```
# R70-C2 E6: the round-69 correction gate's green run at its measured revision
# lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin
REV 4038bb11
FULL 4038bb1150345e11f4c52c8a39ca16cecb9e975a
PROVENANCE git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin <scratch>; git -C <scratch> checkout 4038bb11; git -C <scratch> rev-parse --short HEAD -> 4038bb11; cwd = <scratch>
COMMAND python3 plans/round69_c2_routed_defects.py
GATE-SHA256 ea28b006d528a99befdc193c5463ef552b0a15d0b71b03a091ec011fae115485
OUTPUT-BEGIN
… (the nine lines reproduced verbatim) …
OUTPUT-END
OUTPUT-SHA256 724a1e1ac23cba9d9b0b778aef4c9cda37ee2870af39fe03aeec3f88c12dc449
RC 0
DATE 2026-11-03
```

`GATE-SHA256`/`OUTPUT-SHA256` bind the instrument and the exact stdout; both are derivable by a
reader (commands 7–8). The placeholders for the scratch are acceptable — the scratch is ephemeral;
the lane path is literal on line 2 and in the recommended `PROVENANCE` line.

## 4. (b) D7 — the round-70 lesson Gate reject paragraph

Landed state: `corpus/lessons/round-70.md:12` is exactly `## Gate` (required — the gate's
`section()` at `plans/round70_c2_routed_defects.py:84-94` strip-equals the heading, so a
`## Gate (SOURCES contract v1)` heading would report `no-gate-section`). The reject is `:31`, a
single long line, so the gate's lexical test (`"reject"` and `"reason"` on one physical line,
`:289-291`) passes. That test is the whole of E7's lesson arm: it cannot read the reason's truth,
and the landed reason has three factual problems:

1. **“its first line is `source: S155 — …`”** — false. The candidate's line 1 is **empty**; the
   `source:` triad line is `:2` (`nl` on the staging file; 2869 B, 39 lines, sha
   `25d6a864…85ed`). SourceOpen70 §4 records the same numbering.
2. **“whose probe bytes are not in this lane”** — false at lesson-writing time. The transcript is
   now in this wave: `W/SourceOpen70/S155-toolathlon-transcript-copy.md` (7033 B, sha
   `3b9a4902e33f8eafab65cd899a92885d53fe9c41e14061f0c8037c65337642ee`, copied 21:48; the lesson
   mtimes 21:54 and 21:55:47). What is *not* in the lane is the runnable probe:
   `lanes/kengaku/round8/toolathlon-grader-fixture-probe2.py` (the transcript's Run section invokes
   it; `L/lanes` does not exist and `find` finds no such script) and its receipt.
3. **Quote shape** — the “verbatim” fragment drops the backticks around the path (SourceOpen70 F2).

The reject still holds, on grounds that survive all three: Q1 fails on the candidate's own bytes
(triad offset by the leading blank line; `corpus/QUALITY.md:15`), the cited `S155` resolves in this
lane to a different source (`corpus/SOURCES.md:170` is the TB2 password-recovery `solve.sh`), and
the claim is a tier-C `own-work` row that cannot stand alone (Q2, `corpus/QUALITY.md:24`).

**Drafted paragraph (replace `:31`; keep `## Gate` exact and keep `Reject — reason:` on one
physical line):**

```
- **S244 — the `merge/kengaku` package entry `grader-fixture-coverage`. Reject — reason:** the
  entry fails on its own bytes before any transcript is weighed — its triad is offset by a leading
  blank line (`recheck:` at `:4`, not `:3`; `corpus/QUALITY.md:15` Q1) — and its cited `S155`
  resolves in this lane to a different source (`corpus/SOURCES.md:170`, TB2 password-recovery
  `solve.sh`); the cited transcript is now carried in this wave
  (`.ufo/waves/round-70/w1/SourceOpen70/S155-toolathlon-transcript-copy.md`, 7033 B, sha256
  `3b9a4902…42ee`), but its Run section invokes
  `lanes/kengaku/round8/toolathlon-grader-fixture-probe2.py`, a script and receipt this lane does
  not hold, so the tier-A own-work claim (Q2, `corpus/QUALITY.md:24`) is not re-derivable here.
  **Flip:** the probe script and its receipt land in this lane and re-run
  (`plans/…fixture_probe.py` + a receipt), with S244 re-registered against a source id that
  resolves here. **Registry:** `corpus/SOURCES.md:259` (`| S244 | … | rejected | 2026-11-03 | 180d | — |`).
```

If the writer prefers to keep the landed sentence shape, the minimal truthful substitution is:
“whose probe script and receipt are not in this lane (only the transcript is, at
`W/SourceOpen70/S155-toolathlon-transcript-copy.md`, sha256 `3b9a4902…`)”. Either form keeps the
candidate / reason / flip triple LEARNING asks for and the S244 citation.

## 5. (c) D8 — the receipt set the wave should carry

| file | size / sha256 (snapshot) | what it proves |
|---|---|---|
| `.ufo/waves/round-70/w1-spec.json` | 22264 B, `b065b31b…c71e` | the exact input validated: 14 items, `axes=[coverage, calibration]`, `maxLanes=14`, `reportDir=.ufo/waves/round-70/w1`; roles executor 4, reviewer 3, mutation-tester 2, critic 1, scribe 2, scout 1, connector 1 (attack share 6/14 = 42.9 %) |
| `.ufo/waves/round-70/w1-validate.rc` | 2 B, bytes `0\n`, `9a271f2a…86aa` | the validator exited 0 on that spec — the rc round 69 did not commit |
| `.ufo/waves/round-70/w1-validate.out` | 35426 B, `2041c97f…c986` | the rendered dispatch: `schema=ufo-swarm-wave-dispatch-v1`, `counts={spawn:14,resume:0,total:14}`, `taskCall.tasks=14`, and a policy block `{maxLanes:14, minLanes:8, waveMinLanes:8, waveMaxLanes:16, hardCeiling:256}` matching `scripts/hyaku/ufo-wave-policy.json`'s swarm band |
| `.ufo/waves/round-70/w1-validate.stderr` | 0 B, `e3b0c44…b855` | no diagnostics; meaningful only because rc and out exist (round 69's D8 was an empty stderr *alone*) |
| `.ufo/waves/round-70/w1-dispatch.json` | 35426 B, `2041c97f…c986` | **byte-identical to `.out`** (`cmp` rc 0), so the payload dispatched is the payload validated — no hand edit between validation and handoff |
| `.ufo/waves/round-70/w1.ready` | 157 B | the handoff marker: `{"lane":"kengaku","round":70,"wave":"w1","dispatch":"…/w1-dispatch.json","l1":"KengakuR70"}` |
| `.ufo/waves/round-70/w1.ready.dispatched` | 543 B, timestamp `2026-11-03T21:46:23` | the orchestrator took it and mapped 14 seat ids (incl. `CorrectionDraft → CorrectionDraft-2`) |
| *(missing, recommended)* `w1-validate.cmd` | — | the exact validator argv + binary/version; the validator lives outside the lane, so rc/out provenance is otherwise trust-based. One line (`# cmd: …; omp --version …`) closes it. |
| *(at close)* `.ufo/waves/round-70/w1-results.json` | — | 14 settled seats with nonempty output (round-69 shape); not part of E8 |

**Ledger line:** *D8 is closed: the wave carries the spec, `rc=0`, the rendered 14-task dispatch,
an empty stderr, a dispatch file byte-identical to the validator's stdout, and the dispatch
markers — the round-69 “empty stderr with no rc” shape is not repeated.*

## 6. Prose-only / non-re-deriving clauses (flagged, not closed by the gate)

| clause | gate evidence | status |
|---|---|---|
| **D5 row content** | E5 checks only `lessons/round-69.md` and the heading substring (`:247-259`) | **not re-derived**: the row's “five Mistakes rows” is wrong (lesson has six), and its list mixes rows with routed D2. Fix the count/list before the lesson/index is the record. |
| **D7 reason** | E7 checks `reject`+`reason` co-occurrence and two row substrings (`:285-291`) | **not re-derived**: the landed reason's “first line” and “bytes are not in this lane” are false at the snapshot; only a human re-read catches it. Use §4. |
| **D3 sha256** | E3 compares the row to the constant `INSTRUCTION_SHA` (`:70, :211`) | constant-bound, not byte-bound. The wave now carries the capture (`W/SourceOpen70/instruction.md`, 1882 B, `26a7ac98…`), so a reader *can* re-derive; the gate does not read it. Residual, same family as round-69 M-J/M-K. |
| **E4 semantics** | substring checks (`:224-245`) | lexical only: it passed the wrong `:59` until a human seat found it (A4 item 2). Now correct, but a future wrong pointer would pass again. |
| **D1 residual** | E1 reads only the new provenance file | the old false claims remain at `GateReceipts.md:85-89` and `EvidenceIndex.md:81,83,174-175`; superseded only by the new file. Frozen E1 asks for exactly that, so this is named, not open. |
| **E6 trust** | `check_r69_landing` reads four strings (`:262-276`) | a hand-written receipt would pass. Mitigated in fact: the stdout block reproduces byte for byte at `4038bb11` (command 6/7), which is what makes D6 real rather than prose. |
| **E8 provenance** | rc + nonempty out + err exists (`:308-324`) | the out's content re-derives against the spec and the committed policy (command 15), but nothing names the validator binary; add `w1-validate.cmd`. |

Already repaired, credited (not re-reported as new): the E3/E4 `used-by` dead arm
(`len(c) > 11` vs 11 cells) was live when I first read the gate at 00:47Z; it is now
`len(c) != 11 or NGINX_ENTRY not in c[10]`, documented in `plans/round-70-claims.md` **A4 item 1**
(`:201-205`) with a failable-arm receipt (`corpus/evidence/round70/c2/a4-usedby-arm.txt`). I
verified both arms are live and pass at the snapshot (command 12). Likewise S243's `:59 → :61` is
A4 item 2; the remaining stale copy is the lesson line (§2 D4).

## 7. Touched surfaces and out of scope

- **Wrote:** this file and `W/CorrectionDraft/{trio-fresh.txt, r69-gate-4038.out,
  depth-sha-diff.txt, s244-candidate.txt, w1-receipts.txt}`.
- **Read-only:** the L files in §0, the round-69 wave notes
  (`.ufo/waves/round-69/w1/GateReceipts.md`, `EvidenceIndex.md`), the round-69/70 lessons, the
  source captures under `W/SourceOpen70/`, and the staging candidate
  `/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/grader-fixture-coverage.md`.
- **Out of scope by seat spec, not done:** no edit to any predicate, case table, vector, digest,
  kill rule, target, registry row, lesson, receipt, README, entry or gate; no commit/push/jj
  mutation; no subagent; no `ask`; no `agent://all`. The scratch clone/run under
  `/fast/scratch/hyaku/kengaku-r70/CorrectionDraft` is deleted after the receipts were copied here.

## 8. Verdict

- **D1** closed; `f683297c…` (wave, `PRE-CLASS-ROW`, 33) vs `d65bbda…` (corpus, landing, 34), one
  line, pointer recorded — E1 re-derives.
- **D2** closed; trio receipt byte-equal to a fresh run — E2 re-derives.
- **D3** closed; anchor `instruction.md:6-11,15-18 (S242)` + S242 row with sha and used-by — E3
  re-derives (used-by live after A4).
- **D4** closed after A4; S243 supersedes S241's note with `:61`; the lesson's `line 59` is stale
  and should be fixed.
- **D5** landed but wrong: “five Mistakes rows” vs six, and the list conflates a routed defect with
  a row — E5 cannot see it.
- **D6** closed and reproducible (`REV 4038bb11`, `COMMAND python3 plans/round69_c2_routed_defects.py`,
  `RC 0`, output block byte-equal, gate blob `ea28b006…`).
- **D7** present and passes E7, but its reason needs the §4 restatement (blank first line; the
  transcript is now in-lane; the probe script/receipt are the missing bytes).
- **D8** closed: spec + rc 0 + rendered 14-task dispatch + empty stderr + dispatch identity +
  markers; recommend recording the validator argv.

**Gate observation (not a receipt):** `python3 plans/round70_c2_routed_defects.py` printed
`E1..E8 ok` / `DEFECTS n=0` / `PREDICATE R70-C2 pass`, rc 0 at 00:51:42Z (pre-A4 gate) and again at
00:55:34Z (post-A4 gate, sha `367ce58e…`). This is a working-tree observation while the L1 edits;
the scored C2 green run must be taken by the L1 at the landing tip, and the three content fixes
above should land before it.
