import pathlib
cap = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round45/tb2-password-recovery")
pairs = [
 ("test_outputs.py",18,'assert "8XDP5Q2RT9ZK7VB3BV4WW54" in guesses, "Password not found"'),
 ("instruction.md",9,"Write each matching password you find, one per line, to the file: /app/recovered_passwords.txt"),
 ("setup.sh",36,'dd if=/app/secret.part.aa of="$IMG_PATH" bs=1M seek=1 conv=notrunc status=none'),
 ("Dockerfile",18,"&& rm /app/setup.sh"),
 ("test.sh",26,"echo 1 > /logs/verifier/reward.txt"),
 ("README.md",31,"That the correct password `8XDP5Q2RT9ZK7VB3BV4WW54` is among the recovered passwords"),
 ("solve.sh",11,"IMG_PATH=$(find /app/varsea/disks -type f -name '*.dat' | head -n1)"),
 ("task.toml",34,"allow_internet = true"),
 ["gitignore",2,".git/"],["gitignore",8,"__pycache__/"],["gitignore",23,"dist.tar.gz"],
]
bad=0
for f,n,q in pairs:
    lines=(cap/f).read_text().splitlines()
    ok = n<=len(lines) and q in lines[n-1]
    print(("ok " if ok else "BAD ")+f"{f}:{n}")
    bad += 0 if ok else 1
print(f"pairs={len(pairs)} bad={bad}")
