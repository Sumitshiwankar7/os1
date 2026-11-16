# JSPM UNIVERSITY, PUNE - Operating System Practical Examination
# SET 6  |  Q.1 (30 Marks)  |  Group B - Memory Allocation Strategies
# Programme: B.Tech - Computer Science and Engineering
#
# Question Statement:
# Implement First Fit, Best Fit and Worst Fit memory allocation. Partitions
# (KB): 100, 500, 200, 300, 600. Processes (KB): P1=212, P2=417, P3=112,
# P4=426. Display the partition allocated to each process, the internal
# fragmentation, and the processes that remain unallocated for each strategy.
# Compare the three strategies and state which one utilizes memory best.
"""SET 6 : First Fit, Best Fit and Worst Fit memory allocation (fixed partitions)
One partition holds at most one process; unused space inside it = internal fragmentation."""

PARTITIONS = [100, 500, 200, 300, 600]            # KB
PROCESSES = [("P1", 212), ("P2", 417), ("P3", 112), ("P4", 426)]   # KB


def allocate(strategy):
    used = [False] * len(PARTITIONS)
    rows = []                                       # (process, size, partition no, frag)
    for name, size in PROCESSES:
        candidates = [i for i, p in enumerate(PARTITIONS) if not used[i] and p >= size]
        if not candidates:
            rows.append((name, size, None, None))
            continue
        if strategy == "First Fit":
            idx = candidates[0]
        elif strategy == "Best Fit":
            idx = min(candidates, key=lambda i: PARTITIONS[i])      # smallest that fits
        else:                                                       # Worst Fit
            idx = max(candidates, key=lambda i: PARTITIONS[i])      # largest partition
        used[idx] = True
        rows.append((name, size, idx, PARTITIONS[idx] - size))
    return rows


def show(strategy):
    rows = allocate(strategy)
    print(f"\n{'=' * 64}\n{strategy}\n{'=' * 64}")
    print(f"{'Process':<9}{'Size(KB)':<10}{'Partition':<22}{'Internal Frag(KB)':<18}")
    print("-" * 59)
    total_frag = allocated = 0
    unallocated = []
    for name, size, idx, frag in rows:
        if idx is None:
            print(f"{name:<9}{size:<10}{'NOT ALLOCATED':<22}{'-':<18}")
            unallocated.append(name)
        else:
            print(f"{name:<9}{size:<10}{f'Partition {idx + 1} ({PARTITIONS[idx]} KB)':<22}{frag:<18}")
            total_frag += frag
            allocated += size
    print("-" * 59)
    print(f"Total internal fragmentation : {total_frag} KB")
    print(f"Unallocated processes        : {', '.join(unallocated) if unallocated else 'None'}")
    util = allocated / sum(PARTITIONS) * 100
    print(f"Memory utilization           : {allocated}/{sum(PARTITIONS)} KB = {util:.2f}%")
    return len(unallocated), total_frag, util


if __name__ == "__main__":
    print("Memory partitions (KB):", PARTITIONS)
    print("Processes (KB)        :", ", ".join(f"{n}={s}" for n, s in PROCESSES))

    results = {s: show(s) for s in ("First Fit", "Best Fit", "Worst Fit")}

    print(f"\n{'=' * 64}\nCOMPARISON\n{'=' * 64}")
    print(f"{'Strategy':<12}{'Unallocated':<14}{'Int. Frag (KB)':<17}{'Utilization':<12}")
    for s, (un, fr, ut) in results.items():
        print(f"{s:<12}{un:<14}{fr:<17}{ut:.2f}%")
    best = min(results, key=lambda s: (results[s][0], results[s][1]))
    print(f"\nBest strategy for the given data: {best} "
          f"(fewest unallocated processes, highest memory utilization).")
