from typing import Optional

from otus.trees.bst import BST


class AVL(BST):
    """
    Бинарное, сбалансированное дерево поиска
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def insert(self, key: int) -> None:
        """
        Основной метод вставки ноды
        """
        if self.is_root:
            self._insert(key)
        else:
            root = self.move_to_root()
            root._insert(key)

    def _insert(self, key: int) -> None:
        """
        Вставка ноды
        """
        if key == self.key:
            self.values.append(key)
            return

        if key > self.key:
            if self.right is None:
                self.right = AVL(key, self)
                self.find_bad_balance()
                return
            else:
                self.right._insert(key)

        if key < self.key:
            if self.left is None:
                self.left = AVL(key, self)
                self.find_bad_balance()
                return
            else:
                self.left._insert(key)

    def search(self, key: int) -> Optional['BST']:
        """
        Основной метод поиска ноды
        """
        if self.is_root:
            return self._search(key)
        else:
            root = self.move_to_root()
            return root._search(key)

    def _search(self, key: int) -> Optional['BST']:
        """
        Поиск ноды
        """
        if key == self.key:
            return self

        if key > self.key:
            if not self.right:
                return None
            return self.right._search(key)

        if key < self.key:
            if not self.left:
                return None
            return self.left._search(key)

    def find_bad_balance(self) -> None:
        """
        Поиск ноды, которой нужна ребалансировка
        """
        self.calculate_height()

        if self.parent is None:
            return

        if self.need_rebalance:
            self.rebalance()

        if self.parent is None:
            return

        self.parent.find_bad_balance()

    def rebalance(self) -> None:
        """
        Ребалансировка
        """
        another_side_height: int = self.get_another_side_height()
        left_children_height: int = 0 if not self.left else self.left.height
        right_children_height: int = 0 if not self.right else self.right.height

        # если нода справа относительно родителя
        if self.height > another_side_height and self.parent_side == "left":
            # если высота левого ребенка больше или равна правой - малый поворот направо
            if left_children_height >= right_children_height:
                self.small_right_rotation()
            # если высота левого ребенка меньше правой - большой поворот направо
            elif left_children_height < right_children_height:
                self.big_right_rotation()

        # если нода слева относительно родителя
        elif self.height > another_side_height and self.parent_side == "right":
            # если высота правого ребенка больше или равна левой - малый поворот налево
            if right_children_height >= left_children_height:
                self.small_left_rotation()
            # если высота правого ребенка меньше левой - большой поворот налево
            elif right_children_height < left_children_height:
                self.big_left_rotation()

    def big_right_rotation(self) -> None:
        """
        Большой поворот направо
        """
        self.right.small_left_rotation()
        self.parent.small_right_rotation()

    def big_left_rotation(self) -> None:
        """
        Большой поворот налево
        """
        self.left.small_right_rotation()
        self.parent.small_left_rotation()

    def small_right_rotation(self) -> None:
        """
        Маленький поворот направо
        """
        if self.parent.parent:
            parent_side = self.parent.parent_side

        if self.right:
            self.parent.left = self.right
            self.right.parent = self.parent
        else:
            self.parent.left = None

        self.right = self.parent

        if self.parent.parent:
            parent = self.parent
            self.parent = self.parent.parent
            parent.parent = self
            setattr(self.parent, parent_side, self)
        else:
            self.parent.parent = self
            self.parent = None
        self.calculate_height()
        self.right.calculate_height()

    def small_left_rotation(self) -> None:
        """
        Маленький поворот налево
        """
        if self.parent.parent:
            parent_side = self.parent.parent_side

        if self.left:
            self.parent.right = self.left
            self.left.parent = self.parent
        else:
            self.parent.right = None

        self.left = self.parent

        if self.parent.parent:
            parent = self.parent
            self.parent = self.parent.parent
            parent.parent = self
            setattr(self.parent, parent_side, self)
        else:
            self.parent.parent = self
            self.parent = None
        self.left.calculate_height()
        self.calculate_height()

    @property
    def need_rebalance(self) -> bool:
        """
        Необходима ли ребалансировка
        """
        another_side_height = self.get_another_side_height()
        return all(
            False for i in [1, -1, 0] if i == self.height - another_side_height
        )

    def get_another_side(self) -> Optional['AVL']:
        """
        Получение брата
        """
        if self.key > self.parent.key:
            another_side = self.parent.left
        else:
            another_side = self.parent.right
        return another_side

    def get_another_side_height(self) -> int:
        """
        Высота брата
        """
        another_side = self.get_another_side()
        if another_side:
            another_side_height = another_side.height
        else:
            another_side_height = 0
        return another_side_height
