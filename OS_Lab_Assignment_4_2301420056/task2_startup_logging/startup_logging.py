#!/usr/bin/env python3
"""
Task 2: Simulate system startup with multiprocessing and logging.
Writes log lines into outputs/system_log.txt.
"""
import multiprocessing as mp
import logging, time, os

os.makedirs("../outputs", exist_ok=True)
log_path = "../outputs/system_log.txt"
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(processName)s - %(message)s'
)

def process_task(name, delay=2):
    logging.info(f"{name} started")
    time.sleep(delay)
    logging.info(f"{name} terminated")

if __name__ == '__main__':
    print("System Booting...")
    p1 = mp.Process(target=process_task, args=("Process-1",))
    p2 = mp.Process(target=process_task, args=("Process-2",))
    p1.start(); p2.start()
    p1.join();  p2.join()
    print("System Shutdown.")
    print(f"Logs written to {os.path.abspath(log_path)}")
