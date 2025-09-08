# ==================== Imports ====================
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import heapq
import webbrowser
import os

# ==================== Grafo mejorado ====================
G = nx.DiGraph()

edges_with_attrs = [
    ('q0', 'q1', dict(latencia=30, costo=0.02, ancho_banda=50, riesgo_pirateria=1, label='auth_check')),
    ('q1', 'q2', dict(latencia=15, costo=0.01, ancho_banda=100, riesgo_pirateria=1, label='auth_valid_and_geo_match')),
    ('q1', 'q3', dict(latencia=20, costo=0.01, ancho_banda=10, riesgo_pirateria=8, label='auth_invalid')),
    ('q1', 'q4', dict(latencia=40, costo=0.02, ancho_banda=30, riesgo_pirateria=5, label='auth_valid_but_geo_mismatch')),
    ('q2', 'q5', dict(latencia=25, costo=0.05, ancho_banda=200, riesgo_pirateria=2, label='stream_attempt')),
    ('q4', 'q5', dict(latencia=35, costo=0.05, ancho_banda=80, riesgo_pirateria=4, label='stream_attempt')),
    ('q5', 'q6', dict(latencia=10, costo=0.02, ancho_banda=400, riesgo_pirateria=0, label='usuario_legitimo')),
    ('q5', 'q7', dict(latencia=12, costo=0.03, ancho_banda=400, riesgo_pirateria=9, label='usuario_pirata')),
]

G.add_edges_from([(u, v, attrs) for u, v, attrs in edges_with_attrs])

state_meanings = {
    'q0': 'Inicio',
    'q1': 'Auth Check',
    'q2': 'Geo Match',
    'q3': 'Auth Invalid',
    'q4': 'Geo Mismatch',
    'q5': 'Stream Attempt',
    'q6': 'Usuario Legal',
    'q7': 'Usuario Pirata'
}

# Posiciones para animación matplotlib
pos = nx.spring_layout(G, seed=42, k=1.0)

# ==================== Funciones de búsqueda ====================
def build_adj_for_metric(metric):
    graph = {u:{} for u in G.nodes()}
    for u, v, data in G.edges(data=True):
        val = data.get(metric, data.get('latencia', 1))
        cost = 1.0 / max(val, 1e-6) if metric == 'ancho_banda' else float(val)
        graph[u][v] = cost
    return graph

def bfs(start, goal):
    visited_order = []
    q = deque([[start]])
    visited = set([start])
    while q:
        path = q.popleft()
        node = path[-1]
        visited_order.append(node)
        if node == goal:
            return path, visited_order
        for nbr in G.successors(node):
            if nbr not in visited:
                visited.add(nbr)
                q.append(path + [nbr])
    return None, visited_order

def heuristic_adaptive(n1, n2, metric):
    (x1, y1) = pos[n1]
    (x2, y2) = pos[n2]
    eucl = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
    vals = [1.0 / max(data.get('ancho_banda',1),1e-6) if metric=='ancho_banda' else float(data.get(metric,data.get('latencia',1))) 
            for _,_,data in G.edges(data=True)]
    mean_weight = sum(vals)/len(vals) if vals else 1.0
    return eucl * mean_weight * 0.4

def astar(start, goal, metric):
    graph = build_adj_for_metric(metric)
    open_heap = []
    start_h = heuristic_adaptive(start, goal, metric)
    heapq.heappush(open_heap, (start_h, 0.0, start, [start]))
    closed = set()
    visited_order = []

    while open_heap:
        f, g, node, path = heapq.heappop(open_heap)
        if node in closed:
            continue
        visited_order.append(node)
        if node == goal:
            return path, visited_order, g
        closed.add(node)
        for nbr, w in graph.get(node, {}).items():
            if nbr in closed:
                continue
            new_g = g + w
            h = heuristic_adaptive(nbr, goal, metric)
            heapq.heappush(open_heap, (new_g+h, new_g, nbr, path+[nbr]))
    return None, visited_order, float('inf')

