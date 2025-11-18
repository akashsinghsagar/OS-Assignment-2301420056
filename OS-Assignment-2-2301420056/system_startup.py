#!/usr/bin/env python3
"""
Improved system startup simulation:
- configurable number of processes
- per-process logs with timestamp, process name and PID
- SIGINT handler to gracefully terminate children (Ctrl+C)
"""
import multiprocessing
import time
import logging
import signal
import sys
import os

BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'process_log.txt')

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(processName)s[PID %(process)d] - %(message)s'
)

def system_process(task_name: str, sleep_time: float = 2.0):
    logging.info(f"{task_name} started")
    try:
        time.sleep(sleep_time)
    except Exception as e:
        logging.info(f"{task_name} interrupted: {e}")
    logging.info(f"{task_name} ended")

def install_signal_handlers(children):
    def handler(signum, frame):
        logging.info("Master received SIGINT, terminating children...")
        for p in children:
            if p.is_alive():
                p.terminate()
                logging.info(f"Requested termination of {p.name} (PID {p.pid})")
        logging.shutdown()
        sys.exit(0)
    signal.signal(signal.SIGINT, handler)

if __name__ == '__main__':
    print("System Starting...")
    logging.info("System bootstrap initiated")

    num_procs = 4  # <-- change to required number
    children = []

    for i in range(1, num_procs + 1):
        pname = f"Process-{i}"
        p = multiprocessing.Process(
            target=system_process,
            args=(pname, 2.0 + 0.5 * i),
            name=pname
        )
        children.append(p)

    install_signal_handlers(children)

    for p in children:
        p.start()
        logging.info(f"Launched {p.name} with PID {p.pid}")

    for p in children:
        p.join()
        logging.info(f"{p.name} joined (exitcode={p.exitcode})")

    logging.info("System shutdown complete")
    print("System Shutdown.")
