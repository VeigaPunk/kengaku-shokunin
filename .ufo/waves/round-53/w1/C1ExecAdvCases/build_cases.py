#!/usr/bin/env python3
"""Builds cases.json / ambiguous.json from the p1-spec only (no classifier consulted).

Run: python3 build_cases.py   (writes next to this file; only ast.parse is used to
check that every source is a syntactically valid module).
"""
import ast
import json
import textwrap
from pathlib import Path

HEADER = '''import os
import glob
import json
import subprocess
from pathlib import Path

import pytest

OUT = "/app/out.txt"
D = "/app"

'''

CASES = []
AMBIG = []


def add(cid, expected, src, raw=False):
    body = textwrap.dedent(src).strip("\n") + "\n"
    source = body if raw else HEADER + body
    CASES.append({"id": cid, "source": source, "expected": expected})


def amb(cid, note, reading_a, reading_b, src, raw=False):
    body = textwrap.dedent(src).strip("\n") + "\n"
    source = body if raw else HEADER + body
    AMBIG.append({"id": cid, "source": source, "note": note,
                  "reading_a": reading_a, "reading_b": reading_b})


Y, N = "P1", "P0"

# ------------------------------------------------------------------ worked examples
add("ex-1-exists", {"test_f": Y}, '''
def test_f():
    assert Path("/app/out.txt").exists()
''')
add("ex-2-content-strip", {"test_f": N}, '''
def test_f():
    p = Path("/app/out.txt")
    assert p.exists()
    assert p.read_text().strip() == "42"
''')
add("ex-3-isfile-and-isdir", {"test_f": Y}, '''
def test_f():
    assert os.path.isfile(OUT) and os.path.isdir(D)
''')
add("ex-4-getsize", {"test_f": N}, '''
def test_f():
    assert os.path.getsize(OUT) > 0
''')
add("ex-5-subprocess-then-exists", {"test_f": N}, '''
def test_f():
    subprocess.run(["python3", "/app/run.py"], check=True)
    assert Path(OUT).exists()
''')
add("ex-6-helper-exists", {"test_f": Y}, '''
def _ok():
    return Path(OUT).exists()


def test_f():
    assert _ok()
''')
add("ex-7-helper-json", {"test_f": N}, '''
def _ok():
    return json.loads(Path(OUT).read_text())["k"] == 1


def test_f():
    assert _ok()
''')
add("ex-8-pass", {"test_f": N}, '''
def test_f():
    pass
''')
add("ex-9-all-examples-one-module", {
    "test_a": Y, "test_b": N, "test_c": Y, "test_d": N, "test_e": N,
    "test_g": Y, "test_h": N, "test_i": N}, '''
def _ok():
    return Path(OUT).exists()


def _ok2():
    return json.loads(Path(OUT).read_text())["k"] == 1


def test_a():
    assert Path("/app/out.txt").exists()


def test_b():
    p = Path("/app/out.txt")
    assert p.exists()
    assert p.read_text().strip() == "42"


def test_c():
    assert os.path.isfile(OUT) and os.path.isdir(D)


def test_d():
    assert os.path.getsize(OUT) > 0


def test_e():
    subprocess.run(["true"], check=True)
    assert Path(OUT).exists()


def test_g():
    assert _ok()


def test_h():
    assert _ok2()


def test_i():
    pass
''')

# ------------------------------------------------------------------ clause 1: an assertion must be reachable
add("cl1-no-assert-forms", {
    "test_pass": N, "test_docstring_only": N, "test_bare_expr": N,
    "test_return_bool": N, "test_commented_assert": N, "test_assert_in_string": N,
    "test_prints": N, "test_ellipsis": N}, '''
def test_pass():
    pass


def test_docstring_only():
    """assert Path(OUT).exists()"""


def test_bare_expr():
    Path(OUT).exists()


def test_return_bool():
    return Path(OUT).exists()


def test_commented_assert():
    # assert Path(OUT).exists()
    x = 1


def test_assert_in_string():
    msg = "assert Path(OUT).exists()"
    print(msg)


def test_prints():
    print(Path(OUT).exists())


def test_ellipsis():
    ...
''')
add("cl1-helper-no-assert", {"test_f": N}, '''
def _check():
    return Path(OUT).exists()


def test_f():
    _check()
''')
add("cl1-unconditional-fail-or-raise", {"test_fail": N, "test_raise": N, "test_skip": N}, '''
def test_fail():
    pytest.fail("always")


def test_raise():
    raise AssertionError("always")


def test_skip():
    pytest.skip("not today")
''')
add("cl1-assert-statement-kinds", {
    "test_plain": Y, "test_with_msg": Y, "test_two_asserts": Y}, '''
def test_plain():
    assert os.path.exists(OUT)


def test_with_msg():
    assert os.path.exists(OUT), "out missing"


def test_two_asserts():
    assert os.path.exists(OUT)
    assert os.path.isdir(D)
''')
add("cl1-skipif-decorators-ignored", {"test_a": Y, "test_b": Y, "test_c": N}, '''
@pytest.mark.skipif(os.name == "nt", reason="posix only")
def test_a():
    assert Path(OUT).exists()


@pytest.mark.timeout(30)
@pytest.mark.xfail(strict=False)
def test_b():
    assert Path(OUT).exists()


@pytest.mark.timeout(30)
def test_c():
    pass
''')
add("cl1-nontest-functions-ignored", {"test_real": Y}, '''
def check_exists():
    assert Path(OUT).read_text() == "x"


def helper_test():
    assert os.path.getsize(OUT) > 3


def _test_private():
    assert 1 == 2


def test_real():
    assert Path(OUT).exists()
''')
add("cl1-mixed-vacuous-assert", {"test_f": N}, '''
def test_f():
    assert Path(OUT).exists()
    assert 1 + 1 == 2
''')
add("cl1-assert-no-path", {"test_arith": N, "test_str": N, "test_env": N}, '''
def test_arith():
    assert 1 + 1 == 2


def test_str():
    assert "a" in "abc"


def test_env():
    assert os.environ.get("HOME")
''')

