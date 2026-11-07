import networkx as nx
from collections import deque
from Task_4 import Node, heap_to_tree

def dfs(root):
    """Обхід у глибину: корінь, ліве піддерево, праве піддерево."""
    stack = [root] if root is not None else []
    while stack:
        node = stack.pop()
        yield node
        # Правий додаємо першим, щоб лівий вийшов зі стеку першим.
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)

def bfs(root):
    """Обхід у ширину: рівень за рівнем, зліва направо."""
    queue = deque([root] if root is not None else [])
    while queue:
        node = queue.popleft()
        yield node
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)

def traversal_colors(size):
    """Унікальні HEX RGB кольори зі зростанням яскравості.
    Канали змінюються від (18, 48, 80) до (190, 235, 255).
    Палітра має 535 відтінків: кожен наступний збільшує один канал.
    """
    if not 0 <= size <= 535:
        raise ValueError("Палітра підтримує від 0 до 535 вузлів.")
    palette = []
    channels = [18, 48, 80]
    end = [190, 235, 255]
    palette.append('#{:02X}{:02X}{:02X}'.format(*channels))
    while channels != end:
        for channel in range(3):
            if channels[channel] < end[channel]:
                channels[channel] += 1
                palette.append('#{:02X}{:02X}{:02X}'.format(*channels))
    if size == 0:
        return []
    if size == 1:
        return [palette[0]]
    return [palette[i * (len(palette) - 1) // (size - 1)]
            for i in range(size)]

def tree_to_graph(root):
    """Створює граф і координати за допомогою стеку, без рекурсії."""


    graph = nx.DiGraph()
    positions = {}
    stack = [(root, 0, 0, 1)] if root is not None else []
    while stack:
        node, x, y, layer = stack.pop()
        graph.add_node(node.id, label=node.val)
        positions[node.id] = (x, y)
        for child, direction in ((node.right, 1), (node.left, -1)):
            if child is not None:
                graph.add_edge(node.id, child.id)
                stack.append((child, x + direction / 2 ** layer,
                              y - 1, layer + 1))
    return graph, positions

def visualize_traversal(root, mode="DFS", interval=800):
    """Показує початковий стан і кожне відвідування; interval — мілісекунди."""
    import networkx as nx
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    traversals = {"DFS": dfs, "BFS": bfs}
    if mode not in traversals:
        raise ValueError("Оберіть DFS або BFS.")
    if interval <= 0:
        raise ValueError("Інтервал має бути додатним.")
    order = list(traversals[mode](root))
    colors = traversal_colors(len(order))
    graph, positions = tree_to_graph(root)
    labels = nx.get_node_attributes(graph, "label")
    figure, axes = plt.subplots(figsize=(10, 6))

    def draw_frame(step):
        axes.clear()
        # Кожен кадр відтворюється незалежно; невідвідані вузли сірі.
        for node in order:
            node.color = "#D9D9D9"
        for index, node in enumerate(order[:step]):
            node.color = colors[index]
        by_id = {node.id: node for node in order}
        nx.draw(graph, pos=positions, labels=labels, arrows=False,
                node_size=2000,
                node_color=[by_id[node_id].color for node_id in graph.nodes],
                ax=axes)
        visited = ' -> '.join(str(node.val) for node in order[:step])
        axes.set_title(f"{mode}: крок {step}/{len(order)}\n{visited}")

    animation = FuncAnimation(figure, draw_frame, frames=len(order) + 1,
                              interval=interval, repeat=False)
    # Зберігаємо посилання, доки відкрите вікно.
    figure._traversal_animation = animation
    plt.show()
    return animation

def main():
    root = heap_to_tree([0, 4, 1, 5, 10, 3])
    print("DFS:", [node.val for node in dfs(root)])
    print("BFS:", [node.val for node in bfs(root)])
    visualize_traversal(root, "DFS")
    # Після закриття вікна DFS відкривається вікно BFS.
    visualize_traversal(root, "BFS")

if __name__ == "__main__":
    main()
