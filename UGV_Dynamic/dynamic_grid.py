"""
dynamic_grid.py — Dynamic Obstacle Grid for UGV Navigation
AI Assignment 3 | Part 3 — Dynamic Obstacle Pathfinding

Differences from static grid:
- Obstacles are NOT all known a-priori
- Hidden obstacles are revealed as UGV moves within sensor range
- New obstacles can also appear dynamically during navigation

Grid symbols:
    .  = free cell (known)
    #  = obstacle (known)
    ?  = unknown cell (not yet sensed)
    S  = start
    G  = goal
    *  = path taken
    @  = UGV current position
"""

import random

ROWS = 70
COLS = 70

DENSITY_LEVELS = {
    "low":    0.20,
    "medium": 0.40,
    "high":   0.60,
}

SENSOR_RANGE = 5   # UGV can sense obstacles within 5 cells


def generate_full_grid(density="medium", seed=None):
    """
    Generate the TRUE grid (with all obstacles).
    UGV does not know this — it discovers as it moves.
    """
    if seed is not None:
        random.seed(seed)

    obstacle_prob = DENSITY_LEVELS.get(density, 0.40)
    grid = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(random.random() > obstacle_prob)
        grid.append(row)
    return grid


def generate_known_grid():
    """
    Generate UGV's known grid — initially all unknown.
    True = free, False = obstacle, None = unknown
    """
    return [[None for _ in range(COLS)] for _ in range(ROWS)]


def ensure_passable(true_grid, start, goal):
    """Make sure start and goal are always free."""
    true_grid[start[0]][start[1]] = True
    true_grid[goal[0]][goal[1]]   = True
    return true_grid


def sense_environment(true_grid, known_grid, position, sensor_range=SENSOR_RANGE):
    """
    Update known_grid based on what UGV can sense
    from current position within sensor_range.

    Returns list of newly discovered obstacles.
    """
    r, c = position
    new_obstacles = []

    for dr in range(-sensor_range, sensor_range + 1):
        for dc in range(-sensor_range, sensor_range + 1):
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if known_grid[nr][nc] is None:
                    known_grid[nr][nc] = true_grid[nr][nc]
                    if not true_grid[nr][nc]:
                        new_obstacles.append((nr, nc))

    return new_obstacles


def add_dynamic_obstacle(true_grid, known_grid, exclude=None):
    """
    Randomly add a new obstacle to the true grid
    (simulates dynamic environment change).
    Only adds to cells not yet known to UGV.
    Returns position of new obstacle or None.
    """
    exclude = exclude or set()
    attempts = 0
    while attempts < 100:
        r = random.randint(0, ROWS - 1)
        c = random.randint(0, COLS - 1)
        if (r, c) not in exclude and known_grid[r][c] is None:
            true_grid[r][c] = False
            return (r, c)
        attempts += 1
    return None


def print_known_grid(known_grid, path=None, visited=None,
                     start=None, goal=None, ugv_pos=None, max_size=40):
    """Print UGV's known view of the grid."""
    path_set    = set(path)    if path    else set()
    visited_set = set(visited) if visited else set()

    display_rows = min(ROWS, max_size)
    display_cols = min(COLS, max_size)

    print(f"\n  UGV Known Grid ({display_rows}x{display_cols} of {ROWS}x{COLS}):")
    print("  " + "-" * (display_cols * 2 + 2))

    for r in range(display_rows):
        print("  |", end=" ")
        for c in range(display_cols):
            pos = (r, c)
            if pos == ugv_pos:
                print("@", end=" ")
            elif pos == start:
                print("S", end=" ")
            elif pos == goal:
                print("G", end=" ")
            elif pos in path_set:
                print("*", end=" ")
            elif pos in visited_set:
                print("~", end=" ")
            elif known_grid[r][c] is None:
                print("?", end=" ")
            elif not known_grid[r][c]:
                print("#", end=" ")
            else:
                print(".", end=" ")
        print("|")

    print("  " + "-" * (display_cols * 2 + 2))
    print("  Legend: @=UGV  S=Start  G=Goal  *=Path  ~=Visited  #=Obstacle  ?=Unknown")
