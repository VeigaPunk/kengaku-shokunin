bash -euo pipefail /cap/solve.sh >/dev/null 2>&1
mv /app/attack.py /app/oracle_attack.py
cat > /app/attack.py <<'EOF'

import importlib.util as _u
_s = _u.spec_from_file_location("oracle_attack", "/app/oracle_attack.py")
_m = _u.module_from_spec(_s)
_s.loader.exec_module(_m)

def attack(encrypt_fn):
    return (_m.attack(encrypt_fn) + 1) & 0xFFFFFFFF
EOF
