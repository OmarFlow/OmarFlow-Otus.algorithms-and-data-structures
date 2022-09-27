from random import randint
from typing import Optional

from otus.trees.avl import AVL


class SplayTree(AVL):
    """
    Расширяющееся дерево.

    Нода перемещается в корень при добавлении и поиске
    """

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
                self.right = SplayTree(key, self)
                self.right.rebalance_st()
                return
            else:
                self.right._insert(key)

        if key < self.key:
            if self.left is None:
                self.left = SplayTree(key, self)
                self.left.rebalance_st()
                return
            else:
                self.left._insert(key)

    def search(self, key: int) -> Optional['SplayTree']:
        """
        Основной метод поиска ноды
        """
        if self.is_root:
            return self._search(key)
        else:
            root = self.move_to_root()
            return root._search(key)

    def _search(self, key: int) -> Optional['SplayTree']:
        """
        Поиск ноды
        """
        if key == self.key:
            self.rebalance_st()
            return self

        if key > self.key:
            if not self.right:
                return None
            return self.right._search(key)

        if key < self.key:
            if not self.left:
                return None
            return self.left._search(key)

    def rebalance_st(self) -> None:
        """
        Ребалансировка
        """
        if self.is_root:
            return
        if self.parent_side == "right":
            self.small_left_rotation()
        else:
            self.small_right_rotation()
        self.rebalance_st()


class RandTree(AVL):
    """
    Рандомизированное дерево.

    Нода рандомно перемещается в корень при добавлении и поиске.
    """

    size: int = 1

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
                self.right = RandTree(key, self)
                if randint(1, 100) % RandTree.size == 0:
                    self.right.rebalance_srt()
                RandTree.size += 1
                return
            else:
                self.right._insert(key)

        if key < self.key:
            if self.left is None:
                self.left = RandTree(key, self)
                if randint(1, 100) % RandTree.size == 0:
                    self.left.rebalance_srt()
                RandTree.size += 1
                return
            else:
                self.left._insert(key)

    def search(self, key: int) -> Optional['RandTree']:
        """
        Основной метод поиска ноды
        """
        if self.is_root:
            return self._search(key)
        else:
            root = self.move_to_root()
            return root._search(key)

    def _search(self, key: int) -> Optional['RandTree']:
        """
        Поиск ноды
        """
        if key == self.key:
            if randint(1, 100) % RandTree.size == 0:
                self.rebalance_srt()
            return self

        if key > self.key:
            if not self.right:
                return None
            return self.right._search(key)

        if key < self.key:
            if not self.left:
                return None
            return self.left._search(key)

    def rebalance_srt(self) -> None:
        """
        Ребалансировка
        """
        if self.is_root:
            return
        if self.parent_side == "right":
            self.small_left_rotation()
        else:
            self.small_right_rotation()
        self.rebalance_srt()

    def remove(self, key: int) -> Optional['RandTree']:
        """
        Удаление ноды
        """
        res = super().remove(key)
        RandTree.size -= 1
        return res
