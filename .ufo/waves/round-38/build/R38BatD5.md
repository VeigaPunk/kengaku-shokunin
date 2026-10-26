# R38BatD5 — battery38 D5 module for frozen mutants N21, N22 (wave 1, build)

Seat: executor `R38BatD5`. Target: frozen gate mutants `N21`, `N22` of `plans/round38_c1_verify.py`
(clause `D5`, both cells `silence`). Lane clone
`/fast/scratch/hyaku/kengaku-r38/R38BatD5/lane` @ `2c5f4e0`, `git rev-parse --show-toplevel` =
`/fast/scratch/hyaku/kengaku-r38/R38BatD5/lane`; `sha256 plans/pkg_gate.py` =
`ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41` (freeze digest).

## Deliverable

`battery/d5m.py` (stdlib only: `hashlib`, `pathlib`, `re`, `shutil`), two fixtures:

```
5af18f40f7543fd60c8f4926b8f73553804fd428e91d3700a40f351d3d4ddbd7  battery/d5m.py
```

(L1 copy destination: `plans/battery38/d5m.py` — the module is self-contained, `fid` prefix `d5m-`,
one module for this seat.)

| fid | expect | defects | mutant | direction needed | signature measured |
|---|---|---|---|---|---|
| `d5m-n22-quote-prefix` | reject | `["D5"]` | N22 | silence | ref `D5 DEFECT`, mutant `D5 ok` |
| `d5m-n21-manifest-row-2` | accept | `[]` | N21 | **mirror** | ref `D5 ok`, mutant `D5 DEFECT` |

## Receipts (all reproduced commands, run against the clone)

```
S=/fast/scratch/hyaku/kengaku-r38/R38BatD5; export TMPDIR=$S
python3 plans/round38_c1_verify.py --lane "$S/lane" \
  --battery-dir .../build/R38BatD5/battery --only N21,N22 --work "$S/w"
```

Output (`receipt-counter-subset-run1.txt`; a second run is byte-equal, `cmp` exit 0, both exit 1):

