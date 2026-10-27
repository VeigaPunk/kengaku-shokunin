# R45ProbeFirst — the recorded run of the frozen TB2 `password-recovery` probe

Seat `R45ProbeFirst` (executor, kengaku round 45 wave 1). Scope: make the first recorded (non-dry,
non-stage-check) run of `plans/password_recovery_probe.py`, save stdout as the receipt draft, and report the
summary line, the `regrade` summary, and every CASE line whose observed verdict differs from the frozen
prediction in `corpus/evidence/round45/password-recovery-dry-cases-freeze.txt`.

**Outcome: the claim is NOT an honest-stop. `mismatches=0`.** The 16 frozen predictions all reproduce exactly.

> **Routing note (added after the run).** I first sent §5's findings to `agent://KengakuR45`, which is the
> attempt-1 L1; that attempt has ended and does not own the lane. The attempt-2 L1 that dispatched w1 is
> `KengakuR45-2`, and §5's findings and §9's follow-up were re-routed there (Main also relayed them). §5
> below is the *original* defect report against commit `05b02e2`; §9 records how the attempt-2 L1's fixes
> landed and what is still open. The probe result itself (§§1–4, §6) is unchanged by any of this.

## 1. What I ran

Frozen instrument, at its frozen digest, unchanged:

```
sha256sum plans/password_recovery_probe.py
f87a9eebe464b29d95259cae24c00b56ea58de5bf93fef10884daa673e1488b5  plans/password_recovery_probe.py
```
The counter pins the same value (`plans/round45_c2_verify.py:91` `PROBE_SHA256`). The frozen dry table is also
at its pin (`plans/round45_c2_verify.py:92` `DRY_SHA256` = `46036abe…`; measured `46036abe542aa8e50a59080bda82c154ae4735de25ac64416906de263f71aabb`).

Clone rule honoured: `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"`;
`git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r45/R45ProbeFirst/lane`; every git
call names `-C "$S/lane"`; no commit, no write to the lane tree. The clone's `plans/password_recovery_probe.py`
and `corpus/evidence/round45/password-recovery-dry-cases-freeze.txt` are byte-identical to the lane's
(`cmp` → identical), and the clone's four capture digests match the probe's `PINS` exactly.

## 2. The run (host-safety: inside the envelope)

Command (`S=/fast/scratch/hyaku/kengaku-r45/R45ProbeFirst`), run from the fleet root, stdout captured to a file
so the receipt bytes are exactly the probe's stdout:

```
"$L/.ufo/waves/round-45/claims/envelope.sh" "$S/env" /usr/bin/bash -c \
  'exec /usr/bin/python3 "$2" --lane "$1" --work "$3" > "$4" 2> "$5"' \
  _ "$S/lane" "$L/plans/password_recovery_probe.py" "$S/w" "$S/probe.stdout" "$S/probe.stderr"
```

