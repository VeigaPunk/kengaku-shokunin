# R36CritBattery — C1 battery overfit falsifier (round 36, wave 1)

**Verdict: the frozen C1 battery is gameable.** Two gates that implement **none** of the hardened
contract score `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0`. One of them never opens
the spec, the lane, or a fixture file — it decides from fixture *names* alone. The battery cannot
distinguish either gate from a hardened one, and their counter output is byte-identical.

Scope: this attacks the C1 battery's discriminating power, not the task and not any particular gate
(the real `plans/pkg_gate.py` was absent at freeze). No lane file, claim, harness, spec, ledger row or
git index was written; all writes are under `.ufo/waves/round-36/build/` and `/tmp`.

## 1. Artefacts

| file | sha256 | role |
|---|---|---|
| `build/R36CritBattery/overfit_gate.py` | `50e6b8e1b62a1a16040427eb177aa3588910e42df84cb7a08981662f37acad07` | the overfit gate (`OVERFIT_STRATEGY=identity\|path`) |
| `build/R36CritBattery/exp_cues.py` | `5365ba668ceec9e314215fee6ef0005ccd2babf0ebb9144258e32461a0a60098` | EXP3/5/5b/6 driver |
| `build/R36CritBattery/neutral_battery.py` | `036eeb894e1b9f9e08f8807b8ce666e088124550d1ab97faa986dff2c2f26d05` | rename-invariance battery (NB-A/NB-B) |
| `build/R36CritBattery/battery-identity.txt` | `19fd8034543290f9053027c822127713aff4db109186498a7d0f5f7d14c45958` | counter output, identity gate |
| `build/R36CritBattery/battery-path.txt` | `19fd8034543290f9053027c822127713aff4db109186498a7d0f5f7d14c45958` | counter output, path gate (**byte-identical to the line above**) |
| `build/R36CritBattery/exp_cues.txt` | — | experiment transcript |
| `build/R36CritBattery/neutral_battery.txt` | — | experiment transcript |

The gate is 152 lines and implements **0 of the 12 clause groups** in the ticket's hardened
contract (instrument pins, receipt pin, quote-row parsing, 8×3-25-word quotes on ≥8 lines, S105-S107
cells/tier/status/URL/used-by, teaches ≥8 distinct words, capture SHA256SUMS, provenance trio +
negative space, README/index parity, clean-tree, `--rerun` byte-compare, d4/d5 direction). It parses
no quote table, counts no word, runs nothing, and reads no `git` state.

## 2. Reproduction

```
D=$(mktemp -d /tmp/k36-critb-XXXX)
git clone -q --no-checkout --shared <lane> "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone '/plans/' '/corpus/' '/SCORECARD.md' \
    '/.ufo/waves/round-34/assimilation/captures/'
git -C "$D/lane" checkout -q master          # HEAD f9efce3beb0705ec2e04ba3f8f449d10d64cc1dd
cp build/R36CritBattery/overfit_gate.py "$D/lane/plans/pkg_gate.py"
git -C "$D/lane" add -A                      # index only, so R35-D2's untracked count is 0
cd "$D/lane"
OVERFIT_STRATEGY=identity python3 plans/round36_c1_verify.py --lane .
OVERFIT_STRATEGY=path     python3 plans/round36_c1_verify.py --lane .
```
Frozen instruments in the clone verify at their freeze digests:
`plans/round36_c1_verify.py` = `d7c3687c09ed4c8a09a9d7c63efa9232c2b1aff8ffb229fb8a0505578317df73`,
`plans/pkg-spec-r35.json` = `e085b43505c9848c8d19eb52c52fec1a3282dac3c5b436f59320e95e5c299fc4`
(`sha256sum`). So the counter under test is the frozen one.

### 2.1 Counter output — identity gate (byte-identity to the lane, no semantics)

