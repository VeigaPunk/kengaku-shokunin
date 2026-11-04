# ReviewerC1R80 — independent C1 review

## Findings (severity order)

**P1 — R80-C1's exact reproduction requirement fails for largest-eigenval.** At measured tip `6669fe72e59718acc1a0f32a92849a544b0b2f1c`, `corpus/evidence/round80/largest-eigenval-probe.txt:36,38–39` says the unpredicted timing outcome for size 10 was F. The fresh frozen instrument returns P. It exits 0 because its own predicate excludes observed-only U cases; that does not satisfy round 80's separate byte-equality contract. The committed block SHA256 is `d44ecaed4ca81ca14344fe04aeb95f485e5c1ebe10e0a0a218d899138b839bb6`; fresh stdout excluding REV hashes to `463877700639fcf7a522b207cbf88a3a6eebd2aa40d6afd5e1c258087ce8c784`. The historical-divergence note covers historical-to-minted divergence, not a fresh replay mismatch. No rerun was used to replace this failure. The canonical original probe itself explicitly warns that these outcomes depend on host noise (`plans/round57_c2_eigen_probe.py:19–27`). Recommendation: do not admit the six-of-six exact-reproduction claim on these bytes. Do not silently normalize the timing observations or revise the frozen predicate.

**P1 — Frozen observation contract was edited, and protein's receipt violates the frozen grammar.** `plans/round-80-claims.md` differs from freeze `af51132d8919cedd14d3d3407ae5abc966d5d427`: frozen lines 44–47 require every OBSERVATIONS line to match an enumerated observation form; the tip changes that rule to allow arbitrary instrument stdout. `corpus/evidence/round80/protein-assembly-probe.txt:13–14` contains `grader=...` and `components_aa=...`, neither allowed by the original list. These bytes do reproduce; the defect is the unapproved contract change, not fabrication or a wrong subject. Restore the authoritative freeze for evaluation; contract changes need the supervising owner's decision, not a reviewer edit. This report does not reopen any predicate or propose a weaker substitute.

## Scope, axes, identity

Axes: **coverage** (held at L0 cap), **calibration** (held at 10, exercised). This review measures C1 only; no new score, saturation, task certification, model success, or C2 admission is claimed.

Base `dce7c275381c669e6489f1b795b1505d0824c262`; freeze `af51132d8919cedd14d3d3407ae5abc966d5d427`; measured master `6669fe72e59718acc1a0f32a92849a544b0b2f1c`. The latter is an integration commit, distinct from freeze. A single clean `git clone --shared --no-checkout` was checked out detached at the measured commit after asserting the clone's top-level directory. All receipts/tools/history were read from that clone, not live uncommitted lane files. No C1 gate was imported or executed. No other agent runtime or subagent was invoked.

Commands and observed setup output:

```text
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse master
6669fe72e59718acc1a0f32a92849a544b0b2f1c
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r80/ReviewerC1R80/lane
Cloning into '/fast/scratch/hyaku/kengaku-r80/ReviewerC1R80/lane'...
done.
git -C /fast/scratch/hyaku/kengaku-r80/ReviewerC1R80/lane rev-parse --show-toplevel
/fast/scratch/hyaku/kengaku-r80/ReviewerC1R80/lane
git -C /fast/scratch/hyaku/kengaku-r80/ReviewerC1R80/lane checkout --detach 6669fe72e59718acc1a0f32a92849a544b0b2f1c
HEAD is now at 6669fe72 round-80: integration — six located replays minted and the ledger flipped (R80-C1), V1-V6 routed rows plus the V1 receipt and corrections (R80-C2), S258, lesson, index, wave spec/dispatch
```

LSP availability: `read xd://lsp` returned `No such tool: xd://lsp`. Thus no answering server was available; references/definitions/diagnostics were unavailable. JSON parsing, literal byte comparisons and git diffs below are not presented as semantic LSP proof.

## Independent derivation and grades

Extractor command: `python3 /fast/scratch/hyaku/kengaku-r80/ReviewerC1R80/review.py` (rc 0 means the extractor completed, **not** that every member passed). It reads base JSON with `git show dce7c275381c669e6489f1b795b1505d0824c262:plans/grader-population-ledger.json`, selects `status == executed-unlocated`, then reads each tip row. Output:

```text
BASE dce7c275381c669e6489f1b795b1505d0824c262 TIP 6669fe72e59718acc1a0f32a92849a544b0b2f1c
DERIVED_TARGETS ["cancel-async-tasks", "chess-best-move", "distribution-search", "largest-eigenval", "openssl-selfsigned-cert", "protein-assembly"]
TIP_UNLOCATED []
```