ENVELOPE lines (QUALITY Q32) — the full transcript is at
`.ufo/waves/round-45/w1/R45ProbeFirst/envelope-transcript.txt`:

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r45/R45ProbeFirst/env /fast/scratch/hyaku/kengaku-r45/R45ProbeFirst/env --bind /fast/scratch/hyaku/kengaku-r45/R45ProbeFirst/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/bash -c exec /usr/bin/python3 "$2" --lane "$1" --work "$3" > "$4" 2> "$5" _ /fast/scratch/hyaku/kengaku-r45/R45ProbeFirst/lane /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/password_recovery_probe.py /fast/scratch/hyaku/kengaku-r45/R45ProbeFirst/w /fast/scratch/hyaku/kengaku-r45/R45ProbeFirst/probe.stdout /fast/scratch/hyaku/kengaku-r45/R45ProbeFirst/probe.stderr
ENVELOPE start 23:28:39 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 23:28:43 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```

`~/.local/bin` content digest `c263b11afb1cccf6` before and after → **unchanged**; the measurement counts.
Stderr of the probe: empty. No write landed outside the scratch tree.

## 3. The requested lines

**Summary line** (`plans/password_recovery_probe.py:365`):

```
cases=16 observed_pass=5 observed_fail=11 mismatches=0
```

**`regrade` summary** (the second fresh harness pass over the same end state):

```
regrade cases=16 differ=0
```

**CASE lines whose observed verdict differs from the frozen prediction: NONE.** Every one of the 16 cases
carries `match=yes` and `regrade=same`. Machine cross-check of the receipt against the frozen dry table
(`$S/crosscheck.py`): case ids equal, in the same order, `discrepancies: NONE`; the frozen `predicted=`
verdict, the frozen `tests=` letter pair and the observed `tests=` pair agree for all 16.

| case | frozen | observed | tests | regrade |
|---|---|---|---|---|
| `nop` | fail | fail | F- | same |
| `oracle-solve-sh` | pass | pass | PP | same |
| `constant` | pass | pass | PP | same |
| `constant-crlf` | pass | pass | PP | same |
| `constant-joined` | fail | fail | PF | same |
| `dir-state` | fail | fail | PF | same |
| `empty-file` | fail | fail | PF | same |
| `wrong-23` | fail | fail | PF | same |
| `prefix-decoy` | fail | fail | PF | same |
| `sub-first` | fail | fail | PF | same |
| `sub-last` | fail | fail | PF | same |
| `lower23` | fail | fail | PF | same |
| `decoys-1000` | pass | pass | PP | same |
| `password-eq` | fail | fail | PF | same |
| `crlf-line` | pass | pass | PP | same |
| `under-varsea` | fail | fail | F- | same |

One case carries a note the dry table does not: `dir-state` observed `error=IsADirectoryError` — the second
captured test dies on a non-assert exception, exactly as the case's own requirement text predicts. It is a
`match=yes` case (predicted `PF`), so it is not a mismatch.

**The claim is honest: `mismatches=0`. No honest-stop.**

## 4. Receipt draft

`.ufo/waves/round-45/w1/R45ProbeFirst/password-recovery-probe.txt` — 4659 bytes, sha256
`cf74f451df90aa4adfcc45dc6d9023ba288bf456de939377c97e24ca3c6c924e`, the probe's stdout verbatim.

Reproducibility (the gate's `P10` clause demands a fresh run be byte-equal to the receipt). I ran the probe
three times, in three envelope runs, all `local_bin_content … unchanged`:

1. `--lane "$S/lane"` (my clone) → `cf74f451…`
2. `--lane "$S/lane"`, second work dir → `cf74f451…`
3. `--lane .` with `cwd=$S/lane` (the gate's exact form) → `cf74f451…`

`cmp` says all three are byte-identical, and byte-equal to the draft. The probe is deterministic here, as its
docstring claims ("Deterministic receipt: no temp path, timing or host version is printed").

## 5. Finding for the L1 — the committed receipt carries ENVELOPE lines and fails gate `P10`

**This is the actionable part of my seat, and it is a live defect on the lane right now.**

The L1 seat made its own recorded run at **23:27:11** and committed it as `05b02e2` ("round-45: first recorded
probe run — password-recovery 16 cases, mismatches=0, regrade differ=0"). The file it wrote to
`corpus/evidence/round45/password-recovery-probe.txt` is **5243 bytes** and its first and last lines are
`ENVELOPE …`:

```
ENVELOPE /usr/bin/bwrap … -- python3 plans/password_recovery_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r45/L1/w-probe
ENVELOPE start 23:27:11 cwd=/home/vgpnk/Projects/shokunin/kengaku-shokunin
# tb2 password-recovery grader probe (kengaku round 45) @ terminal-bench-2 2fd12b88
…
cases=16 observed_pass=5 observed_fail=11 mismatches=0
ENVELOPE end 23:27:15 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```

The probe output inside it is byte-identical to mine (I stripped the three `ENVELOPE ` lines and `cmp`ed:
identical, 4659 bytes) — so the L1's **verdicts are right**; only the file's framing is wrong.

**Why it is a defect.** `plans/pkg_gate.py:267-285` (`c_rerun`, the `P10` clause) runs the frozen probe and
requires `r.stdout == want` where `want` is the receipt file's bytes:

```
if r.stdout != want:
    return False, "fresh probe output is not byte-equal to the receipt"
