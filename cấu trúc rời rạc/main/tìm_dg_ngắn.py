import heapq

def dijkstra(graph, start, target):
    dist = {node: float('inf') for node in graph.nodes}
    parent = {node: None for node in graph.nodes}
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == target:
            break
        for v, w in graph.adj_list[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))

    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()

    if not path or path[0] != start:
        return float('inf'), []
    return dist[target], path

def bellman_ford(graph, start, target):
    dist = {node: float('inf') for node in graph.nodes}
    parent = {node: None for node in graph.nodes}
    dist[start] = 0

    n = len(graph.nodes)
    for _ in range(n - 1):
        for u, v, w in graph.edge_list:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
            if not graph.is_directed:
                if dist[v] != float('inf') and dist[v] + w < dist[u]:
                    dist[u] = dist[v] + w
                    parent[u] = v

    for u, v, w in graph.edge_list:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            print("[!] Đồ thị chứa chu trình âm!")
            return None, []

    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()

    if not path or path[0] != start:
        return float('inf'), []
    return dist[target], path