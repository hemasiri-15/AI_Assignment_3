"""
astar.py — A* Search for UGV Navigation
AI Assignment 3 | Part 2 — Static Obstacle Pathfinding

A* uses f(n) = g(n) + h(n) where:
    g(n) = cost from start to current node
    h(n) = heuristic estimate from current node to goal

Heuristic used: Manhattan Distance (admissible for 4-dir movement)
                Euclidean Distance (admissible for 8-dir movement)

Reference: AIMA Chapter 3
"""

import heapq
import math
from grid_map import get_neighbours_8dir, ROWS, COLS


def heuristic_manhattan(a, b):
    """Manhattan distance — admissible for 4-directional movement."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def heuristic_euclidean(a, b):
    """Euclidean distance — admissible for 8-directional movement."""
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


def astar(grid, start, goal):
    """
    A* Search on a 2D grid (8-directional movement).

    Args:
        grid  : 2D list (True=free, False=obstacle)
        start : (row, col) tuple
        goal  : (row, col) tuple

    Returns:
        dict with keys:
            found           — True if path exists
            path            — list of (row,col) from start to goal
            path_length     — total distance in grid units
            nodes_expanded  — nodes popped from frontier
            nodes_generated — nodes added to frontier
    """
    if not grid[start[0]][start[1]]:
        return {"found": False, "error": "Start cell is an obstacle."}
    if not grid[goal[0]][goal[1]]:
        return {"found": False, "error": "Goal cell is an obstacle."}

    # Priority queue: (f_score, g_score, node, path)
    h0 = heuristic_euclidean(start, goal)
    frontier = [(h0, 0, start, [start])]
    explored = {}   # node -> best g_score seen
    nodes_expanded  = 0
    nodes_generated = 1

    while frontier:
        f, g, node, path = heapq.heappop(frontier)

        # Skip if we've explored this node with lower cost
        if node in explored and explored[node] <= g:
            continue

        explored[node] = g
        nodes_expanded += 1

        # Goal check
        if node == goal:
            return {
                "found":           True,
                "path":            path,
                "path_length":     round(g, 2),
                "nodes_expanded":  nodes_expanded,
                "nodes_generated": nodes_generated,
            }

        # Expand neighbours (8-directional)
        for nr, nc, cost in get_neighbours_8dir(grid, node[0], node[1]):
            neighbour = (nr, nc)
            new_g = g + cost
            if neighbour not in explored or explored[neighbour] > new_g:
                h = heuristic_euclidean(neighbour, goal)
                new_f = new_g + h
                heapq.heappush(frontier, (new_f, new_g, neighbour, path + [neighbour]))
                nodes_generated += 1

    return {"found": False, "error": "No path found — goal unreachable.", "nodes_expanded": nodes_expanded, "nodes_generated": nodes_generated}
