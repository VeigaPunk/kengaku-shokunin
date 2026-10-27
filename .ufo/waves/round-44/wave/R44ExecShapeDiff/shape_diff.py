#!/usr/bin/env python3
"""shape_diff — the non-author 're-spelling' screen for a battery against the freeze direction module.

The C1 counter (plans/round44_c1_verify.py) can see whether a battery kills a mutant; it cannot see whether a
fixture is merely the witness fixture re-spelled. This tool answers only that question, mechanically, without
reading intent:

  * the witness module is inventoried statically: every module-level function, marked `fixture` when a
    `FIXTURES` entry's `build` names it (list aliases such as `FIXTURES_ROWS` and a filtering list comprehension
    are resolved statically, so a table assembled from parts still yields exactly its fixtures) and `helper`
    otherwise;
  * every battery module is inventoried the same way;
  * similarity = difflib.SequenceMatcher ratio over token sequences of `ast.dump`, with the tree normalised
    first: local names, parameter names and function names all become `_`; every constant becomes a type marker
    (`<S>` str, `<B>` bytes, `<N>` number, `<C>` other); docstrings are dropped; attribute names survive
    (`_.write`, `_.sha256`), because the ctx/API surface is the shape under test;
  * a pair is ENFORCED when both sides are fixtures (the screen's subject: every battery fixture against every
    witness fixture). Any pair that involves a helper on either side is ADVISORY: shared plumbing ("| " + join, a
    repo-with-two-commits builder) is contextual evidence, not a re-spelled fixture. Enforced pairs above
    `--threshold` (default 0.8) are flagged and make the exit status 1; advisory pairs are always printed.

Nothing here executes, imports or writes: the battery and the witness are read as text and parsed with ast, so
the tool cannot build a fixture, run a tool or touch a git repository.

usage:
  shape_diff.py --battery DIR_OR_FILE --witness FILE [--threshold 0.8] [--all] [--json] [--quiet]
  shape_diff.py --selftest [--witness FILE] [--control DIR] [--threshold 0.8]

selftest: the witness against itself (every fixture must flag its own self-pair at 1.0; its off-diagonal
near-variants are printed as informational) and against the control battery (no enforced pair may flag), then
`SELFTEST RESULT pass|fail` with exit 0|1.
"""
from __future__ import annotations

import argparse
import ast
import copy
import difflib
import json
import re
import sys
from pathlib import Path

DEFAULT_WITNESS = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/claims/witness/w_u.py"
DEFAULT_CONTROL = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/battery43"
DEFAULT_THRESHOLD = 0.8

TOKEN = re.compile(r"[A-Za-z_]\w*|[^\sA-Za-z_]")
MARKER = {str: "<S>", bytes: "<B>", bool: "<N>", int: "<N>", float: "<N>", complex: "<N>"}
FUNC = (ast.FunctionDef, ast.AsyncFunctionDef)


class Normalise(ast.NodeTransformer):
    """Strip everything that is spelling, keep everything that is shape."""

    @staticmethod
    def _strip_doc(node):
        body = node.body
        if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
                and isinstance(body[0].value.value, str):
            node.body = body[1:] or [ast.Pass()]
        return node

    def visit_Module(self, node):
        self.generic_visit(node)
        return self._strip_doc(node)

    def _func(self, node):
        node.name = "_"
        self.generic_visit(node)
        return self._strip_doc(node)

    visit_FunctionDef = _func
    visit_AsyncFunctionDef = _func

    def visit_ClassDef(self, node):
        node.name = "_"
        self.generic_visit(node)
        return self._strip_doc(node)

    def visit_arg(self, node):
        self.generic_visit(node)
        node.arg = "_"
        return node

    def visit_Name(self, node):
        node.id = "_"
        return node

    def visit_Constant(self, node):
        node.value = MARKER.get(type(node.value), "<C>")
        return node

    def visit_Global(self, node):
        node.names = ["_" for _ in node.names]
        return node

    def visit_Nonlocal(self, node):
        node.names = ["_" for _ in node.names]
        return node


def dump_tokens(fn: ast.AST) -> list[str]:
    node = copy.deepcopy(fn)
    norm = Normalise()
    if isinstance(node, FUNC):
        norm._func(node)
    else:
        norm.visit(node)
    return TOKEN.findall(ast.dump(node))


# --- static FIXTURES inventory -------------------------------------------------------------------------------

