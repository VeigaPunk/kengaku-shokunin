# R41CritProbe — attack on `plans/constraints_probe.py` and `corpus/evidence/round41/constraints-probe.txt`

Seat: critic (leaf). Scope: the frozen C2 probe and its receipt — are the 25 cases the end states their
texts claim, is the sandbox faithful where it matters, are the `violates=` tags right per instruction line,
is the CRLF/integrity claim true, is the ground truth right. Nothing frozen was edited; the lane's
`plans/`, `corpus/`, ledgers and git index were read only. Every run used the mandated envelope

```
BWRAP="bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
       --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent"
$BWRAP <cmd>          # scratch TMPDIR=/fast/scratch/hyaku/kengaku-r41/R41CritProbe (deleted at the end)
```

Receipts kept beside this report: `reproduction.txt`, `ground-truth.txt`, `build-vs-text.txt`,
`extra-end-states.txt`, `probe-run1.txt`.

## 1. What reproduces (soundness baseline)

| check | command | output |
|---|---|---|
| captures at pinned digests | `cd corpus/evidence/round41/tb2-constraints-scheduling && sha256sum -c SHA256SUMS` | 10/10 `OK` |
| receipt reproduces | `$BWRAP python3 plans/constraints_probe.py --lane . --work $S/w1` then `diff -u corpus/evidence/round41/constraints-probe.txt` | `IDENTICAL`, 5775 bytes, rc 0 |
| second process, second `--work` | same, `--work $S/w2`, `diff run1 run2` | `IDENTICAL` |
| dry table == frozen table | `--dry` vs `corpus/evidence/round41/constraints-dry-cases-freeze.txt` | `IDENTICAL` |
| probe's `PINS` == grader's `_EXPECTED_SHA256` (test_outputs.py:27-38) | by inspection | same three digests |

So the receipt is reproducible byte-for-byte on this host, and `PINS` really are the grader's own digests.

## 2. Ground truth: correct

Independent enumeration (`ground-truth.txt`) from the three captured calendars and the instruction's
constraints only — never the grader — over every minute of Mon 15 – Fri 19 Jan 2024:

```
valid_slots 2
   Wed 2024-01-17 11:00 UTC
   Thu 2024-01-18 11:00 UTC
earliest Wed 2024-01-17 11:00
carol_max_dtend 12:00 late_events(>=16:45) 0
```

The probe's docstring (constraints_probe.py:27-33) states exactly this, and its per-person busy list matches
the captures event-for-event (8/6/6 VEVENTs). `solve.sh`'s 30-minute scan with the same constraints also
lands on Wed 11:00 (score tie with Thu 11:00 broken by time). No defect here.

## 3. Build vs text: every case builds what it says, with two wordings that lie

`build-vs-text.txt` rebuilds all 25 end states host-side through the frozen `apply_edit` and the same bytes
`run_case` writes (`shutil.copyfile` + `apply_edit` + `meeting.encode()`), then parses the result. All 25
match their text on slot, summary, attendee count, header set and edit target:

- `later-valid-wed-1105` → `20240117T110500Z/20240117T120500Z`, 3 attendees (as written);
- `decoy-first-vevent` → decoy `Wed 11:00 att=0` first, `Fri 15:00 att=3` second (as written);
- `decoy-second-vevent` → `Fri 15:00 att=3` first, decoy second (as written);
- `input-appended` / `input-event-deleted-wed-1000` / `input-crlf-rewrite` → `inputs_byte_ok=False`,
  and `alice_wed10_present=False` only for the deleted case (the edit hits the intended VEVENT and nothing else);
- `no-prodid-header` → header set `V` only; `duration-90min` → 11:00-12:30; `missing-carol` → `att=2`;
  `tzid-form` → `TZID=UTC:…` with no `Z`; `dtstart-value-datetime` → `VALUE=DATE-TIME:…Z`.

The two exceptions are wording, not construction: **D3** and **D2** below. No case's verdict is unsound: I
re-derived the mechanism of every non-obvious result (nop→`FileNotFoundError` in all three tests;
tzid/value→`_dt`'s regex at test_outputs.py:40-43 never matches; folded→the `all(e in b)` test at :112;
lowercase→the literal `"SUMMARY:Team Planning Meeting"` at :112; decoy-first→tests 2-3 take `s` from the
whole file at :135/:151, not from the meeting block at :125-126; seconds-30/wed-1059/bob-0900→earliest
scan :158-166; deleted-input→conflict check reads the tampered `/app`).

