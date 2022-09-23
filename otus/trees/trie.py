from typing import List, Any, Optional


class Trie:
    """
    Префиксное дерево
    """

    def __init__(self):
        self.root = self.Node(None)

    def insert(self, word: str, value: Any) -> None:
        """
        Добавление ключа в дерево
        """
        node: Trie.Node = self.root
        last_idx: int = len(word) - 1

        for idx in range(len(word)):
            letter: str = word[idx]
            if idx == last_idx:
                node.add(letter, value)
                break
            node = node.add(letter, None)

    def search(self, word: str) -> Any:
        """
        Поиск ключа в дереве
        """
        node: Trie.Node = self.root
        for letter in word:
            if not node.exist(letter):
                return False
            node = node.get_node(letter)  # type: ignore
        return node.value

    def remove(self, word: str):
        """
        Удаление ключа в дереве
        """
        node: Trie.Node = self.root
        last_idx: int = len(word) - 1

        for idx in range(len(word)):
            letter: str = word[idx]
            node = node.get_node(letter)  # type: ignore
            if idx == last_idx:
                node.value = None

    def starts_with(self, prefix: str) -> bool:
        """
        Поиск префикса в дереве
        """
        node: Trie.Node = self.root
        for letter in prefix:
            if not node.exist(letter):
                return False
            node = node.get_node(letter)  # type: ignore
        return True

    class Node:
        """
        Узел дерева
        """

        def __init__(self, value):
            self.keys: List[Optional[Trie.Node]] = [None for _ in range(123)]
            self.value: Any = value

        def add(self, key: str, value: Any) -> 'Trie.Node':
            """
            Добавление ключа в ноду
            """
            node: Optional['Trie.Node'] = self.get_node(key)
            # перезаписываем значение, если такой ключ уже есть
            if value and node:
                node.value = value
            # создаём ноду, если такой еще нет
            if node is None:
                node = Trie.Node(value)
                self.keys[ord(key)] = node
                return node
            return node

        def exist(self, key: str) -> bool:
            """
            Проверка существования ключа в узле
            """
            if self.keys[ord(key)] is None:
                return False
            return True

        def get_node(self, key: str) -> Optional['Trie.Node']:
            """
            Получение узла
            """
            idx: int = ord(key)
            return self.keys[idx]