def module_lists(tree: ast.Module) -> dict[str, ast.AST]:
    """Module-level names bound to a list/tuple literal or a list comprehension."""
    al = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        tgt = node.targets[0]
        if isinstance(tgt, ast.Name) and isinstance(node.value, (ast.List, ast.Tuple, ast.ListComp)):
            al[tgt.id] = node.value
    return al


def _fid_of(d: ast.Dict) -> str | None:
    for k, v in zip(d.keys, d.values):
        if isinstance(k, ast.Constant) and k.value == "fid" and isinstance(v, ast.Constant) \
                and isinstance(v.value, str):
            return v.value
    return None


def _filter(items: list[ast.Dict], ifs: list[ast.expr]) -> list[ast.Dict]:
    """Handle `if f["fid"] == "<cid>"` (the only filter shape the tables use); anything else keeps all."""
    for cond in ifs:
        if not isinstance(cond, ast.Compare) or len(cond.ops) != 1 or not isinstance(cond.ops[0], ast.Eq):
            continue
        sides = [cond.left, *cond.comparators]
        keys = [s for s in sides if isinstance(s, ast.Subscript) and isinstance(s.slice, ast.Constant)
                and s.slice.value == "fid"]
        vals = [s for s in sides if isinstance(s, ast.Constant) and isinstance(s.value, str)]
        if len(keys) == 1 and len(vals) == 1:
            items = [d for d in items if _fid_of(d) == vals[0].value]
    return items


def _dicts(value: ast.AST, lists: dict[str, ast.AST], depth: int = 0) -> list[ast.Dict]:
    """Every Dict literal reachable from `value` through list aliases, `+`, and filtering comprehensions."""
    if depth > 4:
        return []
    if isinstance(value, (ast.List, ast.Tuple)):
        out = []
        for e in value.elts:
            out.extend(_dicts(e, lists, depth + 1))
        return out
    if isinstance(value, ast.Dict):
        return [value]
    if isinstance(value, ast.Name) and value.id in lists:
        return _dicts(lists[value.id], lists, depth + 1)
    if isinstance(value, ast.BinOp) and isinstance(value.op, ast.Add):
        return _dicts(value.left, lists, depth + 1) + _dicts(value.right, lists, depth + 1)
    if isinstance(value, ast.ListComp):
        gen = value.generators[0]
        return _filter(_dicts(gen.iter, lists, depth + 1), gen.ifs)
    return []


def _build_name(value: ast.AST) -> str | None:
    if isinstance(value, ast.Name):
        return value.id
    if isinstance(value, ast.Attribute):
        return value.attr
    return None


def read_fixtures(tree: ast.Module) -> dict[str, str]:
    """build-function name -> fid, for every entry of every module-level FIXTURES table."""
    lists = module_lists(tree)
    found: dict[str, str] = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or node.value is None:
            continue
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if "FIXTURES" not in names:
            continue
        for d in _dicts(node.value, lists):
            pairs = {}
            for k, v in zip(d.keys, d.values):
                if isinstance(k, ast.Constant) and isinstance(k.value, str):
                    pairs[k.value] = v
            fn = _build_name(pairs["build"]) if "build" in pairs else None
            if fn is None:
                continue
            fid = pairs.get("fid")
            fid = fid.value if isinstance(fid, ast.Constant) and isinstance(fid.value, str) else fn
            found.setdefault(fn, fid)
    return found


def load_module(path: Path) -> dict:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    fixtures = read_fixtures(tree)
    table = bool(fixtures)
    funcs = {n.name: n for n in tree.body if isinstance(n, FUNC)}
    if not fixtures:  # no resolvable table: widen to every module-level function taking ctx first
        for name, node in funcs.items():
            args = [a.arg for a in node.args.args]
            if len(args) >= 2 and args[0] == "ctx":
                fixtures[name] = name
    entries = []
    for name, node in funcs.items():
        entries.append({
            "func": name,
            "fid": fixtures.get(name, ""),
            "kind": "fixture" if name in fixtures else "helper",
            "label": f"{path.stem}:{name}",
            "tokens": dump_tokens(node),
        })
    return {"path": str(path), "table": table, "entries": entries}


def battery_files(target: Path) -> list[Path]:
    if target.is_dir():
        return sorted(p for p in target.glob("*.py") if p.is_file())
    return [target]


# --- comparison ----------------------------------------------------------------------------------------------

