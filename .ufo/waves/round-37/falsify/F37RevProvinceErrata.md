# F37RevProvinceErrata — round-37 PROVINCE paragraph and append-only errata (wave 2, falsify)

Seat F37RevProvinceErrata · 2026-10-26 · lane tip `357deceb` · baseline `3ea9a1d9` (round-36 verifier spot-check) · freeze `ca790460`.

Method: every erratum was checked against the bytes it corrects with `sed -n` on the pinned captures; append-only was checked with read-only `git diff 3ea9a1d9..357dece`; the two re-runnable instruments in scope (`plans/anchor_digest_check.py`, the regex-log case table) were re-run on **my own clone** `/fast/scratch/hyaku/kengaku-r37/F37RevProvinceErrata/fx/lane` (checkout `357dece`, `rev-parse --show-toplevel` verified, deleted after; receipts copied to `falsify/F37RevProvinceErrata/`). No lane file was edited; no counter was run on the lane; no subagents.

Items reviewed (every append-only erratum landed this round, enumerated by `grep -n -i erratum` over the round's changed files plus PROVINCE's "correction"):

1. `corpus/knowledge/tb2-regex-log-grader.md:267-318` §Errata (round 37) — three errata: S110 anchor sha256 (`:275`), S110 span (`:282`), the `What decides it` column (`:288`, corrections table `:294-303`, non-independence note `:306`, unchanged-spans note `:316`).
2. `corpus/lessons/round-37.md:32` (S110 anchor erratum line — the line `plans/anchor_digest_check.py` keys on) and `:34` (round-36 spot-check line-drift erratum).
3. `LOG.md:1082-1113` round-37 entry (references the lesson's erratum at `:1103`; carries no erratum of its own).
4. `PROVINCE.md:256-260` correction R37-P1 (appended to the round-36 paragraph) and `:264-285` the round-37 paragraph itself.
5. `plans/anchor_digest_check.py` + `corpus/QUALITY.md` Q26 (`:380-391`) — the instrument that enforces the S110 erratum shape.

---

## 1. S110 anchor erratum — verified against the bytes, no defect

- The row as filed still carries the wrong token (append-only; the row is not rewritten):
  `$ sed -n '125p' corpus/SOURCES.md | grep -oE 'sha256 [0-9a-f]+' | awk '{print length($2), $2}'` →
  `63 4f7ac05e70cf922ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c` — **63 hex**.
- The correct digest, two ways:
  `$ sed -n '3p' corpus/evidence/round36/tb2-regex-log/SHA256SUMS` →
  `4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c  instruction.md`;
  `$ sha256sum corpus/evidence/round36/tb2-regex-log/instruction.md` → same 64-hex value.
- The "index 15" claim: `python3 -c "d='4f7ac05e70cf9220ea0f…f9c'; w='4f7ac05e70cf922ea0f…f9c'; …"` →
  `correct[15]= 0 len 64`, `wrong len 63`, `wrong == correct minus index15: True`. The LOG/lesson phrasing
  ("the `0` before `ea0f` was dropped") is the same fact.
- The erratum is *enforced*, not just written. On my clone at the tip:
  `python3 plans/anchor_digest_check.py --lane .` → `rows=107 tokens=15 defects=0`, exit 0; `--verbose`
  prints `EXEMPT S110 anchor=4f7ac05e70cf922ea0f… by=corpus/lessons/round-37.md:32
  correction=4f7ac05e70cf9220ea0f…` — the exemption is keyed to the exact lesson line `:32`, which I read
  whole and which carries both the wrong token and the committed correct digest.
- Shown able to fail, reproduced by me: clone checked out at `3ea9a1d9`, checker bytes from the tip
  (`git show 357dece:plans/anchor_digest_check.py`) run against the baseline tree → five `DEFECT` lines
  (S070/S072/S073/S074 `digest-unknown` at `:92/:94/:95/:96`, S110 `digest-short detail=63-hex` at `:125`),
  `rows=103 tokens=11 defects=5`, exit 1 — exactly QUALITY Q26's and the lesson's Mistakes-row numbers.
- The four `digest-unknown` rows were closed with byte captures, not with edits:
  `corpus/evidence/round37/anchor-captures/` — `sha256sum -c SHA256SUMS` → 5/5 `OK`, exit 0; each row's
  digest cell equals its capture's manifest line (S070 `45ddba7b…`, S072 `081c8264…`, S073 `97b8671f…`,
  S074 `f996dfee…`); `PROVENANCE.md` records a live fetch from each row's pinned commit on 2026-10-26
  (triple-checked: fetched bytes, row digest, round-29 scratch copy for S070/S072/S073).

