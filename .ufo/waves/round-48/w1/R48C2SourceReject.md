# R48C2SourceReject — Docker Hub source re-check

Axes named: coverage (R48-C2; source-evidence item only).

## Evidence
- Target cited by the round-46 Gate: https://hub.docker.com/r/alexgshaw/polyglot-c-py
- Access date: 2026-10-27.
- Reopened with `read` (Docker Hub API-backed rendering). Located quote (17 words): “Recent Tags | Tag | Size | Architectures | Updated | `20260403` | 145.1MB | amd64 | 2026-04-03” (page, “Recent Tags” table).
- Reopened page also shows dated tags `20260402`, `20251031`, `20251029`, and `20251028`, with sizes, architectures, and update dates. The current page therefore does **not** support the literal assertion “no versions”: it lists multiple version-like dated tags. The page does not list gcc or Python versions. The registry page is mutable, so it is not an immutable source for asserting the image contents or toolchain versions. Thus rejection remains justified as evidence insufficiency for claimed gcc/Python versions and mutable-page provenance, but the prior wording “no versions” is stale/overbroad and should be narrowed to “no gcc/Python version evidence.”

## Commands and observed outputs
- `read` `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` (full read): identifies C2 sourced basis as S166 and requires a reopened URL/date/≤25-word quote; no counter or probe was run.
- `read` `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` (full read): Gate row says Docker Hub API page lists tags/sizes/architectures and no gcc/Python versions; mutable tag page cannot ground claimed versions.
- `read` `https://hub.docker.com/r/alexgshaw/polyglot-c-py` returned Docker Hub API-backed page titled `alexgshaw/polyglot-c-py`, pulls 107K, last updated 2026-04-03, and the dated tags listed above.
- Scratch setup command: `mkdir -p /fast/scratch/hyaku/kengaku-r48/R48C2SourceReject && export TMPDIR=/fast/scratch/hyaku/kengaku-r48/R48C2SourceReject`; scratch removed before report completion.

Measured revision: none; no lane tree or claim was measured. No scored counter/probe execution. No tool installation/update.

Limits: Docker Hub listing is mutable and supplies tag metadata, not immutable image digests or the installed gcc/Python versions. This is a scoped source re-check only; it does not claim C2 admission or validate other C2 evidence.

VERDICT: Source rejection still follows for inability to substantiate gcc/Python versions from this mutable page; “no versions” does not follow because dated tags are present.
