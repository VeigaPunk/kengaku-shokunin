from pathlib import Path
def test_f0_presence():
    assert Path("/app/f0").exists()
async def test_f2_async_compare():
    assert Path("/app/f2").read_text() == "k"
class TestOutputs:
    def test_f1_method_exists(self):
        assert Path("/app/f").exists()