```
FIXTURE P0 expect=accept observed=accept ok -- genuine round-35 package
FIXTURE P1 expect=reject observed=reject ok -- 8 one-word quotes
FIXTURE P2 expect=reject observed=reject ok -- 8 copies of one quote
FIXTURE P3 expect=reject observed=reject ok -- an unparsed quote row beside the genuine rows
FIXTURE P4 expect=reject observed=reject ok -- junk teaches cells
FIXTURE P5 expect=reject observed=reject ok -- stub probe printing the receipt
FIXTURE P6 expect=reject observed=reject ok -- untracked leftover file
FIXTURE P7 expect=reject observed=reject ok -- cheapest package: one-word quotes + junk teaches + stub probe + stray file
FIXTURE L1 expect=accept observed=accept ok -- D4 genuine correction line
FIXTURE L2 expect=reject observed=reject ok -- D4 line with the two file:line citations swapped
FIXTURE L3 expect=reject observed=reject ok -- D4 line without the harness token
FIXTURE L4 expect=accept observed=accept ok -- D5 genuine erratum line
FIXTURE L5 expect=reject observed=reject ok -- D5 erratum saying the quote is not present
FIXTURE L6 expect=reject observed=reject ok -- D5 genuine line over an altered (quote-injected) capture
FIXTURES total=14 false_green=0 false_red=0 unevaluated=0
R35-D1 status=open observed=pass agree=NO fixtures=14 false_green=0 false_red=0 unevaluated=0 tip_package_rc=0
R35-D2 status=open observed=pass agree=NO untracked_anywhere=0 line_fixtures_wrong=0/6
R35-D3 status=open observed=fail agree=yes committed_nested_wave_paths=21
R35-D4 status=open observed=fail agree=yes round-36 lesson absent; recount 13 + 23 + 1 = 37 vs stated denominator 38
rows=4 closed=0 observed_pass=2 mismatches=2
PREDICATE C1 fail
```
(`exit=1`, only because the ledger rows are still `open`; `R35-D1` and `R35-D2` already *observe pass*
against this gate — see §5.)

### 2.2 Counter output — path gate (names only)

Exactly the same 14 `FIXTURE` lines and the same `FIXTURES total=14 false_green=0 false_red=0
unevaluated=0`; the saved files are byte-identical (`sha256sum` above, `diff` of the two outputs is
empty). This gate **never opens the spec** and never opens a lane or fixture file; the harness passes
`--spec` but the strategy ignores it, which is why it still answers correctly with a nonexistent spec:

```
OVERFIT_STRATEGY=path python3 plans/pkg_gate.py package --root /tmp/k36-P0-zzz --spec /nonexistent.json  -> rc=0
OVERFIT_STRATEGY=path python3 plans/pkg_gate.py package --root /tmp/k36-P3-zzz --spec /nonexistent.json  -> rc=1
OVERFIT_STRATEGY=path python3 plans/pkg_gate.py d4-line --file /tmp/d4-genuine.txt --spec /nonexistent.json -> rc=0
OVERFIT_STRATEGY=path python3 plans/pkg_gate.py d4-line --file /tmp/other.txt      --spec /nonexistent.json -> rc=1
```

## 3. Cue inventory (each cue, what supplies it, what removes it)

