# JSPM UNIVERSITY, PUNE - Operating System Practical Examination
# SET 9  |  Q.1 (30 Marks)  |  Group C - FIFO and LRU Page Replacement
# Programme: B.Tech - Computer Science and Engineering
#
# Question Statement:
# Simulate FIFO and LRU page replacement with 3 frames for the reference
# string: 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1. Display
# the frame contents after each reference, mark each reference as a page hit
# or fault, and display the total page faults and hit ratio for both
# algorithms. State which algorithm performs better.
"""SET 9 : FIFO and LRU page replacement (3 frames)"""

PAGES = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
FRAMES = 3


def print_header(title):
    print(f"\n{'=' * 52}\n{title}\n{'=' * 52}")
    print(f"{'Ref':<5}" + "".join(f"{'F' + str(i + 1):<5}" for i in range(FRAMES)) + "Result")
    print("-" * 52)


def print_row(page, frames, hit):
    cells = "".join(f"{('-' if f is None else f):<5}" for f in frames)
    print(f"{page:<5}{cells}{'HIT' if hit else 'FAULT'}")


def summary(name, faults):
    hits = len(PAGES) - faults
    ratio = hits / len(PAGES)
    print("-" * 52)
    print(f"Total references : {len(PAGES)}")
    print(f"Page faults      : {faults}")
    print(f"Page hits        : {hits}")
    print(f"Hit ratio        : {hits}/{len(PAGES)} = {ratio:.2f}  ({ratio * 100:.1f}%)")
    print(f"Fault ratio      : {faults}/{len(PAGES)} = {faults / len(PAGES):.2f}")
    return faults, ratio


def fifo():
    print_header("FIFO Page Replacement")
    frames, pointer, faults = [None] * FRAMES, 0, 0     # pointer = oldest page (next victim)
    for page in PAGES:
        hit = page in frames
        if not hit:
            faults += 1
            frames[pointer] = page
            pointer = (pointer + 1) % FRAMES
        print_row(page, frames, hit)
    return summary("FIFO", faults)


def lru():
    print_header("LRU Page Replacement")
    frames, last_used, faults = [None] * FRAMES, {}, 0
    for time, page in enumerate(PAGES):
        hit = page in frames
        if not hit:
            faults += 1
            if None in frames:                          # free frame available
                frames[frames.index(None)] = page
            else:                                       # evict least recently used page
                victim = min(frames, key=lambda p: last_used[p])
                frames[frames.index(victim)] = page
        last_used[page] = time
        print_row(page, frames, hit)
    return summary("LRU", faults)


if __name__ == "__main__":
    print("Page reference string:", PAGES)
    print("Number of frames     :", FRAMES)

    f_faults, f_ratio = fifo()
    l_faults, l_ratio = lru()

    print(f"\n{'=' * 52}\nCOMPARISON\n{'=' * 52}")
    print(f"{'Algorithm':<12}{'Faults':<10}{'Hit ratio':<10}")
    print(f"{'FIFO':<12}{f_faults:<10}{f_ratio:<10.2f}")
    print(f"{'LRU':<12}{l_faults:<10}{l_ratio:<10.2f}")
    if f_faults < l_faults:
        print("\nFIFO performs better (fewer page faults).")
    elif l_faults < f_faults:
        print("\nLRU performs better (fewer page faults, higher hit ratio).")
    else:
        print("\nBoth algorithms perform equally.")
