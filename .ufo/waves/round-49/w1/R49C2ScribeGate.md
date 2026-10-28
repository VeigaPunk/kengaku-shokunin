# R49C2ScribeGate — round-49 lesson `## Gate` draft (S166 re-open + one lead reject)

Seat: R49C2ScribeGate (scribe), serving R49-C2 (coverage). Item: draft the round-49 lesson Gate block — S166
reopened at the pinned raw URL, plus one reject candidate reopened from `SOURCES.md` `## Leads (unopened)`.
Read-only against the lane: the only lane path written is this report file. No lane corpus file was edited, no
commit/push made, no subagent dispatched.

**Axes named.** coverage (primary — the C2 surface and its sourced basis), discernment (the Gate accept/reject
decisions themselves). Calibration is not touched by this seat.

## 1. Freeze precondition (verified before any measurement)

The stage-1 freeze exists in the committed lane tree and predates this measurement. No scored counter or probe
was run by this seat (the item's ordering rule makes any pre-stage-2 scoring invalid, and the Gate item requires
none), so there is no scored receipt here.

```
$ git log --format='%H %cI %s' -1 9d2900af41e4d1fc6022eff99010436fde6dbd93
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28T09:14:40-03:00 2026-10-28 09:14:40 -0300 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims

$ git merge-base --is-ancestor 9d2900af41e4d1fc6022eff99010436fde6dbd93 HEAD ; echo $?
0                                  # ancestor of HEAD

$ git rev-parse HEAD
af88aab193e6034cb9b386472064e3c18fa90128

$ git log --format='%h %cI %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93..HEAD
af88aab 2026-10-28T09:18:20-03:00 round-49: w1 v2 wave spec + dispatch evidence (64 seats, 40 attack, policy v2 accepted)

$ git diff --stat 9d2900af41e4d1fc6022eff99010436fde6dbd93..HEAD -- plans/ corpus/
                                   # empty: no stage-2 amendment, no corpus edit above the freeze
```

Freeze time 2026-10-28T09:14:40-03:00 is earlier than every fetch in §2/§3 (same day, after the wave spec
commit). Only `plans/round-49-claims.md` exists under the freeze for `plans/` (`git ls-tree -r <freeze> -- plans/`)
— the stage-2 counters and literals are exactly as unfilled as the claims file declares.

## 2. S166 re-open at the pin (admit row)

```
REV 9d2900af41e4d1fc6022eff99010436fde6dbd93      # tree whose committed capture was compared
LANE-HEAD-MEASURED af88aab193e6034cb9b386472064e3c18fa90128

$ curl -sS -o s166_test_outputs.py -w 'HTTP %{http_code} bytes=%{size_download}\n' \
    'https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py'
HTTP 200 bytes=1564

$ sha256sum s166_test_outputs.py
b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec  s166_test_outputs.py

$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show \
    9d2900af41e4d1fc6022eff99010436fde6dbd93:corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py > capture_committed.py
$ sha256sum capture_committed.py
b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec  capture_committed.py
$ cmp s166_test_outputs.py capture_committed.py && echo BYTE-EQUAL
BYTE-EQUAL

$ sed -n '27p' s166_test_outputs.py
    test_cases = [(42, "267914296"), (10, "55"), (0, "0")]
```

Digest matches the sha256 pinned in the seat item, in `corpus/SOURCES.md:181` (row S166) and in
`corpus/evidence/round46/tb2-polyglot-c-py/SHA256SUMS:8`
(`b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec  test_outputs.py`). Line 27 is the frozen C2
case table; file is 46 lines / 1564 bytes, matching the S166 row's cited range `test_outputs.py:1-46`.

Committed row state that this re-open does **not** change (`awk -F'|'` on `corpus/SOURCES.md:181`): id `S166`,
class `code`, tier `A`, status `mined`, last-opened `2026-10-27`, recheck `180d`, used-by
`corpus/knowledge/tb2-polyglot-c-py-grader.md`. This seat writes no `SOURCES.md` row and makes no corpus edit.

## 3. Reject candidate — `SOURCES.md` Leads line 218 (tbench.ai task hub / live leaderboard)

Lead text as committed (`corpus/SOURCES.md:218`): “tbench.ai task hub (hub.harborframework.com terminal-bench/4)
and the live leaderboard: opened but only a skeleton leaderboard rendered; task specs and harness repo still to
mine.”

```
$ curl -sSL -o hub.html -w 'HTTP %{http_code} bytes=%{size_download}\n' 'https://hub.harborframework.com/terminal-bench/4'
HTTP 404 bytes=26304
   body text: "Harbor Hub Harbor Hub Datasets Tasks Organizations Jobs Page not found
              The page you're looking for doesn't exist or has been moved. Go home"

$ for p in terminal-bench datasets/terminal-bench terminal-bench/4 tasks ; do printf '%s -> ' "$p"; \
    curl -sS -o /dev/null -w '%{http_code}\n' "https://hub.harborframework.com/$p"; done
terminal-bench -> 404
datasets/terminal-bench -> 200
terminal-bench/4 -> 404
tasks -> 200

$ curl -sSL -o tb.html -w 'HTTP %{http_code} bytes=%{size_download}\n' 'https://hub.harborframework.com/datasets/terminal-bench/terminal-bench'
HTTP 200 bytes=137541
   text: "Terminal-Bench is wide and dynamic. … Terminal-Bench will be continuously updated with new and
          improved tasks. Run … harbor run -d terminal-bench/terminal-bench \"

$ grep -c -i polyglot tb.html ; grep -c -i polyglot tasks.html
0
0
$ curl -sSL 'https://hub.harborframework.com/datasets/terminal-bench/terminal-bench-2-1?tab=tasks' -w 'HTTP %{http_code} bytes=%{size_download}\n'
HTTP 200 bytes=138722
$ grep -c -i polyglot tb21tasks.html
0

$ grep -o 'href="[^"]*"' hubroot.html | sort -u | grep terminal-bench
href="/datasets/terminal-bench/terminal-bench"
href="/datasets/terminal-bench/terminal-bench-2-1"
href="https://hub.harborframework.com/datasets/terminal-bench/terminal-bench/latest?tab=leaderboard&amp;leaderboard=4-0-0"
```

