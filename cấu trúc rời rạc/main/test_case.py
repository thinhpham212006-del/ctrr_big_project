from khời_tạo import Graph
from duyệt_kt import bfs, dfs, is_bipartite
from tìm_dg_ngắn import dijkstra, bellman_ford
from nâng_cao import prim, kruskal, ford_fulkerson
import time 
if __name__ == "__main__":
    print(" Đồ thị mẫu vô hướng")
    g = Graph(is_directed=False)
    edges = [
        ('A', 'B', 6), ('A', 'C', 3), ('A', 'D', 9),
        ('B', 'C', 4), ('B', 'E', 2), ('B', 'F', 7),
        ('C', 'D', 5), ('C', 'E', 8),
        ('D', 'F', 11), ('D', 'G', 14),
        ('E', 'F', 3), ('E', 'H', 10),
        ('F', 'G', 6), ('F', 'H', 5), ('F', 'I', 8),
        ('G', 'I', 9), ('G', 'J', 12),
        ('H', 'I', 4), ('I', 'J', 2)
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)

    g.draw(filename="đồ_thị_ban_đầu.png", title="đồ thị ban đầu")
    
    nodes, adj_matrix = g.get_adjacency_matrix()
    print("\n ma trận kề có trọng số -:")
    print("   ", " ".join(nodes))
    for i, row in enumerate(adj_matrix):
        print(f"{nodes[i]} {row}")

    start_n = 'A'
    print(f"\nBFS từ {start_n}: {bfs(g, start_n)}")
    print(f"DFS từ {start_n}: {dfs(g, start_n)}")

    is_bip, _ = is_bipartite(g)
    print(f"\nCó phải đồ thị 2 phía?: {is_bip}")

    src, dst = 'A', 'F'
    t0 = time.perf_counter()
    d_dist, d_path = dijkstra(g, src, dst)
    d_time = (time.perf_counter() - t0) * 1000
    t0 = time.perf_counter()
    bf_dist, bf_path = bellman_ford(g, src, dst)
    bf_time = (time.perf_counter() - t0) * 1000
    print(f"\nDijkstra ({src} -> {dst}): Khoảng cách = {d_dist}, Đường đi = {d_path} thời gian = {d_time:.4f} ms")
    print(f"Bellman-Ford ({src} -> {dst}): Khoảng cách = {bf_dist}, Đường đi = {bf_path} thời gian = {bf_time:.4f} ms")

    highlight_path = list(zip(d_path[:-1], d_path[1:])) if d_path else []
    g.draw(filename="đường_ngắn_nhất .png", highlight_edges=highlight_path, title=" đường ngắn nhất  A -> F")

    t0 = time.perf_counter()
    prim_mst = prim(g, 'A')
    prim_time = (time.perf_counter() - t0) * 1000
    t0 = time.perf_counter()
    kruskal_mst = kruskal(g)
    kruskal_time = (time.perf_counter() - t0) * 1000
    print(f"\nPrim MST Edges: {prim_mst} (Thời gian: {prim_time:.4f} ms)")
    print(f"Kruskal MST Edges: {kruskal_mst} (Thời gian: {kruskal_time:.4f} ms)")
    g.draw(filename="khung_nhỏ_nhất .png", highlight_edges=[(u, v) for u, v, w in kruskal_mst], title=" cây khung nhỏ nhất  (Kruskal)")

    print(" Đồ thị luồng cực đại (Ford-Fulkerson)")
    g_flow = Graph(is_directed=True)
    flow_edges = [
        ('S', 'A', 15), ('S', 'B', 12), ('S', 'C', 20),
        ('A', 'B', 5),  ('A', 'D', 10),
        ('B', 'C', 4),  ('B', 'D', 8),  ('B', 'E', 6),
        ('C', 'E', 14),
        ('D', 'F', 12), ('D', 'T', 10),
        ('E', 'D', 3),  ('E', 'F', 15),
        ('F', 'T', 25)
    ]
    for u, v, w in flow_edges:
        g_flow.add_edge(u, v, w)

    max_f = ford_fulkerson(g_flow, 'S', 'T')
    print(f"Luồng cực đại từ S tới T = {max_f}")
    g_flow.draw(filename="luồng_cực_đại.png", title=f"đồ thị luồng cực đại  (luồng cực đại  = {max_f})")

    print("Ứng dụng thực tế Logistics")
    logistics_net = Graph(is_directed=False)
    logistics_edges = [
        ('HN_KinhBac', 'HaiPhong_Port', 15),
        ('HN_KinhBac', 'ThaiNguyen_Base', 12),
        ('HN_KinhBac', 'ThanhHoa_Hub', 35),
        ('HaiPhong_Port', 'QuangNinh_Hub', 18),
        ('ThaiNguyen_Base', 'QuangNinh_Hub', 40),
        ('ThanhHoa_Hub', 'Vinh_Hub', 28),
        ('ThanhHoa_Hub', 'DaNang_Central', 85),
        ('Vinh_Hub', 'DaNang_Central', 65),
        ('DaNang_Central', 'QuyNhon_Port', 45),
        ('DaNang_Central', 'TayNguyen_Hub', 55),
        ('QuyNhon_Port', 'KhanhHoa_Hub', 32),
        ('TayNguyen_Hub', 'KhanhHoa_Hub', 38),
        ('TayNguyen_Hub', 'DongNai_Hub', 60),
        ('KhanhHoa_Hub', 'HCM_Central', 75),
        ('DongNai_Hub', 'HCM_Central', 10),
        ('DongNai_Hub', 'BinhDuong_Hub', 8),
        ('HCM_Central', 'BinhDuong_Hub', 12),
        ('HCM_Central', 'LongAn_Hub', 14),
        ('HCM_Central', 'CanTho_Hub', 42),
        ('BinhDuong_Hub', 'CanTho_Hub', 50),
        ('LongAn_Hub', 'CanTho_Hub', 30),
        ('CanTho_Hub', 'AnGiang_Hub', 22)
    ]
    for u, v, w in logistics_edges:
        logistics_net.add_edge(u, v, w)

    mst_solution = kruskal(logistics_net)
    total_cost = sum(w for u, v, w in mst_solution)

    print("Các tuyến cáp cần xây dựng:")
    for u, v, w in mst_solution:
        print(f"  + Kết nối {u} ------ {v} với chi phí: {w} triệu VNĐ")
    print(f"\n chi phí log tối ưu nhất: {total_cost} triệu VNĐ")

    logistics_net.draw(
        filename="logistics_mst.png", 
        highlight_edges=[(u, v) for u, v, w in mst_solution], 
        title=f"Mạng lưới cáp tối ưu (Tổng chi phí: {total_cost}M VND)"
    )