```

Measured on the live lane (`pkg_gate.py package --root <lane> --spec <effective-spec> --rerun`):

```
P10 DEFECT fresh probe output is not byte-equal to the receipt
```

And `plans/round45_c2_verify.py` `V2` runs that gate and fails on it → `V2 DEFECT … gate_exit=1` →
`checks=11 defects=3` → `PREDICATE C2 fail`. Full live-lane counter snapshot at 23:33 (inside the envelope,
digest unchanged):

```
V1 ok listed=9 bad=0 extra=0
V2 DEFECT spec=frozen gate=frozen gate_exit=1
V3 ok rows=8 bad=0
V4 ok cases=16 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=9 tags=9 bad=0
V8 ok order_exit=0 result=PASS
V9 DEFECT case_rows=16/16 bad=["row ids absent outside source lines: ['S149','S150','S151','S152','S153','S154','S155','S156']"]
V10 DEFECT mechanism_rows=16/16 bad=['constant-crlf:tests/test_outputs.py:14 quote not on the line', 'dir-state:tests/test_outputs.py:14 quote not on the line', 'crlf-line:tests/test_outputs.py:14 quote not on the line', 'under-varsea:tests/test_outputs.py:10 quote not on the line']
V11 ok states=48 grader_pass=18 grader_fail=30 disagree=0
checks=11 defects=3
PREDICATE C2 fail
```

Note `V4 ok cases=16 mismatches_named=0/0` — the receipt's *content* is sound; `V8 ok … PASS` — the order of
operations holds. Only the file's framing breaks `P10`.

**The fix (verified, not guessed).** In a scratch clone of the lane (`$S/lane4`, `git clone --shared`, no lane
write): replace the receipt with the bare probe stdout and commit; then

```
P2 ok receipt_sha256=pinned
P10 ok probe_rerun=byte-equal bytes=4659
```

and the order gate stays green:

```
ORDER ok no claims file committed at or before the receipt shows the frozen probe executed
ORDER RESULT PASS
```

**Where the ENVELOPE evidence goes instead.** It must not be committed under `.ufo/waves/round-45/claims/`
*before* the receipt: `plans/order_check.py`'s `CASE_LINE` pattern (`^\s*CASE\s+\S+.*\bobserved=`) treats a
receipt-shaped line in a claims blob as proof the probe ran pre-freeze. I proved both directions in throwaway
fixture repos under my scratch:

- envelope transcript committed under `claims/` **before** the receipt → 16 `kind=case-observed` hits →
  `ORDER FAIL probe-executed-before-receipt hits=16`, exit 1.
- envelope transcript committed **after** the receipt → `ORDER RESULT PASS`, exit 0.

Round 44 followed exactly this shape: its receipt `corpus/evidence/round44/feal-linear-probe.txt` has **0**
`ENVELOPE ` lines, and the envelope evidence sits in
`.ufo/waves/round-44/claims/witness-run.txt`, committed *after*, and carrying no `CASE … observed=` line. The
same holds for the r41/r42/r43 receipts (0 envelope lines each).

So: **bare stdout in the receipt; the ENVELOPE transcript in the seat report / an after-receipt claims file.**

### 5b. `P5` — the spec's row `capture` names do not match the manifest names

`plans/pkg-spec-r45.json` rows name the captures flat (`test_outputs.py`, `setup.sh`, `Dockerfile`,
`test.sh`, `solve.sh`), but the capture manifest `SHA256SUMS` and the frozen counter's `CAPTURES` dict use the
upstream directory layout (`tests/test_outputs.py`, `environment/setup.sh`, `environment/Dockerfile`,
`tests/test.sh`, `solution/solve.sh`). `pkg_gate.py` `c_captures` reads `pinned` keys from the manifest and
looks up `row["capture"]` in them, so five rows are "not pinned in the manifest" (`S149`, `S151`, `S152`,
`S153`, `S155`) — `P5 DEFECT manifest_entries=9 bad=10`. Note the spec's `upstream` fields are correct; only
the sibling `capture` field is flat.

**The spec is frozen** (`SPEC_SHA256 = 3eb696b4…`, measured identical; `pkg-spec-r45.json` is in the
do-not-touch list), and `c_captures` also checks every *quote* capture against the manifest, which is the same
flat-vs-nested mismatch (see 5c). I verified the diagnosis in a scratch clone (`$S/lane3`): remapping only the
spec's row `capture` names to the nested manifest names turns `P5` green (`P5 ok manifest_entries=9 bad=0`)
with nothing else changed. **This is a spec change and therefore the L1's call, not mine** — it needs a
counter re-pin too (`SPEC_SHA256` is pinned in `round45_c2_verify.py:87`).

### 5c. `P3`/`P4`/`P7`/`V9`/`V10` — the entry's defects (all in `corpus/knowledge/tb2-password-recovery-grader.md`)

Not my lane, but measured here so the L1 has the list with root causes:

- **P4** (`checked=19 bad=12`, first `test_outputs.py: unreadable capture`): twelve `## Located quotes` rows
  cite flat capture names (`test_outputs.py:8`, `test.sh:26`, `setup.sh:25`, `solve.sh:16`, `Dockerfile:15`)
  where the capture lives at `tests/test_outputs.py`, `tests/test.sh`, `environment/setup.sh`,
  `solution/solve.sh`, `environment/Dockerfile`. The gate resolves a quote's capture as
  `root/capture_dir/<capture>`, so the flat name does not exist. Twelve rows: 1 `test_outputs.py`, 2 `test.sh`,
  3 `setup.sh`, 3 `solve.sh`, 1 `Dockerfile` = 10 quote rows + the 5 spec rows counted in P5.
