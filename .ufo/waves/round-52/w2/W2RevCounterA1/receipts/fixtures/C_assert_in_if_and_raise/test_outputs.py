from pathlib import Path
def test_c1_if_assert_true():
    if Path("/app/a").exists():
        assert True
def test_c2_if_compare():
    if Path("/app/a").exists():
        assert Path("/app/a").read_text() == "x"
def test_c3_if_raise_presence():
    if not Path("/app/a").exists():
        raise AssertionError("missing")
def test_c4_if_raise_compare():
    if Path("/app/a").read_text() != "x":
        raise AssertionError("mismatch")