Every target's base row was executed-unlocated with debt=no-subject-stamp. Every tip row is executed, subject=tb2-header, round=80. All six receipt first lines have the subject prefix `# tb2 <member> grader probe` followed by `(round 80 re-mint)`; this is a shape match, not an exact-string claim. All six are tracked; stamp source/tool names match the frozen table and both SHA256 fields match measured bytes. All stamp LANE_TIP values are `6250e94b2adaff8cd22d32f7ab45024f092e3235` and `git merge-base --is-ancestor <stamp> HEAD` returned 0. Every stamp records WORKTREE clean and EXIT 0. Stamp commands match frozen prefixes/argv after substituting work/output locations. Five verdicts derive as predicate; protein derives as cases.

| Member | Grade | Deciding evidence |
|---|---|---|
| cancel-async-tasks | SUPPORTED | receipt :1–10 stamps match; OBSERVATIONS hash equals fresh stdout hash below; verdict=predicate |
| chess-best-move | SUPPORTED | receipt :1–10 stamps match; OBSERVATIONS hash equals fresh stdout hash below; verdict=predicate |
| distribution-search | SUPPORTED | receipt :1–10 stamps match; OBSERVATIONS hash equals fresh stdout hash below; verdict=predicate |
| largest-eigenval | OVERCLAIMED | receipt :36,38–39 fails fresh byte equality; verdict=predicate |
| openssl-selfsigned-cert | SUPPORTED | receipt :1–10 stamps match; OBSERVATIONS hash equals fresh stdout hash below; verdict=predicate |
| protein-assembly | OVERCLAIMED | receipt :13–14 violates frozen observation grammar; raw stdout does reproduce; verdict=cases |

“OVERCLAIMED” here distinguishes genuine successful execution from the stronger six-member frozen-contract claim. None of the six is unsupported as evidence of an executed synthetic probe. Under the tip's broadened grammar alone, protein would be SUPPORTED; it is not silently judged under that changed contract.

## Per-member command/output and byte evidence

The six commands ran concurrently with isolated work/output directories; the task explicitly asks fresh frozen-instrument runs. TMPDIR, UV_CACHE_DIR and bytecode settings kept writes inside this seat's scratch. Full fresh stdout and stderr follow. All six exited 0; only five exact-reproduced committed block bytes.

### cancel-async-tasks

Receipt `corpus/evidence/round80/cancel-async-tasks-probe.txt`, SHA256 `7923b6dc39a1c201bd92ab3e4b6651a4c5ff83bc9a5606a1162a29bb6aa7f74e`.

SOURCE_SHA (stamp and measured bytes): `3a69fddb8ab817bf78dad57b4d28e1c964b288c433901560fa98f59ff306922a`.

TOOL_SHA (stamp and measured bytes): `92facdc762bdb29c581eb92b5951f0855bec0de7dc56c8d2308136c889fe7f87`.

OBSERVATIONS SHA256 `24b858f1b23926a04c77fd251338973bfca9196885f4327d3f11954d26247a9c`; fresh normalized stdout SHA256 `24b858f1b23926a04c77fd251338973bfca9196885f4327d3f11954d26247a9c`. Historical observations differ: False; required divergence note present where applicable.

Tip ledger row:
```json
{"classes": ["file-artifact", "signal-delivery", "stdout-inspection", "subprocess-exec", "timing-wall"], "receipt": "corpus/evidence/round80/cancel-async-tasks-probe.txt", "round": 80, "status": "executed", "subject": "tb2-header", "verdict": "predicate"}
```
```text
$ python3 plans/round61_c1_cancel_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r80/ReviewerC1R80/cancel-async-tasks.work --receipt /fast/scratch/hyaku/kengaku-r80/ReviewerC1R80/cancel-async-tasks.out
exit=0
stdout:
REV 6669fe72e59718acc1a0f32a92849a544b0b2f1c
CASE compliant-signal-handler predicted=P/P/P/P/P/P observed=P/P/P/P/P/P ok
CASE threadpool-uncancelled predicted=P/P/P/P/P/F observed=P/P/P/P/P/F ok
CASE kbdint-no-handler predicted=P/P/P/F/F/F observed=P/P/P/F/F/F ok
CASE sequential-sync predicted=P/F/P/F/F/F observed=P/F/P/F/F/F ok
CASE cleanup-missing predicted=P/F/F/F/F/F observed=P/F/F/F/F/F ok
CASE cleanup-double predicted=P/F/F/F/F/F observed=P/F/F/F/F/F ok
CASE started-premature predicted=P/P/P/P/P/F observed=P/P/P/P/P/F ok
CASE partial-cancel predicted=P/P/P/F/F/F observed=P/P/P/F/F/F ok
CASE ignore-sigint predicted=P/P/P/P/P/F observed=P/P/P/P/P/F ok
CASE late-cancel-cleanup predicted=P/P/P/F/F/F observed=P/P/P/F/F/F ok
CASE no-max-enforcement predicted=P/P/F/P/P/F observed=P/P/F/P/P/F ok
CASE no-run-py predicted=F/P/P/P/P/P observed=F/P/P/P/P/P ok
cases=12 legs=72 mismatches=0 setup=0 predicted_u=0
PREDICATE R61-C1 pass
stderr:
(empty)
```

