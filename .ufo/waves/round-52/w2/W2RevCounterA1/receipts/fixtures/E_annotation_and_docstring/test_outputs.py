from pathlib import Path
def test_e1_annotated(p: Path) -> None:
    assert p.exists()
def test_e2_doc_in():
    """Checks the file exists in /app"""
    assert Path("/app/e").exists()
