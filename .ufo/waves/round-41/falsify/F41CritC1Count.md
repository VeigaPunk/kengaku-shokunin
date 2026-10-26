# F41CritC1Count — the C1 denominator recounted, and the SCORECARD erratum on its wording

Seat `F41CritC1Count` (critic, leaf). Round 41 wave 2 (falsify). Lane `kengaku-shokunin`, tip
`3d0058fbde484c9d6c23fd997d9ee09a0663bcdb`, freeze `8ef8b4f`, landing `74513c0`.
Object: the advertised-behaviour denominator behind C1 (`plans/tip_receipts.py` docstring + the
`sources-adopt` registry row), the coverage of the 23 frozen mutants over it, the `ADVERTISED` line, and the
SCORECARD round-41 erratum. Nothing frozen was edited; no lane, fleet-root or jj state written; no shared PATH
directory touched. My only writes were this report directory and `/fast/scratch/hyaku/kengaku-r41/F41CritC1Count`
(deleted at the end). `plans/__pycache__/round41_c1_verify.cpython-314.pyc` keeps its pre-seat mtime
(`15:43:52`, read before this seat started; `git check-ignore` shows the whole directory is ignored).

## 0. Method, envelope, receipts

Tool copies in scratch: `tools/ref.py` is a byte copy of `plans/tip_receipts.py`,
`sha256 = e4f49714299ca1f2a93303c59ac07e691cc45d6126ccf24e5eecab93733f88f3` (equals the counter's `PINS`,
`plans/round41_c1_verify.py:105-108`). `tools/t04.py` is that copy with the frozen T04 `old -> new`
(`plans/round41_c1_verify.py:142-146`) applied once: `old_occurrences=1`, one byte differs.
The fixture lane is built from nothing (`$S/fx`: one `plans/regex_log_probe.py` with a `Run as:` line, one
committed `corpus/evidence/round36/regex-log-probe-first-run.txt`); every git call named `-C "$S/fx"`, no lane
clone was made. Every run used the mandated envelope:

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
      --proc /proc --unshare-pid --die-with-parent env -i HOME=$S/home PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
      TMPDIR=$S/home LANG=C.UTF-8 /usr/bin/python3 <tool> --lane $S/fx --work <w>
