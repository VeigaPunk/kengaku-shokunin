# F41IndepProbe — independent re-run of the five non-frozen end states in the C2 §Corrections

Seat: critic (leaf), kengaku round 41 wave 2. Target: the five end states the round-41 entry's
`## Corrections at integration (round 41, wave 1)` cites from wave-1 `R41CritProbe`
(`corpus/knowledge/tb2-constraints-scheduling-grader.md:398-434`). I rebuilt each from my own bytes,
graded with the pinned grader, and compared letters.

Envelope for every run (host-safety rule, verbatim):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
      --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>
```

Scratch: `/fast/scratch/hyaku/kengaku-r41/F41IndepProbe` (`export TMPDIR`), removed at the end.
Receipts beside this report: `run-c.txt` / `run-d.txt` (two processes, 38 cases, byte-identical,
`sha256=5c968149cc86a84b…`), `probe-run.txt` (first 34-case pass), `diag.txt` (byte census),
`dry.txt`, and the two drivers `probe_indep.py` (scratch copy of the probe + my cases),
`diag.py` (independent driver, imports none of the probe's code). No lane file was written.

## 0. Non-mutation and the lane state I read

| check | command | output |
|---|---|---|
| lane tip | `git -C …/kengaku-shokunin rev-parse HEAD` | `d7c77895752a…` — wave-2 dispatch commit, parent `3d0058f` (the assignment's named tip), which parents `0d57419` ← `74513c0` (wave-1 landing) |
| nothing frozen moved | `cd …/kengaku-shokunin && sha256sum -c .ufo/waves/round-41/claims/frozen-digests.txt` | `11/11 ... OK` (claims, both counters, probe, pkg-spec, dry table, capture `SHA256SUMS`, `tip_receipts.py`, `sources_adopt.py`, `pkg_gate.py`, `order_check.py`) |

`git rev-parse --abbrev-ref HEAD` prints `HEAD`: the git view of the lane is a detached HEAD at the
dispatch commit. Observation only — I ran no git mutation and wrote no index.

## 1. The five claims vs my independent builds — 5/5 agree

Each end state was constructed in `probe_indep.py` from literal bytes (`crlf(s)` maps `\n`→`\r\n`),
not from the probe's LF constants; the claimed letters are the case's `predicted`, so `match=yes` is
agreement. Graded by the same frozen `run_case` (pinned `test_outputs.py`, digest-verified).

| # | end state | claimed by §Corrections | my letters | observed | agree |
|---|---|---|---|---|---|
| 1 | `crlf-folded` | `FPP` (item 1) | `FPP` | `FPP` | **yes** |
| 2 | `crlf-lowercase-summary` | `FPP` (item 1) | `FPP` | `FPP` | **yes** |
| 3 | `crlf-value-datetime` | `FFF` (item 1) | `FFF` | `FFF` | **yes** |
| 4 | `lowercase-attendee-only` | `PPP` (item 2) | `PPP` | `PPP` | **yes** |
| 5 | `input-cr-only` | "also passes 3/3" (item 6) | `PPP` | `PPP` | **yes** |

Evidence (`run-c.txt`, one line each; letters are Test-1/2/3 in file order):

```
32:CASE crlf-folded           … observed=fail tests=FPP predicted_tests=FPP match=yes regrade=same
33:CASE crlf-lowercase-summary … observed=fail tests=FPP predicted_tests=FPP match=yes regrade=same
34:CASE crlf-value-datetime    … observed=fail tests=FFF predicted_tests=FFF match=yes regrade=same
35:CASE lowercase-attendee-only … observed=pass tests=PPP predicted_tests=PPP match=yes regrade=same
37:CASE input-cr-only          … observed=pass tests=PPP predicted_tests=PPP match=yes regrade=same
…
regrade cases=38 differ=0
cases=38 observed_pass=12 observed_fail=26 mismatches=2
```

`mismatches=2` are the two pilot-carried cases of the frozen table, not my extras (`run-c.txt`):
`later-valid-wed-1105 … tests=PFF predicted_tests=PPF match=NO`, `seconds-30 … match=NO` — the same
two the frozen receipt reports (`corpus/evidence/round41/constraints-probe.txt:33`,
`cases=25 … mismatches=2`), i.e. corrections item 3, unchanged.

## 2. Attribution: each verdict is caused by the named property, not by my construction

The frozen 38-case table includes discriminating controls, so no `F` in rows 1-3 can be blamed on the
line breaks and no `P` in rows 4-5 on a missing edit:

| claim | control | letters | what it excludes |
|---|---|---|---|
| 1 `crlf-folded` FPP | `crlf-line-endings` (frozen, `:24`) | `PPP` | CRLF alone passes ⇒ the fold causes `F` |
| 1 | `lf-folded-control` | `FPP` | fold fails with LF too ⇒ line-break axis irrelevant |
| 1 | `crlf-folded-tab` (RFC 5545 3.1 permits htab continuation) | `FPP` | verdict is not an artifact of the space continuation |
| 2 | `lf-lowercase-summary-control` | `FPP` | the case is the SUMMARY property name, not CRLF |
| 3 | `dtstart-value-datetime` (frozen, `:26`) | `FFF` | the explicit `VALUE=DATE-TIME` parameter is the cause |
| 4 | `lowercase-property-names` (frozen, `:30`, lowers SUMMARY **and** ATTENDEE) | `FPP` | only a lowered SUMMARY fails |
| 4 | `lowercase-attendee-only-crlf`, `lowercase-attendee-plain` (`attendee:` no CN) | `PPP`, `PPP` | ATTENDEE case-insensitivity holds in three constructions |
| 5 | `input-crlf-rewrite` (frozen, `:31`) | `PPP` | newline re-encoding is the family |
| 5 | `input-cr-only-alice` (only one calendar rewritten) | `PPP` | verdict does not need all three files |
| 5 | `cr-only-meeting-file` (the *output* file CR-only) | `PPP` | the hole is not limited to the inputs |

## 3. Byte-level mechanism (independent driver, `diag.txt`)

`diag.py` builds each `/app` itself and, inside the envelope, prints for every file the grader reads:
raw sha256, `sha256(read_text().encode())`, and the CRLF / lone-CR / lone-LF census.

- **`input-cr-only`** — raw bytes differ from the pins, the read-text digest does not:

  ```
  FILE alice_calendar.ics raw_sha=5e05e451390b1d8b text_sha=5a5d45804bffd339 lonecr=79 lone_lf=0 pins_match=True
  FILE bob_calendar.ics   raw_sha=01728ab195b6e53c text_sha=c97e85dbcdd75675 lonecr=61 lone_lf=0 pins_match=True
  FILE carol_calendar.ics raw_sha=9878d6895cb31358 text_sha=32a0f8687637df0a lonecr=61 lone_lf=0 pins_match=True
  ```

  This is exactly `test_outputs.py:90` `app_text = read_text()` → `:95` `sha256(app_text.encode())` →
  `:96` compare to `_EXPECTED_SHA256`: Python's universal-newline translation maps lone `\r` to `\n`,
  so the digest of the *original* LF bytes is recovered from a CR-only file. The three inputs are LF
  at the pins (`raw_sha == text_sha`), so the edit is a real re-encoding, not a no-op.
- **rows 1-3 are genuine CRLF files**: `crlf=13/12/12, lonecr=0, lone_lf=0`; the fold's continuation
  is visible (`folded_cont=True`), the lowercase file has `summary_literal=False` with
  `all_emails=True`, the VALUE file has `value_param=True` and `dtstart_literal=None`.
- **row 4 is a genuine LF file** with `summary_literal=True, all_emails=True`, upper-case
  `DTSTART:20240117T110000Z` ⇒ tests 2-3 pass and test 1's ATTENDEE regex (`test_outputs.py:122`,
  `re.I | re.M`) accepts the lower-case property names.
- **`cr-only-meeting-file`** normalises the same way (`lonecr=12, text_sha` equal to the LF text
  digest), so the output file tolerates lone CR as well.

The frozen constants the item-1 premise rests on are LF-only (host-side, module imported read-only):
`FOLDED_ICS crlf 0 lonecr 0 lf 13`, `VALUE_ICS crlf 0 … lf 12`, `LOWER_ICS crlf 0 … lf 12`.

## 4. Citation check on §Corrections

| claim | location | my check |
|---|---|---|
| "only the literal `"SUMMARY:Team Planning Meeting" in b` (`:112`) is case-sensitive" | `test_outputs.py:112` | `112: if "SUMMARY:Team Planning Meeting" in b and all(e in b for e in EMAILS)` — exact |
| "The ATTENDEE regex is case-insensitive (`test_outputs.py:122`)" | `test_outputs.py:122` | `122: rf"^ATTENDEE[:;].*{re.escape(email)}$", meeting, re.I \| re.M` — exact |
| the three RFC-form witnesses "are built from an LF-ended file" | `plans/constraints_probe.py:95`, `:109-118` | census above: 0 CRLF in `FOLDED_ICS`/`VALUE_ICS`/`LOWER_ICS` |
| "Those three are seat observations outside the frozen receipt" | receipt | `constraints-probe.txt` has `cases=25` and rows for `crlf-line-endings`/`folded-attendee-line`/`dtstart-value-datetime`/`lowercase-property-names`/`input-crlf-rewrite`, and no row for any of the five extras |

## 5. What breaks, and the residual limits

Nothing breaks: **5/5 claimed verdicts reproduce**, and every one is attributable in §2-§3. Limits I
could not remove, stated so the entry does not read stronger than the artefacts show:

1. **Named, not byte-pinned.** The five end states carry no artifact in the lane; I reconstructed them
   from their names and the seat's §5 description. Two independent constructions of each name agree
   (space vs tab fold; `attendee;cn=` vs plain `attendee:`; all-three vs one-file CR-only), so the
   verdicts are construction-robust — but a reader cannot re-derive the seat's exact bytes. That is
   inherent to "seat observations outside the frozen receipt", not a defect of the entry.
2. **Item 1's naming narrows the frozen witness.** `lowercase-property-names` lowers SUMMARY *and*
   ATTENDEE; the correction's CRLF counterpart is `crlf-lowercase-summary` (SUMMARY only). I also ran
   the exact CRLF form of the frozen witness, `crlf-lowercase-property-names` → `FPP` (`run-c.txt:44`),
   which is the same letters, so the mapping is coherent; wording only.
3. **Item 6 is narrower than the mechanism.** "lone-CR line ends also passes 3/3" reads as the inputs;
   the same holds for the output file (`cr-only-meeting-file` `PPP`). If the entry wants the general
   statement — newline representation is not checked anywhere in this grader — the receipt for that
   sentence is my `cr-only-meeting-file` row, not the frozen one.
4. **Environment.** Host `/usr/bin/python3` is 3.14.8, the image pins `uvx -p 3.13` (`test.sh:18`).
   The behaviour the five verdicts rest on (`Path.read_text()` universal newlines; literal `in` tests;
   `re.I`) is version-stable, and the target/relevant code is stdlib-only, but this was not executed
   under 3.13 and no image was pulled.
5. **Determinism.** `run-c.txt` and `run-d.txt` are byte-identical across two processes and two
   `--work` dirs (`sha256=5c968149…` both), `regrade cases=38 differ=0`; the in-process regrade is
   weaker by construction, so the two-process diff is the control.

## 6. Impacted axes

- **Coverage (this seat's axis): improved.** 5/5 claimed end states rebuilt and graded; 10
  discriminating controls/adversarial constructions added (tab fold, plain `attendee:`, one-file and
  output-file CR-only, plus the exact-CRLF frozen witness); mechanism pinned at byte level; frozen
  premise (LF witnesses) verified; 11/11 frozen digests unchanged.
- **Depth/soundness:** no contradiction found; the corrections' three line-break claims and the two
  ATTENDEE/input-integrity claims are true as stated, and each is causally isolated from its control.
- Route to the L1: nothing to change for correctness. Optional one-line precision on item 6 (the
  output file tolerates lone CR too) and on item 1's witness mapping — both already true as worded,
  so no unfreeze is required.

VERDICT: indep-agree-5/5
