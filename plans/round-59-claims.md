# Round 59 claims freeze (kengaku, hyaku run 14, 2026-11-02)

Base `5420eac9` (the round-59 wave-R receipt re-landing tip; the round-58 non-author closure
`e0cfa97a` before it). This freeze is written and committed BEFORE the first execution of the
round-59 probe against the TB2 capture (the r57/r58 discipline; the probe's plumbing is proven
only against a toy grader, `--selftest` 2/2 green, and the consistency gate's plumbing only
against its fixture battery, `--selftest` 8/8 green — no capture run, no lane scan). Instrument
self-pins: `plans/round59_c1_openssl_probe.py` sha256
`a7c9b231e4cef27e54aa5b9c3b75e416f8a13389e13b58fb829b8bfa9b6a18cd`;
`plans/receipt_consistency_check.py` sha256
`efd50ef6811b44935d9a456f4acbc0a4786b13168e671e5277b7efed66c44b77`.

Environment: WSL Ubuntu-24.04 (python 3.12.3, bwrap 0.9.0, git 2.56.0, OpenSSL 3.0.13; uv/pytest
absent — the r56 A3.4 canonical counter environment preserved; no environment mutation this
round).

## Carry-in from the round-58 non-author closure — status before this freeze

All four routed items addressed this round, before or beside the claims:

1. **(a) the five orphaned receipts — DISCHARGED at `5420eac9` (wave R, before this freeze).**
   Each cited instrument re-run on a clean WSL-native-fs clone at tip `e0cfa97a`, fresh output
   landed at the cited paths under a dated re-landing header; all five green, predicate fields
   matching the committed close receipts field for field (r50-after `PREDICATE R50-C1 pass`
   exit 0; r46c2-after `PREDICATE C2 pass` exit 0; kl-sha-kill refusal `KILL-EXIT=1`;
   entryargv-full `executed=87 … laundered=0` `PREDICATE R55-C2 pass`; final-tip-receipts
   registry 86/86 + `LANDCHECK PASS n=4` + full entry-truth green). LOG wave entry carries the
   rule: receipts cited by landed rows are committed at landing.
2. **(b) the fixed-checker receipt's exit labels — corrected via R59-C2 below** (the
   correction row is the claim's erratum; the red-before receipt is committed BEFORE the
   erratum lands, so the gate's before-state is on record).
3. **(cosmetic) the counting-unit and report-prose mismatches — dated corrections in this
   file's closing section**, mirrored into the round-58 report's `## Corrections (round 59)`
   section (fleet root) and the round-59 close LOG entry at landing.

## R59-C1 / coverage (lowest owned axis, L0-capped) — the sixteenth grader read and executed: the corpus's first cryptographic-credential + filesystem-metadata gate

The one-more-grader pattern stays class-gated (the r58 planned note): this round registers the
sixteenth executed grader only because its CLASS is new to the executed corpus. Measured
negatives over the committed round-52 population (184 digest-pinned captures at pin `2fd12b88`,
S179): `grep -rl '"openssl"' corpus/evidence/round52/graders` → exactly ONE grader,
`openssl-selfsigned-cert/tests/test_outputs.py`; `grep -rl 'st_mode'` over the same population
→ 9 graders, NONE of them among the 15 executed; so no executed grader reads a cryptographic
credential's structure through the openssl CLI, and none asserts POSIX permission bits.

The grader (`openssl-selfsigned-cert/tests/test_outputs.py`, sha256
`90970bb3c372e8e7fb6bb9ac5f649ba73eb38e1a5ea2e922a9057a72b6b4192d` — byte-identical to the
round-52 population capture of the same path, two independent fetches) runs SIX test functions
over the `/app` artifact set: `test_directory_structure` (presence of `/app/ssl`),
`test_key_file` (POSIX permission bits `st_mode & 0o777 <= 0o600` at :22, and the key's size
read through `openssl rsa -text` — `"2048 bit"` at :31), `test_certificate_file` (subject CN
and O read through `openssl x509 -text`, and the validity window `notAfter − notBefore == 365`
days parsed from `openssl x509 -dates`, :79), `test_combined_pem_file` (substring banner checks
AND a real `openssl x509` parse of the combined PEM, returncode 0), `test_verification_file`
(subject strings, a date line in either format, and a SHA-256 fingerprint matching
`[0-9a-f]{2}(:[0-9a-f]{2}){31}`), `test_python_verification_script` (executes
`python /app/check_cert.py` — a real child process through the `python` entry point — and
asserts its exit code, its success line, the CN and a `YYYY-MM-DD` expiration).

