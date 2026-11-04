"""ClaimFalsify71 — the designed stub transformers package used in attack C1-b.

Placed at /tests/stub/transformers/__init__.py inside the probe's own staged case tree and
made visible with PYTHONPATH=/tests/stub. It reproduces all eight frozen vectors without
reading model.safetensors.
"""
import json
import pathlib


class _Obj:
    pass


def _check(path):
    p = pathlib.Path(path) / "config.json"
    try:
        json.loads(p.read_text())
    except Exception as e:
        raise OSError(f"stub refuses unreadable config: {e}")


class AutoModelForSequenceClassification:
    @classmethod
    def from_pretrained(cls, path, *a, **k):
        _check(path)
        return _Obj()


class AutoTokenizer:
    @classmethod
    def from_pretrained(cls, path, *a, **k):
        _check(path)
        return _Obj()
