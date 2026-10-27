# R45CriticSeparability — causal separability of C1 (fence calibration) vs C2 (tb2 password-recovery grader)

Axes: (a) can either claim land without the other; (b) predicate-sentence identity claims-file vs counter
docstring (kumitate r42 lesson); (c) every pinned counter input exists at its pinned digest. All checks are
read-only on the lane at HEAD `05b02e2` (freeze `b4fcd35`, amendment `52d7486`, receipt `05b02e2`).

## A. Separability verdict: YES, structurally separable — with named shared surfaces (none verdict-changing)

**Input sets are disjoint.** `plans/round45_c1_verify.py` `PINS` (lines 65–99, 33 entries extracted with
`re.findall(r'"(plans/[^"]+)": "([0-9a-f]{64})"')`) covers only `plans/round44_c1_verify.py`, the ten
`plans/refusals45/f*.py` modules, and the 22 `plans/battery42|43|44` modules. `plans/round45_c2_verify.py`
pins only `plans/pkg-spec-r45.json`, `plans/pkg_gate.py`, `plans/password_recovery_probe.py`,
`corpus/evidence/round45/password-recovery-dry-cases-freeze.txt`, and the 9 captures under
`corpus/evidence/round45/tb2-password-recovery/` (`CAPTURES`, lines 74–84). Set intersection: **empty** — no
shared file, no shared capture, no shared counter input.

**Work surfaces are disjoint** (claims file line 30 states it and the counters confirm it): C1 writes
`plans/fixture_fence.py` (+ fence evidence); C2 writes `corpus/knowledge/tb2-password-recovery-grader.md`,
`corpus/SOURCES.md` rows S149–S156, README/PROVINCE lines, and `corpus/evidence/round45/password-recovery-probe.txt`.

**Either can land first.**
- C1 lands without C2: C1's counter runs the round-44 builder in a per-run scratch (`--work`), `strace`s the
  fence; it never touches C2 files (grep of the counter: no references to probe/spec/captures/SOURCES).
- C2 lands without C1: C2's V1–V11 never reference `fixture_fence.py`, `refusals45`, or the batteries (grep:
  zero hits for `fixture_fence|refusals45|battery4|round45_c1` outside docstring mentions — the only hit is
  docstring line 28 "battery45 intent", a stale round-44-era noun that should read "battery44"; cosmetic).

**Shared commits (cosmetic, not causal):** both instruments entered in one commit `b4fcd35` ("freeze claims,
C1 fence counter + hostile/control evidence, C2 password-recovery instruments"); both C2 files were amended
in `52d7486` ("C2 spec to 8 rows"). Shared commits do not couple the predicates — each counter measures its
own work surface on the landing clone.

**Shared claim-adjacent surfaces, tested and found safe:**
- `plans/round-45-claims.md` is one document carrying both claims. C2's V8 invokes
  `plans/order_check.py --claims plans/round-45-claims.md` — but `order_check.py:158-172` only needs the
  claims path committed in HEAD and its *add-commit* (`--diff-filter=A`), never its content. C1 editing its
  own section cannot move C2's V8. **However**, the file already drifted once post-freeze (defect 1).
- `.ufo/waves/round-45/claims/` is scanned by C2's V8 (`order_check.py:115-138` walks every committed blob
  under `claims/` up to the receipt commit, hunting `P10 ok`/`P10 DEFECT`-not-unreadable and
  `CASE … observed=` lines). Live scan of the working tree (`grep -rnE 'P10\s+(DEFECT|ok)|CASE…observed='`)
  found exactly one pattern-shaped line, `control-c2-nothing.txt:11: gate: P10 DEFECT receipt unreadable`,
  which `EXECUTED_EXCUSE` (`order_check.py:60,107`) expressly forgives. And the window is sealed: the receipt
  is already committed (`05b02e2`, receipt-commit = the scan's `upto`), so C1 wave evidence committed into
  `claims/` later is outside the scan by construction (`order_check.py:117` `rev-list upto -- claims_dir`).
  No coupling.
- `corpus/routed-findings.jsonl` (frontier ledger) is append-only output for the L1, not a counter input.

**Residual honest caveat:** the two claims are *textually* co-resident in `plans/round-45-claims.md`, so a
post-freeze edit to the file (one already happened) touches the same artifact both claims cite — a
provenance risk, not a verdict coupling.

## B. Predicate-sentence identity: NO — C2's identical sentence is absent from the claims file; C1's differs by one phrase

Normalized whitespace comparison (script: extract `C[12] passes iff.*?landing tip\.` from each file, flatten
whitespace, `==`):

- **C1** — claims file `round-45-claims.md:48-51`: "C1 passes iff **it** prints `PINS total=33 …`". Counter
  docstring `round45_c1_verify.py:37-41`: "C1 passes iff **`python3 plans/round45_c1_verify.py --lane .`**
  prints `PINS total=33 …`". Otherwise token-identical through "measured on a clean clone of the landing
  tip." → **not byte-identical** ("it" vs the command; referent unambiguous, but the docstring's claim
  "same sentence in plans/round-45-claims.md", line 36, is false as written).
