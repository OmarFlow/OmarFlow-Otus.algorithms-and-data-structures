# Красно-черное дерево с не полной реализацией удаления элементов

from dataclasses import dataclass


@dataclass
class Color:
    red: str = "red"
    black: str = "black"


@dataclass(frozen=True)
class Nil:
    color: str = Color.black


class RBBST:
    nil = Nil()

    def __init__(self, key, parent=None):
        self.key = key
        self.values = [key]
        self.left = RBBST.nil
        self.right = RBBST.nil
        self.parent = parent
        self.color = Color.red if parent else Color.black

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
            if self.right is RBBST.nil:
                self.right = RBBST(key, self)
                self.right.find_bad_balance()
                return
            else:
                self.right._insert(key)

        if key < self.key:
            if self.left is RBBST.nil:
                self.left = RBBST(key, self)
                self.left.find_bad_balance()
                return
            else:
                self.left._insert(key)

    def find_bad_balance(self):
        if self.is_root:
            return
        if self.parent.color == Color.red and self.uncle.color == Color.red:
            self.rebalance_red_uncle()
            self.grandfather.find_bad_balance()
        elif (
            self.parent.color == Color.red and self.uncle.color == Color.black
        ):
            if self.prepare_rebalance_black_uncle():
                grandpa_side = self.rotation()
                self.color = Color.black
                setattr(getattr(self, grandpa_side), "color", Color.red)
                return
            self.parent.rotation()
            self.parent.color = Color.black
            self.brother.color = Color.red

    def prepare_rebalance_black_uncle(self):
        if self.parent_side == self.parent.parent_side:
            return False
        self.rotation()
        return True

    def rotation(self):
        if self.parent_side == "left":
            self.right_rotation()
            return "right"
        else:
            self.left_rotation()
            return "left"

    def right_rotation(self):
        if self.grandfather:
            parent_side = self.parent.parent_side

        if self.right is not RBBST.nil:
            self.parent.left = self.right
            self.right.parent = self.parent
        else:
            self.parent.left = RBBST.nil

        self.right = self.parent

        if self.grandfather:
            parent = self.parent
            self.parent = self.parent.parent
            parent.parent = self
            setattr(self.parent, parent_side, self)
        else:
            self.parent.parent = self
            self.parent = None

    def left_rotation(self):
        if self.grandfather:
            parent_side = self.parent.parent_side

        if self.left is not RBBST.nil:
            self.parent.right = self.left
            self.left.parent = self.parent
        else:
            self.parent.right = RBBST.nil

        self.left = self.parent

        if self.grandfather:
            parent = self.parent
            self.parent = self.parent.parent
            parent.parent = self
            setattr(self.parent, parent_side, self)
        else:
            self.parent.parent = self
            self.parent = None

    def rebalance_red_uncle(self):
        self.parent.color = Color.black
        self.uncle.color = Color.black
        granpda = self.grandfather
        if granpda.is_root:
            granpda.color = Color.black
        else:
            granpda.color = Color.red

    def search(self, key):
        if self.is_root:
            return self._search(key)
        else:
            root = self.move_to_root()
            return root._search(key)

    def _search(self, key):
        if key == self.key:
            return self

        if key > self.key:
            if self.right is RBBST.nil:
                return None
            return self.right._search(key)

        if key < self.key:
            if self.left is RBBST.nil:
                return None
            return self.left._search(key)

    def remove(self, item):
        root = self.move_to_root()
        item = root.search(item)

        if not item:
            return

        item.remove_controller()

    def remove_controller(self):
        if self.color == Color.red and self.is_leaf:
            self.remove_red_leaf()
            return
        elif self.color == Color.black and self.is_leaf:
            self.remove_black_leaf_controller()
            return
        elif self.color == Color.black and self.number_of_children == 1:
            self.remove_black_one_child()
            return

        if self.number_of_children == 2:
            self.swap_items_to_futher_delete()
            self.remove_controller()

    def remove_black_leaf_controller(self):
        if (
            self.parent.color == Color.red
            and self.brother.color == Color.black
            and self.brother.left.color == Color.black
            and self.brother.right.color == Color.black
        ):
            self.parent.color = Color.black
            self.brother.color = Color.red
            self.remove_item()

        elif (
            self.parent.color == Color.red
            and self.brother.color == Color.black
            and self.brother.left.color == Color.red
        ):
            self.brother.right_rotation()
            self.grandfather.color = Color.red
            self.uncle.color = Color.black
            self.remove_item()

        elif (
            self.parent.color == Color.black
            and self.brother.color == Color.red
            and self.brother.right.left.color == Color.black
            and self.brother.right.right.color == Color.black
        ):
            self.brother.right_rotation()
            self.grandfather.color = Color.black
            self.brother.color = Color.red
            self.remove_item()

        elif (
            self.parent.color == Color.black
            and self.brother.color == Color.red
            and self.brother.right.left.color == Color.red
        ):
            self.brother.right.left_rotation()
            self.brother.right_rotation()
            self.uncle.right.color = Color.black
            self.remove_item()

        elif (
            self.parent.color == Color.black
            and self.brother.color == Color.black
            and self.brother.right.color == Color.red
        ):
            self.brother.right.left_rotation()
            self.brother.right_rotation()
            self.grandfather.color = Color.black
            self.remove_item()

        elif (
            self.parent.color == Color.black
            and self.brother.color == Color.black
            and self.brother.left.color == Color.black
            and self.brother.right.color == Color.black
        ):
            self.brother.color = Color.red
            self.remove_item()
            # to do

    def remove_red_leaf(self):
        setattr(self.parent, self.parent_side, RBBST.nil)
        self.remove_item()

    def remove_black_one_child(self):
        child = self.left if self.left is not RBBST.nil else self.right
        setattr(self.parent, self.parent_side, child)
        child.parent = self.parent
        child.color = Color.black
        self.remove_item()

    def swap_items_to_futher_delete(self):
        left_leaf = self.get_swap_item()
        self.swap_items(left_leaf)

    def swap_items(self, swap_item):
        swap_item_right = swap_item.right
        swap_item_left = swap_item.left
        swap_item_parent = swap_item.parent
        swap_item_color = swap_item.color

        if self.left is RBBST.nil:
            swap_item.left = RBBST.nil
        else:
            swap_item.left = self.left
            self.left.parent = swap_item

        if self.right is RBBST.nil:
            swap_item.left = RBBST.nil
        elif self.right == swap_item:
            swap_item.right = self
        else:
            swap_item.right = self.right
            self.right.parent = swap_item

        if self.parent:
            swap_item.parent = self.parent
            setattr(self.parent, self.parent_side, swap_item)
        else:
            swap_item.parent = None

        swap_item.color = self.color
        self.color = swap_item_color

        if swap_item_left is RBBST.nil:
            self.left = RBBST.nil
        else:
            self.left = swap_item_left
            swap_item_left.parent = self

        if swap_item_right is RBBST.nil:
            self.right = RBBST.nil
        else:
            self.right = swap_item_right
            swap_item_right.parent = self

        if swap_item_parent == self:
            self.parent = swap_item
        else:
            self.parent = swap_item_parent
            setattr(swap_item_parent, swap_item_parent.parent_side, self)

    def get_swap_item(self):
        if self.right.left is RBBST.nil:
            return self.right
        else:
            return self.right.move_left()

    def move_left(self):
        left = self.left
        while left.left is not RBBST.nil:
            left = getattr(left, "left")
        return left

    @property
    def is_leaf(self):
        return self.left is RBBST.nil and self.right is RBBST.nil

    @property
    def is_root(self):
        if self.parent is None:
            return True
        return False

    def move_to_root(self):
        item = self
        while not item.is_root:
            item = item.parent
        return item

    @property
    def uncle(self):
        return self.parent.brother

    @property
    def brother(self):
        if self.key > self.parent.key:
            another_side = self.parent.left
        else:
            another_side = self.parent.right
        return another_side

    @property
    def grandfather(self):
        return self.parent.parent

    @property
    def parent_side(self):
        if self.key > self.parent.key:
            return "right"
        else:
            return "left"

    @property
    def number_of_children(self):
        return sum(1 for i in [self.left, self.right] if i is not RBBST.nil)

    def remove_item(self):
        setattr(self.parent, self.parent_side, RBBST.nil)
        self.parent = None
        self.right = None
        self.left = None

    def __str__(self):
        return str(self.values)