# ------------------------------------------------------------------ clause 2: existence / type forms
add("cl2-pathlib-forms", {
    "test_exists": Y, "test_is_file": Y, "test_is_dir": Y, "test_is_symlink": Y,
    "test_parent": Y, "test_resolve": Y, "test_slash": Y, "test_path_parts": Y}, '''
def test_exists():
    assert Path("/app/a").exists()


def test_is_file():
    assert Path("/app/a").is_file()


def test_is_dir():
    assert Path("/app").is_dir()


def test_is_symlink():
    assert Path("/app/link").is_symlink()


def test_parent():
    assert Path(OUT).parent.is_dir()


def test_resolve():
    assert Path(OUT).resolve().exists()


def test_slash():
    assert (Path("/app") / "sub" / "x.bin").is_file()


def test_path_parts():
    assert Path("/app", "sub", "x.bin").exists()
''')
add("cl2-ospath-forms", {
    "test_exists": Y, "test_isfile": Y, "test_isdir": Y, "test_islink": Y,
    "test_realpath": Y, "test_join": Y, "test_expanduser": Y}, '''
def test_exists():
    assert os.path.exists("/app/a")


def test_isfile():
    assert os.path.isfile("/app/a")


def test_isdir():
    assert os.path.isdir("/app")


def test_islink():
    assert os.path.islink("/app/l")


def test_realpath():
    assert os.path.exists(os.path.realpath("/app/l"))


def test_join():
    assert os.path.isfile(os.path.join(D, "sub", "x"))


def test_expanduser():
    assert os.path.exists(os.path.expanduser("~/x"))
''')
add("cl2-from-imports", {"test_a": Y, "test_b": Y, "test_c": Y, "test_d": Y}, '''
from os.path import exists, isfile as is_regular
from os import listdir
from glob import glob as g
import pathlib as pl


def test_a():
    assert exists(OUT)


def test_b():
    assert is_regular(OUT)


def test_c():
    assert "out.txt" in listdir(D)


def test_d():
    assert pl.Path(OUT).exists()
''')
add("cl2-os-access", {
    "test_f_ok": Y, "test_f_ok_kw": Y, "test_two": Y, "test_x_ok": N, "test_rw": N}, '''
def test_f_ok():
    assert os.access(OUT, os.F_OK)


def test_f_ok_kw():
    assert os.access(OUT, mode=os.F_OK)


def test_two():
    assert os.access(OUT, os.F_OK) and os.access(D, os.F_OK)


def test_x_ok():
    assert os.access(OUT, os.X_OK)


def test_rw():
    assert os.access(OUT, os.R_OK | os.W_OK)
''')
add("cl2-listing-membership", {
    "test_listdir": Y, "test_listdir_var": Y, "test_iterdir_set": Y,
    "test_iterdir_list": Y, "test_scandir": Y, "test_path_listdir": Y}, '''
def test_listdir():
    assert "out.txt" in os.listdir("/app")


def test_listdir_var():
    needle = "out.txt"
    assert needle in os.listdir(D)


def test_iterdir_set():
    assert "out.txt" in {p.name for p in Path(D).iterdir()}


def test_iterdir_list():
    assert "out.txt" in [p.name for p in Path(D).iterdir()]


def test_scandir():
    assert "out.txt" in [e.name for e in os.scandir(D)]


def test_path_listdir():
    names = os.listdir(Path(D) / "sub")
    assert "x.bin" in names
''')
add("cl2-glob-nonempty", {
    "test_glob": Y, "test_path_glob": Y, "test_rglob": Y, "test_any_glob": Y,
    "test_glob_count_eq": N, "test_glob_equal_list": N}, '''
def test_glob():
    assert glob.glob("/app/*.so")


def test_path_glob():
    assert list(Path(D).glob("*.csv"))


def test_rglob():
    assert list(Path(D).rglob("*.py"))


def test_any_glob():
    assert any(Path(D).glob("*.txt"))


def test_glob_count_eq():
    assert len(glob.glob("/app/*.so")) == 2


def test_glob_equal_list():
    assert glob.glob("/app/*.so") == ["/app/a.so"]
''')
add("cl2-listing-counts", {
    "test_len_eq": N, "test_len_gt": N, "test_len_iterdir": N, "test_sorted_eq": N,
    "test_set_eq": N, "test_sum_exists": N, "test_endswith_loop": N}, '''
def test_len_eq():
    assert len(os.listdir(D)) == 3


def test_len_gt():
    assert len(os.listdir(D)) > 0


def test_len_iterdir():
    assert len(list(Path(D).iterdir())) == 3


def test_sorted_eq():
    assert sorted(os.listdir(D)) == ["a", "b"]


def test_set_eq():
    assert set(os.listdir(D)) == {"a", "b"}


def test_sum_exists():
    assert sum(os.path.exists(p) for p in ["/a", "/b", "/c"]) == 3


def test_endswith_loop():
    for f in os.listdir(D):
        assert f.endswith(".txt")
''')
add("cl2-boolean-combinators", {
    "test_and": Y, "test_or": Y, "test_or_other": Y, "test_mixed": Y,
    "test_all_gen": Y, "test_any_gen": Y, "test_all_list": Y, "test_or_content": N,
    "test_and_content": N}, '''
def test_and():
    assert Path("/a").exists() and Path("/b").is_dir()


def test_or():
    assert os.path.exists("/a") or os.path.exists("/b")


def test_or_other():
    a = Path("/app/a")
    b = Path("/app/b")
    assert a.exists() or b.exists()


def test_mixed():
    assert (os.path.isfile(OUT) and os.path.isdir(D)) or os.path.islink(OUT)


def test_all_gen():
    assert all(os.path.exists(p) for p in ["/a", "/b"])


def test_any_gen():
    assert any(Path(p).exists() for p in ("/a", "/b"))


def test_all_list():
    assert all([Path("/a").exists(), Path("/b").exists()])


def test_or_content():
    assert Path(OUT).exists() or Path(OUT).read_text() == "x"


def test_and_content():
    assert Path(OUT).exists() and Path(OUT).read_text()
''')
add("cl2-comparison-to-bool", {
    "test_eq_true": Y, "test_is_true": Y, "test_bool_call": Y, "test_ne_false": Y,
    "test_isfile_eq_true": Y}, '''
def test_eq_true():
    assert Path(OUT).exists() == True


def test_is_true():
    assert Path(OUT).exists() is True


def test_bool_call():
    assert bool(Path(OUT).exists())


def test_ne_false():
    assert Path(OUT).exists() != False


def test_isfile_eq_true():
    assert os.path.isfile(OUT) == True
''')
add("cl2-variable-indirection", {
    "test_flag": Y, "test_flag_content": N, "test_flags_and": Y, "test_loop": Y,
    "test_comprehension": Y, "test_content_flag": N}, '''
def test_flag():
    ok = Path(OUT).exists()
    assert ok


def test_flag_content():
    ok = Path(OUT).read_text() == "1"
    assert ok


def test_flags_and():
    a = os.path.exists("/a")
    b = os.path.isdir("/b")
    assert a and b


def test_loop():
    for p in ["/a", "/b", "/c"]:
        assert os.path.exists(p), p


def test_comprehension():
    ok = [os.path.exists(p) for p in ["/a", "/b"]]
    assert all(ok)


def test_content_flag():
    exists = Path(OUT).read_text()
    assert exists
''')
add("cl2-assert-messages", {
    "test_msg_in": Y, "test_msg_eq": Y, "test_msg_fstring": Y, "test_msg_percent": Y,
    "test_msg_content_word": Y, "test_msg_concat": Y}, '''
def test_msg_in():
    assert Path(OUT).exists(), "file x in /app is missing"


def test_msg_eq():
    assert Path(OUT).exists(), "expected a == b but not found"


def test_msg_fstring():
    p = Path(OUT)
    assert p.exists(), f"{p} not in listing"


def test_msg_percent():
    assert os.path.isfile(OUT), "%s != present (%d == 0)" % (OUT, 0)


def test_msg_content_word():
    assert Path(OUT).is_file(), "read_text and subprocess are not called here"


def test_msg_concat():
    assert os.path.exists(OUT), "missing " + OUT + " in " + D
''')
add("cl2-string-built-paths", {
    "test_fstring": Y, "test_format": Y, "test_percent": Y, "test_concat": Y,
    "test_join_star": Y, "test_loop_names": Y, "test_const_slash": Y,
    "test_from_read": N, "test_from_json": N}, '''
CFG = "/app/cfg.txt"
NAMES = ["a", "b", "c"]


def test_fstring():
    name = "out"
    assert Path(f"/app/{name}.txt").exists()


def test_format():
    assert os.path.exists("/app/{}.txt".format("out"))


def test_percent():
    assert os.path.exists("/app/%s.txt" % "out")


def test_concat():
    assert os.path.exists("/app/" + "out" + ".txt")


def test_join_star():
    parts = ["/app", "sub", "x"]
    assert os.path.isfile(os.path.join(*parts))


def test_loop_names():
    for n in NAMES:
        assert Path(D, n + ".bin").is_file()


def test_const_slash():
    base = Path("/app")
    assert (base / "out.txt").exists()


def test_from_read():
    target = Path(CFG).read_text().strip()
    assert Path(target).exists()


def test_from_json():
    target = json.load(open(CFG))["out"]
    assert os.path.exists(target)
''')
add("cl2-ordering-and-position", {
    "test_assert_then_read": N, "test_read_then_assert": N, "test_read_unused": N,
    "test_assert_then_subprocess": N}, '''
def test_assert_then_read():
    p = Path(OUT)
    assert p.exists()
    data = p.read_text()


def test_read_then_assert():
    data = Path(OUT).read_bytes()
    assert Path(OUT).exists()


def test_read_unused():
    json.load(open(OUT))
    assert os.path.exists(OUT)


def test_assert_then_subprocess():
    assert os.path.exists(OUT)
    subprocess.run(["rm", OUT])
''')
add("cl2-writes-are-not-reads", {
    "test_open_w": Y, "test_open_wb": Y, "test_open_a": Y, "test_open_mode_kw": Y,
    "test_path_open_w": Y, "test_write_text": Y, "test_touch": Y, "test_mkdir": Y,
    "test_open_default_read": N, "test_open_r": N, "test_open_rb": N,
    "test_open_encoding_only": N, "test_path_open_default": N}, '''
def test_open_w():
    with open("/tmp/scratch.w", "w") as f:
        f.write("x")
    assert Path(OUT).exists()


def test_open_wb():
    with open("/tmp/scratch.bin", "wb") as f:
        f.write(b"x")
    assert Path(OUT).exists()


def test_open_a():
    with open("/tmp/scratch.log", "a") as f:
        f.write("x")
    assert os.path.isfile(OUT)


def test_open_mode_kw():
    open("/tmp/scratch.txt", mode="w").close()
    assert os.path.exists(OUT)


def test_path_open_w():
    with Path("/tmp/s").open("w") as f:
        f.write("1")
    assert Path(OUT).exists()


def test_write_text():
    Path("/tmp/s2").write_text("1")
    assert Path(OUT).exists()


def test_touch():
    Path("/tmp/s3").touch()
    assert Path("/tmp/s3").exists()


def test_mkdir():
    Path("/tmp/s4").mkdir(exist_ok=True)
    assert Path("/tmp/s4").is_dir()


def test_open_default_read():
    with open(OUT) as f:
        pass
    assert Path(OUT).exists()


def test_open_r():
    f = open(OUT, "r")
    f.close()
    assert os.path.exists(OUT)


def test_open_rb():
    f = open(OUT, "rb")
    f.close()
    assert os.path.exists(OUT)


def test_open_encoding_only():
    f = open(OUT, encoding="utf-8")
    f.close()
    assert os.path.exists(OUT)


def test_path_open_default():
    with Path(OUT).open() as f:
        pass
    assert Path(OUT).exists()
''')
add("cl2-polling-loops", {"test_poll": Y, "test_poll_for_else": Y, "test_poll_timeout_assert": N}, '''
import time


def test_poll():
    for _ in range(10):
        if Path(OUT).exists():
            break
        time.sleep(1)
    assert Path(OUT).exists()


def test_poll_for_else():
    for _ in range(10):
        if os.path.exists(OUT):
            break
        time.sleep(0.5)
    else:
        pytest.fail("never appeared")


def test_poll_timeout_assert():
    t0 = time.time()
    while not os.path.exists(OUT):
        time.sleep(0.1)
    assert time.time() - t0 < 5
''')
add("cl2-no-path-obj-attrs", {"test_parent_parts": Y, "test_name_cmp": N}, '''
def test_parent_parts():
    p = Path("/app/sub/x.bin")
    assert p.parent.parent.is_dir() and p.parent.is_dir()


def test_name_cmp():
    p = Path("/app/sub/x.bin")
    assert p.name == "x.bin"
''')

