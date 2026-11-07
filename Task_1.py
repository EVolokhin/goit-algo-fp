class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node

    def insert_after(self, prev_node: Node, data):
        if prev_node is None:
            print("Попереднього вузла не існує.")
            return
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_node(self, key: int):
        cur = self.head
        if cur and cur.data == key:
            self.head = cur.next
            cur = None
            return
        prev = None
        while cur and cur.data != key:
            prev = cur
            cur = cur.next
        if cur is None:
            return
        prev.next = cur.next
        cur = None

    def search_element(self, data: int) -> Node | None:
        cur = self.head
        while cur:
            if cur.data == data:
                return cur
            cur = cur.next
        return None

    def reverse_list(self):
        """Реверсує список зміною посилань: O(n) часу, O(1) пам'яті."""
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    @staticmethod
    def _merge_sorted_nodes(left, right):
        """Стабільно зливає два відсортовані ланцюжки вузлів."""
        dummy = Node()
        tail = dummy
        while left is not None and right is not None:
            if left.data <= right.data:
                tail.next = left
                left = left.next
            else:
                tail.next = right
                right = right.next
            tail = tail.next
        tail.next = left if left is not None else right
        return dummy.next

    @classmethod
    def _merge_sort_nodes(cls, head):
        if head is None or head.next is None:
            return head

        slow, fast = head, head.next
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next

        right = slow.next
        slow.next = None
        left = cls._merge_sort_nodes(head)
        right = cls._merge_sort_nodes(right)
        return cls._merge_sorted_nodes(left, right)

    def sort_list(self):
        """Сортує за зростанням: O(n log n) часу, O(log n) стеку."""
        self.head = self._merge_sort_nodes(self.head)

    def print_list(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next

def merge_sorted_lists(first: LinkedList, second: LinkedList) -> LinkedList:
    """Зливає два списки, відсортовані за зростанням, за O(n + m).

    Переносить наявні вузли у результат і очищає вхідні списки.
    Вхідні списки мають бути різними та не містити спільних вузлів.
    Додаткова пам'ять — O(1).
    """
    if first is second:
        raise ValueError("Для злиття потрібні два різні списки.")
    result = LinkedList()
    result.head = LinkedList._merge_sorted_nodes(first.head, second.head)
    first.head = None
    second.head = None
    return result

if __name__ == "__main__":

	llist = LinkedList()

# Вставляємо вузли в початок
	llist.insert_at_beginning(5)
	llist.insert_at_beginning(10)
	llist.insert_at_beginning(15)

# Вставляємо вузли в кінець
	llist.insert_at_end(20)
	llist.insert_at_end(25)

# Друк зв'язного списку
	print("Зв'язний список:")
	llist.print_list()

# Видаляємо вузол
	llist.delete_node(10)

	print("\nЗв'язний список після видалення вузла з даними 10:")
	llist.print_list()

# Пошук елемента у зв'язному списку
	print("\nШукаємо елемент 15:")
	element = llist.search_element(15)
	if element:
		print(element.data)

	print("\nСписок після реверсування:")
	llist.reverse_list()
	llist.print_list()

	print("\nСписок після сортування злиттям:")
	llist.sort_list()
	llist.print_list()

	second_list = LinkedList()
	for value in (3, 15, 22, 30):
		second_list.insert_at_end(value)

	print("\nРезультат злиття двох відсортованих списків:")
	merged_list = merge_sorted_lists(llist, second_list)
	merged_list.print_list()
