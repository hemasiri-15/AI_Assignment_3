# AI Assignment 3

**Subject:** Artificial Intelligence
**Reference:** Russell & Norvig — *Artificial Intelligence: A Modern Approach (AIMA)*

---

## Table of Contents
1. [Project Structure](#project-structure)
2. [Part 1 — Dijkstra / Uniform Cost Search](#part-1--dijkstra--uniform-cost-search)
3. [How to Run](#how-to-run)
4. [Demo Output](#demo-output)
5. [References](#references)

---

## Project Structure
```
AI_Assignment_3/
│
├── README.md
├── requirements.txt
│
└── Dijkstra/
    ├── india_cities.py       # Road graph of Indian cities
    └── ucs_dijkstra.py       # Uniform Cost Search implementation
```

---

## Part 1 — Dijkstra / Uniform Cost Search

### What is Uniform Cost Search?

When actions have different costs, the obvious choice for best-first search
is to use the **path cost g(n)** as the evaluation function.

This is called:
- **Dijkstra's Algorithm** — by the theoretical computer science community
- **Uniform Cost Search (UCS)** — by the AI community

> Reference: AIMA Chapter 3 — UCS is a special case of Best-First Search where f(n) = g(n)

---

### Algorithm
```
1. Initialize frontier = priority queue with (cost=0, start_city)
2. Pop node with lowest path cost
3. If node == goal → return path
4. Mark node as explored
5. For each neighbour:
      new_cost = current_cost + edge_cost
      if neighbour not explored → add to frontier
6. Repeat until goal found or frontier empty
```

---

### Properties

| Property | Value |
|----------|-------|
| Complete | Yes (if solution exists) |
| Optimal | Yes (expands lowest cost first) |
| Time Complexity | O(b^(1 + C*/ε)) |
| Space Complexity | O(b^(1 + C*/ε)) |

Where C* = optimal solution cost, ε = minimum edge cost, b = branching factor

---

### India Road Network

The graph contains **50+ major Indian cities** with real approximate road distances.

Cities covered across all regions:

| Region | Cities |
|--------|--------|
| North | Delhi, Chandigarh, Amritsar, Jammu, Srinagar, Shimla |
| East | Kolkata, Patna, Gaya, Ranchi, Bhubaneswar, Guwahati |
| West | Mumbai, Ahmedabad, Pune, Surat, Vadodara, Goa |
| South | Chennai, Bangalore, Hyderabad, Kochi, Trivandrum, Madurai |
| Central | Bhopal, Indore, Nagpur, Jabalpur, Raipur |
| Rajasthan | Jaipur, Jodhpur, Udaipur, Ajmer |
| UP | Lucknow, Agra, Varanasi, Allahabad, Kanpur |

---

### Sample Results

| Route | Shortest Path | Distance |
|-------|--------------|----------|
| Delhi → Mumbai | Delhi → Jaipur → Ahmedabad → Mumbai | 1476 km |
| Chennai → Delhi | Chennai → Hyderabad → Nagpur → Jhansi → Gwalior → Agra → Delhi | 2101 km |
| Amritsar → Trivandrum | Amritsar → Delhi → ... → Madurai → Trivandrum | 3233 km |
| Jaipur → Kolkata | Jaipur → Agra → Kanpur → Allahabad → Varanasi → Gaya → Kolkata | 1594 km |

---

### Measures of Effectiveness

| Route | Nodes Expanded | Nodes Generated |
|-------|---------------|-----------------|
| Delhi → Mumbai | 36 | 75 |
| Chennai → Delhi | 33 | 74 |
| Bangalore → Patna | 34 | 80 |
| Amritsar → Trivandrum | 53 | 103 |
| Jaipur → Kolkata | 39 | 79 |
| Mumbai → Guwahati | 53 | 101 |

---

## How to Run

### Install dependencies
```bash
pip install -r requirements.txt
```

### Interactive mode — enter any two cities
```bash
cd Dijkstra
python3 ucs_dijkstra.py
```

### Demo mode — runs 6 preset routes
```bash
cd Dijkstra
python3 ucs_dijkstra.py demo
```

### Command line — direct query
```bash
cd Dijkstra
python3 ucs_dijkstra.py Delhi Mumbai
```

---

## Demo Output
```
UNIFORM COST SEARCH (DIJKSTRA)
From : Delhi
To   : Mumbai

Shortest Path (3 hops):
Delhi → Jaipur → Ahmedabad → Mumbai

Total Distance : 1476 km
Nodes Expanded : 36
Nodes Generated: 75
```

---

## References

1. Russell, S., & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4th Edition). Pearson.
2. Road distances sourced from open map data (approximate values).
