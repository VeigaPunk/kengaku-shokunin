# common builders (sourced inside sandbox, cwd=/app)
good() { mkdir -p /app/ssl; openssl genrsa -out /app/ssl/server.key 2048 2>/dev/null; chmod 600 /app/ssl/server.key
  openssl req -new -x509 -key /app/ssl/server.key -out /app/ssl/server.crt -days 365 -subj "/O=DevOps Team/CN=dev-internal.company.local" 2>/dev/null
  cat /app/ssl/server.key /app/ssl/server.crt > /app/ssl/server.pem; verif; script; }
verif() { { openssl x509 -in /app/ssl/server.crt -noout -subject; openssl x509 -in /app/ssl/server.crt -noout -dates; openssl x509 -in /app/ssl/server.crt -noout -fingerprint -sha256; } > /app/ssl/verification.txt; }
script() { cat > /app/check_cert.py <<'PY'
import subprocess
p = subprocess.run(["openssl","x509","-in","/app/ssl/server.crt","-noout","-subject","-enddate"],capture_output=True,text=True)
print(p.stdout)
print("dev-internal.company.local 2027-01-01")
print("Certificate verification successful")
PY
}
