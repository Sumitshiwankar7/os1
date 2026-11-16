# JSPM UNIVERSITY, PUNE - Operating System Practical Examination
# SET 2  |  Q.1 (30 Marks)  |  Group A - Process Scheduling (FCFS and SJF)
# Programme: B.Tech - Computer Science and Engineering
#
# Question Statement:
# Implement the FCFS and SJF (non-preemptive) scheduling algorithms for: P1:
# AT=0, BT=6; P2: AT=1, BT=8; P3: AT=2, BT=7; P4: AT=3, BT=3; P5: AT=4, BT=4.
# Display the Gantt chart, completion time, turnaround time and waiting time
# of each process, and the average waiting time and average turnaround time
# for both algorithms. Identify the optimal schedule.
"""SET 2 : FCFS and SJF (non-preemptive) CPU scheduling"""

# (name, arrival time, burst time)
PROCESSES = [("P1", 0, 6), ("P2", 1, 8), ("P3", 2, 7), ("P4", 3, 3), ("P5", 4, 4)]


def fcfs(procs):
    order = sorted(procs, key=lambda p: (p[1], p[0]))
    time, result, gantt = 0, {}, []
    for name, at, bt in order:
        if time < at:
            gantt.append(("Idle", time, at))
            time = at
        start = time
        time += bt
        result[name] = (at, bt, time)
        gantt.append((name, start, time))
    return result, gantt


def sjf_non_preemptive(procs):
    remaining = list(procs)
    time, result, gantt = 0, {}, []
    while remaining:
        ready = [p for p in remaining if p[1] <= time]
        if not ready:                                   # CPU idle
            nxt = min(p[1] for p in remaining)
            gantt.append(("Idle", time, nxt))
            time = nxt
            continue
        # shortest burst first; tie -> earlier arrival, then name
        name, at, bt = min(ready, key=lambda p: (p[2], p[1], p[0]))
        start = time
        time += bt
        result[name] = (at, bt, time)
        gantt.append((name, start, time))
        remaining.remove((name, at, bt))
    return result, gantt


def show(title, result, gantt):
    print(f"\n{'=' * 60}\n{title}\n{'=' * 60}")
    print("Gantt Chart:")
    print("".join(f"| {n} " for n, _, _ in gantt) + "|")
    scale = str(gantt[0][1])
    for n, _, e in gantt:
        scale += str(e).rjust(len(f"| {n} "))
    print(scale)
    print("\nTimeline: " + "  ".join(f"{n}({s}-{e})" for n, s, e in gantt))

    print(f"\n{'Process':<9}{'AT':<5}{'BT':<5}{'CT':<5}{'TAT':<6}{'WT':<5}")
    print("-" * 35)
    tot_tat = tot_wt = 0
    for name in sorted(result):
        at, bt, ct = result[name]
        tat, wt = ct - at, ct - at - bt
        tot_tat += tat
        tot_wt += wt
        print(f"{name:<9}{at:<5}{bt:<5}{ct:<5}{tat:<6}{wt:<5}")
    n = len(result)
    print("-" * 35)
    print(f"Average Turnaround Time = {tot_tat / n:.2f}")
    print(f"Average Waiting Time    = {tot_wt / n:.2f}")
    return tot_wt / n, tot_tat / n


if __name__ == "__main__":
    r1, g1 = fcfs(PROCESSES)
    wt1, tat1 = show("FCFS Scheduling", r1, g1)

    r2, g2 = sjf_non_preemptive(PROCESSES)
    wt2, tat2 = show("SJF (Non-Preemptive) Scheduling", r2, g2)

    print(f"\n{'=' * 60}\nCOMPARISON / OPTIMAL SCHEDULE\n{'=' * 60}")
    print(f"{'Algorithm':<12}{'Avg WT':<10}{'Avg TAT':<10}")
    print(f"{'FCFS':<12}{wt1:<10.2f}{tat1:<10.2f}")
    print(f"{'SJF':<12}{wt2:<10.2f}{tat2:<10.2f}")
    if wt1 < wt2:
        best = "FCFS"
    elif wt2 < wt1:
        best = "SJF (Non-Preemptive)"
    else:
        best = "Both (equal)"
    print(f"\nOptimal schedule: {best} (lowest average waiting time).")
