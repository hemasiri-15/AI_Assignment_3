"""
ugv_static.py — UGV Navigation with Static Obstacles
AI Assignment 3 | Part 2

Simulates an Unmanned Ground Vehicle navigating a 70x70 grid
with known static obstacles using A* search.

Usage:
    python3 ugv_static.py          # interactive mode
    python3 ugv_static.py demo     # run all 3 density levels
"""

import time
import sys
from grid_map import generate_grid, ensure_passable, print_grid, ROWS, COLS
from astar import astar


def run_simulation(density, start, goal, seed=42):
    """Run one UGV simulation and print results."""

    print(f"\n{'='*65}")
    print(f"  UGV NAVIGATION — Static Obstacles")
    print(f"  Density : {density.upper()} ({int({'low':0.2,'medium':0.4,'high':0.6}[density]*100)}% obstacles)")
    print(f"  Start   : {start}")
    print(f"  Goal    : {goal}")
    print(f"{'='*65}")

    # Generate grid
    grid = generate_grid(density=density, seed=seed)
    grid = ensure_passable(grid, start, goal)

    # Count obstacles
    total_cells    = ROWS * COLS
    obstacle_count = sum(1 for r in range(ROWS) for c in range(COLS) if not grid[r][c])

    print(f"\n  Grid Info:")
    print(f"  Total cells    : {total_cells}")
    print(f"  Obstacle cells : {obstacle_count} ({obstacle_count*100//total_cells}%)")
    print(f"  Free cells     : {total_cells - obstacle_count}")

    # Run A* search
    t_start = time.perf_counter()
    result  = astar(grid, start, goal)
    t_end   = time.perf_counter()
    elapsed = round((t_end - t_start) * 1000, 3)

    # Print grid with path
    if result["found"]:
        print_grid(grid, path=result["path"], start=start, goal=goal)
    else:
        print_grid(grid, start=start, goal=goal)

    # Print measures of effectiveness
    print(f"\n  {'─'*45}")
    print(f"  MEASURES OF EFFECTIVENESS")
    print(f"  {'─'*45}")

    if result["found"]:
        path = result["path"]
        print(f"  Status          : PATH FOUND ✓")
        print(f"  Path Length     : {result['path_length']} grid units")
        print(f"  Path Hops       : {len(path) - 1} steps")
        print(f"  Nodes Expanded  : {result.get('nodes_expanded', 'N/A')}")
        print(f"  Nodes Generated : {result['nodes_generated']}")
        print(f"  Time Taken      : {elapsed} ms")
        print(f"  {'─'*45}")
    else:
        print(f"  Status          : NO PATH FOUND ✗")
        print(f"  Reason          : {result.get('error', 'Unknown')}")
        print(f"  Nodes Expanded  : {result.get('nodes_expanded', 'N/A')}")
        print(f"  Time Taken      : {elapsed} ms")
        print(f"  {'─'*45}")

    return result


def run_demo():
    """Demo: run all 3 density levels with same start/goal."""
    start = (5, 5)
    goal  = (64, 64)

    print("\n" + "="*65)
    print("  UGV STATIC OBSTACLE NAVIGATION — DEMO")
    print("  Testing all 3 obstacle density levels")
    print("  Grid: 70x70 | Start: (5,5) | Goal: (64,64)")
    print("="*65)

    results = {}
    for density in ["low", "medium", "high"]:
        result = run_simulation(density, start, goal, seed=42)
        results[density] = result

    # Comparison table
    print(f"\n{'='*65}")
    print(f"  PERFORMANCE COMPARISON ACROSS DENSITY LEVELS")
    print(f"{'='*65}")
    print(f"  {'Density':<10} {'Found':<8} {'Path Len':<12} {'Nodes Exp':<12} {'Time(ms)':<10}")
    print(f"  {'─'*55}")
    for density, result in results.items():
        found    = "Yes" if result["found"] else "No"
        path_len = result.get("path_length", "N/A")
        nodes    = result.get("nodes_expanded", "N/A")
        # re-run for timing
        grid = generate_grid(density=density, seed=42)
        grid = ensure_passable(grid, start, goal)
        t0 = time.perf_counter()
        astar(grid, start, goal)
        t1 = time.perf_counter()
        ms = round((t1-t0)*1000, 3)
        print(f"  {density.capitalize():<10} {found:<8} {str(path_len):<12} {str(nodes):<12} {ms:<10}")
    print(f"{'='*65}")


def run_interactive():
    """Interactive mode — user specifies start and goal."""
    print("\n" + "="*65)
    print("  UGV STATIC OBSTACLE NAVIGATION")
    print(f"  Grid size: {ROWS} x {COLS}")
    print("="*65)

    print("\n  Select obstacle density:")
    print("  1. Low    (20% obstacles)")
    print("  2. Medium (40% obstacles)")
    print("  3. High   (60% obstacles)")

    choice = input("\n  Enter choice (1/2/3): ").strip()
    density_map = {"1": "low", "2": "medium", "3": "high"}
    density = density_map.get(choice, "medium")

    print(f"\n  Enter start position (row col), range 0-69")
    sr = int(input("  Start row: ").strip())
    sc = int(input("  Start col: ").strip())

    print(f"\n  Enter goal position (row col), range 0-69")
    gr = int(input("  Goal row: ").strip())
    gc = int(input("  Goal col: ").strip())

    start = (max(0, min(69, sr)), max(0, min(69, sc)))
    goal  = (max(0, min(69, gr)), max(0, min(69, gc)))

    run_simulation(density, start, goal)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "demo":
        run_demo()
    else:
        run_interactive()
