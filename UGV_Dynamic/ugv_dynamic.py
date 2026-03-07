"""
ugv_dynamic.py — UGV Navigation with Dynamic Obstacles
AI Assignment 3 | Part 3

The UGV navigates a 70x70 grid where:
- Not all obstacles are known a-priori
- New obstacles can appear during navigation
- UGV must replan when path is blocked

Algorithm: Replanning A* (simplified D* Lite)

Usage:
    python3 ugv_dynamic.py          # interactive
    python3 ugv_dynamic.py demo     # demo all density levels
"""

import time
import sys
import random
from dynamic_grid import (
    generate_full_grid, generate_known_grid,
    ensure_passable, sense_environment,
    add_dynamic_obstacle, print_known_grid,
    ROWS, COLS, SENSOR_RANGE
)
from replan_astar import astar_known, path_blocked


def run_simulation(density, start, goal, seed=42,
                   dynamic_obstacles=True, verbose=True):
    """Run one UGV dynamic simulation."""

    if verbose:
        print(f"\n{'='*65}")
        print(f"  UGV NAVIGATION — Dynamic Obstacles")
        print(f"  Density  : {density.upper()}")
        print(f"  Start    : {start}  |  Goal: {goal}")
        print(f"  Dynamic  : {'Yes — obstacles appear during navigation' if dynamic_obstacles else 'No'}")
        print(f"  Sensor   : {SENSOR_RANGE} cell range")
        print(f"{'='*65}")

    # Setup
    random.seed(seed)
    true_grid  = generate_full_grid(density=density, seed=seed)
    true_grid  = ensure_passable(true_grid, start, goal)
    known_grid = generate_known_grid()

    # Metrics
    total_steps        = 0
    total_replans      = 0
    total_nodes_exp    = 0
    total_path_length  = 0.0
    dynamic_obs_added  = 0
    visited            = []

    t_start = time.perf_counter()

    # Initial sense
    sense_environment(true_grid, known_grid, start)

    # Initial plan
    path, _, nodes_exp, _ = astar_known(known_grid, start, goal)
    total_nodes_exp += nodes_exp

    if path is None:
        if verbose:
            print(f"\n  [ERROR] No initial path found.")
        return {"found": False, "error": "No initial path found."}

    current_pos  = start
    current_path = path
    path_idx     = 0
    final_path   = [start]

    # Navigation loop
    while current_pos != goal:

        # Move one step along current path
        if path_idx + 1 >= len(current_path):
            if verbose:
                print(f"\n  [ERROR] Path exhausted before reaching goal.")
            break

        next_pos = current_path[path_idx + 1]
        nr, nc   = next_pos

        # Check if next step is actually free
        if known_grid[nr][nc] is False:
            # Blocked — replan
            total_replans += 1
            path, _, nodes_exp, _ = astar_known(known_grid, current_pos, goal)
            total_nodes_exp += nodes_exp

            if path is None:
                if verbose:
                    print(f"\n  No path found after replan {total_replans}.")
                break

            current_path = path
            path_idx     = 0
            continue

        # Move to next position
        # Calculate step cost
        dr = abs(nr - current_pos[0])
        dc = abs(nc - current_pos[1])
        step_cost = 1.414 if dr + dc == 2 else 1.0

        current_pos       = next_pos
        path_idx         += 1
        total_steps      += 1
        total_path_length = round(total_path_length + step_cost, 3)
        visited.append(current_pos)
        final_path.append(current_pos)

        # Sense environment from new position
        new_obs = sense_environment(true_grid, known_grid, current_pos)

        # Add random dynamic obstacle occasionally
        if dynamic_obstacles and total_steps % 15 == 0:
            protected = set(final_path) | {goal}
            obs = add_dynamic_obstacle(true_grid, known_grid, exclude=protected)
            if obs:
                dynamic_obs_added += 1

        # Replan if new obstacles found on remaining path
        if new_obs and path_blocked(known_grid, current_path, path_idx):
            total_replans += 1
            path, _, nodes_exp, _ = astar_known(known_grid, current_pos, goal)
            total_nodes_exp += nodes_exp

            if path is None:
                if verbose:
                    print(f"\n  No path after replan {total_replans}.")
                break

            current_path = path
            path_idx     = 0

        # Safety limit
        if total_steps > ROWS * COLS:
            if verbose:
                print(f"\n  [WARNING] Step limit reached.")
            break

    t_end   = time.perf_counter()
    elapsed = round((t_end - t_start) * 1000, 3)
    found   = (current_pos == goal)

    # Print final grid
    if verbose:
        print_known_grid(known_grid, path=final_path,
                        visited=visited, start=start,
                        goal=goal, ugv_pos=current_pos)

        print(f"\n  {'─'*45}")
        print(f"  MEASURES OF EFFECTIVENESS")
        print(f"  {'─'*45}")
        print(f"  Status             : {'GOAL REACHED ✓' if found else 'FAILED ✗'}")
        print(f"  Total Steps        : {total_steps}")
        print(f"  Path Length        : {total_path_length} grid units")
        print(f"  Replans Triggered  : {total_replans}")
        print(f"  Total Nodes Exp    : {total_nodes_exp}")
        print(f"  Dynamic Obs Added  : {dynamic_obs_added}")
        print(f"  Time Taken         : {elapsed} ms")
        print(f"  {'─'*45}")

    return {
        "found":            found,
        "steps":            total_steps,
        "path_length":      total_path_length,
        "replans":          total_replans,
        "nodes_expanded":   total_nodes_exp,
        "dynamic_obs":      dynamic_obs_added,
        "time_ms":          elapsed,
    }


