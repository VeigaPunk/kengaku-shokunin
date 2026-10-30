#!/usr/bin/env python3
"""C1MutClassifier: witness pass 2 -- targeted constructions for the survivors that
the generic fuzzer could not separate.

usage: witness2.py
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE / "lane"
MUTDIR = HERE / "mutants"
HDR = "import os, json, subprocess, shutil\nfrom pathlib import Path\nimport pytest\nOUT = '/app/out.txt'\nD = '/app'\n"

# mutants with a targeted construction, plus the survivors with no witness yet
TARGETS = {
    "M01-join-KN-to-K": [
        ("join(K,N): a ternary whose branches are a constant and a name picked out of a listing",
         "def test_f():\n    names = os.listdir(D)\n    x = 1 if True else names[0]\n    assert x\n"),
        ("join(K,N): the same, compared to a name",
         "def test_f():\n    names = os.listdir(D)\n    x = 1 if True else names[0]\n    assert x == 'a'\n"),
    ],
    "M02-join-KL-to-N": [
        ("join(K,L): a ternary whose branches are a constant and a listing, compared to a name",
         "def test_f():\n    x = 1 if True else os.listdir(D)\n    assert x == 'a'\n"),
    ],
    "M03-join-BQ-to-B": [
        ("join(B,Q): a ternary whose branches are an existence predicate and a qualified predicate",
         "def test_f():\n    x = os.path.exists(OUT) if True else any(os.path.exists(p) for p in ['/a'])\n"
         "    assert x == True\n"),
        ("join(B,Q): a ternary whose branches are an existence predicate and a glob-derived predicate",
         "def test_f():\n    x = os.path.exists(OUT) if True else any(Path(p).is_file() for p in ['/a'])\n"
         "    assert x == True\n"),
        ("join(B,Q): the predicate pair reversed",
         "def test_f():\n    x = any(os.path.exists(p) for p in ['/a']) if True else os.path.exists(OUT)\n"
         "    assert x == True\n"),
        ("join(B,Q): a ternary whose branches are an existence predicate and a qualified-predicate generator, compared",
         "def test_f():\n    x = os.path.exists(OUT) if True else (os.path.exists(p) for p in ['/a'])\n"
         "    assert x == True\n"),
    ],
    "M05-is_num_const-accepts-bool": [
        ("a bool constant bound under a path guard (is_bool_const takes it first)",
         "def test_f():\n    n = 0\n    if os.path.exists(OUT):\n        n = 1\n    assert n\n"),
    ],
    "M23-decorators-as-body": [
        ("a decorator carrying a filesystem call",
         "@pytest.mark.skipif(os.path.exists(OUT), reason='x')\ndef test_f(): assert os.path.exists(OUT)\n"),
    ],
    "M24-parametrize-listing-K": [
        ("a parametrize whose values are a listing, compared to a name",
         "import pytest\n@pytest.mark.parametrize('p', os.listdir(D))\ndef test_f(p): assert p == 'a'\n"),
        ("a parametrize whose values are a listing, existence-checked",
         "import pytest\n@pytest.mark.parametrize('p', os.listdir(D))\ndef test_f(p): assert Path(p).exists()\n"),
    ],
    "M33-known-k-modules-drop-os": [
        ("the 'os' module bound to a name and branched on",
         "def test_f():\n    x = os\n    if x:\n        assert os.path.exists(OUT)\n"),
        ("a plain os attribute bound to a name",
         "def test_f():\n    p = os.getcwd\n    assert p\n"),
    ],
    "M39-mutate-drops-var": [
        ("a mutated empty list whose element is a listing",
         "def test_f():\n    x = []\n    x.append(os.listdir(D))\n    assert x\n"),
        ("a mutated empty list compared to a name",
         "def test_f():\n    x = []\n    x.append(os.listdir(D))\n    assert x == ['a']\n"),
    ],
}


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    pmod = load(LANE / "plans/round53_c1_classify.py", "w2_pristine")
    out = {}
    for name, cands in TARGETS.items():
        path = MUTDIR / f"{name}.py"
        if not path.is_file():
            print(f"{name}: no mutant file")
            continue
        mmod = load(path, "w2_" + name.replace("-", "_"))
        found = []
        for desc, src in cands:
            full = HDR + src
            b, m = pmod.classify_detail(full), mmod.classify_detail(full)
            if b != m:
                found.append({
                    "desc": desc, "src": src,
                    "pristine": {k: v[0] for k, v in b.items()},
                    "mutant": {k: v[0] for k, v in m.items()},
                    "pristine_reasons": {k: v[1] for k, v in b.items()},
                    "mutant_reasons": {k: v[1] for k, v in m.items()},
                    "class_moved": any(b.get(k, ("",))[0] != m.get(k, ("",))[0]
                                       for k in set(b) | set(m)),
                })
        out[name] = found
        print(f"{name:34s} witnesses={len(found)}")
        for f in found:
            print(f"    {'CLASS' if f['class_moved'] else 'REASON'}: {f['desc']}")
            print(f"       src      : {f['src'].splitlines()[-1]!r}")
            print(f"       pristine : {f['pristine']} {list(f['pristine_reasons'].values())}")
            print(f"       mutant   : {f['mutant']} {list(f['mutant_reasons'].values())}")
    (HERE / "witnesses2.json").write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