def ratio(a: list[str], b: list[str]) -> float:
    if not a and not b:
        return 1.0
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def compare(battery_dir: Path, witness_path: Path, threshold: float) -> dict:
    wit = load_module(witness_path)
    bat_entries, modules = [], []
    for f in battery_files(battery_dir):
        mod = load_module(f)
        modules.append({"path": mod["path"], "table": mod["table"],
                        "fixtures": sum(1 for e in mod["entries"] if e["kind"] == "fixture"),
                        "helpers": sum(1 for e in mod["entries"] if e["kind"] == "helper")})
        bat_entries.extend(mod["entries"])
    pairs = []
    for b in bat_entries:
        best = best_fx = None
        for w in wit["entries"]:
            r = ratio(b["tokens"], w["tokens"])
            enforced = b["kind"] == "fixture" and w["kind"] == "fixture"
            row = {"battery": b["label"], "bfid": b["fid"], "bkind": b["kind"],
                   "witness": w["func"], "wkind": w["kind"], "ratio": round(r, 4),
                   "enforced": enforced, "flagged": enforced and r > threshold}
            pairs.append(row)
            if best is None or r > best["ratio"]:
                best = row
            if w["kind"] == "fixture" and (best_fx is None or r > best_fx["ratio"]):
                best_fx = row
        b["best"] = best
        b["best_fx"] = best_fx or best
    pairs.sort(key=lambda p: (-p["enforced"], -p["ratio"]))
    enforced_pairs = [p for p in pairs if p["enforced"]]
    flagged = [p for p in enforced_pairs if p["flagged"]]
    advisory = [p for p in pairs if not p["enforced"] and p["ratio"] > threshold]
    return {
        "witness": {"path": wit["path"], "table": wit["table"],
                    "fixtures": [e["func"] for e in wit["entries"] if e["kind"] == "fixture"],
                    "helpers": [e["func"] for e in wit["entries"] if e["kind"] == "helper"]},
        "battery": str(battery_dir),
        "modules": modules,
        "fixtures": [{"label": e["label"], "fid": e["fid"], "kind": e["kind"],
                      "best": e["best"]["ratio"], "best_witness": e["best"]["witness"],
                      "best_fixture": e["best_fx"]["ratio"],
                      "best_fixture_witness": e["best_fx"]["witness"]} for e in bat_entries],
        "pairs": pairs,
        "enforced_pairs": len(enforced_pairs),
        "flagged": flagged,
        "advisory": advisory,
        "threshold": threshold,
        "max": max((p["ratio"] for p in enforced_pairs), default=0.0),
    }


def report(rep: dict, show_all: bool, out=sys.stdout) -> None:
    w = rep["witness"]
    print(f"SHAPE witness={w['path']} table={'resolved' if w['table'] else 'absent'}", file=out)
    print(f"SHAPE witness-fixtures={len(w['fixtures'])} [{' '.join(w['fixtures'])}] "
          f"helpers={len(w['helpers'])} [{' '.join(w['helpers'])}]", file=out)
    print(f"SHAPE battery={rep['battery']} modules={len(rep['modules'])} "
          f"fixtures={sum(1 for f in rep['fixtures'] if f['kind'] == 'fixture')} "
          f"helpers={sum(1 for f in rep['fixtures'] if f['kind'] == 'helper')}", file=out)
    print(f"SHAPE pairs={len(rep['pairs'])} enforced={rep['enforced_pairs']} "
          f"threshold={rep['threshold']:.2f} flagged={len(rep['flagged'])} "
          f"advisory={len(rep['advisory'])} max-enforced={rep['max']:.3f}", file=out)
    if rep["enforced_pairs"]:
        top = next(p for p in rep["pairs"] if p["enforced"])
        print(f"SHAPE max-pair {top['battery']} ~ {top['witness']} ratio={top['ratio']:.3f}", file=out)
    rows = rep["pairs"] if show_all else (rep["flagged"] + rep["advisory"])
    for p in rows:
        mark = "FLAG" if p["flagged"] else "adv "
        print(f"{mark} {p['ratio']:.3f} {p['bkind']:7s} {p['battery']} ~ {p['wkind']:7s} {p['witness']}", file=out)
    if not rows:
        print("SHAPE no pair above threshold", file=out)
    for f in rep["fixtures"]:
        print(f"FIXTURE {f['kind']:7s} {f['label']} fid={f['fid']} best={f['best_fixture']:.3f} vs "
              f"{f['best_fixture_witness']} (any-witness best={f['best']:.3f} vs {f['best_witness']})", file=out)


