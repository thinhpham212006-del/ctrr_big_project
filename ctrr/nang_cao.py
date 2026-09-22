import collections
import heapq

def prim(graph, start_node):
    mst_edges = []
    visited = {start_node}
    edges = [(w, start_node, v) for v, w in graph.adj_list[start_node]]
    heapq.heapify(edges)

    while edges:
        w, u, v = heapq.heappop(edges)
        if v not in visited:
            visited.add(v)
            mst_edges.append((u, v, w))
            for next_v, next_w in graph.adj_list[v]:
                if next_v not in visited:
                    heapq.heappush(edges, (next_w, v, next_v))

    return mst_edges

class DisjointSet:
    def __init__(self, nodes):
        self.parent = {n: n for n in nodes}

    def find(self, i):
        if self.parent[i] == i:
            return i
        return self.find(self.parent[i])

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            self.parent[root_u] = root_v
            return True
        return False

def kruskal(graph):
    mst_edges = []
    ds = DisjointSet(graph.nodes)
    sorted_edges = sorted(graph.edge_list, key=lambda item: item[2])

    for u, v, w in sorted_edges:
        if ds.union(u, v):
            mst_edges.append((u, v, w))
    return mst_edges

def ford_fulkerson(graph, source, sink):
    nodes = sorted(list(graph.nodes))
    n = len(nodes)
    node_map = {node: i for i, node in enumerate(nodes)}

    capacity = [[0] * n for _ in range(n)]
    initial_capacity = [[0] * n for _ in range(n)]
    
    for u, v, w in graph.edge_list:
        capacity[node_map[u]][node_map[v]] += w
        initial_capacity[node_map[u]][node_map[v]] += w

    def bfs_ff(s, t, parent):
        visited = [False] * n
        queue = collections.deque([s])
        visited[s] = True

        while queue:
            u = queue.popleft()
            for v in range(n):
                if not visited[v] and capacity[u][v] > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == t:
                        return True
        return False

    parent = [-1] * n
    max_flow = 0
    s_idx, t_idx = node_map[source], node_map[sink]

    while bfs_ff(s_idx, t_idx, parent):
        path_flow = float('Inf')
        s = t_idx
        while s != s_idx:
            path_flow = min(path_flow, capacity[parent[s]][s])
            s = parent[s]

        max_flow += path_flow
        v = t_idx
        while v != s_idx:
            u = parent[v]
            capacity[u][v] -= path_flow
            capacity[v][u] += path_flow
            v = parent[v]

    flow_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if initial_capacity[i][j] > 0:
                flow_matrix[i][j] = initial_capacity[i][j] - capacity[i][j]

    return max_flow, flow_matrix, node_map