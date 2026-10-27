# R48C2Echo — echo-control critic report

Axes named: coverage (C2); no other axis assessed.

## Freeze / scope

The stage-1 freeze exists at `a543d92083557dd9b33ee674e9b99b03411f80af`, committed `2026-10-27T06:53:29-03:00`; that commit adds `plans/round-48-claims.md`. The claims file has no diff between that commit and lane tip `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767`. I inspected the frozen-base clone at REV `a543d92083557dd9b33ee674e9b99b03411f80af`. The v4 counter and stage-2 amendment are not present there. Therefore I did not run any counter, gate, probe, or scored evaluation; the exact v4 control output remains unmeasured until the L1 commits stage 2.

## Counterexample / analysis

Copying `polyglot-c-py-dry-cases-freeze.txt` verbatim over the receipt is caught by the imported v3 V4 contract independently of P10: dry rows have `CASE <id> predicted=... tests=...` but no `observed=`, `match=`, or receipt summary. `receipt_cases()` accepts only rows matching `CASE <id> predicted=(pass|fail) observed=(pass|fail) ...`; V4 also requires exactly one summary, and checks parsed CASE count against the frozen ids. Thus the copied dry rows can preserve the IDs but cannot yield parsed receipt cases or the required summary. The v4 V7 delta is an additional guard: it requires violated tags evidenced by committed cases, whereas the dry table’s `TAG` declarations are not receipt case violations. This supports the echo control’s expected fail under the frozen contract, but is static analysis, not an executed v4 result.

The exact committed round-46 output is not itself a valid receipt for the required v4/P10-disabled control: `control-c3-echo.txt` says it was measured at `cf7de6af112e5d491ebd47318682b05fe864c125`, has `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt`, `V4 DEFECT receipt, entry or frozen dry table absent`, `checks=13 defects=8`, and `PREDICATE C3 fail`. Its P10 and ordering evidence cannot establish that the round-48 echo control fails with P10 disabled.

## Exact committed gate/control outputs reviewed

- `.ufo/waves/round-46/integrate/c3-landing.txt`, REV label `e9d201455c3774921aa5dfc287f07b4b9f113e76`: V7 reports `both-print` and `toolchain` missing; V8 is `DEFECT`; `checks=13 defects=2`; `PREDICATE C3 fail`. ORDER detail says `ORDER HIT ... control-c3-echo.txt ... kind=gate-p10 ...` and `ORDER RESULT FAIL`.
- `.ufo/waves/round-46/claims/control-c3-base.txt`, measured HEAD `cf7de6af112e5d491ebd47318682b05fe864c125`: `V4 DEFECT receipt, entry or frozen dry table absent`; `checks=13 defects=8`; `PREDICATE C3 fail`.
- `.ufo/waves/round-46/claims/control-c3-filler.txt`, same measured HEAD: `checks=7 defects=6`; `PREDICATE C3 fail`.
- `.ufo/waves/round-46/claims/control-c3-echo.txt`, same measured HEAD: exact observations above; it does fail, but not under the round-48 P10-disabled protocol.

## Commands run

- `git clone --shared --quiet /home/vgpnk/Projects/shokunin/kengaku-shokunin lane` (inside the seat scratch); `git rev-parse HEAD`; `git checkout --quiet a543d92083557dd9b33ee674e9b99b03411f80af`; `git rev-parse HEAD`.
- Lane read-only: `git show --stat a543d92083557dd9b33ee674e9b99b03411f80af`; `git log -1 --format='%H %cI %s' a543d92083557dd9b33ee674e9b99b03411f80af`; `git diff a543d92083557dd9b33ee674e9b99b03411f80af bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767 -- plans/round-48-claims.md` (empty); `git diff ... --stat`.
- `sha256sum plans/round46_c3_verify.py` → `a971c24dd5d0cb880e97ad4dd80315fcf58afaa02f8cffb5cc2e803aa292a8d4`.
- No counter/gate/probe commands were run.

## Sources / limits

Only the lane files and local round-46 lesson were opened. For source provenance, that lesson records URL `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py`, reopened/accessed `2026-10-27`; located quote (≤25 words): “test_cases = [(42, \"267914296\"), (10, \"55\"), (0, \"0\")]”. I did not independently fetch that URL. Limits: stage-2 v4 counter, P10-disabled control receipt, and v4 exact gate outputs are not yet available; no runtime outcome is claimed.

VERDICT: Static evidence indicates verbatim dry-table-as-receipt is rejected by inherited V4 (and should also fail the frozen V7 condition); the required round-48 P10-disabled control execution is unverified and must be recorded after stage 2, without altering the freeze.
