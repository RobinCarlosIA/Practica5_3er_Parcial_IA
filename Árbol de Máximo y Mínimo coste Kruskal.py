import networkx as nx
import matplotlib.pyplot as plt

# Función del Algoritmo de Kruskal
def kruskal(grafo, maximizar=False):
    """
    Algoritmo de Kruskal para construir un Árbol de Expansión Mínimo o Máximo.
    Muestra el proceso paso a paso en la consola.

    Args:
        grafo: Lista de aristas en formato (peso, nodo1, nodo2).
        maximizar: Si es True, calcula el Árbol de Expansión Máximo.

    Returns:
        mst: Lista de aristas del Árbol de Expansión.
    """
    # Ordenamos las aristas por peso: de menor a mayor (Mínimo) o de mayor a menor (Máximo)
    grafo.sort(reverse=maximizar)
    mst = []  # Aquí guardaremos las aristas del Árbol de Expansión
    conjuntos = {}  # Para manejar los conjuntos disjuntos (qué nodos están conectados)

    # Inicializamos cada nodo como su propio conjunto
    nodos = set(nodo for _, nodo1, nodo2 in grafo for nodo in [nodo1, nodo2])
    for nodo in nodos:
        conjuntos[nodo] = nodo

    # Función para encontrar el conjunto al que pertenece un nodo
    def encontrar(nodo):
        # Si el nodo no es su propio representante, seguimos buscando
        if conjuntos[nodo] != nodo:
            conjuntos[nodo] = encontrar(conjuntos[nodo])  # Compactamos el camino
        return conjuntos[nodo]

    # Función para unir dos conjuntos
    def unir(nodo1, nodo2):
        conjunto1 = encontrar(nodo1)
        conjunto2 = encontrar(nodo2)
        conjuntos[conjunto1] = conjunto2  # Unimos los dos conjuntos

    print("Procesando las aristas del grafo:")
    for peso, nodo1, nodo2 in grafo:
        print(f"  Evaluando la arista {nodo1} --({peso})--> {nodo2}")
        # Si los nodos no están en el mismo conjunto, podemos agregar la arista
        if encontrar(nodo1) != encontrar(nodo2):
            mst.append((peso, nodo1, nodo2))  # Agregamos la arista al árbol
            unir(nodo1, nodo2)  # Unimos los conjuntos
            print(f"    Arista agregada al árbol.")
        else:
            print(f"    Arista rechazada (formaría un ciclo).")

    return mst

# Función para dibujar el grafo y el Árbol de Expansión
def dibujar_grafo_y_mst(grafo, mst, maximizar=False):
    """
    Dibuja el grafo original y resalta el Árbol de Expansión.

    Args:
        grafo: Lista de aristas en formato (peso, nodo1, nodo2).
        mst: Lista de aristas del Árbol de Expansión.
        maximizar: Si es True, indica que es un Árbol de Expansión Máximo.
    """
    # Creamos el grafo con NetworkX
    G = nx.Graph()
    for peso, nodo1, nodo2 in grafo:
        G.add_edge(nodo1, nodo2, weight=peso)

    pos = nx.spring_layout(G)  # Posiciones para los nodos
    pesos = nx.get_edge_attributes(G, 'weight')  # Pesos de las aristas

    # Dibujar el grafo completo
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="lightblue", font_size=10, font_weight="bold")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos)

    # Dibujar el MST
    mst_edges = [(nodo1, nodo2) for _, nodo1, nodo2 in mst]
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color="red", width=2)

    # Título del gráfico
    titulo = "Árbol de Expansión Máximo" if maximizar else "Árbol de Expansión Mínimo"
    plt.title(titulo)
    plt.show()

# Grafo con los datos de los ejemplos anteriores
grafo = [
    (2, 'R', 'E'),
    (4, 'R', 'C'),
    (7, 'E', 'G'),
    (3, 'E', 'F'),
    (1, 'C', 'F'),
    (5, 'C', 'D'),
    (2, 'G', 'D'),
    (8, 'F', 'B'),
    (6, 'D', 'B')
]

# Construcción del Árbol de Expansión Mínimo
print("=== Árbol de Expansión Mínimo ===\n")
mst_min = kruskal(grafo)
dibujar_grafo_y_mst(grafo, mst_min)

# Construcción del Árbol de Expansión Máximo
print("\n=== Árbol de Expansión Máximo ===\n")
mst_max = kruskal(grafo, maximizar=True)
dibujar_grafo_y_mst(grafo, mst_max, maximizar=True)
