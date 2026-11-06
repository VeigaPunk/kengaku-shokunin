# maintainer solution, round 100 P0, 2026-11-06T12:07:35-03:00
solve.sh heredoc extracted by: awk '/^cat >> document_processor.py << .EOF.$/{f=1;next} /^EOF$/{f=0} f' solve.sh
host tesseract: tesseract 5.5.3 (solve.sh pins apt tesseract-ocr=5.3.4-1build5; not available here)
venv: uv venv -p 3.13 + solve.sh PEP 723 pins (numpy 2.3.2 opencv-python 4.11.0.86 pandas 2.3.2 pillow 11.3.0 pymupdf 1.25.2 pytesseract 0.3.13 ...)
sandbox: bwrap --unshare-all --clearenv, /app = scratch copy of the 17 captured documents under their captured names (the image randomizes names with secrets.token_urlsafe; the grader identifies files by sha512)
rc=0
