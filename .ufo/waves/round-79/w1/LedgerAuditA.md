# LedgerAuditA — R79 w1 independent population-row audit

## Scope and result

Axes: coverage and calibration. Audited the explicit alphabetical endpoints `adaptive-rejection-sampler` through `fix-git`, inclusive: **30 rows**, not 29. All **30 OK**, no WRONG rows. Status split: 7 executed, 3 executed-unlocated, 20 unexecuted (18 unattempted and 2 browser-required). All class lists equal independently derived census memberships, including duplicate-sensitive list comparison.

Frozen claims were read in full. Observed `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse master` = `5d6843134017780c045e92eed4e83264188a7d47`. Every audited ledger/census/grader/receipt/instrument byte was subsequently fetched using `git show 5d6843134017780c045e92eed4e83264188a7d47:<path>`; therefore this report describes that committed snapshot, not possible later changes. Independently parsed census: classes=16, members=88, pairs=230; every declared class count equaled its CSV membership length. Counter was neither imported nor executed.

## Row verdicts and retained evidence

For each row, `classes=` is the census-derived class list and was compared with the ledger. For unattempted rows, detectors=0 means all four frozen detector regexes were silent over that member’s committed `tests/test_outputs.py`; the displayed 16-hex SHA-256 prefix matched the ledger. Browser evidence is a whitespace-collapsed context window, not a literal physical source line; its entire text occurs in the whitespace-normalized grader body, and it includes the actual matched `selenium` token.

| Row | Verdict | Independently observed evidence |
|---|---|---|
| adaptive-rejection-sampler | OK | classes=file-artifact,numeric-band,stdout-inspection,subprocess-exec; unattempted; detectors=0; sha256=547dc6e107f034f4 |
| bn-fit-modify | OK | classes=file-artifact; unattempted; detectors=0; sha256=364069f893e336a0 |
| break-filter-js-from-html | OK | classes=file-artifact,subprocess-exec; browser-required; matched='selenium'; line=7; evidence='ys import tempfile from pathlib import Path from selenium import webdriver from selenium.common.exceptions' |
| build-cython-ext | OK | classes=file-artifact,git-plumbing,numeric-band,subprocess-exec; unattempted; detectors=0; sha256=6549f1a8e04b6163 |
| build-pmars | OK | classes=file-artifact,subprocess-exec; executed; subject=['tb2-header']; verdict=cases; named=['build-pmars']; receipt=corpus/evidence/round38/build-pmars-probe.txt |
| build-pov-ray | OK | classes=crypto-credential,file-artifact,stdout-inspection,subprocess-exec; unattempted; detectors=0; sha256=64d6ce107503714a |
| caffe-cifar-10 | OK | classes=file-artifact,filesystem-metadata,stdout-inspection,subprocess-exec; unattempted; detectors=0; sha256=10bc2d83f1a42180 |
| cancel-async-tasks | OK | classes=file-artifact,signal-delivery,stdout-inspection,subprocess-exec,timing-wall; unlocated; instrument line2='"""Offline probe of the pinned Terminal-Bench 2.0 `cancel-async-tasks` grader (round 61, C1).'; verdict=predicate; subjects=[]; receipt named=[]; receipt=corpus/evidence/round61/cancel-async-probe.txt |
| chess-best-move | OK | classes=file-artifact; unlocated; instrument line2='"""Offline probe of the pinned Terminal-Bench 2.0 `chess-best-move` grader (round 55, C3).'; verdict=predicate; subjects=[]; receipt named=[]; receipt=corpus/evidence/round55/chess-best-move-probe.txt |
| circuit-fibsqrt | OK | classes=file-artifact,stdout-inspection,subprocess-exec; executed; subject=['tb2-header']; verdict=cases; named=['circuit-fibsqrt']; receipt=corpus/evidence/round42/fibsqrt-probe.txt |
| cobol-modernization | OK | classes=file-artifact,subprocess-exec; unattempted; detectors=0; sha256=009180a7092583fc |
| code-from-image | OK | classes=file-artifact; unattempted; detectors=0; sha256=b9b7cb0033116df8 |
| compile-compcert | OK | classes=file-artifact,filesystem-metadata,stdout-inspection,subprocess-exec; unattempted; detectors=0; sha256=f4cf5200a8011eef |
| configure-git-webserver | OK | classes=stdout-inspection,subprocess-exec; executed; subject=['tb2-header']; verdict=cases; named=['configure-git-webserver']; receipt=corpus/evidence/round37/git-webserver-probe.txt |
| constraints-scheduling | OK | classes=crypto-credential,file-artifact; executed; subject=['tb2-header']; verdict=cases; named=['constraints-scheduling']; receipt=corpus/evidence/round41/constraints-probe.txt |
| count-dataset-tokens | OK | classes=file-artifact; unattempted; detectors=0; sha256=5c11065dc97e9266 |
| crack-7z-hash | OK | classes=file-artifact; unattempted; detectors=0; sha256=f18d7565f6907274 |
| custom-memory-heap-crash | OK | classes=crypto-credential,file-artifact,stdout-inspection,subprocess-exec; unattempted; detectors=0; sha256=4e1cb33f777fa7fb |
| db-wal-recovery | OK | classes=file-artifact,serialization-schema; executed; subject=['tb2-header']; verdict=cases; named=['db-wal-recovery']; receipt=corpus/evidence/round40/db-wal-probe.txt |
| distribution-search | OK | classes=numeric-band; unlocated; instrument line2='"""Offline probe of the pinned Terminal-Bench 2.0 `distribution-search` grader (round 58, C3).'; verdict=predicate; subjects=[]; receipt named=[]; receipt=corpus/evidence/round58/kl-probe.txt |
| dna-assembly | OK | classes=file-artifact,numeric-band,stdout-inspection,subprocess-exec; unattempted; detectors=0; sha256=5c2d0fd2e5f63032 |
| dna-insert | OK | classes=file-artifact,numeric-band,stdout-inspection,subprocess-exec; unattempted; detectors=0; sha256=5bf0651b48969968 |
| extract-elf | OK | classes=file-artifact,serialization-schema,subprocess-exec; unattempted; detectors=0; sha256=825569115217f1ce |
| extract-moves-from-video | OK | classes=file-artifact; unattempted; detectors=0; sha256=565a7617602f33c0 |
| feal-differential-cryptanalysis | OK | classes=candidate-import,shell-exec; executed; subject=['tb2-header']; verdict=cases; named=['feal-differential-cryptanalysis']; receipt=corpus/evidence/round43/feal-probe.txt |
| feal-linear-cryptanalysis | OK | classes=file-artifact; executed; subject=['tb2-header']; verdict=cases; named=['feal-linear-cryptanalysis']; receipt=corpus/evidence/round44/feal-linear-probe.txt |
| filter-js-from-html | OK | classes=file-artifact,network-service,subprocess-exec; browser-required; matched='selenium'; line=12; evidence='b import Path from bs4 import BeautifulSoup from selenium import webdriver from selenium.common.exceptions' |
| financial-document-processor | OK | classes=crypto-credential,file-artifact; unattempted; detectors=0; sha256=978f506ad5c1bfaf |
| fix-code-vulnerability | OK | classes=file-artifact,serialization-schema; unattempted; detectors=0; sha256=c006a5de95b69bd7 |
| fix-git | OK | classes=crypto-credential,file-artifact; unattempted; detectors=0; sha256=a8a6f51eb0d7c4eb |