- **C2** — the docstring sentence `round45_c2_verify.py:9-10` ("C2 passes iff `python3
  plans/round45_c2_verify.py --lane .` prints `checks=11 defects=0`, then `PREDICATE C2 pass`, exit 0,
  measured on a clean clone of the landing tip.") has **no counterpart in the claims file**. `round-45-claims.md:80`
  says only "Counter: `python3 plans/round45_c2_verify.py --lane .` → `checks=11 defects=0`, `PREDICATE C2
  pass`, exit 0." — a counter spec, not an iff-predicate; it omits "measured on a clean clone of the landing
  tip". The docstring's assertion "same sentence in plans/round-45-claims.md" (line 8) is false. This is the
  r42 pattern: two stated authorities, one canonical — fix by adding the docstring's sentence verbatim to the
  C2 section of the claims file (and swapping "it" for the command in C1's).

## C. Every pinned input exists at its pinned digest: YES for all in-counter pins; ledger defects around them

Verified with `sha256sum` / Python digest loop at HEAD:

- C1: all **33/33** `PINS` entries match on-disk bytes (loop printed `mismatches: none`).
- C2: all **9/9** `CAPTURES` digests match files under `corpus/evidence/round45/tb2-password-recovery/`;
  no extra capture files besides `SHA256SUMS`; `SPEC_SHA256`, `GATE_SHA256`, `PROBE_SHA256`, `DRY_SHA256`
  all match on-disk bytes.
- Receipt `corpus/evidence/round45/password-recovery-probe.txt` = sha256
  `587c8b345f8b0341e90640f83b78eafa7c5d5c996cac5e2d0a52a1131a8df23e` (exists, committed `05b02e2`).

**Defects found:**

1. **Frozen claims file mutated post-freeze.** `git show b4fcd35:plans/round-45-claims.md | sha256sum` =
   `79ede48a…` (the value in `frozen-digests.txt:6`); HEAD file = `1e63c4ba…`. Diff of `52d7486`: one cell,
   `S149–S157` → `S149–S156` (claims.md:71). The freeze was amended — permissible given the digest ledger
   was meant to record it, but see 2.
2. **`frozen-digests.txt` is an inconsistent ledger.** `52d7486` appended the *new* digests for
   `round45_c2_verify.py` (line 19, `8c30270…`, matches disk) and `pkg-spec-r45.json` (line 20,
   `3eb696b…`, matches disk) but left their **stale pre-amendment rows** in place (lines 2 `804df725…`,
   4 `b8fc1e53…`) and **never appended** the new claims digest `1e63c4ba…`. Result: two files carry
   duplicate contradictory authorities; the claims file's listed digest is simply wrong. Any verifier
   reading this list naively fails on all three files.
3. **C2 docstring overstates pin coverage.** `round45_c2_verify.py:12` asserts "Every input this counter
   reads that exists at the freeze is pinned here by digest." Counterexamples at the freeze:
   `plans/order_check.py` (executed by V8, sha256 `948d5e1d…`, round-39 instrument — unpinned);
   `plans/round-45-claims.md` (passed to V8 as a path — unpinned, and as defect 1 shows, mutable);
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (V6, `CENSUS` line 97 — a host-absolute,
   fleet-level script outside the lane's clone: unpinned *and* unfrozen, a real cross-lane mutability
   hole; any fleet edit to it changes every lane's V6 verdict).
4. **C2 predicate sentence missing from the claims file** (section B) — the docstring's sameness claim is
   false; the claims file lacks the iff-form and the clean-clone clause.
5. **C1 predicate sentence not byte-identical** (section B) — "it" vs the command; minor but the docstring
   asserts sameness.
6. **Cosmetic:** `round45_c2_verify.py:28` says "battery45 intent" — stale noun (battery45 was discarded
   per claims.md:17); should read battery44.

**Smallest safe corrections:** append the post-amendment digests for `round-45-claims.md` (and ideally mark
the two superseded rows) in `frozen-digests.txt`; add the verbatim iff-sentences to each claim's section in
the claims file; either pin `order_check.py`/`sources-census.sh`/claims-path digests in C2 or narrow the
docstring sentence to name the unpinned inputs; fix "battery45" → "battery44". All are L1-side edits at
integration, since these files are frozen for wave seats.

## Counterexample tested and survived

The strongest available counterexample to separability was C2-V8's `order_check` scanning the *shared*
`claims/` dir and the *shared* claims file: a C1-landing-side commit could in principle plant
`P10 ok`/`CASE … observed=` lines. It cannot move the verdict: the scan's `upto` is the already-committed
receipt commit `05b02e2` (`order_check.py:173-193`), the only matching committed line is an expressly
forgiven `P10 DEFECT receipt unreadable`, and the claims file's content is never read — only its
add-commit. Separability holds.

VERDICT: separable-yes-predicate-identical-no-defects-6
