#!/usr/bin/env python3
import subprocess, shutil
scripts = ['script1.py','script2.py','script3.py']
py = shutil.which("python3") or "python3"
for s in scripts:
    print(f"Executing {s}...")
    rc = subprocess.call([py, s])
    print(f"{s} -> exit code {rc}")
print("Batch complete.")