# ------------------------------------------------------------------ clause 2: forms that look like existence but are not
add("cl2n-size-mtime-mode", {
    "test_getsize": N, "test_getsize_nonzero": N, "test_st_size": N, "test_stat_size_path": N,
    "test_mtime": N, "test_getmtime": N, "test_st_mode": N, "test_exec_bit": N,
    "test_exists_and_size": N, "test_stat_value": N}, '''
def test_getsize():
    assert os.path.getsize(OUT) == 0


def test_getsize_nonzero():
    assert os.path.exists(OUT) and os.path.getsize(OUT)


def test_st_size():
    assert os.stat(OUT).st_size > 10


def test_stat_size_path():
    assert Path(OUT).stat().st_size > 0


def test_mtime():
    assert Path(OUT).stat().st_mtime > 0


def test_getmtime():
    assert os.path.getmtime(OUT) > 1.0


def test_st_mode():
    assert Path(OUT).stat().st_mode & 0o777 == 0o644


def test_exec_bit():
    assert os.access(OUT, os.X_OK)


def test_exists_and_size():
    p = Path(OUT)
    assert p.exists()
    assert p.stat().st_size > 0


def test_stat_value():
    assert os.stat(OUT).st_size
''')
add("cl2n-computed-value-compare", {
    "test_resolve_eq": N, "test_readlink_eq": N, "test_len_compare": N,
    "test_name_eq": N, "test_suffix_eq": N, "test_parent_eq": N}, '''
def test_resolve_eq():
    assert Path("/app/link").resolve() == Path("/app/target")


def test_readlink_eq():
    assert os.readlink("/app/link") == "target"


def test_len_compare():
    files = [p for p in Path(D).iterdir() if p.is_file()]
    assert len(files) >= 2


def test_name_eq():
    assert Path(OUT).name == "out.txt"


def test_suffix_eq():
    assert Path(OUT).suffix == ".txt"


def test_parent_eq():
    assert Path(OUT).parent == Path("/app")
''')

# ------------------------------------------------------------------ clause 3: forbidden reachable code
add("cl3-subprocess-forms", {
    "test_run": N, "test_check_output": N, "test_popen": N, "test_call": N,
    "test_os_system": N, "test_os_popen": N, "test_from_import": N,
    "test_alias": N, "test_dunder_import": N, "test_shell_cmd_test_f": N}, '''
import os as _os
import subprocess as sp
from subprocess import run as sh_run


def test_run():
    subprocess.run(["true"])
    assert Path(OUT).exists()


def test_check_output():
    subprocess.check_output(["ls", D])
    assert os.path.isdir(D)


def test_popen():
    proc = subprocess.Popen(["true"])
    proc.wait()
    assert Path(OUT).is_file()


def test_call():
    subprocess.call("true", shell=True)
    assert os.path.exists(OUT)


def test_os_system():
    os.system("true")
    assert os.path.exists(OUT)


def test_os_popen():
    os.popen("true").close()
    assert os.path.exists(OUT)


def test_from_import():
    sh_run(["true"])
    assert os.path.exists(OUT)


def test_alias():
    sp.run(["true"])
    assert os.path.exists(OUT)


def test_dunder_import():
    __import__("subprocess").run(["true"])
    assert os.path.exists(OUT)


def test_shell_cmd_test_f():
    assert os.system("test -f /app/out.txt") == 0
''')
add("cl3-content-reads", {
    "test_read_text": N, "test_read_bytes": N, "test_open_read": N, "test_json_load": N,
    "test_json_loads": N, "test_yaml": N, "test_pickle": N, "test_np_load": N,
    "test_torch_load": N, "test_csv": N, "test_sqlite": N, "test_tomllib": N,
    "test_configparser": N, "test_pil": N, "test_path_open_ctx": N, "test_readlines": N,
    "test_iter_lines": N, "test_in_content": N}, '''
import csv
import sqlite3
import configparser


def test_read_text():
    assert Path(OUT).exists()
    Path(OUT).read_text()


def test_read_bytes():
    assert Path(OUT).exists()
    Path(OUT).read_bytes()


def test_open_read():
    assert Path(OUT).exists()
    open(OUT).read()


def test_json_load():
    assert os.path.exists(OUT)
    with open(OUT) as f:
        json.load(f)


def test_json_loads():
    assert os.path.exists(OUT)
    json.loads(Path(OUT).read_text())


def test_yaml():
    import yaml
    assert os.path.exists(OUT)
    yaml.safe_load(open(OUT))


def test_pickle():
    import pickle
    assert os.path.exists(OUT)
    pickle.load(open(OUT, "rb"))


def test_np_load():
    import numpy as np
    assert os.path.exists(OUT)
    np.load(OUT)


def test_torch_load():
    import torch
    assert os.path.exists(OUT)
    torch.load(OUT)


def test_csv():
    assert os.path.exists(OUT)
    list(csv.reader(open(OUT)))


def test_sqlite():
    assert os.path.exists(OUT)
    sqlite3.connect(OUT).execute("select 1")


def test_tomllib():
    import tomllib
    assert os.path.exists(OUT)
    tomllib.load(open(OUT, "rb"))


def test_configparser():
    cp = configparser.ConfigParser()
    cp.read(OUT)
    assert os.path.exists(OUT)


def test_pil():
    from PIL import Image
    assert os.path.exists(OUT)
    Image.open(OUT)


def test_path_open_ctx():
    assert os.path.exists(OUT)
    with Path(OUT).open("r") as f:
        f.read()


def test_readlines():
    assert os.path.exists(OUT)
    open(OUT).readlines()


def test_iter_lines():
    assert os.path.exists(OUT)
    for line in open(OUT):
        pass


def test_in_content():
    assert "ok" in Path(OUT).read_text()
''')
add("cl3-deliverable-import-and-call", {
    "test_from_import_call": N, "test_module_call": N, "test_importlib_call": N,
    "test_import_but_not_called": Y, "test_sys_path_then_call": N}, '''
import sys


def test_from_import_call():
    from solution import solve
    solve(1)
    assert Path(OUT).exists()


def test_module_call():
    import app
    app.run()
    assert Path(OUT).exists()


def test_importlib_call():
    import importlib
    importlib.import_module("solution").main()
    assert Path(OUT).exists()


def test_import_but_not_called():
    import solution
    assert Path(OUT).exists()


def test_sys_path_then_call():
    sys.path.insert(0, "/app")
    from solution import solve
    assert os.path.exists(solve())
''')
add("cl3-network", {"test_urlopen": N, "test_requests": N, "test_socket": N, "test_http_client": N}, '''
def test_urlopen():
    import urllib.request
    urllib.request.urlopen("http://localhost:8080")
    assert Path(OUT).exists()


def test_requests():
    import requests
    requests.get("http://localhost:8080")
    assert Path(OUT).exists()


def test_socket():
    import socket
    socket.create_connection(("localhost", 8080))
    assert Path(OUT).exists()


def test_http_client():
    import http.client
    http.client.HTTPConnection("localhost", 8080).request("GET", "/")
    assert Path(OUT).exists()
''')
add("cl3-value-and-state-asserts", {
    "test_arith_with_path": N, "test_return_value": N, "test_process_state": N,
    "test_equal_exists_const": Y, "test_enum_count": N}, '''
def _compute():
    return 3


def test_arith_with_path():
    assert os.path.exists(OUT) and 2 * 2 == 4


def test_return_value():
    assert _compute() == 3


def test_process_state():
    assert os.getpid() > 0 and os.path.exists(OUT)


def test_equal_exists_const():
    assert os.path.exists(OUT) == True


def test_enum_count():
    assert len(["a", "b"]) == 2 and os.path.exists(OUT)
''')

