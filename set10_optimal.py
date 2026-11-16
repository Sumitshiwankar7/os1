# JSPM UNIVERSITY, PUNE - Operating System Practical Examination
# SET 10  |  Q.1 (30 Marks)  |  Group C - Optimal Page Replacement
# Programme: B.Tech - Computer Science and Engineering
#
# Question Statement:
# Implement the Optimal page replacement policy for the reference string: 1,
# 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5. Run the simulation for 3 frames and for 4
# frames. Display the frame contents after each reference, mark each reference
# as a hit or a fault, and display the total page faults and hit ratio.
# Explain why the Optimal policy is not implementable in a real operating
# system.
"""SET 10 : Optimal page replacement for 3 frames and 4 frames"""

PAGES = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]


def optimal(frames_count):
    print(f"\n{'=' * 56}\nOptimal Page Replacement - {frames_count} frames\n{'=' * 56}")
    print(f"{'Ref':<5}" + "".join(f"{'F' + str(i + 1):<5}" for i in range(frames_count)) + "Result")
    print("-" * 56)

    frames, faults = [None] * frames_count, 0
    for i, page in enumerate(PAGES):
        hit = page in frames
        if not hit:
            faults += 1
            if None in frames:
                frames[frames.index(None)] = page
            else:
                future = PAGES[i + 1:]
                # distance to next use; never used again -> infinity (best victim)
                next_use = {p: (future.index(p) if p in future else float("inf")) for p in frames}
                victim = max(frames, key=lambda p: next_use[p])
                frames[frames.index(victim)] = page
        cells = "".join(f"{('-' if f is None else f):<5}" for f in frames)
        print(f"{page:<5}{cells}{'HIT' if hit else 'FAULT'}")

    hits = len(PAGES) - faults
    print("-" * 56)
    print(f"Total references : {len(PAGES)}")
    print(f"Page faults      : {faults}")
    print(f"Page hits        : {hits}")
    print(f"Hit ratio        : {hits}/{len(PAGES)} = {hits / len(PAGES):.2f}  ({hits / len(PAGES) * 100:.1f}%)")
    return faults, hits / len(PAGES)


if __name__ == "__main__":
    print("Page reference string:", PAGES)
    results = {n: optimal(n) for n in (3, 4)}

    print(f"\n{'=' * 56}\nSUMMARY\n{'=' * 56}")
    print(f"{'Frames':<10}{'Faults':<10}{'Hit ratio':<10}")
    for n, (f, r) in results.items():
        print(f"{n:<10}{f:<10}{r:<10.2f}")

    print("""
Why the Optimal policy is not implementable in a real OS:
  Optimal replaces the page whose next use is farthest in the future. This needs
  advance knowledge of the entire future page-reference string, which an operating
  system cannot know because it depends on run-time program behaviour and user input.
  It is therefore used only as a theoretical benchmark to measure practical
  algorithms such as FIFO, LRU and Clock.""")
