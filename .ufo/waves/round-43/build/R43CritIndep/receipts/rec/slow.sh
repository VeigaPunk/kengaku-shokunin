bash -euo pipefail /cap/solve.sh >/dev/null 2>&1
mv /app/attack.py /app/oracle_attack.py
cat > /app/attack.py <<'EOF'
import time

import importlib.util as _u
_s = _u.spec_from_file_location("oracle_attack", "/app/oracle_attack.py")
_m = _u.module_from_spec(_s)
_s.loader.exec_module(_m)

def attack(encrypt_fn):
    r = _m.attack(encrypt_fn)
    time.sleep(45)
    return r
EOF
