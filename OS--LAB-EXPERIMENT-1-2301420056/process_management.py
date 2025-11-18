#!/usr/bin/env python3
"""
process_management.py
Covers:
- Task 1: create N children and wait
- Task 2: exec / run commands from children
- Task 3: zombie & orphan demos
- Task 4: inspect /proc/[pid]
- Task 5: prioritization via os.nice()
Run: python3 process_management.py --task <1|2|3|4|5> [options]
"""
import os
import sys
import time
import subprocess
import argparse
import shlex
import platform
from pathlib import Path

def ensure_linux():
    if platform.system() != "Linux":
        print("WARNING: This script requires Linux (os.fork and /proc). Exiting.")
        sys.exit(1)

def task1_create_children(n):
    print(f"[Task 1] Parent PID: {os.getpid()}, creating {n} children", flush=True)
    children = []
    for i in range(n):
        pid = os.fork()
        if pid == 0:
            # child
            print(f"[Child] PID={os.getpid()} PPID={os.getppid()} Message='Hello from child {i+1}'", flush=True)
            time.sleep(1)
            os._exit(0)
        else:
            children.append(pid)
            print(f"[Parent] spawned child PID={pid}", flush=True)
    # parent waits
    for _ in children:
        waited_pid, status = os.wait()
        print(f"[Parent] wait() returned pid={waited_pid} status={status}", flush=True)
    print("[Task 1] All children reaped.", flush=True)

def task2_exec_children(n, cmd, use_exec=True):
    argv = shlex.split(cmd)
    print(f"[Task 2] Parent PID={os.getpid()}, running {n} children each executing: {argv}", flush=True)
    for i in range(n):
        pid = os.fork()
        if pid == 0:
            # in child
            print(f"[Child {i+1}] PID={os.getpid()} PPID={os.getppid()} ABOUT TO RUN: {argv}", flush=True)
            if use_exec:
                try:
                    os.execvp(argv[0], argv)
                except FileNotFoundError:
                    print(f"[Child {i+1}] exec failed: {argv[0]} not found", flush=True)
                    os._exit(1)
            else:
                # use subprocess instead (child will return back)
                subprocess.run(argv)
                print(f"[Child {i+1}] subprocess finished, exiting", flush=True)
                os._exit(0)
        else:
            print(f"[Parent] spawned child PID={pid} for command", flush=True)
    # parent waits for all
    while True:
        try:
            pid, status = os.wait()
            print(f"[Parent] waited pid={pid} status={status}", flush=True)
        except ChildProcessError:
            break
    print("[Task 2] All children finished.", flush=True)

def task3_zombie_demo():
    print("[Task 3 - zombie] Starting demo", flush=True)
    pid = os.fork()
    if pid == 0:
        # child: exit quickly
        print(f"[Child] PID={os.getpid()} exiting immediately (becomes zombie until parent waits).", flush=True)
        os._exit(0)
    else:
        print(f"[Parent] PID={os.getpid()} NOT calling wait() yet. Checking for defunct processes...", flush=True)
        # run ps and grep for defunct
        p = subprocess.run(["ps", "-el"], capture_output=True, text=True)
        lines = [L for L in p.stdout.splitlines() if "defunct" in L or "<defunct>" in L]
        if lines:
            print("[Parent] Found defunct lines (zombie):")
            for L in lines:
                print(L)
        else:
            print("[Parent] No defunct lines found (timing may vary). Full ps output (filtered for 'defunct'):", flush=True)
        # now wait and reap child so script ends cleanly
        time.sleep(2)
        waited = os.wait()
        print(f"[Parent] After wait(): {waited}", flush=True)
        print("[Task 3 - zombie] Demo complete.", flush=True)

def task3_orphan_demo(sleep_child=10):
    print("[Task 3 - orphan] Demo: parent will exit immediately; child will continue.", flush=True)
    pid = os.fork()
    if pid > 0:
        # parent
        print(f"[Parent] PID={os.getpid()} -> exiting immediately. Child PID={pid}", flush=True)
        os._exit(0)
    else:
        # child
        child_pid = os.getpid()
        print(f"[Child] Started. PID={child_pid} initial PPID={os.getppid()}. Sleeping {sleep_child}s...", flush=True)
        # wait to allow parent to exit and init to adopt
        time.sleep(sleep_child)
        print(f"[Child] After sleep: PID={child_pid} now PPID={os.getppid()} (should be 1 if orphaned).", flush=True)
        os._exit(0)