```

Receipts archived beside this report: `t04-ref.txt`, `t04-mut.txt`, `clonefail.out`, `clonefail.err`,
`tool-digests.txt`. The 23 `adv` citations were checked line by line against the two pinned tools; the exact
`old`-site spans of all 23 mutants were computed from the frozen table itself
(`T01 :107, T02 :241, T03 :314, T04 :319, T05 :336, T06 :383, T07 :123, T08 :291, T09 :100, T10 :81,
T11 :97-98, T12 :52, T13 :355`; `S01 :1022, S02 :1041, S03 :1052, S04 :1039-1040, S05 :1050, S06 :1054-1055,
S07 :1046, S08 :1018, S09 :1027-1028, S11 :1068-1069`, each occurring exactly once).

## 1. `ADVERTISED direct=21 indirect=2 none=0` — the line holds; the unit is mutants, not behaviours

Recount taken from the frozen table, not read off the run (`collections.Counter` over
`round41_c1_verify.MUTANTS`): `total 23 {('direct','receipts'): 12, ('indirect','receipts'): 1,
('direct','sources'): 9, ('indirect','sources'): 1}`, `adv_kind overall Counter({'direct': 21, 'indirect': 2})`,
`empty adv cells []`.

- **Holds mechanically.** `direct` 21 = receipts T01–T05, T07–T13 (12) + sources S01–S09 (9); `indirect` 2 =
  T06, S11; `none` 0. The counter increments one bucket per row and prints the split
  (`plans/round41_c1_verify.py:581-586`, `:633`); the landing receipt prints the same line
  (`integrate/measure-final.txt:79`).
- **What the line is not.** It counts mutants that carry a quote, not advertised behaviours. `none=0` is a
  property of the frozen table: all 23 rows carry a non-empty `adv`, and any other `adv_kind` value is refused as
  invalid (`:589-590`). The line therefore cannot be read as "every advertised behaviour is priced" — §2 is the
  part it does not measure.
- **Per-cell citation audit: 23/23 cited ranges exist and are inside the advertised surface** (TR:12–32 in the
  docstring, SA:1018–1069 inside `main()`). Three cells rest their `direct` on the surface rather than on the
  fragment they quote: **S01** (:188-192) quotes the history comment `:1020-1021` ("Exclusive: before this guard,
  a combined invocation silently ignored the registry"), **S04** (:201-205) the comment `:1035-1036`, **S09**
  (:223-227) the print `:1028 "QUOTE problem="`. The cause-specific advertisements are the `parser.error`
  messages at `:1023`, `:1040`, and the row's `2` clause — all inside the claim's stated surface ("the parser
  messages in `main()`"), so the label stands; the quoted fragment is not itself an advertising sentence.
- **Wording nit (no count change):** `plans/round-41-claims.md:32` and the counter docstring `:21,:34` say "eight
  exit codes"; `SKILL.md:573` lists nine numeric codes — `0` plus the eight failure codes `2,3,4,5,6,7,8,9`.
  "Eight" is right only for the failure codes, which is what the pair directions use.

## 2. The denominator: 34 advertised behaviours carry no mutant (wave 1 said 30)

**Criterion (stated so it is checkable).** A row is *unlisted* when its implementing site is disjoint from every
mutant's `old` span, and no mutant's substitution changes the clause's result on any input where the clause's
precondition still holds. A row is *covered* when some mutant's `old -> new` sits in the code that computes the
result. (This is the wave-1 rule; the one place I depart from its outcome is R10, and that departure is
measured in §3.)

### 2.1 Covered — 24 rows

23 rows are the adv cells themselves (13 receipts, 10 sources; §1 enumerates them). The 24th is
**"any other difference is still `differ`" (`TR:23`, site `TR:322-324`, branch chosen at `TR:319`)** — no adv
cell names it, but T04's swap prices it; measured in §3.

One further clause is priced collaterally and folded in by the wave-1 convention: **"absent git → 2" (`TR:30`)**
shares `die()` (`TR:118-119` → `:107`) with T01. Counting it separately would make the census 59/25, not 58/24.

### 2.2 Unlisted, `plans/tip_receipts.py` — 22 rows

| # | advertised (file:line) | implementing site | why no mutant |
|---|---|---|---|
| 1 | `--list` classifies and runs nothing (`TR:4`, `:233`) | `TR:253-261` | line untouched; **not in R41CritEquiv** |
| 2 | `--only SUBSTR` restricts the population (`TR:4`) | `TR:249-251` | untouched |
| 3 | `--jobs N` runs probes in parallel (`TR:4`) | `TR:297-303` | untouched |
| 4 | scratch parent = `--work`, else env TMPDIR, else platform temp (`TR:4`, `:34-36`) | `TR:263-266` | untouched; **not in R41CritEquiv** |
| 5 | command resolved from the script's own `Run as:` line (`TR:7-8`) | `TR:138-158` | untouched; **not in R41CritEquiv** |
| 6 | that is the same line SKILL/README quote, printed as `doc=` (`TR:8`) | `provenance()` `TR:160-184` | untouched |
| 7 | clone of the lane at HEAD + toplevel/HEAD equality guards are `2` (`TR:9`) | `TR:269-276` | guards call `die()` (T01's site) but no fixture can trip them: `--shared` clone copies refs/HEAD and not config, so clone HEAD == `tip` by construction |
| 8 | every probe is re-run inside that clone (`TR:9`) | `TR:201-211` | untouched; **not in R41CritEquiv** |
| 9 | stdout byte-compared with the committed blob; `first_diff` (`TR:9-10`) | `TR:326`, `TR:186` | untouched |
| 10 | a table-mapped file enters the comparison (`TR:12-13`) | `TR:245`, `:97-98` | T11 prices the *origin* (table vs derived), not entry — both are `kind=byte` |
| 11 | derived mapping is `kind=byte`, `--list` prints `origin=derived` (`TR:16-17`) | `TR:102`, `TR:257` | untouched (T11 changes a table origin, not this print) |
| 12 | script gone → `skip probe-script-absent` (`TR:19-20`) | `TR:287-288` | untouched |
| 13 | a `temp-paths` receipt is still re-run (`TR:21`) | `TR:296`, `TR:318` | untouched |
| 14 | `--tamper` repeatable and comma-splittable (`TR:25`) | `TR:333` | untouched |
| 15 | one byte of the committed bytes flipped, same fresh output re-compared (`TR:25-26`) | `TR:214-226`, `:350` | untouched (T13 breaks the verdict, not the flip) |
| 16 | no `--tamper` → one control on the cheapest byte-equal receipt (`TR:26-27`) | `TR:340-341` | untouched |
| 17 | **clone failure exits 2** (`TR:31`) | `TR:270` | no mutant **and false** — measured rc 1 (§2.5) |
| 18 | **cleanup failure exits 2** (`TR:31`) | `TR:357` | no mutant **and unreachable** — `rmtree(..., ignore_errors=True)` |
| 19 | the lane is read only (`TR:34`) | whole `main`, `TR:243-285` | untouched |
| 20 | probe `TMPDIR`/`TEMP`/`TMP` inside the work dir (`TR:35-36`) | `TR:203-204` | untouched |
| 21 | the work directory is removed on exit (`TR:36`) | `TR:356-357` | untouched |
| 22 | no receipt is ever written (`TR:36`) | whole `main` | untouched |

### 2.3 Unlisted, `plans/sources_adopt.py` CLI — 12 rows

| # | advertised (file:line) | implementing site | why no mutant |
|---|---|---|---|
| 1 | `0` gates an append and prints the append block (`SK:573`) | `SA:1046-1079` (OK path) | S07 prices the collision path only |
| 2 | `2` **unreadable quote artifact** (`SK:573`) | `SA:463`, `:479-480`, `:482`, `:487` | untouched; **not in R41CritEquiv** (S09 prices an unreadable *url-map* at `:1027-1029`) |
| 3 | `4` malformed staged row (`SK:573`) | `SA:559-560` | untouched |
| 4 | `6` quote over the 25-word cap (`SK:573`) | `SA:561-562` | untouched |
| 5 | `7` quote absent from artifact bytes (`SK:573`) | `SA:563-564` | untouched |
| 6 | `8` quote bound to a mismatched URL (`SK:573`) | `SA:565-566` | untouched |
| 7 | `9` quote has no url-map entry (`SK:573`) | `SA:567-568` | untouched (S09 reaches 9 from an unreadable map, not from a missing entry) |
| 8 | `--access-date` required with `--admit-ids` (`SA:1048-1049`) | `SA:1048-1049` | untouched |
| 9 | `--attest-opened` re-dates the opened cell, prints `attested:` (`SA:1005-1007`) | `SA:1065-1067` | untouched |
| 10 | `--out` writes the block and prints `wrote … rows=` (`SA:1074-1076`) | `SA:1074-1076` | untouched |
| 11 | `--scope-to-admit` narrows refusals to the requested rows (`SA:1009-1012`) | `check()` `SA:210-228` | untouched |
| 12 | `--selftest` (17 cases) (`SK:573`) | `selftest()` `SA:621` | untouched |

### 2.4 Deltas against `.ufo/waves/round-41/build/R41CritEquiv.md` §5 (30 → 34)

- **−1: the wave-1 row R10 is covered, not unlisted.** R10 is "any other difference is still `differ`"
  (`TR:23`), which sits in the `else` of the very `if` T04 swaps (`TR:319`), so a fixture does distinguish ref
  from mutant on that clause. Measured, §3.
- **+4 receipts, +1 sources:** rows 1, 4, 5, 8 of §2.2 and row 2 of §2.3. Four are behaviours the wave-1 census
  never listed (`--list`, `--work` selection, `Run as:` resolution, the re-run itself); the fifth is the second
  half of the registry row's own `2` clause ("**or unreadable quote artifact**").
- **R4 kept as one unlisted row** (the report's). The guards share `die()` with T01, but the inputs that would
  trip them are not constructible from a fixture lane: `git clone --shared` copies refs and HEAD, not
  `.git/config`, so `clone HEAD == tip` and `clone toplevel == clone` hold by construction. Sharing a mutant's
  site is not calibration if no input reaches it.
- Arithmetic: covered 24 + unlisted 34 = **58 advertised behaviour rows**. Sensitivity: 33 if row 8 of §2.2
  ("every probe is re-run") is not counted as a separate behaviour; 33 if row 10 of §2.2 is folded into T11's
  precedence clause; 32 if both.

### 2.5 Two advertised causes the unmutated tool does not implement

`TR:30-32` advertises `2 usage/setup (…, clone or cleanup failure, …)`. Neither half holds:

```
# clone failure: lane otherwise valid, one blob in .git/objects corrupted, ls-tree still fine
bwrap … /usr/bin/python3 $S/tools/ref.py --lane $S/fx5 --work $S/w5
rc=1 ; stdout empty ; stderr last line:
subprocess.CalledProcessError: Command '['git', 'clone', '-q', '--shared', …]' returned non-zero exit status 128
```

The clone at `TR:270` is unguarded (`check=True`, no `try`); `main()` is wrapped only for `BrokenPipeError`
(`TR:386-391`), so a clone failure is a traceback at rc 1, not `SETUP: …` at rc 2. Cleanup: the only cleanup is
`shutil.rmtree(ws, ignore_errors=True)` (`TR:357`), which cannot raise. Both are *advertised behaviours with no
implementation*, so no mutant can ever price them — they belong in the denominator, and the C1 surface sentence
inherits them as if they were true. (This confirms R41CritEquiv §3 on my own fixture; the frozen tool is not
edited.)

## 3. Measured: R10 is priced by T04, so the wave-1 count of 30 overcounts by one

Fixture: one mapped `temp-paths` receipt (`corpus/evidence/round36/regex-log-probe-first-run.txt`) whose Mkdtemp
paths mask equal but whose tail differs — `masked bytes differ: byte 19 (line 1)`.

```
bwrap … /usr/bin/python3 $S/tools/ref.py  --lane $S/fx --work $S/w1     # t04-ref.txt
receipt corpus/evidence/round36/regex-log-probe-first-run.txt differ masked bytes differ: byte 19 (line 1) exit=0
receipts=1 byte_equal=0 differ=1 skipped=0
rc=1

