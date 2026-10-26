# R39AdvErrata — round-38 `adv` / pin / sentinel errata, verified against the files

Seat: scribe, round-39 wave 1 (`R39AdvErrata`, leaf). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`,
read at tip `750473847af9c7a461487ba3a589b5519fac5ed8` (freeze `088f7c36` is an ancestor; the six files I cite —
`SCORECARD.md`, `corpus/QUALITY.md`, `plans/pkg_gate.py`, `plans/round39_c1_verify.py`, `plans/round39_c2_verify.py`,
`plans/round-39-claims.md` — show `git diff --stat HEAD` = empty, i.e. committed bytes; the working tree's four
untracked entries are wave-1 outputs). Scratch `/fast/scratch/hyaku/kengaku-r39/R39AdvErrata` (`TMPDIR` there,
removed at exit). Nothing written outside `.ufo/waves/round-39/build/R39AdvErrata{,.md}`; no lane file, index, git
or jj state touched; no tool installed (pacman paused host-wide, nothing needed).

Task: (a) one appended round-39 erratum line per round-38 item below; (b) which of them the round-39 C1 `adv` cells
repeat. Method: every round-38 assertion is checked against the bytes it cites, plus the cheapest observable that
settles it (a regex run on the frozen pattern, the guard predicate evaluated on a crafted argv, `argparse`
semantics, a digest comparison, an absent-`--work` run). I did not re-run the C1/C2 predicates, re-execute the
sentinel's exploit receipts, or run anything that needs network — those are other seats' surfaces or unnecessary
for a wording audit. Receipt with every command and its raw output: `build/R39AdvErrata/verify.txt`.

**12 items, 12 verified as defects, 0 falsified, 2 with a wording correction inside the round-38 report itself
(§4).** Three are already fixed by the round-39 freeze, one partly, eight persist.

## 1. Items and verification

| # | item (source seat) | what it asserts (≤25 words, located) | verified | evidence (file:line, command) | state at round 39 |
|---|---|---|---|---|---|
| 1 | `F38CritBatE` D1 | N11's `adv` "a recheck line must carry a value" overstates: the gate accepts an empty mid-file `recheck:` (`.ufo/waves/round-38/falsify/F38CritBatE.md` §5 D1) | **yes** | `plans/round38_c1_verify.py:118`; `plans/pkg_gate.py:224` `^recheck:\s*\S` `re.M`; regex run → mid-file `True`, EOF `False`; `plans/battery38/p7m.py:49` comment says so | not repeated cell-wise (no recheck mutant); gate false-green persists, **not in round-39 Limits** |
| 2 | `F38CritBatE` D2 | N09's `adv` credits ">=8 distinct words"; the gate counts words only | **yes** | `plans/round38_c1_verify.py:113`; `plans/pkg_gate.py:204-205` count, `:207-208` distinctness *between* rows; `SCORECARD.md:564` still says "distinct" | not repeated cell-wise (no P6 mutant); the row text is uncorrected → erratum owed |
| 3 | `R38CritClaims` §1 | "3 of 22 `adv` cells name no advertising sentence" (N01, N08, N16) | **yes** (wording, §4) | `plans/round38_c1_verify.py:94,110,129`; `corpus/QUALITY.md:436,438`; `pkg_gate.py:298` is a `#` comment; `grep -c "^$" corpus/evidence/round35/tb2-eval/SHA256SUMS` → `0` | 0 of 7 round-39 cells cite only a mutant id; the class recurs in five cells, three of them unadvertised (§3) |
| 4 | `F38CritBatF` D1 | the 21 kills are carried by `battery38`, which `PINS` does not bind | **yes**, fixed | `plans/round39_c1_verify.py:72-98`; PINS 26, battery38 12, battery39 0, mismatched 0; one-line append to `d5m.py` → `f3dad700…` vs pinned `5af18f40…` | **fixed** for battery38; recurs by necessity for battery39 |
| 5 | `F38CritBatF` D2 | docstring's "every input … that exists at the freeze" false; moved source line dies with a traceback | **yes**, fixed | round-39 docstring `:46-48` enumerates the 26; `:288-290` prints `SETUP …`, exit 2; unpinned data at `plans/round37_c1_verify.py:210-217` + spec keys | universal gone, `SETUP` path present; **unpinned fixture data persists**, unnamed |
| 6 | `F38SentinelBattery` F1 | both predicates need network or a warm `~/.cache/uv` (gate falls back to `uv … biopython==1.85`) | **yes** | `plans/pkg_gate.py:272-276`; `python3 -c "import Bio"` → ModuleNotFoundError; `command -v uv` → `~/.local/bin/uv`; `grep -uv\|Bio\|network\|biopython plans/round-39-claims.md` → no match | persists and is inherited: r39 C1 pins the two `--rerun` modules (`plans/round39_c1_verify.py:90-91`), so the round-38 offline flip applies to the r39 `wrong` leg too; neither C1 nor C2 Limits names it |
| 7 | `F38SentinelBattery` F2 | `battery38` unpinned (same defect as item 4, independent seat) | **yes**, fixed | same measurement as item 4 | one fix, two reports |
| 8 | `F38SentinelBattery` F3 | fixtures are arbitrary in-process code; spec escapes; 5-token scan | **partly fixed** | child build `plans/round39_c1_verify.py:170-206` returns JSON only; battery37/36 still in-process `:276` but pinned; guard reads first `--spec` `:294-298` → measured `guard ok = True`, `argparse effective = /etc/passwd`; `SIDECHANNEL` still 5 tokens `:100`; `run_gate` passes no `env=` `:210-221` | strong channel closed; **guard bypass, absolute spec values, inherited env persist** |
| 9 | `F38SentinelBattery` F4 | probe execution escapes the counter's `--work` and can outlive the gate | **yes** | `plans/pkg_gate.py:267-285` (`cwd=root`, no `--work`, no `env=`, `timeout=600`); spec `probe_cmd` = `["plans/tb2_grader_probe.py","--lane","."]`, no work flag | unchanged (gate frozen at `ea638822…`) |
| 10 | `F38SentinelBattery` F5 | C2's V6 executes unpinned fleet-root state at an absolute path | **yes** | `plans/round39_c2_verify.py:65` `CENSUS = "/home/vgpnk/…/scripts/sources-census.sh"` (35,466 B); `:201-204` accepts any `returncode == 0` | unchanged; C2 claims "no check added or relaxed" |
| 11 | `F38SentinelBattery` F6 | `uv`/`git` PATH-resolved inside the verified path | **yes** | `plans/pkg_gate.py:260` `["git", "-C", …]`, `:276` `["uv", …]`; host `uv` = `~/.local/bin/uv` | unchanged |
| 12 | `F38SentinelBattery` F7 | absent `--work` parent → traceback, no `PREDICATE` line | **yes** | `python3 plans/round39_c2_verify.py --lane . --work <absent>` → `FileNotFoundError`, `PREDICATE` lines `0`, `exit=1`; `:264` (C1 `:268`) | unchanged; cosmetic |