**Probe:** `plans/round59_c1_openssl_probe.py` materializes the byte-pinned capture read-only
at `/tests` inside a bubblewrap sandbox (`--unshare-all`, `/usr`+`/etc` ro, `/app` writable —
the r58 sandbox), builds each candidate artifact set INSIDE the sandbox from frozen literal
constants (subject fields, day count, mode bits, PEM composition, verification-file parts,
script source), then runs the six test functions directly (no pytest runner; the capture
imports no pytest). **Declared leg rule** (frozen here, before the first capture run): a leg
is P iff its test function returns normally; F on AssertionError OR any other exception
escaping the function (the artifact under test made the check fail; pytest scores a raising
test as not-pass either way and the reward is binary); SETUP only when the probe's own builder
fails or the sandbox produces no LEGS line. **Declared sandbox shim:** the capture's sixth leg
invokes `["python", script_path]`; this host's interpreter is python3, so the probe binds a
probe-owned `python` → `python3` shim at `/stub` and puts `/stub` first on PATH (the r58
probe-owns-its-stub pattern; the toy selftest exercises the shim). **No key material, no
certificate bytes, and no generated artifact is committed anywhere in the lane** (the r52
GH013 push-protection lesson): the builder generates a fresh RSA key inside the sandbox at run
time — safe because the grader asserts only key SIZE, permission BITS, subject fields and the
validity WINDOW, properties independent of the key bytes.

