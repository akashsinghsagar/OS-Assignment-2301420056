#!/usr/bin/env python3
"""
Task 5: FCFS, SJF (non-preemptive), Round Robin, Priority (non-preemptive).
Computes Waiting Time (WT) and Turnaround Time (TAT).

Edit the 'processes' list below or pass via CLI quickly.
Each process: {pid, at (arrival), bt (burst), pr (priority, lower=higher priority)}
"""

from collections import deque
import argparse, json, sys

def pretty(results, title):
    print(f"\n=== {title} ===")
    print("PID  AT  BT  PR |  CT   WT   TAT")
    total_wt = total_tat = 0
    for r in results:
        print(f"{r['pid']:>3} {r['at']:>3} {r['bt']:>3} {r.get('pr','-'):>3} | {r['ct']:>3} {r['wt']:>4} {r['tat']:>5}")
        total_wt += r['wt']; total_tat += r['tat']
    n = len(results)
    print(f"Avg WT: {total_wt/n:.2f} | Avg TAT: {total_tat/n:.2f}")

def fcfs(processes):
    t = 0; res = []
    for p in sorted(processes, key=lambda x:(x['at'])):
        if t < p['at']: t = p['at']
        t += p['bt']
        ct = t
        tat = ct - p['at']
        wt = tat - p['bt']
        r = p.copy(); r.update(ct=ct, tat=tat, wt=wt)
        res.append(r)
    return res

def sjf_nonpreemptive(processes):
    procs = sorted(processes, key=lambda x:x['at'])
    t = 0; done = []; ready = []
    i = 0
    while i < len(procs) or ready:
        while i < len(procs) and procs[i]['at'] <= t:
            ready.append(procs[i]); i += 1
        if not ready:
            t = procs[i]['at']; continue
        ready.sort(key=lambda x:x['bt'])
        p = ready.pop(0)
        t += p['bt']
        ct = t
        tat = ct - p['at']
        wt = tat - p['bt']
        r = p.copy(); r.update(ct=ct, tat=tat, wt=wt)
        done.append(r)
    return done

def priority_nonpreemptive(processes):
    procs = sorted(processes, key=lambda x:x['at'])
    t = 0; done = []; ready = []
    i = 0
    while i < len(procs) or ready:
        while i < len(procs) and procs[i]['at'] <= t:
            ready.append(procs[i]); i += 1
        if not ready:
            t = procs[i]['at']; continue
        # lower 'pr' means higher priority
        ready.sort(key=lambda x:(x['pr'], x['bt']))
        p = ready.pop(0)
        t += p['bt']
        ct = t
        tat = ct - p['at']
        wt = tat - p['bt']
        r = p.copy(); r.update(ct=ct, tat=tat, wt=wt)
        done.append(r)
    return done

def round_robin(processes, q=2):
    # assume arrival time respected; RR across arrivals
    procs = sorted(processes, key=lambda x:x['at'])
    t = 0; i = 0
    ready = deque(); rem = {p['pid']:p['bt'] for p in procs}
    first_seen = set()
    done = []
    finished = set()

    def add_arrivals(time):
        nonlocal i
        while i < len(procs) and procs[i]['at'] <= time:
            ready.append(procs[i]); i += 1

    add_arrivals(0)
    if not ready and procs:
        t = procs[0]['at']; add_arrivals(t)

    while ready:
        p = ready.popleft()
        if p['pid'] not in first_seen: first_seen.add(p['pid'])
        run = min(q, rem[p['pid']])
        t += run
        rem[p['pid']] -= run
        add_arrivals(t)
        if rem[p['pid']] == 0:
            ct = t
            tat = ct - p['at']
            wt = tat - p['bt']
            r = p.copy(); r.update(ct=ct, tat=tat, wt=wt)
            done.append(r); finished.add(p['pid'])
        else:
            ready.append(p)
    return sorted(done, key=lambda x:x['pid'])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--algo", choices=["fcfs","sjf","rr","priority"], default="fcfs")
    parser.add_argument("--q", type=int, default=2, help="Round Robin time quantum")
    parser.add_argument("--procs", type=str, help='JSON list of processes')
    args = parser.parse_args()

    # Default sample
    processes = [
        {"pid":1, "at":0, "bt":5, "pr":2},
        {"pid":2, "at":1, "bt":3, "pr":1},
        {"pid":3, "at":2, "bt":8, "pr":3},
        {"pid":4, "at":3, "bt":6, "pr":2},
    ]
    if args.procs:
        processes = json.loads(args.procs)

    if args.algo == "fcfs":
        pretty(fcfs(processes), "FCFS")
    elif args.algo == "sjf":
        pretty(sjf_nonpreemptive(processes), "SJF (Non-preemptive)")
    elif args.algo == "priority":
        pretty(priority_nonpreemptive(processes), "Priority (Non-preemptive)")
    else:
        pretty(round_robin(processes, args.q), f"Round Robin (q={args.q})")

if __name__ == "__main__":
    main()