## 2. (a) Draft errata for SCORECARD's round-38 section — append-only, one line per item

Proposed append (never edit `SCORECARD.md:564` or the round-38 row at `:1344`; the lane's own convention is
"recorded here as errata, never patched in place", `SCORECARD.md:84`). Text is ready to paste verbatim under the
round-38 section, after `### Planned (round 39)`:

```
### Round-38 errata (appended round 39, 2026-10-26; measured against tip 7504738)

- **E1 (item 1, `F38CritBatE` D1).** `plans/round38_c1_verify.py:118` advertises "a recheck line must carry a
  value", but `plans/pkg_gate.py:224` accepts an empty `recheck:` whenever a later non-blank line follows (`\s*`
  crosses the newline; re.search on the frozen pattern → True mid-file, False at EOF), so `p7m-n11-empty-recheck`
  demonstrates only the EOF case (`plans/battery38/p7m.py:49`). The frozen cell stands unedited; the gate
  false-green is a C1 limit, not a battery gap.
- **E2 (item 2, `F38CritBatE` D2).** "teaches cells carry >=8 distinct words" above is half enforced:
  `plans/pkg_gate.py:204-205` counts words, `:207-208` checks distinctness *between* rows, so a cell of eight
  identical words is `P6 ok`. Read the row as ">=8 words; teaches cells pairwise distinct".
- **E3 (item 3, `R38CritClaims` §1).** The "3 of 22 `adv` cells name no advertising sentence" entry is exact in
  substance, not in wording: N01 (`:94`) and N08 (`:110`) cite a sentence that does not cover the property (the
  empty pin branch is called unclaimed at `corpus/QUALITY.md:436`; the genuine `SHA256SUMS` has 0 blank lines),
  and N16 (`:129`) cites a code comment (`plans/pkg_gate.py:298`) that `QUALITY.md:438` lists as unclaimed.
- **E4 (items 4 and 7, `F38CritBatF` D1 = `F38SentinelBattery` F2 — one defect, two seats).** Fixed by the
  round-39 freeze: `PINS total=26` = 14 + the twelve `plans/battery38/*.py` digests (26/26 match; a one-line
  append to `d5m.py` gives `f3dad700…` vs pinned `5af18f40…`). Residual, unnamed: the seven kill carriers
  (`plans/battery39`) are pinned 0 times — the directory does not exist at freeze — so the `PINS` line stays
  silent about them and the landing commit is their only binding.
- **E5 (item 5, `F38CritBatF` D2).** The universal claim is gone (the round-39 docstring enumerates the 26,
  `plans/round39_c1_verify.py:46-48`) and a fixture that cannot build now prints `SETUP …` with exit 2
  (`:288-290`). Residual: the fixture data the builders adapt to — `SCORECARD.md` (D4 line),
  `corpus/lessons/round-34.md`, `.ufo/waves/round-34/assimilation/captures/` (`plans/round37_c1_verify.py:210-217`
  per the r35 spec) — is pinned nowhere and named nowhere.
- **E6 (item 6, `F38SentinelBattery` F1).** Both predicates still need network or a warm `~/.cache/uv`:
  `plans/pkg_gate.py:272-276` falls back to `uv run --with biopython==1.85` whenever host `import Bio` fails
  (it does), so every `--rerun` fixture and C2's V2 depend on it. Round-39 C1/C2 Limits do not name the
  precondition; an offline+cold host read `wrong=1` / `killed=18` in round 38.
- **E7 (item 8, `F38SentinelBattery` F3).** Partly fixed: battery38/39 build in a child process that hands back
  JSON only (`plans/round39_c1_verify.py:170-206`), closing the `R38CritClaims` §2 patch channel; battery37/36
  still build in the counter (`:276`) but are pinned. Open: the `--spec` guard reads the *first* occurrence
  (`:294-298`) while argparse takes the last (measured: guard passes with `--spec inside.json --spec
  /etc/passwd`, effective spec `/etc/passwd`); absolute paths inside spec values and the inherited environment
  (`run_gate` passes no `env=`) are unchanged; the side-channel scan is still five literal tokens (`:100`).
- **E8 (item 9, `F38SentinelBattery` F4).** Unchanged: `plans/pkg_gate.py:267-285` runs `probe_cmd` with
  `cwd=root`, no `--work` and no `env=`, and the probe takes no work flag, so only the caller's `TMPDIR`
  confines probe writes; a timeout kills the direct child only.
- **E9 (item 10, `F38SentinelBattery` F5).** Unchanged: `plans/round39_c2_verify.py:65` executes
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (35,466 B, outside the clone, in no pin) and V6
  (`:201-204`) accepts any exit 0, so "C2 passes on a clean clone" rests on fleet-root state.
- **E10 (item 11, `F38SentinelBattery` F6).** Unchanged: the frozen gate resolves `git` (`plans/pkg_gate.py:260`)
  and `uv` (`:276`) on PATH; this host's `uv` is `~/.local/bin/uv`.
- **E11 (item 12, `F38SentinelBattery` F7).** Unchanged and cosmetic: an absent `--work` parent dies before any
  check — `python3 plans/round39_c2_verify.py --lane . --work <absent>` → `FileNotFoundError`, no `PREDICATE`
  line, exit 1 (`plans/round39_c2_verify.py:264`; C1 `:268`).
```

Count note for the L1: items 4 and 7 are the same defect found independently, so the twelve items become eleven
erratum bullets (E4 covers both); the round-38 reports themselves say the two "share one root".

## 3. (b) What the round-39 C1 `adv` cells repeat

Seven cells, `plans/round39_c1_verify.py:104-140`. "Names the property?" = does the cited text state the behaviour
the mutant silences, under the round-38 tiering method reused from `R38CritClaims` §1 (C = sentence names it,
K = component noun only, N = none / disclaimed).

| cell | clause/dir | cited text (exists?) | names the property? | marked? | repeats which round-38 item |
|---|---|---|---|---|---|
| M01 | D5 mirror | Q24 `corpus/QUALITY.md:300-301` (yes) | **no** — measured no-op on the genuine state: the genuine manifest's row 1 *is* the capture's digest, so reference and mutant both print `D5 ok` (F-D) | **indirect** | none; carries N21's relabel, disclosed in-cell |
| M02 | P1 silence | `SCORECARD.md:564` "against a spec of pinned digests … a stub probe dies on its digest pin" (yes) | **partly** — see F-A | **not marked** | **item 3 class (weakened)** + item 2 shape |
| M03 | P3 silence | `plans/pkg_gate.py:9` "quote bounds … come from --spec" (yes) | **no** — provenance of the bound, not that exceeding it rejects; the defect list (`:12-13`) omits word bounds — see F-B | **not marked** | **item 3 class (weakened)** |
| M04 | P7 silence | `SCORECARD.md:564` "SOURCES rows … against a spec of pinned digests" (yes) | **no** — the mutated check reads the *entry's* `source:` lines (`plans/pkg_gate.py:211-221`), not SOURCES registry rows (`:184-209`), and no sentence requires exactly one source line per row id (F-C) | **indirect** | item 3 class, disclosed; the artefact conflation is the one round-38 N12 also carried |
| M05 | RUN rc-silence | `pkg_gate.py:7` "exit 0 = accept, 1 = reject"; `SCORECARD.md:564` "Exit 0 accept / 1 reject / 2 setup" (both yes) | yes | — | none |
| M06 | MAIN rc-mirror | `pkg_gate.py:7` + Q24 `QUALITY.md:300-301` (both yes) | yes | — | none (Q27's `:438` disclaimer is the crash→exit-2 path, not this one) |
| M07 | D5 mirror | Q24 + "the gate strips tags before the flat compare" (a code fact) | **no** — measured: the genuine quote is contiguous in the raw capture, so the strip is not load-bearing and Q24 cannot cover it (F-D) | **indirect** | none; same shape as M01, disclosed |

**Answer to (b).** No round-38 `adv` cell is carried over verbatim — the round-39 list is a different seven
(clauses D5, P1, P3, P7, RUN, MAIN, D5; round-38's N09/N11/N16 have no analogue). Item 3's class (a cell whose
citation does not cover the behaviour) recurs in **five** of the seven cells, in three degrees: two are indirect
and **unmarked** (M02, M03), and three are marked `indirect` but cite text that cannot cover the behaviour at all
(M01, M04, M07 — N08's pattern: the cited acceptance sentence is satisfied by both the reference and the mutant).
Two cells are direct (M05, M06). Attribution: peer critic `R39CritClaims` reached the same M02/M03/M04/M07
conclusion independently (`.ufo/waves/round-39/build/R39CritClaims.md` §1); the measurements and code paths below
are mine, and I did not adopt its Q1 reading (see F-C).

- **F-A (M02, `:107-111`).** The property is "every frozen instrument is checked … not only the first"; the
  mutant keeps `list(pins.items())[:1]`. The spec's `frozen_instruments` order is
  `['plans/tb2_grader_probe.py','plans/round35_c1_verify.py','plans/defect_ledger.py']` (measured), so "the first"
  **is** the probe — the one instrument the cited clause names. The cited sentence therefore covers exactly the
  pin the mutant retains; the completeness claim rests on the generic "against a spec of pinned digests" and is
  not marked indirect. A kill must break pin 2 or 3 (`round35_c1_verify.py`, `defect_ledger.py`), which no
  advertising sentence names. Control state agrees: `MUTANT M02 … SURVIVED exhibits=none`
  (`.ufo/waves/round-39/claims/control-c1-nothing.txt`).
- **F-B (M03, `:114-116`).** The property is "a quote one word above the spec's upper word bound is a defect".
  The cited docstring line (`plans/pkg_gate.py:9-10`) advertises only that the bounds are spec-driven; the
  docstring's own defect list (`:12-13`) omits word bounds; and Q24's one-word example
  (`corpus/QUALITY.md:305`, "an entry of eight one-word quotes") is the **lower** bound. No advertised sentence
  reaches the upper bound, so the cell repeats the withdrawn N02 citation's shape with a real but non-covering
  sentence. `M03 … SURVIVED exhibits=none`.
- **F-C (M04, `:119-120`).** The property is "a row id carries exactly one `source:` line, the pinned URL". The
  mutant edits `c_provenance`'s per-row test (`plans/pkg_gate.py:219-221`), which reads the *entry's* `^source:`
  lines; the SOURCES registry rows are `c_sources` (`:184-209`) and this mutant never reaches them. The cell's
  "SOURCES rows" therefore names the wrong artefact (the round-38 N12 cell carried the same conflation). Q1
  (`corpus/QUALITY.md:15-19`) only says the `source:` line carries "the `S###` row id(s), the URL, and the exact
  anchor" — what a line carries, not how many lines a row id gets — so it neither advertises nor disclaims the
  property; the cell still names no covering sentence. `M04 … SURVIVED exhibits=none`.
- **F-D (M01 `:106-108`, M07 `:144-146`).** Both cite Q24 "the genuine package must be accepted"
  (`corpus/QUALITY.md:300-301`), and both mutations are no-ops on the accepted state — measured: the genuine
  manifest `quarantine-SHA256SUMS` has 2 rows and row 1 *is* `nec-s091-reopen.html`'s digest (`b60af775…`), and
  the D5 quote is contiguous in the **raw** capture bytes (`quote in flat = True`, `quote in raw = True`). A
  sentence both gates satisfy cannot cover either cell: N08's tier on the cited-text standard. The two cells
  differ in what *else* exists on the declared surface: M01 has a covering **class** sentence the cell does not
  name — `SCORECARD.md:564` "the labelled D4/D5 correction lines against a spec of pinned digests" (a digest on
  manifest row 2 is still pinned in the manifest), so M01 is *uncitable*; M07 has no sentence anywhere reaching
  markup stripping, so M07 is *unreachable by any sentence*. Peer `R39CritClaims` reached the same M01 tier move
  independently (its §1 counts now C 2 / K 2 / N 3).

Consequences to state, not to fix here:

1. `plans/round-39-claims.md:62` says "Three of the seven `adv` cells cover their behaviour only indirectly
   (marked in the cell)". Measured split: **2 direct** (M05, M06), **2 indirect and unmarked** (M02, M03), **3
   whose citation cannot cover them** (M01, M04, M07) — and the three marked `indirect` are exactly the last
   three. Within the third group M01 is uncitable (a covering class sentence exists at `SCORECARD.md:564`, the
   cell cites Q24 instead) while M07 is unreachable by any sentence (F-D). So the marker is on the right cells but names the wrong tier ("indirect" where the round-38 method's
   own N08 precedent says unadvertised), and it is missing from the two cells that are genuinely indirect. The
   parenthetical's promise ("marks indirect coverage") is satisfied 0/5 for coverage and 3/5 for marking; the
   7-mutant denominator is unaffected.
2. Item 3's class is *repaired* in the other direction: 0 of 7 cells cite only a mutant id (round 38: 9 of 22 did,
   `R38CritClaims` §1 D3, re-measured: 9), and every one of the seven quoted fragments exists at the location
   named (the `...` elisions are the cell's, and each fragment is contiguous there). So `adv`-cell provenance
   improved from 13/22 located to 7/7 located; what remains is the marking, not the citation.
3. Items 1 and 2 (the two `F38CritBatE` claims) are **not** repeated by any round-39 `adv` cell — there is no P6
   and no recheck mutant — but nothing in the round-39 freeze names the two gate false-greens either. They are
   gate over-acceptances that no future mutant list inherits: a reader of round-39's Limits ("a kill records a
   result difference …; the side-channel scan is a token heuristic …; a child process can still leave a process")
   would not learn that `pkg_gate.py:224` tolerates a mid-file empty `recheck:` or that "distinct" is unenforced
   within a teaches cell. E1/E2 above are the durable record.
4. Items 4/5/7 (pins) are **not** `adv`-cell items; they recur at the counter/predicate locus. Item 4's class is
   fixed at 26 pins for battery38 and recurs for battery39 (0 pins; `ls plans/battery39` → no such directory at
   this read), i.e. the printed `PINS total=26 mismatched=0` is again silent about the seven kill carriers — in
   the honest direction (they do not exist at freeze), but the claims' "pins 26 inputs" does not say so. Item 5's
   false universal is gone.
5. Items 6, 9, 10, 11, 12 (sentinel) recur in round 39 unchanged and unnamed in the claims, and item 10's C2
   shape is now *sharper*: the round-39 C2 claim ("no check added or relaxed", `plans/round-39-claims.md` §C2) is
   true precisely because V6 was copied with its fleet-root absolute path, so the frozen C2 predicate is not
   reproducible off this workstation. Two of the seven sentinel findings can flip a *verdict* on this host, not
   merely its portability: item 6 (offline or cold `~/.cache/uv` → round-38 measured `wrong=1`, `killed=18`, C2
   `defects=1`) and item 10 (missing or shimmed fleet-root census → V6 DEFECT, or V6 green on a two-line shim);
   items 9, 11, 12 and the residual half of item 8 are portability, containment or hygiene. Peer `R39CritClaims`
   §4/D3 now carries item 10 as its third node of the same "predicate reads bytes outside the lane" class
   (`round39_c2_verify.py:65` `CENSUS`, 35,466 B at that path, run against `<lane>/corpus/SOURCES.md`), with the
   count unchanged on its side.

## 4. Precision corrections to the round-38 report text (not new defects)

- **`F38CritBatE` §3** says "`c_sources` has six sub-checks (`plans/pkg_gate.py:196-205`)". Measured: `:196-205`
  holds five (URL, tier, status, used-by, teaches words); the two length guards are `:191-195` and the cross-row
  distinctness check `:207-208` — eight in total. The section's conclusion is unaffected: `p6m` trips exactly the
  URL and teaches sub-checks. (`c_provenance` "five (`:220-229`)" is exact.)
- **`R38CritClaims` §1 headline** "3 of 22 `adv` cells name no advertising sentence": N01 (`:94`) and N08 (`:110`)
  *do* name a sentence; it does not cover the property (empty pin branch unclaimed, `QUALITY.md:436`; genuine
  manifest has 0 blank lines). Only N16 (`:129`) names no advertising text (a `#` comment, `pkg_gate.py:298`).
  The count 3 is right; "name no advertising sentence" should read "cite no sentence that covers the property".
  The landed `SCORECARD.md:1344` copy carries the loose wording and is corrected by E3.

## 5. Not done / limits of this seat

- No C1 or C2 predicate run (§1's pin line was measured by importing the counter's `PINS` and hashing, not by
  running the counter): the frozen predicate is wave-1 executors' and the L1's to run, and `plans/battery39` does
  not exist yet, so `MUTANTS killed=7` is unobservable at this read.
- The sentinel's exploit receipts (`spec-path-escape.txt`, `probe-exec-orphan.txt`, `strace-derivations.txt`) were
  not re-executed; F3's guard bypass was re-measured only as the guard predicate plus `argparse` semantics on the
  round-39 code, which is what decides it; F1's offline+cold-cache flip is carried from round 38's receipt.
- No network-isolation test, no `uv` cache probing, no host-wide write sweep — not needed to settle wording.
- `S117`/`S118`, the C2 probe, the receipt and the captures are outside this seat's scope (other wave-1 seats).

## Evidence

`build/R39AdvErrata/verify.txt` (started 2026-10-26T03:57-03:00, D5/M04 block appended after the peer cross-check; all commands read-only):

- `PINS 26 mismatched 0 battery38 12 battery39 0`; `gate ea638822…`; MUTANTS `D5,P1,P3,P7,RUN,MAIN,D5`;
  `indirect cells ['M01','M04','M07']` — import of `plans/round39_c1_verify.py` + `hashlib` over each pin.
- spec: `3 ['plans/tb2_grader_probe.py','plans/round35_c1_verify.py','plans/defect_ledger.py']`;
  `quote_words [3, 25]`, `min_teaches_words 8`; `probe_cmd ['plans/tb2_grader_probe.py','--lane','.']`.
- gate citations `:7 :9 :13 :113-114 :205 :208 :224 :260 :273 :276 :298` (grep -n, output in receipt).
- recheck regex: `mid-file empty recheck -> True`, `eof empty recheck -> False`.
- round-39 spec guard: `guard ok = True spec occurrences = 2`, `argparse effective = /etc/passwd`.
- absent `--work`: `exit=1`, `PREDICATE lines=0`, `FileNotFoundError … k39-c2-…`.
- host: `ModuleNotFoundError: No module named 'Bio'`; `uv` → `/home/vgpnk/.local/bin/uv`; `git version 2.56.0`;
  census `35466` bytes.
- tamper: `f3dad700… d5m-tamper.py` vs `5af18f40… plans/battery38/d5m.py` (pinned value).
- D5 genuine-state reachability: `quote in flat(tag-stripped) = True | quote in raw(no strip) = True`;
  `manifest rows = 2 | row1 carries capture digest = True`.
- M04 artefact: `c_sources` at `plans/pkg_gate.py:184`, `c_provenance` at `:211`, entry parse `:215`, per-row test
  `:220`; `QUALITY.md:305` = "eight one-word quotes" (lower bound).
- `adv` cells citing `F37XMut`: `[]` (round-38 count with the same pattern: 9).

VERDICT: adv-errata-12-verified-12
