"""
replan_astar.py — Replanning A* for Dynamic Obstacle Navigation
AI Assignment 3 | Part 3

Strategy:
    1. Plan initial path using A* on known grid
    2. Move along path step by step
    3. After each step, sense environment (update known grid)
    4. If new obstacle found on planned path → REPLAN from current position
    5. Repeat until goal reached or no path exists

This is a simplified version of D* Lite (Dynamic A*).

Reference: AIMA Chapter 4 — Search in Partially Observable Environments
"""

import heapq
import math
from dynamic_grid import ROWS, COLS, SENSOR_RANGE


def heuristic(a, b):
    """Euclidean distance heuristic."""
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)


def get_neighbours_8dir(known_grid, row, col):
    """Get walkable neighbours from known grid."""
    neighbours = []
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1),
                   (-1,-1),(-1,1),(1,-1),(1,1)]:
        nr, nc = row+dr, col+dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            cell = known_grid[nr][nc]
            # Treat unknown cells as free (optimistic assumption)
            if cell is True or cell is None:
                cost = 1.414 if abs(dr)+abs(dc)==2 else 1.0
                neighbours.append((nr, nc, cost))
    return neighbours


def astar_known(known_grid, start, goal):
    """
    A* on the UGV's known grid.
    Unknown cells treated as free (optimistic).
    Returns path or None.
    """
    h0       = heuristic(start, goal)
    frontier = [(h0, 0, start, [start])]
    explored = {}
    nodes_expanded  = 0
    nodes_generated = 1

    while frontier:
        f, g, node, path = heapq.heappop(frontier)

        if node in explored and explored[node] <= g:
            continue
        explored[node] = g
        nodes_expanded += 1

        if node == goal:
            return path, round(g, 2), nodes_expanded, nodes_generated

        for nr, nc, cost in get_neighbours_8dir(known_grid, node[0], node[1]):
            neighbour = (nr, nc)
            new_g = g + cost
            if neighbour not in explored or explored[neighbour] > new_g:
                new_f = new_g + heuristic(neighbour, goal)
                heapq.heappush(frontier,
                    (new_f, new_g, neighbour, path+[neighbour]))
                nodes_generated += 1

    return None, 0, nodes_expanded, nodes_generated


def path_blocked(known_grid, path, current_idx):
    """Check if any remaining path step is now blocked."""
    for pos in path[current_idx:]:
        r, c = pos
        if known_grid[r][c] is False:
            return True
    return False
