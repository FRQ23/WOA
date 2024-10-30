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

print("Seleccione el número correspondiente a la ciudad de inicio y la ciudad de destino:")
for idx, city in enumerate(cities):
    print(f"{idx + 1}: {city}")

start_index = int(input("Introduce el número de la ciudad de inicio: ")) - 1
end_index = int(input("Introduce el número de la ciudad de destino: ")) - 1

start_city = cities[start_index]
end_city = cities[end_index]

# Configuración del WOA
num_whales = 50  # Aumentar el número de "ballenas" para cubrir más rutas
num_iterations = 100  # Aumentar el número de iteraciones para mejorar la optimización


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


# Visualizar todas las rutas generadas por WOA en cada iteración
def visualize_all_routes(iteration, whales, best_distance):
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(16, 10))

    plt.subplot(1, 2, 1)
    nx.draw(G, pos, with_labels=True, node_size=3500, node_color="lightblue", font_size=14, font_weight="bold")
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

    best_distances_over_time.append(best_distance)
    visualize_all_routes(iteration + 1, whales, best_distance)


# Visualizar la mejor ruta al final en rojo
def visualize_best_route(final_best_path, final_best_distance):
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 10))
    nx.draw(G, pos, with_labels=True, node_size=3500, node_color="lightblue", font_size=14, font_weight="bold")
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(city1, city2): f"{distance}Km" for (city1, city2), distance in
                                                      distances.items()}, font_size=10)

    best_path_edges = list(zip(final_best_path, final_best_path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=best_path_edges, edge_color="red", width=3)

    plt.title(f"Mejor ruta encontrada: {' -> '.join(final_best_path)}\nDistancia total: {final_best_distance} Km")
    plt.show()


print(
    f"La mejor ruta encontrada de {start_city} a {end_city} es: {' -> '.join(best_path)} con una distancia de {best_distance} Km")
visualize_best_route(best_path, best_distance)