## 4. Sandbox faithfulness where it matters: correct

`extra-end-states.txt` prints the namespace built by the probe's own `sandbox_argv()`:

```
DIAG cwd=/app
DIAG app=['alice_calendar.ics', 'bob_calendar.ics', 'carol_calendar.ics']
DIAG inputs_exists=False   DIAG tests_exists=False
DIAG resolved=/cap/test_outputs.py   DIAG inputs_branch=/inputs exists=False
DIAG root=['app','bin','cap','dev','etc','harness.py','lib','lib64','proc','recipe.sh','sbin','tmp','usr']
```

- `/app` holds exactly the three calendars, as `COPY inputs/ /app/` (Dockerfile:14) with `WORKDIR /app`
  (Dockerfile:4) builds it; the captures' `inputs/` had exactly those three files.
- The `/inputs` branch: in the image the tests run from `/tests/test_outputs.py` (test.sh:22), so
  `Path(__file__).resolve().parent.parent` is `/` and `/inputs` is absent — the digest branch at
  test_outputs.py:94-96 is the live one. The probe's `/cap` binding yields the same `/` and the same absent
  `/inputs`; identical branch. Verified, not assumed.
- The verdict mapping matches the reward rule: test.sh:25-29 writes reward 1 iff pytest exits 0, i.e. iff no
  test fails; the harness maps AssertionError→F and any other exception→F, pytest-compatible for this grader.
- Nothing from the lane, `/home` or `$HOME` is visible inside the sandbox; the outer envelope is the
  operator's, so no shared-PATH write is possible.

Fidelity gaps that are declared, not hidden: host `/usr/bin/python3` is **3.14.8** here while the verifier
pins `uvx -p 3.13` (test.sh:18-21) — the docstring says "host python3 stands in for the image's Ubuntu 24.04
python3 (… uvx -p 3.13)", i.e. it names 3.13 but does not record the actual host version; recipes run as
`vgpnk`, not root; the image is never pulled. None of these can change a verdict for this grader (stdlib
`re`/`hashlib`/`datetime`, ASCII inputs).

## 5. The two headline claims: both true, one of them broader than the receipt shows

**CRLF rewrite passes although instruction.md:17-18 says any modification fails — TRUE, re-derived by hand.**
test_outputs.py:91-96 takes `app_text = …read_text()` (universal newlines) and hashes `app_text.encode()`, so
any pure newline re-encoding normalises back to the pinned bytes. Independent derivation
(`extra-end-states.txt`):

```
LOOPHOLE alice_calendar.ics crlf_readtext_sha=5a5d45804bffd339 pinned_match=True byte_match=False
LOOPHOLE bob_calendar.ics   crlf_readtext_sha=c97e85dbcdd75675 pinned_match=True byte_match=False
LOOPHOLE carol_calendar.ics crlf_readtext_sha=32a0f8687637df0a pinned_match=True byte_match=False
```

and my extra end state `input-cr-only` (lone-CR line ends) also passes 3/3 → the loophole is newline
representation in general, not CRLF specifically. The receipt's `input-crlf-rewrite` is one instance of a
class; the frozen text does not say so.

**"RFC 5545-valid forms fail the structure test" — the conclusion is true, but all three frozen witnesses are
LF-only files, so none of them is itself RFC 5545-conformant.** The receipt's evidence therefore does not
demonstrate the sentence it supports. Strictly conformant end states (CRLF breaks) that I graded through the
frozen `run_case`:

```
EXTRA crlf-folded            tests=FPP   (fold per RFC 5545 3.1: CRLF + space)
EXTRA crlf-lowercase-summary tests=FPP   (property names folded to lower case, RFC 5545 2.1)
EXTRA crlf-value-datetime    tests=FFF   (DTSTART;VALUE=DATE-TIME:…Z)
```

So the finding survives; the witness does not isolate it (D1).

## 6. Defects

Ordered by severity. None blocks admission — each is a caveat the entry must carry, or a wave-2 case — but
all five make the frozen receipt state more than its artefacts show.