| # | cue | supplied by (battery property) | buys | removal that defeats it | evidence |
|---|---|---|---|---|---|
| A | fixture directory basename `k36-P<n>-` encodes the verdict (`P0` accept, `P1..P7` reject) | `tempfile.mkdtemp(prefix=f"k36-{pid}-")` in `build_package_fixtures` | 8/8 package verdicts | neutral/random fixture dir names | NB-A `path` → `false_green=7 false_red=2` |
| B | line-fixture file basenames `d4-genuine.txt`, `d5-genuine.txt`, `d5-altcap.txt` (+ dir `alt-captures`) encode the verdict | `build_line_fixtures` hard-codes the names | 6/6 line verdicts | neutral line-fixture names | NB-A `path` → `L1:reject L4:reject` |
| C | anything not shaped like a fixture is genuine (the tip call is structurally unique: `--root` = lane, `--rerun` used **only** there, `--capture-dir` = the lane's own dir) | `r35_d1` calls `["package","--root",lane,"--rerun","--require-clean-tree"]`; no fixture ever gets `--rerun` | the tip verdict, free | run a junk package through `--rerun`; point the tip check at a copy | NB-A path gate accepts the 7 junk copies it cannot name |
| D | `--root` equals `--spec`'s lane root | the tip invocation `--root .` with `--spec ./plans/...` | accept with **zero** content read | judge a copy of the lane (fresh clone), not the lane judging itself | EXP6: a root holding only a one-line tampered receipt `TAMPERED RECEIPT: cases=0`, **no entry, no sources, no capture** → `rc=0`; the same tree against a foreign spec → `rc=1` |
| E | byte-identity of entry/receipt/SOURCES/README/frozen instruments to the lane's own copy | the battery's genuine fixture is a `shutil.copy2` of lane bytes, so every mutant is a byte difference | P1,P2,P3 (entry), P4 (SOURCES), P5,P7 (probe) — all 5 without parsing anything | a genuine package with one benign edit outside every checked field must **accept** | EXP3 → `identity_rc=1` (false red) while all 22 quote rows still parse; `path_rc=0` |
| F | literal stray-file name `plans/round35_scratch.py` | `build_package_fixtures` writes that exact name for P6/P7 | P6, P7's stray component | rename the stray file (the defect class is "untracked file", not a filename) | EXP5 (`plans/leftover_notes.py`, untracked, `git ls-files --others` = `['plans/leftover_notes.py']`) → `rc=0` false green; EXP5b (battery's name) → `rc=1` |
| G | literal equality with the one genuine D4/D5 line | both genuine fixtures are the lane's line text verbatim; L2/L3/L5 are single-string edits | L1/L4 accept, L2/L3/L5 reject — no directional parse, no token proximity, no negation semantics | a genuine line that is reworded/reordered while remaining true must accept | EXP3-analogue: the gate compares strings, so any legitimate rewording is a false red (code fact, `identity_d4`/`identity_d5`, `overfit_gate.py:113-123`) |
| H | capture byte-identity to the lane's copy (the altered capture is one replaced file; "tiny size" is the named marker) | L6 copies the capture dir then overwrites `nec-s091-reopen.html` (`<html>quote</html>`, 210 B vs 60,335 B) | L6 | an altered capture with plausible size/bytes; and a *legitimate* re-capture must still accept | NB-B/EXP-family: any byte change flips the verdict, benign or not |

Cues available in the battery but **not even needed** by either strategy (the attack surface is wider
than the 8 above): the literal `junk` teaches cell (P4/P7), the stub-probe shape (`sys.stdout.write(`
+ no `argparse`, P5/P7), and git state (`git ls-files --others`, P6/P7 — legitimate here, but the
battery also builds *every* fixture as a fresh repo, so "root has a `.git`" carries no signal).

## 4. Rename-invariance and content probes

`neutral_battery.py` rebuilds the *same* 14 mutations with the same expectations, neutralising the
directory names (A) and the line-fixture names (B); NB-B additionally neutralises F.

```
NB-A path:     false_green=7 false_red=2 unevaluated=0  wrong=['P1:accept','P2:accept','P3:accept','P4:accept','P5:accept','P6:accept','P7:accept','L1:reject','L4:reject']
NB-A identity: false_green=0 false_red=0 unevaluated=0  wrong=[]
NB-B path:     false_green=7 false_red=2 unevaluated=0  wrong=[...same as NB-A...]
NB-B identity: false_green=1 false_red=0 unevaluated=0  wrong=['P6:accept']
```

Reading: (i) the name cues are load-bearing — a rename-only pass with no new fixture already flips the
path gate to 9 wrong verdicts; (ii) byte-identity survives renaming untouched, so **renaming alone is
not sufficient**; (iii) the literal stray name (F) is a one-token cue, removed by one rename.

