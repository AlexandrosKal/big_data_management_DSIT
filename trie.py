# implementation of the trie data structure
class TrieNode:

    def __init__(self):
        self.children = {}
        self.char = '*'
        self.value = None
        self.end = False

    def put(self, key, value):
        if len(key) == 0:
            print("Error: Empty Key")
            return False
        head = key[0]
        if head in self.children:
            current_node = self.children[head]
        else:
            current_node = TrieNode()
            current_node.char = head
            self.children[head] = current_node
        if len(key) > 1:
            tail = key[1:]
            current_node.put(tail, value)
        else:
            current_node.value = value
            current_node.end = True
        return True

    def get(self, key):
        if len(key) == 0:
            print("Error: Empty Key")
            return None
        head = key[0]
        if head in self.children:
            current_node = self.children[head]
        else:
            return None
        val = None
        if len(key) > 1:
            tail = key[1:]
            val = current_node.get(tail)
        elif current_node.end:
            val = current_node.value
        return val

    def query(self, top_lvl_key, keys):
        if len(top_lvl_key) == 0:
            print('Error: empty top level key')
            return None
        val = self.get(top_lvl_key)
        if val is None:
            return None
        if len(keys) == 0:
            return val
        else:
            print(val)
            print(f'KEYS: {keys}')
            for key in keys:
                if len(key) == 0:
                    print('Error: query secondary key path contains empty key')
                    return None
                try:
                    val = val.get(key)
                except (AttributeError, TypeError):
                    return None

            return val

    def delete(self, key):
        if len(key) == 0:
            print("Error: Empty Key")
            return None
        head = key[0]
        if head in self.children:
            current_node = self.children[head]
        else:
            return None
        val = None
        if len(key) > 1:
            tail = key[1:]
            val = current_node.delete(tail)
        elif current_node.end:
            current_node.end = False
            val = current_node.value
            current_node.value = None

        return val

    # print functions used for debugging
    def print_node(self, indent=0):
        prefix = ''
        for i in range(0, indent):
            prefix += '--'
        print(f'{prefix}Node {self.char}')
        print(f'{prefix}Final node: {self.end}, Node value: {self.value}')
        print(f'{prefix}Node children: {list(self.children.keys())}')
        return

    def print_trie(self, level=0):
        self.print_node(level)
        for c in self.children:
            self.children[c].print_trie(level+1)
        return