**D1 — the three "RFC 5545-valid" witnesses are not RFC 5545-valid files.**
`plans/constraints_probe.py:113-114` (`FOLDED_ICS = GOOD_ICS.replace(… "\n ple.com\n")`) and
`:115`/`:116-118` derive every RFC-form case from `GOOD_ICS` (`:109`), which uses `HDR`'s LF endings (`:95`);
build check confirms `crlf=False folded=True`. RFC 5545 3.1 requires CRLF breaks, so
`folded-attendee-line`, `lowercase-property-names` and `dtstart-value-datetime` are each non-conformant on the
line-break axis as well as on the property they test, while the receipt's text and the claims file
("RFC 5545-valid forms fail") assert conformance. Counterexample/evidence: my `crlf-folded`,
`crlf-lowercase-summary`, `crlf-value-datetime` are conformant and produce FPP/FPP/FFF, i.e. the claim is
right and the frozen evidence is impure. Smallest safe correction (wave 2, needs an unfreeze): add the
CRLF-form case(s), or add one limits line — "the RFC witnesses are LF files; the fold/case/VALUE findings
also hold for CRLF-conformant files, graded in `<receipt>`".

**D2 — `lowercase-property-names` misnames the failing property.**
`plans/constraints_probe.py:187` says "lowercase SUMMARY/ATTENDEE names"; the ATTENDEE check is
`re.I | re.M` (test_outputs.py:122), so lower-case ATTENDEE property names are accepted. Only the literal
`"SUMMARY:Team Planning Meeting" in b` (test_outputs.py:112) is case-sensitive. Evidence: my end state
`lowercase-attendee-only` (upper-case SUMMARY, lower-case `attendee;cn=`) is **PPP**. The receipt therefore
overstates the grader's strictness. Smallest correction: "lowercase SUMMARY property name (the ATTENDEE regex
is case-insensitive)".

**D3 — `later-valid-wed-1105`'s description contradicts its own tag set and its observed result.**
`plans/constraints_probe.py:139-141`: the text ships "Wed 11:05-12:05, predicted valid but late", but the case
also carries `violates=("earliest","no-conflict")` and is observed `PFF` — test 2 fails on Carol's 12:00-12:30
lunch and Bob's Wed 12:00 event (test_outputs.py:72-75, :143), i.e. the slot is *invalid*, not "valid but
late". The receipt prints this string verbatim (`constraints-probe.txt:10`). Carried from the pilot, but it is
the one case whose prediction missed, so a reader gets the wrong model from the description. Smallest
correction: "Wed 11:05-12:05: later than the earliest valid slot and invalid (Carol's lunch, Bob's 12:00
event); the pilot predicted valid-but-late".

**D4 — `decoy-second-vevent` is labelled "the pilot decoy's mirror" but is non-discriminating.**
`plans/constraints_probe.py:182-184` puts the *meeting* first at Fri 15:00 and the decoy second, so the
published defect (tests 2-3 read the first `DTSTART`, test_outputs.py:135/:151) and a *correct* grader both
evaluate Fri 15:00: `_hard_ok` rejects it via Alice's 14:00 cap (test_outputs.py:61), so both produce PFF —
the observed verdict. It only rules out a "last DTSTART" reading. Evidence: `build-vs-text.txt` shows the
event order, and the receipt's `tests=PFF` is explained entirely by the Fri 15:00 slot. Smallest correction:
relabel ("meeting first at a slot its own hard window rejects: confirms tests 2-3 do not read the *last*
VEVENT"), or add the discriminating variant (meeting invalid *and* first vs valid decoy second already
covered by `decoy-first-vevent`).

**D5 — the tag vocabulary cannot carry the receipt's sharpest finding.** `plans/constraints_probe.py:81-93`
defines 11 tags covering instruction lines 1, 10, 12, 15, 23, 25, 27. Lines **21** ("Output file must be in
valid ICS format"), 22, 24, 26, 28, 29, 30 have no tag, so the three conformant-rejected cases carry
`violates=()` and the C2 counter's V7 map — built "from ALL receipt cases whose `violates=` carries the tag"
(claims file, C2/Counter) — has **no row for instruction.md:21**. The grader's contradiction of an explicit
instruction line is thus unrepresentable in the requirement map, and V7 cannot show it. The empty `violates=`
is the *correct* encoding under V7's three labels (tagging those cases would make the label "enforced", which
would invert the truth), so the defect is the vocabulary/V7 pair, not the individual case. Smallest safe
correction now (no unfreeze): the entry must state the :21 contradiction in prose and must not let V7's map
imply :21 is enforced; wave 2: add a `valid-ics` tag whose cases V7 reports as "grader stricter".

## 7. `violates=` tag audit

All 11 citations are textually right — checked line by line against the capture
(`instruction.md:1` = window; `:10` = output file/title/attendees/one-hour; `:12` = hard constraints and
no-conflict; `:15` = read-only inputs; `:23` = VERSION/PRODID; `:25` = UTC format; `:27` = earliest). Two
observations on top of D5:

- **Two meanings on the same field.** For a failing case a tag normally names the requirement the artefact
  violates; for `bob-start-0900-wed` (`:146-148`) and `wed-1059-overlaps-alice` (`:171-173`) `earliest` is
  tagged although the artefact *does* satisfy the earliest test (tests=PFP) — the tag there marks a grader gap
  ("the test that should have caught the other violation"). Both meanings feed V7's `mixed` label, which is
  harmless for the label but makes the tag list un-auditable as "violated requirements".
- **Line 15 vs 17-18 for the CRLF case.** `inputs-readonly` cites `instruction.md:15`; the sentence the case
  actually contradicts is at `:17-18` ("exactly match the repo inputs. Any modification will cause the tests
  to fail"), which is what the claims file quotes. Since 17-18 is a *false prediction of the tests* rather
  than a requirement on the artefact, citing :15 is defensible; the entry's prose and the map row will cite
  different lines and should say so.

## 8. Coverage: two requirements can never be exercised on these inputs

`ground-truth.txt` shows the pinned calendars admit exactly two valid slots, both at 11:00, on Wed and Thu.
Consequences, provable rather than sampled:

- test E's Monday tie-break (`test_outputs.py:171-185`) can never fire: `same_minute_candidates` is non-empty
  only at clock 11:00, where it is {Wed, Thu} — `has_monday` is always False.
- both Carol late-buffer blocks (`test_outputs.py:191-208`) can never assert: Carol's latest `DTEND` is 12:00
  and `late_events(>=16:45) 0`, so `end.hour > 16` and the `ee.hour >= 16:45` loop are dead.
- therefore instruction lines 29 (tie-breakers) and 30 (Bob's afternoon preference) are unexercisable, and
  the README's claims "tie-breakers applied correctly, Carol's buffer rule enforced" (`README.md:40`) and
  "Original calendar files remain unmodified" (`README.md:41`) are untestable/overstated on this dataset.

The receipt is silent about this. For the entry that is a *limit*, not a defect of the probe; it does mean
"an embedded scheduling model" should be scoped to `_hard_ok` + `_overlap` + the earliest scan.

Also worth one line in the entry: a malformed output with `DTSTART` but no `DTEND` is **FPP** (my
`no-dtend`) — the 1-hour requirement is only ever checked by the structure test, which is what
`duration-90min` already shows for the 90-minute variant.

## 9. Provenance

The receipt header prints `@ terminal-bench-2 2fd12b88`; nothing in the capture set carries that revision
(README/Dockerfile/test.sh carry no commit), so the revision is an unchecked literal and the verifiable
binding is the digest pin (`PINS`, `SHA256SUMS`, and the grader's own `_EXPECTED_SHA256`, which agree). Fine
as a receipt, but the entry should cite the digests as the pin and the commit as the L1's opening, not as
something the receipt proves.

## 10. Limits I could not remove

- No image pull and no `uvx -p 3.13`; graded with host python 3.14.8 (declared, but the actual host version is
  not in the receipt).
- `regrade=` (receipt `regrade cases=25 differ=0`, `:358`) re-grades the unchanged directory in the same
  process; it cannot detect cross-process nondeterminism and is expected to be `same` by construction. The
  docstring is honest about the mechanism (`:23-25`) but calls it "Re-run stability"; my two-process rerun is
  the stronger control and also came out identical.
- A grader that failed at import would surface as probe `SETUP` (rc 2), not as a grade, unlike pytest's
  exit 2/reward 0. Unreachable with this stdlib-only grader.
- I did not run `plans/round41_c2_verify.py` (other seats' lane); the V7-label consequence in D5 is derived
  from the stated rule and the 11 frozen TAG lines.

## 11. Impacted axes and routing

- **Coverage (7, chosen):** unchanged by this review; D1/D5 and §8 are caveats the entry must carry, and §8's
  dead tie-break/buffer code narrows what "embedded scheduling model" may claim.
- **Depth/soundness:** probe verdicts are reproducible and correct; the ground truth is independently confirmed.
- Route to the C2 scribe/L1: D1→limits line or two extra cases (unfreeze), D2/D3/D4→description fixes
  (unfreeze) or a "known imprecise case text" note, D5→entry prose must own the `instruction.md:21`
  contradiction, §8→entry limit sentence, §9→cite digests as the pin.
- Nothing frozen changed; scratch `/fast/scratch/hyaku/kengaku-r41/R41CritProbe` removed after the receipts in
  this directory were written.

VERDICT: probe-defects-5