### chess-best-move

Receipt `corpus/evidence/round80/chess-best-move-probe.txt`, SHA256 `b32f4b37d7e4e93ecf104cba131dda30df980dfd3078ccaf2a01f13ddd15003c`.

SOURCE_SHA (stamp and measured bytes): `de0826692f8b81c832b8d0633cfe8fa080f2d6142ee9d71b597eba6be9d8aaca`.

TOOL_SHA (stamp and measured bytes): `7bd2863ca745f1656a23617d66a1926b12e2656b17fdc903b69d3eb28ce72d60`.

OBSERVATIONS SHA256 `de0826692f8b81c832b8d0633cfe8fa080f2d6142ee9d71b597eba6be9d8aaca`; fresh normalized stdout SHA256 `de0826692f8b81c832b8d0633cfe8fa080f2d6142ee9d71b597eba6be9d8aaca`. Historical observations differ: False; required divergence note present where applicable.

Tip ledger row:
```json
{"classes": ["file-artifact"], "receipt": "corpus/evidence/round80/chess-best-move-probe.txt", "round": 80, "status": "executed", "subject": "tb2-header", "verdict": "predicate"}
```
```text
$ python3 plans/round55_c3_chess_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r80/ReviewerC1R80/chess-best-move.work --receipt /fast/scratch/hyaku/kengaku-r80/ReviewerC1R80/chess-best-move.out
exit=0
stdout:
CASE both-lowercase-two-lines predicted=P observed=P rc=0
CASE both-space-separated predicted=P observed=P rc=0
CASE reversed-order predicted=P observed=P rc=0
CASE single-move-only predicted=F observed=F rc=1
CASE uppercase-white predicted=F observed=F rc=1
CASE extra-decoy-move predicted=F observed=F rc=1
CASE duplicate-move predicted=F observed=F rc=1
CASE whitespace-padded predicted=P observed=P rc=0
CASE empty-file predicted=F observed=F rc=1
CASE crlf-line-endings predicted=P observed=P rc=0
CASE instruction-example-h1h8 predicted=F observed=F rc=1
CASE fullwidth-unicode-digit predicted=F observed=F rc=1
cases=12 observed_pass=5 observed_fail=7 mismatches=0
PREDICATE R55-C3 pass
stderr:
(empty)
```

### distribution-search

Receipt `corpus/evidence/round80/distribution-search-probe.txt`, SHA256 `fd337d12dff0210e3d84f4ed22619dc92976006677b7ba835dfa959ff69b188d`.

SOURCE_SHA (stamp and measured bytes): `3c93e06a88a6ec8e77b0ed1b81ad298a492513e3f5e7c9f20d6641da5ee53c1f`.

TOOL_SHA (stamp and measured bytes): `51c192f2f98186acb439cb69c2e0370860c362e3bdcb267afea93cd547fa6760`.

OBSERVATIONS SHA256 `0dd2f94963dbedc30aab29494c50581067ce8d7e365a366beb67d1bf179895b8`; fresh normalized stdout SHA256 `0dd2f94963dbedc30aab29494c50581067ce8d7e365a366beb67d1bf179895b8`. Historical observations differ: False; required divergence note present where applicable.

Tip ledger row:
```json
{"classes": ["numeric-band"], "receipt": "corpus/evidence/round80/distribution-search-probe.txt", "round": 80, "status": "executed", "subject": "tb2-header", "verdict": "predicate"}
```
```text
$ python3 plans/round58_c2_kl_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r80/ReviewerC1R80/distribution-search.work --receipt /fast/scratch/hyaku/kengaku-r80/ReviewerC1R80/distribution-search.out
exit=0
stdout:
REV 6669fe72e59718acc1a0f32a92849a544b0b2f1c
CASE sol predicted=P/P/P/P observed=P/P/P/P ok
CASE uniform predicted=P/P/P/F observed=P/P/P/F ok
CASE kb-only-m7 predicted=P/P/P/F observed=P/P/P/F ok
CASE minzero predicted=P/P/F/F observed=P/P/F/F ok
CASE negatom predicted=P/P/F/F observed=P/P/F/F ok
CASE nanatom predicted=P/P/F/F observed=P/P/F/F ok
CASE sumdrift predicted=P/P/F/P observed=P/P/F/P ok
CASE wrongvocab-m5 predicted=P/F/P/F observed=P/F/P/F ok
CASE twod predicted=P/F/P/P observed=P/F/P/P ok
CASE maxover predicted=P/P/F/F observed=P/P/F/F ok
CASE tolbnd predicted=P/P/P/P observed=P/P/P/P ok
CASE intcounts predicted=P/P/F/P observed=P/P/F/P ok
cases=12 legs=48 mismatches=0 setup=0 predicted_u=0
PREDICATE R58-C3 pass
stderr:
(empty)
```

