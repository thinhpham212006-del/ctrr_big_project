import collections

def bfs(graph, start_node):
    visited = []
    queue = collections.deque([start_node])
    seen = {start_node}

    while queue:
        curr = queue.popleft()
        visited.append(curr)
        for neighbor, _ in sorted(graph.adj_list[curr], key=lambda x: str(x[0])):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return visited

def dfs(graph, start_node):
    visited = []
    seen = set()

    def _dfs(u):
        seen.add(u)
        visited.append(u)
        for neighbor, _ in sorted(graph.adj_list[u], key=lambda x: str(x[0])):
            if neighbor not in seen:
                _dfs(neighbor)

    _dfs(start_node)
    return visited

def is_bipartite(graph):
    color = {}
    for node in graph.nodes:
        if node not in color:
            color[node] = 0
            queue = collections.deque([node])
            while queue:
                u = queue.popleft()
                for v, _ in graph.adj_list[u]:
                    if v not in color:
                        color[v] = 1 - color[u]
                        queue.append(v)
                    elif color[v] == color[u]:
                        return False, {}
    return True, color