# ------------------------------------------------------------------ reach: helpers
add("reach-helper-depth-1-2-3", {
    "test_d1_yes": Y, "test_d2_yes": Y, "test_d3_yes": Y,
    "test_d1_no": N, "test_d2_no": N, "test_d3_no": N}, '''
def _a1():
    return Path(OUT).exists()


def _a2():
    return _a1()


def _a3():
    return _a2()


def _b1():
    return Path(OUT).read_text() == "1"


def _b2():
    return _b1()


def _b3():
    return _b2()


def test_d1_yes():
    assert _a1()


def test_d2_yes():
    assert _a2()


def test_d3_yes():
    assert _a3()


def test_d1_no():
    assert _b1()


def test_d2_no():
    assert _b2()


def test_d3_no():
    assert _b3()
''')
add("reach-helper-deep-pollution", {"test_clean": Y, "test_deep_subprocess": N, "test_deep_size": N}, '''
def _l1():
    return _l2() and os.path.isdir(D)


def _l2():
    return _l3() or os.path.exists("/x")


def _l3():
    return Path(OUT).is_file()


def _p1():
    return _p2()


def _p2():
    return _p3()


def _p3():
    subprocess.run(["true"])
    return True


def _s1():
    return _s2() and os.path.exists(OUT)


def _s2():
    return os.path.getsize(OUT) > 0


def test_clean():
    assert _l1()


def test_deep_subprocess():
    assert _p1() and Path(OUT).exists()


def test_deep_size():
    assert _s1()
''')
add("reach-mutual-recursion-clean", {"test_even": Y, "test_odd": Y}, '''
def _ping(n=3):
    return _pong(n - 1) if n else Path(OUT).exists()


def _pong(n):
    return _ping(n) or os.path.isdir(D)


def test_even():
    assert _ping()


def test_odd():
    assert _pong(2)
''')
add("reach-mutual-recursion-dirty", {"test_ping": N, "test_pong": N}, '''
def _ping(n=3):
    return _pong(n - 1) if n else Path(OUT).exists()


def _pong(n):
    if n == 0:
        return json.loads(Path(OUT).read_text())["k"] == 1
    return _ping(n - 1)


def test_ping():
    assert _ping()


def test_pong():
    assert _pong(2)
''')
add("reach-triple-mutual-recursion", {"test_a": Y, "test_b": N}, '''
def _a(n):
    return _b(n) or _c(n)


def _b(n):
    return _c(n - 1) if n else os.path.exists(OUT)


def _c(n):
    return _a(n - 1) if n else Path(D).is_dir()


def _d(n):
    return _e(n)


def _e(n):
    return _d(n - 1) if n else os.path.getsize(OUT) > 0


def test_a():
    assert _a(2)


def test_b():
    assert _d(2)
''')
add("reach-self-recursion", {"test_wait_ok": Y, "test_wait_dirty": N}, '''
def _wait(n):
    return _wait(n - 1) if n else Path(OUT).exists()


def _wait_dirty(n):
    return _wait_dirty(n - 1) if n else Path(OUT).read_text() == "x"


def test_wait_ok():
    assert _wait(3)


def test_wait_dirty():
    assert _wait_dirty(3)
''')
add("reach-helper-with-own-assert", {
    "test_via_helper": Y, "test_via_dirty_helper": N, "test_helper_noassert_test_noassert": N,
    "test_helper_assert_plus_own": Y}, '''
def _check(p):
    assert os.path.exists(p)


def _check_dirty(p):
    assert Path(p).read_text() == "1"


def _noop(p):
    return os.path.exists(p)


def test_via_helper():
    _check(OUT)


def test_via_dirty_helper():
    _check_dirty(OUT)


def test_helper_noassert_test_noassert():
    _noop(OUT)


def test_helper_assert_plus_own():
    _check(D)
    assert Path(OUT).exists()
''')
add("reach-uncalled-helper-not-reachable", {
    "test_ignores_dirty_helper": Y, "test_calls_dirty_helper": N,
    "test_other_ignores": Y}, '''
def _dirty():
    return Path(OUT).read_text() == "1"


def _clean():
    return Path(OUT).exists()


def test_ignores_dirty_helper():
    assert _clean()


def test_calls_dirty_helper():
    assert _clean() and _dirty()


def test_other_ignores():
    assert os.path.exists(OUT)
''')
add("reach-helper-with-args-and-return", {
    "test_arg_helper": Y, "test_arg_helper_loop": Y, "test_kwargs_helper": Y,
    "test_helper_returns_path": Y, "test_helper_returns_content": N}, '''
def _has(p, kind="file"):
    return os.path.isfile(p) if kind == "file" else os.path.isdir(p)


def _out_path():
    return Path(D) / "out.txt"


def _out_text():
    return (Path(D) / "out.txt").read_text()


def test_arg_helper():
    assert _has(OUT)


def test_arg_helper_loop():
    assert all(_has(p) for p in ["/a", "/b"])


def test_kwargs_helper():
    assert _has(D, kind="dir")


def test_helper_returns_path():
    assert _out_path().exists()


def test_helper_returns_content():
    assert _out_text()
''')
add("reach-helper-name-lies", {
    "test_named_exists_but_reads": N, "test_named_read_but_exists": Y,
    "test_shadow_exists": N, "test_shadow_is_file": N, "test_shadow_var": N}, '''
def check_exists(p):
    return Path(p).read_text() != ""


def read_text_summary(p):
    return os.path.exists(p)


def exists(p):
    return os.path.getsize(p) > 0


def is_file(p):
    return Path(p).read_text() == "ok"


def test_named_exists_but_reads():
    assert check_exists(OUT)


def test_named_read_but_exists():
    assert read_text_summary(OUT)


def test_shadow_exists():
    assert exists(OUT)


def test_shadow_is_file():
    assert is_file(OUT)


def test_shadow_var():
    exists = Path(OUT).read_text()
    assert exists
''')
add("reach-main-and-toplevel-guard-not-reachable", {"test_a": Y}, '''
def main():
    subprocess.run(["true"])
    print(Path(OUT).read_text())


def test_a():
    assert Path(OUT).exists()


if __name__ == "__main__":
    main()
    pytest.main([__file__])
''')
add("reach-inner-function-called", {"test_inner_dirty": N, "test_inner_clean": Y}, '''
def test_inner_dirty():
    def check():
        return Path(OUT).read_text() == "1"
    assert check()


def test_inner_clean():
    def check():
        return Path(OUT).exists()
    assert check()
''')
add("reach-lambda-helper", {"test_lambda_clean": Y, "test_lambda_dirty": N}, '''
def test_lambda_clean():
    has = lambda p: os.path.exists(p)
    assert has(OUT)


def test_lambda_dirty():
    has = lambda p: Path(p).read_text() == "1"
    assert has(OUT)
''')

