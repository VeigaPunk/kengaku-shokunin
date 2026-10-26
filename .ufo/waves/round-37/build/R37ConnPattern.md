# R37ConnPattern — cross-claim pattern finder (C1 observability × C2 verdict-echo)

Seat: R37ConnPattern (connector, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Read-only seat: no lane file touched, no scratch clone needed (no fixtures built), no tools installed.

## Axes

- **calibration**: is the lane's own C1 verdict channel as spoofable as the TB2 grader C2 exposes?
- **coverage**: do the recurring grader classes generalize across the three TB2 graders, and what is their smallest shared rule?

---

## Q1 — Does the lane's own gate or counters have the C2 failure class?

C2's failure class, precisely: *the verdict token is read (grepped) from output text that the checked
artefact controls.* In the pinned grader the artefact is the HTTP response body and the verdict channel
is `verify.sh`'s stdout: `verify.sh:62` runs `echo "Content: $CONTENT"` (body echoed verbatim) while
`test_outputs.py:13` decides with `assert "TEST PASSED" in result.stdout` — so a body containing the
literal `TEST PASSED` passes even though `verify.sh:63` reports `TEST FAILED` (receipt case
`token-in-body`, observed pass; also `wget-token-in-body`). The lane has **no site where a verdict
token (`ok`/`DEFECT`/`pass`, exit code) is grepped from instrument or artefact text.** Two sites read
*verdict inputs* from artefact-controlled text, and one clause is the lane's own exemplar of the
correct defense. Enumerated:

### Site 1 — C2 counter V4/V7 grep verdict labels out of the receipt file (C2 class present, defended by P10)

- `plans/round37_c2_verify.py:132` — `obs = [re.search(r" observed=(pass|fail)\b", l) for l in cases]`
- `plans/round37_c2_verify.py:133` — `no = [l.split()[1] for l in cases if " match=NO " in l]`
- `plans/round37_c2_verify.py:176-178` — V7 builds `observed[case] = pass|fail` from the same receipt lines.

The receipt is a file the C2 package author writes. V4 checks only structure: case ids equal the frozen
dry table, summary `cases=22 observed_pass=…` internally consistent, `match=NO` ids named in the entry.
Nothing in V1–V7, V4 or V7 re-runs anything to regenerate the receipt — so **a hand-typed receipt that
copies the frozen case table passes V4 and V7 structurally.** This is exactly the TB2 grader's class:
verdict labels read from text the artefact under test controls. The skip-control
(`.ufo/waves/round-37/claims/control-c2-skip.txt`, built by `claims/make_c2_skip.py`) confirms it: it
carried a hand-typed receipt and went out V2-red (quote shape, teaches, fresh re-run not byte-equal) —
**not** V4- or V7-red. The only thing standing between a fabricated receipt and `PREDICATE C2 pass` is
gate clause P10 inside V2: `plans/pkg_gate.py:267-286` re-runs the frozen probe
(`plans/pkg-spec-r37.json` pins `probe_cmd = ['plans/git_webserver_probe.py', '--lane', '.']` and
`frozen_instruments` pins the probe *and* the gate) with `cwd=package root` and requires
`r.stdout == want` byte-equal (`pkg_gate.py:283`). The probe's inputs (the six captures) are digest-pinned
by P5 and the spec rows. So the C2 counter **does** contain the C2 failure class at the receipt layer and
**defends it with the anti-C2 pattern itself** — re-derivation of the verdict text by a pinned
instrument. If P10 were removed or silenced (mutant M43), a fabricated receipt would pass C2; that is
presumably why M41–M43 exist in the C1 mutant list: the lane's calibration claim and its C2 defense are
the same mechanism.

  Limits of the defense (second-order, not defects under the frozen rules): `r.stderr` is never compared;
  the comparison is whole-stdout equality, so any instrument nondeterminism fails the gate rather than
  being spoofed; and a *degenerate* instrument that just prints its receipt would pass P10 — out of scope
  only because the probe's bytes are digest-pinned (P1).

### Site 2 — C1 counter parses gate stdout whose note payload is fixture-influenced (bounded injection, kill decision unspoofable)

- `plans/round37_c1_verify.py:59` — `CLAUSE_LINE = re.compile(r"^(P\d+|D4|D5) (ok|DEFECT) ")`
- `plans/round37_c1_verify.py:276` — the observed defect set is `frozenset(...)` of clause ids parsed
  from gate stdout; exit code taken from `r.returncode`.

The verdict tokens (`ok`/`DEFECT`, clause ids) are printed by gate-side f-strings
(`pkg_gate.py:301-305` `print(f"{name} {'ok' if ok else 'DEFECT'} {note}")`), never read from fixture
text. But the *note* payload is fixture-influenced, and one note embeds a raw fixture-controlled
filesystem string **unescaped**: `pkg_gate.py:181`
`bad.append(f"{f.name}: capture file not covered by the manifest")` — `f.name` from
`capdir.iterdir()` (line 178) can contain a newline. A capture file named e.g. `x\nP2 DEFECT forged`
would inject a phantom `P2 DEFECT` line into gate stdout, which `CLAUSE_LINE` at counter line 276 then
counts. Ceiling of the spoof, traced:

- it can only **add** phantom ids to the observed DEFECT set — genuine `DEFECT` lines are never removed
  and the exit code is untouched;
- reference, null and mutant runs execute the same fixture bytes, so the injection is identical across
  the comparison — **it cannot manufacture a kill** (a mutant's result differs from reference only via
  the gate branch it silences);
- a battery37 fixture could declare the phantom id and match (`wrong` stays 0), but it demonstrates
  nothing: every mutant sees the same phantom, so no clause gains a kill through it.

Adjacent raw-name notes are safe: `pkg_gate.py:150` P4's `first={bad[0]}` embeds `q.capture`, which
comes from a single-line `QUOTE_ROW` match (a newline cannot appear in one matched row), and
`pkg_gate.py:265` P9's `first={left[0]}` is git C-style-quoted for newline-bearing paths in captured
(non-tty) output. All other notes use `!r` repr or counts.

### Site 3 — gate P10 (c_rerun) is the anti-C2 pattern, not the failure class

`pkg_gate.py:267-286`: verdict = byte-equality of a *fresh* instrument run against the package's
receipt, with the instrument digest-pinned. The verdict text is re-derived, not artefact-read. Note the
asymmetry with the round-36 battery: `plans/round36_c1_verify.py:122-123` (`stub_probe`) overwrites the
probe inside every r36 fixture with a stub that just `sys.stdout.write(receipt)` — so for the 14 frozen
r36 fixtures, P10 always passes trivially and **M41–M43 were unkillable by the r36 battery by
construction**; only battery37 fixtures built on `ctx.genuine_package(d)` (real probe bytes, real
captures, cwd=fixture) can kill them — e.g. a fixture whose receipt differs from a genuine fresh probe
run kills M43; a fixture with the receipt deleted kills M41/M02 (both runs) with reference showing
`{P2,P10}` vs the M41 mutant's `{P2}`. This is a calibration-relevant second-order effect: C1's
"observable result" for P10 is observable only against genuine-package fixtures, which is precisely the
fixture rule the claims doc mandates.

**Net answer:** no lane counter greps its own `PREDICATE … pass` or any verdict token from instrument
output. Two sites read verdict *inputs* from artefact-controlled text — V4/V7's receipt labels (the C2
class, defended by P10's pinned byte-equal re-run) and the C1 counter's parse of note-bearing gate
stdout (one unescaped-filename injection path at `pkg_gate.py:181`, ceiling = phantom DEFECT lines,
symmetric across reference/mutant, kill decision unspoofable). P10 is the lane's own correct
implementation of the anti-C2 defense, and the C2 counter's authenticity claim reduces to it.

---

## Q2 — Recurring grader classes across the three TB2 graders, and their smallest shared rule

Evidence base: `corpus/knowledge/tb2-protein-assembly-grader.md` (r35, S105–S107),
`corpus/knowledge/tb2-regex-log-grader.md` (r36, S108–S110), `corpus/evidence/round37/tb2-git-webserver/`
(S111–S113) with its executed receipt (`cases=22 observed_pass=9 observed_fail=13 mismatches=0`).

Six classes recur (present in all three unless noted):

1. **Single-bit reward by exit-status mapping.** One pytest function → `test.sh` exit →
   `reward.txt` 1/0: protein `test.sh:26-30` ("if [ $? -eq 0 ]" / "echo 1 > /logs/verifier/reward.txt");
   regex `test.sh:25-29` (same two lines at 26/28); git-webserver `test.sh:21-24`. Partial credit is
   representable by none of them.
2. **Literal oracle embedded in the grader file** — the expected answer never leaves the test file:
   protein `flag_aa = "DYKDDDDK"` (`test_outputs.py:28`) plus four more aa literals; regex the nine
   `expected_dates` literals (`test_outputs.py:71-81`) plus the 25-line log; git-webserver the literal
   `[ "$CONTENT" = "hello world" ]` (`verify.sh:63`) plus the literal status `200` (`verify.sh:59`).
3. **Fixed artefact channel:** `/app/gblock.txt` (`test_outputs.py:13`), `/app/regex.txt`
   (`test_outputs.py:21`), `http://localhost:8080/hello.html` (`verify.sh:57,60`).
4. **Normalization asymmetry:** each grader normalizes some faces while leaving requirement-relevant
   faces strict or silent — protein lower-cases and rstrips (`test_outputs.py:16,21`) but admits G-only
   linkers (`[GS]+`, `test_outputs.py:54`); regex `strip()`s the file (`test_outputs.py:25`) but the
   fixture cannot see leading-zero octets, digit-adjacent dates or year width; git-webserver strips only
   trailing newlines via command substitution (`verify.sh:60,63`) while case, BOM, CR and leading space
   fail (receipt cases `capitalised`, `bom`, `crlf`, `leading-space`).
5. **Fixture-bounded enforcement (unobserved requirement faces):** a stated requirement is enforced
   only if the grader's own fixed fixture contains a distinguishing case — protein: the 3000-nt cap
   never decides (longest passing 2768 nt), G-only linker passes; regex: six unobserved faces (the
   hard-coded alternation `hardcoded-expected-dates` passes); git-webserver: the git server, hook and
   push are never read — `static-file-no-git` passes (`verify.sh:49` never reads the expect step's
   status). All three receipts carry an executed row proving the unenforced face.
6. **Verdict/message divergence (echo channel):** full strength only in git-webserver — the verdict is
   a substring of stdout that echoes the artefact (`test_outputs.py:13` × `verify.sh:62`,
   cases `token-in-body`, `wget-token-in-body`); in the other two the verdict is computed, but the
   failure *message* echoes artefact content (protein finding 3: `find` returns −1 and the order
   message misattributes a one-residue substitution; regex `test_outputs.py:90` prints the got-list) —
   same divergence class at lower severity, and it matters to any trajectory analysis that reads
   assertion text as cause.

**Smallest cross-grader rule they share:** *no grader reads the task's requirement source at run time —
each is self-referential, checking the artefact against literals baked into its own test file, so a
stated requirement is enforced exactly insofar as the author-fixed fixture happens to distinguish it.*
(instruction.md participates in none of the three verdicts; checked: none of `test_outputs.py` /
`verify.sh` opens the instruction.) One sentence covers the data-string graders (protein, regex) and the
service/state grader (git-webserver) alike — the new class C2 adds is only that in a service grader the
fixture is *live state the agent built*, which is how the echo-verdict flaw (class 6) becomes reachable
from the artefact side.

**Contradiction stated, not smoothed:** the lane's C2 counter both *contains* the C2 failure class
(V4/V7 trust receipt labels) and *implements its refutation* (P10 byte-equal re-run, V2). These are not
in tension under the frozen rules — authenticity is explicitly delegated to P10 (claims file: "P2 is a
presence check here and authenticity rests on P10") — but it means C2's predicate is exactly as strong as
the lane's own gate clause M43 calibrates, which is the C1↔C2 coupling this seat was routed to find: the
same byte-equal-rerun mechanism is the falsifier of the TB2 grader class (grader: no re-derivation;
lane: re-derivation pinned by digest).

## Verification (commands run, outputs observed)

- `grep -n "HTTP_RESPONSE\|CONTENT=\|echo \"Content\|TEST PASSED\|TEST FAILED" corpus/evidence/round37/tb2-git-webserver/verify.sh` → status curl `:57`, comparison `:59,63`, echo `:62,79`, pass/fail banners `:64,66,81,83`.
- `grep -n "if \[ \$? -eq 0 \]…" …/test.sh` → reward mapping `:21-24`.
- `grep -n "r.stdout != want\|return True, f\"probe_rerun\|def c_rerun" plans/pkg_gate.py` → `267,283,285`.
- `grep -n "CLAUSE_LINE =\|def run_gate\|frozenset(m…\|return (r.returncode" plans/round37_c1_verify.py` → `59,270,276,277`.
- `grep -n "observed=(pass\|match=NO\|observed\[m.group" plans/round37_c2_verify.py` → `132,133,176,178`.
- `python3 -c "import json; …"` over `plans/pkg-spec-r35.json` and `plans/pkg-spec-r37.json` → r35 `probe_cmd ['plans/tb2_grader_probe.py','--lane','.']`, `frozen_instruments [tb2_grader_probe.py, round35_c1_verify.py, defect_ledger.py]`; r37 `probe_cmd ['plans/git_webserver_probe.py','--lane','.']`, `frozen_instruments [git_webserver_probe.py, pkg_gate.py]`, `capture_dir corpus/evidence/round37/tb2-git-webserver`.
- Receipt quotes: `cases=22 observed_pass=9 observed_fail=13 mismatches=0` (`corpus/evidence/round37/git-webserver-probe.txt`, last line); case lines for `token-in-body`, `wget-token-in-body`, `static-file-no-git` read in full.
- `grep -n "f.name\|left\[0\]\|bad\[0\]\|first=" plans/pkg_gate.py` → injection candidates at `150,181,265`; repr/`!r` or line-bound provenance for the rest.
- Round-35/36 entry claims (pass counts `cases=18 observed_pass=5`, `cases=24 observed_pass=8`, six unobserved faces, 2768-nt cap erratum) taken from the two knowledge entries as cited above.

VERDICT: pattern-6-spoofable-sites-2-shared-rules
