# only basic latin characters: https://en.wikipedia.org/wiki/List_of_Unicode_characters
# unicode 32 - 64, 91 - 122 (65 total)
total_chars = 65

def char_to_array_index (char:str):
        unicode = ord(char)
        if (32 <= unicode <= 64) :
            return unicode - 32
        elif (91 <= unicode <= 122) :
            return unicode - 91 + 33
        else :
            return None

def array_index_to_char (index:int) :
    if (0 <= index <= 32) : 
        return chr(index + 32)
    elif (33 <= index <= total_chars) :
        return chr(index + 58)
    else :
        return None


class Node:
    def __init__(self, char: str):
        self.children = [None] * total_chars
        self.word_finished = False
        self.char = char
        self.obj_id = None # id in database

    def list_child_words(self) :
        # returns all words that are children of this node (not including the letter created by this node)
        result = [''] if self.word_finished else []

        for index in range(total_chars):
            child = self.children[index]
            char = array_index_to_char(index)
            if child is not None:
                grandchildren = child.list_child_words()
                for grandchild in grandchildren :
                    result.append(char + grandchild)
        return result

    def list_child_objs(self):
        result = set([self.obj_id]) if self.word_finished else set()
        for child in self.children:
            if child is not None:
                grandchildren = child.list_child_objs()
                result = result.union(grandchildren)
        return result


class Trie:
    def __init__(self):
        self.root = Node('')

    def add(self, word:str, obj_id: int):
        word = word.lower()
        node = self.root
        for char in word:
            array_index = char_to_array_index(char)
            if array_index is not None:
                if node.children[array_index] is None :
                    new_node = Node(char)
                    node.children[array_index] = new_node
                node = node.children[array_index]
        node.word_finished = True
        node.obj_id = obj_id

    def remove(self, word:str):
        word = word.lower()
        node = self.root
        for char in word:
            array_index = char_to_array_index(char)
            if array_index is not None:
                node = node.children[array_index]
            else :
                return
        node.word_finished = False
        node.obj_id = None

    def find_words_with_prefix(self, prefix:str): 
        # returns list of words that have this prefix
        node = self.root
        for char in prefix:
            array_index = char_to_array_index(char)
            if array_index is None or node.children[array_index] is None:
                return []
            else :
                node = node.children[array_index]
        suffixes = node.list_child_words()
        return list(map(lambda suffix : prefix + suffix, suffixes))
    
    def find_objs_with_prefix(self, prefix: str):
        node = self.root
        for char in prefix:
            array_index = char_to_array_index(char)
            if array_index is None or node.children[array_index] is None:
                return {}
            else :
                node = node.children[array_index]
        return node.list_child_objs()



    