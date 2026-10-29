from pathlib import Path
def test_i1_size():
    assert Path("/app/i").exists() and Path("/app/i").stat().st_size > 0
