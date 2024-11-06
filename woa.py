import matplotlib.pyplot as plt
import networkx as nx
import random

# Crear el grafo con ciudades y distancias
G = nx.Graph()
cities = ["Tijuana", "Rosarito", "Ensenada", "Tecate", "Mexicali", "San Felipe", "San Quintín", "Guerrero negro"]
G.add_nodes_from(cities)
distances = {
    ("Tijuana", "Tecate"): 52,
    ("Tijuana", "Rosarito"): 20,
    ("Rosarito", "Ensenada"): 85,
    ("Tecate", "Mexicali"): 135,
    ("Mexicali", "San Felipe"): 197,
    ("Ensenada", "San Quintín"): 185,
    ("Ensenada", "San Felipe"): 246,
    ("San Quintín", "Guerrero negro"): 425,
    ("San Felipe", "Guerrero negro"): 394,
    ("Ensenada", "Tecate"): 100
}
for (city1, city2), distance in distances.items():
    G.add_edge(city1, city2, weight=distance)
    
# Definir las posiciones de los nodos para replicar la disposición de la imagen
pos = {
    "Tijuana": (0, 3),
    "Tecate": (1.5, 3),
    "Mexicali": (4, 3),
    "Rosarito": (-0.1, 1.5),
    "Ensenada": (0.5, 0),
    "San Felipe": (3.5, -1),
    "San Quintín": (0.5, -3),
    "Guerrero negro": (2, -4)
}

# Definir los colores para cada nodo
node_colors = {
    "Tijuana": "skyblue",
    "Rosarito": "lightcoral",
    "Ensenada": "lightgreen",
    "Tecate": "khaki",
    "Mexicali": "lightpink",
    "San Felipe": "lightcyan",
    "San Quintín": "lightgoldenrodyellow",
    "Guerrero negro": "lightgrey"
}
node_color_list = [node_colors[city] for city in G.nodes]

# Dibujar el grafo con las posiciones personalizadas y etiquetar las distancias
plt.figure(figsize=(12, 10))
nx.draw(
    G, pos, with_labels=True, node_size=2500, node_color=node_color_list,
    font_size=12, font_weight="bold", edge_color="black"
)
nx.draw_networkx_edge_labels(
    G, pos, edge_labels={(city1, city2): f"{distance}Km" for (city1, city2), distance in distances.items()}, font_size=10
)

plt.title("Grafo de ciudades en Baja California")
plt.show()

print("Seleccione el número correspondiente a la ciudad de inicio y la ciudad de destino:")
for idx, city in enumerate(cities):
    print(f"{idx + 1}: {city}")

start_index = int(input("Introduce el número de la ciudad de inicio: ")) - 1
end_index = int(input("Introduce el número de la ciudad de destino: ")) - 1

start_city = cities[start_index]
end_city = cities[end_index]

# Configuración del WOA
num_whales = 50  # Aumentar el número de "ballenas" para cubrir más rutas
num_iterations = 3  # Aumentar el número de iteraciones para mejorar la optimización

# Función para calcular la distancia de una ruta
def evaluate_path(path):
    distance = 0
    for i in range(len(path) - 1):
        distance += G[path[i]][path[i + 1]]['weight']
    return distance

# Generar una ruta aleatoria válida desde el inicio hasta el fin
def generate_random_valid_path():
    try:
        path = nx.shortest_path(G, source=start_city, target=end_city, weight="weight")
        random.shuffle(path[1:-1])
        return path
    except nx.NetworkXNoPath:
        return []

# Inicializar ballenas (rutas posibles)
whales = [generate_random_valid_path() for _ in range(num_whales)]
whales = [path for path in whales if path]
best_path = min(whales, key=evaluate_path)
best_distance = evaluate_path(best_path)
best_distances_over_time = [best_distance]

# Imprimir la mejor ruta inicial
evaluated_distances = [evaluate_path(whale) for whale in whales]
print(f"Ruta inicial encontrada con distancia {best_distance}: {' -> '.join(best_path)}")

# Función para visualizar todas las rutas generadas por WOA en cada iteración
def visualize_all_routes(iteration, whales, best_distance):
    plt.figure(figsize=(16, 10))

    plt.subplot(1, 2, 1)
    nx.draw(G, pos, with_labels=True, node_size=3500, node_color=node_color_list, font_size=14, font_weight="bold")
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(city1, city2): f"{distance}Km" for (city1, city2), distance in
                                                      distances.items()}, font_size=10)

    for whale in whales:
        path_edges = list(zip(whale, whale[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="blue", width=1.5, alpha=0.3)

    plt.title(f"Iteración {iteration}\nMejor distancia hasta ahora: {best_distance} Km")

    plt.subplot(1, 2, 2)
    plt.plot(best_distances_over_time, color="blue", marker="o", markersize=4)
    plt.xlabel("Iteración")
    plt.ylabel("Distancia de la mejor ruta")
    plt.title("Convergencia de la distancia de la mejor ruta")

    plt.subplots_adjust(wspace=0.5)
    plt.tight_layout()
    plt.pause(0.5)
    plt.clf()

# Ejecución del WOA en el grafo
all_routes = []
for iteration in range(num_iterations):
    a = 2 - iteration * (2 / num_iterations)
    for i, whale in enumerate(whales):
        r = random.random()
        A = 2 * a * r - a
        C = 2 * r

        # Generar una nueva ruta aleatoria para explorar más caminos
        random_path = generate_random_valid_path()
        if evaluate_path(random_path) < evaluate_path(whale):
            whales[i] = random_path

    current_best_path = min(whales, key=evaluate_path)
    current_best_distance = evaluate_path(current_best_path)
    if current_best_distance < best_distance:
        best_path = current_best_path
        best_distance = current_best_distance
        print(f"Nueva mejor ruta encontrada en iteración {iteration + 1} con distancia {best_distance}: {' -> '.join(best_path)}")
    all_routes.append((iteration + 1, current_best_path, current_best_distance))

    best_distances_over_time.append(best_distance)
    visualize_all_routes(iteration + 1, whales, best_distance)

# Mostrar reporte de todas las soluciones encontradas
print("\nReporte de soluciones:")
print("Iteración | Ruta | Distancia")
print("-" * 50)
for iteration, route, distance in all_routes:
    print(f"{iteration:10} | {' -> '.join(route):50} | {distance:10.2f} Km")

# Visualizar la mejor ruta al final en rojo
def visualize_best_route(final_best_path, final_best_distance):
    plt.figure(figsize=(12, 10))
    nx.draw(G, pos, with_labels=True, node_size=3500, node_color=node_color_list, font_size=14, font_weight="bold")
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(city1, city2): f"{distance}Km" for (city1, city2), distance in
                                                      distances.items()}, font_size=10)

    best_path_edges = list(zip(final_best_path, final_best_path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=best_path_edges, edge_color="red", width=3)

    plt.title(f"Mejor ruta encontrada: {' -> '.join(final_best_path)}\nDistancia total: {final_best_distance} Km")
    plt.show()

print(
    f"La mejor ruta encontrada de {start_city} a {end_city} es: {' -> '.join(best_path)} con una distancia de {best_distance} Km")
visualize_best_route(best_path, best_distance)
