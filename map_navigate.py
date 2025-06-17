import heapq
from collections import deque

# Graph with all cities and distances (in km) from the provided diagram
graph = {
    "Hawassa": {"Adama": 230, "Addis Ababa": 320},
    "Adama": {"Hawassa": 230, "Addis Ababa": 100},
    "Addis Ababa": {"Hawassa": 320, "Adama": 100, "Nekemt": 320, "Dire Dawa": 400, "Debre Markos": 230, "Jima": 330},
    "Nekemt": {"Addis Ababa": 320, "Gambela": 230},
    "Dire Dawa": {"Addis Ababa": 400},
    "Jima": {"Addis Ababa": 330, "Gambela": 430},
    "Gambela": {"Jima": 430, "Nekemt": 230},
    "Debre Markos": {"Addis Ababa": 230, "Bahir Dar": 110, "Dessie": 170},
    "Bahir Dar": {"Debre Markos": 110, "Gondar": 180},
    "Dessie": {"Debre Markos": 170, "Lalibela": 150},
    "Lalibela": {"Dessie": 150, "Mekele": 250},
    "Mekele": {"Lalibela": 250, "Axum": 200, "Gondar": 250},
    "Gondar": {"Bahir Dar": 180, "Mekele": 250},
    "Axum": {"Mekele": 200}
}

# Heuristic values (straight-line distances to Gondar in km, approximate)
heuristics = {
    "Hawassa": 700, "Adama": 600, "Addis Ababa": 500, "Nekemt": 550,
    "Dire Dawa": 700, "Jima": 650, "Gambela": 700, "Debre Markos": 350,
    "Bahir Dar": 150, "Dessie": 400, "Lalibela": 300, "Mekele": 250,
    "Gondar": 0, "Axum": 200
}

def get_neighbors(city, graph):
    """Return list of (neighbor, distance) pairs."""
    return graph.get(city, {}).items()

# BFS
def bfs(start, goal, graph):
    nodes_expanded = 0
    queue = deque([(start, [start])])
    visited = set()
    
    while queue:
        nodes_expanded += 1
        current, path = queue.popleft()
        if current == goal:
            return path, nodes_expanded
        if current not in visited:
            visited.add(current)
            for neighbor, _ in get_neighbors(current, graph):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    return None, nodes_expanded

# DFS
def dfs(start, goal, graph):
    nodes_expanded = 0
    stack = [(start, [start])]
    visited = set()
    
    while stack:
        nodes_expanded += 1
        current, path = stack.pop()
        if current == goal:
            return path, nodes_expanded
        if current not in visited:
            visited.add(current)
            for neighbor, _ in reversed(list(get_neighbors(current, graph))):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    return None, nodes_expanded

# IDDFS
def iddfs(start, goal, graph, max_depth=10):
    nodes_expanded = 0
    
    def dls(current, goal, path, depth, visited):
        nonlocal nodes_expanded
        nodes_expanded += 1
        if current == goal:
            return path
        if depth <= 0 or current in visited:
            return None
        visited.add(current)
        for neighbor, _ in get_neighbors(current, graph):
            if neighbor not in visited:
                result = dls(neighbor, goal, path + [neighbor], depth - 1, visited.copy())
                if result:
                    return result
        return None
    
    for depth in range(max_depth + 1):
        result = dls(start, goal, [start], depth, set())
        if result:
            return result, nodes_expanded
    return None, nodes_expanded

# UCS
def ucs(start, goal, graph):
    nodes_expanded = 0
    queue = [(0, start, [start])]  # (cost, current, path)
    visited = set()
    
    while queue:
        nodes_expanded += 1
        cost, current, path = heapq.heappop(queue)
        if current == goal:
            return path, nodes_expanded
        if current not in visited:
            visited.add(current)
            for neighbor, distance in get_neighbors(current, graph):
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + distance, neighbor, path + [neighbor]))
    return None, nodes_expanded

