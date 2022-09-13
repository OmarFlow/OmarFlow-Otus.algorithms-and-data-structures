class BtreeNodeItem:
    """
    Элемент узла В дерева
    """

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    @property
    def has_childrens(self):
        if self.left or self.right:
            return True
        return False


class BtreeNode(list):
    """
    Узел B дерева
    """

    def __init__(self):
        super().__init__()
        self.length = BTree.array_size


class BTree:
    """
    B дерево
    """

    array_size = 2
    half_array_size = array_size // 2

    def __init__(self, elements, parent=None, parent_item=None):
        self.array = BtreeNode()
        self.parent = parent
        self.parent_item = parent_item
        self.array.extend(
            elements if type(elements) is list else [BtreeNodeItem(elements)]
        )

    def get_intermediate_array(self, index, node_item):
        intermediate_array = [item for item in self.array]
        intermediate_array.insert(index, node_item)
        return intermediate_array

    def get_intermediate_array_middle(self, intermediate_array):
        middle = len(intermediate_array) // 2
        return middle

    def put_in_full_array(self, item, index):
        """
        Вставка элемента в заполненную ноду
        """
        intermediate_array = self.get_intermediate_array(index, item)
        middle = self.get_intermediate_array_middle(intermediate_array)
        middle_value = self.array[middle].value
        parent_is_full = None if self.is_root else self.parent.is_full

        if self.parent is None:
            new_node = BTree([self.array[middle]])
            if self.array[middle].left:
                self.array[middle - 1].right = self.array[middle].left
            new_node_item = new_node.array[0]

        else:
            index = self.parent.parent_binary_search(middle_value)
            new_node_item = BtreeNodeItem(middle_value)
            self.parent.array[-1].right = None
            if not self.parent.is_full:
                self.parent.array.insert(index, new_node_item)
            new_node = self.parent

        new_node_left = BTree(
            intermediate_array[:middle], new_node, new_node_item)
        new_node_item.left = new_node_left
        self.array = intermediate_array[middle + 1:]
        self.parent = new_node
        self.parent_item = new_node_item
        new_node_item.right = self

        if parent_is_full:
            self.parent.put_in_full_array(new_node_item, index)

    def put(self, item):
        root = self.move_to_root()
        root._put(item)

    def _put(self, item):
        index, side = self.binary_search(item)
        node_item = BtreeNodeItem(item)

        if self.check_link(index, side):
            # если есть ссылка на дочерний элемент, проваливаемся в него
            getattr(self.array[index], side)._put(item)
        else:
            if self.is_full:
                self.put_in_full_array(node_item, index)
            else:
                # если ссылок нет и нода не заполнена
                self.array.insert(index, node_item)
                return

    def remove(self, item):
        """
        Основной метод удаления элемента из дерева
        """
        root = self.move_to_root()
        res = root._search(item)

        if not res:
            raise Exception("This item does not exist")

        node, item = res
        node.remove_controller(item)

    def remove_controller(self, item):
        """
        Контроллер удаления элемента из дерева
        """
        if self.is_leaf:
            if self.allow_delete_item:
                self.array.remove(item)
            else:
                if self.brother.allow_delete_item:
                    self.swap_items_when_brother_allow_delete()
                    self.remove_controller(item)
                else:
                    self.swap_items_when_brother_not_allow_delete(item)
        else:
            self.remove_item_from_not_leaf_node(item)

    def remove_item_from_not_leaf_node(self, item):
        left = item.left
        right = item.right

        if left:
            if left.allow_delete_item:
                item.value = left.array[-1].value
                del item.left.array[-1]
                return

        if right:
            if right.allow_delete_item:
                item.value = right.array[0].value
                del item.right.array[0]
                return

        if right and left:
            if not right.allow_delete_item and not left.allow_delete_item:
                new_node = BTree(left.array + right.array)

                item_index = self.array.index(item)
                try:
                    right = self.array[item_index - 1]
                except IndexError:
                    left = self.array[item_index + 1]

                self.array.remove(item)

                if right:
                    right.right = new_node
                    new_node.parent_item = right
                else:
                    left.left = new_node
                    new_node.parent_item = left

    def swap_items_when_brother_not_allow_delete(self, item):
        parent_item_index = self.parent.array.index(self.parent_item)
        parent_side = self.parent_side
        try:
            right = self.parent.array[parent_item_index - 1]
        except IndexError:
            left = self.parent.array[parent_item_index + 1]

        self.array.remove(item)

        brother = self.brother.array
        parent_item = self.parent_item
        self.parent.array.remove(parent_item)
        parent_item.left = None
        parent_item.right = None

        if parent_side == "left":
            self.array.append(parent_item)
            self.array.extend(brother)
        else:
            self.array.extend(brother)
            self.array.append(parent_item)

        if right:
            right.right = self
            self.parent_item = right
        else:
            left.left = self
            self.parent_item = left

    def swap_items_when_brother_allow_delete(self):
        if self.parent_side == "left":
            index = 0
        else:
            index = -1
        self.array.append(BtreeNodeItem(self.parent_item.value))
        self.parent_item.value = self.brother.array[index].value
        del self.brother.array[index]

    def search(self, num):
        """
        Основной метод поиска элемента
        """
        root = self.move_to_root()
        res = root._search(num)
        if not res:
            return
        _, item = res
        return item.value

    def _search(self, num):
        """
        Поиск элемента
        """
        if num > self.array[-1].value and not self.array[-1].right:
            return

        if num < self.array[0].value and not self.array[0].left:
            return

        for i in self.array:
            right = i.right
            left = i.left
            if num == i.value:
                return self, i
            elif num > i.value:
                if right:
                    return i.right._search(num)
                continue
            elif num < i.value:
                if left:
                    return i.left._search(num)
                continue

    def parent_binary_search(self, num):
        """
        Поиск для вставки элемента в родительской ноде
        """
        low = 0
        high = len(self.array) - 1

        if len(self.array) == 1:
            if num > self.array[0].value:
                return 1
            else:
                return 0

        if len(self.array) == 2:
            if num > self.array[1].value:
                return 2
            elif num < self.array[0].value:
                return 0
            else:
                return 1

        while low <= high:
            mid = (low + high) // 2
            if self.array[mid - 1].value <= num <= self.array[mid + 1].value:
                if num > self.array[mid].value:
                    return mid + 1
                return mid

            if num > self.array[mid].value:
                low = mid + 1

            if num < self.array[mid].value:
                high = mid - 1

    def binary_search(self, num):
        """
        Поиск для вставки или дальнейшего поиска позиции для элемента
        """
        low = 0
        high = len(self.array) - 1

        if len(self.array) == 1:
            if num > self.array[0].value:
                if self.check_link(0, "right"):
                    return 0, "right"
                else:
                    return 1, "stub"
            else:
                return 0, "left"

        if len(self.array) == 2:
            if num > self.array[1].value:
                if self.check_link(1, "right"):
                    return (1, "right")
                else:
                    return (2, "stub")

            elif num < self.array[0].value:
                return (0, "left")
            else:
                return (1, "left")

        while low <= high:
            mid = (low + high) // 2
            if self.array[mid - 1].value <= num <= self.array[mid + 1].value:
                if num > self.array[mid].value:
                    return (mid + 1, "left")
                return (mid, "right")

            if num > self.array[mid].value:
                low = mid + 1

            if num < self.array[mid].value:
                high = mid - 1

    def check_link(self, index, child_side):
        """
        Проверка наличия у элемента ссылки на дочерний элемент
        """
        if child_side == "stub":
            return False

        if getattr(self.array[index], child_side) is None:
            return False
        else:
            return True

    def move_to_root(self):
        if self.is_root:
            return self
        root = self.parent
        while root.parent:
            root = root.parent
        return root

    @property
    def is_root(self):
        if self.parent:
            return False
        return True

    @property
    def is_full(self):
        return len(self.array) == BTree.array_size

    @property
    def is_leaf(self):
        return all(not item.has_childrens for item in self.array)

    @property
    def values(self):
        return [i.value for i in self.array]

    @property
    def allow_delete_item(self):
        """
        Проверка на возможность удаления элемента
        """
        return len(self.array) > BTree.half_array_size

    @property
    def brother(self):
        """
        Получение соседнего элемента
        """
        return (
            self.parent_item.left
            if self.parent_item.left != self
            else self.parent_item.right
        )

    @property
    def parent_side(self):
        """
        Определение своей стороны у родителя
        """
        if self.array[0].value > self.parent_item.value:
            return "right"
        else:
            return "left"

    def __str__(self):
        return str(self.values)