```
PINS total=14 mismatched=0
FIXTURE r36-P0 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-P1 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P2 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P3 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P4 expect=reject declared=- observed_rc=1 observed_defects=P6 ok
FIXTURE r36-P5 expect=reject declared=- observed_rc=1 observed_defects=P1 ok
FIXTURE r36-P6 expect=reject declared=- observed_rc=1 observed_defects=P9 ok
FIXTURE r36-P7 expect=reject declared=- observed_rc=1 observed_defects=P1,P3,P6,P9 ok
FIXTURE r36-L1 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-L2 expect=reject declared=- observed_rc=1 observed_defects=D4 ok
FIXTURE r36-L3 expect=reject declared=- observed_rc=1 observed_defects=D4 ok
FIXTURE r36-L4 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-L5 expect=reject declared=- observed_rc=1 observed_defects=D5 ok
FIXTURE r36-L6 expect=reject declared=- observed_rc=1 observed_defects=D5 ok
FIXTURE d4-m44-file-unreadable expect=reject declared=D4 observed_rc=1 observed_defects=D4 ok
FIXTURE d4-m45-not-one-line expect=reject declared=D4 observed_rc=1 observed_defects=D4 ok
FIXTURE d4-m46-label-not-carried expect=reject declared=D4 observed_rc=1 observed_defects=D4 ok
FIXTURE d5-m48-file-unreadable expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE d5-m49-two-lines expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE d5-m50-label-altered expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE d5-m51-require-missing expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE d5-m52-forbid-present expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE d5-m53-capture-missing expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE d5-m55-quote-absent expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE p23-p2-receipt-deleted expect=reject declared=P2 observed_rc=1 observed_defects=P2 ok
FIXTURE p23-p2-receipt-byte expect=reject declared=P2 observed_rc=1 observed_defects=P2 ok
FIXTURE p23-p3-heading-renamed expect=reject declared=P3,P4 observed_rc=1 observed_defects=P3,P4 ok
FIXTURE p23-p3-seven-texts expect=reject declared=P3 observed_rc=1 observed_defects=P3 ok
FIXTURE p23-p3-seven-locations expect=reject declared=P3 observed_rc=1 observed_defects=P3 ok
FIXTURE p23-p3-two-word-quote expect=reject declared=P3 observed_rc=1 observed_defects=P3 ok
FIXTURE p4-no-quote-row expect=reject declared=P3,P4 observed_rc=1 observed_defects=P3,P4 ok
FIXTURE p4-capture-unreadable expect=reject declared=P4,P5 observed_rc=1 observed_defects=P4,P5 ok
FIXTURE p4-line-outside expect=reject declared=P4 observed_rc=1 observed_defects=P4 ok
FIXTURE p4-one-char-off expect=reject declared=P4 observed_rc=1 observed_defects=P4 ok
FIXTURE p5-manifest-absent expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p5-manifest-unparsed-line expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p5-capture-bytes-stale-digest expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p5-row-capture-unpinned expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p5-manifest-digest-off-pin expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p5-quote-cites-unpinned expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p5-extra-capture-file expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p6-m20-registry-row-duplicated expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m21-row-with-twelve-cells expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m22-url-off-the-pinned-raw-path expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m23-row-tier-b expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m24-row-status-queued expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m25-used-by-another-path expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m26-five-word-teaches-cell expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m27-two-identical-teaches-cells expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p7-m28-entry-deleted expect=reject declared=P3,P4,P7,P8 observed_rc=1 observed_defects=P3,P4,P7,P8 ok
FIXTURE p7-m29-source-url expect=reject declared=P7 observed_rc=1 observed_defects=P7 ok
FIXTURE p7-m30-verified-at expect=reject declared=P7 observed_rc=1 observed_defects=P7 ok
FIXTURE p7-m31-recheck-line expect=reject declared=P7 observed_rc=1 observed_defects=P7 ok
FIXTURE p7-m32-negative-heading expect=reject declared=P7 observed_rc=1 observed_defects=P7 ok
FIXTURE p7-m33-falsifier-word expect=reject declared=P7 observed_rc=1 observed_defects=P7 ok
FIXTURE p8-readme-deleted expect=reject declared=P8 observed_rc=1 observed_defects=P8 ok
FIXTURE p8-index-row-duplicated expect=reject declared=P8 observed_rc=1 observed_defects=P8 ok
FIXTURE p8-index-row-missing-sid expect=reject declared=P8 observed_rc=1 observed_defects=P8 ok
FIXTURE p8-coverage-bullet-removed expect=reject declared=P8 observed_rc=1 observed_defects=P8 ok
FIXTURE p8-extra-knowledge-file expect=reject declared=P8 observed_rc=1 observed_defects=P8 ok
FIXTURE p910-not-a-git-repo expect=reject declared=P9 observed_rc=1 observed_defects=P9 ok
FIXTURE p910-receipt-deleted expect=reject declared=P10,P2 observed_rc=1 observed_defects=P10,P2 ok
FIXTURE p910-probe-exits-1 expect=reject declared=P1,P10 observed_rc=1 observed_defects=P1,P10 ok
FIXTURE p910-receipt-one-byte expect=reject declared=P10,P2 observed_rc=1 observed_defects=P10,P2 ok
FIXTURE d5m-n22-quote-prefix expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE d5m-n21-manifest-row-2 expect=accept declared=- observed_rc=0 observed_defects=- ok
BATTERY fixtures=66 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N21 D5 silence SURVIVED -- the capture digest is looked up in every manifest row, not only the first [F37XMutD5 X3]
MUTANT N22 D5 silence killed by=d5m-n22-quote-prefix -- the whole quote must be present, not a 20-character prefix [F37XMutD5 X4]
MUTANTS total=2 killed=1 survived=1 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

Requirement-by-requirement: both of my `FIXTURE` lines `ok` (`wrong=0` over all 66), `renamed_disagree=0`,
`sidechannel=0`, `null_detected=0`; N22 `killed by=d5m-n22-quote-prefix`. N21 does **not** reach `killed`
— see the blocker below; that is not a missing fixture.

## Direct evidence: reference gate vs mutant gate on my two fixtures

`receipt-probe.txt` (driver `probe_n21.py`; gate copies in scratch, spec = the frozen r35 spec):

```
-- d5m-n22-quote-prefix expect=reject declared=['D5'] argv=d5-line --file
   ref rc=1 D5
        | D5 DEFECT directional=False digest_pinned=True bad=['quote absent from the capture']
        | defects=1
   N21 rc=1 D5
        | D5 DEFECT directional=False digest_pinned=True bad=['quote absent from the capture']
        | defects=1
   N22 rc=0 D5
        | D5 ok directional=True digest_pinned=True bad=0
        | defects=0