## 2. S110 span erratum — verified against the bytes, no defect

`$ wc -l corpus/evidence/round36/tb2-regex-log/instruction.md` → 19 lines. `sed -n` over the capture:
lines 1–4 requirement sentences, 5 blank, 6–7 requirement sentences, 8 blank, 9–10 requirement
sentences, 11 `Example Python usage:`, 12–19 the example code block — exactly as the erratum at `:282`
states. The filed bytes it corrects are still there: the entry's `source:` line says "requirement
bullets, lines 1–11" (includes the non-requirement line 11 — one, as filed) and `corpus/SOURCES.md:125`
says `instruction.md:1-19` (includes lines 12–19 — eight, as filed). Exact bullet anchor `1-10` is right.
The new round-37 rows already use the corrected convention: S113's anchor cell says `instruction.md:1-10`.

## 3. `What decides it` errata — verified by independent re-derivation, no defect

- Receipt shape: `corpus/evidence/round36/regex-log-probe.txt` lines are
  `case=… predicted=… observed=… match=… assertion=… requirement=…` — no per-line field, as the erratum
  says. Assertion counts (my commands): 11 of the 16 `observed=fail` lines carry one byte-identical
  `assertion=` string; 6 distinct strings over the 16 fails; 7 over all 24 (the 8 passes carry `-`).
  All three numbers reproduce exactly.