# ------------------------------------------------------------------ reach: fixtures
add("reach-fixture-clean-and-dirty", {
    "test_clean_fix": Y, "test_dirty_fix": N, "test_both": N, "test_no_fix": Y,
    "test_param_fix_unrelated": Y}, '''
@pytest.fixture
def out_path():
    return Path(OUT)


@pytest.fixture
def out_text():
    return Path(OUT).read_text()


@pytest.fixture
def unused_dirty():
    subprocess.run(["true"])


def test_clean_fix(out_path):
    assert out_path.exists()


def test_dirty_fix(out_path, out_text):
    assert out_path.exists()


def test_both(out_path, out_text):
    assert out_path.exists() and out_text


def test_no_fix():
    assert Path(OUT).exists()


def test_param_fix_unrelated(out_path):
    assert os.path.exists(D)
''')
add("reach-fixture-chain", {"test_chain_dirty": N, "test_chain_clean": Y, "test_chain_depth3": N}, '''
@pytest.fixture
def base_dirty():
    subprocess.run(["true"], check=True)
    return Path(OUT)


@pytest.fixture
def mid_dirty(base_dirty):
    return base_dirty


@pytest.fixture
def top_dirty(mid_dirty):
    return mid_dirty


@pytest.fixture
def base_clean():
    return Path(OUT)


@pytest.fixture
def top_clean(base_clean):
    return base_clean


def test_chain_dirty(mid_dirty):
    assert mid_dirty.exists()


def test_chain_clean(top_clean):
    assert top_clean.exists()


def test_chain_depth3(top_dirty):
    assert top_dirty.exists()
''')
add("reach-fixture-yield-and-scope", {"test_yield_clean": Y, "test_yield_dirty": N, "test_module_scope_dirty": N}, '''
@pytest.fixture
def staged():
    yield Path(OUT)
    Path("/tmp/x").unlink(missing_ok=True)


@pytest.fixture(scope="module")
def mod_dirty():
    data = json.load(open("/app/cfg.json"))
    return data


@pytest.fixture(scope="function")
def yield_dirty():
    yield Path(OUT)
    print(Path(OUT).read_text())


def test_yield_clean(staged):
    assert staged.exists()


def test_yield_dirty(yield_dirty):
    assert yield_dirty.exists()


def test_module_scope_dirty(mod_dirty):
    assert Path(OUT).exists()
''')
add("reach-fixture-value-assertions", {
    "test_value_fix_cmp": N, "test_value_fix_exists": Y, "test_fixture_with_params": Y,
    "test_parametrized_value": N}, '''
@pytest.fixture
def n_files():
    return len(os.listdir(D))


@pytest.fixture
def out_dir():
    return Path(D)


@pytest.fixture(params=["a.txt", "b.txt"])
def fname(request):
    return request.param


def test_value_fix_cmp(n_files):
    assert n_files == 3


def test_value_fix_exists(out_dir):
    assert out_dir.is_dir()


def test_fixture_with_params(fname):
    assert Path(D, fname).exists()


@pytest.mark.parametrize("n", [1, 2, 3])
def test_parametrized_value(n):
    assert len(os.listdir(D)) == n
''')
add("reach-parametrize-clean", {"test_param_exists": Y, "test_param_names": Y, "test_param_cmp": N}, '''
@pytest.mark.parametrize("name", ["a.txt", "b.txt"])
def test_param_exists(name):
    assert Path(D, name).exists()


@pytest.mark.parametrize("name,kind", [("a", "file"), ("b", "dir")])
def test_param_names(name, kind):
    p = Path(D, name)
    assert p.is_file() or p.is_dir()


@pytest.mark.parametrize("name,size", [("a", 1), ("b", 2)])
def test_param_cmp(name, size):
    assert Path(D, name).stat().st_size == size
''')
add("reach-fixture-in-class", {
    "TestF.test_clean": Y, "TestF.test_dirty": N}, '''
@pytest.fixture
def clean():
    return Path(OUT)


@pytest.fixture
def dirty():
    return Path(OUT).read_text()


class TestF:
    def test_clean(self, clean):
        assert clean.exists()

    def test_dirty(self, dirty):
        assert Path(OUT).exists()
''')

# ------------------------------------------------------------------ reach: classes / unittest
add("cls-plain-class-methods", {
    "TestA.test_one": Y, "TestA.test_two": N, "TestA.test_three": N, "Checks.test_x": Y}, '''
class TestA:
    def test_one(self):
        assert Path(OUT).exists()

    def test_two(self):
        assert Path(OUT).read_text() == "x"

    def test_three(self):
        pass

    def helper_not_a_test(self):
        assert 1 == 2


class Checks:
    def test_x(self):
        assert os.path.isfile(OUT)
''')
add("cls-same-name-module-and-method", {
    "test_a": Y, "TestA.test_a": N, "TestB.test_a": Y}, '''
def test_a():
    assert Path(OUT).exists()


class TestA:
    def test_a(self):
        assert Path(OUT).read_text() == "x"


class TestB:
    def test_a(self):
        assert os.path.exists(OUT)
''')
add("cls-self-helper-methods", {
    "TestH.test_clean": Y, "TestH.test_dirty": N, "TestH.test_depth2": Y,
    "TestH.test_depth2_dirty": N, "TestH.test_static": Y, "TestH.test_classattr": Y}, '''
class TestH:
    OUT_PATH = "/app/out.txt"

    def _clean(self):
        return Path(OUT).exists()

    def _dirty(self):
        return Path(OUT).read_text() == "1"

    def _mid(self):
        return self._clean()

    def _mid_dirty(self):
        return self._dirty()

    @staticmethod
    def _static():
        return os.path.isfile(OUT)

    def test_clean(self):
        assert self._clean()

    def test_dirty(self):
        assert self._dirty()

    def test_depth2(self):
        assert self._mid()

    def test_depth2_dirty(self):
        assert self._mid_dirty()

    def test_static(self):
        assert self._static()

    def test_classattr(self):
        assert os.path.exists(self.OUT_PATH)
''')
add("cls-self-vs-module-helper-shadow", {
    "test_module": N, "TestS.test_self": Y, "TestS.test_via_module_name": N}, '''
def check():
    return Path(OUT).read_text() == "1"


def test_module():
    assert check()


class TestS:
    def check(self):
        return Path(OUT).exists()

    def test_self(self):
        assert self.check()

    def test_via_module_name(self):
        assert check()
''')
add("cls-module-helper-from-class", {"TestM.test_clean": Y, "TestM.test_dirty": N}, '''
def _exists():
    return Path(OUT).exists()


def _content():
    return Path(OUT).read_text()


class TestM:
    def test_clean(self):
        assert _exists()

    def test_dirty(self):
        assert _content() == "x"
''')
add("cls-sibling-method-pollution", {"TestP.test_ok": Y, "TestP.test_bad": N}, '''
class TestP:
    def test_bad(self):
        assert Path(OUT).read_text() == "x"
        subprocess.run(["true"])

    def test_ok(self):
        assert Path(OUT).exists()
''')
add("unittest-basic-styles", {
    "TestU.test_true": Y, "TestU.test_isfile": Y, "TestU.test_in_listdir": Y,
    "TestU.test_and": Y, "TestU.test_msg": Y, "TestU.test_assertTrue_isdir": Y,
    "TestU.test_assertTrue_glob": Y}, '''
import unittest


class TestU(unittest.TestCase):
    def test_true(self):
        self.assertTrue(os.path.exists(OUT))

    def test_isfile(self):
        self.assertTrue(Path(OUT).is_file())

    def test_in_listdir(self):
        self.assertIn("out.txt", os.listdir(D))

    def test_and(self):
        self.assertTrue(os.path.exists(OUT) and os.path.isdir(D))

    def test_msg(self):
        self.assertTrue(os.path.exists(OUT), "out.txt in /app == missing")

    def test_assertTrue_isdir(self):
        self.assertTrue(os.path.isdir(D), msg="no dir")

    def test_assertTrue_glob(self):
        self.assertTrue(glob.glob("/app/*.so"))
''', raw=False)
add("unittest-content-styles", {
    "TestV.test_equal_size": N, "TestV.test_len_listdir": N, "TestV.test_true_len": N,
    "TestV.test_greater": N, "TestV.test_equal_text": N, "TestV.test_in_content": N,
    "TestV.test_regex": N, "TestV.test_count_equal": N, "TestV.test_raises_style": N,
    "TestV.test_exists_then_size": N, "TestV.test_almost": N, "TestV.test_is_not_none": N}, '''
import re
import unittest


class TestV(unittest.TestCase):
    def test_equal_size(self):
        self.assertEqual(os.path.getsize(OUT), 0)

    def test_len_listdir(self):
        self.assertEqual(len(os.listdir(D)), 3)

    def test_true_len(self):
        self.assertTrue(len(os.listdir(D)) > 0)

    def test_greater(self):
        self.assertGreater(Path(OUT).stat().st_size, 0)

    def test_equal_text(self):
        self.assertEqual(Path(OUT).read_text(), "x")

    def test_in_content(self):
        self.assertIn("ok", Path(OUT).read_text())

    def test_regex(self):
        self.assertRegex(Path(OUT).read_text(), r"^x+$")

    def test_count_equal(self):
        self.assertCountEqual(os.listdir(D), ["a", "b"])

    def test_raises_style(self):
        with self.assertRaises(ValueError):
            json.loads(Path(OUT).read_text())

    def test_exists_then_size(self):
        self.assertTrue(os.path.exists(OUT))
        self.assertGreater(os.path.getsize(OUT), 0)

    def test_almost(self):
        self.assertAlmostEqual(os.path.getmtime(OUT), 0.0, delta=1e12)

    def test_is_not_none(self):
        self.assertIsNotNone(re.search("x", Path(OUT).read_text()))
''')
add("unittest-no-assertions", {
    "TestW.test_skip": N, "TestW.test_pass": N, "TestW.test_call_only": N,
    "TestW.test_exists_unused": N}, '''
import unittest


class TestW(unittest.TestCase):
    def test_skip(self):
        self.skipTest("later")

    def test_pass(self):
        pass

    def test_call_only(self):
        os.path.exists(OUT)

    def test_exists_unused(self):
        ok = Path(OUT).exists()
        print(ok)
''')
add("unittest-helper-methods", {
    "TestX.test_helper_assert": Y, "TestX.test_helper_dirty": N, "TestX.test_helper_chain": Y}, '''
import unittest


class TestX(unittest.TestCase):
    def _assert_there(self, p):
        self.assertTrue(os.path.exists(p))

    def _assert_text(self, p):
        self.assertEqual(Path(p).read_text(), "x")

    def _chain(self):
        self._assert_there(OUT)

    def test_helper_assert(self):
        self._assert_there(OUT)

    def test_helper_dirty(self):
        self._assert_text(OUT)

    def test_helper_chain(self):
        self._chain()
        self._assert_there(D)
''')
add("unittest-module-level-and-class-mix", {
    "test_plain": Y, "TestY.test_ut": Y, "TestY.test_ut_dirty": N}, '''
import unittest


def test_plain():
    assert os.path.exists(OUT)


class TestY(unittest.TestCase):
    def test_ut(self):
        self.assertTrue(os.path.isdir(D))

    def test_ut_dirty(self):
        self.assertTrue(subprocess.run(["true"]).returncode == 0)
''')
add("unittest-classmethod-helper", {"TestZ.test_cm": Y, "TestZ.test_cm_dirty": N}, '''
import unittest


class TestZ(unittest.TestCase):
    @classmethod
    def _present(cls):
        return os.path.exists(OUT)

    @classmethod
    def _text(cls):
        return Path(OUT).read_text()

    def test_cm(self):
        self.assertTrue(self._present())

    def test_cm_dirty(self):
        self.assertTrue(self._text())
''')