- **P3** (`out_of_word_range=1`): one quote is a single word — `OUTPUT_FILE="recovered_passwords.txt"`
  (`solution/solve.sh:51`); the rule is 3–25 words (`spec.entry_rules.quote_words`).
- **P7** (`no '## Negative space' section`): the entry has no `## Negative space` section, and
  `c_provenance` also wants a falsifier (`falsifi(?:er|ed|es|ability)`) in it, plus a `verified-at:` and a
  `recheck:` line.
- **V9** (`row ids absent outside source lines`): the entry body never mentions `S149`…`S156` outside the
  `source:` lines. Also `PROVINCE.md` names the task and the entry on no line, and README's `## Frontier`
  does not name the task (both are modified-but-uncommitted in the lane: `M PROVINCE.md`, `M corpus/README.md`).
- **V10** (4 quote-not-on-the-line): for four rows the cited line does not contain the quote —
  `constant-crlf` and `crlf-line` quote `read_text().strip().split("\n")` / `strip().split("\n")` at
  `tests/test_outputs.py:14`, where the actual line 14 is
  `guesses = Path("/app/recovered_passwords.txt").read_text().strip().split("\n")`; `dir-state` quotes
  `test_recovery_file_exists()` at line 14, but that text is on line 8; `under-varsea` quotes
  `recovered_pass_path.exists()` at line 10, where line 10 is
  `assert recovered_pass_path.exists(), "Recovery file not found"`. (The counter's `norm()` is a whitespace
  collapse; the mismatch is in the *substring* and the ≥2-word rule, not in whitespace.)

## 6. Order of operations — the claim holds

`plans/order_check.py --lane <lane> --claims plans/round-45-claims.md --receipt corpus/evidence/round45/password-recovery-probe.txt`
on the live lane (the receipt committed at `05b02e2`, the freeze at `b4fcd35`):

```
ORDER claims=plans/round-45-claims.md round=45 freeze=b4fcd35141acda5fa0980a34dd29ab880b702ee6
ORDER receipt=corpus/evidence/round45/password-recovery-probe.txt receipt_commit=05b02e2b7894a9c83219685f2374905e11c1beda claims_dir=.ufo/waves/round-45/claims/
ORDER scanned commits=2 file_entries=32 distinct_blobs=18
ORDER ok no claims file committed at or before the receipt shows the frozen probe executed
ORDER RESULT PASS
```

I also checked every committed blob under `.ufo/waves/round-45/claims/` on every commit for a
`CASE … observed=` line: **none**. So no pre-freeze full-probe run is evidenced anywhere in history, and the
L1's 23:27:11 run (after the 21:24 freeze) is correctly the first recorded one. My run at 23:28:39 is the
second and is byte-identical to it.

## 7. What I changed

Nothing in the lane. I wrote only:

- `.ufo/waves/round-45/w1/R45ProbeFirst.md` (this report),
- `.ufo/waves/round-45/w1/R45ProbeFirst/password-recovery-probe.txt` (the receipt draft, bare stdout),
- `.ufo/waves/round-45/w1/R45ProbeFirst/envelope-transcript.txt` (the ENVELOPE lines).

All scratch under `/fast/scratch/hyaku/kengaku-r45/R45ProbeFirst`, deleted with
`python3 plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r45 R45ProbeFirst "$S"`.

## 8. Risks / caveats

- I did **not** modify the lane, the spec, the counter, the gate, the entry, `SOURCES.md`, `PROVINCE.md` or
  `README.md` — all the fixes in §5 need the L1 (they touch frozen or L1-owned files).
- `P5` cannot be fixed by editing the capture tree: the manifest and the captures are frozen, and the counter's
  own `CAPTURES` dict already uses the nested names, so the spec's flat `capture` field is the outlier.
  *(Superseded by §9: the attempt-2 L1 resolved this by flattening the capture tree and re-pinning the spec
  and counter.)*
- The `dir-state` note `error=IsADirectoryError` is new information relative to the dry table (which predicts
  only `PF`). It does not change the verdict, but the entry's mechanism row for `dir-state` should quote a line
  that actually says what happened (§5c).
- `P9` (`untracked=83…120`) is a working-tree state, not a defect of the package; it will settle when the L1
  commits.
- Tooling: no installs were needed or made this round (`bwrap`, `python3`, `zip`, `dd`, `strings`, `grep`,
  `od`, `tr`, `date`, `find`, `awk`, `sort`, `cut`, `head`, `sed`, `seq` all present on the host, verified).

