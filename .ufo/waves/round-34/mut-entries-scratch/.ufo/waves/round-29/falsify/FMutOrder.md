writer: KengakuR29-2.FMutOrder-2

# FMutOrder — mapping-order replacement mutant

## Scope and axes

Round 29 only. Axes: behavioral detector discrimination; source-order fidelity; frozen-population coverage; isolated execution and exact-byte restoration. This is one mutation probe, not a round-admission judgment or an independent oracle.

Production source was read, including `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py:140-147,385-548`. Only the isolated copy was mutated. No production, fixture, corpus, index, Git/JJ state, or sibling source was edited. No delegation, other agent runtime, network request, package transaction, linter, or formatter was invoked. No tools were installed or updated; the existing `/usr/bin/python3` reported version 3.14.8.

## Attack and expected detector

The pinned generator `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/generate_test_data.py:11-16` applies GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP in that order. The preregistration requires exact sequential order and a later-token-cascade hand case at `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-29-claims.md:35-45,73-77`.

Created an isolated tree with these commands:

```sh
mktemp -d /tmp/KengakuR29-2.FMutOrder-2.XXXXXX
cp -a /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans /tmp/KengakuR29-2.FMutOrder-2.WuoW6r/plans
```

The first command returned `/tmp/KengakuR29-2.FMutOrder-2.WuoW6r`; the copy command exited 0. A pristine byte backup was also retained at `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutOrder-2/pristine.config_projection.py`.

The only source change was at `/tmp/KengakuR29-2.FMutOrder-2.WuoW6r/plans/config_projection.py:143`, inside `project()`:

```diff
-    for name in ORDER:
+    for name in values:
```

This plausible defect substitutes caller mapping insertion order for generator order. It is the requested mapping-order alternative, not a claim to have rerun the author's reverse-ORDER mutant. The reference `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round29-calibration/mutation-witness.txt:1-5` was read as an untrusted prior receipt; all results below were independently exercised.

Expected detector: `--selftest` must reject the reverse-insertion cascade fixture while pristine/restored controls pass. The hand fixture at `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/hand/cascade-order.case.json:6-16` inserts mapping keys in the reverse of source order and makes each replacement value carry the next source token.

## Reused bounded detector and actual outputs

The unchanged driver is `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutOrder-2/detector.py`. It ran the following exact commands in each byte state, concurrently, each with a 60-second subprocess timeout:

```sh
/usr/bin/python3 /tmp/KengakuR29-2.FMutOrder-2.WuoW6r/plans/config_projection.py --selftest --root /tmp/KengakuR29-2.FMutOrder-2.WuoW6r
/usr/bin/python3 /tmp/KengakuR29-2.FMutOrder-2.WuoW6r/plans/config_projection.py --summary --root /tmp/KengakuR29-2.FMutOrder-2.WuoW6r
/usr/bin/python3 /tmp/KengakuR29-2.FMutOrder-2.WuoW6r/plans/config_projection.py --json --root /tmp/KengakuR29-2.FMutOrder-2.WuoW6r
```

The three driver invocations were:

```sh
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutOrder-2/detector.py pristine
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutOrder-2/detector.py mutated
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutOrder-2/detector.py restored
```

All driver invocations exited 0; detector exit codes are recorded separately below. No subprocess timed out.

| Byte state | `--selftest` exit | Selftest stdout / stderr | `--summary` exit | `--json` exit |
|---|---:|---|---:|---:|
| pristine | 0 | 20 completed cases; 599 / 0 bytes | 0 | 0 |
| mutated | 1 | empty stdout; 0 / 762 bytes | 0 | 0 |
| restored | 0 | 20 completed cases; 599 / 0 bytes | 0 | 0 |

Each summary ended with `TOTAL findings=0 exit=0`. Each summary stdout was 6,914 bytes; each JSON stdout was 3,881,050 bytes. Summary/JSON stderr was empty in every state. JSON reported 812 input tasks, 3 profiles, 2,436 task/profile projections and an empty findings array in every state.

Mutated selftest traceback: `/tmp/KengakuR29-2.FMutOrder-2.WuoW6r/plans/config_projection.py:548` → `:533` → `selftest():438`, ending with `AssertionError`. The exact failing assertion at line 438 is:

```python
assert text == order_case["expected_projected_text"] and [s["applied_replacements"] for s in steps] == order_case["expected_dynamic_replacement_hits_by_source_step"]
```

Its first comparison fails. The second operand is short-circuited in that assertion; the unchanged driver's separate direct call to the isolated `project()` records the differing hit vector as diagnostic evidence, not as a second executed assertion.

## Exact hand-probe mismatches