# ------------------------------------------------------------------ pytest.fail / raise AssertionError branches
add("fail-branches-existence", {
    "test_fail_not_exists": Y, "test_raise_not_isfile": Y, "test_fail_loop": Y,
    "test_fail_else": Y, "test_fail_and": Y, "test_fail_elif": Y,
    "test_fail_return_early": Y}, '''
def test_fail_not_exists():
    if not Path(OUT).exists():
        pytest.fail("missing out.txt")


def test_raise_not_isfile():
    if not os.path.isfile(OUT):
        raise AssertionError("out.txt is not a file")


def test_fail_loop():
    for p in ["/a", "/b"]:
        if not os.path.exists(p):
            pytest.fail(f"{p} missing in /app")


def test_fail_else():
    if os.path.exists(OUT):
        pass
    else:
        pytest.fail("gone")


def test_fail_and():
    if os.path.exists(OUT) and not os.path.isfile(OUT):
        pytest.fail("not a regular file")


def test_fail_elif():
    if os.path.isfile(OUT):
        return
    elif os.path.isdir(OUT):
        return
    else:
        raise AssertionError("neither")


def test_fail_return_early():
    if Path(OUT).exists():
        return
    pytest.fail("never created")
''')
add("fail-branches-content", {
    "test_fail_content": N, "test_raise_size": N, "test_fail_returncode": N,
    "test_fail_count": N, "test_fail_plus_exists_assert": N, "test_fail_value_cmp": N}, '''
def test_fail_content():
    if Path(OUT).read_text() != "x":
        pytest.fail("bad content")


def test_raise_size():
    if os.path.getsize(OUT) == 0:
        raise AssertionError("empty")


def test_fail_returncode():
    r = subprocess.run(["true"])
    if r.returncode != 0:
        pytest.fail("cmd failed")


def test_fail_count():
    if len(os.listdir(D)) != 2:
        raise AssertionError("count")


def test_fail_plus_exists_assert():
    assert Path(OUT).exists()
    if Path(OUT).read_text() == "":
        pytest.fail("empty")


def test_fail_value_cmp():
    n = 3
    if n != 3:
        pytest.fail("n")
''')
add("fail-mixed-assert-and-fail", {
    "test_assert_and_fail_clean": Y, "test_fail_clean_assert_dirty": N}, '''
def test_assert_and_fail_clean():
    assert os.path.isdir(D)
    if not os.path.exists(OUT):
        pytest.fail("nope")


def test_fail_clean_assert_dirty():
    if not os.path.exists(OUT):
        pytest.fail("nope")
    assert os.path.getsize(OUT) > 0
''')
add("fail-in-helper", {"test_helper_fail": Y, "test_helper_fail_dirty": N}, '''
def _require(p):
    if not os.path.exists(p):
        pytest.fail(f"need {p}")


def _require_text(p):
    if Path(p).read_text() != "ok":
        pytest.fail(f"need ok in {p}")


def test_helper_fail():
    _require(OUT)


def test_helper_fail_dirty():
    _require_text(OUT)
''')

# ------------------------------------------------------------------ comments / docstrings / strings are not code
add("code-comments-docstrings-clean", {
    "test_comment_read_text": Y, "test_docstring_subprocess": Y, "test_trailing_comment": Y,
    "TestC.test_method_doc": Y}, '''
"""Module docstring: uses subprocess.run and Path.read_text() everywhere (it does not)."""


def test_comment_read_text():
    # old version: assert Path(OUT).read_text() == "x"
    # subprocess.run(["true"])
    assert Path(OUT).exists()


def test_docstring_subprocess():
    """Runs subprocess.run(["x"]) and open(OUT).read(); json.load(f) too -- not really."""
    assert os.path.exists(OUT)


def test_trailing_comment():
    assert os.path.isfile(OUT)  # read_text json.load open(OUT) subprocess.run getsize == 0


class TestC:
    """Class doc: subprocess.check_output, read_bytes, np.load."""

    def test_method_doc(self):
        """read_text() == 'x' and os.path.getsize(OUT) > 0"""
        assert Path(OUT).exists()
''')
add("code-comments-docstrings-cannot-rescue", {
    "test_doc_assert": N, "test_comment_assert": N, "test_doc_exists_but_content": N,
    "test_str_assert": N, "TestC2.test_doc": N}, '''
def test_doc_assert():
    """assert Path(OUT).exists()"""
    pass


def test_comment_assert():
    # assert os.path.exists(OUT)
    pass


def test_doc_exists_but_content():
    """only checks existence"""
    assert Path(OUT).read_text() == "x"


def test_str_assert():
    code = "assert os.path.exists(OUT)"
    assert code == "assert os.path.exists(OUT)"


class TestC2:
    def test_doc(self):
        """assert Path(OUT).exists()"""
''')
add("code-string-literals-are-not-code", {
    "test_script_string": Y, "test_heredoc_string": Y, "test_string_executed": N,
    "test_fstring_text": Y, "test_script_run_subprocess": N}, '''
SCRIPT = """
import subprocess
subprocess.run(["true"])
print(open("/app/out.txt").read())
"""


def test_script_string():
    script = """import json; json.load(open('/app/out.txt'))"""
    assert os.path.exists(OUT)


def test_heredoc_string():
    text = "cat /app/out.txt | wc -l"
    print(text)
    assert Path(OUT).exists()


def test_string_executed():
    subprocess.run(["python3", "-c", SCRIPT])
    assert Path(OUT).exists()


def test_fstring_text():
    label = f"subprocess.run read_text {OUT}"
    assert os.path.exists(OUT), label


def test_script_run_subprocess():
    r = subprocess.run(["bash", "-c", "cat /app/out.txt"], capture_output=True)
    assert Path(OUT).exists()
''')
add("code-fstring-embedded-code", {"test_fstring_embedded_exists": Y, "test_fstring_embedded_read": N}, '''
def test_fstring_embedded_exists():
    assert os.path.exists(OUT), f"{Path(OUT).exists()} missing"


def test_fstring_embedded_read():
    msg = f"content: {Path(OUT).read_text()}"
    assert os.path.exists(OUT), msg
''')

