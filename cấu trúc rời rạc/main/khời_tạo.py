import collections
import matplotlib.pyplot as plt
import networkx as nx

class Graph:
    def __init__(self, is_directed=False):
        self.is_directed = is_directed
        self.nodes = set()
        self.adj_list = collections.defaultdict(list)
        self.edge_list = []

    def add_node(self, node):
        self.nodes.add(node)
        if node not in self.adj_list:
            self.adj_list[node] = []

    def add_edge(self, u, v, weight=1):
        self.add_node(u)
        self.add_node(v)
        self.adj_list[u].append((v, weight))
        self.edge_list.append((u, v, weight))
        if not self.is_directed:
            self.adj_list[v].append((u, weight))

    def draw(self, filename="graph.png", highlight_edges=None, title="Graph Visual"):
        G = nx.DiGraph() if self.is_directed else nx.Graph()
        for u in self.nodes:
            G.add_node(u)
        for u, v, w in self.edge_list:
            G.add_edge(u, v, weight=w)

        pos = nx.spring_layout(G, seed=42)
        plt.figure(figsize=(8, 6))
        plt.title(title)

        edge_colors = []
        hl_set = set(highlight_edges) if highlight_edges else set()
        
        for u, v in G.edges():
            if (u, v) in hl_set or (not self.is_directed and (v, u) in hl_set):
                edge_colors.append('red')
            else:
                edge_colors.append('black')

        nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=700)
        nx.draw_networkx_labels(G, pos, font_weight='bold')
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2, arrowsize=20 if self.is_directed else 10)
        
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.savefig(filename)
        print(f"[+] Đã lưu hình ảnh đồ thị tại: {filename}")
        plt.close()

    def get_adjacency_matrix(self):
        sorted_nodes = sorted(list(self.nodes))
        node_to_idx = {node: i for i, node in enumerate(sorted_nodes)}
        n = len(sorted_nodes)
        matrix = [[0] * n for _ in range(n)]

        for u in self.adj_list:
            for v, w in self.adj_list[u]:
                matrix[node_to_idx[u]][node_to_idx[v]] = w
        return sorted_nodes, matrix