# ==================== Animación Matplotlib ====================
def animate_and_show(path, visited, metric, title):
    fig, ax = plt.subplots(figsize=(9,5))
    ax.set_title(f"{title} — métrica: {metric}", fontsize=14, fontweight='bold')
    ax.axis('off')

    edge_labels = {}
    for u, v, data in G.edges(data=True):
        if metric=='latencia': edge_labels[(u,v)] = f"{data['latencia']}ms"
        elif metric=='costo': edge_labels[(u,v)] = f"${data['costo']}"
        elif metric=='ancho_banda': edge_labels[(u,v)] = f"{data['ancho_banda']}Mbps"
        elif metric=='riesgo_pirateria': edge_labels[(u,v)] = f"{data['riesgo_pirateria']}/10"

    def update(i):
        ax.clear()
        ax.set_title(f"{title} — métrica: {metric}", fontsize=14, fontweight='bold')
        ax.axis('off')
        node_colors = []
        for n in G.nodes():
            if path and n in path[:max(1,i)]: node_colors.append('#2ecc71')
            elif n in visited[:i]: node_colors.append('#f39c12')
            else: node_colors.append('#3498db')
        edge_colors = []
        path_edges = set(zip(path[:i], path[1:i+1])) if path else set()
        for u,v in G.edges(): edge_colors.append('red' if (u,v) in path_edges else 'gray')

        nx.draw_networkx_nodes(G, pos, node_size=900, node_color=node_colors, edgecolors='black', linewidths=1)
        nx.draw_networkx_labels(G, pos, font_weight='bold', font_color='white')
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrows=True, arrowsize=18, width=2, connectionstyle="arc3,rad=0.12")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

    frames = max(len(visited)+1, (len(path)+1 if path else 2))
    ani = animation.FuncAnimation(fig, update, frames=frames, interval=800, repeat=False)
    plt.show()

# ==================== Mapa interactivo PyVis ====================
# ==================== Mapa interactivo PyVis ====================
def create_interactive_map(path, metric, html_name="grafo_interactivo.html"):
    from pyvis.network import Network

    net = Network(height='90vh', width='100%', directed=True, notebook=False)
    net.barnes_hut()

    # Añadir nodos
    for n in G.nodes():
        color = "#EAEAEA"
        if n == start_node: color = "#B6FFB6"
        elif n == goal_node: color = "#FFD580"
        elif n == "q6": color = "#ADD8FF"
        elif n == "q7": color = "#FFB6A6"
        net.add_node(n, label=f"{n}\n{state_meanings[n]}",
                     title=f"<b>{n}</b><br>{state_meanings[n]}", color=color)

    # Añadir aristas
    path_edge_set = set(zip(path, path[1:])) if path else set()
    for u, v, data in G.edges(data=True):
        tooltip = (f"<b>{data.get('label','')}</b><br>"
                   f"Latencia: {data.get('latencia')}ms<br>"
                   f"Costo: ${data.get('costo')}<br>"
                   f"Ancho banda: {data.get('ancho_banda')}Mbps<br>"
                   f"Riesgo piratería: {data.get('riesgo_pirateria')}/10")
        net.add_edge(u, v,
                     title=tooltip,
                     color='red' if (u,v) in path_edge_set else 'gray',
                     width=4 if (u,v) in path_edge_set else 2)

    # Generar HTML y abrir
    net.write_html(html_name)  # <-- Cambiado de net.show() a write_html()
    webbrowser.open(f"file://{os.path.abspath(html_name)}")


# ==================== Interacción principal ====================
if __name__=="__main__":
    print("==== Grafo Mejorado (Pipeline Streaming) ====")
    print("Nodos disponibles:", list(G.nodes()))
    print("==============================================================\n")

    metric = input("Elige métrica (latencia/costo/ancho_banda/riesgo_pirateria): ").strip()
    if metric not in ['latencia','costo','ancho_banda','riesgo_pirateria']: metric='latencia'

    start_node = input("Nodo de inicio (ej q0): ").strip()
    goal_node = input("Nodo objetivo (ej q6): ").strip()
    if start_node not in G.nodes() or goal_node not in G.nodes(): exit("Nodo inválido")

    bfs_path, bfs_visited = bfs(start_node, goal_node)
    adj_metric = build_adj_for_metric(metric)
    bfs_cost = sum([adj_metric[u][v] for u,v in zip(bfs_path,bfs_path[1:])]) if bfs_path else 0

        # ---------- RESULTADO BFS ----------
    print("\n--- RESULTADO BFS ---")
    print("Camino:", bfs_path)
    print(f"Costo ({metric}):", bfs_cost)
    print("Nodos explorados:", bfs_visited)
    animate_and_show(bfs_path, bfs_visited, metric, "BFS")

    # ---------- RESULTADO A* ----------
    astar_path, astar_visited, astar_cost = astar(start_node, goal_node, metric)
    print("\n--- RESULTADO A* ---")
    print("Camino:", astar_path)
    print(f"Costo ({metric}):", astar_cost)
    print("Nodos explorados:", astar_visited)
    animate_and_show(astar_path, astar_visited, metric, "A*")

    # ---------- MAPA INTERACTIVO ----------
    print("\nGenerando mapa interactivo (se abrirá en tu navegador)...")
    create_interactive_map(astar_path, metric)
    print("Mapa abierto en el navegador.")

    