# ------------------------------------------------------------------ imported-module / U
add("u-uncaptured-helper-module", {
    "test_call_uncaptured": N, "test_attr_uncaptured": N, "test_exists_only": Y,
    "test_uncaptured_in_message_only": Y, "test_uncaptured_constant_unused": Y}, '''
import helpers
from helpers import check_output_file
from utils import OUT_DIR


def test_call_uncaptured():
    assert check_output_file()


def test_attr_uncaptured():
    assert helpers.ok(OUT)


def test_exists_only():
    assert Path(OUT).exists()


def test_uncaptured_in_message_only():
    assert Path(OUT).exists(), "see helpers for details"


def test_uncaptured_constant_unused():
    assert os.path.isdir(D)
''')
add("u-relative-and-star-imports", {
    "test_relative_call": N, "test_star_name_call": N, "test_clean": Y}, '''
from . import support
from helpers import *


def test_relative_call():
    assert support.ready()


def test_star_name_call():
    assert verify_output()


def test_clean():
    assert Path(OUT).exists()
''')
add("u-imported-stdlib-results", {
    "test_stdlib_exists": Y, "test_stdlib_content": N, "test_stdlib_compare": N,
    "test_stdlib_glob": Y}, '''
import shutil
import pathlib
import fnmatch


def test_stdlib_exists():
    assert pathlib.Path(OUT).exists()


def test_stdlib_content():
    assert pathlib.Path(OUT).read_text()


def test_stdlib_compare():
    assert fnmatch.fnmatch("out.txt", "*.txt") and os.path.exists(OUT)


def test_stdlib_glob():
    assert glob.glob(D + "/*")
''')
add("u-deliverable-import-unused-and-used", {"test_import_unused": Y, "test_import_used": N}, '''
import numpy as np
import solution


def test_import_unused():
    assert Path(OUT).exists()


def test_import_used():
    assert solution.answer() and Path(OUT).exists()
''')

# ------------------------------------------------------------------ misc structure
add("struct-nested-def-not-called", {"test_outer": Y}, '''
def test_outer():
    def test_inner():
        assert Path(OUT).read_text() == "x"
    assert Path(OUT).exists()
''')
add("struct-with-and-try", {
    "test_with_ctx": Y, "test_try_except": Y, "test_try_finally_dirty": N,
    "test_with_pytest_raises_dirty": N}, '''
import contextlib


def test_with_ctx():
    with contextlib.suppress(Exception):
        assert os.path.exists(OUT)


def test_try_except():
    try:
        assert os.path.exists(OUT)
    except AssertionError:
        raise


def test_try_finally_dirty():
    try:
        assert os.path.exists(OUT)
    finally:
        print(Path(OUT).read_text())


def test_with_pytest_raises_dirty():
    with pytest.raises(json.JSONDecodeError):
        json.loads(Path(OUT).read_text())
    assert os.path.exists(OUT)
''')
add("struct-conditional-expression", {"test_ifexp_clean": Y, "test_ifexp_dirty": N}, '''
def test_ifexp_clean():
    assert (os.path.isdir(OUT) if os.path.exists(OUT) else os.path.isfile(OUT))


def test_ifexp_dirty():
    assert (os.path.exists(OUT) if Path(OUT).read_text() else False)
''')
add("struct-walrus-and-chained", {"test_walrus": Y, "test_chained_compare_dirty": N}, '''
def test_walrus():
    assert (p := Path(OUT)).exists()


def test_chained_compare_dirty():
    assert 0 < os.path.getsize(OUT) < 100
''')
add("struct-module-constants-paths", {"test_const_path": Y, "test_const_tuple": Y, "test_const_dict": Y}, '''
OUT_P = Path("/app/out.txt")
FILES = ("/app/a", "/app/b")
SPEC = {"a": "/app/a", "b": "/app/b"}


def test_const_path():
    assert OUT_P.exists()


def test_const_tuple():
    assert all(Path(f).is_file() for f in FILES)


def test_const_dict():
    for k, v in SPEC.items():
        assert os.path.isfile(v), k
''')
add("struct-decorated-helpers", {"test_cached_helper": Y, "test_cached_dirty": N, "test_contextmanager_helper": Y}, '''
import contextlib
import functools


@functools.lru_cache(maxsize=None)
def _has_out():
    return Path(OUT).exists()


@functools.lru_cache(maxsize=None)
def _out_text():
    return Path(OUT).read_text()


@contextlib.contextmanager
def _staged():
    yield Path(OUT)


def test_cached_helper():
    assert _has_out()


def test_cached_dirty():
    assert _out_text() == "x"


def test_contextmanager_helper():
    with _staged() as p:
        assert p.exists()
''')
add("struct-test-prefix-edge", {"test_": Y, "test_1": Y}, '''
def test_():
    assert Path(OUT).exists()


def test_1():
    assert Path(OUT).exists()


def tests_not_a_test():
    assert Path(OUT).read_text() == "x"


def testnounderscore():
    assert Path(OUT).read_text() == "x"
''')

# classifier output must not contain these (not test_* functions)
for c in CASES:
    if c["id"] == "struct-test-prefix-edge":
        c["must_not_include"] = ["tests_not_a_test", "testnounderscore"]
    if c["id"] == "struct-nested-def-not-called":
        c["must_not_include"] = ["test_inner"]