All ten named receipts and all three instruments returned `TRACKED` from `git ls-files --error-unmatch`. Successful `git show <freeze>:<path>` additionally established their existence in the frozen tree. Each of the seven executed receipts has its exact own-member `# tb2 <member> grader probe` header at line 1; no predicate/vector observation takes precedence over its CASE observations; each names exactly one of the 88 population members under whole-name boundaries `(?<![\w.-])<member>(?![\w.-])`. Thus none is a population artifact. The three unlocated receipts have execution observations, none of the five frozen subject shapes, the required round directory and debt, and a tracked instrument whose second line names the correct member and round.

## Receipt byte identities and concrete observation locations

| Member | Receipt SHA-256 | First CASE location and text |
|---|---|---|
| build-pmars | `2408b477b0299e1339064b4b3df968a00174b3a5999016073b5fe4fd8cbb4ef9` | 4: CASE empty-tree predicted=fail observed=fail tests=FFFF predicted_tests=FFFF match=yes violates=from-source,no-x11,debian-source,extract-to-app,install-path,results-format,debugger-works test_headless_no_x11:error=CalledProcessError -- do-nothing: no binary, empty /app |
| cancel-async-tasks | `3a69fddb8ab817bf78dad57b4d28e1c964b288c433901560fa98f59ff306922a` | 2: CASE compliant-signal-handler predicted=P/P/P/P/P/P observed=P/P/P/P/P/P ok |
| chess-best-move | `de0826692f8b81c832b8d0633cfe8fa080f2d6142ee9d71b597eba6be9d8aaca` | 1: CASE both-lowercase-two-lines predicted=P observed=P rc=0 |
| circuit-fibsqrt | `2a54ca8a76619a173280727938441fcf129ddcd482cc0a4d55f65b38d41ad92a` | 7: CASE nop predicted=fail observed=fail tests=PPF predicted_tests=PPF match=yes regrade=same violates=output-function,example-208,example-20000 -- the shipped example circuit (prints N/2) left in place |
| configure-git-webserver | `835507129cb536ff6c927b5b05650dd4712891bd3ec218948659655597ec29f8` | 5: CASE no-server tools=curl predicted=fail observed=fail match=yes -- verify.sh:57-59 — nothing listens on :8080, curl reports 000, the 200 branch is skipped |
| constraints-scheduling | `c5aa674277f9b9473de4c0884629c577f2b6467d8b73c3a90eec33b24b7701da` | 7: CASE nop predicted=fail observed=fail tests=FFF predicted_tests=FFF match=yes regrade=same violates=output-file test_structure_event_title_attendees_duration_window:error=FileNotFoundError,test_constraints_conflicts_business_hours:error=FileNotFoundError,test_earliest_tiebreakers_and_carol_buffer:error=FileNotFoundError -- no output file: all three tests read it (pilot) |
| db-wal-recovery | `c74c6b91c8c49b1788f2dd7aa0d66edce0db0b52b549baf89ce69cfa8e2a730e` | 6: CASE empty-app predicted=fail observed=fail tests=FFFFFFF predicted_tests=FFFFFFF match=yes regrade=same violates=extract-all,json-at-path,eleven-records test_recovered_json_is_valid:error=FileNotFoundError,test_recovered_data_structure:error=FileNotFoundError,test_recovered_data_sorted:error=FileNotFoundError,test_recovered_data_completeness:error=FileNotFoundError,test_no_duplicate_ids:error=FileNotFoundError,test_wal_was_decrypted:error=FileNotFoundError -- do-nothing on an empty /app: no database, no recovered.json |
| distribution-search | `3c93e06a88a6ec8e77b0ed1b81ad298a492513e3f5e7c9f20d6641da5ee53c1f` | 2: CASE sol predicted=P/P/P/P observed=P/P/P/P ok |
| feal-differential-cryptanalysis | `8c987463d6c9b4dd7c7478beedbefef20e6a7996ec59d1620167d66ae4e637b4` | 10: CASE nop predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same violates=attack-file,recover-key5 error=ModuleNotFoundError -- no /app/attack.py (the shipped feal.py only) |
| feal-linear-cryptanalysis | `40308211216be063084eb9a1f22faded5a8550d392a83f6e13545e2ddae205a0` | 9: CASE nop predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same violates=decrypt-all,plaintexts-file,known-plaintext-attack,recover-key error=FileNotFoundError -- no /app/plaintexts.txt (the image state only) |

