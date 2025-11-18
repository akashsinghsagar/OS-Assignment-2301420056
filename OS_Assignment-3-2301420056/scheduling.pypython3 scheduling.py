# CPU Scheduling Algorithms: FCFS, SJF, Round Robin

def find_avg_time_fcfs(processes, burst_time):
    n = len(processes)
    waiting_time = [0] * n
    turnaround_time = [0] * n

    # Waiting time calculation
    for i in range(1, n):
        waiting_time[i] = waiting_time[i-1] + burst_time[i-1]

    # Turnaround time = waiting + burst
    for i in range(n):
        turnaround_time[i] = burst_time[i] + waiting_time[i]

    print("\n--- FCFS Scheduling ---")
    print("Process\tBurst\tWaiting\tTurnaround")
    for i in range(n):
        print(f"P{processes[i]}\t{burst_time[i]}\t{waiting_time[i]}\t{turnaround_time[i]}")

    print("Average Waiting Time:", sum(waiting_time)/n)
    print("Average Turnaround Time:", sum(turnaround_time)/n)


def find_avg_time_sjf(processes, burst_time):
    n = len(processes)
    waiting_time = [0] * n
    turnaround_time = [0] * n

    # Sort by burst time
    sorted_pairs = sorted(zip(burst_time, processes))
    burst_time = [x[0] for x in sorted_pairs]
    processes = [x[1] for x in sorted_pairs]

    for i in range(1, n):
        waiting_time[i] = waiting_time[i-1] + burst_time[i-1]

    for i in range(n):
        turnaround_time[i] = burst_time[i] + waiting_time[i]

    print("\n--- SJF Scheduling ---")
    print("Process\tBurst\tWaiting\tTurnaround")
    for i in range(n):
        print(f"P{processes[i]}\t{burst_time[i]}\t{waiting_time[i]}\t{turnaround_time[i]}")

    print("Average Waiting Time:", sum(waiting_time)/n)
    print("Average Turnaround Time:", sum(turnaround_time)/n)


def round_robin(processes, burst_time, quantum):
    n = len(processes)
    rem_bt = burst_time[:]
    t = 0  # current time
    waiting_time = [0] * n
    turnaround_time = [0] * n

    print("\n--- Round Robin Scheduling (q =", quantum, ") ---")
    print("Gantt Chart:")

    while True:
        done = True
        for i in range(n):
            if rem_bt[i] > 0:
                done = False
                if rem_bt[i] > quantum:
                    t += quantum
                    rem_bt[i] -= quantum
                    print(f"| P{processes[i]} ", end="")
                else:
                    t += rem_bt[i]
                    waiting_time[i] = t - burst_time[i]
                    rem_bt[i] = 0
                    print(f"| P{processes[i]} ", end="")
        if done:
            break
    print("|")

    for i in range(n):
        turnaround_time[i] = burst_time[i] + waiting_time[i]

    print("Process\tBurst\tWaiting\tTurnaround")
    for i in range(n):
        print(f"P{processes[i]}\t{burst_time[i]}\t{waiting_time[i]}\t{turnaround_time[i]}")

    print("Average Waiting Time:", sum(waiting_time)/n)
    print("Average Turnaround Time:", sum(turnaround_time)/n)


if __name__ == "__main__":
    processes = [1, 2, 3]
    burst_time = [5, 8, 12]  # You can change this
    quantum = 4

    find_avg_time_fcfs(processes, burst_time)
    find_avg_time_sjf(processes, burst_time)
    round_robin(processes, burst_time, quantum)



