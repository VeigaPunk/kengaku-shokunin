# R48C2ScribeGate — round-48 lesson `## Gate` block draft (C2 sourced basis)

**Axis named:** coverage (R48-C2). **Seat:** scribe. **Item:** draft the round-48 lesson `Gate` block — S166
reopened this round (URL, access date, ≤25-word located quote from the pinned `test_outputs.py`) plus one reject
(the Docker Hub mutable tag page, r46 reason re-checked). Lane corpus was **not** edited: the block below is a
draft for the L1 (`KengakuR48`) to land.

**REV `a543d92083557dd9b33ee674e9b99b03411f80af`** (stage-1 freeze, verified in the committed lane tree) —
**REV `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767`** (lane tip read; `corpus/` and `plans/` byte-identical to
the freeze — `git diff --stat a543d920..HEAD -- corpus plans` printed nothing).

**Landing note:** the round-48 lesson already carries the placeholder `## Gate` → `(filled at integration)` at
`corpus/lessons/round-48.md:12-14` (untracked at read time). The block below replaces that one line; the heading
stays. This seat did not touch the file.

**No scored counter or probe was run.** Per C2 ordering (claims §Ordering), no probe of the C2 package may run
before the stage-2 commit, and stage 2 is not committed (`git log a543d920..HEAD` = `453ddfd`, `bf783c1`, both
dispatch/handoff bookkeeping; no round-48 `stage-2` commit exists). Nothing this seat observed is a counter
receipt.

---

## Draft block (for `corpus/lessons/round-48*.md`; not landed here)

```markdown
## Gate

Reopened or re-checked this round by seat `R48C2ScribeGate` (scribe) for the C2 sourced basis (claims §2b), access
date 2026-10-27 (times -03), against the stage-1 freeze `a543d92083557dd9b33ee674e9b99b03411f80af`
(2026-10-27T06:53:29-03:00) and before any stage-2 pin and any probe run. S166 was fetched fresh at the pin: the
bytes are `cmp`-identical to the committed capture `corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py`,
sha256 `b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec` (the digest in `SHA256SUMS` line 8 and
in the S166 row). Base URL
`https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/`.

| candidate | verdict | reason + flip | URL | accessed | located quote |
|---|---|---|---|---|---|
| `tests/test_outputs.py` (S166) | ACCEPT (reopened; verdict unchanged) | the executed predicate itself; the reopened bytes are the pinned bytes (digest equal), and `:44` is the line that grades *both* runtimes against one literal — the ground of the `both-print` tag whose missing violating case is the r46 V7 defect. Flips to reject on any digest change at the pin | `…2fd12b88…/polyglot-c-py/tests/test_outputs.py` | 2026-10-27 | `:44 "assert python_out == expected and c_out == expected, ("` (9 words) |
| Docker Hub tag page `alexgshaw/polyglot-c-py` | **REJECT** (re-checked; reason holds, flip sharpened) | the page states no gcc or CPython version and its tags are mutable date tags, so it cannot evidence the toolchain the task promises. Re-checked 2026-10-27: the tags API lists 5 tags, all date-named (`20260403`, `20260402`, `20251031`, `20251029`, `20251028`), with no version field on any tag or image record; the hydrated page contains 0 occurrences of `python` and no gcc version string (its three `gcc` matches are JS asset names, `gccoq32s.js`). The digest r46 recorded (`sha256:43f9d558…`, 152153707 B) now binds the two newest tags, **not** the tag `task.toml:29` names (`alexgshaw/polyglot-c-py:20251031` → `sha256:0f1c3b78…`, 148540671 B), and the version is in any case decided at build time by `Dockerfile:6 "RUN apt update -y && apt install -y gcc"` on `Dockerfile:2 "FROM ubuntu:24.04"`. Flip: a digest-pinned manifest inspection at the digest of the tag `task.toml:29` names, listing the installed gcc and CPython versions | https://hub.docker.com/r/alexgshaw/polyglot-c-py | 2026-10-27 | no document text; nearest tokens in the hydrated page: `"digest","sha256:43f9d55805dfcfaeb7875c620b9313bde9cd263a2d75362d730710c935dc4c04"` and `"name":"20251031"`,`"digest":"sha256:0f1c3b7816d70cf5551573fd6aeef76893f2ae3000be2419997b6871b5d987ed"` (tags API) |

`…2fd12b88…` abbreviates `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6`.
```

