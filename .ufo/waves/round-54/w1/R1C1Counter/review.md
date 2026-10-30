# R1C1Counter — R54-C1 correctness review

Axes: novelty (assigned), calibration (measurement honesty), correctness. Recommendation: do not rely on this counter for C1 admission. This is a review recommendation, not a judgment/admission. No production changes.

## Scope and evidence

Read the complete frozen claims file first (lines 1–222). Reviewed the entire added 575-line counter against base→freeze diff (`git -C LANE diff 6c919180260ea545589c2c0a007a06f554b529d3 17f90355c3ec17dcf15f7980d83f1943ae428fe5 -- plans/round54_c1_anchor.py`: 575 insertions). All counter line citations below refer to `plans/round54_c1_anchor.py` as read, snapshot 92A3. Claims snapshot 076A. No git mutation, clone, network, package install, or production edit.

LSP discovery: `read xd://lsp` returned `No such tool`; no server/status/references/definitions/diagnostics device is mounted. Literal fallback `grep 'round54_c1_anchor|verify_proof_bytes|_collect_digests' plans/` found the claims command and internal callers at 199,216,260,290,362; this is not semantic proof of repository-wide caller absence.

## Predicate leg → function → lines

| Frozen requirement | Executing implementation | Assessment |
|---|---|---|
| BINDING: clean SOURCE | `cmd_verify` 329–331 | Checked; failure returns tuple, not documented integer. |
| SOURCE HEAD == landing lane branch tip | `cmd_verify` 332–337 | Missing: HEAD is only checked against ancestor freeze_rev; no lane-tip comparison. |
| sha256 of exact committed freeze claims bytes, same proof digest | `_git` 61–62; `cmd_verify` 338–361; `canonical_digest` 75–77 | Git output decoded in text mode then re-encoded, not exact-byte-safe; additionally checks HEAD/disk equality. Proof reader broken. |
| ATTESTATION: deserialize, ≥1 Bitcoin attestation | `cmd_verify` 354–370 | Unreachable for valid serialized proof: raw stream passed instead of deserialization context. |
| Independent op walk from file digest | `_collect_digests` 143–174; callers 199–200,260–265,290–295,362–367 | Wrong library names/attributes; returns integer keys where callers expect timestamp nodes; no comparison to carried node.msg. |
| Derived attested digest = header merkle root | `cmd_verify` 370–384; optional library check 389–401 | Also wrongly requires attested digest == file digest (371–374), rejecting normal Merkle paths. |
| double-sha256(header) = explorer hash | `_double_sha256` 57–58; `cmd_verify` 380–387,425–426 | Implemented comparison, subject to earlier blockers. |
| EXTERNAL PIN: ≥2 files; independent public sources fetched this round | `cmd_verify` 413–429 | Counts files and arbitrary source strings only. URL/fetched_at presence is checked, not provenance/independence/freshness. |
| Receipt height/time agree; mainnet height floor | `cmd_verify` 375–376,422–426 | Comparisons present; height claim does not establish header membership in mainnet. |
| header time < landing after-run wall time | `cmd_verify` 404–409 | Compares against current verification clock, not recorded landing-receipt time. |
| stamped_at skew | `cmd_verify` 404–407 | One-sided `block_time >= stamped_at - 7200`; stamped_at is mutable metadata, no independent stamp-time authentication. |
| CONTROLS four cases fail same logic | `_verify_control_cases` 177–237; `cmd_verify` 432–440 | Different helpers; forged call has wrong arity; byte 5 is magic, not op path; count reports unexpected successes as failures. |
| Pass only if all four legs hold | `cmd_verify` 433–442 | Controls skipped unless flag supplied; canonical frozen command does supply it. Even with flag its forged-case exception becomes apparent success. |

## Findings (severity order)

### BLOCKER B1 — Every valid proof is rejected by the reader API

Lines 198,256,285,356 and selftest 527 call `DetachedTimestampFile.deserialize(fd)` on raw file/BytesIO streams. The installed library requires `StreamDeserializationContext`. Probe serialized a valid Bitcoin-attested tree using `StreamSerializationContext`: counter-style reader raised `AttributeError: '_io.BytesIO' object has no attribute 'assert_magic'`; the same bytes with `StreamDeserializationContext` parsed successfully. Main `cmd_verify` catches this and returns `_fail(...)` at 358, so honest confirmation can never reach ATTESTATION. Pending-only and forged selftests look green for this unrelated reader error.

