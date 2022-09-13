from otus.trees.avl import AVL


class SplayTree(AVL):
    """
    Расширяющееся дерево
    """
    def insert(self, key):
        if self.is_root:
            self._insert(key)
        else:
            root = self.move_to_root()
            root._insert(key)

    def _insert(self, key):
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

    def search(self, key):
        if self.is_root:
            return self._search(key)
        else:
            root = self.move_to_root()
            return root._search(key)

    def _search(self, key):
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

    def rebalance_st(self):
        if self.is_root:
            return
        if self.parent_side == "right":
            self.small_left_rotation()
        else:
            self.small_right_rotation()
        self.rebalance_st()


class RandTree(AVL):
    """
    Рандомизированное дерево
    """
    size = 1
    def insert(self, key):
        if self.is_root:
            self._insert(key)
        else:
            root = self.move_to_root()
            root._insert(key)

    def _insert(self, key):
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

    def search(self, key):
        if self.is_root:
            return self._search(key)
        else:
            root = self.move_to_root()
            return root._search(key)

    def _search(self, key):
        if key == self.key:
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

    def rebalance_srt(self):
        if self.is_root:
            return
        if self.parent_side == "right":
            self.small_left_rotation()
        else:
            self.small_right_rotation()
        self.rebalance_srt()

    def remove(self, key):
        res = super().remove(key)
        RandTree.size -= 1
        return res
