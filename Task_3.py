import heapq
from itertools import count
from math import inf, isfinite

class Graph:
    """Граф зі списками суміжності; за замовчуванням неорієнтований."""

    def __init__(self, directed=False):
        self.adjacency = {}
        self.directed = directed

    def add_vertex(self, vertex):
        self.adjacency.setdefault(vertex, [])

    def add_edge(self, source, target, weight):
        if not isfinite(weight) or weight < 0:
            raise ValueError("Вага ребра має бути скінченною та невід'ємною.")
        self.add_vertex(source)
        self.add_vertex(target)
        self.adjacency[source].append((target, weight))
        if not self.directed:
            self.adjacency[target].append((source, weight))

def dijkstra(graph, start):
    """Повертає відстані й попередників для всіх вершин графа.

    Недосяжні вершини мають відстань inf. Купа містить записи
    (відстань, порядковий номер, вершина), щоб не порівнювати назви
    вершин при однакових відстанях. Застарілі записи пропускаються.
    """
    if start not in graph.adjacency:
        raise ValueError("Початкова вершина відсутня у графі.")

    distances = {vertex: inf for vertex in graph.adjacency}
    predecessors = {vertex: None for vertex in graph.adjacency}
    distances[start] = 0
    sequence = count()
    heap = [(0, next(sequence), start)]

    while heap:
        current_distance, _, vertex = heapq.heappop(heap)
        if current_distance != distances[vertex]:
            continue

        for neighbor, weight in graph.adjacency[vertex]:
            candidate = current_distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                predecessors[neighbor] = vertex
                heapq.heappush(heap, (candidate, next(sequence), neighbor))

    return distances, predecessors

def reconstruct_path(predecessors, start, target):
    """Відновлює шлях за результатом Дейкстри; [] означає відсутність шляху."""
    path = []
    current = target
    while current is not None:
        path.append(current)
        if current == start:
            return path[::-1]
        current = predecessors[current]
    return []

def main():
    graph = Graph()
    for source, target, weight in (
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "C", 1),
        ("B", "D", 5),
        ("C", "D", 8),
        ("C", "E", 10),
        ("D", "E", 2),
        ("D", "F", 6),
        ("E", "F", 3),
    ):
        graph.add_edge(source, target, weight)
    graph.add_vertex("G")  # Ізольована вершина для демонстрації недосяжності.

    start = "A"
    distances, predecessors = dijkstra(graph, start)
    print(f"Найкоротші шляхи від вершини {start}:")
    for vertex, distance in distances.items():
        if distance == inf:
            print(f"{vertex}: недосяжна")
        else:
            path = reconstruct_path(predecessors, start, vertex)
            print(f"{vertex}: відстань {distance}, шлях {' -> '.join(path)}")

if __name__ == "__main__":
    main()
