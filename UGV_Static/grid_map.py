"""
grid_map.py — 70x70 Grid Map for UGV Navigation
AI Assignment 3 | Part 2 — Static Obstacle Pathfinding

Generates a grid with random obstacles at three density levels.
Obstacles are known a-priori (static environment).

Grid symbols:
    .  = free cell
    #  = obstacle
    S  = start
    G  = goal
    *  = path taken by UGV
"""

import random

# Grid dimensions
ROWS = 70
COLS = 70

# Obstacle density levels
DENSITY_LEVELS = {
    "low":    0.20,   # 20% cells are obstacles
    "medium": 0.40,   # 40% cells are obstacles
    "high":   0.60,   # 60% cells are obstacles
}


def generate_grid(density="medium", seed=None):
    """
    Generate a 70x70 grid with random obstacles.

    Args:
        density : "low", "medium", or "high"
        seed    : random seed for reproducibility

    Returns:
        grid — 2D list of booleans (True = free, False = obstacle)
    """
    if seed is not None:
        random.seed(seed)

    obstacle_prob = DENSITY_LEVELS.get(density, 0.40)
    grid = []

    for r in range(ROWS):
        row = []
        for c in range(COLS):
            # Free cell if random > obstacle probability
            row.append(random.random() > obstacle_prob)
        grid.append(row)

    return grid


def ensure_passable(grid, start, goal):
    """Make sure start and goal cells are always free."""
    sr, sc = start
    gr, gc = goal
    grid[sr][sc] = True
    grid[gr][gc] = True
    return grid


def print_grid(grid, path=None, start=None, goal=None, max_size=40):
    """
    Print the grid to terminal.
    Limits display to max_size x max_size for readability.
    """
    path_set = set(path) if path else set()
    display_rows = min(ROWS, max_size)
    display_cols = min(COLS, max_size)

    print(f"\n  Grid ({display_rows}x{display_cols} shown of {ROWS}x{COLS}):")
    print("  " + "-" * (display_cols * 2 + 2))

    for r in range(display_rows):
        print("  |", end=" ")
        for c in range(display_cols):
            pos = (r, c)
            if pos == start:
                print("S", end=" ")
            elif pos == goal:
                print("G", end=" ")
            elif pos in path_set:
                print("*", end=" ")
            elif not grid[r][c]:
                print("#", end=" ")
            else:
                print(".", end=" ")
        print("|")

    print("  " + "-" * (display_cols * 2 + 2))
    print(f"  Legend: S=Start  G=Goal  *=Path  #=Obstacle  .=Free")


def get_neighbours(grid, row, col):
    """
    Get valid neighbouring cells (4-directional movement).
    Returns list of (row, col) tuples.
    """
    neighbours = []
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc]:
            neighbours.append((nr, nc))
    return neighbours


def get_neighbours_8dir(grid, row, col):
    """
    Get valid neighbouring cells (8-directional movement).
    Diagonal moves cost sqrt(2) ≈ 1.414
    """
    neighbours = []
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1),
                   (-1,-1),(-1,1),(1,-1),(1,1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc]:
            cost = 1.414 if abs(dr) + abs(dc) == 2 else 1.0
            neighbours.append((nr, nc, cost))
    return neighbours