Observed shape: the lead's exact path is gone (404); the live hub exposes dataset landing pages only, which
serve an install/run recipe (`uv tool install "harbor[modal,daytona]"`, `harbor run -d terminal-bench/terminal-bench`),
a citation block, and `github.com/harbor-framework/terminal-bench` links. No per-task specification, requirement
map, version history or content digest appears in the server-rendered bytes of `/datasets/terminal-bench/terminal-bench`,
`…/terminal-bench-2-1`, `…?tab=tasks` and `/tasks` (0 `polyglot` occurrences in each). The pages hydrate
client-side, so absence in server bytes is not proof the rendered app lists no tasks — but nothing at a pin is
citable from them, and the dataset page itself states it is continuously updated.

Incidental observation (not scored, not a row, outside this seat's item): the `terminal-bench-2-1` page carries a
citation naming `arXiv 2601.11868` (`@misc{merrill2026terminalbenchbenchmarkingagentshard, …}`). That is a
separate candidate for a future Gate; this seat neither opened nor judged it.

## 4. Drafted `## Gate` block (drop-in for `corpus/lessons/round-49.md`)

Draft only — the L1 owns the lesson file and this seat did not touch it. No new `SOURCES.md` row is created by the
block; S166 keeps every cell.

```markdown
## Gate

Re-opened this round by the L1, access date 2026-10-28 for every row (times -03), after the stage-1 freeze
(`9d2900af41e4d1fc6022eff99010436fde6dbd93`, 2026-10-28T09:14:40-03:00) and before any scored C2 work. S166 was
re-opened at its pinned raw URL and the fetched bytes are `cmp`-identical to the round-46 committed capture
inside the freeze (`corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py`, `SHA256SUMS:8`). No new
`SOURCES.md` row is written and S166 keeps its tier/status/used-by cells; the reject below decides a `Leads
(unopened)` entry and therefore adds no row either.

| candidate | verdict | reason + flip | URL | accessed | located quote (≤25 words) |
|---|---|---|---|---|---|
| S166 — `tests/test_outputs.py` (TB2 `polyglot-c-py`) | **ACCEPT** — the claim's primary scoring predicate | the pin is a commit path, so the bytes are content-addressed, and the live fetch is byte-equal to the committed capture (sha256 `b94a7a98…ddec`, 1564 B, 46 lines); this is the exact predicate the frozen C2 case table is written against: one exact directory listing, one gcc compile, python3/C stdout equality on three fixed sizes. Flip: reject if a re-fetch at commit `2fd12b88…` changes the digest | `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py` | 2026-10-28 | `:27 "test_cases = [(42, \"267914296\"), (10, \"55\"), (0, \"0\")]"` (8 words) |
| Lead `tbench.ai` task hub / live leaderboard (`SOURCES.md` Leads, line 218) | **REJECT** as a row and as a case-table ground | the lead's URL now 404s; the live hub serves only a run recipe plus a dataset page that says it is continuously updated, with no per-task spec, requirement map or digest in its server bytes (0 `polyglot` occurrences on the dataset, `?tab=tasks` and `/tasks` pages), so nothing is citable at a pin and the page can move under a recheck. It also defers to `harbor run -d terminal-bench/terminal-bench`, i.e. to the repository S166 already pins, adding no independent bytes. Flip: a stable per-task endpoint (or a versioned dataset revision id) that serves task bytes with a digest and a version history | `https://hub.harborframework.com/terminal-bench/4` (404); live dataset page `https://hub.harborframework.com/datasets/terminal-bench/terminal-bench` (200) | 2026-10-28 | 404 body: `Page not found The page you're looking for doesn't exist or has been moved.` (14 words); live page: `Terminal-Bench will be continuously updated with new and improved tasks.` (9 words) |

The hub adds no basis the claim needs: the C2 case table stays grounded in the immutable repo pin alone.
```

## 5. Limits

- The hub pages are client-hydrated; the reject is stated on server-rendered bytes and on the lead URL's 404,
  not on a claim that the rendered app contains no task list.
- No full rendered-browser inspection of `hub.harborframework.com` was made (no browser tool used; HTTP only).
- Only one lead was reopened, as the item specifies; the other Leads entries are untouched.
- S166 was re-opened by HTTP fetch at the pinned commit path; the byte-equality check is against the committed
  capture inside the freeze, so a network substitution would have to reproduce the same 1564 bytes to pass.
- No counter, probe, `--dry` or `--stage-check` was executed: this seat records no C2 evidence beyond the Gate
  block, and asserts no R49-C1/R49-C2 admission.
- Tooling: none installed or upgraded; no pacman transaction attempted.
- Scratch tree `/fast/scratch/hyaku/kengaku-r49/R49C2ScribeGate` was removed before yield (`ls` after removal
  errors with "No such file or directory"); no scratch path is cited as evidence.

## VERDICT

Gate draft complete for R49-C2: S166 **ACCEPT** (live bytes at commit `2fd12b88…` sha256
`b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec`, byte-equal to the committed freeze capture,
line 27 quote verified); one lead **REJECT** (`SOURCES.md` Leads line 218, hub URL 404 / live page mutable and
spec-free). Stage-1 freeze `9d2900af…` verified present, ancestor of `af88aab…` and earlier than every
measurement; no scored run made; lane corpus untouched.
