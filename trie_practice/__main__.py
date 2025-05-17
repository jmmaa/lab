from __future__ import annotations
from dataclasses import dataclass
import random
import string


@dataclass
class TrieNode:
    children: dict[str, TrieNode]
    is_terminal: bool

    def __repr__(self) -> str:
        return f"[{self.children}:{self.is_terminal}]"


@dataclass
class Trie:
    def __post_init__(self):
        self.root = TrieNode({}, False)

    def insert(self, word: str):
        current_node = self.root

        for c in word:
            if c not in current_node.children:
                current_node.children[c] = TrieNode({}, False)

                current_node = current_node.children[c]

            else:
                current_node = current_node.children[c]

        current_node.is_terminal = True

        # print(f'done inserting "{word}"')

    def has(self, word: str):
        current_node = self.root

        for c in word:
            if c in current_node.children:
                current_node = current_node.children[c]

            else:
                return False

        return current_node.is_terminal

    def get_all_words(self, node: TrieNode, word: str, results: list[str]):
        # Method to recursively traverse the trie
        # and return a whole word.
        if node.is_terminal:
            results.append(word)

        for a, n in node.children.items():
            self.get_all_words(n, word + a, results)

    def autocomplete(self, word: str):
        results = []
        current_node = self.root
        prefix = ""

        # find the starting node
        for c in word:
            if c in current_node.children:
                prefix += c
                current_node = current_node.children[c]

        self.get_all_words(current_node, word, results)

        return results


if __name__ == "__main__":
    trie = Trie()

    strings = [s for s in string.ascii_lowercase]

    for _ in range(10000):
        random.shuffle(strings)
        trie.insert("".join(strings))

    while True:
        match input("insert, autocomplete").split(","):
            case ["insert", value]:
                trie.insert(value)
            case ["autocomplete", value]:
                print(trie.autocomplete(value))

            case _:
                print("wrong input")

    # print(trie.autocomplete("pokemon/golde"))


# TODO: UPLOAD ALL OF THIS SHIEEET IN GITHUB
