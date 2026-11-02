# Terminal-Bench 2.0 `openssl-selfsigned-cert` — the corpus's first cryptographic-credential + filesystem-metadata grader

source: S218 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/openssl-selfsigned-cert/task.toml — the task's machine-readable self-definition (a TLS-credential construction objective)
source: S219 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/openssl-selfsigned-cert/tests/test_outputs.py — the executed scoring predicate (six legs: permission bits, openssl-rsa size, x509 subject + 365-day window, PEM substring AND parse, verification-file formats, a child-process contract)
source: S220 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/openssl-selfsigned-cert/solution/solve.sh — the maintainer oracle (genrsa → chmod 600 → req -x509 -days 365 → concatenated PEM → openssl-written verification.txt → a load_cert_chain-backed check_cert.py)
source: S221 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/openssl-selfsigned-cert/instruction.md — the agent-facing instruction (six numbered requirements, one per grader leg)
verified-at: corpus/evidence/round59/openssl-probe.txt (probe `plans/round59_c1_openssl_probe.py --lane .`, cases=12 legs=72 mismatches=2 setup=0 predicted_u=0, PREDICATE R59-C1 fail, exit 1, at tip `002cde8e`; the 2 misses are author-transcription errors, dated-corrected in `plans/round-59-claims.md` — see Findings)
recheck: 180d — from the lane root re-run `python3 plans/round59_c1_openssl_probe.py --lane . --work <scratch>` and compare the CASE lines with the corrected observed vectors below (any drift is a mismatch line); re-open S219 at the pin if the receipt's capture sha refuses

## The class, worded narrowly

The decisive legs read a **cryptographic credential's structure through a production crypto
tool and assert a filesystem-metadata property**: the key leg shells out to `openssl rsa
-text` and asserts the literal `"2048 bit"` (S219 :31) plus a POSIX permission-bits bound
`st_mode & 0o777 <= 0o600` (:22); the certificate leg reads the subject (CN substring, O
substring case-insensitively) and the validity WINDOW out of `openssl x509 -text/-dates`
(notBefore→notAfter == exactly 365 days, :79); the PEM leg requires both banner substrings
AND a real `openssl x509` parse (returncode 0) of the combined file; the verification leg is
format-only (subject strings, a date line in either of two formats, a SHA-256 fingerprint
matching `[0-9a-f]{2}(:[0-9a-f]{2}){31}`); the script leg executes `python /app/check_cert.py`
as a child process and prices its exit code, its success line, the CN and a `YYYY-MM-DD`
expiration. Named against the lane's fifteen executed exemplars this is the
**crypto-credential + filesystem-metadata gate** class — membership/multiset/regex/service/
dual-runtime/exact-set are exact predicates, r57's is a wall-clock ordering, r58's is a
numeric band on aggregated functionals; no earlier executed grader shells out to a crypto
tool over a credential, and none asserts mode bits. Measured negatives (2026-11-02, the
committed round-52 population): `grep -rl '"openssl"' corpus/evidence/round52/graders` →
exactly this grader; `grep -rl 'st_mode'` → 9 graders, none executed.

## Probe findings (honest: 70 of 72 frozen predictions confirmed; the 2 misses are the author's)

The probe (r58 sandbox pattern: bwrap `--unshare-all`, `/usr`+`/etc` ro, `/app` writable;
capture byte-pinned at /tests; builder code generates each candidate INSIDE the sandbox from
frozen constants — no key material, certificate bytes or generated artifact is committed
anywhere in the lane, the r52 GH013 lesson) ran the capture's six legs against 12 candidates.
One capture run only (freeze `002cde8e` precedes it): 70 legs matched; `perm-loose` and
`key-1024` were predicted `F/P/...` and observed `P/F/...` — the freeze table transposed the
first two legs for exactly those rows (its own defect-class annotations name the key leg as
the failing one); dated correction in `plans/round-59-claims.md`, mined in
`corpus/lessons/round-59.md`. The confirmed structure, from the 70 confirmed legs plus the 2
observed:

- the permission-bits tooth and the openssl-rsa size tooth are INDEPENDENT (mode 0644 with a
  2048-bit key fails only the bits tooth; a 1024-bit key at mode 0600 fails only the size
  tooth — both observed P/F on dir, F on key);
- the PEM leg has two teeth in one function: banner substrings (`PRIVATE KEY`,
  `CERTIFICATE`) AND the openssl parse — a key-only PEM and a garbage-cert PEM both fail it;
- the cert subject failure propagates to the verification-file and script legs (they price
  the same CN string) but not to the key/PEM legs;
- `org-upper` passes: the O comparison is case-insensitive by the grader's own stated
  leniency;
- `script-missing` fails cleanly (the leg's `subprocess.run(["python", …])` raises — an
  artifact-absence failure, not probe setup), and `dir-absent` fails all six legs including
  the script leg (the oracle-shaped script reads the missing cert and exits nonzero);
- the validity-window leg parses `%b %d %H:%M:%S %Y %Z` dates out of openssl output and
  requires exactly 365 days — `-days 30` fails it, nothing else moves.

## Negative space (what this entry does not establish)

The capture is read and its legs executed offline against synthetic lane-built artifact sets;
this is not task validity (S190's specificity bar is checked only as the observation that the
instruction's six requirements map one-to-one onto the six test functions, S221), not the
container's behaviour (`alexgshaw/openssl-selfsigned-cert:20251031` never runs), not agent
performance, not the `python`-on-PATH assumption of real harness images (the probe declares
its own `python`→`python3` shim in `plans/round-59-claims.md`), and not the openssl 3.x vs
the image's openssl version behavioural distance (the asserted substrings — `2048 bit`,
subject spellings, `-dates` format — are stable across the 1.1→3.0 line but that stability is
asserted here only for 3.0.13, this host's build). The 365-day equality leg is exact by
construction of `openssl req -x509 -days 365` (notBefore today, notAfter +365d) but a leap-day
boundary case was NOT probed. What would falsify the class line: any earlier-executed grader
shown to shell out to a crypto tool over a credential or to assert mode bits (the grep
negatives above are over the committed round-52 population, not the upstream history).

Extends `corpus/knowledge/tb2-distribution-search-grader.md` (the fifteenth) and the
grader-semantics line in `corpus/knowledge/benchmark-grader-semantics.md`: the executed-corpus
class set grows to exact / timing / tolerance-band / crypto-credential+fs-metadata.

## Round-60 addendum (2026-11-02): the corrected zero-U re-freeze completes the admission — 72/72

The round-59 run's two prediction misses were author transcription, not grader behaviour;
round 60 lands the Q25-sanctioned new-claim re-freeze (`plans/round-60-claims.md`, freeze
`9e37311f`): the probe's predictions are derived at run time from the case definitions
(`predict_legs()`, each predicate grounded in this entry's capture anchors), the correction
is proven to be exactly the transposition (`--check-frozen-table`: 10 rows byte-identical,
perm-loose/key-1024 differing exactly at dir/key), and the derived table agrees with the r59
receipt's observed vectors 12/12 (`--check-receipt`; the r59 receipt of record stays
byte-identical). Scored run at the freeze tip, clean WSL clone: `cases=12 legs=72
mismatches=0 setup=0 predicted_u=0`, `PREDICATE R59-C1 pass`, exit 0 — receipt
`corpus/evidence/round60/openssl-probe-refreeze.txt` (measured at `9e37311f`; the grader's
six legs answer exactly as this entry describes, now under a full-commitment clean verdict).
No leg's semantics changed; no new ground is claimed — still 16 of 89 TB2 task graders read.
