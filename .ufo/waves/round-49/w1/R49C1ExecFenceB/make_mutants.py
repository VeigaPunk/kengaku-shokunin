#!/usr/bin/env python3
"""Generate the C1 mutant battery for the variant-B fence.

Each mutant is one textual weakening of `fence_b.py` at a named kind-classification guard; each entry names the
fixtures whose observed verdict must change if that guard is doing work. Written for the dev harness MUTANTS leg
(seat R49C1ExecFenceB). No lane file is touched.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "fence_b.py"
OUT = HERE / "mutants"

# (name, note, [(old, new)] , targets)
MUTANTS = [
    ("m01_objects_redirect_unguarded", "objects/: the store may be redirected out (symlink + dir kind and the "
     "object-info name kind are dropped) - the redirect class is admitted or traced",
     [('''    for name, mode, _s, _n in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{_rel(q, label)} is a symlink"
        if not stat.S_ISDIR(mode):
            return f"{label}/{name} is not a directory"
        if name == "info":''',
       '''    for name, mode, _s, _n in ents:
        q = p / name
        if name == "info":'''),
      ('''        if not stat.S_ISREG(mode) or not GRAPH_FILE.match(name):
            return f"{_rel(q, label)} is not an object-info kind the fence classifies"
''', "")],
     ["p_info_redirect", "s_objects_link", "p_pack_redirect"]),
    ("m02_objects_hardlink_off", "objects/: the multiply-linked loose object refusal is dropped",
     [('''            if _linked(omode, _on):
                return f"{_rel(qq, label)} has more than one hard link"''', "")],
     ["f16_objects_hardlink_out"]),
    ("m03_config_path_kind_off", "config: path-kind keys are classified as inert scalars (no inside-d proof)",
     [('''        pathy = (kind == "core" and key in CORE_PATH_KEYS) or key.endswith(PATH_SUFFIXES)''',
       '''        pathy = False''')],
     ["f20_attributes_file", "c_core_attributes_path", "c_excludes_file", "f2_deep"]),
    ("m04_store_redirect_unguarded", "store top level: symlink redirects are followed (refs, packed-refs and "
     "objects may live outside d)",
     [('''        if stat.S_ISLNK(mode):
            return f"{label}/{name} is a symlink"
        kind = STORE_KINDS.get(name)''',
       '''        kind = STORE_KINDS.get(name)'''),
      ('''        if kind == "dir":
            if not stat.S_ISDIR(mode):
                return f"{label}/{name} is not a directory"
            continue
        if not stat.S_ISREG(mode):
            return f"{label}/{name} is not a regular file"''',
       '''        if kind == "dir":
            continue''')],
     ["s_packed_refs", "p_refs_redirect", "s_refs_link", "s_objects_link"]),
    ("m05_config_path_absolute", "config: path-kind values are accepted absolute (an outside reader is allowed)",
     [('''    if not val or val.startswith("/") or val.startswith("~") or "\\x00" in val:
        return False
    if any(part in ("..", "") for part in val.split("/")):
        return False
    target = os.path.join(str(repo), val)
    try:
        st = os.lstat(target)
    except OSError:
        return True                      # names nothing the fence could read
    return not stat.S_ISLNK(st.st_mode)''',
       '''    return bool(val) and "\\x00" not in val''')],
     ["f20_attributes_file", "c_core_attributes_path", "c_excludes_file"]),
    ("m06_config_url_scalar", "config: the [url] section kind is treated as inert scalars (insteadOf admitted)",
     [('REDIRECT_SECTIONS = {"include", "includeif", "url"}', 'REDIRECT_SECTIONS = {"include", "includeif"}')],
     ["c_url_rewrite"]),
    ("m07_lane_membership_off", "decision: --lane need not name a collected repository (plain dir admitted)",
     [('''    if _norm(lane) not in {_norm(r) for r in repos}:
        return f"--lane {lane_tok!r} is not a repository inside the fixture"
''', "")],
     ["f6_above", "a_phantom_order"]),
    ("m08_refs_namespace_allowlist", "refs: namespace allowlist restored (heads/tags only) - over-refusal kind",
     [('''        if not REF_COMP.match(name) or name.endswith(".lock"):
            return f"{_rel(q, label)} is not a refname component"''',
       '''        if name not in ("heads", "tags"):
            return f"{_rel(q, label)} is not a refname component"''')],
     ["n14_stash_entry", "n16_notes_ref"]),
    ("m09_noncore_sections_refused", "config: any section that is not core/extensions is unclassified",
     [('''    return "scalar"''', '''    return None''')],
     ["n12_local_config_user", "n13_remote_origin"]),
    ("m10_detached_head_refused", "store: HEAD must be symbolic (a detached HEAD is refused)",
     [('''            elif not HEX40.match(body):
                return f"{label}/HEAD is neither symbolic nor a detached 40-hex id"''',
       '''            else:
                return f"{label}/HEAD is not a plain symbolic HEAD"''')],
     ["n03_detached_head", "n08_tag_detached"]),
    ("m11_objects_info_refused", "objects/info: every entry is refused (pre-repair behaviour)",
     [('''    any other name is refused."""
    ents = _entries(p)''',
       '''    any other name is refused."""
    return f"{label} present (object-store info refused)"
    ents = _entries(p)''')],
     ["n15_commit_graph", "n07_reflog_gc"]),
    ("m12_info_refs_refused", "info/: git's `refs` list is refused (only `exclude` classified)",
     [('''        if name == "refs":
            why = _info_refs(q, f"{label}/refs")
            if why:
                return why
            continue''',
       '''        if name == "refs":
            return f"{_rel(q, label)} is not git's exclude file"''')],
     ["n07_reflog_gc"]),
    ("m13_argv_shape_off", "argv: the exact option-shape check is dropped (abbreviations admitted)",
     [('''    if tool == "order":
        if len(argv) != 6 or tuple(argv[0::2]) != ORDER_SHAPE:
            return None, f"order argv is not the contract shape {list(ORDER_SHAPE)}"
        vals = dict(zip(argv[0::2], argv[1::2]))''',
       '''    if tool == "order":
        vals = dict(zip(argv[0::2], argv[1::2]))''')],
     ["f3_abbrev"]),
]


def main():
    src = SRC.read_text()
    OUT.mkdir(exist_ok=True)
    index = []
    for name, note, subs, targets in MUTANTS:
        text = src
        for old, new in subs:
            if text.count(old) != 1:
                print(f"FAIL {name}: anchor count={text.count(old)}", file=sys.stderr)
                return 2
            text = text.replace(old, new)
        path = OUT / f"{name}.py"
        path.write_text(text)
        index.append({"file": name, "path": str(path), "targets": targets, "note": note})
        print(f"MUTANT-WRITTEN {name} bytes={len(text)} targets={','.join(targets)}")
    (OUT / "index.json").write_text(json.dumps(index, indent=1) + "\n")
    print(f"INDEX {OUT / 'index.json'} total={len(index)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
