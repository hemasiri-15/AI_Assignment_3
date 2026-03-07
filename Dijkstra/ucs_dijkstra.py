"""
ucs_dijkstra.py — Uniform Cost Search (Dijkstra's Algorithm)
AI Assignment 3 | Informed Search

Uniform Cost Search expands the node with the lowest path cost.
This is identical to Dijkstra's algorithm.

Reference: AIMA Chapter 3 — Search Algorithms
           UCS is a special case of Best-First Search where f(n) = g(n)

Algorithm:
    1. Start with frontier = priority queue with (cost=0, start_city)
    2. Pop node with lowest cost
    3. If goal → return path
    4. Expand neighbours, add to frontier if not visited
    5. Repeat until goal found or frontier empty
"""

import heapq
from india_cities import INDIA_ROAD_GRAPH, get_all_cities


def uniform_cost_search(start, goal):
    """
    Uniform Cost Search (Dijkstra) from start to goal.

    Args:
        start : starting city name (string)
        goal  : destination city name (string)

    Returns:
        dict with keys:
            path          — list of cities from start to goal
            total_distance — total road distance in km
            nodes_expanded — number of nodes popped from frontier
            nodes_generated — number of nodes added to frontier
            found          — True if path exists
    """

    if start not in INDIA_ROAD_GRAPH:
        return {"found": False, "error": f"City '{start}' not found in graph."}
    if goal not in INDIA_ROAD_GRAPH:
        return {"found": False, "error": f"City '{goal}' not found in graph."}
    if start == goal:
        return {
            "found": True,
            "path": [start],
            "total_distance": 0,
            "nodes_expanded": 0,
            "nodes_generated": 1,
        }

    # Priority queue: (cost, city, path)
    frontier = [(0, start, [start])]
    explored = set()
    nodes_expanded  = 0
    nodes_generated = 1

    while frontier:
        cost, city, path = heapq.heappop(frontier)

        # Skip if already explored with lower cost
        if city in explored:
            continue

        explored.add(city)
        nodes_expanded += 1

        # Goal check
        if city == goal:
            return {
                "found":           True,
                "path":            path,
                "total_distance":  cost,
                "nodes_expanded":  nodes_expanded,
                "nodes_generated": nodes_generated,
            }

        # Expand neighbours
        for neighbour, distance in INDIA_ROAD_GRAPH.get(city, []):
            if neighbour not in explored:
                new_cost = cost + distance
                heapq.heappush(frontier, (new_cost, neighbour, path + [neighbour]))
                nodes_generated += 1

    return {"found": False, "error": f"No path found from '{start}' to '{goal}'."}


def print_result(result, start, goal):
    """Pretty print the UCS result."""
    print("\n" + "=" * 65)
    print(f"  UNIFORM COST SEARCH (DIJKSTRA)")
    print(f"  From : {start}")
    print(f"  To   : {goal}")
    print("=" * 65)

    if not result["found"]:
        print(f"  [ERROR] {result.get('error', 'No path found.')}")
        return

    path = result["path"]
    print(f"\n  Shortest Path ({len(path) - 1} hops):")
    print(f"  {' → '.join(path)}")
    print(f"\n  Total Distance : {result['total_distance']} km")
    print(f"  Nodes Expanded : {result['nodes_expanded']}")
    print(f"  Nodes Generated: {result['nodes_generated']}")
    print("=" * 65)


def run_interactive():
    """Interactive mode — user inputs start and goal cities."""
    cities = get_all_cities()

    print("\n" + "=" * 65)
    print("  INDIA ROAD NETWORK — Uniform Cost Search")
    print("  Finds shortest road distance between any two cities")
    print("=" * 65)
    print(f"\n  Available cities ({len(cities)} total):")

    # Print cities in columns
    for i, city in enumerate(cities):
        print(f"  {city:<20}", end="")
        if (i + 1) % 3 == 0:
            print()
    print("\n")

    while True:
        start = input("  Enter start city (or 'quit'): ").strip().title()
        if start.lower() == "quit":
            break

        goal = input("  Enter goal city: ").strip().title()
        if goal.lower() == "quit":
            break

        result = uniform_cost_search(start, goal)
        print_result(result, start, goal)

        another = input("\n  Search another route? (y/n): ").strip().lower()
        if another != "y":
            break

    print("\n  Thank you for using India Road Network UCS!")


def run_demo():
    """Demo mode — runs several preset routes."""
    demo_routes = [
        ("Delhi",     "Mumbai"),
        ("Chennai",   "Delhi"),
        ("Bangalore", "Patna"),
        ("Amritsar",  "Trivandrum"),
        ("Jaipur",    "Kolkata"),
        ("Mumbai",    "Guwahati"),
    ]

    print("\n" + "=" * 65)
    print("  INDIA ROAD NETWORK — UCS Demo Routes")
    print("=" * 65)

    for start, goal in demo_routes:
        result = uniform_cost_search(start, goal)
        print_result(result, start, goal)


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        # Command line: python3 ucs_dijkstra.py Delhi Mumbai
        start  = sys.argv[1].title()
        goal   = sys.argv[2].title()
        result = uniform_cost_search(start, goal)
        print_result(result, start, goal)
    elif len(sys.argv) == 2 and sys.argv[1] == "demo":
        run_demo()
    else:
        run_interactive()
