# F42RevBatArow — non-author honesty review of `plans/battery42/a_row.py` (X9 / X13 / X15)

Seat: reviewer, kengaku round 42 wave 2 (FALSIFY), 2026-10-26. Target: `plans/battery42/a_row.py`
sha256 `947194e4517fb94b8d3529e6c4d5118585697497103784655ddd736635b48df8` — byte-identical in the lane
working copy and in my clone at `508434ad55c709337065611691c426f05875492d` (`sha256sum` on both; lane tip
`3e8a2e5e` carries the same file). Counter `plans/round42_c1_verify.py` sha256
`559fca0c9254e4c09f2406f75ba9559e370012ccb1ecdc91c9a944abbe0c6649` = the frozen digest in
`.ufo/waves/round-42/claims/frozen-digests.txt`; tool pin `anchor_digest_check.py`
`11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2` = frozen. Clone:
`/fast/scratch/hyaku/kengaku-r42/F42RevBatArow/lane` (`git rev-parse --show-toplevel` printed that path
before every git call); nothing committed anywhere. I am not the module's author (R42BatAncRow built it);
I read the author's report `.ufo/waves/round-42/build/R42BatAncRow.md` only after forming my own reading
of the code.

## 1. Axes attacked

1. **Shape honesty** — for each of the six fixtures: does the built repo instantiate the advertised
   sentence of the mutant it kills, or does it reach the declared rc/class direction another way
   (the wave-1 substitute shapes: receipt-is-directory, emptied-directory, staged-manifest-only)?
2. **Witness derivation** — does the module read, import or copy
   `.ufo/waves/round-42/claims/witness/{w_anchor,w_order}.py`, or is it a renamed copy of them?
3. **Fixture-leverage tricks** — repo-local `.git/config` keys, symlinks, `core.worktree`, gpg/
   `log.showSignature` payloads in the module source **and in the repos it actually builds**.
4. **Live kill** — the counter on my clone, inside the Q32 envelope, `--battery-dir` holding only this
   module, `--only X9,X13,X15`.

## 2. Advertised sentences and old → new (counter source, quoted)

| mutant | adv (plans/round42_c1_verify.py) | old → new |
|---|---|---|
| X9 (`:166-170`) | `anchor_digest_check.py:34-35 'A row that matches the census regex but does not have 11 cells is a row-malformed defect'` | `if len(r["cells"]) != NCELLS:` → `if len(r["cells"]) > NCELLS:` |
| X13 (`:176-180`) | `anchor_digest_check.py:73 '`--evidence-ref head` (default) reads HEAD blobs, so an unpromoted capture never counts'` | argparse `default="head"` → `default="index"` |
| X15 (`:186-190`) | `anchor_digest_check.py:108-110 'at least one other token that is 64 lowercase hex and a digest **of the capture that row names**'` | `and (t in row_scope if row_scope is not None else t in allowed)` → `and t in allowed` (`anchor_digest_check.py:454-455`) |

Emission sites (grep, one each): `row-malformed` only at `anchor_digest_check.py:477-480` (inside the
X9-mutated cell-count branch, which `continue`s before any token is read); `erratum-incomplete` at
`:465` gated by `if not supported:` over the X15-mutated `supported` set (`:454-455`); `digest-unknown`
at `:535` (token ∉ row scope and ∉ global A). So each fixture's declared classes can only flow through
the mutated span's branch — the honesty question is whether the *input* is the advertised shape.

## 3. Built-state evidence (the decisive check)

I rebuilt all six fixtures with the counter's own build child
(`--build-module $S/bat/a_row.py --dest $S/built`, inside the envelope, receipt `run-build-child.txt`)
and inspected the actual repos (`git config --list --local`, `find -type l`, `log`, `diff --cached
--name-only HEAD`, row census, digest recomputation). Receipt: `inspect-built.txt`. Per fixture:

| fixture (builder) | kills | verdict | built state (measured) |
|---|---|---|---|
| `a_row-x9-short-no-token` (`a_row.py:49`) | X9 | **honest** | 1 commit, clean; row S901 `cells=10 anchor-cell='' tokens=[]`. A census row short one cell with no digest claim — exactly the sentence's subject; `row-malformed` has exactly one emission site, the mutated line. Mutant (`>11` only) leaves it unflagged → rc 0. |
| `a_row-x9-registry-short-valid` (`:61`) | X9 | **honest** | 6 rows: S911/S913/S915 11-cell claim-less (raise nothing), S912/S914 11-cell correctly anchored, **S916 `cells=10` carrying a CORRECT committed digest** (`4b73cf48…` = the alpha capture, same token S912 resolves). Green on every digest test, disqualified only by cell count — the strongest form of the advertised shape; rules out any "flagged because the digest was wrong" reading. |
| `a_row-x13-staged-capture` (`:82`) | X13 (X7 side-effect in full runs only) | **honest** | `index-vs-HEAD delta: corpus/evidence/alpha/cap.txt` — the capture FILE itself is the only staged thing (manifest stays at HEAD, verified); HEAD bytes digest `7d2a59bf8ddf`, index bytes `c5af99eb2553`, committed row claims `c5af99eb2553…`. The unpromoted capture is precisely what the sentence names: head mode → `digest-unknown`, index mode → resolved. |
| `a_row-x13-url-staged` (`:102`) | X13 | **honest** | same unpromoted-capture delta on `corpus/evidence/tb2-wiki/test_outputs.py` (HEAD `0cc3bf1b175c`, index `9a6c2b6f0fb7`, row claims `9a6c2b6f0fb7…`), row bound through the pinned `raw.githubusercontent.com` URL + `task.toml name = "tb2/wiki"` route, plus a clean sibling row S904. Demonstrates the sentence on the URL binding branch, not just the explicit-path one. |
| `a_row-x15-sibling-digest` (`:126`) | X15 | **honest** | corrected row S905 is BOUND to its own capture (row scope `1740d730e15e…`); its anchor `f281d6d8c062…` is committed nowhere; the erratum's correction `9b2c71da385d…` is the sibling row S906's real committed capture digest (file bytes AND its SHA256SUMS entry). In global A, not in the row's scope — exactly the laundering shape the sentence forbids; unmutated → `digest-unknown`+`erratum-incomplete`, mutant exempts → rc 0. |
| `a_row-x15-manifest-sibling` (`:144`) | X15 | **honest** | erratum committed in a LATER commit (`log: e8ad807 erratum ; 0c77cd6 rows`); correction `d78f4847e4fa…` is the sibling capture's manifest-listed OLDER digest (sibling file is now `6a64702d0e55…`, its committed SHA256SUMS lists `d78f4847…`) — in global A only via the manifest view, still outside the URL-bound row's scope (`1241278651f1…`). Harder variant of the same sentence; both declared classes fire unmutated and both vanish under the mutant. |

None of the three wave-1 substitute shapes is present: the module is anchor-only (every argv is
`["--lane", str(r)]`; no `--claims`/`--receipt` exists in it), so no directory-receipt shape is even
expressible, and both X13 fixtures stage the capture file itself, not a manifest or locator table.

## 4. Witness derivation check

- Source scan: `grep -nE "witness|w_anchor|w_order|\.ufo|open\(|read_text|read_bytes|import |subprocess|os\.|shutil|eval|exec"` on `a_row.py` → single hit `8:import hashlib`. The module reads nothing and imports nothing but `hashlib`; the counter's own SIDECHANNEL scan (which includes `witness`, `/home/`, `.local`, `core.`) passed: `sidechannel=0` in every run.
- Structure overlap (shared non-blank lines, `LC_ALL=C comm -12`): a_row vs w_anchor = 29 of 151/127 — all battery-contract boilerplate (`PIN`, `import hashlib`, `dig`/`capture`/`commit` bodies, `ctx.write(r / "corpus/SOURCES.md",` openers, `return ["--lane", str(r)]`, the `FIXTURES = [` frame) that the counter's module contract (`round42_c1_verify.py:49-57`) requires of every battery module; a_row vs w_order = 4 trivial lines. Fixture ids, builders, row shapes, registry layouts and erratum texts are all distinct from the witness modules (witness w9's short row carries a real capture digest; a_row's primary is digest-free and its second sits in a six-row registry with a correct digest; witness w13 stages capture+SHA256SUMS and leaves the row uncommitted in the worktree; a_row commits the advanced row and stages only the capture; witness w15 is a one-row registry with a same-commit erratum; a_row's are two-row registries, one with a later-commit erratum citing a stale manifest view). **Not a renamed copy.**

## 5. Fixture-leverage tricks