def task4_inspect(pid):
    print(f"[Task 4] Inspecting PID {pid}", flush=True)
    proc = Path(f"/proc/{pid}")
    if not proc.exists():
        print(f"[Task 4] /proc/{pid} does not exist. Process may not be running or you lack permission.", flush=True)
        return
    # read /proc/[pid]/status
    status_path = proc / "status"
    print("\n-- status --")
    try:
        with open(status_path, "r") as f:
            for line in f:
                if line.startswith(("Name:", "State:", "VmRSS:", "VmSize:", "Threads:")):
                    print(line.strip())
    except Exception as e:
        print("Error reading status:", e)
    # exe
    try:
        exe = os.readlink(str(proc / "exe"))
        print("\n-- exe ->", exe)
    except Exception as e:
        print("\n-- exe not readable:", e)
    # fd
    try:
        fds = list((proc / "fd").iterdir())
        print(f"\n-- {len(fds)} open file descriptors:")
        for fd in fds:
            try:
                target = os.readlink(fd)
                print(f"{fd.name} -> {target}")
            except Exception as e:
                print(f"{fd.name} -> (unreadable) {e}")
    except Exception as e:
        print("\n-- fd not accessible:", e)

def task5_priority(n_children=3, iterations=3_000_000):
    print(f"[Task 5] Spawning {n_children} CPU-bound children with different nice values.", flush=True)
    children = []
    nicelist = [0, 5, 10, 15, 19]  # typical choices; we'll take first n_children
    nicelist = nicelist[:n_children]
    for i, niceval in enumerate(nicelist):
        pid = os.fork()
        if pid == 0:
            # child
            try:
                os.nice(niceval)
            except Exception:
                pass
            imp_pid = os.getpid()
            print(f"[Child] PID={imp_pid} nice={niceval} starting work.", flush=True)
            # CPU-bound work (tunable)
            s = 0
            for k in range(iterations):
                s += (k & 1)
            print(f"[Child] PID={imp_pid} nice={niceval} finished work. result={s}", flush=True)
            os._exit(0)
        else:
            children.append(pid)
            print(f"[Parent] spawned child {pid} with target nice={niceval}", flush=True)
    # parent waits and logs finish order as they exit
    order = []
    try:
        while True:
            pid, status = os.wait()
            order.append(pid)
            print(f"[Parent] Child finished: pid={pid} status={status}", flush=True)
    except ChildProcessError:
        pass
    print("[Task 5] Finish order (PIDs):", order, flush=True)

def main():
    ensure_linux()
    parser = argparse.ArgumentParser(description="OS Lab tasks: fork/exec/zombie/orphan/proc/nice")
    parser.add_argument("--task", required=True, choices=["1","2","3z","3o","4","5"], help="which task: 1, 2, 3z (zombie), 3o (orphan), 4, 5")
    parser.add_argument("--n", type=int, default=3, help="number of child processes")
    parser.add_argument("--cmd", type=str, default="ls -l", help="command for task2 (quoted)")
    parser.add_argument("--pid", type=int, help="pid for task4")
    parser.add_argument("--iterations", type=int, default=2_000_000, help="work iterations for task5 (lower on weak machines)")
    args = parser.parse_args()

    if args.task == "1":
        task1_create_children(args.n)
    elif args.task == "2":
        task2_exec_children(args.n, args.cmd, use_exec=True)
    elif args.task == "3z":
        task3_zombie_demo()
    elif args.task == "3o":
        task3_orphan_demo(sleep_child=10)
    elif args.task == "4":
        if not args.pid:
            print("Please provide --pid <pid> for task 4", flush=True)
            sys.exit(1)
        task4_inspect(args.pid)
    elif args.task == "5":
        task5_priority(args.n, args.iterations)
    else:
        print("Unknown task", flush=True)

if __name__ == "__main__":
    main()
