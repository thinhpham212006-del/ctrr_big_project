import collections
import heapq

# --- 1. CHU TRÌNH EULER ---
def fleury(graph, start_node):
    adj = collections.defaultdict(list)
    for u in graph.adj_list:
        for v, w in graph.adj_list[u]:
            adj[u].append(v)

    def count_dfs(u, visited):
        count = 1
        visited.add(u)
        for v in adj[u]:
            if v not in visited:
                count += count_dfs(v, visited)
        return count

    def is_valid_next_edge(u, v):
        if len(adj[u]) == 1:
            return True
        v1 = count_dfs(u, set())
        adj[u].remove(v)
        if not graph.is_directed:
            adj[v].remove(u)
        v2 = count_dfs(u, set())
        adj[u].append(v)
        if not graph.is_directed:
            adj[v].append(u)
        return False if v1 > v2 else True

    curr = start_node
    path = [curr]
    edges_in_order = []

    while len(adj[curr]) > 0:
        for v in list(adj[curr]):
            if is_valid_next_edge(curr, v):
                edges_in_order.append((curr, v))
                adj[curr].remove(v)
                if not graph.is_directed:
                    adj[v].remove(curr)
                curr = v
                path.append(curr)
                break
    return path, edges_in_order

def hierholzer(graph, start_node):
    adj = collections.defaultdict(list)
    for u in graph.adj_list:
        for v, w in graph.adj_list[u]:
            adj[u].append(v)

    curr_path = [start_node]
    circuit = []

    while curr_path:
        curr_v = curr_path[-1]
        if adj[curr_v]:
            next_v = adj[curr_v].pop()
            if not graph.is_directed:
                adj[next_v].remove(curr_v)
            curr_path.append(next_v)
        else:
            circuit.append(curr_path.pop())

    circuit.reverse()
    edges = [(circuit[i], circuit[i+1]) for i in range(len(circuit)-1)]
    return circuit, edges

# --- 2. CÂY KHUNG NHỎ NHẤT (MST) ---
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

# --- 3. LUỒNG CỰC ĐẠI ---
def ford_fulkerson(graph, source, sink):
    nodes = sorted(list(graph.nodes))
    n = len(nodes)
    node_map = {node: i for i, node in enumerate(nodes)}

    capacity = [[0] * n for _ in range(n)]
    for u, v, w in graph.edge_list:
        capacity[node_map[u]][node_map[v]] += w

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

    return max_flow