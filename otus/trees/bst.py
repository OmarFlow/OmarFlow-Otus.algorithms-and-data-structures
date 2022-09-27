from typing import Optional, List


class BST:
    """
    Бинарное дерево поиска
    """

    def __init__(self, key: int, parent=None):
        self.left: Optional[BST] = None
        self.right: Optional[BST] = None
        self.key: int = key
        self.values: List[int] = [key]
        self.parent: Optional[BST] = parent
        self.height: int = 1

    def insert(self, key: int) -> None:
        """
        Вставка ноды
        """
        if key == self.key:
            self.values.append(key)
            return

        if key > self.key:
            if not self.right:
                self.right = BST(key, self)
                return
            else:
                self.right.insert(key)

        if key < self.key:
            if not self.left:
                self.left = BST(key, self)
                return
            else:
                self.left.insert(key)

    def search(self, key: int) -> Optional['BST']:
        """
        Поиск ноды
        """
        if key == self.key:
            return self

        if key > self.key:
            if not self.right:
                return None
            return self.right.search(key)

        if key < self.key:
            if not self.left:
                return None
            return self.left.search(key)

    def remove(self, key: int) -> Optional['BST']:
        """
        Основной метод удаления ноды
        """
        root: BST = self.move_to_root()
        item: Optional[BST] = root.search(key)

        if not item:
            return

        if item.number_of_children == 0:
            return item.remove_leaf()
        elif item.number_of_children == 1:
            return item.remove_one_child()
        elif item.number_of_children == 2:
            return item.remove_two_child()

    def remove_leaf(self) -> 'BST':
        """
        Удаление листа
        """
        if self.is_root:
            self.remove_item()
            return self
        setattr(self.parent, self.parent_side, None)
        self.parent.calculate_height()
        self.remove_item()
        return self

    def remove_one_child(self) -> 'BST':
        """
        Удаление ноды с 1им ребенком
        """
        if self.is_root:
            node: BST = self.left if self.left else self.right
            setattr(self, node.parent_side, None)
            node.parent = None
            return node

        child: BST = self.left if self.left else self.right
        child.parent = self.parent
        setattr(self.parent, self.parent_side, child)
        self.parent.calculate_height()
        self.remove_item()

    def remove_two_child(self) -> 'BST':
        """
        Удаление ноды с 2мя детьми
        """
        if self.right.left is None:
            if self.is_root:
                self.right.parent = None
            else:
                self.right.parent = self.parent
                setattr(self.parent, self.parent_side, self.right)
            self.right.left = self.left
            self.left.parent = self.right
            self.right.calculate_height()
            right: BST = self.right
            self.remove_item()
            return right
        else:
            max_left_node: BST = self.right.move_left()
            if max_left_node.right:
                max_left_node.right.parent = max_left_node.parent
                setattr(
                    max_left_node.parent,
                    max_left_node.parent_side,
                    max_left_node.right,
                )
                self.swap_deleted_item(max_left_node)
                max_left_node.calculate_height()
                self.remove_item()
                return max_left_node
            else:
                self.swap_deleted_item(max_left_node)
                max_left_node.calculate_height()
                self.remove_item()
                return max_left_node

    @staticmethod
    def sort(node) -> None:
        """
        Вывод элементов в порядке возрастания
        """
        if node is None:
            return
        node.sort(node.left)
        print(node.values)
        node.sort(node.right)

    @property
    def parent_side(self) -> str:
        """
        Сторона ноды у родителя
        """
        if self.key > self.parent.key:
            return "right"
        else:
            return "left"

    @property
    def number_of_children(self) -> int:
        """
        Кол-во детей у ноды
        """
        return sum(1 for i in [self.left, self.right] if i is not None)

    def calculate_height(self) -> None:
        """
        Подсчёт высоты ноды
        """
        self.height = (
            max(
                self.left.height if self.left else 0,
                self.right.height if self.right else 0,
            )
            + 1
        )

    def move_left(self) -> 'BST':
        """
        Передвижение к самой левой ноде
        """
        left = self.left
        while left.left:
            left = getattr(left, "left")
        return left

    def swap_deleted_item(self, item: 'BST') -> None:
        """
        Перемещение ноды при удалении ноды с 2мя детьми
        """
        if not item.right:
            setattr(item.parent, item.parent_side, None)

        if self.is_root:
            item.parent = None
        else:
            item.parent = self.parent
            setattr(self.parent, self.parent_side, item)
        item.right = self.right
        item.left = self.left
        self.right.parent = item
        self.left.parent = item

    def remove_item(self) -> None:
        """
        Отвязка ноды
        """
        setattr(self.parent, self.parent_side, None)
        self.parent = None
        self.right = None
        self.left = None

    @property
    def is_root(self) -> bool:
        """
        Является ли нода корнем
        """
        if self.parent is None:
            return True
        return False

    def move_to_root(self) -> 'BST':
        """
        Передвижение к корню
        """
        item = self
        while not item.is_root:
            item = item.parent
        return item

    def __str__(self):
        return str(self.values)
