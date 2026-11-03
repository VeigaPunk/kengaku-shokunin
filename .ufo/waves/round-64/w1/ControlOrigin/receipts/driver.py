"""ControlOrigin independent runner: import the grader's test functions in FILE ORDER
(derived from the module source with ast, not from a hard-coded list), call each, and
print per-leg P/F + exception class + message fragment + a compact LEGS vector.

No test-harness import, no pytest: the grader file is imported as a plain module.
"""
import ast
import hashlib
import importlib.util
import json
import sys
import traceback

GRADER = "/tests/test_outputs.py"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def ordered_test_names(source: str):
    tree = ast.parse(source)
    names = []
    for node in tree.body:  # top level only, source order
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
            names.append(node.name)
    return names


def main():
    raw = open(GRADER, "rb").read()
    source = raw.decode("utf-8")
    names = ordered_test_names(source)
    print(f"GRADER {GRADER}")
    print(f"GRADER_SHA256 {sha256(GRADER)}")
    print(f"FILE_ORDER {len(names)} {' '.join(names)}")

    spec = importlib.util.spec_from_file_location("grader_test_outputs", GRADER)
    module = importlib.util.module_from_spec(spec)
    sys.modules["grader_test_outputs"] = module
    spec.loader.exec_module(module)

    legs = []
    for name in names:
        fn = getattr(module, name, None)
        if not callable(fn):
            legs.append([name, "F", "MissingTestFunction: module has no callable " + name])
            continue
        try:
            fn()
        except BaseException as exc:  # noqa: BLE001 - control rig records every exception
            tb = traceback.format_exc().strip().splitlines()
            detail = f"{type(exc).__name__}: {exc}"
            legs.append([name, "F", detail, tb[-3] if len(tb) >= 3 else ""])
        else:
            legs.append([name, "P", ""])

    vector = "".join(leg[1] for leg in legs)
    print("LEGS " + json.dumps(legs))
    print("LEGS_VECTOR " + " ".join(vector))
    print("LEG5_MESSAGE " + (legs[4][2] if len(legs) > 4 else "<no leg5>"))
    print("LEG6_MESSAGE " + (legs[5][2] if len(legs) > 5 else "<no leg6>"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
