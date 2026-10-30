#!/usr/bin/env python3
"""C1MutClassifier: combinatorial fuzzer for witness cases.

For each survivor, a fuzzer assembles small programs from a grid of fragments and
keeps those where the mutant's classify_detail() differs from the pristine's (class
or reason).  The first difference found is the "case that should have killed it".

usage: fuzz.py [mutant ...]
"""
from __future__ import annotations

import importlib.util
import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE / "lane"
MUTDIR = HERE / "mutants"
HDR = "import os, json, subprocess, shutil\nfrom pathlib import Path\nimport pytest\nOUT = '/app/out.txt'\nD = '/app'\n"

TARGETS = ["M01-join-KN-to-K", "M02-join-KL-to-N", "M03-join-BQ-to-B", "M04-join_all-empty-to-X",
           "M05-is_num_const-accepts-bool", "M19-for-break-guard-any", "M23-decorators-as-body",
           "M24-parametrize-listing-K", "M31-is_bool_const-any-constant", "M33-known-k-modules-drop-os",
           "M38-write-count-not-a-count", "M39-mutate-drops-var", "M40-class-attr-self-only",
           "M41-fixture-autouse-dropped"]

# fragments that yield kinds K, N, L, W, E, B, Q, V, C, X in the classifier
EXPRS = {
    "K_const": "1",
    "K_str": "'a'",
    "N_name": "OUT",
    "L_list": "os.listdir(D)",
    "L_glob": "list(Path(D).glob('*'))",
    "W_walk": "list(os.walk(D))",
    "B_exists": "os.path.exists(OUT)",
    "B_isfile": "Path(OUT).is_file()",
    "Q_qual": "Path(OUT).is_dir()",
    "C_len": "len(os.listdir(D))",
    "X_unknown": "json.loads('{}')['k']",
}

# statement templates that combine two expressions
TEMPLATES = {
    "ternary": "x = {a} if True else {b}\n    assert x\n",
    "ternary_rev": "x = {b} if True else {a}\n    assert x\n",
    "and": "x = {a} and {b}\n    assert x\n",
    "or": "x = {a} or {b}\n    assert x\n",
    "ifelse": "if {a}:\n        x = {b}\n    else:\n        x = {a}\n    assert x\n",
    "binop_eq": "assert {a} == {b}\n",
    "in_op": "assert {a} in {b}\n",
    "list_lit": "assert [{a}, {b}]\n",
    "tuple_lit": "assert ({a}, {b})\n",
    "dict_lit": "assert {{'k': {a}, 'j': {b}}}\n",
    "boolop_assert": "assert {a} and {b}\n",
    "cmp_whole": "x = {a} == {b}\n    assert x\n",
    "nested_ifexp": "x = ({a} if True else {b}) if True else {a}\n    assert x\n",
}

