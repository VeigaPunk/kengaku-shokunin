# F42RevBatAroute — honesty review of `plans/battery42/a_route.py` (kills X1, X3, X12)

Seat F42RevBatAroute (reviewer, kengaku round 42 wave 2 FALSIFY), 2026-10-26.
Target: `plans/battery42/a_route.py` (169 lines), non-author review of whether each fixture builds the
shape the advertised sentence of the mutant it kills describes, or a substitute that reaches the declared
direction another way (wave-1 `R42CritC1Counter` §1 standard). Method: full read of the module, of the
counter's mutant table (`plans/round42_c1_verify.py:146-155,171-175`) and of the tool's binding code
(`plans/anchor_digest_check.py:254-258,260-290,313-350`); a full-module counter run and six
single-fixture probe runs, all inside the Q32 envelope. No lsp server is mounted in this seat session;
the review is full-text read plus empirical runs. Installed no tools (none needed).

Reviewed bytes = landing bytes: `sha256sum` of the lane working-tree file and of my clone's copy both give
`d6dad7cd1458838dcd546f2176ff5b2217faab78cc68b92c86ad94b688adf81f`; `git -C $S/lane diff --stat
508434ad55c7… ff14d76d32d6… -- plans/battery42/a_route.py plans/round42_c1_verify.py
plans/anchor_digest_check.py` prints nothing (docs tip = landing tip for these three files). Clone at
`/fast/scratch/hyaku/kengaku-r42/F42RevBatAroute/lane`, tip `508434a`, `rev-parse --show-toplevel` = the
clone; no git mutation performed.

## 1. The three mutants (counter table, verbatim `adv` and `old -> new`)

- **X1** anchor rc-mirror direct — adv `plans/anchor_digest_check.py:50-52 'Provenance row — a committed
  markdown under corpus/evidence/ whose table line carries this row's id'`;
  `got = [(cap, "provenance-row") for cap, _ in idx["prov_sid"].get(sid, [])]` → `got = []`.
- **X3** anchor rc-mirror direct — adv `plans/anchor_digest_check.py:57-58 'A provenance URL (an evidence
  markdown naming the same <repo>/<subpath>) is consulted when the task.toml route finds nothing'`;
  `if (repo, subpath) in idx["prov_url"]:` → `if False:`.
- **X12** anchor rc-mirror direct — adv `plans/anchor_digest_check.py:55-56 'matched **exactly** against
  the name = "<org>/<task>" a committed task.toml gives' (slash-less name fallback dropped)`;
  `pick = next((n for n in names if "/" in n), names[0] if names else None)` →
  `pick = next((n for n in names if "/" in n), None)`.

## 2. Per-fixture verdicts

Probe method: for each fixture a one-fixture battery dir (module copy with `FIXTURES` cut to that entry by
ast, in my scratch), counter run `--only X1,X3,X12`; receipt
`.ufo/waves/round-42/falsify/F42RevBatAroute/receipt-probe-matrix.txt`. Result matrix — every fixture
kills exactly its designed mutant, off-diagonal zeros (no incidental kills):

| fixture | kills (probe) | verdict | reason |
|---|---|---|---|
| a_route-x1-provenance-table | X1 only | honest | PROVENANCE.md committed at `corpus/evidence/42/route-a`; its table line carries row id S125 and ticked `registry.capture` resolving beside it — the tool:50-52 shape verbatim, plus a digest column. Row text has no URL and no `corpus/evidence/` path, so route 1 is the only binder; under X1 the row is unbound (rc 0→1). |
| a_route-x1-two-row-registry | X1 only | honest | Same shape at registry scale: two rows S126/S127, two tables in two evidence dirs, ticked `first.capture`/`second.capture`, no digest column (shows the advertised shape needs only row id + resolving filename); capture batch committed one commit before the rows. Rows carry no URL/path → route 1 only. |
| a_route-x3-provenance-url | X3 only | honest | No `task.toml` anywhere in the tree → the task.toml route finds nothing (`hits` empty, tool:331); the PROVENANCE.md URL column names the same `(repo, subpath)` as the row's raw URL, so the fallback at tool:343 is the only binder. PROVENANCE lines carry no row id, so route 1 is empty too. |
| a_route-x3-blob-url | X3 only | honest | Stronger than the minimum: blob-form URL (`URL_BLOB` parsed, tool:298-299) and a committed `task.toml` naming a different task (`acme/other-task` → slug `other-task`), so the task.toml route finds nothing even though a task.toml exists — the non-degenerate "finds nothing" case; the URL-column fallback is the only binder. |
| a_route-x12-slashless-toml | X12 only | honest | `task.toml` `name = "circuit-task"` (slash-less) in the only task dir; the URL's task component matches it exactly, binding via the slash-less fallback (tool:256) that X12 drops. No PROVENANCE.md → the X3 fallback route is impossible; row has no evidence path → route 3 impossible. |
| a_route-x12-two-tomls | X12 only | honest | Two task dirs: slash-less `data-task` (the binder) plus a decoy slashed `bench/other-task`; three-component subpath `group/data-task/lookup-circuit.txt`; capture accepted via its SHA256SUMS entry view. Under X12 the slash-less dir contributes no slug → unbound. |