### largest-eigenval

Receipt `corpus/evidence/round80/largest-eigenval-probe.txt`, SHA256 `9179d62d67d1f1d43cfb4ac5fb7dcd33918ce589f1b03ed8176b9a623c3f4493`.

SOURCE_SHA (stamp and measured bytes): `463877700639fcf7a522b207cbf88a3a6eebd2aa40d6afd5e1c258087ce8c784`.

TOOL_SHA (stamp and measured bytes): `4f2b8bebb451c5f67d26dc06c76dbd99f3a459f41d9e8a8d555af12d15e0f105`.

OBSERVATIONS SHA256 `d44ecaed4ca81ca14344fe04aeb95f485e5c1ebe10e0a0a218d899138b839bb6`; fresh normalized stdout SHA256 `463877700639fcf7a522b207cbf88a3a6eebd2aa40d6afd5e1c258087ce8c784`. Historical observations differ: True; required divergence note present where applicable.

Tip ledger row:
```json
{"classes": ["numeric-band", "timing-wall"], "receipt": "corpus/evidence/round80/largest-eigenval-probe.txt", "round": 80, "status": "executed", "subject": "tb2-header", "verdict": "predicate"}
```
```text
$ python3 plans/round57_c2_eigen_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r80/ReviewerC1R80/largest-eigenval.work --receipt /fast/scratch/hyaku/kengaku-r80/ReviewerC1R80/largest-eigenval.out
exit=0
stdout:
CASE eig-sleep-pair-s2 predicted=P observed=P rc=0
CASE eig-bare-pair-s2 predicted=P observed=P rc=0
CASE zero-e1-pair-s2 predicted=F observed=F rc=1
CASE eig-sleep-pair-s5 predicted=P observed=P rc=0
CASE eig-bare-pair-s5 predicted=P observed=P rc=0
CASE zero-e1-pair-s5 predicted=F observed=F rc=1
CASE eig-sleep-pair-s10 predicted=P observed=P rc=0
CASE eig-bare-pair-s10 predicted=P observed=P rc=0
CASE zero-e1-pair-s10 predicted=F observed=F rc=1
CASE eig-sleep-dom-s2 predicted=P observed=P rc=0
CASE eig-bare-dom-s2 predicted=P observed=P rc=0
CASE zero-e1-dom-s2 predicted=F observed=F rc=1
CASE eig-sleep-dom-s5 predicted=P observed=P rc=0
CASE eig-bare-dom-s5 predicted=P observed=P rc=0
CASE zero-e1-dom-s5 predicted=F observed=F rc=1
CASE eig-sleep-dom-s10 predicted=P observed=P rc=0
CASE eig-bare-dom-s10 predicted=P observed=P rc=0
CASE zero-e1-dom-s10 predicted=F observed=F rc=1
CASE eig-sleep-speed-s2 predicted=F observed=F rc=1
CASE eig-bare-speed-s2 predicted=U observed=F rc=1 (observed-only)
CASE zero-e1-speed-s2 predicted=P observed=P rc=0
CASE eig-sleep-speed-s10 predicted=F observed=F rc=1
CASE eig-bare-speed-s10 predicted=U observed=P rc=0 (observed-only)
CASE zero-e1-speed-s10 predicted=P observed=P rc=0
cases=24 observed_pass=15 observed_fail=9 mismatches=0 setup=0
OBSERVED-U eig-bare-speed-s2=F eig-bare-speed-s10=P
PREDICATE R57-C2 pass
stderr:
(empty)
```
Exact failure diff:
```diff
--- committed OBSERVATIONS
+++ fresh stdout
@@ -20,8 +20,8 @@
 CASE eig-bare-speed-s2 predicted=U observed=F rc=1 (observed-only)
 CASE zero-e1-speed-s2 predicted=P observed=P rc=0
 CASE eig-sleep-speed-s10 predicted=F observed=F rc=1
-CASE eig-bare-speed-s10 predicted=U observed=F rc=1 (observed-only)
+CASE eig-bare-speed-s10 predicted=U observed=P rc=0 (observed-only)
 CASE zero-e1-speed-s10 predicted=P observed=P rc=0
-cases=24 observed_pass=14 observed_fail=10 mismatches=0 setup=0
-OBSERVED-U eig-bare-speed-s2=F eig-bare-speed-s10=F
+cases=24 observed_pass=15 observed_fail=9 mismatches=0 setup=0
+OBSERVED-U eig-bare-speed-s2=F eig-bare-speed-s10=P
 PREDICATE R57-C2 pass
```

### openssl-selfsigned-cert