**Frozen prediction table** (full commitment, zero U — every leg is a deterministic function
of the candidate's declared properties; 12 cases × 6 legs = 72 predictions):

| case | defect class exercised | dir | key | cert | pem | verif | script |
|---|---|---|---|---|---|---|---|
| sol | none — the maintainer oracle's construction (S220) | P | P | P | P | P | P |
| perm-loose | key mode 0644 (the permission-bits leg) | F | P | P | P | P | P |
| key-1024 | 1024-bit key (the openssl rsa size leg) | F | P | P | P | P | P |
| days-30 | 30-day validity window | P | P | F | P | P | P |
| cn-wrong | wrong Common Name (cert + verification + script legs) | P | P | F | P | F | F |
| pem-keyonly | PEM holds the key only (substring tooth) | P | P | P | F | P | P |
| pem-garbage | PEM banners present, certificate block corrupt (openssl-parse tooth) | P | P | P | F | P | P |
| fp-absent | verification.txt without the SHA-256 fingerprint | P | P | P | P | F | P |
| script-silent | check_cert.py exits 0 silently | P | P | P | P | P | F |
| dir-absent | no /app/ssl at all | F | F | F | F | F | F |
| org-upper | Organization in caps (the grader's stated leniency) | P | P | P | P | P | P |
| script-missing | check_cert.py absent (artifact-absence is a leg failure, not setup) | P | P | P | P | P | F |

Controls: the do-nothing control is the same table against the base bytes — the probe and the
capture are both absent at `5420eac9`'s parent for round-59 paths
(`git cat-file -e 5420eac9:corpus/evidence/round59` fails; `git show 5420eac9:PROVINCE.md |
grep -c sixteenth` → 0, rc 1 — structural anchors per the R57-W1 rule, no negation matches:
"sixteenth" never appears at base); a no-op cannot produce the after-state. The sha-refusal
kill class is inherited from the r58 probe design (byte-pinned capture, SetupError on drift).
Falsifier direction check: cases 6 and 7 separate the PEM leg's two teeth (substring vs
parse); cases 2 and 3 separate the key leg's two teeth (mode bits vs bit length) — the table
predicts the same leg vector for both, but the receipts print which tooth fires via the
per-case construction (the knowledge entry names each case's tooth).

Predicate: `python3 plans/round59_c1_openssl_probe.py --lane .` → 12 CASE lines all `ok`,
`cases=12 legs=72 mismatches=0 setup=0 predicted_u=0`, `PREDICATE R59-C1 pass`, exit 0;
receipt `corpus/evidence/round59/openssl-probe.txt` (the registry/tip-receipt culture applies:
bare argv is the entry form, `--receipt` produces the committed receipt).

**Class line:** the corpus's executed graders now cover exact predicates (majority), a
wall-clock timing gate (r57), a numeric tolerance band on aggregated functionals (r58), and —
new this round — a cryptographic-credential gate whose decisive legs read the credential's
structure through a production crypto tool and assert a filesystem-metadata property
(permission bits) plus a child-process contract (the `python` entry point). Registration
discipline: the probe gets a SKILL registry row + ledger row in the SAME commit that lands the
SCORECARD counting command (the r58 lesson-3 rule: a runnable-command form in prose advertises
the tool).

## R59-C2 / operability (held at ceiling 10) — the receipt self-consistency gate

The round-58 closure's finding (b) was caught by a human reading a receipt: its `exit=0`
labels under fx-red and fx-words contradict its own `rc=1 want_rc=1 ok` selftest lines and its
own ANCHORLINE `live=1` payload lines. The class — a receipt whose own cross-checkable fields
contradict each other — had no mechanical check. New gate `plans/receipt_consistency_check.py`
scans every committed `.txt`/`.log` receipt under `.ufo/waves/` and `corpus/evidence/` and
counts three defect classes: R1 exit-vs-payload (a bare `exit=<n>` label must agree with the
nearest preceding `ANCHORLINE … live=<k>`: n == 1 iff k > 0; unanchored labels defect too),
R2 selftest-label (`rc=<a> want_rc=<b>` must carry `ok` iff a == b), R3 selftest-summary (a
`SELFTEST pass` summary under a contradicting line, or with no line at all, is a defect).
Erratum discipline: a `===`-delimited dated block naming `ERRATUM (round` and
`receipt_consistency_check` converts that file's defects to `errata=<n>` (declared, dated,
still printed; R1/Q26 house form — the receipt bytes stay as captured, the correction is
appended). Selftest 8/8 (both exit-map directions, unanchored, both label contradictions,
erratum conversion, foreign-block refusal, vacuous pass).

**Before-state** (measured over the whole committed population BEFORE the erratum lands —
dev survey repeated by the gate itself on the freeze tip; the numbers the red receipt must
print): `defects=2 errata=0`, both in
`.ufo/waves/round-58/recon/esc-falsifier-fixed-checker.txt` (its :9 fx-red and :13 fx-words
labels), exit 1 — the round-58 closure's finding (b), reproduced mechanically. No other
committed receipt in either population carries an inconsistency.

**After:** the erratum is appended to that receipt naming the wrong labels, the right values
(exit 1 under fx-red and fx-words), and the reason (capture-script bug; the payload's
ANCHORLINE lines and the file's own selftest rc lines are the red-direction evidence of
record); the gate re-run on the erratum tip prints `defects=0 errata=2`, `PREDICATE R59-C2
pass`, exit 0. Registration: SKILL registry row + ledger row in the same commit as the
SCORECARD counting command.

Controls: the do-nothing control cannot pass the before-state (the two contradicting labels
are committed bytes at base); the gate cannot be green before the erratum because the erratum
marker is what converts the defects; the foreign-block selftest case (7) shows a non-gating
erratum cannot launder a defect.

## Sources opened this round (the round-59 Gate; all at pin 2fd12b88, 2026-11-02, bytes hashed on arrival, captures committed at this freeze)

| row | file | kind/tier | located quote (≤25 words) | sha256 |
|---|---|---|---|---|
| S218 | `openssl-selfsigned-cert/task.toml` | spec / A | task.toml:6 "Evaluates an agent's ability to generate self-signed TLS certificates using OpenSSL, manage cryptographic keys with proper permissions, and create verification scripts." (21 words) | `75c8913f0fa15890786c11999cde920b8bfc10d4ce8a14edf1e76985a2ac5800` |
| S219 | `openssl-selfsigned-cert/tests/test_outputs.py` | code / A | test_outputs.py:22 "assert key_permissions <= 0o600, f\"Key permissions too open: {key_permissions:o}\"" (9 words); :79 "assert days_diff == 365, (" (5 words) | `90970bb3c372e8e7fb6bb9ac5f649ba73eb38e1a5ea2e922a9057a72b6b4192d` |
| S220 | `openssl-selfsigned-cert/solution/solve.sh` | code / A | solution/solve.sh:14 "openssl req -new -x509 -key /app/ssl/server.key -out /app/ssl/server.crt -days 365 -subj \"/O=DevOps Team/CN=dev-internal.company.local\"" (13 words); :8 the genrsa 2048; :11 the chmod 600 | `58cf3c844e907745cd81fb4bd75efb3d080e2f0e82b589c56c954ae6e1756510` |
| S221 | `openssl-selfsigned-cert/instruction.md` | docs / A | instruction.md:5,7 "Generate a 2048-bit RSA private key: … Ensure proper permissions (600) for the key file" (14 words) | `38054a3371f7c2c853478a2f9af0bff858437d5b28a9a07483238f06e566921f` |

S219's bytes are byte-identical to the round-52 population capture of the same path (two
independent fetches agree on the sha256) — the pin holds across reads. S220 is the maintainer
oracle: the probe's `sol` candidate mirrors its construction (genrsa 2048 → chmod 600 → req
-x509 -days 365 with that -subj → cat key+cert into the PEM → openssl-written
verification.txt → a check_cert.py printing CN, ISO expiration, the success line). All four
admit tier A for their narrow scopes (the task's own spec, the executed grader, the
maintainer's solver, the agent-facing instruction); no rejections; no flips of existing rows.
C1 is the round's sourced claim (rides S218–S221). Rejections kept: none this round.

## Dated corrections (the cosmetic carry-in; measured commands; the superseded lines stay as written)

1. **The round-58 report's Sources-and-frontier prose says the round-58 lesson mines "three
   rows"; the landed lesson has FOUR.** The fourth row (the registry-advertisement mistake)
   was added at wave F2, after the report prose was drafted — an honest progression the
   closure named status-neutral. Counting command:
   `grep -cE '^\| (freeze|landing|fixture authoring) ' corpus/lessons/round-58.md` → 4 at the
   round-59 tip. The LOG close entry's mistakes list names only three classes
   ("freeze-exit-path, non-idempotent edit script, fixture byte-derivation") — the same
   undercount; corrected by this entry and the close LOG entry.
2. **The round-58 report's quality trend says the repair cascade "broke six tip-counter
   surfaces"; the LOG close entry says "four tip counters".** Both are true under their own
   counting units and the one-second timeline: the LOG entry (wave E, `2016a08`—era) counted
   the four counter legs that had gone red BY THEN (round36-c2 W4; round51-routing
   vocabulary+check fields; r40 a_tok uniqueness; round-close E11); the report counted the six
   defect SURFACES the cascade exposed by the final tip (the four above, counted once each
   with the two check fields as one surface, plus the registry advertisement of the repaired
   checker — which went red only at the final-tip capture, wave F2, `9defcad6`). Correction:
   one counting unit named per claim — "N counter legs red" vs "N defect surfaces caught" —
   recorded here, in the round-58 report's Corrections section, and in the close LOG entry.
   Counting commands: `grep -c 'broke four tip counters' LOG.md` → 1 (the wave-E unit);
   `grep -c 'broke six tip-counter surfaces' <fleet>/.ufo/reports/round-58/kengaku.md` → 1
   (the report's surfaces unit).

## Amendment 1 to the C2 instrument (dated 2026-11-02, BEFORE any C2 receipt of record landed — the Q25 window)

The freeze pinned `plans/receipt_consistency_check.py` sha256
`efd50ef6811b44935d9a456f4acbc0a4786b13168e671e5277b7efed66c44b77`. Its R1 rule carried an
extra tooth this freeze's own before-state never used: a bare `exit=` label with NO preceding
ANCHORLINE was counted as an `unanchored` DEFECT. Measured over the real committed population
at the freeze tip (clean clone, receipt not landed): that tooth flags 13 labels across five
historical receipt files (K26RecoveryEvidence.txt ×3 in four copied fixture trees,
defs-repro.txt, R42ScratchGuard RECEIPT.txt ×3) whose exit labels refer to arbitrary commands —
uncheckable, NOT contradictory. No contradiction among them; the freeze's "before-state =
defects=2" statement (from the dev survey, which priced contradiction only) was right and the
frozen instrument over-counted. Amended per Q25's window (no C2 receipt of record existed):
the amended instrument sha256 is
`3767a4476c26c0c53b80fcb2978be1716d64d97bbca619b82ea1c69884848faa` — the change is exactly the
removal of the unanchored-defect branch (R1 now prices only exit labels that follow an
ANCHORLINE) and selftest case 3 flips from "unanchored fails" to "unanchored skips" as the
scope-fence case, named here. Unmoved: the other seven selftest expectations byte-identical,
the finding-(b) detection (2 defects, both in esc-falsifier-fixed-checker.txt), the erratum
conversion, the before→after numbers this section froze. The C1 battery receipt landed in the
same window is a different instrument and is untouched.

## Dated correction: R59-C1's frozen prediction table mispredicted 2 of 72 legs (measured at the first and only capture run, 2026-11-02)

The freeze's table rows for `perm-loose` and `key-1024` read F/P in their first two columns
(dir, key); the correct predictions — which the freeze's OWN "defect class exercised" column
names (the permission-bits leg; the openssl-rsa size leg) — are P/F: in both candidates the
/app/ssl directory exists (dir passes) and the KEY property fails. I transcribed the two legs
transposed for exactly those two rows, in both the markdown table and the probe's CASES
tuples (one source, retyped twice — the r58 fixture-bytes lesson in a new form). The scored
run (the only capture run; freeze `002cde8e` precedes it; receipt
`corpus/evidence/round59/openssl-probe.txt`) observed
`perm-loose observed=P/F/P/P/P/P` and `key-1024 observed=P/F/P/P/P/P` against
`predicted=F/P/P/P/P/P`; the other 70 legs matched (`cases=12 legs=72 mismatches=2 setup=0
predicted_u=0`, `PREDICATE R59-C1 fail`, exit 1). Per Q25's last sentence the table is NOT
re-frozen to match the observation and the observed run cannot be re-scored: **R59-C1's
frozen predicate (mismatches=0) is FAIL, honestly carried** — the grader's behaviour on every
leg matches the class analysis, the two misses are author-transcription errors, the correction
is mined in `corpus/lessons/round-59.md`, and a corrected zero-U re-freeze is next round's
work if a round needs it. Re-derive: `python3 plans/round59_c1_openssl_probe.py --lane .` →
`mismatches=2` and the two MISMATCH lines name the same four cells.

=== ERRATUM (round 60, 2026-11-02) — the counting command in correction 2 of the section above does not
reproduce: the backticked `grep -c 'broke four tip counters' LOG.md` form prints 0, not 1, on the committed
bytes — the phrase is line-wrapped at LOG.md:1961-1962 ("The repair cascade broke⏎four tip counters before
closure") and grep -c counts matching LINES (S223, corpus/evidence/round60/grep-manual/grep.html:379): a
phrase spanning a wrapped line does not match. This is the round-59 non-author closure's routed defect 3,
and it is the red-before defect of record for the round-60 counting-command reproduction gate
(plans/correction_command_check.py; red-before receipt .ufo/waves/round-60/recon/c2-red-before.txt at the
freeze tip 9e37311f names it as the population's one defect). Two reproducing commands, each on its own
line so the gate's same-line pairing is unambiguous, both priced at the corrections tip:

`grep -c 'The repair cascade broke' LOG.md` → 1

(the sentence-start fragment: unwrapped, unique, stable — got=1 want=1 ok)

`grep -c 'four tip counters' LOG.md` → 2

(got=2, honestly priced: the r59 spotcheck's suggested unwrapped-token form printed 1 at the r59 tip, and
THIS round's own wave-F LOG entry quoted the token, doubling the count — the gate's first live catch, a new
instance of exactly the class it prices, created and captured in the same round; mined in
corpus/lessons/round-60.md). The same erratum corrects the citation precision the r59 closure routed as
defect 2: the carry-in (b) sentence "the red-before receipt is committed BEFORE the erratum lands" is
imprecise — both the receipt and the erratum land in commit 85ef87e5; the MEASUREMENT was made at e0512854,
where the receipt file does not yet exist. Measured-at vs landed-at is now named per citation in the
registry row and PROVINCE (round-60 precision fixes). ===


=== ERRATUM CONTINUATION (round 60, 2026-11-02, dated at the corrections-2 landing) — the gate's SECOND live catch, same self-quoting mechanism, larger blast radius: the wave-C LOG entry quoted BOTH reproducing commands with their then-current results, and each quotation added a line containing the quoted token to LOG.md, drifting both counts AGAIN before the final tip could price them (at the corrections tip e26b330e the gate printed defects=0 errata=3 — the two new drifts converted beside the original wrapped-phrase defect; the row's stored evidence fragment read defects=0 errata=1, so the entry-truth counter correctly flagged the fragment as missing and the tip run FAILED PREDICATE R55-C2 — the counters caught the drift, the honest-stop machinery working). The two commands are re-priced here at CURRENT truth (one command per line); the r59-tip values (1 and 2) are named as history; the mined rule hardens: a LOG entry never quotes a counting-command literal at all (name the class, not the command), because every quotation of a token adds a line containing it:

`grep -c 'The repair cascade broke' LOG.md` → 2

(re-priced: got=2 — 1 at the r59 tip; the wave-C LOG entry's own quotation of this fragment added the second line)

`grep -c 'four tip counters' LOG.md` → 3

(re-priced: got=3 — 1 at the r59 tip, 2 after the wave-F entry quoted it, 3 after wave-C quoted it again; the ladder is the mined mechanism made visible)