-- d5m-n21-manifest-row-2 expect=accept declared=[] argv=d5-line --file
   ref rc=0 D5
        | D5 ok directional=True digest_pinned=True bad=0
        | defects=0
   N21 rc=1 D5
        | D5 DEFECT directional=False digest_pinned=False bad=['capture digest is not the one in the manifest']
        | defects=1
   N22 rc=0 D5
        | D5 ok directional=True digest_pinned=True bad=0
        | defects=0
```

N22 is exactly the silence signature (`ref DEFECT` → mutant `ok`). N21 is exactly the mirror signature
(`ref ok` → mutant `DEFECT`). The fixtures are cross-independent: each one leaves the other mutant's
observable unchanged.

## BLOCKER (needs the claim owner, not this seat): N21's frozen direction cell cannot be satisfied

`MUTANTS` N21 is `("N21", "D5", "silence", …)` with the replacement
`sums.splitlines()` → `sums.splitlines()[:1]` (`plans/round38_c1_verify.py:140-141`). The mutation makes
the gate **stricter**, so it can only ever add the pin defect:

* `cmd_d5` has exactly two defect sources (`plans/pkg_gate.py:334-355`): the pin test
  `any(len(parts) >= 2 and parts[0] == digest and parts[-1].endswith(name) for parts in <rows>)`, and the
  quote test. The quote test and every early return are byte-identical in the mutant.
* The mutant's row sequence `splitlines()[:1]` is a **prefix** of the reference's `splitlines()`, and the
  per-row predicate `P` is identical, so `mutant_pinned ⇒ reference_pinned`.
* Therefore `reference_bad ⊆ mutant_bad`, and (`bad == []`) ⇔ the clause prints `ok`. A silence kill needs
  `ref DEFECT ∧ mutant ok` — impossible for every input, not just the shapes I tried.

Manifest-shape matrix (same genuine capture and erratum line, `receipt-probe.txt`):

```
shape                          reference        N21              N22              superset
genuine-row-1                  rc=0 D=-         rc=0 D=-         rc=0 D=-         superset=True
decoy-1-genuine-2              rc=0 D=-         rc=1 D=D5        rc=0 D=-         superset=True
genuine-1-decoy-2              rc=0 D=-         rc=0 D=-         rc=0 D=-         superset=True
blank-genuine-2                rc=0 D=-         rc=1 D=D5        rc=0 D=-         superset=True
genuine-2-only-empty-line-1    rc=0 D=-         rc=1 D=D5        rc=0 D=-         superset=True
decoy-only                     rc=1 D=D5        rc=1 D=D5        rc=1 D=D5        superset=True
empty-manifest                 rc=1 D=D5        rc=1 D=D5        rc=1 D=D5        superset=True
genuine-wrong-suffix           rc=1 D=D5        rc=1 D=D5        rc=1 D=D5        superset=True
```

No shape has `ref DEFECT` with a passing mutant. The counter's own predicate confirms the two cells:

```
== counter predicate applied to the seat fixtures (both direction cells) ==
   d5m-n22-quote-prefix     vs N21: silence=False mirror=False
   d5m-n22-quote-prefix     vs N22: silence=True mirror=False
   d5m-n21-manifest-row-2   vs N21: silence=False mirror=True
   d5m-n21-manifest-row-2   vs N22: silence=False mirror=False
