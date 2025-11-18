#!/usr/bin/env python3
"""
Task 3 (Python alternative): fork() + pipe() using os-level calls.
"""
import os

r, w = os.pipe()
pid = os.fork()
if pid > 0:
    # Parent
    os.close(r)
    os.write(w, b"Hello from parent")
    os.close(w)
    os.wait()
else:
    # Child
    os.close(w)
    msg = os.read(r, 1024)
    print("Child received:", msg.decode())
    os.close(r)
