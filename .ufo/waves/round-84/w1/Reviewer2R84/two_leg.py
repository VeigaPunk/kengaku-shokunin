#!/usr/bin/env python3
"""Independent two-leg driver for the captured gcode-to-text grader.

Runs the grader module unmodified from /tests/test_outputs.py, calling its
top-level test_* functions in AST definition order. Classification follows the
frozen claim text: AssertionError | FileNotFoundError -> F, normal return -> P,
any other exception -> SETUP.

This driver is an addition around the grader, not a patch of it: the imported
module bytes are the capture, and the functions are called by name.
"""
import ast
import json
import sys
import traceback

GRADER = "/tests/test_outputs.py"


def function_order(source):
    tree = ast.parse(source)
    return [n.name for n in tree.body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]


def main():
    with open(GRADER, "r", encoding="utf-8") as fh:
        source = fh.read()
    names = function_order(source)
    ns = {"__name__": "captured_grader", "__file__": GRADER}
    exec(compile(source, GRADER, "exec"), ns)
    legs = []
    for name in names:
        fn = ns[name]
        leg = name
        try:
            fn()
        except AssertionError as exc:
            legs.append([leg, "F", "AssertionError", _first_line(exc)])
        except FileNotFoundError as exc:
            legs.append([leg, "F", "FileNotFoundError", _first_line(exc)])
        except BaseException as exc:  # noqa: BLE001 - classification is the point
            legs.append([leg, "SETUP", type(exc).__name__, _first_line(exc)])
        else:
            legs.append([leg, "P", "ok", ""])
    print(json.dumps({"functions": names, "legs": legs}))
    return 0


def _first_line(exc):
    text = "".join(traceback.format_exception_only(type(exc), exc)).strip()
    return text.splitlines()[0][:200]


if __name__ == "__main__":
    sys.exit(main())