```

Exact, minimal correction (one token in the frozen counter, `plans/round38_c1_verify.py:140`:
`("N21", "D5", "silence",` → `("N21", "D5", "mirror",`). Demonstrated in scratch on a copy — the delivered
module bytes are complete for both mutants, no fixture change needed:

```
=== N21 direction=mirror, same module bytes, subset run ===
FIXTURE d5m-n22-quote-prefix expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE d5m-n21-manifest-row-2 expect=accept declared=- observed_rc=0 observed_defects=- ok
BATTERY fixtures=66 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N21 D5 mirror killed by=d5m-n21-manifest-row-2 -- the capture digest is looked up in every manifest row, not only the first [F37XMutD5 X3]
MUTANT N22 D5 silence killed by=d5m-n22-quote-prefix -- the whole quote must be present, not a 20-character prefix [F37XMutD5 X4]
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

I did **not** edit the frozen counter, the claims, the gate, the spec, the batteries or any lane file. Under
the freeze as written, `killed=22` is unreachable by *any* battery38 content: with N21's cell at `silence`
the maximum is `killed=21 survived=1`. The frozen kill rule already says a survivor means "C1 not admitted,
reported as an honest stop" — so this is a freeze-time defect of the counter's direction cell, priced before
any fixture existed, and it needs a re-freeze (or an L1 decision to land at 21/22 and report the stop), not
a wave-1 workaround.

## Load-bearing table (delete one fixture at a time, same command, `receipt-*`)

| battery dir contents | N22 | N21 | N21 differing fixtures |
|---|---|---|---|
| my module, both fixtures | `killed by=d5m-n22-quote-prefix` | `SURVIVED` (as frozen) | 1/12 d5-line |
| only `d5m-n21-manifest-row-2` | **`SURVIVED`** | `SURVIVED` | 1/11 d5-line |
| only `d5m-n22-quote-prefix` | `killed by=d5m-n22-quote-prefix` | `SURVIVED` | **0/11 d5-line** |

```
=== load-bearing: battery with only the n21 fixture ===
BATTERY fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N21 D5 silence SURVIVED -- …
MUTANT N22 D5 silence SURVIVED -- the whole quote must be present, not a 20-character prefix [F37XMutD5 X4]
MUTANTS total=2 killed=0 survived=2 invalid=0 null_detected=0
=== load-bearing: battery with only the n22 fixture ===
BATTERY fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N21 D5 silence SURVIVED -- …
MUTANT N22 D5 silence killed by=d5m-n22-quote-prefix -- …
MUTANTS total=2 killed=1 survived=1 invalid=0 null_detected=0
```

So N22's kill is entirely load-bearing on `d5m-n22-quote-prefix` (delete it → `SURVIVED`). N21's *detection*
is entirely load-bearing on `d5m-n21-manifest-row-2` (delete it → `differing=0/11`, i.e. no fixture in the
whole 65-fixture battery changes N21's observable at all); its *kill* is blocked by the direction cell, not
by any fixture that is missing.

## Fixture design (what each one does, why it is isolated)

* `d5m-n22-quote-prefix` — copy `ctx.d5_capture_dir()` into `d/captures`, rewrite the capture to
  `re.sub(r"\s+", "", spec.d5.quote)[:20]` (`ただし、RAKUDAベンチマークは1ター`, 20 chars), re-pin
  `quarantine-SHA256SUMS` to the new digest, erratum file = the genuine line from `ctx.d5_line()`. The pin
  passes (`digest_pinned=True`), so the only failing sub-check is the quote — one defect, `D5`, as the
  reference's own note shows.
* `d5m-n21-manifest-row-2` — genuine capture and erratum line untouched; manifest = decoy row
  (`"0"*64  geniac-s105-reopen.html`) first, the genuine digest row second. The unmodified gate accepts
  (`D5 ok … digest_pinned=True`), and this is the only fixture in the 65-fixture battery whose matching
  manifest row is not row 1 (`F37XMutD5` F2), which is why it is kept in the module.

Operability checks: module tokens — `/proc`, `ppid`, `cmdline`, `psutil`, `environ` all absent
(`python3 -c` membership test printed `False False False False False`), `sidechannel=0` from the counter;
stdlib only; `fid`s unique across the battery (`SETUP duplicate` never fired; `fixtures=66`, 64 pre-existing
+ 2); renamed-path invariance `renamed_disagree=0`; null-gate control `null_detected=0`; one module per
battery dir; every write is inside the fixture dir `d` (no lane, index, corpus or plans write).

## Risks / limits

* If the L1 keeps the freeze as written, the wave's C1 predicate is red at `killed=21/22` and the only
  admissible outcome is the honest stop the kill rule already names. Re-freezing the N21 cell is a claim-owner
  action; my module needs no change for either outcome.
* `d5m-n21-manifest-row-2` is an accept-side row; if some later gate change makes it a reject, the row turns
  `FIXTURE … WRONG`, which is the intended calibration signal (it is anchored to the frozen gate digest).
* Nothing about N22 depends on locale: the quote has no whitespace (70 chars, `re.search(r"\s", quote)` is
  empty), so the prefix cut is stable at 20 characters.
* I installed no tools (no `uv`/`npm`/binary install, no pacman), so there is no tooling line to record.

## Cleanup

`rm -rf /fast/scratch/hyaku/kengaku-r38/R38BatD5` after the receipts were copied into this directory
(`battery/d5m.py`, `probe_n21.py`, `receipt-counter-subset-run1.txt`, `receipt-counter-subset-run2.txt`,
`receipt-probe.txt`). No lane file, lane Git index, jj state, fleet-root file or sibling lane was written;
no corpus/ or plans/ tree was copied into the build directory.

VERDICT: battery38-d5m-killed-1/2-wrong-0
