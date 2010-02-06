# This my the class-based (as opposed to dict-based) trie implementation
# it uses significantly more memory than the other
class TrieNode(object):
	def __init__(self, char, terminal = False):
		self.char = char
		self.children = []

class Trie(object):
	def __init__(self, filename = None):
		self.root = TrieNode('')
		self.suggestions = []

	def add_from_list(self, list):
		for word in list:
			self.add_word(word)

	def add_from_file(self, filename, lowercase = False):
		file = open(filename, 'r')
		for line in file:
			line = line.rstrip()
			if lowercase:
				line = line.lower()
			self.add_word(line)
		file.close()

	def add_word(self, word):
		current_node = self.root
		for char in word:
			# TODO: Account for whitespace nodes
			char_present = False
			for child in current_node.children:
				# If a key is present, set the current node and continue
				if child.char == char:
					char_present = True
					current_node = child
			# If no key is found, create a node and update 
			# the current node 
			if not char_present:
				node = TrieNode(char)
				node.char = char
				current_node.children.append(node)
				current_node = current_node.children[len(current_node.children) - 1]
		# Append empty node for each full word
		# Without this, subsets (big from [[big]ger,est]) will not be found
		current_node.children.append(TrieNode(''))

	def search(self, prefix):
		self.suggestions = [] # Reset suggestions
		current_node = self.root
		prefix = prefix.rstrip().strip().lower()
		
		for char in prefix:
			char_present = False
			for child in current_node.children:
				if child.char == char:
					char_present = True
					current_node = child
			if not char_present:
				current_node = None
				break
		if current_node:
			self.build_suggestions(prefix, current_node)
		return self.suggestions
	
	def build_suggestions(self, prefix, node):
		self.build_words(prefix, node)
		return self.suggestions

	def build_words(self, prefix, node):
		# Loop through nodes
		for child in node.children:
			word = prefix + child.char
			# Recurse if node has children
			if len(child.children):
				self.build_words(word, child)
			else:
				self.suggestions.append(word)
