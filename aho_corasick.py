from collections import deque


class TrieNode:
    def __init__(self, letter):
        self.letter = letter
        self.children = {}
        self.end_of_word = False
        self.fail_node = None
        self.output = []


class AhoCorasick:
    def __init__(self):
        self.root = TrieNode("*")
        self.queue = deque([])

    def add_word(self, word):
        curr_node = self.root

        for letter in word:
            if letter not in curr_node.children:
                curr_node.children[letter] = TrieNode(letter)
            curr_node = curr_node.children[letter]
            curr_node.letter = letter
        curr_node.end_of_word = True
        curr_node.output.append(word)

    def build_fail_links(self):
        for char, child in self.root.children.items():
            self.queue.append(child)
            child.fail_node = self.root

        while len(self.queue) > 0:
            curr_node = self.queue.popleft()
            for char, child in curr_node.children.items():
                self.queue.append(child)
                letter = child.letter

                while curr_node.fail_node:
                    for ch, fail_node_child in curr_node.fail_node.children.items():
                        if fail_node_child.letter == letter:
                            child.fail_node = fail_node_child
                            if fail_node_child.end_of_word:
                                child.end_of_word = True
                                for out in fail_node_child.output:
                                    child.output.append(out)

                    if child.fail_node is not None:
                        break
                    curr_node = curr_node.fail_node

                if child.fail_node is None:
                    child.fail_node = self.root

    def find_words_in(self, word):
        if word == "":
            return True

        output = {}
        curr_node = self.root

        for i in range(0, len(word)):
            letter = word[i]
            found = True
            while letter not in curr_node.children:
                if curr_node.fail_node is not None:
                    curr_node = curr_node.fail_node
                else:
                    found = False
                    break

            if not found:
                continue

            curr_node = curr_node.children[letter]
            if curr_node.end_of_word:
                for out in curr_node.output:
                    if out not in output.keys():
                        output[out] = []
                    output[out].append(i-len(out)+1)

        return len(output) > 0, output


if __name__ == "__main__":
    trie = AhoCorasick()

    words = ["a", "ab", "bc", "aab", "aac", "bd"]
    # words = ["he", "she", "hers", "his"]

    for word in words:
        trie.add_word(word)
    trie.build_fail_links()

    print(trie.find_words_in("bcaab"))
    # print(trie.find_words_in("ahishers"))
