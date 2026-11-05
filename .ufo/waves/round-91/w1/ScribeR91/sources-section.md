## Sources & frontier

**Admitted this round (CORPUS rule 1: each row written after its source was opened, with URL, access date and a located quote).**

- **S281** — Terminal-Bench 2.0 `modernize-scientific-stack` grader, `tests/test_outputs.py` at `2fd12b88aafdd04a52c298e3940bcb189f9766d6`. Tier A, scope `member replay only`, status `mined`; used by the round-91 lesson (`## Gate`), the C1 receipt `corpus/evidence/round91/modernize-probe.txt` and the case table `plans/round91-cases.json`. Access 2026-11-05, `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/modernize-scientific-stack/tests/test_outputs.py`, HTTP 200, 2330 B, sha256 `0c24195ff46527764c7f8ceda9c608a189ab4a01619282942fcd27a2ea02a977`, byte-identical to the round-52 capture (`corpus/evidence/round52/graders/modernize-scientific-stack/tests/test_outputs.py`). Located quote: line 27, `assert "Station 101" in output, "Must output Station 101 results"`. The scribe re-checked the captured file: `def` lines at 11 (`test_modernized_code_runs`) and 46 (`test_dependency_file_exists`) and the sha256 above [measured]. The frozen claims text cites lines 16–42 and 45–48; those ranges are wrong against the bytes (lesson M2) and are not repaired in the frozen text.

**Rejected this round.**

- **S282** — the same member's `tests/test.sh` verifier wrapper, `2fd12b88…`. Access 2026-11-05, HTTP 200, 721 B, sha256 `e868c85466ebf4815e2e4efbd252bf50ad979bceb14325a9377b1bbf852f0281`. Located quote: line 5, `apt-get install -y curl`. Rejected: a network-bound apt/uv wrapper that adds no grader semantics beyond S281, and the offline replay forbids its network legs. Flip: a claim about verifier-harness behaviour (reward mapping, uvx exit semantics) opened as its own replay with the network legs pinned.

**Registry and census.** `corpus/SOURCES.md` rows 272 → 274 (measured by counting `^| S` lines at BASE `59764383` and at the tip `a8de3e69`; the diff adds two rows). `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` exits 0 and prints `kengaku ok` at the tip [measured].

**Frontier (not admitted, routed).**

- The residual of the C1 member is the counter's L5 parser, not a source gap: the grader bytes and receipt are settled; the counter must be amended under a new frozen predicate before the member counts as executed (`corpus/lessons/round-91.md`, Routed to round 92).
- The four blind-spot anchor rows S260, S261, S265, S266 parse under the repaired QUOTE_RE and are cited, but carry no capture pin, so their quotes are not captured-checked (lesson M5). The supersede row that would add the pin is a registry edit not made this round.
- Next offline member candidates are those listed in `.ufo/waves/round-89/w1/ScoutR89/next.md` §4.2 (the `filesystem-metadata` class is now 3 of 10 and remains the thinnest); no candidate is opened or admitted in this round.
- `merge/kengaku/` stays held by L0 `kengaku | round-54`; nothing is adopted this round.