## Reproduction and strongest attack candidate

No WRONG rows, so no WRONG-row reproduction commands are applicable. Byte retrieval template (read-only):

```sh
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 5d6843134017780c045e92eed4e83264188a7d47:plans/grader-population-ledger.json
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 5d6843134017780c045e92eed4e83264188a7d47:corpus/evidence/round62/class-survey.txt
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 5d6843134017780c045e92eed4e83264188a7d47:corpus/evidence/round52/graders/adaptive-rejection-sampler/tests/test_outputs.py | sha256sum
```

First attack candidate: **adaptive-rejection-sampler**. Its actual row is OK: all four detectors silent; actual prefix `547dc6e107f034f4`. The counter source at `plans/round79_c1_population_ledger.py:288-295` only checks whether unattempted evidence starts with `no-blocker:`; it does not validate the displayed digest. [INFERENCE] Changing only this row’s claimed digest should escape that counter’s evidence checks. This is an unexercised counter-hardening attack, not a demonstrated ledger defect, and does not reopen the frozen claim. No mutation fixture or counter run was performed.

Frozen blocker regexes applied independently (all four for every unexecuted row):

```text
browser-required: selenium|webdriver\.(?:Chrome|Firefox)|chromedriver
vm-required: qemu-system|qemu-img|/app/isos/|win311
external-db-required: GOLDEN_SQL_PATH|/tests/golden\.sql|DB_PATH\s*=\s*Path\(
candidate-library-required: sys\.path\.append\(\s*[\"\x27]/app
```

## Boundaries, risks, cleanup

Only this advisory report is written in the lane. No implementation files changed, no tools installed, no build/lint/test/formatter or committed counter executed, no git mutations, no external state changed. No supported symbol refactor was needed; no LSP tool was exposed in this seat. The first scratch mkdir failed because an unset environment variable expanded to a root-relative path; a subsequent explicit-default creation succeeded and its EXIT trap removed the empty owned directory. No scratch files remain. No blocker prevents completion. Scope is this 30-row snapshot only; no inference of other rows’ correctness or of end-to-end runtime replay authenticity.

Self-evaluation: accuracy 4 (committed-byte checks, but no runtime replay authenticity audit); completeness 5 (all 30 endpoint-inclusive rows, including unlocated details); clarity 4 (full evidence table is dense); actionability 4 (specific unexercised hash-check attack identified); conciseness 4 (receipt identities add length). Overall 4.2/5. Highest-impact improvement would be exercising the digest-only mutant in a separately authorized fixture; this report intentionally distinguishes inference from measured findings. User-agreement self-check: the requested independent row audit is complete without treating a hypothetical counter bypass as a WRONG row.