Directional content probes (EXP3/EXP5 in §3) are the minimal pair that flips E and F: a genuine package
that must accept and the stray-file defect that must reject. Neither is in the frozen battery.

## 5. Consequence for C1 (calibration)

- The frozen predicate is a behavioural one: 14 accept/reject snapshots. It reads **no property of the
  gate**, so the ticket's rule "a gate must never recognise fixtures by name, path, or marker string"
  is unenforced by the thing that scores C1. A clean `FIXTURES` line is evidence of *verdict
  reproduction*, not of hardening.
- This recurses the round-35 defect one level up: R35-D1 was "the counter accepts junk packages". The
  round-36 battery accepts a *gate* that accepts junk packages whenever the junk is not one of the seven
  named mutants. Same class, one meta-level higher.
- `R35-D1` and `R35-D2` already `observed=pass` under this gate (`tip_package_rc=0`,
  `untracked_anywhere=0`, `line_fixtures_wrong=0/6`), so closing those two rows on the strength of a
  clean battery would mark the defects closed on evidence that does not establish the gate's contract.
  Wave 1 should not close them on the battery line alone.
- Nothing here touches C2 (different counter, different surfaces).
- Impacted axes: **calibration** (C1's entire axis move). No coverage/novelty/depth/freshness effect.

## 6. Smallest safe correction

Ordered by cost; S1 and S2 are harness/battery changes, S3 is record-only.

1. **S1 — rename-invariance pass (0 new fixtures, 1 harness change).** Build the same 14 fixtures a
   second time with neutralised directory and file names (my `neutral_battery.py` is a working
   reference) and require both passes clean. Kills cues A and B outright (measured: `fg=7 fr=2`). This
   is the cheapest change that makes the predicate see a name-recognising gate, and it cannot
   over-constrain a compliant gate because the fixture contents and expectations are untouched.
2. **S2 — two content fixtures (needs a freeze amendment; total 14 → 16).**
   - **P8** genuine package with one benign prose token added **outside** every checked field (e.g. in
     the capture-source line of the entry) — **must accept**. Kills E: byte-identity false-reds it
     (EXP3, `identity_rc=1` with all 22 quote rows intact). A compliant gate passes it, because the
     contract does not pin entry bytes.
   - **P9** the P6 defect with the stray file renamed — **must reject**. Kills F (EXP5: `rc=0`).
   These two are the minimum that force the gate to distinguish "changed" from "defective" in both
   directions; they prescribe no implementation.
3. **S3 — record as a limit, do not repair the frozen battery this round.** The claims' kill rule says a
   mutant surviving a wave-2 mutation seat is reported as a limit, never repaired into the frozen
   battery. File a ledger row (proposed `R36-D1`, class `battery-accepts-recognising-gate`, source this
   report) and a lesson line: a clean `FIXTURES` line is necessary but not sufficient; wave 2 must rerun
   S1 and S2 against the landing gate and report the result. If the landing gate is only ever measured
   by the frozen 14, C1's calibration delta should be reported as unevidenced, not earned.

## 7. Bounds

- No hardened `plans/pkg_gate.py` existed at freeze; no claim is made that the landing gate *is*
  overfitted. The claim is about what the frozen predicate can and cannot see, demonstrated by two
  gates that satisfy it while implementing none of it.
- All fixtures were built in `mktemp` repos top-verified against their own path
  (`git rev-parse --show-toplevel` == fixture dir); no commit was made; the clone's index was the only
  git mutation; the clone and all experiment dirs were removed after capture.
- The counter was run at clone HEAD `f9efce3` with the frozen harness and spec digests shown in §2.
- Tools: none installed or upgraded (`python3` 3.14.8 as shipped; no `uv`/`npx`/`pacman` calls).

VERDICT: overfit-gate-clean-cues-8
