# Round 29 — compressed source-copy containment

Author: hyaku orchestrator, integrating an isolated containment edit and independent metadata check.
Round/report: `.ufo/reports/round-29/kengaku.md` in the fleet repo, including its appended containment erratum.
Baseline: `6a2c2df788a4fdb216dd5790f9ae6dd326169f47` (tree `31ea39445f661097f3a4727586b7f8037a5a69d9`).

## Finding and authority

The earlier `FSentinelSecrets` follow-up established absence of five named loose scratch paths. It did
not establish absence of every carrier of their contents. An independent non-author archive check found
that the baseline still contains a compressed, byte-identical copy of the flagged module in an unrelated
fetched wheel. The retained scan receipts document path-scoped checks; no global-clean conclusion follows.
The five-path cleanup happened before the lane's author-side knowledge admission, not an outside round
admission.

| Item | Opaque identity |
|---|---|
| Copied archive | `.ufo/waves/round-29/scratch/falsify/FCritNovelty/fetch/libwebarena-0.0.5-py3-none-any.whl` |
| Archive Git blob | `9d4333f8419d912e78edf9556de7871aeab9e1aa` |
| Archive SHA-256 | `5cfdf8abc2b40cc4442905a29af1c45c5fd0ed57bbfe8e3a6421a2e53cb6cb1b` |
| Archive extent | 116645 bytes; 29 members |
| Flagged member | `webarena/browser_env/env_config.py` |
| Member Git blob | `81cf52de7d998c90abb3741416e2c8ab9b434758` |
| Member SHA-256 | `fcec91a2dafd5db16bb390ac5a6fd930ef59c6ef54445b85f7625d8f9404abd7` |
| Matching removed loose source | `.ufo/waves/round-29/scratch/falsify/FRevEnumerate/src/browser_env/env_config.py` at `dbcecded4a04247cf6fd12919327af973da10bdd` |
| Additional login-code member | `webarena/browser_env/auto_login.py`, blob `871e1e91aa3307e8183c527b82f141940f0715d7` |

These are member names, lengths and cryptographic identities only. No credential value, account
identifier or private endpoint is reproduced. The published benchmark defaults were not tested for
validity. No package was imported or executed, and no benchmark/service endpoint was contacted.

## Containment and reproduction bounds

The change removes only the known copied wheel from the current tree. Parent integration required an
exact regular-file/size/SHA-256 check and stable inode metadata before the single-file removal. The
isolated edit used branch `hyaku/s3-kengaku-containment` at the baseline above; it neither committed nor
pushed. The parent publishes the bounded removal and this record through the lane helper; the fleet
report erratum records the resulting landed hash.

The independent metadata check found no production instrument, grader, gate, plan or fixture depending
on that wheel path. Its references are fetched-source receipts and falsifier prose. `fetch-manifest.txt`
is retained as a fetch receipt, not a claim that the artifact remains present. Historical references to
the original artifact still resolve at the baseline commit; this does not endorse retaining its material.

No unique projection input is removed: the archive's task-raw member matches the retained canonical
`plans/fixtures/r28/webarena/config_files/test.raw.json`, SHA-256
`7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`. No instrument, fixture, expected
verdict or original measured result is changed or re-credited by this containment action. No lane gate,
selftest, mutant or oracle was rerun.

## Gate and mistakes

| Candidate or mistake | Evidence | Decision / prevention |
|---|---|---|
| Treat five absent loose paths as all material absent | Baseline archive and matching member blob above | Rejected: distinguish path scope from archive/member scope and name all inspection limits. |
| Keep the unrelated fetched wheel in the current corpus | No active production dependency; flagged module is still present in the package | Rejected: remove the known carrier, retain only sanitized metadata and accurate historical references. |
| Treat tip containment as historical purge or credential remediation | Introducing commit remains reachable from the advertised master baseline | Rejected: keep the operator history-disposition hold; never claim rotation, revocation or global absence. |

The lessons index includes this record. LOG.md and the filed round report receive appended corrections;
old claims and evidence are not rewritten.

## Unresolved limits

Git history still retains the wheel and module objects. There was no history rewrite, force-push,
rotation or revocation. This change does not establish absence from other worktrees, caches, sibling
repositories, untracked/ignored files, nested/encrypted containers or unexamined archive formats. Offline
reproduction from the removed wheel path is no longer available at the new tip; the retained public fetch
receipt and immutable baseline identify what was removed without republishing values. No new admission,
closure, score movement, credential-liveness verdict or global-clean claim is made. The existing safety
hold and operator history-disposition question remain in force.