---

## Exact commands run and observed outputs

All read-only. Scratch root `/fast/scratch/hyaku/kengaku-r48/R48C2ScribeGate` (`TMPDIR` exported there); no
fixture git store, no clone, no lane write.

1. **Freeze exists and predates this measurement.**
   `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t a543d92083557dd9b33ee674e9b99b03411f80af`
   → `commit`; `git log -1 --format='%H%n%an <%ae>%n%cI%n%s'` on it →

   ```
   a543d92083557dd9b33ee674e9b99b03411f80af
   kengaku-shokunin <kengaku@shokunin.local>
   2026-10-27T06:53:29-03:00
   round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter) claims
   ```

   `git rev-parse HEAD` → `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767`. Measurement clock `date '+%Y-%m-%d %H:%M:%S %z'`
   → `2026-10-27 08:32:42 -0300`. Freeze precedes every read below.

2. **Freeze-consistent reads.** `git diff --name-only a543d920..HEAD` → only
   `.ufo/waves/round-48/{build_spec.py,w1-dispatch.json,w1-spec.json,w1-validate.err,w1.ready}`;
   `git diff --stat a543d920..HEAD -- corpus plans` → empty. So `corpus/` and `plans/` read at the tip are the
   frozen bytes.

3. **S166 reopened at the pin.**
   `curl -sS -w 'HTTP %{http_code}' -o test_outputs.py "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py"`
   → `HTTP 200`; `sha256sum test_outputs.py` → `b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec`
   (46 lines). Lane capture digest identical, and
   `cmp -s corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py <fetch>` → identical (`CMP-IDENTICAL`).

   Byte-exact lines read back from the fetch (`repr`, line numbers as in the file):

   ```
   17 '    polyglot_files = os.listdir("/app/polyglot")'
   18 '    assert polyglot_files == ["main.py.c"], ('
   24 '        ["gcc", "/app/polyglot/main.py.c", "-o", "/app/polyglot/cmain"], check=True'
   27 '    test_cases = [(42, "267914296"), (10, "55"), (0, "0")]'
   44 '        assert python_out == expected and c_out == expected, ('
   ```

   Quote used in the draft: `assert python_out == expected and c_out == expected, (` — 9 words,
   `in line 44` → `True`.

