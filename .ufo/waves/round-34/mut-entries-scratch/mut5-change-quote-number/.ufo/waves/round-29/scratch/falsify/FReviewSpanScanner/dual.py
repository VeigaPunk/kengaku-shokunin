"""Dual-version verification of scanner/provenance findings.

Runs the same battery against:
  A) contract target  = lane master 56fd949a plans/config_projection.py
  B) live worktree copy (sha a91f3943..., edited 2026-10-21T14:16 local)
Both are byte snapshots under this agent's scratch dir. No production file is touched.
"""
import importlib.util
import json
import subprocess
import sys

HERE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FReviewSpanScanner"
VERSIONS = {"A_master_56fd949a": HERE + "/target_master.py", "B_worktree_a91f3943": HERE + "/target_worktree.py"}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def battery(cp):
    out = {}

    # F1: template() on a path whose FIRST element after path[0] is an int
    try:
        out["F1_template_int_first"] = repr(cp.template((0, 0)))
    except Exception as e:
        out["F1_template_int_first"] = "EXC %s: %s" % (type(e).__name__, e)

    # F1b: provenance() over a valid-JSON root array-of-arrays
    raw = '[["__MAP__"]]'
    try:
        recs = cp.provenance(raw, cp.string_spans(raw))
        out["F1b_provenance_array_of_arrays"] = json.dumps(recs)
    except Exception as e:
        out["F1b_provenance_array_of_arrays"] = "EXC %s: %s" % (type(e).__name__, e)

    # F2: two sibling keys carrying the same token -> distinguishable location?
    raw2 = '[{"a__MAP__":1,"b__MAP__":2}]'
    recs2 = cp.provenance(raw2, cp.string_spans(raw2))
    out["F2_sibling_keys"] = json.dumps([(r["string_role"], r["json_pointer"], r["path_template"], r["task_index"]) for r in recs2])

    # F2b: does a key-role json_pointer resolve to the string holding the token?
    raw3 = '[{"sites":[{"__MAP__":1}]}]'
    recs3 = cp.provenance(raw3, cp.string_spans(raw3))
    out["F2b_key_role_nested"] = json.dumps([(r["string_role"], r["json_pointer"], r["path_template"], r["task_index"]) for r in recs3])

    # F3: task_index type at root-object level
    raw4 = '{"__MAP__":1}'
    recs4 = cp.provenance(raw4, cp.string_spans(raw4))
    out["F3_root_object_task_index"] = json.dumps([(r["task_index"], type(r["task_index"]).__name__) for r in recs4])

    # F4: pointer() for the empty path (RFC 6901: "" is whole doc, "/" is the ""-named member)
    out["F4_pointer_empty_path"] = repr(cp.pointer(()))
    out["F4_pointer_root_element"] = repr(cp.pointer((0,)))

    # F5: NaN / Infinity handling in string_spans
    for lit in ("[NaN]", "[Infinity]", "[-Infinity]"):
        try:
            cp.string_spans(lit)
            out["F5_string_spans" + lit] = "OK"
        except Exception as e:
            out["F5_string_spans" + lit] = "EXC %s: %s" % (type(e).__name__, e)

    # F6: spans strictly increasing / non-overlapping on a nested+escaped document
    doc = '{"a\\"b":[1,{"c":"d"}],"e":{"f":[{"g":1}]}}'
    sp = cp.string_spans(doc)
    starts = [s[0] for s in sp]
    out["F6_strictly_increasing"] = all(starts[i] < starts[i + 1] for i in range(len(starts) - 1))
    out["F6_non_overlapping"] = all(sp[i][1] <= sp[i + 1][0] for i in range(len(sp) - 1))

    # F7: key-span path convention (parent path) vs value-span path
    out["F7_spans_dict_root"] = json.dumps(cp.string_spans('{"k":{"v":1}}'))

    # F8: trailing-garbage tolerance depends on `assert end == length`
    try:
        out["F8_trailing_garbage"] = repr(cp.string_spans('{"a":1} XX'))
    except Exception as e:
        out["F8_trailing_garbage"] = "EXC %s: %s" % (type(e).__name__, e)

    return out


for name, path in VERSIONS.items():
    print("=" * 78)
    print("VERSION", name, path)
    cp = load(path, "cp_" + name)
    res = battery(cp)
    for k in sorted(res):
        print("  %-38s %s" % (k, res[k]))
    # -O behaviour of the CLI entry point
    for flags in ([], ["-O"]):
        r = subprocess.run([sys.executable] + flags + [path, "--root", "/home/vgpnk/Projects/shokunin/kengaku-shokunin", "--summary"],
                           capture_output=True, text=True, cwd=HERE)
        tail = [l for l in r.stdout.splitlines() if l.startswith("FINDING") or l.startswith("SELFTEST")][:1]
        print("  CLI flags=%-6r rc=%d out=%s stderr_tail=%r" % (flags, r.returncode, tail, r.stderr.strip()[-120:]))
