import heapq
import uuid
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())

def heap_to_tree(heap):
    """Будує дерево з масиву готової купи за O(n) часу й пам'яті.
    Для вузла i лівий нащадок має індекс 2*i+1, правий — 2*i+2.
    Порядок елементів зберігається; порожня купа повертає None.
    """
    nodes = [Node(value) for value in heap]
    for index, node in enumerate(nodes):
        left_index = 2 * index + 1
        right_index = 2 * index + 2
        if left_index < len(nodes):
            node.left = nodes[left_index]
        if right_index < len(nodes):
            node.right = nodes[right_index]
    return nodes[0] if nodes else None

def add_edges(graph, node, pos, x=0, y=0, layer=1):
    """Рекурсивно додає вузли, ребра та координати для малювання."""
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        pos[node.id] = (x, y)
        if node.left is not None:
            graph.add_edge(node.id, node.left.id)
            add_edges(graph, node.left, pos, x - 1 / 2 ** layer,
                      y - 1, layer + 1)
        if node.right is not None:
            graph.add_edge(node.id, node.right.id)
            add_edges(graph, node.right, pos, x + 1 / 2 ** layer,
                      y - 1, layer + 1)
    return graph

def draw_tree(tree_root):
    """Відображає дерево; порожнє дерево показує як порожню купу."""
    tree = nx.DiGraph()
    pos = {}
    add_edges(tree, tree_root, pos)
    colors = [data["color"] for _, data in tree.nodes(data=True)]
    labels = {node_id: data["label"] for node_id, data in tree.nodes(data=True)}

    _, axes = plt.subplots(figsize=(10, 6))
    axes.set_title("Бінарна купа" if tree_root is not None else "Купа порожня")
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2000,
            node_color=colors, ax=axes)
    plt.show()

def visualize_heap(heap):
    """Візуалізує готову мінімальну або максимальну бінарну купу."""
    draw_tree(heap_to_tree(heap))

def main():
    heap = [10, 4, 5, 0, 1, 3, 3]
    heapq.heapify(heap)
    print("Масив мінімальної купи:", heap)
    visualize_heap(heap)

if __name__ == "__main__":
    main()
