# JSPM UNIVERSITY, PUNE - Operating System Practical Examination
# SET 7  |  Q.1 (30 Marks)  |  Group C - Banker's Algorithm for Deadlock Avoidance
# Programme: B.Tech - Computer Science and Engineering
#
# Question Statement:
# Simulate the Banker's algorithm for 5 processes (P0-P4) and 3 resource types
# (A,B,C). Allocation: P0=(0,1,0), P1=(2,0,0), P2=(3,0,2), P3=(2,1,1),
# P4=(0,0,2). Maximum: P0=(7,5,3), P1=(3,2,2), P2=(9,0,2), P3=(2,2,2),
# P4=(4,3,3). Available: (3,3,2). Calculate the Need matrix, check whether the
# system is in a safe state and display the safe sequence. Then check whether
# a request by P1 for (1,0,2) can be granted immediately.
"""SET 7 : Banker's algorithm - deadlock AVOIDANCE
Need matrix, safe-state check, safe sequence, and a resource request by P1 = (1,0,2)."""

ALLOCATION = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
MAXIMUM    = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
AVAILABLE  = [3, 3, 2]
RESOURCES  = ["A", "B", "C"]


def calc_need(maximum, allocation):
    return [[m - a for m, a in zip(mr, ar)] for mr, ar in zip(maximum, allocation)]


def is_safe(allocation, need, available):
    """Safety algorithm. Returns (is_safe, safe_sequence)."""
    n, m = len(allocation), len(available)
    work, finish, sequence = available[:], [False] * n, []
    while len(sequence) < n:
        found = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                work = [work[j] + allocation[i][j] for j in range(m)]   # P(i) finishes, releases
                finish[i] = True
                sequence.append(i)
                found = True
        if not found:
            break
    return all(finish), sequence


def request_resources(pid, request, allocation, need, available):
    """Resource-request algorithm. Returns (granted, reason)."""
    m = len(available)
    if any(request[j] > need[pid][j] for j in range(m)):
        return False, "Request > Need (process exceeded its maximum claim)"
    if any(request[j] > available[j] for j in range(m)):
        return False, "Request > Available (resources not available, process must wait)"
    # pretend to allocate
    new_avail = [available[j] - request[j] for j in range(m)]
    new_alloc = [row[:] for row in allocation]
    new_need = [row[:] for row in need]
    for j in range(m):
        new_alloc[pid][j] += request[j]
        new_need[pid][j] -= request[j]
    safe, seq = is_safe(new_alloc, new_need, new_avail)
    if safe:
        return True, "System stays SAFE. Safe sequence: " + " -> ".join(f"P{i}" for i in seq)
    return False, "Granting it would leave the system in an UNSAFE state"


def print_table(allocation, maximum, need, available):
    n = len(allocation)
    hdr = lambda t: "".join(f"{t + r:<4}" for r in RESOURCES)
    print(f"{'Process':<9}{hdr('Al')}   {hdr('Mx')}   {hdr('Nd')}")
    print("-" * 45)
    for i in range(n):
        print(f"{'P' + str(i):<9}{''.join(f'{v:<4}' for v in allocation[i])}   "
              f"{''.join(f'{v:<4}' for v in maximum[i])}   {''.join(f'{v:<4}' for v in need[i])}")
    print(f"\nAvailable = {tuple(available)}")


if __name__ == "__main__":
    need = calc_need(MAXIMUM, ALLOCATION)
    print("Allocation / Maximum / Need matrices")
    print_table(ALLOCATION, MAXIMUM, need, AVAILABLE)

    print("\n--- Safety check of the initial state ---")
    safe, seq = is_safe(ALLOCATION, need, AVAILABLE)
    if safe:
        print("System is in a SAFE state.")
        print("Safe sequence: <" + ", ".join(f"P{i}" for i in seq) + ">")
    else:
        print("System is in an UNSAFE state.")

    print("\n--- Resource request: P1 requests (1,0,2) ---")
    granted, reason = request_resources(1, [1, 0, 2], ALLOCATION, need, AVAILABLE)
    print("Request GRANTED immediately." if granted else "Request DENIED.")
    print("Reason:", reason)