## 9. Follow-up after the attempt-2 L1's fixes (measured 23:41–23:47)

The attempt-2 L1 (`KengakuR45-2`) acted on §5 while I was finishing this report. I re-measured the live lane
after each change. **My probe result is unaffected** (§§1–4 stand), and the §5 defects are now largely closed.

**Closed and verified on the live lane** (`pkg_gate.py package --root <lane> --spec <effective> --rerun`):

```
P1 ok pinned=2 mismatched=0
P2 ok receipt_sha256=pinned
P3 ok rows=19 distinct_quotes=19 distinct_lines=19 out_of_word_range=0
P4 ok checked=19 bad=0 first=0
P5 ok manifest_entries=9 bad=0 first=0
P6 ok rows=8 bad=0 first=0
P7 ok source_lines=8 bad=0 first=0
P8 ok index_rows=52 knowledge_files=52 bad=0 first=0
P10 ok probe_rerun=byte-equal bytes=4659
gate defects=0
```

The receipt is now 4659 bytes with **0** `ENVELOPE ` lines, and a fresh probe run is byte-equal to it — my §5
P10 fix is confirmed landed. The L1 flattened the capture tree to the flat-basename convention the spec and
counter use, which closed `P3`/`P4`/`P5`/`P7` at the same time.

Live counter now: `checks=11 defects=2` (was 3), `V2` and `V10` still open; `V1`, `V3`–`V9`, `V11` all ok;
`V8 ok order_exit=0 result=PASS`.

**Still open, both with `KengakuR45-2` (reported to it directly):**

1. **`V10` — four `## Mechanism` rows.** The counter requires the quote to be on the cited line
   (`q not in norm(lines[int(line)-1])`) *and* to be ≥2 words (`len(q.split()) < 2`). The four failing rows are
   `constant-crlf` and `dir-state` (`test_outputs.py:14`, quote `read_text().strip().split("\n")`),
   `crlf-line` (`test_outputs.py:14`, quote `strip().split("\n")`), and `under-varsea`
   (`test_outputs.py:10`, quote `recovered_pass_path.exists()`) — each is a single word, and none is a
   substring of its cited line. Verified corrections, each verbatim on the cited line and ≥2 words:
   - line 14 → `guesses = Path("/app/recovered_passwords.txt").read_text()` (3 words, in-line)
   - line 10 → `assert recovered_pass_path.exists(), "Recovery file not found"` (6 words, in-line)
   (`DECISIVE` allows `under-varsea` only lines (9,10) and `dir-state` only (10,14), so the cites stay on 10/14.)
   The other 12 mechanism rows pass.
2. **Freeze bookkeeping.** The L1 changed the frozen probe (`f87a9eeb…` → `9363e03e4ae3ef12f5cdc901c707922bf472222a98eecb079fa8075ac1beb4ab`),
   the spec, `SHA256SUMS` and the counter, but `plans/round-45-claims.md` is unmodified and the committed
   `.ufo/waves/round-45/claims/frozen-digests.txt` still lists the pre-change digests
   (`f87a9eeb…` probe, `916042fb…` SHA256SUMS, `804df725…`/`8c302709…` counter, `b8fc1e53…` spec). The live
   counter pins `PROBE_SHA256=9363e03e…` and `SPEC_SHA256=2f924ffae0b6d0a3346e23b106ec3d5ea03689222923e82509891238649e8244`,
   and the live spec pins the new probe digest — so counter and spec agree with each other, but the freeze
   commit `b4fcd35` and `frozen-digests.txt` no longer describe the tree. The spec is a frozen artefact per the
   task spec and my seat was told not to change it, so the re-pin and the claims-file update are the L1's call.
   Worth noting: `V5` now passes only because `PROBE_SHA256` was re-pinned in the same edit that changed the
   probe, so that "frozen probe" check is now self-referential — a line in the claims file naming the
   pre-data freeze correction would make the re-pin legible.

Also noted for the L1: `P9` (`untracked=159`, first `.ufo/waves/round-45/make_wave2_spec.py`) is working-tree
hygiene and clears on commit; `P2` wants the spec's `receipt_sha256` filled with the committed receipt's digest
so the gate is self-consistent outside the counter's runtime override.

**The order gate stays green** through all of this (`V8 ok order_exit=0 result=PASS`): the receipt commit
`05b02e2` is after the freeze `b4fcd35`, and no committed claims blob carries a `CASE … observed=` line.

VERDICT: probe-first-cases-16-mismatches-0