def run_demo():
    """Demo: compare static-only vs dynamic obstacles."""
    start = (5, 5)
    goal  = (64, 64)

    print("\n" + "="*65)
    print("  UGV DYNAMIC OBSTACLE NAVIGATION — DEMO")
    print("  Grid: 70x70 | Start: (5,5) | Goal: (64,64)")
    print("="*65)

    results = {}
    for density in ["low", "medium", "high"]:
        result = run_simulation(density, start, goal,
                                seed=42, dynamic_obstacles=True)
        results[density] = result

    # Comparison table
    print(f"\n{'='*65}")
    print(f"  PERFORMANCE COMPARISON — DYNAMIC OBSTACLES")
    print(f"{'='*65}")
    print(f"  {'Density':<10} {'Found':<8} {'Steps':<8} "
          f"{'Path Len':<12} {'Replans':<10} {'Nodes Exp':<12} {'Time(ms)'}")
    print(f"  {'─'*60}")
    for density, r in results.items():
        found    = "Yes" if r["found"] else "No"
        steps    = r.get("steps", "N/A")
        plen     = r.get("path_length", "N/A")
        replans  = r.get("replans", "N/A")
        nodes    = r.get("nodes_expanded", "N/A")
        ms       = r.get("time_ms", "N/A")
        print(f"  {density.capitalize():<10} {found:<8} {str(steps):<8} "
              f"{str(plen):<12} {str(replans):<10} {str(nodes):<12} {ms}")
    print(f"{'='*65}")


def run_interactive():
    """Interactive mode."""
    print("\n" + "="*65)
    print("  UGV DYNAMIC OBSTACLE NAVIGATION")
    print(f"  Grid: {ROWS}x{COLS} | Sensor range: {SENSOR_RANGE} cells")
    print("="*65)

    print("\n  Select obstacle density:")
    print("  1. Low    (20%)")
    print("  2. Medium (40%)")
    print("  3. High   (60%)")
    choice  = input("\n  Enter choice (1/2/3): ").strip()
    density = {"1":"low","2":"medium","3":"high"}.get(choice,"medium")

    sr = int(input("  Start row (0-69): ").strip())
    sc = int(input("  Start col (0-69): ").strip())
    gr = int(input("  Goal row  (0-69): ").strip())
    gc = int(input("  Goal col  (0-69): ").strip())

    start = (max(0,min(69,sr)), max(0,min(69,sc)))
    goal  = (max(0,min(69,gr)), max(0,min(69,gc)))

    run_simulation(density, start, goal)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "demo":
        run_demo()
    else:
        run_interactive()