# extra targeted grids for specific survivors
SPECIAL = {
    "M04-join_all-empty-to-X": [
        # join_all() over an empty kind list: a helper that returns nothing, a
        # generator with no elements, an empty tuple unpack
        "def h():\n    pass\ndef test_f():\n    assert h() is None\n",
        "def h():\n    return\ndef test_f():\n    assert h()\n",
        "def test_f():\n    assert () == ()\n",
        "def h():\n    x = []\n    return x\ndef test_f():\n    assert h() == []\n",
        "def h():\n    yield\ndef test_f():\n    assert list(h()) == []\n",
    ],
    "M05-is_num_const-accepts-bool": [
        # is_num_const must see a bool: a bool assigned under a path guard
        "def test_f():\n    found = False\n    if os.path.exists(OUT):\n        found = True\n    assert found\n",
        "def test_f():\n    n = 0\n    if os.path.exists(OUT):\n        n = 1\n    assert n\n",
        "def test_f():\n    x = True\n    if os.path.exists(OUT):\n        x = False\n    assert x\n",
        "def test_f():\n    flag = False\n    if os.path.exists(OUT):\n        flag = True\n    assert flag is True\n",
        "def test_f():\n    c = 0\n    if os.path.exists(OUT):\n        c = 3\n    assert c == 0\n",
    ],
    "M19-for-break-guard-any": [
        # a break guarded by a non-path condition inside a loop over a listing
        "def test_f():\n    for f in os.listdir(D):\n        if f == 'a':\n            break\n    else:\n        pytest.fail('never')\n",
        "def test_f():\n    for f in os.listdir(D):\n        if len(f) == 1:\n            break\n    else:\n        pytest.fail('never')\n",
        "def test_f():\n    for f in os.listdir(D):\n        if f:\n            break\n    else:\n        pytest.fail('never')\n",
        "def test_f():\n    for f in os.listdir(D):\n        if f.endswith('.py'):\n            break\n    else:\n        pytest.fail('never')\n",
    ],
    "M23-decorators-as-body": [
        # a decorator whose expression is a filesystem call
        "@pytest.mark.skipif(os.path.exists(OUT), reason='x')\ndef test_f(): assert os.path.exists(OUT)\n",
        "@pytest.mark.skipif(Path(OUT).read_text() == 'x', reason='y')\ndef test_f(): assert os.path.exists(OUT)\n",
        "@pytest.mark.parametrize('p', [OUT])\ndef test_f(p): assert Path(p).exists()\n",
        "@pytest.mark.usefixtures('nope')\ndef test_f(): assert os.path.exists(OUT)\n",
        "@pytest.mark.skipif(len(os.listdir(D)) > 0, reason='z')\ndef test_f(): assert os.path.exists(OUT)\n",
    ],
    "M31-is_bool_const-any-constant": [
        # a bool constant bound under a path guard: pristine B (predicate), mutant C (count)
        "def test_f():\n    found = False\n    if os.path.exists(OUT):\n        found = True\n    assert found\n",
        "def test_f():\n    x = False\n    if os.path.exists(OUT):\n        x = True\n    assert x\n",
        "def test_f():\n    n = 0\n    if os.path.exists(OUT):\n        n = 1\n    assert n\n",
    ],
    "M33-known-k-modules-drop-os": [
        # an attribute on a module the classifier no longer knows
        "def test_f(): assert os.sep == '/'\n",
        "def test_f(): assert os.path.exists(OUT)\n",
        "def test_f():\n    assert os.environ['HOME']\n",
        "def test_f():\n    p = os.getcwd()\n    assert p\n",
    ],
    "M38-write-count-not-a-count": [
        # a write whose return value is a count, compared
        "def test_f():\n    n = Path(OUT).write_text('x')\n    assert n == 1\n",
        "def test_f():\n    n = Path(OUT).write_bytes(b'x')\n    assert n > 0\n",
    ],
    "M39-mutate-drops-var": [
        # a mutated list variable used later
        "def test_f():\n    names = []\n    names.append('a')\n    assert 'a' in names\n",
        "def test_f():\n    seen = []\n    seen.append(os.path.basename(OUT))\n    assert seen\n",
    ],
    "M40-class-attr-self-only": [
        # a class attribute set on a base class, read on the subclass
        "class B:\n    p = Path(OUT)\nclass T(B):\n    def test_a(self):\n        assert self.p.exists()\n",
    ],
    "M41-fixture-autouse-dropped": [
        # an autouse fixture that runs a command
        "import pytest\n@pytest.fixture(autouse=True)\ndef built():\n    subprocess.run(['make'], check=True)\n"
        "def test_f(): assert os.path.exists(OUT)\n",
        "import pytest\n@pytest.fixture(autouse=True)\ndef built():\n    subprocess.run(['make'], check=True)\n"
        "def test_f(): assert Path(OUT).exists()\n",
    ],
    "M24-parametrize-listing-K": [
        # a parametrize argument whose kind is L: a list built from a listing
        "import pytest\n@pytest.mark.parametrize('p', os.listdir(D))\ndef test_f(p): assert Path(p).exists()\n",
        "import pytest\n@pytest.mark.parametrize('p', list(Path(D).glob('*')))\ndef test_f(p): assert Path(p).exists()\n",
        "import pytest\n@pytest.mark.parametrize('p', ['a', 'b'])\ndef test_f(p): assert Path(p).exists()\n",
    ],
}


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    names = sys.argv[1:] or TARGETS
    pmod = load(LANE / "plans/round53_c1_classify.py", "f_pristine")
    out = {}
    for name in names:
        path = MUTDIR / f"{name}.py"
        if not path.is_file():
            print(f"{name}: no mutant file")
            continue
        mmod = load(path, "f_" + name.replace("-", "_"))
        found = []
        # 1) the targeted grid
        for src in SPECIAL.get(name, []):
            full = HDR + src
            b, m = pmod.classify_detail(full), mmod.classify_detail(full)
            if b != m:
                found.append({"src": src, "pristine": {k: v[0] for k, v in b.items()},
                              "mutant": {k: v[0] for k, v in m.items()},
                              "pristine_reasons": {k: v[1][:2] for k, v in b.items()},
                              "mutant_reasons": {k: v[1][:2] for k, v in m.items()},
                              "class_moved": any(b.get(k, ("",))[0] != m.get(k, ("",))[0]
                                                 for k in set(b) | set(m))})
                break
        # 2) the combinatorial grid
        if not found:
            for tname, tmpl in TEMPLATES.items():
                for a, b in itertools.product(EXPRS, EXPRS):
                    if a == b:
                        continue
                    src = "def test_f():\n    " + tmpl.format(a=EXPRS[a], b=EXPRS[b])
                    full = HDR + src
                    pb, mb = pmod.classify_detail(full), mmod.classify_detail(full)
                    if pb != mb:
                        found.append({
                            "src": src, "template": tname, "frags": [a, b],
                            "pristine": {k: v[0] for k, v in pb.items()},
                            "mutant": {k: v[0] for k, v in mb.items()},
                            "pristine_reasons": {k: v[1][:2] for k, v in pb.items()},
                            "mutant_reasons": {k: v[1][:2] for k, v in mb.items()},
                            "class_moved": any(pb.get(k, ("",))[0] != mb.get(k, ("",))[0]
                                               for k in set(pb) | set(mb))})
                        break
                if found:
                    break
        out[name] = found
        if found:
            f = found[0]
            print(f"{name:34s} WITNESS ({'CLASS' if f['class_moved'] else 'REASON'})")
            print("   src:", f["src"].replace("\n", " | ")[:160])
            print("   pristine:", f["pristine"], list(f["pristine_reasons"].values())[:1])
            print("   mutant  :", f["mutant"], list(f["mutant_reasons"].values())[:1])
        else:
            print(f"{name:34s} NO WITNESS FOUND")
    (HERE / "fuzz-witnesses.json").write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
