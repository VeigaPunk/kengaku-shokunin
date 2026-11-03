# Round 68 — kengaku

author: kengaku L1 round 68 attempt 1
date: 2026-11-03
lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
status: skeleton drafted by the SourcesRows scribe seat (wave w1). The L1 owns this file; the
placeholders below are the L1's to fill or remove.

## Gate

**Sources opened this round** (SOURCES contract v1 rule 1: URL, access date, ≤25-word located
quote). Byte captures: `.ufo/waves/round-68/w1/SourcesRows/sources/`; receipt:
`.ufo/waves/round-68/w1/SourcesRows/S240-receipt.md`; scout captures under
`.ufo/waves/round-68/w1/recon/`.

- **S240 — REJECTED as specified (CPython `Lib/http/client.py` at `v3.14.8`).**
  URL https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/http/client.py · accessed
  2026-11-03 (HTTP/2 200; 59576 bytes; sha256
  `016aa7664201a82f0f37ddfb11ed662dd1f07aa23c9470c6a3cb3278aa479230`; the scout capture
  `recon/S240-client-py.txt` is byte-identical).
  Located quote: `def __repr__(self):` — `:1559`, inside `class IncompleteRead` (`:1554`); it is
  the file's only `def __repr__` (`awk 'NR>=858 && NR<=1531 && /__repr__/'` → `0`). Scout receipt
  `recon/S240-receipt.md` (`S240 opened=True sha=016aa766…`) records the same line and concludes
  the format is not produced by `http.client.HTTPConnection`.
  Reason: the frozen row's anchor (`HTTPConnection.__repr__` line) does not exist —
  `class HTTPConnection` (`:858`) defines no `__repr__`/`__str__`, so `object.__repr__` renders
  `<http.client.HTTPConnection object at …>`. This source cannot ground the corrected clause's
  mechanism.
  Flip: a CPython release that adds `HTTPConnection.__repr__` rendering host and port as separate
  fields.
