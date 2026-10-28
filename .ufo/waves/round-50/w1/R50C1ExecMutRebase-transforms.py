"""Transform set for the round-50 C1 mutant rebase (authored against C1ExecRepair/fence_candidate.py).

Each row: an exact-once substring transform of the fence. `find`/`repl` are byte-exact source text; the
authoring tool turns each pair into a unified diff and witnesses the kill (verdict-vector change).
`class` names the axis the row mutates.
"""

TX = [
    dict(id="c1-mut-gitfile-credit-revert", cls="gitfile (n20/n21 honest credit)",
         description="Revert the `.git`-file admission: refuse any `.git` file again instead of resolving its "
                     "`gitdir:` target inside `d` and classifying the store it names.",
         effect="The honest linked-worktree (n20) and separate-gitdir (n21) fixtures lose the credit the repair "
                "gives them: their verdicts flip ADMIT->BREACH, i.e. the fence over-refuses exactly the two "
                "documented states the repair admits.",
         find='''            if name == ".git":
                target, why = _dir_ref(p, _rel(p, d), t, d, True)
                if why:
                    return None, None, why
                gitfiles.append((t, target))''',
         repl='''            if name == ".git":
                return None, None, f"{_rel(p, d)} is a file (gitdir redirect), not a directory"'''),

    dict(id="c1-mut-store-pointer-boundary-dead", cls="gitfile/worktree pointer boundary",
         description="Delete the inside-`d` test in `_pointer`, so a `gitdir:`/`commondir` pointer may name a "
                     "target anywhere on the host.",
         effect="A `.git` file or `commondir` naming a store outside `d` is followed instead of refused: the "
                "hostile out-of-`d` gitdir class flips BREACH->ADMIT (the store behind it classifies as plain).",
         find='''    if not _inside(target, d):
        return None, text, f"{label} names {text!r}, which resolves outside the fixture"''',
         repl='''    if False:
        return None, text, f"{label} names {text!r}, which resolves outside the fixture"'''),

    dict(id="c1-mut-worktree-commondir-store-unproved", cls="worktree commondir",
         description="Stop classifying the store a per-worktree `commondir` names.",
         effect="A linked worktree whose common store is hidden behind `commondir` is admitted without the "
                "common store being classified: the worktree-metadata hostile class flips BREACH->ADMIT.",
         find='''    return _store(common, f"{label}/commondir store", d, seen)''',
         repl='''    return None'''),

    dict(id="c1-mut-worktree-metadata-open", cls="worktree metadata allowlist",
         description="Drop the `WORKTREE_TOP` allowlist: any entry under a per-worktree metadata dir is "
                     "accepted.",
         effect="A worktree metadata dir carrying entries git never writes is admitted: the worktree-metadata "
                "hostile class flips BREACH->ADMIT.",
         find='''        if name not in WORKTREE_TOP:
            return f"{label}/{name} is not worktree metadata git writes"''',
         repl='''        if False:
            return f"{label}/{name} is not worktree metadata git writes"'''),

    dict(id="c1-mut-worktree-gitdir-unproved", cls="worktree gitdir back-pointer",
         description="Stop proving a per-worktree `gitdir` back-pointer (existence, symlink, link count, "
                     "inside-`d`).",
         effect="A worktree whose `gitdir` names a file outside `d`, a symlink or a dangling path is admitted: "
                "the worktree-metadata hostile class flips BREACH->ADMIT.",
         find='''    _back, why = _file_ref(p / "gitdir", f"{label}/gitdir", p, d, False)''',
         repl='''    _back, why = None, None'''),

    dict(id="c1-mut-alternates-boundary-dead", cls="alternates (n22) boundary",
         description="Delete the inside-`d` test on `objects/info/alternates` entries, keeping the per-entry "
                     "existence/symlink checks.",
         effect="An alternates file naming an object store outside `d` is admitted: the hostile alternates class "
                "flips BREACH->ADMIT while the honest in-`d` alternates fixture (n22) is unaffected.",
         find='''        if not _inside(target, d):
            return f"{label} names {text!r}, which resolves outside the fixture"''',
         repl='''        if False:
            return f"{label} names {text!r}, which resolves outside the fixture"'''),

    dict(id="c1-mut-alternates-credit-revert", cls="alternates (n22 honest credit)",
         description="Revert the alternates credit: any non-empty `objects/info` is refused again as an "
                     "object-store redirect.",
         effect="The honest `objects/info/alternates`-inside-`d` fixture (n22) flips ADMIT->BREACH while every "
                "hostile alternates module stays refused.",
         find='''                if iname != "alternates":
                    return f"{label}/info/{iname} is not git's alternates file"
                why = _alternates(q / iname, f"{label}/info/{iname}", p, d)
                if why:
                    return why''',
         repl='''                return f"{label}/info/{iname} present (object-store redirect)"'''),

    dict(id="c1-mut-fetch-head-not-allowlisted", cls="FETCH_HEAD (n18 honest credit)",
         description="Remove `FETCH_HEAD` from the store allowlist.",
         effect="The honest shallow-boundary/fetch fixture (n18) loses the credit the repair gives it and flips "
                "ADMIT->BREACH; the refusal reason becomes `FETCH_HEAD is not a plain-init entry`.",
         find='''GIT_TOP = {"HEAD", "ORIG_HEAD", "FETCH_HEAD", "COMMIT_EDITMSG", "config", "description", "hooks", "index",
           "info", "logs", "objects", "refs", "packed-refs", "worktrees"}''',
         repl='''GIT_TOP = {"HEAD", "ORIG_HEAD", "COMMIT_EDITMSG", "config", "description", "hooks", "index",
           "info", "logs", "objects", "refs", "packed-refs", "worktrees"}'''),

    dict(id="c1-mut-replace-namespace-dropped", cls="refs/replace (n17 honest credit)",
         description="Drop `replace` from the ref namespaces the fence accepts.",
         effect="The honest `refs/replace/<40-hex>` fixture (n17) flips ADMIT->BREACH: the fence refuses a "
                "ref namespace git writes.",
         find='''        if name not in GIT_REF_NAMESPACES:
            return f"{label}/{name} is not refs/heads, refs/tags or refs/replace"''',
         repl='''        if name not in {"heads", "tags"}:
            return f"{label}/{name} is not refs/heads, refs/tags or refs/replace"'''),

    dict(id="c1-mut-refs-remotes-open", cls="refs namespace",
         description="Add the other namespaces git writes (`remotes`, `stash`, `notes`, `bisect`) to the "
                     "accepted set.",
         effect="Ref namespaces the plain-init allowlist closed are re-opened; the hostile refs class flips "
                "BREACH->ADMIT if any frozen module uses one.",
         find='''        if name not in GIT_REF_NAMESPACES:
            return f"{label}/{name} is not refs/heads, refs/tags or refs/replace"''',
         repl='''        if name not in GIT_REF_NAMESPACES and name not in {"remotes", "stash", "notes", "bisect"}:
            return f"{label}/{name} is not refs/heads, refs/tags or refs/replace"'''),

    dict(id="c1-mut-config-leg-dead", cls="config",
         description="Return None from `_config` before parsing: the whole `.git/config` classification "
                     "(sections, keys, CR, non-ASCII, NUL) is skipped.",
         effect="Every config-borne escape family (include/includeIf/BOM/CR/attributesFile/excludesFile/"
                "url-rewrite/worktree/remote/user) is admitted; hostile config modules flip BREACH->ADMIT and "
                "the honest config-bearing fixtures the fence over-refuses flip to ADMIT.",
         find='''def _config(p, label):
    """Parse `.git/config` strictly. Anything the parser does not fully classify is refused."""''',
         repl='''def _config(p, label):
    """Parse `.git/config` strictly. Anything the parser does not fully classify is refused."""
    return None'''),

    dict(id="c1-mut-config-unknown-key-admitted", cls="config key allowlist",
         description="Admit a config key that is not on the `[core]`/`[extensions]` allowlist instead of "
                     "refusing it.",
         effect="Any allowlisted section may carry unlisted keys; the config-key escape family flips "
                "BREACH->ADMIT if a frozen module reaches the key check.",
         find='''        if need is None:
            return f"{label}/config key {sect}.{key} is not allowlisted"''',
         repl='''        if need is None:
            continue'''),

    dict(id="c1-mut-argv-order-shape-permuted", cls="argv shape",
         description="Permute `ORDER_SHAPE`: the `order` tool's exact option sequence is no longer the "
                     "contract's.",
         effect="Every honest `order` fixture is refused on its argv shape: ADMIT->BREACH on the whole order "
                "leg (the argv check is the first decision, so nothing downstream masks it).",
         find='''ORDER_SHAPE = ("--lane", "--claims", "--receipt")''',
         repl='''ORDER_SHAPE = ("--claims", "--lane", "--receipt")'''),

    dict(id="c1-mut-argv-inside-dead", cls="argv boundary",
         description="Delete the inside-`d` test on argv values.",
         effect="An argv value escaping `d` (`..`, absolute path) is no longer refused at the argv leg; the "
                "hostile escape is caught only if a later leg still refuses it.",
         find='''        raw = val if val.startswith("/") else os.path.join(str(d), val)
        if not _inside(raw, d):
            return None, f"{opt} value {val!r} resolves outside the fixture"''',
         repl='''        raw = val if val.startswith("/") else os.path.join(str(d), val)'''),

    dict(id="c1-mut-argv-nul-dead", cls="argv encoding",
         description="Delete the NUL test on argv values.",
         effect="An argv value carrying a NUL byte is no longer refused at the encoding leg; the hostile NUL "
                "module is caught only if a later leg still refuses it.",
         find='''        if "\\x00" in val:
            return None, f"{opt} value carries a NUL byte"''',
         repl='''        if False:
            return None, f"{opt} value carries a NUL byte"'''),

    dict(id="c1-mut-head-ref-raw-sha", cls="HEAD shape",
         description="Widen `HEAD_REF` to accept a raw 40-hex detached HEAD beside the branch ref.",
         effect="Detached-HEAD stores the plain-init allowlist refused are admitted: the detached-HEAD honest "
                "fixtures flip BREACH->ADMIT (over-refusal removed without a repair claim).",
         find='''HEAD_REF = re.compile(rb"\\Aref: refs/heads/[A-Za-z0-9_][A-Za-z0-9._/-]*\\n\\Z")''',
         repl='''HEAD_REF = re.compile(rb"\\A(?:ref: refs/heads/[A-Za-z0-9_][A-Za-z0-9._/-]*|[0-9a-f]{40})\\n\\Z")'''),

    dict(id="c1-mut-store-info-namespace-widen", cls="store info namespace",
         description="Accept any regular file under `.git/info`, not only git's `exclude`.",
         effect="A store carrying `info/refs` (or any other info entry) is admitted: the store-info over-"
                "refusal flips BREACH->ADMIT.",
         find='''            if stat.S_ISLNK(mode) or not stat.S_ISREG(mode) or name != "exclude":''',
         repl='''            if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):'''),

    dict(id="c1-mut-logs-namespace-widen", cls="reflog namespace",
         description="Widen `_log_name_ok` to any `refs/<...>` path instead of `refs/heads|tags`.",
         effect="`logs/refs/stash` and `logs/refs/notes/*` are admitted: the reflog-name over-refusal flips "
                "BREACH->ADMIT on those honest fixtures.",
         find='''    m = re.fullmatch(r"refs/(?:heads|tags)/(.+)", rel, re.ASCII)
    if not m:
        return False
    return all(SAFE_NAME.match(part) for part in m.group(1).split("/"))''',
         repl='''    m = re.fullmatch(r"refs/(?:[A-Za-z0-9._-]+/)*[A-Za-z0-9._-]+", rel, re.ASCII)
    if not m:
        return False
    return True'''),

    dict(id="c1-mut-hardlink-leg-dead", cls="hardlink",
         description="Make the multi-link test return False always: a file shared with a name outside `d` is "
                     "no longer refused.",
         effect="The hardlinked loose-object hostile module is admitted (its bytes are not provably the "
                "fixture's): BREACH->ADMIT with the refusal reason gone.",
         find='''def _linked(mode, nlink):
    """A regular file with another name somewhere is not provably inside `d`: refuse it."""
    return stat.S_ISREG(mode) and nlink > 1''',
         repl='''def _linked(mode, nlink):
    """A regular file with another name somewhere is not provably inside `d`: refuse it."""
    return False'''),

    dict(id="c1-mut-tree-file-symlink-dead", cls="symlink (tree)",
         description="Delete the file-level symlink test in the tree walk.",
         effect="A regular-file entry that is a symlink inside the fixture is no longer refused at the tree "
                "leg; the hostile symlink class is admitted if no later leg refuses it.",
         find='''            if stat.S_ISLNK(mode):
                return None, None, f"{_rel(p, d)} is a symlink"
            if not stat.S_ISREG(mode):
                return None, None, f"{_rel(p, d)} is a special file"''',
         repl='''            if not stat.S_ISREG(mode):
                return None, None, f"{_rel(p, d)} is a special file"'''),

    dict(id="c1-mut-store-entry-symlink-dead", cls="symlink (store)",
         description="Delete the per-entry symlink test in `_store`, so `.git/<dir>` may itself be a symlink.",
         effect="`.git/objects` (or `refs`) as a symlink is no longer refused at the store leg; the hostile "
                "symlinked-objects class is admitted if no later leg refuses it.",
         find='''    for name, mode, size, n in ents:
        q = gd / name
        if stat.S_ISLNK(mode):
            return f"{label}/{name} is a symlink"
        if name not in GIT_TOP:''',
         repl='''    for name, mode, size, n in ents:
        q = gd / name
        if name not in GIT_TOP:'''),

    dict(id="c1-mut-entry-cap-shrink", cls="tree cap",
         description="Shrink `ENTRY_CAP` 200000 -> 40.",
         effect="Every honest fixture with more than 40 walked entries is refused as pathological: "
                "ADMIT->BREACH on the larger batteries (the cap is load-bearing for legitimate fixtures).",
         find='''ENTRY_CAP = 200000''',
         repl='''ENTRY_CAP = 40'''),

    dict(id="c1-mut-lane-membership-dead", cls="argv lane membership",
         description="Stop requiring `--lane` to name a collected repository inside the fixture.",
         effect="A fixture whose `--lane` names a directory above/outside the collected repos is admitted: the "
                "hostile above-`d` lane class flips BREACH->ADMIT.",
         find='''    if _norm(lane) not in {_norm(r) for r in repos} | {_norm(r) for r, _t in gitfiles}:''',
         repl='''    if False:'''),

    dict(id="c1-mut-inside-dead", cls="boundary property (global)",
         description="Make `_inside` return True unconditionally: every lexical inside-`d` proof in the fence "
                     "is dead at once.",
         effect="All path-boundary refusals (gitdir, commondir, alternates, argv, lane) disappear together: "
                "the whole hostile boundary family flips BREACH->ADMIT.",
         find='''def _inside(p, d):
    p, d = _norm(p), _norm(d)
    return p == d or p.startswith(d + os.sep)''',
         repl='''def _inside(p, d):
    p, d = _norm(p), _norm(d)
    return True'''),

    dict(id="c1-mut-gitfile-commondir-branch-dropped", cls="gitfile (n20 worktree shape)",
         description="Classify a `.git`-file target only as a store; never as per-worktree metadata carrying "
                     "`commondir`.",
         effect="The honest linked-worktree fixture (n20) flips ADMIT->BREACH: its target is a metadata dir "
                "whose `commondir` is not a plain-init entry.",
         find='''    if "commondir" in {name for name, _m, _s, _n in ents}:
        return _worktree(target, label, d, seen)
    return _store(target, label, d, seen)''',
         repl='''    return _store(target, label, d, seen)'''),

    dict(id="c1-mut-mount-check-added", cls="mount boundary",
         description="Add a device-boundary test the fence does not have: any walked entry whose `st_dev` "
                     "differs from the fixture dir's is refused.",
         effect="Intended direction: a fixture containing a mount crossing is refused. Measured direction: the "
                "frozen population holds no cross-device fixture and every fixture is built on one device, so "
                "the verdict vector cannot change -- the mount axis is unexercised by this population.",
         find='''        for name in files:
            p = t / name
            try:
                mode = os.lstat(p).st_mode''',
         repl='''        for name in files:
            p = t / name
            try:
                mode = os.lstat(p).st_mode
                if os.lstat(str(d)).st_dev != os.lstat(p).st_dev:
                    return None, None, f"{_rel(p, d)} crosses a mount boundary"'''),

    dict(id="c1-mut-objects-info-namespace-widen", cls="store info namespace (objects)",
         description="Accept any name under `.git/objects/info` instead of only git's `alternates`.",
         effect="A store carrying `objects/info/commit-graph` (git writes it) is admitted: the info/ over-"
                "refusal flips BREACH->ADMIT on the honest commit-graph fixture.",
         find='''                if iname != "alternates":
                    return f"{label}/info/{iname} is not git's alternates file"''',
         repl='''                if iname != "alternates":
                    continue'''),

    dict(id="c1-mut-config-bare-any-value", cls="config value",
         description="Stop requiring `core.bare` (and any must-be-false key) to be falsey.",
         effect="A store whose config declares `core.bare = true` is admitted: the hostel bare-repo class "
                "flips BREACH->ADMIT.",
         find='''        elif need == "false":
            if val not in FALSEY:
                return f"{label}/config {sect}.{key} must be false"''',
         repl='''        elif need == "false":
            if False:
                return f"{label}/config {sect}.{key} must be false"'''),

    dict(id="c1-mut-index-cap-shrink", cls="cap (index)",
         description="Shrink `INDEX_CAP` 1<<24 -> 1 byte.",
         effect="Every honest fixture with a `.git/index` (all of the battery) is refused: ADMIT->BREACH on "
                "the whole population, i.e. the index cap is load-bearing.",
         find='''INDEX_CAP = 1 << 24         # a `.git/index` larger than this is refused''',
         repl='''INDEX_CAP = 1              # a `.git/index` larger than this is refused'''),

    dict(id="c1-mut-anchor-opts-narrow", cls="argv options",
         description="Drop `--verbose` from the anchor tool's accepted option set.",
         effect="Every honest anchor fixture whose argv carries `--verbose` is refused on its argv shape: "
                "ADMIT->BREACH on that leg.",
         find='''ANCHOR_OPTS = {"--lane": True, "--evidence-ref": True, "--verbose": False}''',
         repl='''ANCHOR_OPTS = {"--lane": True, "--evidence-ref": True}'''),

    dict(id="c1-mut-repo-cap-zero", cls="cap (repos)",
         description="Shrink `REPO_CAP` 64 -> 0.",
         effect="Any fixture holding a repository is refused as pathological: ADMIT->BREACH on every honest "
                "fixture with a repo.",
         find='''REPO_CAP = 64               # collected repos before the fixture is refused as pathological''',
         repl='''REPO_CAP = 0                # collected repos before the fixture is refused as pathological'''),

    dict(id="c1-mut-gitdir-target-symlink-dead", cls="symlink (gitdir target)",
         description="Delete the symlink test on a `gitdir:` target directory in `_dir_ref`.",
         effect="A `.git` file naming a symlinked directory is followed instead of refused; the hostile "
                "symlinked-gitdir class flips BREACH->ADMIT if the target store classifies as plain.",
         find='''    if stat.S_ISLNK(st.st_mode):
        return None, f"{label} names {text!r}, which is a symlink"
    if not stat.S_ISDIR(st.st_mode):''',
         repl='''    if not stat.S_ISDIR(st.st_mode):'''),

    dict(id="c1-mut-objects-entry-symlink-dead", cls="symlink (objects entry)",
         description="Delete the symlink test on entries of `.git/objects` in `_objects`.",
         effect="An `objects/<xx>`, `objects/info` or `objects/pack` entry that is a symlink is followed "
                "instead of refused: the hostile symlinked-objects class flips BREACH->ADMIT if the target "
                "classifies as plain.",
         find='''    for name, mode, _s, _n in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{_rel(q, label)} is a symlink"
        if not stat.S_ISDIR(mode):
            return f"{label}/{name} is not a directory"''',
         repl='''    for name, mode, _s, _n in ents:
        q = p / name
        if not stat.S_ISDIR(mode):
            return f"{label}/{name} is not a directory"'''),

    dict(id="c1-mut-store-dir-symlink-open", cls="symlink (store entry, dir)",
         description="Delete the symlink test in `_store` AND the is-a-directory test for the allowlisted "
                     "directories, so `.git/objects` or `.git/refs` may itself be a symlink.",
         effect="A store whose `objects` (or `refs`) is a symlink to a directory outside `d` is followed and "
                "classified by content instead of refused at the leg: the hostile symlinked-objects class "
                "flips BREACH->ADMIT.",
         find='''    for name, mode, size, n in ents:
        q = gd / name
        if stat.S_ISLNK(mode):
            return f"{label}/{name} is a symlink"
        if name not in GIT_TOP:
            return f"{label}/{name} is not a plain-init entry"
        have.add(name)
        if name in GIT_DIRS:
            if not stat.S_ISDIR(mode):
                return f"{label}/{name} is not a directory"
            continue''',
         repl='''    for name, mode, size, n in ents:
        q = gd / name
        if name not in GIT_TOP:
            return f"{label}/{name} is not a plain-init entry"
        have.add(name)
        if name in GIT_DIRS:
            continue'''),

    dict(id="c1-mut-tree-dir-symlink-open", cls="symlink (tree dir)",
         description="Delete the symlink test in the tree walk's directory loop AND the is-a-directory test, "
                     "so a `.git` that is a symlink to a directory is collected as a repository.",
         effect="A worktree whose `.git` is a symlink to a store is treated as a repository and the store is "
                "classified by content instead of refused at the tree leg.",
         find='''            if stat.S_ISLNK(mode):
                return None, None, f"{_rel(p, d)} is a symlink"
            if not stat.S_ISDIR(mode):
                return None, None, f"{_rel(p, d)} is not a directory"
            if name == ".git":''',
         repl='''            if not stat.S_ISDIR(mode) and not stat.S_ISLNK(mode):
                return None, None, f"{_rel(p, d)} is not a directory"
            if name == ".git":'''),
]
