class RBNode:
    def __init__(self, key, color="R"):
        self.key = key
        self.color = color  # "R" или "B"
        self.left = None
        self.right = None
        self.parent = None  # обязательно для удобства поворотов

class RBTree:
    def __init__(self):
        self.root = None

    def left_rotate(self, x):
        """Левый поворот вокруг узла x.
        y = x.right становится новым корнем поддерева.
        x становится левым ребёнком y.
        """
        y = x.right
        # Переносим левое поддерево y в правое поддерево x
        x.right = y.left
        if y.left is not None:
            y.left.parent = x
        # Поднимаем y на место x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        # x становится левым ребёнком y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        """Правый поворот вокруг узла x.
        y = x.left становится новым корнем поддерева.
        x становится правым ребёнком y.
        """
        y = x.left
        # Переносим правое поддерево y в левое поддерево x
        x.left = y.right
        if y.right is not None:
            y.right.parent = x
        # Поднимаем y на место x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        # x становится правым ребёнком y
        y.right = x
        x.parent = y

    def insert(self, key):
        """Вставка нового ключа в КЧ-дерево."""
        # 1. Обычная вставка в BST
        new_node = RBNode(key)
        parent = None
        current = self.root
        while current is not None:
            parent = current
            if key < current.key:
                current = current.left
            else:
                current = current.right
        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        # 2. Балансировка
        self.fix_insert(new_node)
        # 3. Корень всегда чёрный
        self.root.color = "B"

    def fix_insert(self, node):
        """Балансировка после вставки. Восстанавливает свойства КЧ-дерева."""
        while node.parent is not None and node.parent.color == "R":
            parent = node.parent
            grandpa = parent.parent
            if parent == grandpa.left:
                # Родитель — левый ребёнок дедушки
                uncle = grandpa.right
                # Случай 1: дядя красный
                if uncle is not None and uncle.color == "R":
                    parent.color = "B"
                    uncle.color = "B"
                    grandpa.color = "R"
                    node = grandpa  # Продолжаем с дедушки
                else:
                    # Дядя чёрный (или None)
                    # Случай 2: node — правый ребёнок parent
                    if node == parent.right:
                        self.left_rotate(parent)
                        node = parent
                        parent = node.parent
                    # Случай 3: node — левый ребёнок parent
                    parent.color = "B"
                    grandpa.color = "R"
                    self.right_rotate(grandpa)
                    break  # Свойства восстановлены
            else:
                # Родитель — правый ребёнок дедушки (зеркальный случай)
                uncle = grandpa.left
                # Случай 1: дядя красный
                if uncle is not None and uncle.color == "R":
                    parent.color = "B"
                    uncle.color = "B"
                    grandpa.color = "R"
                    node = grandpa
                else:
                    # Дядя чёрный (или None)
                    # Случай 2: node — левый ребёнок parent
                    if node == parent.left:
                        self.right_rotate(parent)
                        node = parent
                        parent = node.parent
                    # Случай 3: node — правый ребёнок parent
                    parent.color = "B"
                    grandpa.color = "R"
                    self.left_rotate(grandpa)
                    break

    def _inorder_with_colors(self, node, result=None):
        """Симметричный обход с цветами."""
        if result is None:
            result = []
        if node is not None:
            self._inorder_with_colors(node.left, result)
            result.append((node.key, node.color))
            self._inorder_with_colors(node.right, result)
        return result

    def inorder_print(self):
        """Печать обхода с цветами."""
        result = self._inorder_with_colors(self.root)
        print("Inorder:", result)
        return result

    def _count_black_height(self, node):
        """Подсчёт чёрной высоты (количество чёрных узлов на пути до листа)."""
        if node is None:
            return 1  # NIL-узел считается чёрным
        left_bh = self._count_black_height(node.left)
        right_bh = self._count_black_height(node.right)
        if left_bh != right_bh:
            return -1  # Нарушение: разные чёрные высоты
        return left_bh + (1 if node.color == "B" else 0)

    def is_valid(self):
        """Проверка корректности КЧ-дерева."""
        if self.root is None:
            return True
        # 1. Корень чёрный
        if self.root.color != "B":
            print("Ошибка: корень не чёрный!")
            return False
        # 2. Все пути от корня до листьев имеют одинаковую чёрную высоту
        bh = self._count_black_height(self.root)
        if bh == -1:
            print("Ошибка: разные чёрные высоты!")
            return False
        # 3. Нет двух красных узлов подряд
        def check_no_red_red(node):
            if node is None:
                return True
            if node.color == "R":
                if (node.left is not None and node.left.color == "R") or \
                   (node.right is not None and node.right.color == "R"):
                    print(f"Ошибка: два красных узла подряд у {node.key}!")
                    return False
            return check_no_red_red(node.left) and check_no_red_red(node.right)
        # 4. NIL-узлы чёрные (по определению None считается чёрным)
        # 5. BST-свойство
        def check_bst(node, min_val=float('-inf'), max_val=float('inf')):
            if node is None:
                return True
            if not (min_val < node.key < max_val):
                print(f"Ошибка BST: {node.key} не в диапазоне ({min_val}, {max_val})")
                return False
            return check_bst(node.left, min_val, node.key) and \
                   check_bst(node.right, node.key, max_val)
        return check_no_red_red(self.root) and check_bst(self.root)

    def print_tree(self, node=None, prefix="", is_last=True):
        """Красивый вывод дерева в консоль."""
        if node is None:
            node = self.root
        if node is None:
            return
        print(prefix + ("└── " if is_last else "├── ") + f"{node.key}({node.color})")
        children = []
        if node.left:
            children.append((node.left, "L"))
        if node.right:
            children.append((node.right, "R"))
        for i, (child, _) in enumerate(children):
            is_last_child = (i == len(children) - 1)
            self.print_tree(child, prefix + ("    " if is_last else "│   "), is_last_child)


# === ТЕСТИРОВАНИЕ ===
print("=" * 60)
print("ТЕСТИРОВАНИЕ КРАСНО-ЧЁРНОГО ДЕРЕВА")
print("=" * 60)

tree = RBTree()

# Тестовая последовательность 
test_sequence = [7, 3, 18, 10, 22, 8, 11, 26]

for key in test_sequence:
    print(f"\n--- Вставка {key} ---")
    tree.insert(key)
    print("Структура дерева:")
    tree.print_tree()
    print("Inorder обход:", tree.inorder_print())
    valid = tree.is_valid()
    print(f"Дерево валидно: {valid}")
    if not valid:
        print("!!! ОШИБКА: дерево невалидно !!!")
        break

print("\n" + "=" * 60)
print("ИТОГОВОЕ ДЕРЕВО:")
print("=" * 60)
tree.print_tree()
print("\nИтоговый inorder:", tree._inorder_with_colors(tree.root))
print(f"Итоговая валидность: {tree.is_valid()}")
