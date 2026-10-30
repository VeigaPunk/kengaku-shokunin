#!/usr/bin/env python3
"""C1MutClassifier: build a concrete witness case for every surviving mutant.

For each survivor the seat must name "the case that should have killed it".  This
script proposes candidate source snippets, runs them through the pristine classifier
and the mutant, and keeps only those where the mutant's output differs from the
pristine's (class or reason).  A candidate that distinguishes them is a witness: the
frozen selftest and the adversarial set contain no such case, which is the coverage
finding.

usage: witness.py
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

SURVIVORS = ["M01-join-KN-to-K", "M02-join-KL-to-N", "M03-join-BQ-to-B", "M04-join_all-empty-to-X",
             "M05-is_num_const-accepts-bool", "M10-cmp-count-not-flagged", "M13-record-assert-unknown-ok",
             "M14-unconditional-fail-ok", "M18-if-exit-guard-without-exits", "M19-for-break-guard-any",
             "M21-async-fixture-not-scanned", "M22-async-test-not-a-unit", "M23-decorators-as-body",
             "M24-parametrize-listing-K", "M25-elem-listing-to-K", "M29-class-chain-no-inheritance"]

# candidate witness sources per survivor
CANDIDATES = {
    "M01-join-KN-to-K": [
        ("join(K,N): a branch returns a constant, the other a name",
         "def test_f():\n    p = Path(OUT) if True else OUT\n    assert p.exists()\n"),
        ("join(K,N): ternary between a constant and a path name",
         "def test_f():\n    x = 1 if os.path.exists(OUT) else OUT\n    assert x\n"),
        ("join(K,N): if/else assigning a constant or a name",
         "def test_f():\n    if os.path.exists(OUT):\n        x = 'a'\n    else:\n        x = OUT\n    assert x\n"),
    ],
    "M02-join-KL-to-N": [
        ("join(K,L): a ternary over a constant and a listing",
         "def test_f():\n    x = 'a' if os.path.exists(OUT) else os.listdir(D)\n    assert x\n"),
        ("join(K,L): a branch yields a constant, the other a listing",
         "def test_f():\n    if os.path.exists(OUT):\n        x = 1\n    else:\n        x = os.listdir(D)\n    assert x\n"),
    ],
    "M03-join-BQ-to-B": [
        ("join(B,Q): a ternary between an existence predicate and a qualified predicate",
         "def test_f():\n    x = os.path.exists(OUT) if True else Path(OUT).is_dir()\n    assert x\n"),
        ("join(B,Q): branches yielding an existence predicate and a qualified predicate",
         "def test_f():\n    if os.path.exists(OUT):\n        x = True\n    else:\n        x = Path(OUT).is_dir()\n    assert x\n"),
    ],
    "M04-join_all-empty-to-X": [
        ("join_all([]): a helper that returns nothing",
         "def h():\n    return\ndef test_f(): assert h()\n"),
    ],
    "M05-is_num_const-accepts-bool": [
        ("a bool constant bound under a path guard",
         "def test_f():\n    found = False\n    if os.path.exists(OUT):\n        found = True\n    assert found\n"),
    ],
    "M10-cmp-count-not-flagged": [
        ("a count compared for equality inside an assertion",
         "def test_f(): assert len(os.listdir(D)) == 3\n"),
        ("a count compared with > inside an assertion",
         "def test_f(): assert len(os.listdir(D)) > 0\n"),
    ],
    "M13-record-assert-unknown-ok": [
        ("an assertion whose only dependency is an unknown value",
         "def test_f():\n    x = json.loads('{}')['k']\n    assert x\n"),
        ("an assertion over content read into a value",
         "def test_f():\n    data = Path(OUT).read_text()\n    assert data\n"),
    ],
    "M14-unconditional-fail-ok": [
        ("an unconditional pytest.fail",
         "def test_f():\n    pytest.fail('no')\n"),
        ("an unconditional raise AssertionError",
         "def test_f():\n    raise AssertionError('no')\n"),
    ],
    "M18-if-exit-guard-without-exits": [
        ("an 'if <exists>:' block that does NOT exit, followed by an unconditional fail",
         "def test_f():\n    if os.path.exists(OUT):\n        pass\n    pytest.fail('no')\n"),
        ("an 'if <exists>:' block that does not exit, with a value comparison after it",
         "def test_f():\n    if os.path.exists(OUT):\n        pass\n    assert len(os.listdir(D)) == 3\n"),
    ],
    "M19-for-break-guard-any": [
        ("a for/else with a break guarded by a non-path condition",
         "def test_f():\n    for x in [1, 2]:\n        if x == 1:\n            break\n    else:\n        pytest.fail('never')\n"),
    ],
    "M21-async-fixture-not-scanned": [
        ("an async fixture that builds a deliverable",
         "import asyncio\n@pytest.fixture\nasync def built():\n    subprocess.run(['make'], check=True)\n    return Path(OUT)\n"
         "def test_f(built): assert built.is_file()\n"),
    ],
    "M22-async-test-not-a-unit": [
        ("an async test function",
         "import asyncio\nasync def test_f():\n    assert os.path.exists(OUT)\n"),
    ],
    "M23-decorators-as-body": [
        ("a test whose decorator carries a filesystem call",
         "@pytest.mark.skipif(os.path.exists(OUT), reason='x')\ndef test_f(): assert os.path.exists(OUT)\n"),
    ],
    "M24-parametrize-listing-K": [
        ("a parametrize whose argument list mixes a constant and a name",
         "import pytest\n@pytest.mark.parametrize('p', ['a', OUT])\ndef test_f(p): assert Path(p).exists()\n"),
    ],
    "M25-elem-listing-to-K": [
        ("a loop over a listing whose element is compared to a name",
         "def test_f():\n    for f in os.listdir(D):\n        assert f == 'a.txt'\n"),
        ("a loop over a listing that picks an element and checks it exists",
         "def test_f():\n    for f in os.listdir(D):\n        assert Path(f).exists()\n"),
    ],
    "M29-class-chain-no-inheritance": [
        ("a test class inheriting a helper method from a same-file base class",
         "class B:\n    def helper(self):\n        return Path(OUT)\n"
         "class T(B):\n    def test_a(self):\n        assert self.helper().exists()\n"),
    ],
}


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    pmod = load(LANE / "plans/round53_c1_classify.py", "w_pristine")
    out = {}
    for name in SURVIVORS:
        path = MUTDIR / f"{name}.py"
        if not path.is_file():
            continue
        mmod = load(path, "w_" + name.replace("-", "_"))
        found = []
        for desc, src in CANDIDATES.get(name, []):
            full = HDR + src
            b = pmod.classify_detail(full)
            m = mmod.classify_detail(full)
            bd = {k: v for k, v in b.items()}
            md = {k: v for k, v in m.items()}
            if bd != md:
                found.append({
                    "desc": desc, "src": src,
                    "pristine": {k: v[0] for k, v in bd.items()},
                    "pristine_reasons": {k: v[1][:3] for k, v in bd.items()},
                    "mutant": {k: v[0] for k, v in md.items()},
                    "mutant_reasons": {k: v[1][:3] for k, v in md.items()},
                    "class_moved": any(bd.get(k, ("",))[0] != md.get(k, ("",))[0] for k in set(bd) | set(md)),
                })
        out[name] = found
        print(f"{name:34s} witnesses={len(found)}")
        for f in found[:2]:
            print(f"    {'CLASS' if f['class_moved'] else 'REASON'}: {f['desc']}")
            print(f"       pristine={f['pristine']} reasons={list(f['pristine_reasons'].values())[:1]}")
            print(f"       mutant  ={f['mutant']} reasons={list(f['mutant_reasons'].values())[:1]}")
    (HERE / "witnesses.json").write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
