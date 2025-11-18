#!/usr/bin/env bash
set -e
echo "== Task 1: Batch Processing =="
( cd task1_batch && ./batch_run.py ) | tee ../outputs/task1_batch_output.txt

echo -e "\n== Task 2: Startup Logging =="
( cd task2_startup_logging && ./startup_logging.py ) | tee -a outputs/task2_console.txt
echo "Log file content:"
cat outputs/system_log.txt | tee -a outputs/task2_console.txt

echo -e "\n== Task 3: Syscalls & IPC =="
( cd task3_syscalls_ipc && ./os_ipc --exec ) | tee outputs/task3_exec.txt
( cd task3_syscalls_ipc && ./os_ipc --pipe ) | tee outputs/task3_pipe.txt
( cd task3_syscalls_ipc && ./py_pipe_fork.py ) | tee -a outputs/task3_pipe.txt

echo -e "\n== Task 4: VM Detection & Shell =="
( cd task4_vm_detection && ./sysinfo.sh ) | tee outputs/task4_sysinfo.txt
( cd task4_vm_detection && ./vm_detect.py ) | tee outputs/task4_vmdetect.txt

echo -e "\n== Task 5: Scheduling =="
( cd task5_cpu_scheduling && ./scheduling.py --algo fcfs ) | tee outputs/task5_fcfs.txt
( cd task5_cpu_scheduling && ./scheduling.py --algo sjf )  | tee outputs/task5_sjf.txt
( cd task5_cpu_scheduling && ./scheduling.py --algo rr --q 3 ) | tee outputs/task5_rr.txt
( cd task5_cpu_scheduling && ./scheduling.py --algo priority ) | tee outputs/task5_priority.txt

echo -e "\nAll outputs saved under: outputs/"