### BLOCKER B2 — Independent walk cannot run, and its return type breaks every caller

At 152 initialization uses nonexistent `OpRipemd160`; observed `AttributeError: module 'opentimestamps.core.op' has no attribute 'OpRipemd160'`. Diagnostic isolation by prepopulating only the SHA256 map exposed another observed failure: append handling 161 uses nonexistent `OpAppend.arg`. Beyond these, 158 stores `id(ts)` as keys, but callers 200,263,293,365 access `ts.attestations`, which integers do not have. Isolated root walk returned keys `['int']`. These are independent blockers after fixing deserialization. `_collect_digests` never compares computed digest with each child.msg; an unreachable carried message is not explicitly rejected. The adversarial child probe presently crashes on `.arg` rather than proving structural rejection; no full forged-proof PASS is claimed.

### BLOCKER B3 — Reachability is confused with identity; real OTS Merkle proofs fail

Lines 371–374 require the selected attested digest to equal the original file digest. Frozen ATTESTATION requires a *path* from one to the other, not equality. A normal append/hash Merkle path changes the digest. Consequently correcting B1/B2 still rejects ordinary calendar aggregation proofs. Compare against the derived node digest and header root, not the original leaf digest. This is code-path evidence, not a live confirmed-proof run.

### MAJOR M1 — Controls silently certify an uncalled forged verifier, and report the count backwards

Caller 216 supplies four positional arguments; definition 272 requires five (`expect_setup_ok` has no default and is unused). Broad `except Exception` at 217–218 turns the resulting TypeError into `forged-proof failed-as-required` without any verification. At 198–204 another swallowed reader/walk failure sets the purported real header root to None. Byte 5 flipped at 211 is within the OTS magic (`004f70656e54696d65737461` prefix; byte5=84), not the serialized op path required by claims 79–82. Wrong-bundle is only a string-inequality helper at 221, not proof verification. Pending/absent call a partial helper rather than canonical `cmd_verify`.

Observed direct control invocation: `controls count 0` plus all four `failed-as-required` lines. `case()` increments `failed` when a control unexpectedly PASSES (188–190), and final gating 438 correctly fails on unexpected successes, but 435 prints that count as `failed`. Thus honest rejection prints `CONTROLS forged=4 failed=0`, contrary to frozen required `failed=4`; it also masks invalid control execution as rejection. Fixing print wording alone does not repair coverage.

### MAJOR M2 — External provenance/freshness and scoring-time ordering are not enforced

Lines 422–429 only require source/url/fetched_at keys, compare hash/height/time, and count distinct user-controlled source strings. No parsing or temporal comparison of fetched_at, no source identity normalization/public-source requirement, no check URL agrees with source, no evidence the header is actually from the claimed public chains. Two relabeled stale/fabricated receipts satisfy this block's checks. No PoW/chain verification supplies an alternative external witness. This is a latent bypass in this leg, not a demonstrated end-to-end PASS because B1–B3 prevent one.

Lines 404–409 use `time.time()` when re-verifying, never the landing receipt's after-run wall time required by claims 77–78. A block after scoring but before later verification would pass this local comparison. stamped_at skew has an explicit lower-bound check, but arbitrary backdating of metadata is not independently detected.

### MAJOR M3 — SOURCE/anchor commitment checks do not establish the declared landing state

`tip` at 332 is SOURCE HEAD; no comparison to lane branch tip exists. Any clean source descendant of freeze_rev with equal claims satisfies the source tests even when not landing tip. Metadata/proof/header/receipts are read from independently supplied anchor path (305–311,321,355,380,413), never bound to committed SOURCE bytes or verified tracked there. Frozen after-target requires committed artifacts and clean landing-tip measurement. The implementation cannot establish either fact for those supplied artifacts.

### MAJOR M4 — Failure return contract is inconsistent and diagnostics disappear

`_fail` and `_setup` return `(rc, lines)` at 65–72. Many `cmd_verify` branches return that tuple directly (331,335,337,340,349,358,361,369,374,376,382,384,398,401,403,407,409,415,421,424,426,429); `main` forwards it into `sys.exit` at 575. The CLI then emits a tuple on stderr, exits 1 even for setup-class 2, and omits the specified predicate/leg stdout diagnostics. Schema/empty freeze branches instead take `[0]` but never print their accumulated setup messages (323,326). JSON errors and unsupported-walk errors can escape. Fail-closed is not success, but promised usage/error observables are broken.

