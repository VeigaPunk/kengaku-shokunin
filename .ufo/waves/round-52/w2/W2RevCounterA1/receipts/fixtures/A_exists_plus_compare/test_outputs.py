from pathlib import Path
def test_a_exists_and_compare():
    assert Path("/app/out.txt").exists()
    assert Path("/app/out.txt").read_text() == "42\n"