# Greedy Best-First Search
def greedy_best_first(start, goal, graph, heuristics):
    nodes_expanded = 0
    queue = [(heuristics[start], start, [start])]  # (heuristic, current, path)
    visited = set()
    
    while queue:
        nodes_expanded += 1
        _, current, path = heapq.heappop(queue)
        if current == goal:
            return path, nodes_expanded
        if current not in visited:
            visited.add(current)
            for neighbor, _ in get_neighbors(current, graph):
                if neighbor not in visited:
                    heapq.heappush(queue, (heuristics[neighbor], neighbor, path + [neighbor]))
    return None, nodes_expanded

# A* Search
def a_star(start, goal, graph, heuristics):
    nodes_expanded = 0
    open_list = [(heuristics[start], [start], 0)]  # (f_score, path, g_score)
    closed_list = set()
    
    while open_list:
        nodes_expanded += 1
        f_score, current_path, g_score = heapq.heappop(open_list)
        current_node = current_path[-1]
        
        if current_node == goal:
            return current_path, nodes_expanded
        
        if current_node not in closed_list:
            closed_list.add(current_node)
            for neighbor, distance in get_neighbors(current_node, graph):
                if neighbor not in closed_list:
                    new_g_score = g_score + distance
                    new_path = current_path + [neighbor]
                    h_score = heuristics[neighbor]
                    new_f_score = new_g_score + h_score
                    heapq.heappush(open_list, (new_f_score, new_path, new_g_score))
    return None, nodes_expanded

if __name__ == "__main__":
    start_city = "Hawassa"
    goal_city = "Gondar"
    
    # Run all search techniques
    searches = {
        "BFS": bfs,
        "DFS": dfs,
        "IDDFS": iddfs,
        "UCS": ucs,
        "Greedy Best-First": greedy_best_first,
        "A*": a_star
    }
    
    results = {}
    for name, search_func in searches.items():
        path, nodes_expanded = search_func(start_city, goal_city, graph, heuristics) if name in ["A*", "Greedy Best-First"] else search_func(start_city, goal_city, graph)
        if path:
            total_distance = sum(graph[path[i]][path[i + 1]] for i in range(len(path) - 1)) if name in ["UCS", "A*"] else "N/A (unweighted)"
            results[name] = {"path": path, "distance": total_distance, "nodes_expanded": nodes_expanded}
            print(f"{name}:")
            print(f"  Path: {' -> '.join(path)}")
            print(f"  Total Distance: {total_distance} km" if isinstance(total_distance, (int, float)) else f"  Total Distance: {total_distance}")
            print(f"  Nodes Expanded: {nodes_expanded}")
        else:
            print(f"{name}: No path found")
        print()
    
    # Performance Evaluation and Ranking
    # Weights: Path Cost (40%), Nodes Expanded (30%), Memory (20%), Optimality (10%)
    rankings = {}
    for name in results:
        score = 0
        # Path Cost (1 if optimal, 0 if N/A)
        score += 1 * 0.4 if isinstance(results[name]["distance"], (int, float)) and results[name]["distance"] == 840 else 0 * 0.4
        # Nodes Expanded (inverse rank, 6 = best, 1 = worst)
        node_counts = [results[alg]["nodes_expanded"] for alg in results]
        node_rank = 7 - sorted(node_counts).index(results[name]["nodes_expanded"])  # 6 to 1
        score += node_rank * 0.3 / 6  # Normalize to 0-1
        # Memory Usage (1 = low, 6 = high: BFS > UCS/A*/Greedy > DFS/IDDFS)
        memory_rank = {"BFS": 6, "DFS": 2, "IDDFS": 2, "UCS": 4, "Greedy Best-First": 4, "A*": 4}.get(name, 4)
        score += (7 - memory_rank) * 0.2 / 6  # Invert and normalize
        # Optimality (1 if guaranteed, 0 if not)
        score += 1 * 0.1 if name in ["UCS", "A*"] or name == "BFS" else 0 * 0.1
        rankings[name] = score
    
    # Sort and rank algorithms
    ranked_algorithms = sorted(rankings.items(), key=lambda x: x[1], reverse=True)
    print("Ranking of Search Algorithms (Higher Score is Better):")
    for rank, (algorithm, score) in enumerate(ranked_algorithms, 1):
        print(f"{rank}. {algorithm}: Score = {score:.2f}")