4. **Reject re-checked.**
   `curl -sS -o hub-page.html "https://hub.docker.com/r/alexgshaw/polyglot-c-py"` → `HTTP 200`, 285281 bytes,
   sha256 `4b85c86e58a465d052d212aa2de509cc9585145671b871687bb584936cf73c1f`.
   `curl -sS -o hub-api.json "https://hub.docker.com/v2/repositories/alexgshaw/polyglot-c-py/tags?page_size=25"`
   → `HTTP 200`, 4175 bytes, sha256 `c7d7024d8de171fe44e3edb972d1c2bd7a6ee85bbf376ca4f96019403683589d`.

   Tags API (`count` 5), verbatim fields:

   ```
   20260403  last_updated 2026-04-03T08:31:47.9721Z  digest sha256:43f9d55805dfc…  full_size 152153707  amd64
   20260402  last_updated 2026-04-03T07:51:55.972518Z digest sha256:43f9d55805dfc…  full_size 152153707  amd64
   20251031  last_updated 2025-10-31T02:56:02.045378Z digest sha256:0f1c3b7816d70c…  full_size 148540671  amd64
   20251029  last_updated 2025-10-29T00:48:45.374715Z digest sha256:0f1c3b7816d70c…  full_size 148540671  amd64
   20251028  last_updated 2025-10-28T22:06:38.956029Z digest sha256:7bfc968f7487ab…  full_size 148540671  amd64
   ```

   Tag-record keys: `content_type, creator, digest, full_size, id, images, last_updated, last_updater,
   last_updater_username, media_type, name, repository, tag_last_pulled, tag_last_pushed, tag_status, v2`;
   image-record keys: `architecture, digest, features, last_pulled, last_pushed, os, os_features, os_version, size,
   status, variant`. No `version`-named field on either record (`no version fields: []`).

   Hydrated page: `grep -c -i python hub-page.html` → `0`; the three `gcc` matches are asset paths, e.g.
   `https://dockerstatic.com/hub-ui/gccoq32s.js` — no toolchain version string. Digest tokens present in the page:
   `sha256:43f9d558…dc4c04`, `sha256:0f1c3b78…dc987ed`, `sha256:7bfc968f…16c2e65`.

   The task's own tag: `corpus/evidence/round46/tb2-polyglot-c-py/task.toml:29` →
   `docker_image = "alexgshaw/polyglot-c-py:20251031"`; `Dockerfile:2` → `FROM ubuntu:24.04`; `Dockerfile:6` →
   `RUN apt update -y && apt install -y gcc`.

   Verdict on the r46 reason: **holds**. Both halves re-checked true — no gcc/CPython version is stated anywhere
   on the page or tag API, and the tag reference is a mutable date tag (`tag_status: active`, `last_updated` a
   push time per tag). One refinement, reported for the L1's decision and touching no claim predicate, control or
   kill rule: the r46 flip named the digest `sha256:43f9d558…`, which today binds `20260403`/`20260402`, while the
   task's tag `20251031` binds `sha256:0f1c3b78…` — the flip is only useful if it names the digest of the tag the
   task actually cites.

## Limits

- No scored counter (`round48_c2_verify.py` / `round46_c3_verify.py`) and no probe (`polyglot_c_py_probe.py`)
  was executed; stage 2 is uncommitted, so the C2 ordering forbids it. This report contains **no C2 admission or
  rejection evidence** — only Gate provenance.
- No clone at the frozen base was created. Equivalence was established by `git diff --stat a543d920..HEAD --
  corpus plans` (empty) over the read-only lane checkout; the seat read no writable path in the lane. If the L1
  wants a clone-based REV, the same three commands above reproduce at `a543d920`.
- The Docker Hub observation is a snapshot: tag→digest mappings are mutable by construction, so the recorded
  digests (`4b85c86e…`, `c7d7024d…`) are the comparison anchors for a re-check, not a durable claim about tags.
- The ≤25-word quote is one line of the pinned file; the block does not re-argue the class (already worded in the
  round-46 entry) and does not speak to C1.
- `hub-page.html` (285 KB) and `hub-api.json` lived only in scratch and were removed after their values were
  transcribed above; no scratch path is cited as evidence. No tool was installed or updated.

## Findings

1. **S166 is reopenable and byte-stable at the pin** — fresh `HTTP 200`, digest equal to the committed capture and
   to `SHA256SUMS` line 8; freeze `a543d920` predates the fetch. The Gate's admit row needs no re-wording.
2. **The Docker Hub reject survives its re-check**, and the page additionally cannot ground the tag the task
   cites (`20251031` → `sha256:0f1c3b78…`), so the r46 flip digest should be corrected to that tag's digest if
   the L1 lands a flip sentence.
3. **Gate-block ordering is clean** for the lesson: the block is written after the stage-1 freeze and before stage
   2, so it cannot be read as a post-hoc justification of a measurement.
4. **Defect of my own run:** none outstanding — the scratch dir was removed after transcription (see Limits for
   why no separate receipt file was placed in the wave dir: seat write scope is this report file only).

**VERDICT:** Gate block drafted for the L1 — S166 ACCEPT (reopened, digest-verified, `:44`, 9-word quote) and
Docker Hub `alexgshaw/polyglot-c-py` REJECT (reason re-checked, flip digest refined). No scored run, no claim
admission, lane corpus untouched.