None of the six is a substitute in the wave-1 sense: the wave-1 substitutes (receipt-is-directory,
emptied-directory, staged-manifest-only) reached the kill through a mechanism other than the advertised
one; here the single-fixture matrix proves the converse — a fixture kills X1/X3/X12 **only** if the
advertised route was its binder, because the other routes are structurally unavailable in each fixture
(no URL in row for X1; no row id in table and no task.toml match for X3; no PROVENANCE.md for X12).

## 3. Counter runs (all inside the Q32 envelope, §6)

Full-module run — battery dir holding only `a_route.py` (copy sha256-equal to the lane file),
`--only X1,X3,X12`; receipt `…/F42RevBatAroute/receipt-run-a-route-only.txt`, verbatim MUTANT lines:

```
MUTANT X1 anchor rc-mirror killed by=a_route-x1-provenance-table attributed=L318 hits=2 -- plans/anchor_digest_check.py:50-52 'Provenance row — a committed markdown under corpus/evi
MUTANT X3 anchor rc-mirror killed by=a_route-x3-provenance-url attributed=L343 hits=2 -- plans/anchor_digest_check.py:57-58 'A provenance URL (an evidence markdown naming the same
MUTANT X12 anchor rc-mirror killed by=a_route-x12-slashless-toml attributed=L256 hits=2 -- plans/anchor_digest_check.py:55-56 'matched **exactly** against the name = "<org>/<task>"
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=3/3 order=0/0
ADVERTISED direct=3 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

rc=0; `PINS total=2 mismatched=0`; all six FIXTURE lines `observed_rc=0 observed=- ok`. `hits=2` per
mutant = exactly the designed pair (matches the landing run `measure-final.txt` lines 37/38/42, which
also show `hits=2`). Single-fixture probes: each fixture `killed by=<itself> hits=1` for its own mutant,
`SURVIVED exhibits=none` for the other two (rc=1 expected: dev exit requires survived=0).

## 4. Witness copy check — clean

The battery may not import, copy or read `.ufo/waves/round-42/claims/witness/` (counter docstring line 57).
`a_route.py` imports only `hashlib`; it contains no `open(`, no `ctx.sh`, no path pointing outside the
fixture dir; every file it touches is created by `ctx.write` inside `d`. difflib against the witness
modules: ratio **0.178** vs `w_anchor.py`, **0.145** vs `w_order.py`; the only common blocks ≥2 lines are
`import hashlib`, the census HDR string (lane-dictated format), blank-line runs, the `def row(sid,
source, anchor):` signature line and `FIXTURES = [`. Even `dig`'s body differs (param `body` vs `b`);
`row()` bodies differ (scope `binding route` vs `fixture`, used-by `corpus/knowledge/fixture.md` vs
`x.md`); no `cap()` helper; row ids, directory layouts, table columns, URLs and commit graphs all differ.
The counter's own sidechannel token scan (token list includes `witness`) reports `sidechannel=0`. **Not a
renamed copy.**

## 5. Repo-local config / symlink / core.worktree / gpg — none

Grep of the module for `config|worktree|gpg|sign|symlink|os\.|subprocess|open(|ctx.sh|environ|import |witness|.ufo`
matches only the docstring fence, `import hashlib`, `SHA = …` and `HDR = …`. The module calls only
`ctx.init` / `ctx.write` / `ctx.git(add, commit)`; `ctx.init` is a bare `git init -q -b master`
(`round42_c1_verify.py:261-264`) writing no config; identity and config are pinned by env
(`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, fixed fixture author/committer and dates,
`GIT_CEILING_DIRECTORIES`, `round42_c1_verify.py:229-237`); `ctx.git` refuses any repo that is not its own
toplevel. `ctx.write` creates plain files only — no symlinks. No gpg/signature surface anywhere.

## 6. Envelope receipt (Q32)

Every counter run above was executed inside

```
/usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- <command>
```

Full-module run: `date +%T` 18:06:24 before → 18:06:25 after;
`ls -A /home/vgpnk/.local/bin | sha256sum` = `8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52`
before and after (unchanged). Probe runs used the same envelope (same session, minutes later). Scratch
`/fast/scratch/hyaku/kengaku-r42/F42RevBatAroute` (TMPDIR pointed there; deleted after this report via
`plans/scratch_guard.py safe-rm`).

## 7. Attribution context (known limit, not a defect of this module)

Wave-1 `R42CritAttribution` §2.1 measured the span leg vacuous for 8/14; X1's span L318 runs on every row
(span_hit 9/9 on the witness family), while X3 (L343) and X12 (L256) are discriminating (1/9). For this
module the weakness is mitigated by construction: because each fixture has exactly one available binding
route (§2), the reproduced result difference can only be caused by the advertised route's removal — the
property the span leg cannot check is supplied by the fixture design itself.

## 8. Non-blocking observations

- Fixture row ids S125–S129 coincide with the lane's real round-42 row ids (S125–S128). Cosmetic only:
  fixtures are standalone repos, row ids are per-repo, no counter surface reads the lane's rows in a
  battery run.
- `a_route-x1-two-row-registry`'s PROVENANCE table lines carry pinned URLs that feed `prov_url`, but the
  rows carry no URL, so nothing ever looks them up — inert, not a second route.
- Route 3 (explicit lane path) has no mutant in the 14 and gets no fixture here; the module's declared
  scope (routes 1, 2 and the slash-less fallback = exactly X1/X3/X12) is complete for its mutants.

Report: .ufo/waves/round-42/falsify/F42RevBatAroute.md
VERDICT: battery42-a_route-honest-6/6-substitute-0
