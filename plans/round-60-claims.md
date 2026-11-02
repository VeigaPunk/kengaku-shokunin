# Round 60 claims freeze (kengaku, hyaku run 14, 2026-11-02)

Base `9482c8408f62e2a13a69f27870f1825bbbe73d8b` (the round-59 non-author closure tip,
`rejected-honest-stop` with C2 admitted and C1 honestly carried). This freeze is written and
committed BEFORE the round's first scored run of either instrument (the r57–r59 discipline:
plumbing is proven only against toys/fixtures — the amended probe's `--selftest` 2/2 toy
green and the three read-only modes green at the base worktree, receipts beside this file;
the gate's `--selftest` 6/6). Instrument self-pins:

- `plans/round59_c1_openssl_probe.py` (amended) sha256
  `6faf217c723efaf8d24bd15a9e8aeb873328af4a7f8e9c4ab4ca94b2465d4646` — supersedes the r59
  freeze's pin `a7c9b231e4cef27e54aa5b9c3b75e416f8a13389e13b58fb829b8bfa9b6a18cd` (both
  digests named per Q25; the amendment is a NEW claim that re-freezes — Q25's last sentence
  — never a retroactive edit of the r59 freeze).
- `plans/correction_command_check.py` (new gate) sha256
  `b8ad6bd65dac8d6172baa3def9852bf7c214e1408b8512a82448bfdca9b0c690`.

Environment: WSL Ubuntu-24.04 (python 3.12.3, bwrap 0.9.0, git 2.56.0, OpenSSL 3.0.13;
uv/pytest absent — the r56 A3.4 canonical counter environment preserved; no environment
mutation this round). Measured on clean WSL-native-fs clones; every exit label in a receipt
is captured inside the runner script (the host harness swallows `$?` for inline `wsl.exe
bash -lc` chains — first-hand re-observation of the r58 finding-(b) capture hazard: the
gate's own first interactive invocation printed exit 0 under the broken harness while
printing `PREDICATE R60-C2 fail`; a runner-captured rc=1; mined in the round-60 lesson).

Carry-in (round-59 non-author closure, `corpus/lessons/round-59-verifier-spotcheck.md` §6,
four status-neutral routed defects): (1) the fleet-repo round-58 report erratum append is
uncommitted in the fleet working tree — this lane may not mutate the fleet root, so the
append is mirrored byte-for-byte into this lane (`.ufo/waves/round-60/r58-report-corrections-mirror.md`)
and the fleet-root landing is routed to the orchestrator in the round report; (2) two
`path@hash` citations miss the landing commits — the in-lane occurrences (the
`receipt-consistency-check` registry row and the PROVINCE round-59 paragraph) are corrected
this round with dated notes; the fleet-report occurrences are in the mirror + report; (3)
the dated correction's counting command that does not reproduce (`grep -c 'broke four tip
counters' LOG.md` → 0, the phrase line-wrapped at LOG.md:1961-1962) — this is R60-C2's
red-before defect of record, converted by a dated erratum; (4) SCORECARD's round-59 cell
says SOURCES "210→214", stale by S222 (215 at the r59 tip, 216 after this round's S223) —
a dated touch-up line lands in the SCORECARD round-59 section.

## R60-C1 / coverage (lowest owned axis, L0-capped) — the corrected zero-U re-freeze of the sixteenth grader's 72-leg prediction table (the Q25-sanctioned new claim that completes the r59 admission)

The round-59 closure ruled R59-C1 NOT admitted: its frozen table carried two author
transcription misses (perm-loose/key-1024 first two legs transposed), the observed run
re-derived 70/72, and per Q25 the observed run cannot be re-scored and the table was not
re-frozen to the observation. The r59 freeze itself names the completion path: "a corrected
zero-U re-freeze is next round's work if a round needs it". This round needs it; the mined
fix (r59 lesson, freeze-transcription row) names the mechanism: **a prediction table must be
GENERATED from the case definitions in one pass (the probe gains a table-rendering mode; the
freeze embeds that output verbatim), never retyped by hand into a second artifact.**

**Probe amendment (the changed lines, named per Q25):** (a) `CASES` no longer store
predicted vectors — each tuple is now `(name, defect class, cfg)`; the r59 freeze's
defect-class annotations are carried verbatim as the class strings; (b) `predict_legs(cfg)`
is added — a static model of the six legs over the candidate's declared builder properties,
each predicate grounded in the capture's own assertions (test_outputs.py:8-12 dir; :22+:31
key; :47-80 cert; :84-102 pem; :105-136 verif; :139-158 script — every anchor verified
against the committed capture bytes); (c) `run_battery` sources every prediction from
`predict_legs` at run time (CASE/summary/PREDICATE line formats and the leg rule unchanged);
(d) three read-only modes added — `--render-table` (prints the generated table),
`--check-frozen-table` (compares the derived table against the r59 frozen table parsed from
`plans/round-59-claims.md`), `--check-receipt <path>` (compares against a receipt's observed
CASE vectors); (e) the docstring gains the dated amendment note. Unchanged: the bwrap
sandbox, builder template, byte-pinned capture + sha refusal, shim, leg rule, selftest
fixtures, exit map.