### MINOR m1 — Exact-byte binding and CLI/documentation mismatches

`_git(..., text=True)` normalizes line endings before 341 re-encoding, so it does not hash exact committed bytes for arbitrary claims bytes; actual frozen UTF-8/LF claims are not shown affected. `_sha256` 53–54 is annotated bytes but returns hex str and is unused. `--selftest` exits 2; the supported command is `selftest` (568). `--calendar` is recorded in metadata (112) but not passed to stamp subprocess (98). These do not repair or worsen the main blocked predicate.

No NIT-only findings.

## Selftest execution and case fidelity

Runtime: `/fast/scratch/hyaku/kengaku-r54/l1/venv/otsenv/bin/python`; counter absolute lane path; `TMPDIR=/fast/scratch/hyaku/kengaku-r54/R1C1Counter`, `PYTHONDONTWRITEBYTECODE=1`.

1. Requested literal `python COUNTER --selftest`: exit 2, argparse `the following arguments are required: cmd`.
2. Supported `python COUNTER selftest`: exit 0, `[selftest] 8/8 PASS`.

| Case | Lines | Does it test its name? |
|---|---|---|
| digest-canonical | 457–458 | Yes: compares canonical digest to independent standard-library expression; narrow. |
| pending-only-fails | 460–470 | No semantic attestation test: malformed reader API rejects even valid proof. |
| absent-fails | 472–474 | Yes: nonexistent file returns setup rc=2, expected nonzero. |
| attestation-good-header-passes | 487–500 | Yes: library merkle-root check on synthetic header; not canonical verifier or real chain membership. |
| attestation-bad-header-fails | 494–501 | Yes: mismatched merkle root must raise. Broad exception accepts unrelated exceptions too. |
| attestation-short-digest-fails | 502–507 | Yes: short digest library call must raise; same broad-exception caveat. |
| bitcoinlib-present | 477–479,508–510 | Import sentinel only; condition literally True after successful import, not a verifier correctness check. |
| forged-proof-fails | 512–532 | Vacuous integrity evidence: starts pending-only (already must fail), and bad stream API always raises; untouched proof also fails. Does not show flipping caused rejection. |

None exercises `cmd_verify` successful path, `_collect_digests` success, EXTERNAL PIN, source-tip equivalence, time ordering, or actual control harness wiring. Thus 8/8 is observed but not evidence the predicate works.

## Probe receipt

Preserved source: `probe.py` alongside this report. The final probe run exited 0 and printed:

```text
counter-reader AttributeError '_io.BytesIO' object has no attribute 'assert_magic'
context-reader OK
valid-tree AttributeError module 'opentimestamps.core.op' has no attribute 'OpRipemd160'
isolated-unreachable-child AttributeError 'OpAppend' object has no attribute 'arg'
isolated-root keys ['int']
controls count 0
  CONTROL forged-proof failed-as-required (flipped digest byte must break verification)
  CONTROL wrong-bundle failed-as-required (binding rc=1)
  CONTROL pending-only failed-as-required (attestation leg rc=1)
  CONTROL absent failed-as-required (attestation leg rc=2)
proof prefix byte5 84 header prefix 004f70656e54696d65737461
```

The in-process `_UNARY_ALGOS` prepopulation is explicitly diagnostic isolation, not a production fix or end-to-end bypass. Earlier probe attempts stopped on immutable child.msg assignment, then missing `.arg`; the final preserved version handles these without claiming reachability was rejected correctly.

## Residual risk and verification gaps

No confirmed upgraded live anchor was verified end-to-end; no public explorer network fetch was performed; no runtime forged-PASS or frozen kill-rule admission is asserted. Static external-pin bypass descriptions apply to the local block after prior blockers are repaired, not the currently unreachable whole command. Prior-art novelty cap and saturation are outside this seat's review: no score increase is recommended from 8/8. No resume/rerouting/runtime integration changes exist in the assigned diff. L1 should retain the frozen instrument and route any repair via its amendment contract, then rerun a positive canonical verify plus correctly causal controls, fresh-source provenance and landing-time tests. No tools installed. Scratch removed before handoff.

Self-evaluation: accuracy 4 (no confirmed live-proof run); completeness 4 (semantic LSP unavailable); clarity 4 (many independent blockers require detail); actionability 4 (frozen repair policy belongs to L1); conciseness 4 (case map retained for requested thoroughness); overall 4.0. Highest-impact improvement is an authorized canonical positive-path run after the reader/walk/control defects are resolved.
