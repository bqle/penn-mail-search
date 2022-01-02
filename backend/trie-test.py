import unittest
from trie import Trie, Node

class TestTrie(unittest.TestCase):
    @classmethod
    def setUp(self) -> None:
        self.trie = Trie()
        self.trie.add('boo', 1)
        self.trie.add('baa', 2)
        self.trie.add('bop', 3)
        self.trie.add('ben le', 4)
        self.trie


    def test_one_prefix(self):
        words = self.trie.find_words_with_prefix('b')
        print(words)
        self.assertEqual(len(words), 4)

    def test_exact_word(self):
        words = self.trie.find_words_with_prefix('baa')
        print(words)
        self.assertEqual(1, len(words))

    def test_all_words(self):
        words = self.trie.find_words_with_prefix('')
        print(words)
        self.assertEqual(4, len(words))

    def test_all_characters(self):
        all_chars = ''
        for index in range (32, 65):
            all_chars += chr(index)
        for index in range (91, 123):
            all_chars += chr(index)
        self.trie.add(all_chars, 0)
        words = self.trie.find_words_with_prefix(all_chars[0:-1])
        print(words)
        self.assertEqual(len(words), 1)
    
    def test_get_objs(self):
        objs = self.trie.find_objs_with_prefix('b')
        print(objs)
        self.assertEqual(len(objs), 4)

if __name__ == '__main__':
    unittest.main()