# Round 31 C1 counter re-attack

Axes: **coverage** (does the frozen counter measure the claimed entry?) and **calibration** (does the committed control receipt identify a do-nothing/pre-append run?). Scope: `plans/adoption_check.py`, `plans/round31_c1_verify.py`, wave-1 critic `build/R31CritC1.md`, and `claims/control-nothing.txt`.

## Re-run on current lane bytes

Command (lane root):

```
python3 plans/adoption_check.py --expect .ufo/waves/round-31/adoption-expect.json --census
```

Observed stdout `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok`, exit 0. Command `python3 plans/round31_c1_verify.py --lane .` observed `checks=6 defects=0`, exit 0. These prove the present lane passes the implemented predicates, not the frozen semantic kill rule.

## Rebuilding V1/V2b/V3/V4b/V8 against current code

The exact old fixture directories described in `build/R31CritC1.md:14-21,237` are not present in the lane; `find .ufo/waves/round-31 -maxdepth 2 -type f -name '*V*' -o -path '*/fixtures/*'` returned no paths. Rebuilt relevant bytes in an isolated `/tmp/r31fx-R31C1Counter` copy of the current lane (no production files changed), retained current `plans/adoption_check.py` and `round31_c1_verify.py`, and re-ran both counters:

- **V1, 63-byte stub:** construction from `R31CritC1.md:25-53` no longer passes the *frozen counter*. Current `adoption_check.py:104-128` enforces exact distinct source-ID set, opened date, and index-row uniqueness/non-empty title/description; `round31_c1_verify.py:114-121` additionally requires >=40 lines and >=3000 bytes; `:46-53` requires frozen path and date; `:68-88` checks each registry URL host/path is named by its source line. A 63-byte file cannot satisfy V5. Result: **fell**.
- **V2b, re-headed unrelated 6,653-byte body:** size can satisfy V5, but old fixture's fabricated `stub` source rows (`R31CritC1.md:36-46`) are not current registry URL citations. It fails V2 unless source lines are changed to contain each actual row URL host/path; the unrelated body may still pass because current verifier checks substring presence, not quote locatability or semantic relevance. Thus the *exact construction* **fell**, while the broader unrelated-body vulnerability **survives** (inference from checks V2/V3/V5, with no content-identity check).
- **V3, retarget expect to nonexistent path:** `adoption_check.py:60-81` still takes path from JSON, so the old path-retarget attack against that counter **survives** if counts/rows/index are aligned. The second verifier hard-codes `ENTRY` (`round31_c1_verify.py:32,46-53`) and rejects missing frozen entry regardless of expectation; end-to-end C1 acceptance **fell**.
- **V4b, past date retarget:** old counter-only retarget (`R31CritC1.md:84-96`) **survives** when registry opened and entry verified-at are retargeted consistently: counter reads access_date from expectation (`adoption_check.py:60-61,79,114-117`). The verifier does not hard-code date; its V1 reads expect date (`round31_c1_verify.py:50-52`), so it also **survives end-to-end** under a retargeted expect file. It does not establish the frozen literal 2026-10-25.
- **V8, landed-tree forged control by changing untracked expect path:** `R31CritC1.md:158-170` is blocked by V6 if receipt is left intact: `round31_c1_verify.py:124-135` hashes current expect bytes and requires that digest in receipt. But the receipt is not authenticated against a commit/tree identity; a landed tree can reproduce it by restoring the *frozen* expect JSON and constructing the zero-entry state (or by changing receipt and expect together, since both are ordinary lane files). The precise V8 retarget alone **fell**; the broader reproducibility-from-landed-tree concern **survives** absent a pinned pre-append tree identity.

Rebuild command evidence: `mkdir -p /tmp/r31fx-R31C1Counter && cp -a <lane>/. /tmp/r31fx-R31C1Counter/` followed by edits only under `/tmp`, then the two commands above. Fixture results are as stated from current source predicates; no legacy fixture bytes existed to replay byte-for-byte.

## Control receipt reproduction

`claims/control-nothing.txt:1-8` records SHA256 `a6a7631c...a5c8` for the expect file, command, seven-field counter output, and `exit=1`. `sha256sum .ufo/waves/round-31/adoption-expect.json` currently equals the recorded digest. `git ls-files .ufo/waves/round-31/claims/control-nothing.txt .ufo/waves/round-31/adoption-expect.json` shows both files tracked; `git show dbb07364:.ufo/waves/round-31/claims/control-nothing.txt | sha256sum` matches the working receipt hash `990a1d9a...e502`. Therefore the receipt is committed, but the expectation is also committed and its digest is reproducible from landed bytes.

Can the recorded output be reproduced from a landed tree? **Yes, as a predicate result**: the tracked expectation dictates path/date/source IDs; a tree omitting the entry and index while retaining the three registry rows can produce the zero counters and exit 1 (the counter's logic at `adoption_check.py:69-81,87-98,104-128,149-164`). It is not the actual landed tree: the current landed lane produces the nonzero pass line above. The receipt's digest blocks silent retargeting *without changing the receipt*, but does not cryptographically prove the tree that was run; it only binds one input file. The control does now record exit status, fixing the original omission.

## Finding and smallest safe correction

Coverage remains bounded by syntactic checks: the counter does not check quotes, source revision contents, nor the claimed correction (frozen claim `plans/round-31-claims.md:30-42`). The second verifier checks URL-string identity, listed pin substrings, length and index title, but its six checks are presence tests (`round31_c1_verify.py:46-135`); source-line URL matching is not proof of a located quote at pinned bytes. Preserve the frozen counter but do not grant coverage from its line alone; require human/reviewer verification of the entry and cited quote locatability per the frozen kill rule.

For calibration, smallest safe receipt improvement: include the pre-append commit/tree hash (and preferably hash of the exact command output) alongside expect digest and exit. V6 currently validates only digest and literal `exit=1` (`round31_c1_verify.py:124-135`), so it cannot distinguish a recorded run on the pre-append tree from a recreated state.

VERDICT: V1 and the exact V2b stub-row fixture fell under current gates; V3's old-counter retarget survives only in `adoption_check.py` but fails overall on the hard-coded verifier path; V4b survives both counters by retargeting the tracked expectation; V8's expect-retarget-only forgery fell, while a zero-entry predicate state remains reproducible from a landed tree because the receipt pins no tree identity. Coverage claim survives only with reviewer-verified entry/quote evidence; calibration control is improved but not tree-authenticated.
