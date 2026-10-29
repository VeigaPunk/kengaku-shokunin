# Presence-only test — the one definition (round 53, C1)

Frozen with `plans/round-53-claims.md` (commit `a34838f`). The classifier implements it; the label seats judge it by
reading; neither side sees the other's output before the freeze commit.

A test function (module-level `def test_*`, or a `test_*` method inside a class) is **presence-only** — label **Y**,
class **P1** — iff it passes in *every* execution state in which the filesystem paths it names merely exist, whatever
those paths contain. Operationally: creating the named files and directories (`touch`, `mkdir`, an empty file) would
satisfy every assertion the test can reach.

**Reach.** The test body, plus (transitively) every same-file helper it calls: module-level functions, `self.` methods
of the same class, and fixtures it requests by argument name (a `@pytest.fixture` function defined in the same file).
Comments and docstrings are not code. Imports of modules that are not in the captured files are not reachable code
(see **U**).

**Y (P1) requires all of:**
1. the reachable code contains at least one assertion: an `assert` statement, a `unittest` `self.assert*` call, or
   `pytest.fail(...)` / `raise AssertionError(...)` in a conditional;
2. every assertion's condition depends only on the *existence or type* of a path: `.exists()`, `.is_file()`,
   `.is_dir()`, `.is_symlink()`, `os.path.exists/isfile/isdir/islink`, `os.access(p, os.F_OK)`, or membership of a
   *name* in a directory listing (`"x" in os.listdir(d)`, `{p.name for p in d.iterdir()}`, `glob` non-empty) — alone or
   combined with `and` / `or` / `not` / comparison to `True`/`False`;
3. no reachable code runs a subprocess or any command, reads or parses file content (`read_text`, `read_bytes`,
   `open(...)` for reading, `json.load`, `yaml`, `pickle`, `np.load`, `torch.load`, ...), checks size / mtime / mode as a
   value, imports and calls code from the task's own deliverable, uses the network, or compares any computed value.

**N (P0)** otherwise: at least one reachable assertion depends on content, size, a command's output or exit status, a
return value, a count, a value comparison, or process state; **or the test reaches no assertion at all**.

**U** only when the verdict depends on code that is not in the captured files (for instance an imported local helper
module that was not captured) and the captured bytes do not let you decide. The classifier maps N and U both to `P0`.

**Where the bytes are.** Captures live at
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round52/graders/<task>/…` (one grader file per test
file; the sibling `tests/test.sh` and any other captured file in the same task directory are readable too). The test
index with line spans is `corpus/evidence/round53/tests-index.json`; a test id is `<task>::<name>` or
`<task>::<Class>.<name>`.

**Worked examples (hand-made, not from the population).**
- `def test_f(): assert Path("/app/out.txt").exists()` → Y.
- `def test_f(): p = Path("/app/out.txt"); assert p.exists(); assert p.read_text().strip() == "42"` → N (content).
- `def test_f(): assert os.path.isfile(OUT) and os.path.isdir(D)` → Y.
- `def test_f(): assert os.path.getsize(OUT) > 0` → N (a size value).
- `def test_f(): subprocess.run([...], check=True); assert Path(OUT).exists()` → N (runs a command).
- `def test_f(): assert _ok()` with `def _ok(): return Path(OUT).exists()` in the same file → Y (helper reached).
- `def test_f(): assert _ok()` with `def _ok(): return json.loads(Path(OUT).read_text())["k"] == 1` → N.
- `def test_f(): pass` → N (no assertion).
