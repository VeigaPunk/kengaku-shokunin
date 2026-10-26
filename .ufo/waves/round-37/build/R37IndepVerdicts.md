# R37IndepVerdicts — independent re-run of the TB2 `configure-git-webserver` receipt (round 37, C2)

Seat: `R37IndepVerdicts` (executor, wave 1). Scope: falsify or confirm
`corpus/evidence/round37/git-webserver-probe.txt` (22 cases) with a *different* isolation from the
probe's bubblewrap, and add 3 predicted extra cases. No lane file other than this report directory
was written; no commit, no gate/counter/probe change.

## What ran

Artifacts (all under this seat's build subdir):

- `indep.py` — runner; parses the case table from the frozen
  `corpus/evidence/round37/git-webserver-dry-cases-freeze.txt` (`sha256=0095e591…b66f3`, 22 CASE
  lines), pins and checks both captures, runs each case, applies `test_outputs.py:13`'s rule.
- `extras-predictions.txt` — the three extra predictions, written **before** the first run.
- `indep-receipt.txt` (run 1) and `indep-receipt-run2.txt` (run 2, `--keep`) — receipts.
- `indep-receipt-run2.txt` is byte-equal to run 1 (`cmp -s … && echo BYTE-EQUAL` → `RUN2 BYTE-EQUAL to run1`).

Command (both runs):

```
python3 .ufo/waves/round-37/build/R37IndepVerdicts/indep.py \
  --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin \
  --work /fast/scratch/hyaku/kengaku-r37/R37IndepVerdicts/work \
  --receipt …/R37IndepVerdicts/indep-receipt.txt
```

Output tail: `cases=22 agree_receipt=22 disagree_receipt=0 predicted_match=22` /
`extras=3 extra_matched=3` / `INDEP agree=22/22 extra=3/3`.

Capture digests verified before any case: `verify.sh`
`1dc44c923b797ed24ca423c9b9efcd9c1eed4d7261007139b0a724f4e2f53d05`,
`test_outputs.py` `526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37`.

## Isolation (not the probe's)

Per case: `unshare --user --map-root-user --net --fork`, then `ip link set lo up` inside the fresh
net namespace — so `:8080` is a private loopback and two cases can never see each other; no server
outside the namespace can answer. `HOME`, cwd and `TMPDIR` are per-case directories under scratch;
`PATH` contains only `bash sleep chmod mkdir cat` plus `curl` (or `wget` for the wget cases).
`apt-get` and `expect` are absent from PATH (host has no `/usr/bin/expect`:
`ls: cannot access '/usr/bin/expect': No such file or directory`), and the wget cases' bin dir
listing is `bash cat chmod mkdir sleep wget` — no `curl`. Server behaviour comes from the frozen
JSON of each freeze line, served by an inline `http.server` written for this run (files / catch-all /
sequence / head-200-get-404 modes). The verdict is `"TEST PASSED" in stdout`
(`test_outputs.py:13`) applied to `bash verify.sh`'s captured stdout.

Isolation evidence: the operator's `~/.ssh/config` had `mtime=2026-10-11 10:33:49`,
`sha256=eb75d8b0…9f77` before and after both runs (unchanged), while the per-case HOME received
verify.sh's config (`Host localhost / StrictHostKeyChecking no / UserKnownHostsFile=/dev/null`);
`git_test.exp` was written in the per-case cwd, not the lane.

## Per-case comparison (22/22 agree)

| case | tools | receipt | indep | match |
|---|---|---|---|---|
| no-server | curl | fail | fail | yes |
| static-file-no-git | curl | pass | pass | yes |
| exact-no-newline | curl | pass | pass | yes |
| trailing-newlines | curl | pass | pass | yes |
| capitalised | curl | fail | fail | yes |
| leading-space | curl | fail | fail | yes |
| trailing-space | curl | fail | fail | yes |
| crlf | curl | fail | fail | yes |
| bom | curl | fail | fail | yes |
| empty-200 | curl | fail | fail | yes |
| not-found | curl | fail | fail | yes |
| http-500-right-body | curl | fail | fail | yes |
| redirect-301 | curl | fail | fail | yes |
| catch-all-200 | curl | pass | pass | yes |
| wrong-port-8081 | curl | fail | fail | yes |
| token-in-body | curl | pass | pass | yes |
| status-then-content-split | curl | pass | pass | yes |
| first-request-404 | curl | fail | fail | yes |
| slow-server-3s | curl | pass | pass | yes |
| wget-static-file | wget | pass | pass | yes |
| wget-404 | wget | fail | fail | yes |
| wget-token-in-body | wget | pass | pass | yes |

Beyond the verdicts, the **full per-case grader stdout is byte-identical to the receipt in all 22
cases** (read-only Python parse of both receipts, comparing the quoted `grader-stdout:` blocks:
`cases 22 stdout_identical 22 differing []`). `verify.sh` exited 0 in all
22 (its trailing `echo "Test completed"` decides its status; the rule never reads it).

Spot anchors reproduced in my run, same as receipt: `no-server` prints
`❌ TEST FAILED: Web server returned HTTP 000`; `token-in-body` prints
`Content: TEST PASSED` **and** `❌ TEST FAILED: Content does not match expected output`, yet passes
the substring rule; `crlf` shows `Got: 'hello world` followed by a lone `'` line (the `\r` breaks
the echo); `wget-404` prints `❌ TEST FAILED: Web server could not be reached`.

## Extra cases: predictions first, 3/3 matched

Predictions recorded in `extras-predictions.txt` before the run:

| extra case | prediction | observed | evidence |
|---|---|---|---|
| `x-token-line` — body `xx TEST PASSED yy` | pass | pass | stdout `Content: xx TEST PASSED yy`, then `❌ TEST FAILED`; substring rule still matches between other words |
| `x-head200-get404` — 200 for HEAD, 404 for GET | fail | fail | stdout `❌ TEST FAILED: Web server returned HTTP 404`; the status probe is a GET (`verify.sh:57`, no `-I`) |
| `x-gzip-header` — body `hello world`, header `Content-Encoding: gzip` | pass | pass | stdout `Content: hello world` / `✅ TEST PASSED`; curl runs without `--compressed`, so it neither asks for nor decodes gzip |

The third is a blind spot the receipt did not cover: a lying `Content-Encoding` header is invisible
to the grader. The first widens `token-in-body`: the token need not be the whole body.

## Findings

- **No disagreement**: 22/22 verdicts, and 22/22 full stdout blocks, match the receipt. Nothing in
  this run is evidence against the probe.
- The receipt's headline mechanisms are reproduced under an independent sandbox: status-only gate at
  `verify.sh:57-59`, newline-stripping comparison at `:60-63`, two separate requests at `:57,60`,
  body-echo substring verdict at `test_outputs.py:13`, curl-without-`-L`/timeout, wget branch at
  `:73-80`.
- Residual risk, stated not hidden: my namespace has no bwrap `/tests` bind or private `/proc`;
  `verify.sh` is executed from the pinned lane path instead of `/tests/verify.sh` (same bytes,
  pinned digest), and it never references `/tests` itself. Neither run exercises a real git push,
  nginx or sshd, so this confirms what the grader's verdict depends on — not that the intended
  solution passes, exactly the probe's stated limit. User-namespace availability is host-dependent;
  it is enabled here (`/proc/sys/kernel/unprivileged_userns_clone` = 1, `unshare -rn` smoke ok).

No tools were installed; no package manager was run. Scratch
`/fast/scratch/hyaku/kengaku-r37/R37IndepVerdicts` was removed before finishing (receipts copied
into this report's directory first).

VERDICT: indep-agree-22/22-extra-3/3