bwrap … /usr/bin/python3 $S/tools/t04.py  --lane $S/fx --work $S/w2     # t04-mut.txt
receipt corpus/evidence/round36/regex-log-probe-first-run.txt skip reason=declared-nonreproducible-absolute-scratch-paths (equal after masking)
receipts=1 byte_equal=0 differ=0 skipped=1
rc=0
```

Reading: `if mask(fresh) == mask(blob):` becoming `!=` swaps the two branches, so on a masked-unequal receipt the
reference reports `differ` (exit 1) and T04 reports `skip` (exit 0). The clause "any other difference is still
`differ`" is therefore exercised by a frozen mutant and a fixture can price it. It moves from the unlisted column
to the covered column; the mutant is not equivalent, and no frozen file changes.

## 4. The SCORECARD round-41 erratum on the C1 wording — correct on the letter, incomplete on the substance

The erratum (`SCORECARD.md:1542-1544`) says the C1 count is over the standing battery `plans/battery41` (the
counter's `BATTERY_REL`), "not 'no committed fixture'", because the freeze commit's own witness modules kill
23/23.

**Holds.** The counter's population is `BATTERY_REL = "plans/battery41"` (`plans/round41_c1_verify.py:100`)
and its docstring says so ("Battery = `plans/battery41/*.py`, nothing else", `:43`). The witness modules are committed at the
freeze commit, not merely on disk:

```
git -C … ls-tree -r 8ef8b4fc… --name-only | grep round-41/claims    # 16 files, incl.
.ufo/waves/round-41/claims/witness/w_receipts.py
.ufo/waves/round-41/claims/witness/w_sources.py
.ufo/waves/round-41/claims/control-c1-witness-as-battery.txt
```

and that committed control ends `MUTANTS total=23 killed=23 survived=0 invalid=0 null_detected=0`,
`ADVERTISED direct=21 indirect=2 none=0`, `PREDICATE C1 pass`, `exit=0`. So the frozen C1 heading "and no
committed fixture demonstrates" (`plans/round-41-claims.md:27`) is literally false, and the erratum's
replacement wording is the honest one — it also matches the claim's own before-control, which already says "no
`plans/battery41`" (`:57`). The frozen text is internally inconsistent; the erratum resolves it correctly.

**Breaks / incomplete.** Three things the erratum leaves standing:

1. **The "before" state is vacuous.** Under the corrected wording, `BATTERY fixtures=0 → fixtures=48` (row
   `SCORECARD.md:1539`) measures that `plans/battery41` did not exist at freeze, not a calibration state of the
   two tools — with the committed witness modules as the battery the predicate already passes at the freeze
   commit. The delta measured is fixture authorship, not a change in the tools.
2. **`23/23` is a mutant count, not "advertised behaviours demonstrated".** The round title
   (`SCORECARD.md:1529`) still reads "two tools' advertised behaviours demonstrated (23/23 attributed)". Under §2
   the same 23 mutants sit over 58 advertised behaviour rows, 34 of which no mutant can price (two of them the
   false exit-2 causes of §2.5). The erratum corrects the population but not this denominator.
3. **"Kill" ≠ "demonstrate".** The erratum's justification is a direction-level kill count. The wave-2 counter
   limits (`R41CritC1Counter` A1′/§3, `R41SentinelCounter` F1) and R41CritEquiv §2/§4 show that four of the 23
   witness kills are crash-mediated or on a different clause. The erratum's sentence is defensible as written
   ("kill"), but a reader will take 23/23 as validation of the advertised surface.

**Smallest safe correction** (L1, one sentence, no predicate change): append to `SCORECARD.md:1544` —
"the before state is red only because `plans/battery41` does not exist at freeze; with the committed witness
modules as the battery the predicate already passes at the freeze commit, and 23 is a mutant count over 58
advertised behaviour rows, 34 of which no mutant prices (`.ufo/waves/round-41/falsify/F41CritC1Count.md`)."

## 5. Not in this seat

I did not run the battery, the counter, or any admission-vector attack (other wave-2 seats own those), did not
re-measure C2, and did not edit any frozen file, tool, battery module, lesson, SCORECARD or claims text. Scratch
`/fast/scratch/hyaku/kengaku-r41/F41CritC1Count` deleted after the receipts above were copied here.

VERDICT: advertised-58-covered-24-direct-21-indirect-2
