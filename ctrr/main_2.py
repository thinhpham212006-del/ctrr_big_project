import os
import time
from khoi_tao import Graph
from duyet_kt import bfs, dfs, is_bipartite
from tim_dg_ngan import dijkstra, bellman_ford
from nang_cao import prim, kruskal, ford_fulkerson

OUTPUT_DIR = "output_results"
DATA_FILE = "graph_data.txt"

def load_graph_data(filepath):
    graphs = {'UNDIRECTED': None, 'DIRECTED': None, 'LOGISTICS': None}
    current_type = None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                if line in ['UNDIRECTED', 'DIRECTED', 'LOGISTICS']:
                    current_type = line
                    is_directed = (current_type == 'DIRECTED')
                    graphs[current_type] = Graph(is_directed=is_directed)
                else:
                    if current_type and graphs[current_type] is not None:
                        parts = line.split(',')
                        if len(parts) == 3:
                            u = parts[0].strip()
                            v = parts[1].strip()
                            w = int(parts[2].strip())
                            graphs[current_type].add_edge(u, v, w)
    except Exception as e:
        print("Lỗi: " + str(e))
        return None
    
    return graphs

def setup_output_directory():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print("Đã tạo thư mục: " + OUTPUT_DIR)

def test_undirected_graph(g):
    print("\n" + "="*60)
    print(" ĐỒ THỊ VÔ HƯỚNG")
    print("="*60)
    
    print("Số đỉnh: " + str(len(g.nodes)) + ", Số cạnh: " + str(len(g.edge_list)))
    
    g.draw(filename=OUTPUT_DIR + "/01_undirected_graph.png", title="đồ thị vô hướng")
    
    nodes, adj_matrix = g.get_adjacency_matrix()
    print("\nMa trận kề:")
    print("    " + " ".join(str(n) for n in nodes))
    for i, row in enumerate(adj_matrix):
        print(str(nodes[i]) + "  " + str(row))
    
    start_n = 'A'
    print("\nDuyệt BFS từ đỉnh " + str(start_n) + ": " + str(bfs(g, start_n)))
    print("Duyệt DFS từ đỉnh " + str(start_n) + ": " + str(dfs(g, start_n)))
    
    is_bip, _ = is_bipartite(g)
    print("Là đồ thị hai phía: " + ("Có" if is_bip else "Không"))
    
    src, dst = 'A', 'J'
    print("\nĐường đi ngắn nhất từ " + str(src) + " đến " + str(dst) + ":")
    
    t0 = time.perf_counter()
    d_dist, d_path = dijkstra(g, src, dst)
    d_time = (time.perf_counter() - t0) * 1000
    print("Dijkstra: Khoảng cách=" + str(d_dist) + ", Đường đi=" + str(d_path) + ", Thời gian=" + str(round(d_time, 4)) + "ms")
    
    t0 = time.perf_counter()
    bf_dist, bf_path = bellman_ford(g, src, dst)
    bf_time = (time.perf_counter() - t0) * 1000
    print("Bellman-Ford: Khoảng cách=" + str(bf_dist) + ", Đường đi=" + str(bf_path) + ", Thời gian=" + str(round(bf_time, 4)) + "ms")
    
    highlight_path = list(zip(d_path[:-1], d_path[1:])) if d_path else []
    g.draw(filename=OUTPUT_DIR + "/02_shortest_path.png", highlight_edges=highlight_path, 
           title="Đường đi ngắn nhất: " + str(src) + "-" + str(dst))
    
    print("\nCây khung nhỏ nhất (MST):")
    t0 = time.perf_counter()
    prim_mst = prim(g, 'A')
    prim_time = (time.perf_counter() - t0) * 1000
    prim_cost = sum(w for _, _, w in prim_mst)
    print("Prim: Chi phí=" + str(prim_cost) + ", Thời gian=" + str(round(prim_time, 4)) + "ms")
    
    t0 = time.perf_counter()
    kruskal_mst = kruskal(g)
    kruskal_time = (time.perf_counter() - t0) * 1000
    kruskal_cost = sum(w for _, _, w in kruskal_mst)
    print("Kruskal: Chi phí=" + str(kruskal_cost) + ", Thời gian=" + str(round(kruskal_time, 4)) + "ms")
    
    g.draw(filename=OUTPUT_DIR + "/03_mst.png", 
           highlight_edges=[(u, v) for u, v, w in kruskal_mst],
           title="Cây khung nhỏ nhất - Chi phí: " + str(kruskal_cost))

def test_directed_graph(g):
    print("\n" + "="*60)
    print("ĐỒ THỊ CÓ HƯỚNG - LUỒNG CỰC ĐẠI")
    print("="*60)
    
    print("Số đỉnh: " + str(len(g.nodes)) + ", Số cạnh: " + str(len(g.edge_list)))
    
    g.draw(filename=OUTPUT_DIR + "/04_directed_graph.png", title="đồ thị có hướng")
    
    if 'S' in g.nodes and 'T' in g.nodes:
        max_f, flow_matrix, node_map = ford_fulkerson(g, 'S', 'T')
        print("Luồng cực đại (S đến T): " + str(max_f))
        
        edge_labels = {}
        highlight_edges = []

        for u, v, c in g.edge_list:
            u_idx = node_map[u]
            v_idx = node_map[v]
            f = flow_matrix[u_idx][v_idx]
            
            edge_labels[(u, v)] = f"{f}/{c}"
            if f > 0:
                highlight_edges.append((u, v))

        g.draw(
            filename=OUTPUT_DIR + "/05_max_flow.png",
            highlight_edges=highlight_edges,
            edge_custom_labels=edge_labels,
            title="Luồng cực đại: " + str(max_f)
        )

def test_logistics(g):
    print("\n" + "="*60)
    print("TỐI ƯU HÓA LOGISTICS - CÂY KHUNG NHỎ NHẤT")
    print("="*60)
    
    print("Số trung tâm (Hubs): " + str(len(g.nodes)) + ", Số tuyến đường: " + str(len(g.edge_list)))
    
    g.draw(filename=OUTPUT_DIR + "/06_logistics_graph.png", title="mạng lưới Logistics")
    
    mst = kruskal(g)
    total_cost = sum(w for _, _, w in mst)
    
    print("\nCác tuyến đường kết nối tối ưu cần xây dựng (MST):")
    for u, v, w in mst:
        print("  " + str(u) + " - " + str(v) + ": " + str(w) + " triệu VNĐ")
    print("\nTổng chi phí tối ưu: " + str(total_cost) + " triệu VNĐ")
    
    g.draw(filename=OUTPUT_DIR + "/07_logistics_mst.png",
           highlight_edges=[(u, v) for u, v, w in mst],
           title="mạng lưới Logistics tối ưu - Chi phí: " + str(total_cost) + " triệu VNĐ")

if __name__ == "__main__":
    
    
    setup_output_directory()
    
    graphs = load_graph_data(DATA_FILE)
    
    if graphs is None:
        print("Lỗi khi tải dữ liệu đồ thị")
    else:
        if graphs['UNDIRECTED'] is not None:
            test_undirected_graph(graphs['UNDIRECTED'])
        
        if graphs['DIRECTED'] is not None:
            test_directed_graph(graphs['DIRECTED'])
        
        if graphs['LOGISTICS'] is not None:
            test_logistics(graphs['LOGISTICS'])
        
        print("\n" + "="*60)
        print("Kết quả lưu tại thư mục: " + OUTPUT_DIR)
        print("="*60)