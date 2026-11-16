# JSPM UNIVERSITY, PUNE - Operating System Practical Examination
# SET 3  |  Q.1 (30 Marks)  |  Group A - Process Scheduling (Round Robin and Priority)
# Programme: B.Tech - Computer Science and Engineering
#
# Question Statement:
# Implement Round Robin (time quantum = 3) and Priority (non-preemptive, lower
# number = higher priority) scheduling for processes all arriving at time 0:
# P1: BT=10, Pr=3; P2: BT=1, Pr=1; P3: BT=2, Pr=4; P4: BT=1, Pr=5; P5: BT=5,
# Pr=2. Display the Gantt chart, turnaround time and waiting time of each
# process, and the average waiting time and average turnaround time for both
# algorithms. Identify the optimal schedule.
"""SET 3 : Round Robin (time quantum = 3) and Priority (non-preemptive) scheduling
All processes arrive at time 0. Lower priority number = higher priority."""
from collections import deque

# (name, arrival, burst, priority)
PROCESSES = [("P1", 0, 10, 3), ("P2", 0, 1, 1), ("P3", 0, 2, 4),
             ("P4", 0, 1, 5), ("P5", 0, 5, 2)]
QUANTUM = 3


def round_robin(procs, quantum):
    remaining = {n: bt for n, _, bt, _ in procs}
    queue = deque(n for n, _, _, _ in procs)          # all arrive at 0 -> FIFO order
    time, completion, gantt = 0, {}, []
    while queue:
        name = queue.popleft()
        run = min(quantum, remaining[name])
        gantt.append((name, time, time + run))
        time += run
        remaining[name] -= run
        if remaining[name] > 0:
            queue.append(name)                         # back of the queue
        else:
            completion[name] = time
    return completion, gantt


def priority_np(procs):
    order = sorted(procs, key=lambda p: (p[3], p[1], p[0]))   # priority, then arrival
    time, completion, gantt = 0, {}, []
    for name, at, bt, _ in order:
        time = max(time, at)
        gantt.append((name, time, time + bt))
        time += bt
        completion[name] = time
    return completion, gantt


def show(title, procs, completion, gantt):
    print(f"\n{'=' * 62}\n{title}\n{'=' * 62}")
    print("Gantt Chart:")
    print("".join(f"| {n} " for n, _, _ in gantt) + "|")
    scale = str(gantt[0][1])
    for n, _, e in gantt:
        scale += str(e).rjust(len(f"| {n} "))
    print(scale)

    print(f"\n{'Process':<9}{'AT':<5}{'BT':<5}{'Pri':<5}{'CT':<5}{'TAT':<6}{'WT':<5}")
    print("-" * 40)
    tot_tat = tot_wt = 0
    for name, at, bt, pr in sorted(procs):
        ct = completion[name]
        tat, wt = ct - at, ct - at - bt
        tot_tat += tat
        tot_wt += wt
        print(f"{name:<9}{at:<5}{bt:<5}{pr:<5}{ct:<5}{tat:<6}{wt:<5}")
    n = len(procs)
    print("-" * 40)
    print(f"Average Turnaround Time = {tot_tat / n:.2f}")
    print(f"Average Waiting Time    = {tot_wt / n:.2f}")
    return tot_wt / n, tot_tat / n


if __name__ == "__main__":
    c1, g1 = round_robin(PROCESSES, QUANTUM)
    wt1, tat1 = show(f"Round Robin (Time Quantum = {QUANTUM})", PROCESSES, c1, g1)

    c2, g2 = priority_np(PROCESSES)
    wt2, tat2 = show("Priority Scheduling (Non-Preemptive)", PROCESSES, c2, g2)

    print(f"\n{'=' * 62}\nCOMPARISON / OPTIMAL SCHEDULE\n{'=' * 62}")
    print(f"{'Algorithm':<22}{'Avg WT':<10}{'Avg TAT':<10}")
    print(f"{'Round Robin (q=3)':<22}{wt1:<10.2f}{tat1:<10.2f}")
    print(f"{'Priority (non-pre.)':<22}{wt2:<10.2f}{tat2:<10.2f}")
    best = "Round Robin" if wt1 < wt2 else "Priority" if wt2 < wt1 else "Both (equal)"
    print(f"\nOptimal schedule: {best} (lowest average waiting and turnaround time).")