Receipt `corpus/evidence/round80/openssl-selfsigned-cert-probe.txt`, SHA256 `08c10b0d12e18e39daf834538da039c9e31474858a7b3ce3d6d2c393db7b8585`.

SOURCE_SHA (stamp and measured bytes): `ae89476cde80dfeb09106af53c8eab43a89afcde696d800ec0d0c60aa309b094`.

TOOL_SHA (stamp and measured bytes): `6faf217c723efaf8d24bd15a9e8aeb873328af4a7f8e9c4ab4ca94b2465d4646`.

OBSERVATIONS SHA256 `dc02aab0cca295f57cf54bfd0ea09dc0231b6ecac0715ca3ed8493af8730151c`; fresh normalized stdout SHA256 `dc02aab0cca295f57cf54bfd0ea09dc0231b6ecac0715ca3ed8493af8730151c`. Historical observations differ: True; required divergence note present where applicable.

Tip ledger row:
```json
{"classes": ["crypto-credential", "file-artifact", "filesystem-metadata", "stdout-inspection", "subprocess-exec"], "receipt": "corpus/evidence/round80/openssl-selfsigned-cert-probe.txt", "round": 80, "status": "executed", "subject": "tb2-header", "verdict": "predicate"}
```
```text
$ python3 plans/round59_c1_openssl_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r80/ReviewerC1R80/openssl-selfsigned-cert.work --receipt /fast/scratch/hyaku/kengaku-r80/ReviewerC1R80/openssl-selfsigned-cert.out
exit=0
stdout:
REV 6669fe72e59718acc1a0f32a92849a544b0b2f1c
CASE sol predicted=P/P/P/P/P/P observed=P/P/P/P/P/P ok
CASE perm-loose predicted=P/F/P/P/P/P observed=P/F/P/P/P/P ok
CASE key-1024 predicted=P/F/P/P/P/P observed=P/F/P/P/P/P ok
CASE days-30 predicted=P/P/F/P/P/P observed=P/P/F/P/P/P ok
CASE cn-wrong predicted=P/P/F/P/F/F observed=P/P/F/P/F/F ok
CASE pem-keyonly predicted=P/P/P/F/P/P observed=P/P/P/F/P/P ok
CASE pem-garbage predicted=P/P/P/F/P/P observed=P/P/P/F/P/P ok
CASE fp-absent predicted=P/P/P/P/F/P observed=P/P/P/P/F/P ok
CASE script-silent predicted=P/P/P/P/P/F observed=P/P/P/P/P/F ok
CASE dir-absent predicted=F/F/F/F/F/F observed=F/F/F/F/F/F ok
CASE org-upper predicted=P/P/P/P/P/P observed=P/P/P/P/P/P ok
CASE script-missing predicted=P/P/P/P/P/F observed=P/P/P/P/P/F ok
cases=12 legs=72 mismatches=0 setup=0 predicted_u=0
PREDICATE R59-C1 pass
stderr:
(empty)
```

### protein-assembly

Receipt `corpus/evidence/round80/protein-assembly-probe.txt`, SHA256 `82b910af1d9333e5479bbf7379e5e66341bea44e41ba81765a35758b5322da5b`.

SOURCE_SHA (stamp and measured bytes): `2359d9067906f59d2c55b5802603d1ef45c376f653ad9997de1ef7da412b25b8`.

TOOL_SHA (stamp and measured bytes): `acd7d38dca3a982d22900ca034c50aa3d22817395273bbc62b5665b1913040d0`.

OBSERVATIONS SHA256 `702d020c356779cdf4b51c2d6861b748f220427a5aba5c63337f1b90812fd531`; fresh normalized stdout SHA256 `702d020c356779cdf4b51c2d6861b748f220427a5aba5c63337f1b90812fd531`. Historical observations differ: False; required divergence note present where applicable.