Locations below refer to `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/hand/cascade-order.case.json` and the byte-identical copied fixture. Diagnostic outputs are retained in the mutated receipt's `hand_probe` object. Pristine and restored hand probes had no mismatches.

| Location / compared field | Expected | Mutated actual |
|---|---|---|
| fixture line 25; `project()` return `text`; selftest line 438 | `[{"task_id":0,"start_url":"https://map.invalid/order/probe"}]\n` | `[{"task_id":0,"start_url":"__REDDIT__/probe"}]\n` |
| fixture line 30; returned `steps[*].applied_replacements`, in execution order | `[1,1,1,1,1,1]` | `[0,0,0,0,0,1]` |
| fixture line 6; returned `steps[*].name` | `[GITLAB,REDDIT,SHOPPING,SHOPPING_ADMIN,WIKIPEDIA,MAP]` | `[MAP,WIKIPEDIA,SHOPPING_ADMIN,SHOPPING,REDDIT,GITLAB]` |
| fixture line 26; parsed projected-task JSON pointer `/0/start_url` | `https://map.invalid/order/probe` | `__REDDIT__/probe` |
| fixture line 29; remaining known-token occurrences in projected serialized text | 0 occurrences | 1 occurrence, `__REDDIT__` |

The displayed `\n` is the one terminal newline character in each serialized text, not two literal output characters. In name-aligned replacement counts, GITLAB remained 1 occurrence replaced; REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA and MAP each changed from 1 expected replacement to 0 actual replacements. The mutant's final text also exactly matches the fixture's prior mapping-order prediction at line 33, now observed rather than assumed.

## Does frozen real data alone detect it?

**No, for this tested mutant and the frozen three-profile population.** Both the summary and the complete JSON outputs were byte-for-byte identical across pristine, mutated and restored runs, confirmed with `cmp --silent` (exit 0 for each comparison). Their shared stdout SHA-256 values were:

- summary: `5ce5cb0f91ad279d446a475de757b9aa4a5b67a4b02df8d9aeac0d01be74636f`;
- JSON: `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`.

Thus this is not merely agreement on totals: the full reported per-task projections and provenance also agree in that frozen domain. The frozen value mappings at `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/profiles.json:4-10,15-21,26-32` already use the generator order. [INFERENCE] That input construction masks the mapping-order defect; the independent reverse-insertion cascade fixture provides the discrimination. The summary-only detector survived this mutant; the instrument's selftest killed it. This is a coverage boundary, not permission to alter C1 or to claim exhaustive mutation coverage. No result is asserted for an unexecuted reversed-loop mutant.

## Restoration and retained evidence

The edit at copied line 143 was reversed immediately after the mutated run. Source SHA-256:

| State | `/tmp/KengakuR29-2.FMutOrder-2.WuoW6r/plans/config_projection.py` |
|---|---|
| pristine | `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3` |
| mutated | `df6edbf6efedacbbb2234ffd4c093ee5d1e0fa46c09001f0b8c4403830b0728b` |
| restored | `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3` |

`cmp --silent` between the retained pristine byte backup and the restored copied source exited 0 and produced the explicit recorded result `restored_source_exact_bytes=true` through its success-print command. The restored selftest stdout hash also returned to its pristine value `1fa3c1fcb6d6b3f7b2a83097b8473343bf278fb20b88c1fcfa99161878058d44`.

All tracked lane hashes stayed equal across the three receipts, including the instrument, manifest, generator, raw data, profiles and hand fixtures. All copied input hashes stayed equal to their lane counterparts. In particular:

- manifest: `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87`;
- generator: `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd`;
- raw data: `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`;
- profiles: `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018`;
- cascade hand case: `4f957db3c3a8c19e951b6b225e9520cfc631fc09f864c9b4aad72464d9639fb3`.

Complete commands, exits, timings in seconds, byte counts, stdout/stderr digests, input/source hashes and hand operands are retained at:

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutOrder-2/pristine/receipt.json`;
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutOrder-2/mutated/receipt.json`;
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutOrder-2/restored/receipt.json`.

Each receipt directory also retains `selftest.stdout.txt`, `selftest.stderr.txt`, `summary.stdout.txt`, `summary.stderr.txt`, `json.stdout.txt`, and `json.stderr.txt` from that state. The detector and pristine backup are retained as reproduction evidence, not production changes.

Quoted source/terminal excerpts were counted programmatically with Python `len(text.split())`: loop lines 4 and 4 words; failing assertion 12; summary final line 3; exception name 1. Each excerpt is below 25 words; these excerpts total 24 words. Structured expected/actual values above are data, not prose quotations.

**Scoped result: KILLED by the hand-cascade selftest; SURVIVED the frozen-real-data summary/JSON detector; exact source bytes restored and passing controls recovered.**

VERDICT: PASS