**The generated table** (verbatim `--render-table` output, measured at the base worktree
pre-freeze, REV 9482c840; the scored run's own receipt re-derives it at the freeze tip):

```
REV 9482c8408f62e2a13a69f27870f1825bbbe73d8b
| case | defect class exercised | dir | key | cert | pem | verif | script |
|---|---|---|---|---|---|---|---|
| sol | none -- the maintainer oracle's construction (S220) | P | P | P | P | P | P |
| perm-loose | key mode 0644 (the permission-bits leg) | P | F | P | P | P | P |
| key-1024 | 1024-bit key (the openssl rsa size leg) | P | F | P | P | P | P |
| days-30 | 30-day validity window | P | P | F | P | P | P |
| cn-wrong | wrong Common Name (cert + verification + script legs) | P | P | F | P | F | F |
| pem-keyonly | PEM holds the key only (substring tooth) | P | P | P | F | P | P |
| pem-garbage | PEM banners present, certificate block corrupt (openssl-parse tooth) | P | P | P | F | P | P |
| fp-absent | verification.txt without the SHA-256 fingerprint | P | P | P | P | F | P |
| script-silent | check_cert.py exits 0 silently | P | P | P | P | P | F |
| dir-absent | no /app/ssl at all | F | F | F | F | F | F |
| org-upper | Organization in caps (the grader's stated leniency) | P | P | P | P | P | P |
| script-missing | check_cert.py absent (artifact-absence is a leg failure, not setup) | P | P | P | P | P | F |
TABLE cases=12 legs=72 predicted_u=0 source=CASES+predict_legs
```

**Falsifier-direction check** (verbatim `--check-frozen-table`; the correction is EXACTLY
the transposition — ten rows byte-identical to the r59 freeze, the two corrected rows
differing exactly at the dir/key legs):

```
REV 9482c8408f62e2a13a69f27870f1825bbbe73d8b
DIFF perm-loose legs=[0, 1] frozen=F/P/P/P/P/P derived=P/F/P/P/P/P
DIFF key-1024 legs=[0, 1] frozen=F/P/P/P/P/P derived=P/F/P/P/P/P
FROZEN-TABLE rows=12 differing=2 missing=0 ok
```

**Output-side cross-check** (verbatim `--check-receipt corpus/evidence/round59/openssl-probe.txt`;
provenance documentation only — the derivation NEVER reads either artifact: `predict_legs`
consumes only the `CASES` cfg dicts; both check modes are separate code paths run after):

```
REV 9482c8408f62e2a13a69f27870f1825bbbe73d8b
OBSERVED-CHECK cases=12 agree=12
```

That the derived table agrees with the r59 receipt's observed vectors 12/12 is exactly what
the non-author closure re-derived from committed bytes; the agreement is recorded here as a
cross-check, not as the derivation's input.

**Frozen predicate:** one clean scored battery run on a clean WSL-native-fs clone at THIS
freeze tip — `python3 plans/round59_c1_openssl_probe.py --lane . --work <scratch>
--receipt corpus/evidence/round60/openssl-probe-refreeze.txt` → 12 CASE lines all `ok`,
`cases=12 legs=72 mismatches=0 setup=0 predicted_u=0`, `PREDICATE R59-C1 pass`, exit 0. The
receipt is a NEW file (the r59 receipt of record, `corpus/evidence/round59/openssl-probe.txt`,
stays byte-identical — the observed run is not re-scored and no history is rewritten; the
entry argv stays bare, so the registered entry's tip behavior becomes the clean verdict).
Registration: the SKILL registry row and the entrytruth ledger row flip RED→GREEN with dated
reasons in the same landing commit that carries the SCORECARD counting command (the r58
lesson-3 rule).

Controls: the do-nothing control holds — at the base tip the registered entry (bare probe,
old CASES) prints `mismatches=2`, `PREDICATE R59-C1 fail`, exit 1 (the judge re-derived
byte-identically from the committed receipt), and the amended instrument, the new receipt
path and the claims doc are all absent at base (`git cat-file -e
9482c840:corpus/evidence/round60` fails; `git cat-file -e
9482c840:plans/round-60-claims.md` fails) — a no-op round cannot move the row. The
sha-refusal kill class is inherited unchanged: any byte drift on the pinned capture is a
SetupError (`SETUP`/non-zero exit), never a silent downgrade. The r59 class line (the
corpus's first crypto-credential + filesystem-metadata gate; 16 of 89 TB2 graders read) is
registered and unchanged — this claim completes its admission, it does not widen the class.

R13 separability: C1's verify condition needs only the amended probe + the battery run;
C2's needs only the gate + the erratum. Reverting C2's files does not move C1's predicate
and vice versa (disjoint artifacts; the only shared file is this claims doc).

## R60-C2 / operability (held at ceiling 10) — the counting-command reproduction gate closes the r59 routed-defect-3 class red→green

The round-59 closure routed defect 3: a dated correction's own counting command does not
reproduce — the r59 claims doc's cosmetic-correction section prints
`grep -c 'broke four tip counters' LOG.md` → 1 while the committed bytes give 0 (the phrase
is line-wrapped at LOG.md:1961-1962). A dated correction asserts current truth (QUALITY R12:
"a stale assertion is closed by an appended correction that itself re-derive[s]"); its
counting command is a falsifiable assertion that must keep re-deriving at the tip. The class
had no mechanical check; the r59 receipt-consistency gate prices receipts' internal
consistency, not the reproducibility of counting commands cited in corrections.

**Gate:** `plans/correction_command_check.py` (self-pin above; `--selftest` 6/6 — both
verdict directions, the erratum conversion, the foreign-block refusal, the scope fences,
and the empty-population setup). Frozen population `plans/round-*-claims.md`; within a file
only the body of a section whose heading matches `dated correction` (case-insensitive) is
scanned — corrections assert current truth; freeze-time before-anchor commands elsewhere in
a claims doc are historical statements about the freeze revision and are out of scope by
design. Frozen command class: a backticked `grep -c<flags> 'PATTERN' PATH` on one line
followed on the same line by `→ <digits>`; the gate re-runs it with cwd=lane (shlex-split
argv, no shell), rejecting out-of-lane paths (absolute, `..`, `<fleet>`-style placeholders)
as `out_of_scope` — not defects — because the gate reads the lane read-only. Erratum
discipline (the R1 house form, mirroring the receipt gate): a `===`-delimited block in the
same file containing both `ERRATUM (round` and `correction_command_check` converts that
file's defects to `errata=<n>` — declared, dated, still printed; a foreign block converts
nothing. Exit 0 iff undeclared defects = 0; 1 on any; 2 on setup (empty population — never
a vacuous pass). Named limits: only grep -c-family commands with an explicit same-line
expectation are re-run (the r59 correction's python3 re-derive command is out of scope);
only same-line pairs are priced; the gate prices the claimed count, not the sentence's
meaning.

**Grounding (the round's sourced claim): S223** (opened this round 2026-11-02; capture
`corpus/evidence/round60/grep-manual/grep.html`, sha256
`517177d02c39c446470c898273036a7616f705e4cbdcb6486b76a25700675f37`, quote at :379, 11
words, count derived by command): grep -c counts **matching LINES** per input file — a
phrase spanning a wrapped line does not match. This is the mechanism of the routed defect
and the reason the gate's scope fence is the grep -c family (line semantics are exactly
what makes the class checkable). Adopted through `plans/sources_adopt.py` (quote validation
+ registry admission exit 0, 215 staged rows before, collisions=0, malformed=0,
duplicates=0); used-by: this file and the round-60 lesson.

**Pre-freeze survey** (the r59 lesson's instrument-scope rule: measure the defect class
against the real population BEFORE the instrument freezes — receipt
`.ufo/waves/round-60/recon/cmd-terrain-scan.txt`, measured at the base tip `9482c840` on a
clean WSL-native-fs clone): 3 commands across the population's single dated-corrections
section — 1 reproduces, 1 fails (the routed defect), 1 names a fleet-root path the
prototype chased (the frozen gate classifies that class out-of-lane/out-of-scope, not a
defect — the r58 report lives in the fleet repo this lane may only read).

**Before-state of record** (measured at THIS freeze tip on a clean clone, after the gate
exists; receipt `.ufo/waves/round-60/recon/c2-red-before.txt`):
`CMDPOP files=37 sections=1 commands=3 ok=1 out_of_scope=1 defects=1 errata=0`,
`PREDICATE R60-C2 fail`, exit 1 — the one defect is the routed wrapped-phrase command
(`got=0 want=1`).

**After:** a dated ERRATUM block appended to `plans/round-59-claims.md` §Dated corrections
naming the wrong command and its mechanism (S223's line semantics), carrying the reproducing
command `grep -c 'four tip counters' LOG.md` → 1 — measured `got=1 want=1 ok`; the gate
re-run then prints `defects=0 errata=1`, `PREDICATE R60-C2 pass`, exit 0 (receipt
`.ufo/waves/round-60/recon/c2-green-after.txt`, lands with the round's receipts commit).
The same landing carries the routed-defect-2 citation repairs (the registry row and the
PROVINCE paragraph now cite landing commits) and the routed-defect-4 SCORECARD touch-up.
Registration: SKILL registry row + entrytruth ledger row in the same commit as the
SCORECARD counting command.

Controls: the do-nothing control cannot pass the before-state — the wrapped-phrase command
is a committed byte at base and the erratum block is what converts it, so a no-op round
stays exit 1; the foreign-block selftest case (4) shows a non-gating erratum cannot launder
a defect; the fences case (5) shows out-of-lane and expectation-less commands are skipped,
not priced.

R13 separability: stated under C1 — disjoint artifacts both ways.

## Amendment 1 (round 60, dated 2026-11-02, after the freeze; the gate instrument is unchanged — this corrects this file's AFTER-state prose only)

The after-state paragraph above said the erratum carries "`grep -c 'four tip counters' LOG.md`
→ 1 — measured got=1 want=1 ok". The r59 spotcheck's suggested unwrapped-token form printed 1
at the r59 tip — and then went stale before this round landed, because this round's own
wave-F LOG entry quotes the token, doubling the count to 2. The gate priced the freeze doc's
own erratum draft live (`CMD-DEFECT got=2 want=1` under the then-current text, converted by
the marker) — its first live catch, a new instance of exactly the class it prices, created
and captured in the same round; mined in `corpus/lessons/round-60.md`. The LANDED erratum
(one command per line, so the gate's same-line pairing stays unambiguous) prices both forms
at current truth: `grep -c 'The repair cascade broke' LOG.md` → 1 (the stable sentence-start
fragment) and `grep -c 'four tip counters' LOG.md` → 2 (the drifted token, honestly priced).
Green-after of record at the corrections tip: `CMDPOP files=37 sections=2 commands=5 ok=3
out_of_scope=1 defects=0 errata=1`, `PREDICATE R60-C2 pass`, exit 0 (receipt
`.ufo/waves/round-60/recon/c2-green-after.txt`, lands with the round's receipts commit). The
gate's frozen bytes are NOT touched here — receipts of record exist (the red-before ran at the
frozen sha), so a docstring edit would be a post-receipt instrument change; the same-line
pairing limit is instead named HERE as the instrument's recorded limit: a line carrying two
backticked grep commands pairs the first with the first following arrow, so erratum and
correction text carries ONE command per line (the landed erratum obeys this).
