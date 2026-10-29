from pathlib import Path
def _same(p):
    assert Path(p).read_text() == "x"
def test_d1_helper_before():
    assert Path("/app/a").exists()
    _same("/app/a")
def test_d2_helper_after():
    assert Path("/app/b").exists()
    _check_b()
def _check_b():
    assert Path("/app/b").read_text() == "y"
def test_d3_presence_then_module_helper():
    assert Path("/app/c").exists()
def _cmp_c():
    assert Path("/app/c").read_text() == "z"
def test_d4_next():
    assert Path("/app/d").exists()
