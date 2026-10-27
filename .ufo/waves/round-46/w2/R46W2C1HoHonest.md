# R46W2C1HoHonest — over-refusal check

Axis: calibration (honest-novel acceptance vs refusal). The nine new honest fixture builds cover packed refs after `gc`/`pack-refs`, annotated tags, detached HEAD, a merge commit, `.gitignore`, a 30-commit linear history, reflog gc, annotated-tag-plus-detached-HEAD, and an ignored untracked file. Each is a plain `git init` repository built by the round-44 C1 builder contract; all nine are newly named modules in the counter's `--sealed` override and produced a `SEALED ... clean fixtures=1 admitted=0 hung=0 touches=0` rollup. Thus **9/9 were refused**, with no outside touches. That behavior is not a valid honest refusal: the fence is designed to refuse hostile fixtures, not ordinary repository states.

Evidence and limits:
- Clean clone HEAD was verified as `42d5043afac952fcb43bf4798757785dd258cf85`; top-level was `/fast/scratch/hyaku/kengaku-r46/R46W2C1HoHonest/lane`.
- Counter executed through the required envelope with `--sealed <override>` and `--work "$S"`. Envelope output: `ENVELOPE start 02:47:04 cwd=/home/vgpnk/Projects/shokunin` (run command is in receipt); final line: `ENVELOPE end 02:47:18 exit=1 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged`.
- Receipt: `receipts/c1-counter-override.txt`. Its conclusion lines: `SEALED total=21 clean=21 leaked=0 read=0 hung=0 build_errors=0`; `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`; `CALIBRATION advertised=41 contradicted=0`; `PREDICATE C1 fail`. The fail is expected for this override because adding nine modules violates the counter's frozen exact SEALED total of 12. Consequently this is a direct fence behavior probe, not a passing/frozen C1 run; do not interpret the override predicate as the pinned result.
- The nine fixture builds themselves are auditable in the isolated scratch clone's temporary override, but only the counter output was retained as receipt. No lane files changed.

VERDICT: honest-novel-9-refused-9