- **S240 — ADMITTED (replacement source: urllib3 `src/urllib3/connection.py` at `2.7.0`).**
  URL https://raw.githubusercontent.com/urllib3/urllib3/2.7.0/src/urllib3/connection.py ·
  accessed 2026-11-03 (HTTP/2 200; 42786 bytes; sha256
  `668b37ab12835bdf8643a695a9f050551339b280742231f163fc575a925a1532`; byte-identical to pip
  26.2.1's vendored `pip/_vendor/urllib3/connection.py`, `pip/_vendor/vendor.txt:11` →
  `urllib3==2.7.0`; scout capture `recon/S241-urllib3-2.7.0-connection.py` matches; scout receipt
  `recon/S241-receipt.md` gives the same `:164` quote for its secondary 2.7.0 capture — adopt the
  2.7.0 bytes, not the receipt's 2.5.0 primary, which has no renderer).
  Located quote: `return f"{type(self).__name__}(host={self.host!r}, port={self.port!r})"` —
  `:164`, inside `def __str__` (`:163`), `class HTTPConnection` (`:82`). Chain:
  `NewConnectionError.__init__` formats `f"{conn}: {message}"` (`exceptions.py:148`, sha256
  `8503c7a2aa38cb0e3a7ac3525647225505d5520031580825b21e8c6f242d6be4`).
  Gate result: **admit** — host and port are separate fields, so the literal `localhost:8080` is
  not a form this renderer produces. Captured K2 stderr: `host='localhost'` ×5, `port=8080` ×5,
  `localhost:8080` ×0 (`corpus/evidence/round68/pypi/stderr/K2.txt`).
  Note on the CPython receipt's other quote (`:921`, `(self.host, self.port) =
  self._get_hostport(host, port)`): it shows separate *attributes*, not a rendering; relabelling
  the claims sentence as "stores host and port separately" would still not support
  `HTTPConnection.__repr__`.

- **S240 — RE-OPENED (attempt 2, 2026-11-03).** URL
  https://raw.githubusercontent.com/urllib3/urllib3/2.7.0/src/urllib3/connection.py · accessed
  2026-11-03 attempt 2 (HTTP/2 200; 42786 bytes; sha256
  `668b37ab12835bdf8643a695a9f050551339b280742231f163fc575a925a1532` — matches the row and the
  attempt-1 capture; capture `w2/SourceReopen/connection.py`). Located quote:
  `return f"{type(self).__name__}(host={self.host!r}, port={self.port!r})"` — `:164`, inside
  `def __str__` (`:163`), `class HTTPConnection` (`:82`). The row's `exceptions.py:148` chain
  re-checked (9945 B, sha256 `8503c7a2aa38cb0e3a7ac3525647225505d5520031580825b21e8c6f242d6be4`).
  The pip 26.2.1 wheel (PyPI digest `71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e`)
  carries `pip/_vendor/urllib3/connection.py` byte-identical to the 2.7.0 fetch, so the row's
  vendoring claim is verified against the named release. Row shape: 11 columns, tier A, opened
  2026-11-03, recheck 180d, `used-by` resolves; status was `queued` → corrected to `mined` (below).
  Row verdict: stands as written after the status fix.
- **S240's rejected CPython row — RE-CHECKED (attempt 2, 2026-11-03).**
  https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/http/client.py · HTTP/2 200 ·
  59576 bytes · sha256 `016aa7664201a82f0f37ddfb11ed662dd1f07aa23c9470c6a3cb3278aa479230`;
  `class HTTPConnection` defines no `__repr__`/`__str__`; the file's only `def __repr__` is at
  `:1559`, inside `class IncompleteRead` (`:1554`). Rejection confirmed; the admitted row remains
  the urllib3 2.7.0 renderer.
**Admitted rows this round:** S240 — urllib3 `src/urllib3/connection.py` at tag `2.7.0`
(option A in `w1/SourcesRows.md`; the S240 id was never written, so it carries the row that
grounds the corrected clause).
**Rejected rows this round:** the CPython `Lib/http/client.py` row as specified (see above);
its rejection and the re-source are recorded by amendment A1 in `plans/round-68-claims.md`.
**Assimilation:** none this round (F4; L0 `kengaku | round-54` unresolved).

**Registry status change (rule 2, old→new).** S240 `status`: `queued` → `mined` (2026-11-03, attempt 2):
the row's `used-by` cell names `corpus/knowledge/tb2-network-service-offline-grader.md`, which cites
S240, and the contract defines `mined` as "cited by ≥1 path in `used-by`". Attempt 1 wrote the row
with `queued` (w2 `CensusAudit` finding F1; `SourceReopen` F1). No other cell changed; the census stays
exit 0.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| reference-drift (wrong-sha citation) | `corpus/lessons/round-67-verifier-spotcheck.md` §5 item 1 — the round-67 report and `corpus/evidence/round67/pipe/a1-mutants.txt` cite `32bacf1d629e7d5809788ef7ea2183fd7b08a11b10c383cc9942e2f58842b836` (the pre-A1 probe at `dcc39ea3`) as the amended counter; the receipt of record binds `03793f4f9e184e8f829916ef848e0f0d41d94b1bef8ed17eda0fe3c28b0a9f1e` | none — the report quoted the sha from memory instead of re-hashing the committed bytes | the R68-C2 erratum (`plans/round-67-claims.md` `## Erratum (round 68)`): both shas named, golden value `03793f4f…`; gate E1 re-hashes the committed probe and the receipt at check time |
| number-drift (count drift) | `corpus/lessons/round-67-verifier-spotcheck.md` §5 item 2 — report and `LOG.md:2542` say A1 mutants "8 killed, 1 accepted"; the committed `a1-mutants.txt` shows 7 refused (rc 1) + 1 accepted by design = 8 mutants | none — the count was copied from prose, not re-derived from the committed file | the R68-C2 erratum states `7 refused` and `1 accepted by design`; gate E2 requires both substrings in the erratum section |
| mechanism-attribution (wrong-source-memory, same family as the sha-citation row) | `plans/round-68-claims.md` §R68-C1 attributes the stderr rendering to `http.client.HTTPConnection.__repr__`; the opened bytes show no such method — the renderer is urllib3 2.7.0 `HTTPConnection.__str__` (`w1/SourcesRows/S240-receipt.md` §A–§B, `w1/RenderingTrace.md` §5) | none — no gate opens a source row's anchor before the freeze; the row was written from memory of CPython's API | the lesson Gate rejects the CPython row and admits urllib3 2.7.0; amendment A1 (dated) in the claims doc records the re-source; the S240 row's anchor is a checked line of committed bytes |
| kill-rule-misstatement | `plans/round-68-claims.md` kill rule (c) names "the 900 s bound"; the instrument's `LEG_TIMEOUT = 900` is dead code — the operative bound is the round-63 module's `LEG_TIMEOUT = 180`, and a timeout scores `F` under the frozen leg rule rather than exit-2 (`w1/ForgeScan.md` M-1; `w1/ClaimFalsify.md` kill-rule review) | the sentinel and critic seats — the checker's behaviour under `TimeoutExpired` was demonstrated on a forged receipt | recorded, not patched: amendment A1 item 2 names the effective 180 s bound and the `F`-on-timeout mapping; the scored run saw no timeout, verdict stands |
| counter-under-enforcement | `plans/round68_c2_correction_gate.py` E1 returned the first `## Erratum (round 68)` section and never counted headings; a duplicated section passed (`w1/ForgeScan.md` M-2; `w1/gate/clause-fixtures.txt`) | the sentinel's fake-root fixture and the executor's clause fixtures | patched per the R67-A1 pattern (amendment A1 item 3): E1 counts heading lines and requires exactly one; post-patch duplicate fixture refuses (`corpus/evidence/round68/c2-e1-exactly-one.txt`) |
| report-contract-omission (a round report filed with no `## SHONEN` and no `## Trend verdicts`) | the attempt-1 report (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-68/kengaku.md`, sha256 `0399cd5376d27e1c006075929a9b3511c820fc326b4a3751a4cd9b78b8573839`, 12415 B, fleet commit `a7575677`) carries seven `##` sections and neither required heading (`grep -c '^## SHONEN'` → 0, `grep -c '^## Trend verdicts'` → 0); the driver's content check failed — `lane-dead-no-report kengaku round=68`, `.ufo/watchdog.log:2132` (2026-11-03T20:20:14-03:00) | none — the prompt's pre-report gate `grep -c '^## SHONEN' <report>` must print 1 and attempt 1 did not run it; the lane had no executable check for the section set | `plans/round68_report_contract.py` (A2, frozen `7803bdd4`): S1–S6, red on the attempt-1 bytes (`PREDICATE R68-A2 fail`, rc 1), green on a compliant skeleton, selftest `n=5 red-refused=4 green-ok=1`; the attempt-2 report is gated before filing |
| record-shape-drift (the lesson's own `## Mistakes` table split by a blank line, a finding restated as orphan prose outside it, and A2's seat arithmetic wrong) | `corpus/lessons/round-68.md:64` blank line split the table after the number-drift row; `:68–77` repeated the mechanism-attribution row as prose; `plans/round-68-claims.md` A2 item 4 said "10 seats" while the dispatched spec has 12 (`.ufo/waves/round-68/w2-spec.json`) | the w2 `ScribeAttempt2` seat's `nl -ba` read and seat count | table merged, orphan removed, and the dated A4 erratum corrects the seat count to 12 (executor 4; attack 4/12 = 33 %) |
| registry-incompleteness (`round66_c1_tensor_probe` had no SKILL registry row) | `grep -c 'round66_c1_tensor_probe' SKILL.md` → 0 at `0e52fb5d`; the round-66 capability entered the table in round 66 but its probe was never registered | the w1 `RegistryRows` seat (finding 2) and the w2 `ScribeAttempt2` seat | row appended to the `## Gate/probe registry` (`grep -c` → 2); its command re-derives `CHECK ok cases=5`, `PREDICATE R66-C1 pass`, rc 0 |
| registry-status-drift (S240 left `queued` while its `used-by` cited it) | `corpus/SOURCES.md:255` status `queued` at `0e52fb5d`; the contract defines `mined` as cited by ≥1 path in `used-by`, and the cell names `corpus/knowledge/tb2-network-service-offline-grader.md` | the w2 `CensusAudit` seat (medium finding) | status `queued` → `mined` in place (rule 2 old→new logged in this lesson's Gate); census still exit 0 |
| capability-table-omission (four capabilities declared entered, none in the table) | `python3 plans/round68_capability_table.py --lane .` → `MISMATCH n=4` at `7803bdd4` (receipt `.ufo/waves/round-68/w2/capability-table/red-before.txt`); the `## Capabilities` table stopped at round 51 | the w2 `CensusAudit` seat (low finding) and the L1's A3 re-derivation | four rows appended (rounds 64–67, first-working rounds and re-derivable evidence commands); same command → `MISMATCH n=0`, `PREDICATE R68-A3 pass`; selftest `n=5 red-refused=4 green-ok=1` |