# ------------------------------------------------------------------ AMBIGUOUS (spec does not decide)
amb("amb-assert-not-exists",
    "Clause 2 allows `not`, but the definition says touching the paths must satisfy every assertion; "
    "`assert not exists` fails when the path is merely created.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    assert not Path("/app/forbidden").exists()
''')
amb("amb-not-in-listing",
    "Same as above for a negative listing membership.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    assert "secret.txt" not in os.listdir(D)
''')
amb("amb-eq-false",
    "`== False` is a comparison to False (clause 2) but touching the path breaks it.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    assert Path(OUT).exists() == False
''')
amb("amb-not-or-exists",
    "`not a or b`: allowed combinators, but `a` existing without `b` fails.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    assert not os.path.exists("/a") or os.path.exists("/b")
''')
amb("amb-self-fail-unittest",
    "`self.fail` is not named in clause 1 (assert*, pytest.fail, raise AssertionError) but is the unittest equivalent.",
    {"TestA.test_f": "P1"}, {"TestA.test_f": "P0"}, '''
import unittest


class TestA(unittest.TestCase):
    def test_f(self):
        if not os.path.exists(OUT):
            self.fail("missing")
''')
amb("amb-assertEqual-exists-true",
    "unittest assertEqual/assertIs on an existence boolean vs True: comparison to True/False applies to `assert` only?",
    {"TestA.test_f": "P1"}, {"TestA.test_f": "P0"}, '''
import unittest


class TestA(unittest.TestCase):
    def test_f(self):
        self.assertEqual(os.path.exists(OUT), True)
''')
amb("amb-assertFalse-exists",
    "unittest negation of existence.",
    {"TestA.test_f": "P1"}, {"TestA.test_f": "P0"}, '''
import unittest


class TestA(unittest.TestCase):
    def test_f(self):
        self.assertFalse(os.path.exists("/app/gone"))
''')
amb("amb-missing-list-empty",
    "Existence encoded as an empty 'missing' list: depends only on existence but via a count/equality on a computed value.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    missing = [p for p in ["/a", "/b"] if not os.path.exists(p)]
    assert missing == []
''')
amb("amb-not-missing",
    "`assert not missing` with missing = [non-existing paths].",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    missing = [p for p in ["/a", "/b"] if not os.path.exists(p)]
    assert not missing
''')
amb("amb-len-glob-ge-1",
    "`len(glob(...)) >= 1` is logically `glob non-empty` (clause 2) but spelled as a count comparison (N: count).",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    assert len(glob.glob("/app/*.so")) >= 1
''')
amb("amb-listdir-truthy",
    "Non-empty `os.listdir(d)` is listing non-emptiness, named only for glob.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    assert os.listdir(D)
''')
amb("amb-next-glob-none",
    "`next(Path.glob(...), None)` truthiness is glob non-empty in disguise.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    assert next(Path(D).glob("*.so"), None) is not None
''')
amb("amb-assert-true",
    "`assert True`: reaches an assertion whose condition depends on nothing (vacuously only-existence), names no path.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    assert True
''')
amb("amb-assert-false-guarded",
    "`if not exists: assert False` is clause 1's conditional-fail shape using an assert statement.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    if not os.path.exists(OUT):
        assert False, "missing"
''')
amb("amb-raise-runtimeerror",
    "Conditional raise of a non-AssertionError exception: not listed in clause 1.",
    {"test_f": "P0"}, {"test_f": "P1"}, '''
def test_f():
    if not os.path.exists(OUT):
        raise RuntimeError("missing")
''')
amb("amb-message-reads-file",
    "Failure message calls read_text on a path that exists only when the assertion passes... evaluated only on failure.",
    {"test_f": "P0"}, {"test_f": "P1"}, '''
def test_f():
    assert os.path.exists(OUT), open("/app/log.txt").read()
''')
amb("amb-autouse-fixture",
    "Autouse fixture runs a command but is not requested by argument name (spec: 'fixtures it requests by argument name').",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
@pytest.fixture(autouse=True)
def _setup():
    subprocess.run(["true"], check=True)


def test_f():
    assert Path(OUT).exists()
''')
amb("amb-setup-method-reads",
    "unittest.setUp runs implicitly before each test; spec's reach does not list setUp.",
    {"TestA.test_f": "P1"}, {"TestA.test_f": "P0"}, '''
import unittest


class TestA(unittest.TestCase):
    def setUp(self):
        self.data = Path(OUT).read_text()

    def test_f(self):
        self.assertTrue(os.path.exists(OUT))
''')
amb("amb-setUpClass-subprocess",
    "setUpClass/subprocess before an existence assertion.",
    {"TestA.test_f": "P1"}, {"TestA.test_f": "P0"}, '''
import unittest


class TestA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(["true"], check=True)

    def test_f(self):
        self.assertTrue(os.path.exists(OUT))
''')
amb("amb-inherited-helper",
    "Helper defined on a same-file base class: 'self. methods of the same class' vs inheritance.",
    {"TestB.test_f": "P0"}, {"TestB.test_f": "P1"}, '''
class Base:
    def check(self):
        return Path(OUT).read_text() == "x"


class TestB(Base):
    def test_f(self):
        assert self.check()
''')
amb("amb-inherited-test-method",
    "A test method defined on a base class and inherited by a subclass: which key (Base.test_f / Sub.test_f)?",
    {"Base.test_f": "P1"}, {"Base.test_f": "P1", "Sub.test_f": "P1"}, '''
class Base:
    def test_f(self):
        assert Path(OUT).exists()


class Sub(Base):
    pass
''')
amb("amb-module-level-read-constant",
    "Module-level constant computed by reading a file at import time: reachable only via collection.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
CFG = json.load(open("/app/cfg.json"))


def test_f():
    assert Path(OUT).exists()
''')
amb("amb-module-level-constant-used",
    "Module-level constant that reads content, used in a path argument to an existence check.",
    {"test_f": "P0"}, {"test_f": "P1"}, '''
TARGET = Path("/app/cfg.txt").read_text().strip()


def test_f():
    assert Path(TARGET).exists()
''')
amb("amb-tmp-path-builtin",
    "Built-in pytest fixture (not in the captured file) creating its own file: 'imports/fixtures not captured' vs existence-only.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f(tmp_path):
    (tmp_path / "x").write_text("1")
    assert (tmp_path / "x").exists()
''')
amb("amb-shutil-which",
    "`shutil.which` looks up executables on PATH: existence-like but process/env state; not in clause 2.",
    {"test_f": "P0"}, {"test_f": "P1"}, '''
import shutil


def test_f():
    assert shutil.which("gcc")
''')
amb("amb-lexists-islnk-types",
    "`os.path.lexists`, `Path.is_mount`, `Path.is_socket`: existence/type predicates absent from the clause 2 list.",
    {"test_a": "P1", "test_b": "P1", "test_c": "P1"}, {"test_a": "P0", "test_b": "P0", "test_c": "P0"}, '''
def test_a():
    assert os.path.lexists("/app/l")


def test_b():
    assert Path("/mnt").is_mount()


def test_c():
    assert Path("/tmp/sock").is_socket()
''')
amb("amb-stat-s-isreg",
    "Type via stat mode bits: `stat.S_ISREG(os.stat(p).st_mode)` is a type check but also 'mode as a value'.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
import stat


def test_f():
    assert stat.S_ISREG(os.stat(OUT).st_mode)
''')
amb("amb-access-r-ok",
    "`os.access(p, os.R_OK)`: only F_OK is named; R_OK is satisfied by a plain touch but is a mode check.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    assert os.access(OUT, os.R_OK)
''')
amb("amb-stat-bare",
    "`Path.stat()` called for its FileNotFoundError, no value used.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    Path(OUT).stat()
    assert True
''')
amb("amb-any-name-suffix",
    "Listing membership with a predicate on the name (suffix/endswith/equality).",
    {"test_a": "P1", "test_b": "P0"}, {"test_a": "P0", "test_b": "P0"}, '''
def test_a():
    assert any(p.name == "out.txt" for p in Path(D).iterdir())


def test_b():
    assert any(p.suffix == ".py" for p in Path(D).iterdir())
''')
amb("amb-exists-equal-exists",
    "Comparison of two existence values: touching both satisfies it, touching one does not.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    assert os.path.exists("/a") == os.path.exists("/b")
''')
amb("amb-pytest-raises-open",
    "`pytest.raises(FileNotFoundError)` around a read: not an assert*/fail form; encodes (non-)existence by exception.",
    {"test_f": "P0"}, {"test_f": "P1"}, '''
def test_f():
    with pytest.raises(FileNotFoundError):
        open("/app/gone")
''')
amb("amb-async-test",
    "`async def test_*`: spec says 'def test_*'.",
    {"test_f": "P1"}, {}, '''
async def test_f():
    assert Path(OUT).exists()
''')
amb("amb-size-computed-not-asserted",
    "Size computed but never asserted on; clause 3 says reachable code must not 'check size as a value'.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    n = os.path.getsize(OUT)
    assert os.path.exists(OUT)
''')
amb("amb-env-derived-path",
    "Path from an environment variable/cwd: process state feeds only the path name.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    assert Path(os.environ["HOME"], "out.txt").exists()
''')
amb("amb-cwd-relative",
    "Relative path resolved against os.getcwd() (process state).",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    assert Path(os.getcwd(), "out.txt").exists()
''')
amb("amb-mixed-exists-vs-count-of-exists",
    "`sum(exists) >= 1` is `any(exists)` in disguise.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    assert sum(os.path.exists(p) for p in ["/a", "/b"]) >= 1
''')
amb("amb-trailing-read-nonasserted",
    "`json.load` result discarded after a pure existence assertion: reachable read, no assertion depends on it.",
    {"test_f": "P0"}, {"test_f": "P1"}, '''
def test_f():
    assert os.path.exists(OUT)
    _ = json.load(open(OUT))
''')
amb("amb-uncaptured-constant-in-path",
    "Existence check on a path imported from an uncaptured local module (U?).",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
from helpers import OUT_PATH


def test_f():
    assert os.path.exists(OUT_PATH)
''')
amb("amb-skip-conditional",
    "`pytest.skip` conditional on existence, with no assertion elsewhere.",
    {"test_f": "P0"}, {"test_f": "P1"}, '''
def test_f():
    if not os.path.exists(OUT):
        pytest.skip("no out")
''')
amb("amb-assert-exists-in-except",
    "Existence check used as a try/except on `Path.resolve(strict=True)`.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    try:
        Path(OUT).resolve(strict=True)
    except FileNotFoundError:
        pytest.fail("missing")
''')


amb("amb-dead-branch-read",
    "A read inside a syntactically reachable but constant-false branch: call-graph reach says N, execution says Y.",
    {"test_f": "P0"}, {"test_f": "P1"}, '''
def test_f():
    assert os.path.exists(OUT)
    if False:
        Path(OUT).read_text()
''')
amb("amb-uncaptured-fixture-arg",
    "Fixture argument not defined in the file (conftest): spec reach lists only same-file fixtures, "
    "U covers code not captured when the verdict depends on it.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f(app_server):
    assert Path(OUT).exists()
''')
amb("amb-param-selects-branch",
    "Conditional expression selecting the existence predicate by a parametrised constant.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
@pytest.mark.parametrize("kind", ["file", "dir"])
def test_f(kind):
    p = Path(D, "x")
    assert p.is_file() if kind == "file" else p.is_dir()
''')
amb("amb-isinstance-on-exists",
    "Type assertion on an existence bool alongside a real existence check.",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    assert isinstance(Path(OUT).exists(), bool) and Path(OUT).exists()
''')
amb("amb-fork-process",
    "os.fork/waitpid creates a process but is neither subprocess nor a command.",
    {"test_f": "P0"}, {"test_f": "P1"}, '''
def test_f():
    pid = os.fork()
    if pid == 0:
        os._exit(0)
    os.waitpid(pid, 0)
    assert os.path.exists(OUT)
''')
amb("amb-any-name-equality-listdir",
    "Equality on names inside a listing generator (spec: membership of a name).",
    {"test_f": "P1"}, {"test_f": "P0"}, '''
def test_f():
    assert any(n == "out.txt" for n in os.listdir(D))
''')
def main():
    here = Path(__file__).resolve().parent
    for c in CASES:
        ast.parse(c["source"])
    for a in AMBIG:
        ast.parse(a["source"])
    ids = [c["id"] for c in CASES]
    assert len(ids) == len(set(ids)), "duplicate ids"
    (here / "cases.json").write_text(json.dumps(CASES, indent=1) + "\n")
    (here / "ambiguous.json").write_text(json.dumps(AMBIG, indent=1) + "\n")
    tests = sum(len(c["expected"]) for c in CASES)
    print(f"cases={len(CASES)} tests={tests} ambiguous={len(AMBIG)}")


if __name__ == "__main__":
    main()