Tip ledger row:
```json
{"classes": ["file-artifact"], "receipt": "corpus/evidence/round80/protein-assembly-probe.txt", "round": 80, "status": "executed", "subject": "tb2-header", "verdict": "cases"}
```
```text
$ uv run --no-project --with biopython python3 plans/tb2_grader_probe.py --lane .
exit=0
stdout:
grader=corpus/evidence/round35/tb2-eval/test_outputs.py sha256=44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582 pin=2fd12b88aafdd04a52c298e3940bcb189f9766d6 biopython=1.88
components_aa=8,259,158,235,182 max_passing_nt=2766 cap_nt=3000
case=valid-balanced predicted=pass observed=pass match=yes nt=2586 gcwin=ok assertion='-' requirement='all bullets: GS linkers 5..20, order, no Met/stop, GC windows, <=3000 nt'
case=uppercase predicted=pass observed=pass match=yes nt=2586 gcwin=ok assertion='-' requirement='file holds only the sequence (case is not specified)'
case=no-trailing-newline predicted=pass observed=pass match=yes nt=2586 gcwin=ok assertion='-' requirement='file holds only the sequence'
case=trailing-empty-line predicted=fail observed=fail match=yes nt=2586 gcwin=ok assertion='Invalid number of lines in gblock.txt.' requirement='No empty lines'
case=start-codon-prefixed predicted=fail observed=fail match=yes nt=2589 gcwin=ok assertion='Start of gBlock must match flag protein.' requirement='no start codon / remove N-terminal Met'
case=stop-codon-appended predicted=fail observed=fail match=yes nt=2589 gcwin=ok assertion='End of gBlock must match snap protein.' requirement='no stop codon'
case=linker-4aa predicted=fail observed=fail match=yes nt=2583 gcwin=ok assertion='Linker must be between 5 and 20 amino acids long.' requirement='linkers 5..20 aa'
case=linker-21aa predicted=fail observed=fail match=yes nt=2634 gcwin=ok assertion='Linker must be between 5 and 20 amino acids long.' requirement='linkers 5..20 aa'
case=linker-20aa predicted=pass observed=pass match=yes nt=2631 gcwin=ok assertion='-' requirement='linkers 5..20 aa (upper bound inclusive)'
case=linker-non-gs predicted=fail observed=fail match=yes nt=2586 gcwin=ok assertion='Linker must only contain G and S amino acids.' requirement='only GS linkers between subproteins'
case=linker-g-only predicted=pass observed=pass match=yes nt=2586 gcwin=ok assertion='-' requirement='GS linkers (a G-only linker is not distinguished)'
case=n-terminal-linker predicted=fail observed=fail match=yes nt=2601 gcwin=ok assertion='Start of gBlock must match flag protein.' requirement='no GS linker on the N terminus'
case=c-terminal-linker predicted=fail observed=fail match=yes nt=2601 gcwin=ok assertion='End of gBlock must match snap protein.' requirement='no GS linker on the C terminus'
case=donor-acceptor-swapped predicted=fail observed=fail match=yes nt=2586 gcwin=ok assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' requirement='subprotein order'
case=donor-one-substitution predicted=fail observed=fail match=yes nt=2586 gcwin=ok assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' requirement='donor matches its PDB sequence'
case=donor-repeated predicted=fail observed=fail match=yes nt=3378 gcwin=ok assertion='gBlock must be at most 3000 nucleotides.' requirement='do not repeat a protein'
case=non-acgt-base predicted=fail observed=fail match=yes nt=2586 gcwin=ok assertion='gBlock must contain only A, T, C, G.' requirement='gBlock is a DNA sequence'
case=gc-window-high predicted=fail observed=fail match=yes nt=2586 gcwin=violated assertion='GC content must be between 30 and 70% in all 50 nucleotide windows.' requirement='GC 30..70% in every 50-nt window'
cases=18 observed_pass=5 observed_fail=13 mismatches=0
stderr:
Downloading biopython (3.1MiB)
Downloading numpy (15.9MiB)
 Downloaded biopython
 Downloaded numpy
Installed 2 packages in 70ms
```

## Frozen contract comparison

Command: `git -C /fast/scratch/hyaku/kengaku-r80/ReviewerC1R80/lane diff af51132d8919cedd14d3d3407ae5abc966d5d427 6669fe72e59718acc1a0f32a92849a544b0b2f1c -- plans/round-80-claims.md plans/round80_probes.json` (rc 0):

```diff
diff --git a/plans/round-80-claims.md b/plans/round-80-claims.md
index d2ef65f3..c2ce438d 100644
--- a/plans/round-80-claims.md
+++ b/plans/round-80-claims.md
@@ -14,8 +14,9 @@ predicate sentence below is the same sentence in the counter's code and in the r
 tracked receipt under `corpus/evidence/round80/` whose first line is the frozen subject shape
 `# tb2 <member> grader probe`, whose stamp block names the historical receipt with its sha256, the
 instrument with its sha256 at the measured tip, a `LANE_TIP` reachable from the measured tip,
-`WORKTREE clean`, `EXIT 0` and the command that replays it, whose observation lines equal a fresh
-re-run of that frozen instrument at the measured tree, and whose ledger row is `executed` with
+`WORKTREE clean`, `EXIT 0` and the command that replays it, whose `OBSERVATIONS` block equals the
+instrument's stdout at the measured tree (`REV <commit>` lines excluded on both sides, because the
+block is committed bytes and the measured tip moves), and whose ledger row is `executed` with
 `subject=tb2-header`, the receipt's own observation form as `verdict`, and `round=80`; and the
 round-79 population gate still exits 0 with `executed=24 unlocated=0`.
 
@@ -42,9 +43,12 @@ Target (after): `TARGET members=6 located=6 reproduced=6 ledger_flipped=6 diverg
 ledger_flipped=0`, `DEFECTS n>=6`, exit 1.
 
 **Observation forms (frozen).** A receipt's observation block is every line between
