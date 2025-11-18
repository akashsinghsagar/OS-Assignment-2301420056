#!/usr/bin/env python3
import multiprocessing
import time
import logging
import os

# ensure logs dir exists
os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'logs'), exist_ok=True)
LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'logs', 'process_log_minimal.txt')

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(processName)s[PID %(process)d] - %(message)s'
)

def system_process(name):
    logging.info(f"{name} started")
    time.sleep(2)
    logging.info(f"{name} ended")

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=system_process, args=('Process-1',), name='Process-1')
    p2 = multiprocessing.Process(target=system_process, args=('Process-2',), name='Process-2')
    p1.start(); logging.info(f"Launched {p1.name} PID={p1.pid}")
    p2.start(); logging.info(f"Launched {p2.name} PID={p2.pid}")
    p1.join(); logging.info(f"{p1.name} joined (exit={p1.exitcode})")
    p2.join(); logging.info(f"{p2.name} joined (exit={p2.exitcode})")
    print("Minimal: System Shutdown.")
