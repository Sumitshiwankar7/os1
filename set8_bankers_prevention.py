# JSPM UNIVERSITY, PUNE - Operating System Practical Examination
# SET 8  |  Q.1 (30 Marks)  |  Group C - Banker's Algorithm for Deadlock Prevention
# Programme: B.Tech - Computer Science and Engineering
#
# Question Statement:
# Simulate the Banker's algorithm for 4 processes (P0-P3) and 3 resource types
# (A,B,C). Allocation: P0=(0,1,0), P1=(2,0,0), P2=(3,0,3), P3=(2,1,1).
# Maximum: P0=(7,5,3), P1=(3,2,2), P2=(9,0,6), P3=(2,2,2). Available: (3,3,2).
# Calculate the Need matrix and verify the initial state is safe. Then process
# each request independently with the resource-request algorithm and display
# whether it is granted or denied with the reason: (a) P1 requests (1,0,2);
# (b) P0 requests (0,2,0); (c) P2 requests (4,0,1).
"""SET 8 : Banker's algorithm - deadlock PREVENTION (resource-request algorithm)
4 processes, 3 resource types. Each request is processed independently on the initial state."""

ALLOCATION = [[0, 1, 0], [2, 0, 0], [3, 0, 3], [2, 1, 1]]
MAXIMUM    = [[7, 5, 3], [3, 2, 2], [9, 0, 6], [2, 2, 2]]
AVAILABLE  = [3, 3, 2]
RESOURCES  = ["A", "B", "C"]
REQUESTS   = [("a", 1, [1, 0, 2]), ("b", 0, [0, 2, 0]), ("c", 2, [4, 0, 1])]   # (label, pid, request)


def calc_need(maximum, allocation):
    return [[m - a for m, a in zip(mr, ar)] for mr, ar in zip(maximum, allocation)]


def is_safe(allocation, need, available):
    n, m = len(allocation), len(available)
    work, finish, sequence = available[:], [False] * n, []
    while len(sequence) < n:
        found = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                work = [work[j] + allocation[i][j] for j in range(m)]
                finish[i] = True
                sequence.append(i)
                found = True
        if not found:
            break
    return all(finish), sequence


def request_resources(pid, request, allocation, need, available):
    m = len(available)
    if any(request[j] > need[pid][j] for j in range(m)):
        return False, f"DENIED: Request {tuple(request)} > Need {tuple(need[pid])} (exceeds maximum claim)"
    if any(request[j] > available[j] for j in range(m)):
        return False, f"DENIED: Request {tuple(request)} > Available {tuple(available)} (process must wait)"
    new_avail = [available[j] - request[j] for j in range(m)]
    new_alloc = [row[:] for row in allocation]
    new_need = [row[:] for row in need]
    for j in range(m):
        new_alloc[pid][j] += request[j]
        new_need[pid][j] -= request[j]
    safe, seq = is_safe(new_alloc, new_need, new_avail)
    if safe:
        return True, ("GRANTED: state after allocation is SAFE, safe sequence = "
                      + " -> ".join(f"P{i}" for i in seq))
    return False, "DENIED: allocation would put the system in an UNSAFE state (possible deadlock)"


if __name__ == "__main__":
    need = calc_need(MAXIMUM, ALLOCATION)
    hdr = lambda t: "".join(f"{t + r:<4}" for r in RESOURCES)
    print(f"{'Process':<9}{hdr('Al')}   {hdr('Mx')}   {hdr('Nd')}")
    print("-" * 45)
    for i in range(len(ALLOCATION)):
        print(f"{'P' + str(i):<9}{''.join(f'{v:<4}' for v in ALLOCATION[i])}   "
              f"{''.join(f'{v:<4}' for v in MAXIMUM[i])}   {''.join(f'{v:<4}' for v in need[i])}")
    print(f"\nAvailable = {tuple(AVAILABLE)}")

    print("\n--- Initial state safety check ---")
    safe, seq = is_safe(ALLOCATION, need, AVAILABLE)
    print("Initial state is", "SAFE" if safe else "UNSAFE")
    if safe:
        print("Safe sequence: <" + ", ".join(f"P{i}" for i in seq) + ">")

    print("\n--- Resource requests (each processed independently) ---")
    for label, pid, req in REQUESTS:
        granted, reason = request_resources(pid, req, ALLOCATION, need, AVAILABLE)
        print(f"({label}) P{pid} requests {tuple(req)}  ->  {reason}")