-`OBSERVATIONS_BEGIN` and `OBSERVATIONS_END`; every such line must match one of
+`OBSERVATIONS_BEGIN` and `OBSERVATIONS_END`, written verbatim from the instrument's stdout with
+`REV <commit>` lines removed (the block is committed bytes, so a commit-dependent line would make
+every later replay mismatch). The *observation lines* are those matching one of
 `^CASE `, `^case=`, `^cases=`, `^MISMATCH `, `^OBSERVED-U `, `^VECTOR `,
-`^PREDICATE R<n>-C<m> (pass|fail)`. `REV` lines are excluded (commit-dependent). The ledger row's
+`^PREDICATE R<n>-C<m> (pass|fail)`; the tool's own other lines (e.g. `grader=`, `components_aa=`)
+stay in the block and are compared too. The ledger row's
 `verdict` is the round-79 observation precedence: `predicate` if any `^PREDICATE ... pass`,
 else `vectors` on `^VECTOR `, else `cases` on `^CASE `/`^case=`.
 
```

The probe table itself has no diff. An independent enumeration of block lines against the original frozen regex found no invalid lines for the other five members, and exactly protein lines 13–14 quoted above. Stamp prefix/argv checks returned True/True for all six. The original frozen file was also read in full through `git show af51132d8919cedd14d3d3407ae5abc966d5d427:plans/round-80-claims.md`.

## Population invariant

Command: `python3 plans/round79_c1_population_ledger.py --lane .` in the clone (rc 0). Relevant exact output (the intervening member/class inventory is omitted):

```text
UNIVERSE classes=16 members=88 pairs=230 census_executed=17 census_covered=12
LEDGER rows=88 executed=24 unlocated=0 unexecuted=64
COVERAGE replayed=24 covered=15 covered_located=15 uncovered=container-image census_covered=12
DEFECTS n=0
TARGET classes=16 members=88 pairs=230 replayed=24 located=24 unlocated=0 unexecuted=64 unaccounted=0 unbacked=0 understated=0 covered=15
PREDICATE R79-C1 pass
```

## Claim width, residual risk, gaps

The sentence promising **all six** fresh reproducible receipts is wider than the observed evidence: the eigen replay differs on frozen observation lines even though its older predicate passes. The new tip additionally replaces the frozen block grammar. The four unqualified SUPPORTED flips meet subject/stamp/hash/ledger/reproduction requirements; protein meets the actual replay requirement but not the original frozen observation-form definition. The population invariant is independently green and does not repair either defect. No new certified benchmark task successes are established by synthetic candidates.

One run per instrument, not an estimate of stability or a saturation sample. The eigen source explicitly anticipates host-dependent U outcomes; this is evidence against exact replay determinism, not justification for treating the mismatching fresh run as equal. No C1 gate selftest/mutants/controls were run or imported, and C2 is outside this seat. Historical cleanliness is a recorded stamp, not a reconstructed proof of the minting process; reachability and tracked byte hashes were independently established.

Tools/dependencies: no global tools installed or updated; the frozen uv invocation resolved biopython 1.88 and numpy 2.5.4 into this seat's isolated UV_CACHE_DIR (package-index channel), needed for protein's frozen prefix. Exact uv stderr is above. No PATH directory or host package manager was touched.

## Independent extractor (executed source)

Retained here because scratch is removed before handoff. It does not import either round-80 counter. Its raw `grade` field deliberately covers subject/stamp/ledger/replay checks; the final table additionally applies the original frozen observation grammar, as explained above.

```python
import concurrent.futures
import hashlib
import json
import os
import pathlib
import re
import shlex
import subprocess

S = pathlib.Path(__file__).parent
D = S / 'lane'
BASE = 'dce7c275381c669e6489f1b795b1505d0824c262'

def git(*args):
    return subprocess.check_output(['git', '-C', str(D), *args], text=True)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def normalize(text):
    return ''.join(line for line in text.splitlines(keepends=True) if not line.startswith('REV '))

base = json.loads(git('show', BASE + ':plans/grader-population-ledger.json'))
current = json.loads((D / 'plans/grader-population-ledger.json').read_text())
targets = sorted(m for m, row in base['members'].items() if row['status'] == 'executed-unlocated')
probes = json.loads((D / 'plans/round80_probes.json').read_text())['members']
tracked = set(git('ls-files').splitlines())
print('BASE', BASE, 'TIP', git('rev-parse', 'HEAD').strip(), flush=True)
print('DERIVED_TARGETS', json.dumps(targets), flush=True)
print('TIP_UNLOCATED', json.dumps(sorted(m for m,r in current['members'].items() if r['status'] == 'executed-unlocated')), flush=True)

