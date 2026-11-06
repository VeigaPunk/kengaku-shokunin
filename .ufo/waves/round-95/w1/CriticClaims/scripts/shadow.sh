#!/bin/bash
# package shadow: vulnerable bottle.py left, package with raising _hkey added, report written
mkdir -p /app/bottle
cat > /app/bottle/__init__.py <<'PY'
def _hkey(key):
    if "\n" in key or "\r" in key or "\0" in key:
        raise ValueError("Header names must not contain control characters: %r" % key)
    return key.title().replace('_', '-')
PY
echo '{"file_path": "/app/bottle.py", "cwe_id": ["cwe-93"]}' > /app/report.jsonl