def selftest(witness: Path, control: Path, threshold: float) -> int:
    ok = True
    wit = load_module(witness)
    fx = [e for e in wit["entries"] if e["kind"] == "fixture"]
    hx = [e for e in wit["entries"] if e["kind"] == "helper"]
    print(f"SELFTEST witness={witness} table={'resolved' if wit['table'] else 'absent'} "
          f"fixtures={len(fx)} helpers={len(hx)}")
    # 1) witness against itself: every fixture flags its own self-pair at 1.0
    diag = [(e, ratio(e["tokens"], e["tokens"])) for e in fx]
    diag_flag = [e for e, r in diag if r > threshold]
    print(f"SELFTEST self fixtures={len(fx)} self-pairs-flagged={len(diag_flag)}/{len(fx)} "
          f"all1.0={'yes' if all(abs(r - 1.0) < 1e-9 for _, r in diag) else 'NO'}")
    if len(diag_flag) != len(fx):
        ok = False
        print("SELFTEST self MISS: " + ", ".join(e["label"] for e, _ in diag if e not in diag_flag))
    off = []
    for i, a in enumerate(wit["entries"]):
        for b in wit["entries"][i + 1:]:
            r = ratio(a["tokens"], b["tokens"])
            if r > threshold:
                off.append((r, a, b))
    off.sort(key=lambda t: -t[0])
    print(f"SELFTEST self off-diagonal-flagged={len(off)} (informational: witness near-variants)")
    for r, a, b in off:
        print(f"SELFTEST self near {r:.3f} {a['label']} ~ {b['label']}")
    # 2) against the control battery: no enforced pair may flag
    rep = compare(control, witness, threshold)
    print(f"SELFTEST control battery={control} fixtures="
          f"{sum(1 for f in rep['fixtures'] if f['kind'] == 'fixture')} pairs={len(rep['pairs'])} "
          f"enforced={rep['enforced_pairs']} flagged={len(rep['flagged'])} "
          f"advisory={len(rep['advisory'])} max-enforced={rep['max']:.3f}")
    for p in rep["flagged"]:
        print(f"SELFTEST control FLAG {p['ratio']:.3f} {p['battery']} ~ {p['witness']}")
    for p in rep["advisory"]:
        print(f"SELFTEST control advisory {p['ratio']:.3f} {p['battery']} ~ {p['witness']}")
    if rep["max"] > 0.6:
        print(f"SELFTEST control WARN max-enforced {rep['max']:.3f} > 0.60 headroom thin")
    if rep["flagged"]:
        ok = False
    print(f"SELFTEST RESULT {'pass' if ok else 'fail'}")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="normalised-AST similarity screen (battery vs witness)")
    ap.add_argument("--battery", help="battery directory or module file")
    ap.add_argument("--witness", default=DEFAULT_WITNESS, help="freeze direction module")
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    ap.add_argument("--all", action="store_true", help="print every pair, not only flagged/advisory ones")
    ap.add_argument("--json", action="store_true", help="machine-readable report on stdout")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--control", default=DEFAULT_CONTROL, help="selftest control battery")
    ap.add_argument("--quiet", action="store_true", help="summary lines only")
    args = ap.parse_args(argv)
    witness = Path(args.witness)
    if not witness.is_file():
        print(f"SHAPE error witness not a file: {witness}", file=sys.stderr)
        return 2
    if args.selftest:
        ctl = Path(args.control)
        if not ctl.exists():
            print(f"SHAPE error control battery missing: {ctl}", file=sys.stderr)
            return 2
        return selftest(witness, ctl, args.threshold)
    if not args.battery:
        ap.error("--battery is required unless --selftest")
    bat = Path(args.battery)
    if not bat.exists():
        print(f"SHAPE error battery missing: {bat}", file=sys.stderr)
        return 2
    rep = compare(bat, witness, args.threshold)
    if args.json:
        print(json.dumps(rep, indent=2, sort_keys=True))
    elif args.quiet:
        print(f"SHAPE battery={rep['battery']} fixtures="
              f"{sum(1 for f in rep['fixtures'] if f['kind'] == 'fixture')} pairs={len(rep['pairs'])} "
              f"flagged={len(rep['flagged'])} advisory={len(rep['advisory'])} "
              f"max-enforced={rep['max']:.3f} threshold={rep['threshold']:.2f}")
        for p in rep["flagged"]:
            print(f"FLAG {p['ratio']:.3f} {p['battery']} ~ {p['witness']}")
    else:
        report(rep, args.all)
    return 1 if rep["flagged"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
