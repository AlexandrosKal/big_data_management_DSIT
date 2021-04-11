import trie as tr

my_trie = tr.TrieNode()

my_trie.put('ee', 'value1')
my_trie.put('po', 'value2')
my_trie.put('e', 'value3')
my_trie.put('e', {'key1': {'12': 1}})
my_trie.print_trie()

print('DELETE e')
#print(my_trie.delete('e'))
print("DONE")

print(my_trie.query('e', ['key1', '12', '2']))