def review(m):
    p = probes[m]
    row = current['members'][m]
    path = row['receipt']
    receipt = (D / path).read_text()
    lines = receipt.splitlines()
    start = lines.index('OBSERVATIONS_BEGIN')
    end = lines.index('OBSERVATIONS_END')
    observation = ''.join(receipt.splitlines(keepends=True)[start + 1:end])
    stamp = dict(line.split(' ', 1) for line in lines[1:start] if ' ' in line)
    work = S / (m + '.work')
    work.mkdir(exist_ok=True)
    argv = [a.replace('{work}', str(work)).replace('{out}', str(S / (m + '.out'))) for a in p['argv']]
    command = p.get('prefix', ['python3']) + [p['tool']] + argv
    env = dict(os.environ, TMPDIR=str(S), PYTHONDONTWRITEBYTECODE='1', UV_CACHE_DIR=str(S / 'uv-cache'), UV_PYTHON_DOWNLOADS='never')
    proc = subprocess.run(command, cwd=D, env=env, capture_output=True, text=True, timeout=p['timeout'])
    fresh = normalize(proc.stdout)
    expected = normalize(observation)
    source_sha = sha((D / p['historical']).read_bytes())
    tool_sha = sha((D / p['tool']).read_bytes())
    form = 'predicate' if re.search(r'^PREDICATE R\d+-C\d+ pass$', observation, re.M) else 'vectors' if re.search(r'^VECTOR ', observation,re.M) else 'cases' if re.search(r'^(CASE |case=)', observation,re.M) else 'none'
    history = (D / p['historical']).read_text()
    obs_re = re.compile(r'^(?:CASE |case=|cases=|MISMATCH |OBSERVED-U |VECTOR |PREDICATE R\d+-C\d+ (?:pass|fail))')
    old_lines = [l for l in history.splitlines() if obs_re.match(l)]
    new_lines = [l for l in observation.splitlines() if obs_re.match(l)]
    divergence = old_lines != new_lines
    ancestor = subprocess.run(['git','-C',str(D),'merge-base','--is-ancestor',stamp.get('LANE_TIP','missing'),'HEAD'],capture_output=True,text=True)
    checks = {
        'tracked': path in tracked,
        'subject': bool(re.fullmatch(r'# tb2 '+re.escape(m)+r' grader probe(?: \(round 80 re-mint\))?',lines[0])),
        'member': stamp.get('MEMBER') == m,
        'source': stamp.get('SOURCE_RECEIPT') == p['historical'],
        'source_sha': stamp.get('SOURCE_SHA') == source_sha,
        'tool': stamp.get('TOOL') == p['tool'],
        'tool_sha': stamp.get('TOOL_SHA') == tool_sha,
        'reachable': ancestor.returncode == 0,
        'worktree_stamp': stamp.get('WORKTREE') == 'clean',
        'exit_stamp': stamp.get('EXIT') == '0',
        'command': p['tool'] in shlex.split(stamp.get('COMMAND','')),
        'nonempty': bool(observation),
        'reproduction': fresh == expected,
        'exit': proc.returncode == 0,
        'ledger': row['status'] == 'executed' and row.get('subject') == 'tb2-header' and row['round'] == 80 and row.get('verdict') == form,
        'divergence_noted': not divergence or any(l.startswith('HISTORICAL-DIVERGENCE ') for l in lines),
    }
    return {'member':m,'grade':'SUPPORTED' if all(checks.values()) else 'UNSUPPORTED','receipt':path,'receipt_sha':sha(receipt.encode()),'source_sha':source_sha,'tool_sha':tool_sha,'first_line':lines[0],'stamp':stamp,'row':row,'checks':checks,'observation_sha':sha(expected.encode()),'fresh_sha':sha(fresh.encode()),'historical_divergence':divergence,'command':shlex.join(command),'returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'observations':observation,'numbered_receipt':'\n'.join(f'{i}: {l}' for i,l in enumerate(lines,1))}

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    results = list(pool.map(review, targets))
(S / 'results.json').write_text(json.dumps(results,indent=2))
for r in results:
    print(json.dumps(r,sort_keys=True),flush=True)
```

## Self-evaluation

Accuracy 4/5: commands, fresh stdout and differing hashes retained; historical mint cleanliness remains stamp-only. Completeness 4/5: all six flips and the population invariant covered; temporal stability not sampled. Clarity 4/5: separates execution, exact reproduction and frozen grammar, at the cost of a long evidence appendix. Actionability 4/5: exact failing paths/lines identified; reviewer cannot authorize a frozen-contract revision. Conciseness 4/5: full stdout/source retained intentionally for reproducibility. Overall 4.0/5. Highest-impact next decision belongs to Main: treat the failing frozen target as an honest stop rather than admit through the changed grammar. Would the user agree? The report preserves the observed failure without reducing the six-member scope.