- **Independent re-derivation of every corrected flip set** (my own script
  `falsify/F37RevProvinceErrata/flipcheck.py`, run on my clone; output `flipcheck-run1.txt`): loads the
  frozen case table from `plans/regex_log_probe.py` (digest `63cb75cf…5eedf`, matches the entry/LOG pin),
  AST-extracts `sample_logs` (25 elements, per-element source lines) and `expected_dates` from the pinned
  capture, computes per-line `re.findall` for each case pattern (after the grader's `.strip()`) against
  the compliant control `reference-month-aware`, and compares. Result: **12/12 flip sets equal the
  erratum's measured sets** — `no-ip-condition` {38,44,45,50,62,63,64,65,67}, `ip-octets-unbounded`
  {44,45,64,65,67}, `ip-no-left-boundary` {44,50,63}, `ip-no-right-boundary` {62,64,65,67},
  `ip-before-date-only` {35,41,59}, `first-date-only` {36,42}, date pair {57}/{56}, month pair {52}/{53},
  day pair {54}/{55}. Control soundness: the control's full-log output equals `expected_dates` (True).
- Receipt cross-check: my own execution of the captured grader function for all 24 cases agrees with the
  committed receipt on every `predicted/observed/match` — `cases=24 disagreements=0` (the erratum's
  "23 file-mode cases: 0 `observed=` mismatches" is the same fact; `regex-file-absent` is the only
  absent-mode case).
- The filed cells the erratum corrects are byte-confirmed wrong: `sed -n '37p;38p'` → 37 is the comment
  `# Y: multiple dates, pick last`, 38 is `No IP here but 2022-05-05 appears`; `sed -n '41p;42p;62p'` →
  none of 41/42/62 carries an out-of-range octet, while 44/45/64/65/67 do (256/456); 60 is a Y sample
  line, 61 a comment, 62 `192.168.1.1abc`, 63 `abc10.0.0.5`; 38 has a date and no IPv4 at all.
- The "unchanged and still correct" claims re-verified: spans 34–68 (`sample_logs`), 84 (`log_text =
  "\n".join(sample_logs)`), 71–81 (`expected_dates`), 87 (`re.findall`), 90 (`assert matches ==
  expected_dates`) all sit on those bytes; `grep -c '1134'` → 0, `grep -c '02-29'` → 0; receipt line 18
  `case=hardcoded-expected-dates predicted=pass observed=pass`. The non-independence arithmetic checks:
  pair union {44,50,62,63,64,65,67} (7 lines), octet-owned {44,45,64,65,67}, intersection {44,64,65,67}
  = 4 of 7, as written at `:306`.
- `sha256sum -c corpus/evidence/round36/tb2-regex-log/SHA256SUMS` (run in the capture dir) → 5/5 `OK`,
  exit 0 — the errata header's stated precondition.

## 4. Round-36 spot-check line-drift erratum — verified against the bytes, no defect

The erratum (`lessons/round-37.md:34`, echoed nowhere as an edit) says the spot-check's "72–82" correction
at `round-36-verifier-spotcheck.md:68,91` is itself off by one. Byte check: `sed -n '68p'` and `sed -n
'91p'` of the spot-check both carry "72–82"; on the pinned capture, `sed -n '71p'` → `expected_dates = [`,
lines 72–80 are the nine literals, `sed -n '81p'` → `]`, line 82 blank — so `round-36.md:18` ("71-81",
verified by `sed -n '18p'`) was right and the spot-check's "72–82" is wrong, exactly as the erratum says.
The spot-check file itself is untouched this round (`git diff 3ea9a1d9..357dece -- …verifier-spotcheck.md`
→ empty): the non-author file was not edited, the correction lives in the lesson and LOG. The round-37
lesson's own S108 row already uses the correct "71-81" span.

## 5. PROVINCE R37-P1 correction — verified, no defect

R37-P1 (`PROVINCE.md:256-260`) supersedes three clauses of the round-36 paragraph; all three exist as
filed (`sed -n '243,255p'`): (a) "over 24 frozen `/app/regex.txt` candidates" next to "The graded artefact
is an agent-authored regex file" — the juxtaposition R37-P1 disambiguates (the frozen probe's cases are
lane-authored patterns; the receipt and case table show no agent output); (b) the refusal list without a
correctness/contamination clause — R37-P1 adds "no regex or log-parsing correctness and no contamination
measurement", consistent with the entry's own negative space; (c) "other 88 TB2 tasks" → "86 of TB2's 89
task graders" — arithmetic 89−3=86, denominator supported by
`corpus/knowledge/benchmark-verifier-execution-model.md:93` ("of its 89 `tests/test.sh` files at the
pinned commit") and by `tb2-git-webserver-grader.md:50`. The PROVINCE diff is one pure-addition hunk
(`@@ -253,5 +253,33 @@`), so the round-36 paragraph stands as filed with the correction appended after it.

## 6. Round-37 PROVINCE paragraph (`:264-285`) — verified, no defect

- Receipt verbatim: `corpus/evidence/round37/git-webserver-probe.txt` ends
  `cases=22 observed_pass=9 observed_fail=13 mismatches=0`; the frozen dry table
  (`git-webserver-dry-cases-freeze.txt`) holds the same 22 case ids in the same order,
  `cases=22 predicted_pass=9 predicted_fail=13`.
- Registry: S111–S113 rows at `corpus/SOURCES.md:126-128` (+S114 at `:129`); row quotes byte-verified on
  the captures — `test_outputs.py:13` `assert "TEST PASSED" in result.stdout, "Did not pass test"`,
  `verify.sh:62` `echo "Content: $CONTENT"`, `instruction.md:9` `then I see the output "hello world".`;
  row digests resolve (`sha256sum -c corpus/evidence/round37/tb2-git-webserver/SHA256SUMS` → 6/6 `OK`,
  exit 0) and the anchor checker resolves all four new rows via the committed manifests.
- Sandbox claims vs `plans/git_webserver_probe.py`: `--unshare-net` (private network namespace),
  `--tmpfs /tmp`, `HOME=/work/home`, `--dir /tests` + `--ro-bind` of the two capture files, `PATH=/work/bin`
  holding only the case's tool symlinks, `expect` bound to `/dev/null` when present — all present in
  `sandbox_argv`/`prepare`/`run_case`. "No root" verified empirically: the probe-shaped bwrap argv running
  `/usr/bin/id` prints `uid=1000(vgpnk)` (identity-mapped, non-root; host uid also 1000) — receipt
  `bwrap-id.txt`. "A service the probe starts": `RUN_SH` starts `/work/server.py` (a lane-owned
  `TCPServer` on the case's port) and waits for `/work/ready` before the harness; the graded state is the
  two requests `verify.sh:57` (status) and `:60` (body) make to it.
- Refusal list matches the entry's own negative space (no image/harness/real submission, no
  validity/certification, no difficulty/gameability, no assertion-correctness judgment, no contamination,
  nothing from a real-image run); "89 carry `tests/test.sh`; 3 are read" is supported at
  `tb2-git-webserver-grader.md:50` and `benchmark-verifier-execution-model.md:93`.
- Reported-out targets exist and say what PROVINCE claims: `.ufo/waves/round-37/build/R37ConnSibling.md`
  §S4 (lines 79-88: tameshi `tools/mutate-and-run.sh`, kumitate `gate-mutants.mjs`) and
  `.ufo/waves/round-37/build/R37DockerOracle.md`. "The round35/36 paragraphs above stay as written":
  PROVINCE.md has zero removed lines across the whole round diff; the round-35 clause stands at `:238`.

## 7. Append-only discipline — verified, nothing rewritten in place

`git diff --stat 3ea9a1d9..357dece` (whole tree): **71 files changed, 8323 insertions(+), 0 deletions**.
Per errata-target file, removed lines (`git diff … | grep -c '^-[^-]'`): PROVINCE.md 0, SOURCES.md 0,
tb2-regex-log-grader.md 0, LOG.md 0, round-36-verifier-spotcheck.md 0 (file absent from the diff —
untouched), round-36.md 0 (untouched), SCORECARD.md 0. Each touched file is a single pure-addition hunk
at the end of its prior content: tb2-regex-log `@@ -263,3 +263,56 @@`, PROVINCE `@@ -253,5 +253,33 @@`,
SOURCES `@@ -123,6 +123,10 @@`, LOG `@@ -1078,3 +1078,36 @@`. `plans/pkg_gate.py`,
`plans/regex_log_probe.py` and `benchmark-verifier-execution-model.md` are absent from the diff — the
gate and the frozen probe were not touched.

---

## Findings

### F1 — minor — `tb2-regex-log-grader.md:298` (errata corrections table, `no-ip-condition` row): "a superset of the two rows below" has no reading that is both literal and true

The cell says the case's 9-line flip set (38, 44, 45, 50, 62, 63, 64, 65, 67) is "a superset of the two
rows below, so it is coarse, not attributable". The two rows immediately below it in that table are
`last date on a line` (measured {36, 42}) and `octets 0–255` ({44, 45, 64, 65, 67}); the 9-line set
contains neither 36 nor 42, so on the literal reading the superset claim is **false** for
`first-date-only` (my re-derivation and the seat's own `line-attribution.txt` agree: on the two-date
lines the no-IP pattern matches the same last date the control does, so 36/42 are not its flips). The
claim is true for the two IP-property rows — `octets 0–255` and the `IPv4 not alnum-adjacent` pair
({44,50,63}, {62,64,65,67} are both subsets) — which is almost certainly the intended referent, and the
cell's conclusion ("coarse, not attributable") holds under either reading. No measured number is wrong;
the defect is an unresolvable referent in a document whose purpose is attribution precision. Fix shape:
name the rows ("a superset of the octets and alnum-adjacency rows' flip sets") in a future erratum.

### Observations (not defects)

- `plans/anchor_digest_check.py`'s `ERRATUM` pattern and QUALITY Q26 hardcode `round 37`. Declared scope
  (Q26 is titled "Round37 criterion"; the docstring says "Built for kengaku round 37"), and it fails
  closed: a round-38 erratum of the same shape will print a defect for the corrected row until the
  pattern is extended. Recorded so the next round extends it rather than rediscovers it.
- The round-37 paragraph's "(S111–S113)" names the three pinned task files; the entry's `source:` block
  also carries S114 (prior art, tier B). The Gate table, the entry's §Prior art and the LOG cover S114;
  no byte is misstated.
- "Adjacent: … serving plane (kama)" is a routing reminder; the round's only service is the probe's
  lane-owned `http.server` on a private loopback (the entry says so), and no model-serving-plane surface
  is touched.

## Residual risk and verification gaps

- I did not re-run `plans/round37_c1_verify.py` / `round37_c2_verify.py` (other seats' predicates; the
  landing receipt `.ufo/waves/round-37/integrate/measure-final.txt` covers them). In-scope instruments I
  did re-run on my clone: `anchor_digest_check.py` (tip: `defects=0` exit 0; baseline tree: `defects=5`
  exit 1) and the frozen regex-log case table (24/24 receipt agreement, 12/12 flip sets).
- The four anchor-captures' equality with upstream rests on `PROVENANCE.md`'s recorded 2026-10-26 fetch
  (triple-checked there); I verified manifest↔row-cell equality, not a second live fetch.
- The errata's assertion-truncation claim (why 11 receipts share one string) follows from the probe's
  `first[:157] + "..."` truncation; I verified the counts, not the truncation constant.

Receipts: `falsify/F37RevProvinceErrata/{flipcheck-run1.txt, anchor-check-tip.txt,
anchor-check-baseline.txt, byte-verify.txt, bwrap-id.txt}`. Scratch
`/fast/scratch/hyaku/kengaku-r37/F37RevProvinceErrata` deleted after writing.

VERDICT: province-errata-1-defects