- Module source: no `git config`, no symlink creation, no `core.worktree` / `gpg` / `log.showSignature` / `include.path` / `fsmonitor` / `hooksPath` / `alias.` tokens (grep above; the counter's token scan agrees).
- Built repos (all six, `inspect-built.txt`): `git config --list --local` returns only the four `git init` defaults (`core.repositoryformatversion`, `core.filemode`, `core.bare`, `core.logallrefupdates`); `find <fixture> -type l` → none. The only index-vs-HEAD deltas are the two X13 capture files, as designed. **No trick present.**

## 6. Live counter run (my clone, Q32 envelope)

Command: `python3 $S/lane/plans/round42_c1_verify.py --lane $S/lane --battery-dir $S/bat --only X9,X13,X15 --work $S/w1` where `$S/bat` holds only `a_row.py`. Envelope for every run:
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>`. Receipt `run-counter-only.txt` (18:06, before/after local-bin listing digest `8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52` unchanged; hash method `ls -A /home/vgpnk/.local/bin | LC_ALL=C sort | sha256sum` — the plain pipeline is collation-dependent across tool environments, same 102 entries either way):

```
PINS total=2 mismatched=0
FIXTURE a_row-x9-short-no-token tool=anchor expect=reject declared=row-malformed observed_rc=1 observed=row-malformed ok
FIXTURE a_row-x9-registry-short-valid tool=anchor expect=reject declared=row-malformed observed_rc=1 observed=row-malformed ok
FIXTURE a_row-x13-staged-capture tool=anchor expect=reject declared=digest-unknown observed_rc=1 observed=digest-unknown ok
FIXTURE a_row-x13-url-staged tool=anchor expect=reject declared=digest-unknown observed_rc=1 observed=digest-unknown ok
FIXTURE a_row-x15-sibling-digest tool=anchor expect=reject declared=digest-unknown,erratum-incomplete observed_rc=1 observed=digest-unknown,erratum-incomplete ok
FIXTURE a_row-x15-manifest-sibling tool=anchor expect=reject declared=digest-unknown,erratum-incomplete observed_rc=1 observed=digest-unknown,erratum-incomplete ok
MUTANT X9 anchor rc-silence killed by=a_row-x9-short-no-token attributed=L477 hits=2 -- plans/anchor_digest_check.py:34-35 'A row that matches the census regex but does not have 
MUTANT X13 anchor rc-silence killed by=a_row-x13-staged-capture attributed=L570 hits=2 -- plans/anchor_digest_check.py:73 '`--evidence-ref head` (default) reads HEAD blobs, so an u
MUTANT X15 anchor rc-silence killed by=a_row-x15-sibling-digest attributed=L455 hits=2 -- plans/anchor_digest_check.py:108-110 'at least one other token that is 64 lowercase hex an
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=3/3 order=0/0
ADVERTISED direct=3 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

Second run, same module, full default mutant set (receipt `run-counter-full.txt`, rc=1 as expected for a
single module): `MUTANT X7 anchor silence killed by=a_row-x13-staged-capture attributed=L535 hits=4`
also appears — the author's disclosed side effect (`R42BatAncRow.md` §4: "not claimed as its design
intent"); with `--only X9,X13,X15` it does not fire. `wrong=0 tampered=0 sidechannel=0` and
`PINS-AFTER mismatched=0` in both runs.

## 7. Verdict table

| fixture | mutant(s) killed | honest / substitute / incidental | reason in one line |
|---|---|---|---|
| `a_row-x9-short-no-token` | X9 | honest | 10-cell census row, no digest claim; the only `row-malformed` site is the mutated cell-count line. |
| `a_row-x9-registry-short-valid` | X9 | honest | 10-cell row with a CORRECT committed digest — disqualified only by cell count. |
| `a_row-x13-staged-capture` | X13 | honest | staged delta is the capture file itself; committed row claims the index-only digest; head vs index is the whole flip. |
| `a_row-x13-url-staged` | X13 | honest | same unpromoted-capture shape through the URL/task.toml binding branch, clean sibling beside it. |
| `a_row-x15-sibling-digest` | X15 | honest | bound row; erratum cites the sibling's real committed digest — in A, not in the row's scope. |
| `a_row-x15-manifest-sibling` | X15 | honest | later-commit erratum; correction reachable in A only via the sibling's stale manifest view. |

**6/6 honest, 0 substitute, 0 incidental.** The module demonstrates the three advertised sentences with
independent second triggers on different binding branches, and its X13/X15 shapes are materially
different from — and stricter than — the witness modules' (committed rows, capture-only staging,
later-commit errata, manifest-view corrections).

## 8. Limits

- Attribution stays the freeze's known limit: the attributed spans (cell-count line, argparse default,
  `supported` set) execute on every row/invocation, so `attributed=L…` alone proves nothing about
  intent; this review is the non-author gate the freeze names, and it rests on the built shapes above,
  not on attribution.
- I ran `--only` (predicate n/a by the counter's own rule) plus one full-default run of this module
  alone; I did not re-derive the landing's 14/14 across the other four modules.
- The X7 side-kill on `a_row-x13-staged-capture` is real but outside this module's declared intent;
  whether battery42's dedicated X7 coverage is honest is another seat's row.
- Fixtures are 1-6-row synthetic registries; they do not model the lane's 109-row `SOURCES.md` (author's
  own stated limit; the advertised sentences are per-row, so this does not weaken the kills).

## Receipts (all under `.ufo/waves/round-42/falsify/F42RevBatArow/`, each < 1 MiB)

| file | sha256 |
|---|---|
| `run-counter-only.txt` | `7ef95b0f79a24517d9da3eccf794898d9d357f221e2d98cad3a2cad72d884fa5` |
| `run-counter-full.txt` | `8adcd3e9114ae6442131be23de735bc24e201b9cc6a479862f4311b43aa0f685` |
| `run-build-child.txt` | `c5b3612c51aee523587b9323056b0cdc79543e8685bd1d19b753994ade2db653` |
| `inspect-built.txt` | `9afb234db85e26ff6bdd9dcf672d2c0bad903e0a72e80271f0380dd011d64e66` |

Every run above executed inside the Q32 envelope; `date +%T` and the local-bin listing digest are recorded
before/after in each receipt (18:03:53 session start → 18:07 runs; digest `8cf5b151…d52` unchanged across
all my runs). Nothing installed or upgraded (no pacman/uv/npm call); no lane file touched; scratch
`/fast/scratch/hyaku/kengaku-r42/F42RevBatArow` removed after the report was written.

VERDICT: battery42-a_row-honest-6/6-substitute-0
